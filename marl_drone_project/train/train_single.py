import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from env.grid_env import GridEnvironment
from train.dqn_agent import DQNAgent

NUM_DRONES = 3

env = GridEnvironment(num_drones=NUM_DRONES)

# reset before accessing state
env.reset()

state_size = len(env.get_agent_state(0))
action_size = 6

agent = DQNAgent(state_size, action_size)

episodes = 300

for episode in range(episodes):
    env.reset()

    total_reward = 0
    done = False
    step = 0

    while not done:
        # get per-agent states
        agent_states = [env.get_agent_state(i) for i in range(NUM_DRONES)]

        # select actions
        actions = []
        for i in range(NUM_DRONES):
            actions.append(agent.select_action(agent_states[i]))

        # step environment
        _, rewards, done = env.step(actions)

        # next states
        next_agent_states = [env.get_agent_state(i) for i in range(NUM_DRONES)]

        # store experience
        for i in range(NUM_DRONES):
            global_reward = sum(rewards)

            agent.store(
                agent_states[i],
                actions[i],
                global_reward,
                next_agent_states[i],
                done
            )

        agent.train()

        total_reward += sum(rewards)
        step += 1

    # coverage metric
    coverage = np.sum(env.grid) / env.grid.size

    print(
        f"Episode {episode} DONE | Reward: {total_reward} | Steps: {step} | Coverage: {coverage:.2f} | Epsilon: {agent.epsilon:.3f}"
    )