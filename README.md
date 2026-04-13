# 🚁 MARL Drone Swarm for Search & Rescue (QMIX + ROS2 + Gazebo)

## 📌 Overview

This project implements a **Multi-Agent Reinforcement Learning (MARL)** based drone swarm using the **QMIX algorithm** for coordinated exploration and coverage.

The system simulates **multiple drones operating collaboratively** in a 3D grid environment and deploys the trained policy into a **realistic Gazebo simulation using ROS2**.

---

## 🎯 Objectives

* Develop coordinated multi-drone exploration using MARL
* Maximize area coverage with minimal overlap
* Transition from training (grid world) to real-time simulation (Gazebo)
* Build a scalable framework for **search & rescue applications**

---

## 🧠 Key Technologies

* **Reinforcement Learning**: QMIX (Centralized Training, Decentralized Execution)
* **Simulation**: Gazebo (GZ Sim)
* **Middleware**: ROS2 (Jazzy)
* **Language**: Python
* **Environment**: Custom 3D Grid (25 × 25 × 3)

---

## 🏗️ System Architecture

```
Training Phase:
Grid Environment → QMIX Training → Trained Model (.pth)

Deployment Phase:
Gazebo → State Builder → QMIX Inference → Action Mapper → Drone Movement
```

---

## 📁 Project Structure

```
capstone_project/
│
├── drone_ws/                          # ROS2 workspace
│   └── src/marl_controller/
│       ├── marl_controller/
│       │   ├── controller_node.py     # Main ROS2 controller
│       │   ├── state_builder.py       # Builds RL state
│       │   ├── action_mapper.py       # Converts actions → movement
│       │   ├── qmix_inference.py      # Loads trained model
│       │   └── qmix_agent.py
│       │
│       ├── models/
│       │   └── qmix_phase1.pth        # Trained QMIX model
│       │
│       ├── package.xml
│       └── setup.py
│
├── marl_drone_project/                # Training code
│   ├── env/grid_env.py               # Custom environment
│   ├── train/train_qmix.py           # QMIX training
│   ├── train/qmix_agent.py
│   ├── utils/replay_buffer.py
│   └── main.py
│
├── spawn_drones.sh                   # Spawns drones in Gazebo
├── run_all.sh                        # Runs full system
├── my_world.sdf                      # Gazebo world
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Install Dependencies

```bash
sudo apt update
sudo apt install ros-jazzy-desktop
sudo apt install ros-jazzy-ros-gz
```

---

### 2️⃣ Setup Python Environment

```bash
cd marl_drone_project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3️⃣ Build ROS2 Workspace

```bash
cd drone_ws
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
```

---

## 🚀 Running the Project

### 🔥 One Command (Recommended)

```bash
./run_all.sh
```

---

### 🧪 Manual Run (Optional)

#### Terminal 1 — Gazebo

```bash
gz sim my_world.sdf
```

#### Terminal 2 — Spawn Drones

```bash
bash spawn_drones.sh
```

#### Terminal 3 — Controller

```bash
cd marl_drone_project
source venv/bin/activate

cd ../drone_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 run marl_controller controller_node
```

---

## 🤖 How It Works

### 🧠 State Representation (24-dim)

Each drone observes:

* Own position (x, y, z)
* Positions of other drones
* Neighboring cell occupancy (6 directions)

---

### 🎮 Action Space

| Action | Movement                   |
| ------ | -------------------------- |
| 0      | +X                         |
| 1      | -X                         |
| 2      | +Y                         |
| 3      | -Y                         |
| 4      | +Z (ignored in deployment) |
| 5      | -Z (ignored in deployment) |

---

### 🛰️ Execution Flow

1. Get drone positions
2. Build state (StateBuilder)
3. QMIX predicts actions
4. ActionMapper updates positions
5. Gazebo updates drone positions

---

## 📊 Results

* Coordinated multi-agent exploration
* Reduced overlap between drones
* Emergent swarm behavior
* Stable deployment in Gazebo

---

## ⚠️ Limitations

* Uses simplified drone model (boxes)
* Movement via pose updates (not real physics control)
* No obstacle avoidance (yet)

---

## 🚀 Future Improvements

* ✅ Real drone model (quadrotor)
* ✅ Obstacle avoidance & mapping
* ✅ Coverage heatmap visualization
* ✅ YOLO-based victim detection
* ✅ Real-world deployment integration

---

## 👨‍💻 Author

**Omkar Patil**
Capstone Project — MARL Drone Swarm

---

## ⭐ Acknowledgements

* ROS2 Community
* Gazebo Simulation
* MARL & QMIX research papers

---

## 📌 Note

This project demonstrates the integration of **deep reinforcement learning with robotic simulation**, bridging the gap between theoretical AI and real-world autonomous systems.

---
