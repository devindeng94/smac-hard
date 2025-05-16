import torch as th
import torch.nn as nn
import torch.nn.functional as F
import pdb

class LDSAAgent(nn.Module):
    def __init__(self, input_shape, args):
        super(LDSAAgent, self).__init__()
        self.args = args

        # agent embedding
        self.fc1_agent_embed = nn.Linear(input_shape, args.rnn_hidden_dim) 
        self.rnn_agent_embed = nn.GRUCell(args.rnn_hidden_dim, args.rnn_hidden_dim)
        self.fc2_agent_embed = nn.Linear(args.rnn_hidden_dim, args.agent_subtask_embed_dim)

        # subtask representation
        if args.subtask_repr_layers == 2:
            self.subtask_embed_net = nn.Sequential(nn.Linear(args.n_subtasks, args.agent_subtask_embed_dim),
                                            nn.ReLU(),
                                            nn.Linear(args.agent_subtask_embed_dim, args.agent_subtask_embed_dim))
        elif args.subtask_repr_layers == 1:
            self.subtask_embed_net = nn.Linear(args.n_subtasks, args.agent_subtask_embed_dim, bias=False)
        
        # subtask policy
        self.fc1_subtask_policy = nn.Linear(input_shape, args.rnn_hidden_dim)
        self.rnn_subtask_policy = nn.GRUCell(args.rnn_hidden_dim, args.rnn_hidden_dim)
        if not args.subtask_policy_use_hypernet:
            self.fc2_subtask_policy = nn.Linear(args.rnn_hidden_dim, args.n_subtasks * args.n_actions)
        else:
            self.fc2_w = nn.Linear(args.agent_subtask_embed_dim, args.rnn_hidden_dim * args.n_actions)
            self.fc2_b = nn.Linear(args.agent_subtask_embed_dim, args.n_actions)
        

    def init_hidden_subtask_policy(self):
        # make hidden states on same device as model
        return self.fc1_subtask_policy.weight.new(1, self.args.rnn_hidden_dim).zero_()

    def init_hidden_agent_embed(self):
        # make hidden states on same device as model
        return self.fc1_agent_embed.weight.new(1, self.args.rnn_hidden_dim).zero_()

    def forward(self, inputs, hidden_state_subtask_policy, hidden_state_agent_embed, test_mode=False):
        # inputs: [bs*n_agents, input_shape]
        # subtask_embed_input: [bs*n_subtasks, n_subtasks]
        # agent embedding
        x_agent_embed = F.relu(self.fc1_agent_embed(inputs))
        h_in_agent_embed = hidden_state_agent_embed.reshape(-1, self.args.rnn_hidden_dim)
        h_agent_embed = self.rnn_agent_embed(x_agent_embed, h_in_agent_embed)
        agent_embed = self.fc2_agent_embed(h_agent_embed).reshape(-1, self.args.n_agents, self.args.agent_subtask_embed_dim) # [bs, n_agents, embed_dim]

        # subtask representation
        bs = agent_embed.shape[0]
        subtask_one_hot = th.eye(self.args.n_subtasks, device=inputs.device).unsqueeze(0).expand(bs, -1, -1) # [bs, n_subtasks, n_subtasks]
        subtask_embed = self.subtask_embed_net(subtask_one_hot) # [bs, n_subtasks, embed_dim]
        if self.args.use_tanh:
            subtask_embed = F.tanh(subtask_embed)

        # subtask policy
        x_subtask_policy = F.relu(self.fc1_subtask_policy(inputs))
        h_in_subtask_policy = hidden_state_subtask_policy.reshape(-1, self.args.rnn_hidden_dim)
        h_subtask_policy = self.rnn_subtask_policy(x_subtask_policy, h_in_subtask_policy)  # [bs*n_agents, rnn_hidden_dim]
        if not self.args.subtask_policy_use_hypernet:
            q = self.fc2_subtask_policy(h_subtask_policy).reshape(-1, self.args.n_subtasks, self.args.n_actions) # [bs*n_agents, n_subtasks, n_actions]
        else:
            subtask_embed_detach = subtask_embed.clone().detach()[0]  # [n_subtasks, embed_dim]
            w2 = self.fc2_w(subtask_embed_detach) # [n_subtasks, rnn_hidden_dim*n_actions]
            b2 = self.fc2_b(subtask_embed_detach) # [n_subtasks, n_actions]
            w2 = w2.unsqueeze(0).expand(bs * self.args.n_agents, -1, -1).reshape(-1, self.args.rnn_hidden_dim, self.args.n_actions) # [bs*n_agents*n_subtasks, rnn_hidden_dim, n_actions]
            b2 = b2.unsqueeze(0).expand(bs * self.args.n_agents, -1, -1).reshape(-1, 1, self.args.n_actions) # [bs*n_agents*n_subtasks, 1, n_actions]
            h_subtask_policy_ = h_subtask_policy.unsqueeze(1).expand(-1, self.args.n_subtasks, -1).reshape(-1, 1, self.args.rnn_hidden_dim) # [bs*n_agents*n_subtasks, 1, rnn_hidden_dim]
            q = th.bmm(h_subtask_policy_, w2) + b2
            q = q.reshape(-1, self.args.n_subtasks, self.args.n_actions) # [bs*n_agents, n_subtasks, n_actions]

        # subtask selection
        subtask_prob_logit = th.bmm(agent_embed, subtask_embed.permute(0, 2, 1)) # [bs, n_agents, n_subtasks]
        if self.args.random_sele:
            subtask_prob_logit = th.rand_like(subtask_prob_logit)
        if test_mode and self.args.test_argmax:
            prob_max = th.max(subtask_prob_logit, dim=-1, keepdim=True)[1]
            subtask_prob = th.zeros_like(subtask_prob_logit).scatter_(-1, prob_max, 1)
        else:
            if self.args.sft_way == "softmax":
                subtask_prob = F.softmax(subtask_prob_logit, dim=-1) # [bs, n_agents, n_subtasks]
            elif self.args.sft_way == "gumbel_softmax":
                subtask_prob = F.gumbel_softmax(subtask_prob_logit, hard=True, dim=-1)
        subtask_prob = subtask_prob.reshape(-1, 1, self.args.n_subtasks) # [bs*n_agents, 1, n_subtasks]
        if self.args.evaluate:
            print('chosen_subtask_prob', subtask_prob.reshape(self.args.n_agents, self.args.n_subtasks))
        q = th.bmm(subtask_prob, q).squeeze(1) # [bs*n_agents, n_actions]

        return q, h_subtask_policy, h_agent_embed, subtask_prob_logit, subtask_embed 
        # [bs*n_agents, n_actions], [bs*n_agents, rnn_hidden_dim], [bs*n_agents, rnn_hidden_dim], [bs*n_agents, 1, n_subtasks], [bs, n_subtasks, embed_dim]

