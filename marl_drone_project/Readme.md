# 🚁 MARL Drone Swarm Coverage using QMIX

A **Multi-Agent Reinforcement Learning (MARL)** project where a swarm of drones learns to collaboratively explore a **3D environment** for search and rescue scenarios.

This project implements **QMIX-based cooperative learning** with advanced reward shaping to achieve efficient, coordinated coverage.

---

## 📌 Overview

* Environment: **3D grid (25 × 25 × 3)**
* Agents: **6 drones**
* Objective: **Maximize coverage of unexplored area**
* Constraints:

  * Obstacles (trees)
  * Limited steps
  * Collision avoidance

The system demonstrates **emergent coordination** without explicit communication.

---

## 🧠 Key Idea

> **Centralized Training, Decentralized Execution**

* Each drone learns its own policy
* A **QMIX mixing network** combines individual Q-values into a global objective
* Training uses a **global coverage reward**, enforcing cooperation

---

## 🗂️ Project Structure

```
.
├── env/
│   └── grid_env.py          # 3D environment + reward shaping
├── train/
│   ├── dqn_agent.py         # Independent DQN baseline
│   ├── qmix_agent.py        # QMIX implementation
│   ├── train_qmix.py        # QMIX training loop
│   └── train_single.py      # DQN training loop
├── utils/
│   └── replay_buffer.py
├── main.py
├── qmix_phase1.pth          # Saved model checkpoint
└── requirements.txt
```

---

## ⚙️ Environment Details

* Grid: **25 × 25 × 3**

* Obstacles: Random trees (`-1`)

* Free cells:

  * `0` → unexplored
  * `1` → explored

* Episode ends when:

  * Full coverage OR
  * Max steps (1200)

---

## 👁️ State Representation (Per Drone)

Each drone observes:

1. Own position (normalized)
2. Other drones' positions
3. 6 neighboring cell values

👉 Partial observability → promotes coordination learning

---

## 🎮 Action Space

Each drone has **6 discrete actions**:

* +X, -X
* +Y, -Y
* +Z, -Z

Constraints:

* Cannot leave grid
* Cannot enter obstacle cells

---

## 🎯 Reward Design (Advanced)

The reward function is carefully engineered to guide learning:

### Basic Rewards

* New cell explored → **+15**
* Revisiting → **-3**
* Collision → **-15**
* Step penalty → **-2**

### Advanced Shaping

#### 🔹 Frontier Exploration

* Bonus for nearby unexplored cells

#### 🔹 Cleanup Phase (>60% coverage)

* Strong reward for finishing isolated cells (**+50**)

#### 🔹 Global Pressure

* Encourages exploration:

```
(1 - coverage)^3 × 25
```

#### 🔹 Distance Guidance

* Reward for moving toward nearest unexplored cell

#### 🔹 Zone Guidance

* Each drone assigned a region → reduces overlap

#### 🔹 Coverage Bonus

```
coverage × 40
```

---

## 🤖 QMIX Architecture

* Each drone:

```
MLP: state → 64 → action Q-values
```

* Mixing Network:

```
(agent Qs + global state) → Q_total
```

* Optimized using **global reward**

> ⚠️ Note: This is a simplified QMIX (no monotonic constraint)

---

## 🏋️ Training Pipeline

For each episode:

1. Reset environment
2. Collect states
3. Select actions (ε-greedy)
4. Step environment
5. Compute **global coverage reward**
6. Store transition in replay buffer
7. Train periodically
8. Update epsilon

### Training Setup

* Episodes: **400**
* Batch size: **32**
* Replay buffer: **10,000**
* Target update: every 50 steps

---

## 🌍 Global Reward (Key Design)

Instead of per-agent reward:

```
coverage = explored_cells / valid_cells
global_reward = coverage × 100
```

👉 Ensures all agents optimize **team objective**

---

## 📊 Results

Training progression:

* Initial: **~0.65 coverage**
* Mid: **~0.80 coverage**
* Final: **~0.88 coverage**

### Observations

* Stable convergence after ~150 episodes
* Reduced overlap between drones
* Efficient area partitioning emerges automatically

---

## 🚀 Running the Project

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run environment test

```bash
python main.py
```

### Train QMIX

```bash
python train/train_qmix.py
```

---

## 💾 Model Saving

Models are automatically saved as:

```
qmix_phase1.pth
```

Includes:

* Agent networks
* Target networks
* Mixer
* Epsilon

---

## ⚠️ Known Limitations

* QMIX does not enforce monotonicity constraint
* Training not fully vectorized (slower)
* No real-time visualization
* No communication learning between agents

---

## 🔮 Future Work

* ROS2 + Gazebo integration
* Victim detection (YOLO)
* Sensor simulation (camera, LiDAR)
* Communication-aware MARL
* Scaling to larger swarms

---

## 📚 References

* QMIX (Rashid et al., 2018)
* DQN (Mnih et al., 2015)

---

## 📄 License

MIT License
