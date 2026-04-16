import subprocess
import time

class ActionMapper:

    def __init__(self):
        self.offset = -12
        self.grid_size = 25

    def get_next_pos(self, pos, action):
        x, y, z = pos

        if action == 0:
            x += 1
        elif action == 1:
            x -= 1
        elif action == 2:
            y += 1
        elif action == 3:
            y -= 1

        x = max(0, min(self.grid_size - 1, x))
        y = max(0, min(self.grid_size - 1, y))

        return [x, y, 2.0]

    def move_drone(self, drone_name, pos):

        wx = float(pos[0] + self.offset)
        wy = float(pos[1] + self.offset)

        cmd = f'gz service -s /world/default/set_pose \
--reqtype gz.msgs.Pose \
--reptype gz.msgs.Boolean \
--timeout 200 \
--req \'name: "{drone_name}", position: {{ x: {wx}, y: {wy}, z: 2 }}\''

        subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(0.099)