import numpy as np


class GridEnvironment:
    def __init__(self, x_size=25, y_size=25, z_size=3, num_drones=6):
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.num_drones = num_drones

        self.grid = np.zeros((x_size, y_size, z_size))
        self.drone_positions = []

        self.max_steps = 1200
        self.current_step = 0

        self.tree_density = 0.03

    def reset(self):
        self.grid = np.zeros((self.x_size, self.y_size, self.z_size))
        self.drone_positions = []

        self.drone_coverage = [set() for _ in range(self.num_drones)]

        num_cells = self.x_size * self.y_size * self.z_size
        num_trees = int(self.tree_density * num_cells)

        # 🌲 Trees
        for _ in range(num_trees):
            x = np.random.randint(0, self.x_size)
            y = np.random.randint(0, self.y_size)
            z = np.random.randint(0, self.z_size)
            self.grid[x, y, z] = -1

        # Spawn drones
        for _ in range(self.num_drones):
            while True:
                x = np.random.randint(0, self.x_size)
                y = np.random.randint(0, self.y_size)
                z = np.random.randint(0, self.z_size)

                if self.grid[x, y, z] != -1:
                    break

            self.drone_positions.append([x, y, z])

        # BALANCED ZONES 
        self.drone_zones = []
        edges = np.linspace(0, self.x_size, self.num_drones + 1, dtype=int)

        for i in range(self.num_drones):
            start = edges[i]
            end = edges[i + 1]
            self.drone_zones.append((start, end))

        # mark initial coverage
        for i, (x, y, z) in enumerate(self.drone_positions):
            self.grid[x, y, z] = 1
            self.drone_coverage[i].add((x, y, z))

        self.prev_coverage = [0] * self.num_drones
        self.current_step = 0

        return self.get_state()

    def get_state(self):
        return np.concatenate((
            self.grid.flatten(),
            np.array(self.drone_positions).flatten()
        ))

    def get_agent_state(self, agent_id):
        x, y, z = self.drone_positions[agent_id]

        own = [x / self.x_size, y / self.y_size, z / self.z_size]

        others = []
        for i, pos in enumerate(self.drone_positions):
            if i != agent_id:
                ox, oy, oz = pos
                others.extend([ox / self.x_size, oy / self.y_size, oz / self.z_size])

        neighbors = []
        directions = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

        for dx, dy, dz in directions:
            nx, ny, nz = x+dx, y+dy, z+dz
            if 0 <= nx < self.x_size and 0 <= ny < self.y_size and 0 <= nz < self.z_size:
                neighbors.append(self.grid[nx, ny, nz])
            else:
                neighbors.append(1)

        return np.array(own + others + neighbors)

    def step(self, actions):
        rewards = [0] * self.num_drones
        new_positions = []

        directions = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

        # 🔹 MOVE
        for i in range(self.num_drones):
            x, y, z = self.drone_positions[i]
            nx, ny, nz = x, y, z

            if actions[i] == 0 and x+1 < self.x_size: nx = x+1
            elif actions[i] == 1 and x-1 >= 0: nx = x-1
            elif actions[i] == 2 and y+1 < self.y_size: ny = y+1
            elif actions[i] == 3 and y-1 >= 0: ny = y-1
            elif actions[i] == 4 and z+1 < self.z_size: nz = z+1
            elif actions[i] == 5 and z-1 >= 0: nz = z-1

            if self.grid[nx, ny, nz] == -1:
                nx, ny, nz = x, y, z

            new_positions.append([nx, ny, nz])

        valid_cells = np.sum(self.grid != -1)
        explored_cells = np.sum(self.grid == 1)
        coverage = explored_cells / valid_cells

        cleanup_mode = coverage > 0.6

        #  REWARD
        for i in range(self.num_drones):
            reward = -2

            # STRONGER COLLISION CONTROL
            if new_positions.count(new_positions[i]) > 1:
                reward -= 15
                new_positions[i] = self.drone_positions[i]
            else:
                x, y, z = new_positions[i]

                if self.grid[x, y, z] == 0:
                    frontier_bonus = 0
                    unexplored_neighbors = 0

                    for dx, dy, dz in directions:
                        nx, ny, nz = x+dx, y+dy, z+dz
                        if 0 <= nx < self.x_size and 0 <= ny < self.y_size and 0 <= nz < self.z_size:
                            if self.grid[nx, ny, nz] == 0:
                                frontier_bonus += 5
                                unexplored_neighbors += 1

                    if cleanup_mode:
                        if unexplored_neighbors <= 2:
                            reward += 50   # increased
                        else:
                            reward += 10
                    else:
                        reward += 15

                    reward += frontier_bonus
                else:
                    reward -= 3

            rewards[i] = reward

        # last update
        for i in range(self.num_drones):
            self.drone_positions[i] = new_positions[i]
            x, y, z = new_positions[i]

            self.grid[x, y, z] = 1
            self.drone_coverage[i].add((x, y, z))

        self.current_step += 1

        # GLOBAL PRESSURE
        unexplored_ratio = (1 - coverage) ** 3
        for i in range(self.num_drones):
            rewards[i] += unexplored_ratio * 25

        # TARGET GUIDANCE
        unexplored_positions = np.argwhere(self.grid == 0)
        if len(unexplored_positions) > 0:
            for i in range(self.num_drones):
                x, y, z = self.drone_positions[i]
                dists = np.abs(unexplored_positions - np.array([x, y, z])).sum(axis=1)
                min_dist = np.min(dists)

                if cleanup_mode:
                    rewards[i] += 15 / (min_dist + 1)  # boosted
                else:
                    rewards[i] += 3 / (min_dist + 1)

        # COVERAGE BONUS
        rewards = [r + coverage * 40 for r in rewards]

        # ZONE GUIDANCE 
        for i in range(self.num_drones):
            x, _, _ = self.drone_positions[i]
            zone_start, zone_end = self.drone_zones[i]

            if not (zone_start <= x < zone_end):
                if coverage < 0.6:
                    rewards[i] -= 1
                elif coverage < 0.8:
                    rewards[i] -= 3
                else:
                    rewards[i] -= 1

        # DONE
        done = False

        if explored_cells == valid_cells:
            done = True
            rewards = [r + 200 for r in rewards]

        if self.current_step >= self.max_steps:
            done = True

        return self.get_state(), rewards, done

    def get_drone_coverage(self):
        return [len(c) for c in self.drone_coverage]

    def get_drone_coverage_percent(self):
        valid_cells = np.sum(self.grid != -1)
        return [len(c) / valid_cells for c in self.drone_coverage]
    
    def print_forest_slice(self, z=0):
        print(f"\n🌲 Forest slice at z={z}")

        for y in range(self.y_size):
            row = ""
            for x in range(self.x_size):
                val = self.grid[x, y, z]

                if val == -1:
                    row += " 🌲 "
                elif val == 1:
                    row += " 0 "
                else:
                    row += " . "

            print(row)