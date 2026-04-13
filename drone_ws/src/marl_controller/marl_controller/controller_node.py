import rclpy
from rclpy.node import Node
import random

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

        # 🔥 GOOD START POSITIONS (SPREAD)
        self.current_positions = {
            "drone1": [3, 3, 2.0],
            "drone2": [12, 3, 2.0],
            "drone3": [21, 3, 2.0],
            "drone4": [3, 12, 2.0],
            "drone5": [12, 12, 2.0],
            "drone6": [21, 12, 2.0],
        }

        self.visited = set()
        self.qmix = None

        # 🔥 FASTER LOOP (5x SPEED)
        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info("🚀 MARL Controller Started")

    def control_loop(self):

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

        actions = self.qmix.get_actions(states)

        occupied = set()

        for i, drone_name in enumerate(self.drone_names):

            action = actions[i]

            # 🔥 REMOVE Z
            if action >= 4:
                action = action % 4

            # 🔥 ADD EXPLORATION (VERY IMPORTANT)
            if random.random() < 0.3:
                action = random.randint(0, 3)

            pos = self.current_positions[drone_name]

            new_pos = self.action_mapper.execute_action(
                drone_name,
                action,
                pos,
                occupied
            )

            new_pos = [
                int(round(new_pos[0])),
                int(round(new_pos[1])),
                2.0
            ]

            self.current_positions[drone_name] = new_pos
            occupied.add((new_pos[0], new_pos[1]))

            self.visited.add((new_pos[0], new_pos[1]))

        coverage = len(self.visited) / (25 * 25)
        print(f" Coverage: {coverage:.2f}")


def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()