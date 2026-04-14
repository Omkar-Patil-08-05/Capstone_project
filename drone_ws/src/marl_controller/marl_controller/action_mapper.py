import subprocess
import time


class ActionMapper:

    def __init__(self):
        self.offset = -11

    def get_next_pos(self, current_pos, action):
        x, y, z = current_pos

        if action == 0:
            x += 1
        elif action == 1:
            x -= 1
        elif action == 2:
            y += 1
        elif action == 3:
            y -= 1

        # 🔥 HARD LIMIT (NO BORDER STICK)
        x = max(2, min(22, x))
        y = max(2, min(22, y))

        return [x, y, z]

    def execute_move(self, drone_name, pos):
        wx = pos[0] + self.offset
        wy = pos[1] + self.offset

        cmd = f'gz service -s /world/default/set_pose \
--reqtype gz.msgs.Pose \
--reptype gz.msgs.Boolean \
--timeout 100 \
--req \'name: "{drone_name}", position: {{ x: {wx}, y: {wy}, z: 2 }}\''

        subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)

        # 🔥 CRITICAL: prevent overload
        time.sleep(0.05)