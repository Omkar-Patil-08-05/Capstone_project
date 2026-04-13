import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import torch
from env.grid_env import GridEnvironment
from train.qmix_agent import QMIXAgent

NUM_DRONES = 6

env = GridEnvironment(x_size=25, y_size=25, z_size=3, num_drones=NUM_DRONES)

env.reset()

# Always trust env (prevents mismatch bugs)
NUM_DRONES = env.num_drones

state_size = len(env.get_agent_state(0))
action_size = 6

agent = QMIXAgent(NUM_DRONES, state_size, action_size)

episodes = 400

coverage_history = []
best_coverage = 0

try:
    for episode in range(episodes):
        env.reset()

        total_reward = 0
        done = False

        while not done:
            states = [env.get_agent_state(i) for i in range(env.num_drones)]

            actions = agent.select_actions(states)

            _, rewards, done = env.step(actions)

            next_states = [env.get_agent_state(i) for i in range(env.num_drones)]

            # ✅ GLOBAL COVERAGE REWARD (correct)
            valid_cells = np.sum(env.grid != -1)
            explored_cells = np.sum(env.grid == 1)
            coverage = explored_cells / valid_cells

            global_reward = coverage * 100

            agent.store((states, actions, global_reward, next_states, done))

            # train only after enough experience
            if len(agent.memory) > 500 and env.current_step % 5 == 0:
                agent.train()

            total_reward += global_reward

        # Coverage calculation
        valid_cells = np.sum(env.grid != -1)
        explored_cells = np.sum(env.grid == 1)
        coverage = explored_cells / valid_cells

        coverage_history.append(coverage)
        best_coverage = max(best_coverage, coverage)

        drone_cells = env.get_drone_coverage()
        drone_percent = env.get_drone_coverage_percent()

        print(
            f"Episode {episode} | Reward: {total_reward} | Coverage: {best_coverage:.2f} | Epsilon: {agent.epsilon:.3f}"
        )

        print(f"Drone Coverage (cells): {drone_cells}")
        print(f"Drone Coverage (%): {[round(p*100, 2) for p in drone_percent]}")

        # env.print_forest_slice(z=0)
        if episode % 10 == 0:
            env.print_forest_slice(z=0)

        # CRITICAL FIX — EPSILON DECAY PER EPISODE 
        if agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay

except KeyboardInterrupt:
    print("\n⚠️ Training interrupted manually!")

finally:
    torch.save({
        "agents": [a.state_dict() for a in agent.agents],
        "target_agents": [a.state_dict() for a in agent.target_agents],
        "mixer": agent.mixer.state_dict(),
        "target_mixer": agent.target_mixer.state_dict(),
        "epsilon": agent.epsilon
    }, "qmix_phase1.pth")

    print("✅ Model saved successfully (QMIX full state)")