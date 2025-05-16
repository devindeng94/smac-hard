import torch as th
import torch.nn as nn
import torch.nn.functional as F
from .vae import VAE
import pdb

class MAPCAgent(nn.Module):

    def __init__(self, input_shape, args):

        super(MAPCAgent, self).__init__()

        self.args = args

        # Policy Encoder
        self.policy_fc1 = nn.Linear(args.n_policies, args.policy_embed_dim)
        self.policy_fc2 = nn.Linear(args.policy_embed_dim, args.policy_embed_dim)

        # Opponent Strategy
        self.oppo = OppoStrategy(input_shape, args)

        # Agent
        self.agent_fc1 = nn.Linear(input_shape + args.policy_embed_dim, args.rnn_hidden_dim)
        self.agent_rnn = nn.GRUCell(args.rnn_hidden_dim, args.rnn_hidden_dim)
        self.agent_fc2 = nn.Linear(args.rnn_hidden_dim, args.n_actions)

    def init_hidden_oppo(self):
        return self.oppo.oppo_fc1.weight.new(1, self.args.oppo_hidden_dim).zero_()
    
    def init_hidden_agent(self):
        return self.agent_fc1.weight.new(1, self.args.rnn_hidden_dim).zero_()
    

    def forward(self, inputs, hidden_oppo, hidden_agent, test_mode=False):

        # inputs [bs, n, input_shape]
        
        if len(inputs.shape) == 2:
            bs = inputs.shape[0] // self.args.n_agents
            n_agents = self.args.n_agents
        else:
        # Policy Encoder
            bs = inputs.shape[0]
            n_agents = self.args.n_agents

        
        policy_one_hot = th.eye(self.args.n_policies, device=inputs.device).unsqueeze(0).expand(bs, -1, -1)
        policy_x = F.relu(self.policy_fc1(policy_one_hot))
        policy_embed = F.tanh(self.policy_fc2(policy_x))    #[bs, n_policy, policy_embed_dim]
        policy_embed = policy_embed.expand(bs, self.args.n_policies, self.args.policy_embed_dim)
        
        # Opponent Strategy
        emb, vae_input, vae_loss = self.oppo(inputs, hidden_oppo)
        
        # emb: [bs * n * policy_embed_dim]

        emb = emb.reshape(-1, n_agents, self.args.policy_embed_dim)

        policy_prob_logit = th.bmm(emb, policy_embed.permute(0, 2, 1))  #[bs, n , n_policy]

        if test_mode:
            prob_max = th.max(policy_prob_logit, dim=-1, keepdim=True)[1]
            policy_prob = th.zeros_like(policy_prob_logit).scatter_(-1, prob_max, 1)
        else:
            if self.args.sft_way == "softmax":
                policy_prob = F.softmax(policy_prob_logit, dim=-1) # [bs, n_agents, n_subtasks]
            elif self.args.sft_way == "gumbel_softmax":
                policy_prob = F.gumbel_softmax(policy_prob_logit, hard=True, dim=-1)
                
        policy_prob = policy_prob.reshape(bs, n_agents, self.args.n_policies) # [bs*n_agents, 1, n_subtasks]

        # Agent
        inputs = inputs.reshape(bs, n_agents, -1)
        agent_input = th.cat((inputs, policy_prob @ policy_embed), -1)
        agent_x = F.relu(self.agent_fc1(agent_input))
        agent_x = agent_x.reshape(bs * n_agents, -1)
        h_hidden_agent = hidden_agent.reshape(-1, self.args.rnn_hidden_dim)
        h_agent_embed = self.agent_rnn(agent_x, h_hidden_agent).reshape(bs, n_agents, -1)
        
        
        agent_q = self.agent_fc2(h_agent_embed)
              # q,      h_oppo     h_agent
        return agent_q, vae_input, h_agent_embed, policy_prob_logit, policy_prob, policy_embed, vae_loss


class OppoStrategy(nn.Module):

    def __init__(self, input_shape, args):

        super(OppoStrategy, self).__init__()

        self.args = args
        self.oppo_fc1 = nn.Linear(input_shape, args.oppo_hidden_dim)
        self.oppo_rnn = nn.GRUCell(args.oppo_hidden_dim, args.oppo_hidden_dim)

        self.vae = VAE(args)

    def forward(self, inputs, hidden_oppo):

        oppo_x = F.relu(self.oppo_fc1(inputs))  
        h_hidden_oppo = hidden_oppo.reshape(-1, self.args.oppo_hidden_dim)  
        vae_input = self.oppo_rnn(oppo_x, h_hidden_oppo)    #[n, oppo_hidden_dim]
        _, emb, _, _, _, vae_loss = self.vae(vae_input)
        return emb, vae_input, vae_loss