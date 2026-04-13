import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from utils.replay_buffer import ReplayBuffer


class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()

        self.net = nn.Sequential(
            nn.Linear(state_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_size)
        )

    def forward(self, x):
        return self.net(x)


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.model = DQN(state_size, action_size)
        self.target_model = DQN(state_size, action_size)

        self.target_model.load_state_dict(self.model.state_dict())

        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()

        self.memory = ReplayBuffer(10000)

        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.05

        self.batch_size = 64
        self.action_size = action_size

        self.update_target_steps = 100
        self.step_count = 0

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)

        state = torch.FloatTensor(state)
        with torch.no_grad():
            q_values = self.model(state)

        return torch.argmax(q_values).item()

    def store(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)

    def train(self):
        if len(self.memory) < self.batch_size:
            return

        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)

        states = torch.FloatTensor(states)
        next_states = torch.FloatTensor(next_states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        dones = torch.FloatTensor(dones)

        q_values = self.model(states)
        next_q_values = self.target_model(next_states)

        q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
        next_q_value = torch.max(next_q_values, dim=1)[0]

        target = rewards + (1 - dones) * self.gamma * next_q_value

        loss = self.loss_fn(q_value, target.detach())

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # epsilon decay
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # update target network
        self.step_count += 1
        if self.step_count % self.update_target_steps == 0:
            self.target_model.load_state_dict(self.model.state_dict())