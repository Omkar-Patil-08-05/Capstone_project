import numpy as np


class StateBuilder:

    def __init__(self, num_drones):
        self.num_drones = num_drones

        self.x_size = 25
        self.y_size = 25
        self.z_size = 3

        self.scale = 1.0

        self.grid = np.zeros((self.x_size, self.y_size, self.z_size))
        self.drone_positions = [[0, 0, 0] for _ in range(num_drones)]

    def _to_grid(self, x, y, z):
        gx = int(round(x / self.scale))
        gy = int(round(y / self.scale))
        gz = int(round(z / 1.0))

        gx = max(0, min(self.x_size - 1, gx))
        gy = max(0, min(self.y_size - 1, gy))
        gz = max(0, min(self.z_size - 1, gz))

        return gx, gy, gz

    def update_positions(self, positions):
        self.drone_positions = positions

        for pos in positions:
            gx, gy, gz = self._to_grid(pos[0], pos[1], pos[2])

            if self.grid[gx][gy][gz] == 0:
                self.grid[gx][gy][gz] = 1

    def get_all_states(self):
        states = []

        directions = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

        for i in range(self.num_drones):

            x, y, z = self.drone_positions[i]
            gx, gy, gz = self._to_grid(x, y, z)

            own = [
                gx / self.x_size,
                gy / self.y_size,
                gz / self.z_size
            ]

            others = []
            for j, pos in enumerate(self.drone_positions):
                if j != i:
                    ox, oy, oz = pos
                    ogx, ogy, ogz = self._to_grid(ox, oy, oz)

                    others.extend([
                        ogx / self.x_size,
                        ogy / self.y_size,
                        ogz / self.z_size
                    ])

            neighbors = []
            for dx, dy, dz in directions:
                nx, ny, nz = gx+dx, gy+dy, gz+dz

                if 0 <= nx < self.x_size and 0 <= ny < self.y_size and 0 <= nz < self.z_size:
                    neighbors.append(self.grid[nx, ny, nz])
                else:
                    neighbors.append(1)

            state = np.array(own + others + neighbors)
            states.append(state)

        return states