import subprocess


class ActionMapper:

    def __init__(self):
        self.step_size = 1

    def get_next_pos(self, pos, action):
        x, y, z = pos

        if action == 0:
            x += self.step_size
        elif action == 1:
            x -= self.step_size
        elif action == 2:
            y += self.step_size
        elif action == 3:
            y -= self.step_size

        x = max(0, min(24, x))
        y = max(0, min(24, y))

        return [x, y, z]

    def move_drone(self, drone_name, pos):

        x, y, z = pos

        world_x = x - 12
        world_y = y - 12

        cmd = f"""
        gz service -s /world/default/set_pose \
        --reqtype gz.msgs.Pose \
        --reptype gz.msgs.Boolean \
        --timeout 200 \
        --req 'name: "{drone_name}", position: {{x: {float(world_x)}, y: {float(world_y)}, z: {float(z)}}}'
        """

        # ✅ NON-BLOCKING CALL
        subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )