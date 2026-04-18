# Capstone Project: Multi-Agent Reinforcement Learning for Drone Swarm Coordination in Search and Rescue

## Overview

This project implements a **Multi-Agent Reinforcement Learning (MARL)-based drone swarm system** designed for **search-and-rescue operations in disaster environments** such as earthquakes, floods, landslides, and collapsed structures.

The current implementation focuses on **cooperative drone movement and area coverage using QMIX**, where multiple drones learn to coordinate efficiently inside a simulated 3D environment.

The system is divided into two major stages:

* **Training Stage** – drones learn coordinated exploration behavior inside a custom grid environment.
* **Deployment Stage** – trained policy is deployed in ROS2 + Gazebo for multi-drone simulation.

---

## Project Objective

The goal is to build an intelligent drone swarm that can:

* autonomously explore large disaster zones
* minimize overlap between drones
* maximize area coverage
* avoid inefficient repeated search
* provide a scalable foundation for future victim detection systems

---

## Current System Architecture

```text
Training Environment
        ↓
QMIX Multi-Agent Learning
        ↓
Trained Model Export (.pth)
        ↓
ROS2 Deployment
        ↓
Gazebo Multi-Drone Simulation
        ↓
Live Action Execution
```

---

## Repository Structure

```text
Capstone_project/
│
├── marl_drone_project/
│   ├── env/
│   │   └── grid_env.py
│   │
│   ├── train/
│   │   ├── train_qmix.py
│   │   └── qmix_agent.py
│   │
│   ├── utils/
│   │   └── replay_buffer.py
│   │
│   ├── models/
│   │   └── qmix_phase1.pth
│   │
│   └── main.py
│
├── drone_ws/
│   └── src/
│       └── marl_controller/
│           ├── controller_node.py
│           ├── state_builder.py
│           ├── qmix_inference.py
│           └── action_mapper.py
│
├── models/
│   └── simple_drone/
│
├── worlds/
│   └── my_world.sdf
│
└── run_all.sh
```

---

## Phase 1: Training Environment

### Grid-Based 3D Environment

A custom grid environment is used for training before deployment into Gazebo.

Environment size:

```text
25 × 25 × 3
```

Each drone moves inside discrete grid cells.

### Drone Actions

Each drone has six movement actions:

```text
0 → +X
1 → -X
2 → +Y
3 → -Y
4 → +Z
5 → -Z
```

### Reward Objectives

The reward system encourages:

* exploration of unvisited cells
* wider coverage
* reduced overlap
* collision avoidance
* efficient cooperative movement

### Learning Algorithm

QMIX is used because:

* each drone learns local policy
* team learns global cooperative objective

---

## QMIX Training Pipeline

Training process:

```text
State → Action → Reward → Next State → Replay Buffer → QMIX Update
```

### Components

* **qmix_agent.py** → individual agent Q-networks + mixing network
* **train_qmix.py** → training loop
* **replay_buffer.py** → experience storage

### Output Model

After training:

```text
qmix_phase1.pth
```

This stores learned swarm behavior.

---

## Phase 2: ROS2 Deployment

After training, the learned policy is deployed into ROS2.

### Main Controller

`controller_node.py` performs:

* reads drone states
* builds RL-compatible observation
* runs trained model inference
* publishes movement commands

---

## State Construction

`state_builder.py` converts Gazebo drone positions into RL input.

Each drone receives:

* own position
* neighboring drone positions
* nearby occupancy information

Current state dimension:

```text
24-dimensional state vector
```

---

## Inference Module

`qmix_inference.py` loads:

```text
qmix_phase1.pth
```

and predicts movement action in real time.

---

## Action Execution

`action_mapper.py` converts predicted actions into drone movement inside Gazebo.

Current movement type:

* direct pose updates
* simplified simulation motion

---

## Gazebo Simulation

The project currently uses:

* Gazebo world (`my_world.sdf`)
* simplified drone model (`simple_drone`)

This provides a lightweight simulation for swarm testing.

---

## Execution

Run the full system:

```bash
./run_all.sh
```

This launches:

* Gazebo
* ROS2 nodes
* drone controller

---

## Current Achievements

The system currently supports:

* multi-drone cooperative movement
* QMIX-trained swarm behavior
* ROS2 integration
* Gazebo deployment
* coordinated area coverage

---

## Current Limitations

The current version does not yet include:

* obstacle avoidance
* victim detection
* camera perception
* YOLO object detection
* database storage
* alert generation

---

## Planned Next Phase

Next stage will integrate:

```text
Gazebo Camera → YOLO Detection → Object Classification → Location Storage → Alert System
```

This will enable:

* human detection
* animal detection
* rescue location reporting

---

## Future Extensions

Planned upgrades include:

* real quadrotor dynamics
* obstacle-aware navigation
* live heatmap visualization
* disaster scenario simulation
* full rescue communication pipeline

---

## Technology Stack

* Python
* PyTorch
* ROS2
* Gazebo
* QMIX (MARL)

---

## Research Focus

This project demonstrates how cooperative reinforcement learning can be applied to large-scale autonomous drone search systems.

It serves as a foundation for intelligent disaster-response robotics.

---
