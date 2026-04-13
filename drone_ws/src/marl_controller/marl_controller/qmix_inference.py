import torch
from marl_controller.qmix_agent import QMIXAgent


class QMIXInference:
    def __init__(self, model_path, num_drones, state_size, action_size):

        self.num_drones = num_drones

        self.agent = QMIXAgent(num_drones, state_size, action_size)

        self.agent.load_model(model_path)

        self.agent.epsilon = 0.0

        for a in self.agent.agents:
            a.eval()

        self.agent.mixer.eval()

        print("✅ QMIX Inference Ready")

    def get_actions(self, states):
        actions = []

        with torch.no_grad():
            for i in range(self.num_drones):
                state = torch.FloatTensor(states[i])
                q_values = self.agent.agents[i](state)
                action = torch.argmax(q_values).item()
                actions.append(action)

        return actions