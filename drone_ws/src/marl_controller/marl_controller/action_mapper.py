import subprocess
import random


class ActionMapper:

    def __init__(self):
        self.grid_size = 25
        self.offset = -12

    def execute_action(self, drone_name, action, current_pos, occupied):

        import time

        x, y, z = current_pos
        nx, ny = x, y

        # boundary correction
        if x <= 0:
            action = 0
        elif x >= self.grid_size - 1:
            action = 1
        elif y <= 0:
            action = 2
        elif y >= self.grid_size - 1:
            action = 3

        # action map
        if action == 0:
            nx = x + 1
        elif action == 1:
            nx = x - 1
        elif action == 2:
            ny = y + 1
        elif action == 3:
            ny = y - 1

        nx = max(0, min(self.grid_size - 1, nx))
        ny = max(0, min(self.grid_size - 1, ny))

        # collision avoidance
        if (nx, ny) in occupied:
            return current_pos

        # 🔥 INTERPOLATION (THIS FIXES JUMPING)
        steps = 5
        for i in range(1, steps + 1):
            ix = x + (nx - x) * (i / steps)
            iy = y + (ny - y) * (i / steps)

            wx = ix + self.offset
            wy = iy + self.offset

            cmd = f'gz service -s /world/default/set_pose --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean --timeout 100 --req \'name: "{drone_name}", position: {{ x: {wx}, y: {wy}, z: 2 }}\''

            subprocess.run(cmd, shell=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)

            time.sleep(0.02)

        return [nx, ny, 2.0]