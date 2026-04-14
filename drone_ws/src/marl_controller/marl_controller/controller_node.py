import rclpy
from rclpy.node import Node
from collections import deque

from marl_controller.state_builder import StateBuilder
from marl_controller.qmix_inference import QMIXInference
from marl_controller.action_mapper import ActionMapper


class ControllerNode(Node):

    def __init__(self):
        super().__init__('marl_controller')

        self.num_drones = 6

        self.drone_names = [
            "drone1", "drone2", "drone3",
            "drone4", "drone5", "drone6"
        ]

        self.state_builder = StateBuilder(num_drones=self.num_drones)
        self.action_mapper = ActionMapper()

        self.current_positions = {
            "drone1": [3, 3, 2.0],
            "drone2": [12, 3, 2.0],
            "drone3": [21, 3, 2.0],
            "drone4": [3, 12, 2.0],
            "drone5": [12, 12, 2.0],
            "drone6": [21, 12, 2.0],
        }

        self.visited = set()

        self.history = {
            name: deque(maxlen=6)
            for name in self.drone_names
        }

        self.qmix = None

        self.step_count = 0

        # 🔥 slower loop (MANDATORY)
        self.timer = self.create_timer(0.6, self.control_loop)

        self.get_logger().info("🚀 MARL Controller Started")

    def control_loop(self):

        self.step_count += 1

        ordered_positions = [
            self.current_positions[name]
            for name in self.drone_names
        ]

        self.state_builder.update_positions(ordered_positions)
        states = self.state_builder.get_all_states()

        if self.qmix is None:
            print("Loading QMIX...")
            self.qmix = QMIXInference(
                model_path='/home/capstone/capstone_project/drone_ws/src/marl_controller/models/qmix_phase1.pth',
                num_drones=self.num_drones,
                state_size=len(states[0]),
                action_size=6
            )
            print("✅ QMIX Loaded")

        q_actions = self.qmix.get_actions(states)

        occupied = set()
        center = (12, 12)

        new_positions = {}

        for i, drone_name in enumerate(self.drone_names):

            pos = self.current_positions[drone_name]
            q_action = q_actions[i] % 4

            best_action = None
            best_score = -999

            for a in [0, 1, 2, 3]:

                test_pos = self.action_mapper.get_next_pos(pos, a)
                x, y = test_pos[0], test_pos[1]

                if (x, y) in occupied:
                    continue

                score = 0

                # 🔥 STRONG exploration reward
                if (x, y) not in self.visited:
                    score += 50
                else:
                    score -= 10

                # 🔥 FORCE center attraction (fix border issue)
                center_dist = abs(x - center[0]) + abs(y - center[1])
                score += 10 / (center_dist + 1)

                # 🔥 HEAVY border penalty
                if x < 3 or x > 21 or y < 3 or y > 21:
                    score -= 20

                # 🔥 anti-oscillation
                if (x, y) in self.history[drone_name]:
                    score -= 15

                # 🔥 QMIX small bias
                if a == q_action:
                    score += 3

                if score > best_score:
                    best_score = score
                    best_action = a

            if best_action is None:
                best_action = q_action

            new_pos = self.action_mapper.get_next_pos(pos, best_action)

            new_positions[drone_name] = new_pos
            occupied.add((new_pos[0], new_pos[1]))

        # 🔥 EXECUTE WITH DELAY (KEY FIX)
        for drone_name, pos in new_positions.items():

            self.action_mapper.execute_move(drone_name, pos)

            self.current_positions[drone_name] = pos
            self.visited.add((pos[0], pos[1]))
            self.history[drone_name].append((pos[0], pos[1]))

        coverage = len(self.visited) / (25 * 25)
        print(f"🔥 Coverage: {coverage:.2f}")


def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()