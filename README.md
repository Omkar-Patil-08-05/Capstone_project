# 🚁 MARL Drone Swarm for Search & Rescue  
### *(QMIX + ROS2 + Gazebo + Visualization)*

---

## 📌 Overview

This project implements a **Multi-Agent Reinforcement Learning (MARL)** based drone swarm using the **QMIX algorithm** for coordinated exploration and area coverage.

The system transitions from a **custom grid-based training environment** to a **real-time multi-drone simulation in Gazebo using ROS2**, demonstrating how learned cooperative behavior can be deployed in a robotic system.

The current implementation achieves:

- Coordinated multi-drone exploration  
- Near 100% area coverage  
- Obstacle-aware navigation  
- Real-time simulation with ROS2  
- Result visualization (graphs + animation)

---

## 🎯 Objectives

- Develop coordinated multi-drone exploration using MARL  
- Maximize coverage while minimizing overlap  
- Enable obstacle-aware navigation  
- Bridge training → real-time robotic simulation  
- Build a foundation for search & rescue systems  

---

## 🧠 Key Technologies

- Reinforcement Learning: QMIX (CTDE paradigm)  
- Simulation: Gazebo (GZ Sim)  
- Middleware: ROS2 (Jazzy)  
- Language: Python  
- Visualization: Matplotlib (graphs + animation)  
- Environment: Custom Grid (25 × 25 × 3)  

---

## 🏗️ System Architecture

Training Phase:
Grid Environment → QMIX Training → Trained Model (.pth)

Deployment Phase:
Gazebo → State Builder → QMIX Inference → Action Mapper → Drone Movement

Evaluation Phase:
Simulation Logs → CSV → Graphs + Heatmaps + Animation

---

## 📁 Project Structure

capstone_project/
│
├── drone_ws/                          # ROS2 workspace  
│   └── src/marl_controller/  
│       ├── marl_controller/  
│       │   ├── controller_node.py  
│       │   ├── state_builder.py  
│       │   ├── action_mapper.py  
│       │   ├── qmix_inference.py  
│       │  
│       ├── models/  
│       │   └── qmix_phase1.pth  
│
├── marl_drone_project/                # Training code  
│   ├── env/grid_env.py  
│   ├── train/train_qmix.py  
│   ├── utils/replay_buffer.py  
│
├── results/                           # NEW  
│   ├── logger.py  
│   ├── plot_results.py  
│   ├── animate.py  
│   ├── *.csv  
│   └── *.png / *.gif  
│
├── models/simple_drone/  
├── my_world.sdf  
├── spawn_drones.sh  
├── run_all.sh  
└── README.md  

---

## ⚙️ Installation & Setup

### 1️⃣ Install Dependencies

sudo apt update  
sudo apt install ros-jazzy-desktop  
sudo apt install ros-jazzy-ros-gz  

---

### 2️⃣ Setup Python Environment

cd marl_drone_project  
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  

---

### 3️⃣ Build ROS2 Workspace

cd drone_ws  
source /opt/ros/jazzy/setup.bash  
colcon build  
source install/setup.bash  

---

## 🚀 Running the Project

### 🔥 Full System

./run_all.sh  

---

## 🤖 System Functionality

### 🧠 State Representation

Each drone observes:

- Own position  
- Neighbor drone positions  
- Local spatial structure  

---

### 🎮 Action Space

| Action | Movement |
|--------|--------|
| 0 | +X |
| 1 | -X |
| 2 | +Y |
| 3 | -Y |
| 4 | +Z |
| 5 | -Z |

---

### 🚧 Obstacle Avoidance

- Static obstacles (trees) added in Gazebo  
- Hard constraints prevent entering obstacle cells  
- Drones dynamically navigate around obstacles  

---

### 🤝 Multi-Agent Coordination

- Simultaneous drone movement (non-blocking execution)  
- Reduced overlap via reward shaping + heuristics  
- Balanced exploration across agents  

---

## 📊 Results & Visualization

The system generates:

- Coverage vs Time (efficiency & convergence)  
- Heatmap (spatial exploration)  
- Trajectories (coordination)  
- Per-drone coverage (fairness)  
- Coverage speed (efficiency analysis)  
- Heatmap with obstacles (validation)  
- Swarm animation (movement + coordination)  

---

## 🏆 Key Achievements

- Near 100% coverage in 25×25 environment  
- Emergent coordinated swarm behavior  
- Successful deployment from training → simulation  
- Obstacle-aware exploration  
- Complete evaluation pipeline (logs → graphs → animation)  

---

## ⚠️ Current Limitations

- Simplified drone model (no real physics)  
- Grid-based movement abstraction  
- No perception system yet  
- Static obstacles only  

---

## 🚀 Future Work

### Perception & Intelligence
- YOLO-based victim detection  
- Camera integration in Gazebo  
- Object classification  

### Navigation Enhancements
- Dynamic obstacle avoidance  
- Continuous motion (velocity control)  
- Path smoothing  

### Realism Improvements
- Full quadrotor physics  
- PX4 / MAVROS integration  
- Outdoor terrain simulation  

### System Expansion
- Multi-zone coordination  
- Communication-aware MARL  
- Real-time dashboard  

---

## 👨‍💻 Author

Omkar Patil  
Capstone Project — MARL Drone Swarm  

---

## 📌 Summary

This project demonstrates how multi-agent reinforcement learning enables coordinated autonomous exploration, bridging:

theoretical AI → robotic simulation → real-world applications