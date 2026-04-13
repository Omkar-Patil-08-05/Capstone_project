import numpy as np
import torch
from env.grid_env import GridEnvironment
from train.qmix_agent import QMIXAgent

NUM_DRONES = 6

env = GridEnvironment(x_size=25, y_size=25, z_size=3, num_drones=NUM_DRONES)
env.reset()

state_size = len(env.get_agent_state(0))
action_size = 6

agent = QMIXAgent(NUM_DRONES, state_size, action_size)

# ✅ Load trained model
agent.load_model("qmix_phase1.pth")

episodes = 3  

for episode in range(episodes):
    env.reset()
    done = False

    print(f"\n🚀 EVALUATION EPISODE {episode}")

    while not done:
        states = [env.get_agent_state(i) for i in range(env.num_drones)]

        actions = agent.select_actions(states)

        _, rewards, done = env.step(actions)

        # print grid every few steps
        if env.current_step % 50 == 0:
            env.print_forest_slice(z=0)

    # ✅ final coverage
    valid_cells = np.sum(env.grid != -1)
    explored_cells = np.sum(env.grid == 1)
    coverage = explored_cells / valid_cells

    print(f"\n✅ Final Coverage: {coverage:.3f}")

    drone_percent = env.get_drone_coverage_percent()
    print(f"Drone Coverage (%): {[round(p*100, 2) for p in drone_percent]}")