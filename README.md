<<<<<<< HEAD
# Robot-Object-Detection-YOLO
Real-time object and obstacle detection for mobile robots using YOLOv8, integrated as a ROS2 node that subscribes to a live camera feed (Gazebo simulation or real hardware) and publishes annotated detections.
=======
# Robot Object Detection YOLO

Simple ROS package for running a YOLO-based object detector on a robot.

## Contents
- `src/robot_object_detection_yolo` - ROS package source
- `models/yolov8n.pt` - YOLO model

## Prerequisites
- Ubuntu / Linux
- Python 3.10
- ROS 2 (workspace already contains built install files)
- Virtualenv (optional but recommended)

## Quick start
1. Activate virtualenv (if present):

   source venv_yolo/bin/activate

2. Build workspace (if needed):

   colcon build

# Robot-Object-Detection-YOLO

Real-time object and obstacle detection for mobile robots using YOLOv8, integrated as a ROS2 node that subscribes to a live camera feed (Gazebo simulation or real hardware) and publishes annotated detections.

## Contents
- `src/robot_object_detection_yolo` - ROS package source
- `models/yolov8n.pt` - YOLO model

## Prerequisites
- Ubuntu / Linux
- Python 3.10
- ROS 2 (workspace already contains built install files)
- Virtualenv (optional but recommended)

## Quick start
1. Activate virtualenv (if present):

   source venv_yolo/bin/activate

2. Build workspace (if needed):

   colcon build

3. Source the workspace:

   source install/setup.bash

4. Run the detector (example):

   ros2 run robot_object_detection_yolo detector_node

Adjust launch/run commands to your ROS setup as needed.

## Files of interest
- `src/robot_object_detection_yolo/robot_object_detection_yolo/detector_node.py` - detector node
- `src/robot_object_detection_yolo/launch/detector_launch.py` - launch file
- `models/yolov8n.pt` - model weights

## Pushing to GitHub
If you want me to push this workspace to `https://github.com/shiavm17/Robot-Object-Detection-YOLO.git`, ensure your local environment has appropriate Git credentials (HTTPS token or SSH key) configured.

To push manually:

```
cd /home/shivam/yolo_ws
git init                # if not already a repo
git remote add origin https://github.com/shiavm17/Robot-Object-Detection-YOLO.git
git add .
git commit -m "Initial commit: Robot Object Detection YOLO"
git branch -M main
git push -u origin main
```

If push fails due to authentication, create a personal access token and use it for HTTPS pushes, or configure SSH keys.

---
Merged README content (resolved conflict).
