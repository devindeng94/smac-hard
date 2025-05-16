import copy
from components.episode_buffer import EpisodeBatch
from modules.mixers.vdn import VDNMixer
from modules.mixers.qmix import QMixer
import torch as th
from torch.optim import RMSprop
import torch.nn.functional as F

class LDSALearner:
    def __init__(self, mac, scheme, logger, args):
        self.args = args
        self.mac = mac
        self.logger = logger

        self.params = list(mac.parameters())

        self.last_target_update_episode = 0

        self.mixer = None
        if args.mixer is not None:
            if args.mixer == "vdn":
                self.mixer = VDNMixer()
            elif args.mixer == "qmix":
                self.mixer = QMixer(args)
            else:
                raise ValueError("Mixer {} not recognised.".format(args.mixer))
            self.params += list(self.mixer.parameters())
            self.target_mixer = copy.deepcopy(self.mixer)

        self.optimiser = RMSprop(params=self.params, lr=args.lr, alpha=args.optim_alpha, eps=args.optim_eps)

        # a little wasteful to deepcopy (e.g. duplicates action selector), but should work for any MAC
        self.target_mac = copy.deepcopy(mac)

        self.log_stats_t = -self.args.learner_log_interval - 1

    def train(self, batch: EpisodeBatch, t_env: int, episode_num: int):
        # Get the relevant quantities
        rewards = batch["reward"][:, :-1]  # [bs, eplen, 1]
        actions = batch["actions"][:, :-1] # [bs, eplen, n_agents, 1]
        terminated = batch["terminated"][:, :-1].float() # [bs, eplen, 1]
        mask = batch["filled"][:, :-1].float() # [bs, eplen, 1]
        mask[:, 1:] = mask[:, 1:] * (1 - terminated[:, :-1])
        avail_actions = batch["avail_actions"] # [bs, eplen+1, n_agents, n_actions]

        # Calculate estimated Q-Values
        mac_out = []
        subtask_prob_logits = []
        subtask_prob_logits_last = []
        subtask_embeds = []
        self.mac.init_hidden(batch.batch_size)
        for t in range(batch.max_seq_length):
            agent_outs, subtask_prob_logit, subtask_embed = self.mac.forward(batch, t=t)
            mac_out.append(agent_outs)
            if t > 0:
                subtask_prob_logits.append(subtask_prob_logit)
            if t < batch.max_seq_length - 1:
                subtask_prob_logits_last.append(subtask_prob_logit)
                subtask_embeds.append(subtask_embed)
        mac_out = th.stack(mac_out, dim=1)  # Concat over time [bs, eplen+1, n_agents, n_actions]
        subtask_prob_logits = th.stack(subtask_prob_logits, dim=1) # [bs, eplen, n_agents, n_subtasks]
        subtask_prob_logits_last = th.stack(subtask_prob_logits_last, dim=1) # [bs, eplen, n_agents, n_subtasks]
        subtask_embeds = th.stack(subtask_embeds, dim=1) # [bs, eplen, n_subtasks, embed_dim]

        # Pick the Q-Values for the actions taken by each agent
        chosen_action_qvals = th.gather(mac_out[:, :-1], dim=3, index=actions).squeeze(3)  # Remove the last dim [bs, eplen, n_agents]

        # Calculate the Q-Values necessary for the target
        target_mac_out = []
        self.target_mac.init_hidden(batch.batch_size)
        for t in range(batch.max_seq_length):
            target_agent_outs, _, _ = self.target_mac.forward(batch, t=t)
            target_mac_out.append(target_agent_outs)

        # We don't need the first timesteps Q-Value estimate for calculating targets
        target_mac_out = th.stack(target_mac_out[1:], dim=1)  # Concat across time

        # Mask out unavailable actions
        target_mac_out[avail_actions[:, 1:] == 0] = -9999999

        # Max over target Q-Values
        if self.args.double_q:
            # Get actions that maximise live Q (for double q-learning)
            mac_out_detach = mac_out.clone().detach()
            mac_out_detach[avail_actions == 0] = -9999999
            cur_max_actions = mac_out_detach[:, 1:].max(dim=3, keepdim=True)[1]
            target_max_qvals = th.gather(target_mac_out, 3, cur_max_actions).squeeze(3)
        else:
            target_max_qvals = target_mac_out.max(dim=3)[0]

        # Mix
        if self.mixer is not None:
            chosen_action_qvals = self.mixer(chosen_action_qvals, batch["state"][:, :-1]) # [bs, eplen, 1]
            target_max_qvals = self.target_mixer(target_max_qvals, batch["state"][:, 1:])

        # Calculate 1-step Q-Learning targets
        targets = rewards + self.args.gamma * (1 - terminated) * target_max_qvals

        # Td-error
        td_error = (chosen_action_qvals - targets.detach())
        mask = mask.expand_as(td_error)
        # 0-out the targets that came from padded data
        masked_td_error = td_error * mask
        # Normal L2 loss, take mean over actual data
        td_loss = (masked_td_error ** 2).sum() / mask.sum()

        # MSE loss of representation between two different subtasks
        subtask_embeds1 = subtask_embeds.unsqueeze(3) # [bs, eplen, n_subtasks, 1, embed_dim]
        subtask_embeds2 = subtask_embeds.unsqueeze(2).clone().detach() # [bs, eplen, 1, n_subtasks, embed_dim]
        subtask_dis = ((subtask_embeds1 - subtask_embeds2) ** 2).sum(dim=4, keepdim=True) # [bs, eplen, n_subtasks, n_subtasks, 1]
        subtask_dis = subtask_dis.sum([4, 3, 2]).unsqueeze(-1) # [bs, eplen, 1]
        subtask_dis = subtask_dis / (self.args.n_subtasks * (self.args.n_subtasks - 1)) # [bs, eplen, 1]
        masked_subtask_dis = subtask_dis * mask
        subtask_dis_loss = masked_subtask_dis.sum() / mask.sum()

        # KL loss of subtask prob between two adjacent frames
        subtask_probs = F.softmax(subtask_prob_logits, dim=-1) # [bs, eplen, n_agents, n_subtasks]
        subtask_probs_last = F.softmax(subtask_prob_logits_last, dim=-1) # [bs, eplen, n_agents, n_subtasks]
        subtask_prob_kl = th.sum(subtask_probs_last.detach() * ( - th.log(subtask_probs + 1e-8)), dim=[3, 2]).unsqueeze(-1) / self.args.n_agents #[bs, eplen, 1]
        mask_ = mask[:, 1:] # [bs, eplen-1, 1]
        mask_ = th.cat([mask_, th.zeros(mask_.shape[0], 1, 1, device=mask_.device)], dim=1) # [bs, eplen, 1]
        subtask_prob_kl_loss = subtask_prob_kl.sum() / mask_.sum()

        loss = td_loss - self.args.lambda_subtask_repr * subtask_dis_loss + self.args.lambda_subtask_prob * subtask_prob_kl_loss

        # Optimise
        self.optimiser.zero_grad()
        loss.backward()
        grad_norm = th.nn.utils.clip_grad_norm_(self.params, self.args.grad_norm_clip)
        self.optimiser.step()

        if (episode_num - self.last_target_update_episode) / self.args.target_update_interval >= 1.0:
            self._update_targets()
            self.last_target_update_episode = episode_num

        if t_env - self.log_stats_t >= self.args.learner_log_interval:
            self.logger.log_stat("loss", loss.item(), t_env)
            self.logger.log_stat("td_loss", td_loss.item(), t_env)
            self.logger.log_stat("subtask_dis_loss", subtask_dis_loss.item(), t_env)
            self.logger.log_stat("subtask_prob_kl_loss", subtask_prob_kl_loss.item(), t_env)
            #self.logger.log_stat("grad_norm", grad_norm.item(), t_env)
            mask_elems = mask.sum().item()
            self.logger.log_stat("td_error_abs", (masked_td_error.abs().sum().item()/mask_elems), t_env)
            self.logger.log_stat("q_taken_mean", (chosen_action_qvals * mask).sum().item()/(mask_elems * self.args.n_agents), t_env)
            self.logger.log_stat("target_mean", (targets * mask).sum().item()/(mask_elems * self.args.n_agents), t_env)
            self.log_stats_t = t_env

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
