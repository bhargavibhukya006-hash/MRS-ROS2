# MRS-ROS2

Multi-agent system using ROS2, A* path planning, and dynamic obstacles.
# MRS-ROS2 🚀

## 📌 Overview

This project implements a **multi-agent collaborative system** where three agents coordinate to complete tasks in a shared environment. The system ensures **collision-free navigation**, **dynamic obstacle handling**, and **task allocation**.

We integrate **ROS2 (Humble)** for communication and control, while the simulation is visualized using **Pygame**.

---

## 🎯 Problem Statement Coverage

### ✔ Objective

* Multi-agent collaboration on shared tasks
* Coordinated movement with collision avoidance
* Task sharing and completion
* Simulation-based demonstration

### ✔ Requirements

* **Coordination Protocol** → Implemented via `Coordinator`
* **Collision-Free Movement** → A* + collision resolution
* **Joint Task Completion** → Pickup & delivery system
* **Failure Handling** → Agent recovery mechanism

---

## ⚙️ Key Features

* 🧠 **A* Global Path Planning**
* 🔄 **Dynamic Obstacles** (move every step)
* 🤖 **Multi-Agent Coordination**
* 🚫 **Collision Avoidance System**
* ♻️ **Failure & Recovery Handling**
* 📡 **ROS2 Integration** (publisher-based control)
* 🎮 **Pygame Visualization**

---

## 🏗️ System Architecture

* **Planning Layer** → A* (pathfinding.py)
* **Coordination Layer** → Task allocation (coordination.py)
* **Execution Layer** → Simulation loop (main.py)
* **Communication Layer** → ROS2 node (ros_node.py)

---

## ▶️ How to Run

### 1️⃣ Run ROS2 Node (WSL - Ubuntu)

```bash
source /opt/ros/humble/setup.bash
python3 ros_node.py
```

### 2️⃣ Run Simulation (Windows / VS Code)

```bash
python main.py
```

---

## 🎮 Control via ROS2

Modify in `ros_node.py`:

* `FAST` → agents move
* `SLOW` → agents pause

---

## 📊 Evaluation Criteria Coverage

* ✔ Task Completion Rate
* ✔ Coordination Quality
* ✔ Collision-Free Operation
* ✔ Fault Tolerance (Recovery logic)
* ✔ Real-time Simulation Demo

---

## 🤖 Reinforcement Learning (Bonus)

We explored:

* Q-Learning
* Deep Q-Network (DQN)

for adaptive agent behavior (stored models included).

---

## ⚠️ Notes

* ROS2 runs on **WSL (Ubuntu)**
* Simulation runs on **Windows (Pygame)**
* Communication handled via lightweight bridge

---

## 🚀 Future Improvements

* Full ROS-native integration
* Gazebo / Webots simulation
* Real robot deployment

---

## 👩‍💻 Team

Hackathon Submission
