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

        # anti-oscillation memory
        self.history = {
            name: deque(maxlen=5)
            for name in self.drone_names
        }

        self.qmix = None

        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info("🚀 MARL Controller Started")

    def distance_to_unvisited(self, pos):
        min_dist = float('inf')

        for x in range(25):
            for y in range(25):
                if (x, y) not in self.visited:
                    d = abs(pos[0] - x) + abs(pos[1] - y)
                    min_dist = min(min_dist, d)

        return min_dist if min_dist != float('inf') else 0

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

        q_actions = self.qmix.get_actions(states)

        occupied = set()

        for i, drone_name in enumerate(self.drone_names):

            pos = self.current_positions[drone_name]
            q_action = q_actions[i] % 4

            candidate_actions = [0, 1, 2, 3]
            valid_actions = []

            # 🔥 STRICT FILTERING
            for a in candidate_actions:

                test_pos = self.action_mapper.get_next_pos(pos, a)
                x, y = test_pos[0], test_pos[1]

                # ❌ anti-oscillation
                if (x, y) in self.history[drone_name]:
                    continue

                # ❌ collision avoidance
                if (x, y) in occupied:
                    continue

                # ❌ STRICT BOUNDARY BUFFER (CRITICAL)
                if x <= 2 or x >= 22 or y <= 2 or y >= 22:
                    continue

                valid_actions.append(a)

            # fallback if nothing valid
            if not valid_actions:
                valid_actions = candidate_actions

            # 🔥 QMIX PRIORITY
            if q_action in valid_actions:
                action = q_action
            else:
                # fallback logic (light guidance only)
                best_action = None
                best_score = -1

                for a in valid_actions:
                    test_pos = self.action_mapper.get_next_pos(pos, a)

                    score = 0

                    if (test_pos[0], test_pos[1]) not in self.visited:
                        score += 10

                    dist = self.distance_to_unvisited(test_pos)
                    score += 5 / (dist + 1)

                    if score > best_score:
                        best_score = score
                        best_action = a

                action = best_action

            # execute
            new_pos = self.action_mapper.execute_action(
                drone_name,
                action,
                pos,
                occupied
            )

            # 🔥 FINAL HARD CLAMP (MOST IMPORTANT FIX)
            nx = int(round(new_pos[0]))
            ny = int(round(new_pos[1]))

            nx = max(2, min(22, nx))
            ny = max(2, min(22, ny))

            new_pos = [nx, ny, 2.0]

            self.current_positions[drone_name] = new_pos
            occupied.add((nx, ny))
            self.visited.add((nx, ny))

            self.history[drone_name].append((nx, ny))

        coverage = len(self.visited) / (25 * 25)
        print(f"🔥 Coverage: {coverage:.2f}")


def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()