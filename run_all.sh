#!/bin/bash

echo "🚀 STARTING COMPLETE MARL SYSTEM..."

# -----------------------------
# 1️⃣ Kill old Gazebo processes
# -----------------------------
echo "🧹 Cleaning old Gazebo..."
pkill -f gz

sleep 2

# -----------------------------
# 2️⃣ Build workspace
# -----------------------------
echo "🔨 Building workspace..."
cd ~/capstone_project/drone_ws || exit

rm -rf build install log
colcon build

# -----------------------------
# 3️⃣ Start Gazebo (background)
# -----------------------------
echo "🌍 Starting Gazebo..."
cd ~/capstone_project || exit

source /opt/ros/jazzy/setup.bash

gz sim -r my_world.sdf &

sleep 5   # give time to load

# -----------------------------
# 4️⃣ Spawn drones
# -----------------------------
echo "🚁 Spawning drones..."
cd ~/capstone_project/drone_ws || exit

source /opt/ros/jazzy/setup.bash

chmod +x spawn_drones.sh
./spawn_drones.sh

sleep 3

# -----------------------------
# 5️⃣ Run controller
# -----------------------------
echo "🧠 Starting MARL controller..."
cd ~/capstone_project/marl_drone_project || exit

source venv/bin/activate

export PYTHONPATH=$PYTHONPATH:~/capstone_project/marl_drone_project/venv/lib/python3.12/site-packages

cd ~/capstone_project/drone_ws || exit

source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 run marl_controller controller_node
