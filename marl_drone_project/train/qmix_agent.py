from importlib.resources import path

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

# ------------------------
# Individual Agent Network
# ------------------------
class AgentQNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, action_size)
        )

    def forward(self, x):
        return self.net(x)


# ------------------------
# Mixing Network (Improved QMIX)
# ------------------------
class MixingNetwork(nn.Module):
    def __init__(self, n_agents, global_state_size):
        super().__init__()

        input_size = n_agents + global_state_size

        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, agent_qs, global_state):
        x = torch.cat([agent_qs, global_state], dim=1)
        return self.net(x)


# ------------------------
# Replay Buffer
# ------------------------
class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, data):
        self.buffer.append(data)

    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)


# ------------------------
# QMIX Agent
# ------------------------
class QMIXAgent:
    def __init__(self, n_agents, state_size, action_size):

        self.n_agents = n_agents
        self.action_size = action_size
        self.global_state_size = state_size * n_agents

        # agent networks
        self.agents = [AgentQNetwork(state_size, action_size) for _ in range(n_agents)]
        self.target_agents = [AgentQNetwork(state_size, action_size) for _ in range(n_agents)]

        # mixer
        self.mixer = MixingNetwork(n_agents, self.global_state_size)
        self.target_mixer = MixingNetwork(n_agents, self.global_state_size)

        # target copy
        for i in range(n_agents):
            self.target_agents[i].load_state_dict(self.agents[i].state_dict())

        self.target_mixer.load_state_dict(self.mixer.state_dict())

        # optimizer
        self.optimizer = optim.Adam(
            list(self.mixer.parameters()) +
            [p for agent in self.agents for p in agent.parameters()],
            lr=0.001
        )

        # replay memory
        self.memory = ReplayBuffer()

        # hyperparameters
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_decay = 0.9997
        self.epsilon_min = 0.2

        self.batch_size = 32

        # target update
        self.train_step = 0
        self.target_update = 50

    # ------------------------
    # Action Selection
    # ------------------------
    def select_actions(self, states):
        actions = []

        for i in range(self.n_agents):
            if random.random() < self.epsilon:
                actions.append(random.randint(0, self.action_size - 1))
            else:
                state = torch.FloatTensor(states[i])
                q = self.agents[i](state)
                actions.append(torch.argmax(q).item())

        return actions

    # ------------------------
    # Store Transition
    # ------------------------
    def store(self, transition):
        self.memory.push(transition)

    # ------------------------
    # Train
    # ------------------------
    def train(self):
        if len(self.memory) < self.batch_size:
            return

        batch = self.memory.sample(self.batch_size)

        loss_total = 0

        for transition in batch[:16]:
            states, actions, reward, next_states, done = transition

            agent_qs = []
            next_agent_qs = []

            for i in range(self.n_agents):
                s = torch.FloatTensor(states[i])
                ns = torch.FloatTensor(next_states[i])

                q = self.agents[i](s)[actions[i]]
                next_q = torch.max(self.target_agents[i](ns))

                agent_qs.append(q)
                next_agent_qs.append(next_q)

            agent_qs = torch.stack(agent_qs).unsqueeze(0)
            next_agent_qs = torch.stack(next_agent_qs).unsqueeze(0)

            global_state = torch.FloatTensor(np.concatenate(states)).unsqueeze(0)
            next_global_state = torch.FloatTensor(np.concatenate(next_states)).unsqueeze(0)

            q_total = self.mixer(agent_qs, global_state)
            next_q_total = self.target_mixer(next_agent_qs, next_global_state)

            target = reward + (1 - done) * self.gamma * next_q_total

            loss = nn.functional.smooth_l1_loss(q_total, target.detach())
            loss_total += loss

        loss_total = loss_total.mean()

        self.optimizer.zero_grad()
        loss_total.backward()
        torch.nn.utils.clip_grad_norm_(
            list(self.mixer.parameters()) +
            [p for agent in self.agents for p in agent.parameters()],
            10
        )           
        self.optimizer.step()

        # target update
        self.train_step += 1

        if self.train_step % self.target_update == 0:
            for i in range(self.n_agents):
                self.target_agents[i].load_state_dict(self.agents[i].state_dict())

            self.target_mixer.load_state_dict(self.mixer.state_dict())

    
    def load_model(self, path):
        checkpoint = torch.load(path)

        for i in range(self.n_agents):
            self.agents[i].load_state_dict(checkpoint["agents"][i])
            self.target_agents[i].load_state_dict(checkpoint["target_agents"][i])

        self.mixer.load_state_dict(checkpoint["mixer"])
        self.target_mixer.load_state_dict(checkpoint["target_mixer"])

        self.epsilon = checkpoint["epsilon"]

        print("✅ Model loaded successfully") 