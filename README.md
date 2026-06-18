<div align="center">

# 🤖 Robot Object Detection YOLO

### Real-time object & obstacle detection for mobile robots, powered by YOLOv8 and ROS2

[![ROS2](https://img.shields.io/badge/ROS2-Humble-22314E?style=for-the-badge&logo=ros&logoColor=white)](https://docs.ros.org/en/humble/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge&logo=yolo&logoColor=black)](https://github.com/ultralytics/ultralytics)
[![Gazebo](https://img.shields.io/badge/Gazebo-Classic-F58220?style=for-the-badge&logo=gazebo&logoColor=white)](https://classic.gazebosim.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](#license)

*A robot that can drive, see, and tell you what it's looking at — all in real time.*

</div>

---

## 📌 What is this?

This is a ROS2 node that gives a mobile robot the ability to actually understand what's in front of it. It grabs whatever the robot's camera is seeing, runs it through a YOLOv8 model, and instantly publishes two things back into the ROS2 ecosystem: an annotated image with bounding boxes drawn around everything it spotted, and a clean JSON feed listing exactly what it found and how confident it is.

I built and tested this against a simulated TortoiseBot in Gazebo, driving it around with keyboard teleop while the detector picked out people and obstacles live, frame by frame.

```
        📡 Camera Feed                🧠 YOLOv8 Detector              📤 Output
  /raspberrypi_camera/image_raw  ──▶   detector_node.py   ──┬──▶   /detection_image
                                                              └──▶   /detections (JSON)
```

---

## 🎬 See it in action

<div align="center">

**The simulation world — a Gazebo room the robot explores**

<img src="images/gazebo_room_world.png" width="650" alt="Gazebo room world"/>

<br/><br/>

**Everything running together — Gazebo, teleop control, and live detection side by side**

<img src="src/Screenshot from 2026-06-18 11-07-29.png" width="800" alt="Full pipeline running"/>

<br/><br/>

**Close-up of the robot's eyes — the live camera feed in rqt_image_view**

<img src="src/Screenshot from 2026-06-18 11-07-58.png" width="650" alt="rqt_image_view closeup"/>

</div>

---

## ✨ What it does

| Feature | Description |
|---|---|
| 🎯 Real-time detection | Runs YOLOv8 inference on every incoming camera frame |
| 🖼️ Annotated output | Publishes a frame with labeled bounding boxes on `/detection_image` |
| 📊 Structured data | Publishes JSON detections (label, confidence, bbox) on `/detections` |
| 🟢 People highlighted | Person detections in green, everything else in blue — obstacles and people are visually distinct at a glance |
| 🎮 Tested with teleop | Drive the robot manually and watch detections update live as the world changes |
| 🔧 Fully configurable | Camera topic, model path, and confidence threshold are all ROS2 parameters — no code changes needed to point it at a different robot |

---

## 🧰 Built with

<div align="center">

![ROS2](https://img.shields.io/badge/-ROS2_Humble-22314E?style=flat-square&logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/-Python_3.10-3776AB?style=flat-square&logo=python&logoColor=white)
![Ultralytics](https://img.shields.io/badge/-Ultralytics_YOLOv8-111111?style=flat-square)
![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![Gazebo](https://img.shields.io/badge/-Gazebo_Classic-F58220?style=flat-square&logo=gazebo&logoColor=white)

</div>

---

## 📁 Project structure

```
robot_object_detection_yolo/
│
├── 📄 README.md
├── 📄 package.xml
├── 📄 setup.py
├── 📄 setup.cfg
├── 🚀 run_detector.sh              ← the script you'll actually run
├── 🙈 .gitignore
│
├── 📂 robot_object_detection_yolo/
│   └── 🐍 detector_node.py         ← the brain of the operation
│
├── 📂 launch/
│   └── 🚀 detector_launch.py
│
├── 📂 models/
│   └── 🧠 yolov8n.pt               (downloaded separately, not in git)
│
├── 📂 images/                      ← the screenshots you're looking at above
│
└── 📂 test/
```

---

## ⚙️ How it actually works

The node sits in a constant loop: a frame comes in on the camera topic, YOLOv8 looks at it, and for everything it recognizes, two things happen at once.

First, a copy of the frame gets a bounding box and label drawn on it — green for people, blue for anything else — and that gets republished as a regular image on `/detection_image`, so you can just open `rqt_image_view` and watch it like a video feed.

Second, every single detection gets boiled down into a tiny JSON object — label, confidence score, bounding box coordinates — and all of those get bundled together and published on `/detections`. This is the part other systems would actually plug into. A navigation stack could read it to avoid people. A logging node could read it to build a record of what the robot has seen over time. Nothing downstream needs to touch a single pixel of image data.

Three parameters control everything, so the same node works on a completely different robot without editing a line of code:

- **`camera_topic`** — which topic to subscribe to (defaults to `/camera/image_raw`)
- **`model_path`** — where the YOLOv8 weights live
- **`confidence_threshold`** — how sure the model needs to be before it reports something (defaults to `0.5`)

---

## 🛠️ Setup

### What you'll need

- 🐧 Ubuntu 22.04
- 🤖 ROS2 Humble
- 🐍 Python 3.10
- 🎮 Gazebo Classic (for simulation)

### 1️⃣ Clone it into a workspace

```bash
mkdir -p ~/yolo_ws/src
cd ~/yolo_ws/src
git clone https://github.com/shiavm17/Robot-Object-Detection-YOLO.git robot_object_detection_yolo
```

### 2️⃣ Set up a virtual environment

ROS2's own Python packages need to stay visible alongside YOLOv8's, so the venv is built with `--system-site-packages`:

```bash
cd ~/yolo_ws
python3 -m venv --system-site-packages venv_yolo
source venv_yolo/bin/activate
pip install --upgrade pip
pip install --upgrade --force-reinstall numpy==1.26.4 matplotlib pyparsing opencv-python ultralytics
```

> 💡 **Why pin numpy?** The system's matplotlib and ROS2's `cv_bridge` were both built against NumPy 1.x. Run them under NumPy 2.x and you'll hit `AttributeError: _ARRAY_API not found`. Pinning `numpy==1.26.4` inside the venv sidesteps the whole mess without touching anything system-wide.

### 3️⃣ Grab the YOLOv8 weights

```bash
cd ~/yolo_ws/src/robot_object_detection_yolo
mkdir -p models
python3 -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
mv yolov8n.pt models/
```

### 4️⃣ Build it

```bash
cd ~/yolo_ws
source /opt/ros/humble/setup.bash
source venv_yolo/bin/activate
colcon build --packages-select robot_object_detection_yolo
```

---

## ▶️ Running the detector

Here's a quirk worth knowing about: `colcon build` generates the installed executable with a shebang pointing at the *system* Python, not your virtual environment — even if the venv was active while building. So `ros2 run` on its own won't be able to find `ultralytics` or `cv2`.

The fix is `run_detector.sh`, a small wrapper that activates the venv first and then runs the node directly:

```bash
#!/bin/bash
source /home/shivam/yolo_ws/venv_yolo/bin/activate
exec python3 /home/shivam/yolo_ws/install/robot_object_detection_yolo/lib/python3.10/site-packages/robot_object_detection_yolo/detector_node.py "$@"
```

Just run it:

```bash
~/yolo_ws/src/robot_object_detection_yolo/run_detector.sh
```

Pointing it at a specific topic (the TortoiseBot used for testing publishes on `/raspberrypi_camera/image_raw`, not the default):

```bash
~/yolo_ws/src/robot_object_detection_yolo/run_detector.sh --ros-args -p camera_topic:=/raspberrypi_camera/image_raw
```

---

## 🚦 Running the full simulation, start to finish

This is the exact sequence that produced the screenshots above. Six terminals, each doing one job.

<table>
<tr><th>Terminal</th><th>Purpose</th><th>Command</th></tr>
<tr>
<td>1️⃣</td>
<td>Robot state publisher</td>
<td>

```bash
source /opt/ros/humble/setup.bash
source ~/tortoisebot_ws/install/setup.bash
ros2 launch tortoisebot_description state_publisher.launch.py use_sim_time:=True
```

</td>
</tr>
<tr>
<td>2️⃣</td>
<td>Gazebo world + robot spawn</td>
<td>

```bash
source /opt/ros/humble/setup.bash
source ~/tortoisebot_ws/install/setup.bash
ros2 launch tortoisebot_gazebo gazebo.launch.py
```

</td>
</tr>
<tr>
<td>3️⃣</td>
<td>YOLOv8 detector</td>
<td>

```bash
source /opt/ros/humble/setup.bash
~/yolo_ws/src/robot_object_detection_yolo/run_detector.sh \
  --ros-args -p camera_topic:=/raspberrypi_camera/image_raw
```

</td>
</tr>
<tr>
<td>4️⃣</td>
<td>Live detection viewer</td>
<td>

```bash
source /opt/ros/humble/setup.bash
ros2 run rqt_image_view rqt_image_view
```
*(select `/detection_image` from the dropdown)*

</td>
</tr>
<tr>
<td>5️⃣</td>
<td>Drive the robot</td>
<td>

```bash
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

</td>
</tr>
<tr>
<td>6️⃣</td>
<td>Raw detection feed <i>(optional)</i></td>
<td>

```bash
source /opt/ros/humble/setup.bash
ros2 topic echo /detections
```

</td>
</tr>
</table>

> ⚠️ **Order matters.** Always start the state publisher *before* Gazebo. Spawning the robot depends on `/robot_description` already having a publisher — launch Gazebo too early and the robot just never appears in the world.

---

## 🐛 Things that went wrong (and how they got fixed)

Building this wasn't a straight line, so here's the real troubleshooting log — genuinely useful if you're setting this up yourself and hit the same walls.

<details>
<summary><b>🔴 NumPy 1.x vs 2.x — <code>AttributeError: _ARRAY_API not found</code></b></summary>
<br>

Ultralytics pulls in matplotlib, which on this system resolved to an old apt-installed build compiled against NumPy 1.x. NumPy 2.x breaks it instantly. **Fix:** pin `numpy==1.26.4` inside a dedicated virtual environment, leaving system packages untouched.
</details>

<details>
<summary><b>🔴 The installed node crashes with the same NumPy error, even after fixing the venv</b></summary>
<br>

`colcon build` writes the installed executable's shebang as `/usr/bin/python3`, ignoring whatever virtual environment was active during the build. **Fix:** `run_detector.sh` sidesteps the generated executable entirely and calls the node's `.py` file directly through the venv's own Python.
</details>

<details>
<summary><b>🔴 Robot never appears in Gazebo, camera topic never publishes anything</b></summary>
<br>

`spawn_entity` waits for a robot description on `/robot_description` before it'll place anything in the world. Launch Gazebo before that topic has a publisher, and the spawn step waits forever with nothing to spawn. **Fix:** always confirm `ros2 topic info /robot_description` shows at least one publisher before launching Gazebo.
</details>

<details>
<summary><b>🔴 robot_state_publisher loads fine but never actually publishes</b></summary>
<br>

Some launch files default `use_sim_time` to `False`, which quietly switches the state publisher onto a real-hardware URDF branch instead of the simulation one. **Fix:** always pass `use_sim_time:=True` explicitly when launching for simulation.
</details>

<details>
<summary><b>🔴 <code>Address already in use</code> when relaunching Gazebo</b></summary>
<br>

`Ctrl+C` doesn't always fully kill `gzserver`/`gzclient`, leaving the network port held by a zombie process. **Fix:**

```bash
pkill -9 -f gzserver
pkill -9 -f gzclient
pkill -9 -f gazebo
```
</details>

---

## 🚀 What's next

- [ ] Migrate from Gazebo Classic to Gazebo Ignition/Garden
- [ ] Fuse LiDAR scans with camera detections for true obstacle avoidance
- [ ] Feed detections into the navigation stack for reactive path planning
- [ ] Train a custom YOLOv8 model on robot-specific object classes
- [ ] Deploy on real TortoiseBot hardware with a Raspberry Pi camera
- [ ] Auto-switch between sim and real camera topics with a single launch arg

---

## 📜 License

MIT — use it, fork it, build on it.

<div align="center">

*A robotics and computer vision portfolio project — built, broken, and fixed one terminal tab at a time.* 🛠️

</div>
