import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

RESULTS_DIR = os.path.expanduser("~/capstone_project/results")

# -------------------------------
# LOAD LATEST POSITION FILE
# -------------------------------
files = os.listdir(RESULTS_DIR)
pos_file = sorted([f for f in files if f.startswith("positions_") and f.endswith(".csv")])[-1]

pos_path = os.path.join(RESULTS_DIR, pos_file)

print("Using:", pos_path)

pos = pd.read_csv(pos_path)

# -------------------------------
# GRID SETTINGS
# -------------------------------
GRID_SIZE = 25

# obstacles (same as controller)
obstacles = [
    (4, 4),
    (8, 6),
    (12, 10),
    (16, 14),
    (20, 18),
    (6, 18),
    (18, 6),
    (10, 20),
    (14, 8)
]

# -------------------------------
# PREPARE DATA
# -------------------------------
time_steps = sorted(pos["time_step"].unique())
drones = pos["drone"].unique()

# -------------------------------
# SETUP PLOT
# -------------------------------
fig, ax = plt.subplots()
ax.set_xlim(0, GRID_SIZE)
ax.set_ylim(0, GRID_SIZE)
ax.set_title("Drone Swarm Exploration")

# scatter for drones
scatters = {
    drone: ax.plot([], [], marker='o', linestyle='', label=drone)[0]
    for drone in drones
}

# draw obstacles
ox = [o[0] for o in obstacles]
oy = [o[1] for o in obstacles]
ax.scatter(ox, oy, marker="X", s=120)

ax.legend()

# -------------------------------
# UPDATE FUNCTION
# -------------------------------
def update(frame):
    current = pos[pos["time_step"] == frame]

    for drone in drones:
        d = current[current["drone"] == drone]

        if not d.empty:
            x = d["x"].values[0]
            y = d["y"].values[0]
            scatters[drone].set_data(x, y)

    ax.set_title(f"Swarm Exploration (Step {frame})")

    return list(scatters.values())

# -------------------------------
# CREATE ANIMATION
# -------------------------------
ani = animation.FuncAnimation(
    fig,
    update,
    frames=time_steps,
    interval=150,   # speed (lower = faster)
    blit=True
)

# -------------------------------
# SAVE AS GIF
# -------------------------------
output_path = os.path.join(RESULTS_DIR, "swarm_animation.gif")

ani.save(output_path, writer="pillow")

print("Saved:", output_path)

plt.show()