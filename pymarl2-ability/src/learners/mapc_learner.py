import copy
from components.episode_buffer import EpisodeBatch
from modules.mixers.nmix import Mixer
from modules.mixers.qmix_policy import QMixerPolicy
from utils.rl_utils import build_td_lambda_targets, build_q_lambda_targets
import torch as th
from torch.optim import RMSprop, Adam
import numpy as np
import torch.nn.functional as F
import pdb

from utils.th_utils import get_parameters_num

class MAPCLearner:
    def __init__(self, mac, scheme, logger, args):
        self.args = args
        self.mac = mac
        self.logger = logger
        
        self.last_target_update_episode = 0
        self.device = th.device('cuda' if args.use_cuda  else 'cpu')
        self.params = list(mac.parameters())

        
        if args.mixer == "qmix_policy":
            self.mixer = QMixerPolicy(args)
        elif args.mixer == 'qmix':
            self.mixer = Mixer(args)
        else:
            raise "mixer error"
        
        self.target_mixer = copy.deepcopy(self.mixer)
        self.params += list(self.mixer.parameters())

        print('Mixer Size: ')
        print(get_parameters_num(self.mixer.parameters()))

        if self.args.optimizer == 'adam':
            self.optimiser = Adam(params=self.params,  lr=args.lr, weight_decay=getattr(args, "weight_decay", 0))
        else:
            self.optimiser = RMSprop(params=self.params, lr=args.lr, alpha=args.optim_alpha, eps=args.optim_eps)

        # a little wasteful to deepcopy (e.g. duplicates action selector), but should work for any MAC
        self.target_mac = copy.deepcopy(mac)
        self.log_stats_t = -self.args.learner_log_interval - 1

        # priority replay
        self.use_per = getattr(self.args, 'use_per', False)
        self.return_priority = getattr(self.args, "return_priority", False)
        if self.use_per:
            self.priority_max = float('-inf')
            self.priority_min = float('inf')

        
    def train(self, batch: EpisodeBatch, t_env: int, episode_num: int, per_weight=None):
        # Get the relevant quantities
        rewards = batch["reward"][:, :-1]
        actions = batch["actions"][:, :-1]
        terminated = batch["terminated"][:, :-1].float()
        mask = batch["filled"][:, :-1].float()
        mask[:, 1:] = mask[:, 1:] * (1 - terminated[:, :-1])
        avail_actions = batch["avail_actions"]
        
        # Calculate estimated Q-Values
        self.mac.agent.train()

        mac_out = []
        policy_prob_logits = []
        policy_prob_logits_pre = []
        policy_probs = []
        policy_embeds = []
        vae_losses = []

        self.mac.init_hidden(batch.batch_size)
        for t in range(batch.max_seq_length):
            agent_outs, policy_prob_logit, policy_prob, policy_embed, vae_loss = self.mac.forward(batch, t=t)
            mac_out.append(agent_outs)
            policy_probs.append(policy_prob)
            vae_losses.append(vae_loss)
            if t > 0:
                policy_prob_logits.append(policy_prob_logit)
            if t < batch.max_seq_length - 1:
                policy_prob_logits_pre.append(policy_prob_logit)
                policy_embeds.append(policy_embed)


        mac_out = th.stack(mac_out, dim=1)  # Concat over time
        policy_prob_logits = th.stack(policy_prob_logits, dim=1)
        policy_prob_logits_pre = th.stack(policy_prob_logits_pre, dim=1)
        policy_probs = th.stack(policy_probs, dim=1)
        policy_embeds = th.stack(policy_embeds, dim=1)
        vae_losses = th.stack(vae_losses, dim=0)

        # Pick the Q-Values for the actions taken by each agent
        #[bs, T, n, a]
        chosen_action_qvals = th.gather(mac_out[:, :-1], dim=3, index=actions).squeeze(3)  # Remove the last dim

        # Calculate the Q-Values necessary for the target
        with th.no_grad():
            self.target_mac.agent.train()
            target_mac_out = []
            target_policy_probs = []

            self.target_mac.init_hidden(batch.batch_size)
            for t in range(batch.max_seq_length):
                target_agent_outs, _, target_policy_prob, _, _ = self.target_mac.forward(batch, t=t)
                target_mac_out.append(target_agent_outs)
                target_policy_probs.append(target_policy_prob)

            target_mac_out = th.stack(target_mac_out, dim=1)  # Concat across time
            target_policy_probs = th.stack(target_policy_probs, dim=1)

            # Max over target Q-Values/ Double q learning
            mac_out_detach = mac_out.clone().detach()
            mac_out_detach[avail_actions == 0] = -9999999
            cur_max_actions = mac_out_detach.max(dim=3, keepdim=True)[1]
            target_max_qvals = th.gather(target_mac_out, 3, cur_max_actions).squeeze(3)
            
            if self.args.mixer == 'qmix_policy':
                target_policy_shape = target_policy_probs.shape
                target_policy_probs = target_policy_probs.reshape(target_policy_shape[0], target_policy_shape[1], -1)          
                target_max_qvals = self.target_mixer(target_max_qvals, th.cat((batch["state"], target_policy_probs.detach()), -1))
            elif self.args.mixer == 'qmix':
                target_max_qvals = self.target_mixer(target_max_qvals, batch["state"])


            if getattr(self.args, 'q_lambda', False):
                qvals = th.gather(target_mac_out, 3, batch["actions"]).squeeze(3)
                qvals = self.target_mixer(qvals, batch["state"])

                targets = build_q_lambda_targets(rewards, terminated, mask, target_max_qvals, qvals,
                                    self.args.gamma, self.args.td_lambda)
            else:
                targets = build_td_lambda_targets(rewards, terminated, mask, target_max_qvals, 
                                                    self.args.n_agents, self.args.gamma, self.args.td_lambda)

        # Mixer
        if self.args.mixer == 'qmix_policy':
            policy_shape = policy_probs.shape
            policy_probs = policy_probs.reshape(policy_shape[0], policy_shape[1], -1)         
            chosen_action_qvals = self.mixer(chosen_action_qvals, th.cat((batch["state"], policy_probs.detach()), -1)[:, :-1])
        elif self.args.mixer == 'qmix':
            chosen_action_qvals = self.mixer(chosen_action_qvals, batch["state"][:, :-1])


        td_error = (chosen_action_qvals - targets.detach())
        td_error2 = 0.5 * td_error.pow(2)

        mask = mask.expand_as(td_error2)
        masked_td_error = td_error2 * mask

        # important sampling for PER
        if self.use_per:
            per_weight = th.from_numpy(per_weight).unsqueeze(-1).to(device=self.device)
            masked_td_error = masked_td_error.sum(1) * per_weight

        td_loss = masked_td_error.sum() / mask.sum()

        # MSE loss of representation between two different subtasks
        policy_embeds1 = policy_embeds.unsqueeze(3) # [bs, eplen, n_subtasks, 1, embed_dim]
        policy_embeds2 = policy_embeds.unsqueeze(2).clone().detach() # [bs, eplen, 1, n_subtasks, embed_dim]
        policy_dis = ((policy_embeds1 - policy_embeds2) ** 2).sum(dim=4, keepdim=True) # [bs, eplen, n_subtasks, n_subtasks, 1]
        policy_dis = policy_dis.sum([4, 3, 2]).unsqueeze(-1) # [bs, eplen, 1]
        policy_dis = policy_dis / (self.args.n_policies * (self.args.n_policies - 1)) # [bs, eplen, 1]
        masked_policy_dis = policy_dis * mask
        policy_dis_loss = masked_policy_dis.sum() / mask.sum()


        policy_prob_dist = F.softmax(policy_prob_logits, dim=-1) # [bs, eplen, n_agents, n_subtasks] # Target
        policy_prob_dist_pre = F.softmax(policy_prob_logits_pre, dim=-1) # [bs, eplen, n_agents, n_subtasks]    # Input
        '''
        log_policy_prob_dist_pre = th.log(policy_prob_dist_pre)
        kl_loss_criteria = th.nn.KLDivLoss(reduction='none')
        kl_loss = kl_loss_criteria(log_policy_prob_dist_pre, policy_prob_dist)
        masked_kl_loss = kl_loss.sum(dim=[-1,-2]).unsqueeze(-1) * mask
        kl_loss = masked_kl_loss.sum() / mask.sum()
        '''
        policy_prob_kl = th.sum(policy_prob_dist_pre.detach() * ( - th.log(policy_prob_dist + 1e-8)), dim=[3,2]).unsqueeze(-1) / self.args.n_agents #[bs, eplen, 1]
        mask_ = mask[:, 1:] # [bs, eplen-1, 1]
        mask_ = th.cat([mask_, th.zeros(mask_.shape[0], 1, 1, device=mask_.device)], dim=1) # [bs, eplen, 1]
        kl_loss = policy_prob_kl.sum() / mask_.sum()
        
        #loss = td_loss - self.args.lambda_subtask_repr * policy_dis_loss + self.args.lambda_subtask_prob * kl_loss + vae_losses.sum()/vae_losses.shape[0]
        loss = td_loss - self.args.lambda_subtask_repr * policy_dis_loss + vae_losses.sum()/vae_losses.shape[0]
        # Optimise
        self.optimiser.zero_grad()
        loss.backward()
        grad_norm = th.nn.utils.clip_grad_norm_(self.params, self.args.grad_norm_clip)
        self.optimiser.step()

        #self.target_mac.load_oppo(self.mac)

        if (episode_num - self.last_target_update_episode) / self.args.target_update_interval >= 1.0:
            self._update_targets()
            self.last_target_update_episode = episode_num

        if t_env - self.log_stats_t >= self.args.learner_log_interval:
            self.logger.log_stat("loss", loss.item(), t_env)
            self.logger.log_stat("td_loss", td_loss.item(), t_env)
            self.logger.log_stat("policy_dis_loss", policy_dis_loss.item(), t_env)
            self.logger.log_stat("policy_prob_kl_loss", kl_loss.item(), t_env)
            #self.logger.log_stat("grad_norm", grad_norm.item(), t_env)
            mask_elems = mask.sum().item()
            self.logger.log_stat("td_error_abs", (masked_td_error.abs().sum().item()/mask_elems), t_env)
            self.logger.log_stat("q_taken_mean", (chosen_action_qvals * mask).sum().item()/(mask_elems * self.args.n_agents), t_env)
            self.logger.log_stat("target_mean", (targets * mask).sum().item()/(mask_elems * self.args.n_agents), t_env)
            self.logger.log_stat("vae_loss", (vae_losses.sum()/vae_losses.shape[0]).item(), t_env)
            self.log_stats_t = t_env
            

        # return info
        info = {}
        # calculate priority
        if self.use_per:
            if self.return_priority:
                info["td_errors_abs"] = rewards.sum(1).detach().to('cpu')
                # normalize to [0, 1]
                self.priority_max = max(th.max(info["td_errors_abs"]).item(), self.priority_max)
                self.priority_min = min(th.min(info["td_errors_abs"]).item(), self.priority_min)
                info["td_errors_abs"] = (info["td_errors_abs"] - self.priority_min) \
                                / (self.priority_max - self.priority_min + 1e-5)
            else:
                info["td_errors_abs"] = ((td_error.abs() * mask).sum(1) \
                                / th.sqrt(mask.sum(1))).detach().to('cpu')
        return info

    def _update_targets(self):
        self.target_mac.load_state(self.mac)
        if self.mixer is not None:
            self.target_mixer.load_state_dict(self.mixer.state_dict())
        self.logger.console_logger.info("Updated target network")

    def cuda(self):
        self.mac.cuda()
        self.target_mac.cuda()
        if self.mixer is not None:
            self.mixer.cuda()
            self.target_mixer.cuda()
            
    def save_models(self, path):
        self.mac.save_models(path)
        if self.mixer is not None:
            th.save(self.mixer.state_dict(), "{}/mixer.th".format(path))
        th.save(self.optimiser.state_dict(), "{}/opt.th".format(path))

    def load_models(self, path):
        self.mac.load_models(path)
        # Not quite right but I don't want to save target networks
        self.target_mac.load_models(path)
        if self.mixer is not None:
            self.mixer.load_state_dict(th.load("{}/mixer.th".format(path), map_location=lambda storage, loc: storage))
        self.optimiser.load_state_dict(th.load("{}/opt.th".format(path), map_location=lambda storage, loc: storage))
