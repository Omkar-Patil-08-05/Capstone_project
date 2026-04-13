import subprocess


class ActionMapper:

    def __init__(self):
        self.step_size = 0.5   # smoother movement

    def execute_action(self, drone_name, action, current_pos):
        x, y, z = current_pos

        # Movement mapping
        if action == 0:      # +X
            x += self.step_size
        elif action == 1:    # -X
            x -= self.step_size
        elif action == 2:    # +Y
            y += self.step_size
        elif action == 3:    # -Y
            y -= self.step_size
        elif action == 4:    # +Z
            z += 0.2
        elif action == 5:    # -Z
            z -= 0.2

        print(f"[MOVE] {drone_name} -> ({x:.2f}, {y:.2f}, {z:.2f})")

        # 🔥 Correct movement command
        cmd = (
            f'gz service -s /world/default/set_pose_vector '
            f'--reqtype gz.msgs.Pose_V '
            f'--reptype gz.msgs.Boolean '
            f'--timeout 300 '
            f'--req \'pose: [{{name: "{drone_name}", position: {{x: {x}, y: {y}, z: {z}}}}}]\''
        )

        subprocess.run(cmd, shell=True)

        return [x, y, z]