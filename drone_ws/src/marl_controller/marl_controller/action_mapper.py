import subprocess
import time


class ActionMapper:

    def __init__(self):
        self.grid_size = 25
        self.offset = -11  # safe offset

    def get_next_pos(self, current_pos, action):
        x, y, z = current_pos
        nx, ny = x, y

        if action == 0:
            nx = x + 1
        elif action == 1:
            nx = x - 1
        elif action == 2:
            ny = y + 1
        elif action == 3:
            ny = y - 1

        # clamp safe range
        nx = max(1, min(23, nx))
        ny = max(1, min(23, ny))

        return [nx, ny, z]

    def execute_action(self, drone_name, action, current_pos, occupied):

        x, y, z = current_pos

        next_pos = self.get_next_pos(current_pos, action)
        nx, ny = next_pos[0], next_pos[1]

        if (nx, ny) in occupied:
            return current_pos

        steps = 4
        for i in range(1, steps + 1):
            ix = x + (nx - x) * (i / steps)
            iy = y + (ny - y) * (i / steps)

            wx = ix - 11
            wy = iy - 11

            cmd = f'gz service -s /world/default/set_pose --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean --timeout 100 --req \'name: "{drone_name}", position: {{ x: {wx}, y: {wy}, z: 2 }}\''

            subprocess.run(cmd, shell=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

            time.sleep(0.04)

        return [nx, ny, 2.0]