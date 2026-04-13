import rclpy
from rclpy.node import Node

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

        # Initial positions (same as spawn)
        self.current_positions = {
            "drone1": [0, 0, 0.5],
            "drone2": [2, 0, 0.5],
            "drone3": [4, 0, 0.5],
            "drone4": [6, 0, 0.5],
            "drone5": [8, 0, 0.5],
            "drone6": [10, 0, 0.5],
        }

        self.qmix = None

        # Timer loop
        self.timer = self.create_timer(1.0, self.control_loop)

        self.get_logger().info("🚀 MARL Controller Started")

    def control_loop(self):

        print("\n===== CONTROL LOOP =====")

        # Ordered positions
        ordered_positions = [
            self.current_positions[name]
            for name in self.drone_names
        ]

        print("Positions:", ordered_positions)

        # Build states
        self.state_builder.update_positions(ordered_positions)
        states = self.state_builder.get_all_states()

        print("States built")

        # Load QMIX once
        if self.qmix is None:
            print("Loading QMIX model...")
            self.qmix = QMIXInference(
                model_path='/home/capstone/capstone_project/drone_ws/src/marl_controller/models/qmix_phase1.pth',
                num_drones=self.num_drones,
                state_size=len(states[0]),
                action_size=6
            )
            print("QMIX loaded")

        # Get actions
        actions = self.qmix.get_actions(states)
        print("Actions:", actions)

        # Execute actions
        for i, drone_name in enumerate(self.drone_names):
            action = actions[i]
            pos = self.current_positions[drone_name]

            new_pos = self.action_mapper.execute_action(
                drone_name,
                action,
                pos
            )

            self.current_positions[drone_name] = new_pos


def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()