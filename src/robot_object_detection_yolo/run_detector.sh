#!/bin/bash
source /home/shivam/yolo_ws/venv_yolo/bin/activate
exec python3 /home/shivam/yolo_ws/install/robot_object_detection_yolo/lib/python3.10/site-packages/robot_object_detection_yolo/detector_node.py "$@"
