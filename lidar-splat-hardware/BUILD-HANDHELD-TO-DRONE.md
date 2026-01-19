# Practical Build: Handheld → Drone Scanner

Your requirements:
- Indoor AND outdoor
- Correct position and scale relative to world
- Capture intrinsics/extrinsics for better COLMAP
- Depth data for better point cloud before splat generation
- Start handheld, eventually mount on drone

---

## Recommended Architecture

### Phase 1: Handheld Prototype (~$2,500)

```
┌────────────────────────────────────────────────────────┐
│              HANDHELD SCANNER v1                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │              Livox Mid-360                        │ │
│  │         (LiDAR + Built-in IMU)                   │ │
│  │    - 40m range, 360° x 59° FOV                   │ │
│  │    - 200k pts/s                                  │ │
│  │    - Built-in 6-axis IMU                         │ │
│  │    - Hardware sync (PPS input)                   │ │
│  └──────────────────────────────────────────────────┘ │
│                        │                               │
│                   PPS sync                             │
│                        │                               │
│  ┌──────────────────────────────────────────────────┐ │
│  │         Global Shutter Camera                     │ │
│  │    - FLIR Blackfly S (BFS-U3-16S2C)              │ │
│  │    - or: Intel D455 (includes depth)             │ │
│  │    - External trigger input                      │ │
│  └──────────────────────────────────────────────────┘ │
│                        │                               │
│                        ▼                               │
│  ┌──────────────────────────────────────────────────┐ │
│  │              Laptop / Jetson                      │ │
│  │    - Record: ROS2 bag                            │ │
│  │    - Process: FAST-LIVO2                         │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Phase 2: Add Georeferencing (~$500 more)

```
Add: RTK GPS Module
     ├── u-blox ZED-F9P (~$200)
     └── RTK antenna (~$50)

Base station options:
     ├── Your own base (~$300)
     ├── NTRIP service (free-$50/mo)
     └── Survey control points (free)
```

### Phase 3: Drone Mount (~$1,000 more)

```
Lightweight version:
     ├── Livox Mid-360 (265g)
     ├── Wide-angle camera (50g)
     ├── Sync board (20g)
     └── Mounting plate (50g)
         ─────────────
         Total: ~385g

Compatible drones:
     ├── DJI M300/M350 (2.7kg payload)
     ├── Custom build (variable)
     └── DJI Mavic 3 (limited payload)
```

---

## Component Selection

### Option A: Simplest (Intel D455 Only)

**Pros**: Single unit, built-in depth, IMU, pre-calibrated
**Cons**: 6m depth range, no LiDAR scale outdoors

| Part | Model | Cost |
|------|-------|------|
| Depth Camera | Intel RealSense D455 | $400 |
| Mount/Handle | 3D printed | $20 |
| Laptop | Existing | $0 |
| **Total** | | **$420** |

**Best for**: Indoor only, objects, rooms

---

### Option B: Recommended (LiDAR + Camera)

**Pros**: True scale, 40m range, indoor/outdoor, drone-ready
**Cons**: Requires calibration, more complex

| Part | Model | Cost |
|------|-------|------|
| LiDAR | Livox Mid-360 | $1,000 |
| Camera | FLIR Blackfly S BFS-U3-16S2C | $500 |
| Lens | 4mm wide angle (120° FOV) | $50 |
| Sync Board | Teensy 4.1 + custom PCB | $50 |
| IMU | Use Mid-360 built-in | $0 |
| Handle/Frame | 3D printed + aluminum | $50 |
| Cables | USB3, trigger | $30 |
| Laptop | Existing (or Jetson Orin $500) | $0-500 |
| **Total** | | **$1,680-2,180** |

**Add for georeferencing**:
| Part | Model | Cost |
|------|-------|------|
| RTK GPS | SparkFun RTK Express | $500 |
| **or** | u-blox ZED-F9P + antenna | $250 |

---

### Option C: Maximum Quality

**Matches XGRIDS capability more closely**

| Part | Model | Cost |
|------|-------|------|
| LiDAR | Hesai XT32 (used) | $500-2,000 |
| Main Camera | FLIR Blackfly S 5MP GS | $700 |
| Wide Camera | Fisheye (190° FOV) | $300 |
| IMU | Xsens MTi-3 | $400 |
| Sync Board | Custom with PTP | $100 |
| RTK GPS | u-blox ZED-F9P | $200 |
| Compute | Jetson Orin NX | $700 |
| Frame | CNC aluminum | $200 |
| **Total** | | **$3,100-4,600** |

---

## Hardware Time Sync Design

### Why You Need This

Without sync:
```
Time:     0ms    10ms    20ms    30ms
Camera:   ─●─────────────●─────────────●───
LiDAR:    ────●─────────────●─────────────●
IMU:      ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

Problem: Camera frame at 0ms pairs with LiDAR from 10ms
         At 1m/s walking speed = 1cm position error per frame
```

With sync:
```
Time:     0ms    10ms    20ms    30ms
Trigger:  ─●─────────────●─────────────●───
Camera:   ─●─────────────●─────────────●───
LiDAR:    ─●─────────────●─────────────●───
IMU:      ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

All sensors capture at exact same moment
```

### Sync Board Design (Teensy 4.1)

```cpp
// sync_board.ino - Microsecond-precision multi-sensor trigger

#define CAMERA_TRIGGER_PIN 2
#define LIDAR_PPS_PIN 3
#define SYNC_RATE_HZ 10  // 10 fps

IntervalTimer syncTimer;

void setup() {
    pinMode(CAMERA_TRIGGER_PIN, OUTPUT);
    pinMode(LIDAR_PPS_PIN, OUTPUT);

    // Start sync timer
    syncTimer.begin(triggerAllSensors, 1000000 / SYNC_RATE_HZ);
}

void triggerAllSensors() {
    // Simultaneous pulse to all sensors
    digitalWriteFast(CAMERA_TRIGGER_PIN, HIGH);
    digitalWriteFast(LIDAR_PPS_PIN, HIGH);

    delayMicroseconds(100);  // 100μs pulse width

    digitalWriteFast(CAMERA_TRIGGER_PIN, LOW);
    digitalWriteFast(LIDAR_PPS_PIN, LOW);

    // Log timestamp for data association
    Serial.println(micros());
}

void loop() {
    // Handle serial commands for rate adjustment
}
```

### Wiring Diagram

```
                    ┌─────────────────┐
                    │   Teensy 4.1    │
                    │                 │
     USB to PC ────►│ USB             │
                    │                 │
                    │ Pin 2 ──────────┼──► Camera trigger (3.3V GPIO)
                    │                 │
                    │ Pin 3 ──────────┼──► LiDAR PPS input
                    │                 │
                    │ GND ────────────┼──► Common ground
                    │                 │
                    └─────────────────┘
```

---

## Calibration Procedure

### Step 1: Camera Intrinsics

```bash
# Print checkerboard (9x6, 25mm squares)
# Capture 20-30 images from different angles

# Using OpenCV
python calibrate_camera.py --input images/ --output camera_intrinsics.yaml

# Or using Kalibr
kalibr_calibrate_cameras \
    --target checkerboard.yaml \
    --bag camera_calib.bag \
    --models pinhole-radtan \
    --topics /camera/image_raw
```

**Output**: `camera_intrinsics.yaml`
```yaml
camera_matrix:
  - [fx, 0, cx]
  - [0, fy, cy]
  - [0, 0, 1]
distortion_coefficients: [k1, k2, p1, p2, k3]
```

### Step 2: Camera-LiDAR Extrinsics

**Method A: Target-based (more accurate)**

```bash
# Use checkerboard with reflective markers
# Detect in both camera image and LiDAR intensity

# Using lidar_camera_calibration package
roslaunch lidar_camera_calibration calibration.launch
```

**Method B: Feature matching (easier)**

```bash
# Using FAST-Calib (recommended for FAST-LIVO2)
git clone https://github.com/hku-mars/FAST-Calib
cd FAST-Calib
# Follow instructions to collect calibration data
# Outputs extrinsics for FAST-LIVO2 config
```

**Output**: Transform matrix (LiDAR → Camera)
```yaml
extrinsic_T:  # Translation [x, y, z] in meters
  - 0.05
  - 0.0
  - -0.02
extrinsic_R:  # Rotation matrix
  - [1.0, 0.0, 0.0]
  - [0.0, 1.0, 0.0]
  - [0.0, 0.0, 1.0]
```

### Step 3: Verify Calibration

```bash
# Project LiDAR points onto camera image
# Points should align with edges/features

roslaunch verify_calibration project_lidar.launch
```

Good calibration:
```
[LiDAR points overlay on camera image]
- Points align with object edges
- No systematic offset
- Works across entire image
```

---

## Software Pipeline

### Recording (ROS2)

```bash
# Terminal 1: Launch sensors
ros2 launch my_scanner sensors.launch.py

# Terminal 2: Record bag
ros2 bag record \
    /livox/lidar \
    /livox/imu \
    /camera/image_raw \
    /camera/camera_info \
    /gps/fix \
    -o scan_session_001
```

### Processing with FAST-LIVO2

```bash
# Configure sensors in config/my_scanner.yaml
# Set calibrated extrinsics

ros2 launch fast_livo2 mapping.launch.py \
    config:=config/my_scanner.yaml \
    bag:=scan_session_001

# Outputs:
# - Trajectory (poses per frame)
# - Dense colorized point cloud
# - Loop-closure corrected map
```

### Export to COLMAP Format

```python
# convert_to_colmap.py
import numpy as np
from scipy.spatial.transform import Rotation

def export_colmap(trajectory, camera_intrinsics, output_dir):
    """
    Convert SLAM output to COLMAP format for PostShot/3DGS
    """

    # cameras.txt - intrinsics
    with open(f"{output_dir}/cameras.txt", "w") as f:
        f.write("# Camera list with one line of data per camera:\n")
        f.write("# CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]\n")
        fx, fy, cx, cy = camera_intrinsics['focal'], camera_intrinsics['principal']
        f.write(f"1 PINHOLE {width} {height} {fx} {fy} {cx} {cy}\n")

    # images.txt - extrinsics (poses)
    with open(f"{output_dir}/images.txt", "w") as f:
        f.write("# Image list with two lines of data per image:\n")
        f.write("# IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME\n")

        for i, pose in enumerate(trajectory):
            # COLMAP uses world-to-camera transform
            R = pose[:3, :3]
            t = pose[:3, 3]

            # Convert to quaternion (w, x, y, z)
            quat = Rotation.from_matrix(R).as_quat()  # x, y, z, w
            qw, qx, qy, qz = quat[3], quat[0], quat[1], quat[2]

            # COLMAP translation = -R * t
            t_colmap = -R @ t

            f.write(f"{i+1} {qw} {qx} {qy} {qz} {t_colmap[0]} {t_colmap[1]} {t_colmap[2]} 1 frame_{i:06d}.jpg\n")
            f.write("\n")  # Empty line for 2D points (not needed for 3DGS)

    # points3D.txt - use LiDAR point cloud
    # Export dense cloud, or subsample for initialization
```

### 3DGS Training with Depth Supervision

```bash
# Option 1: PostShot with external point cloud
postshot train \
    --input colmap_output/ \
    --point-cloud lidar_cloud.ply \
    --depth-supervision \
    --output splat_output/

# Option 2: Nerfstudio with depth
ns-train splatfacto \
    --data processed/ \
    --pipeline.model.use-depth-loss True \
    --pipeline.model.depth-loss-mult 0.1
```

---

## World Coordinates & Scale

### Method 1: RTK GPS (Outdoor)

```
Setup:
1. RTK base station at known point (or NTRIP)
2. RTK rover on scanner
3. GPS coordinates logged with each frame
4. SLAM initialized with GPS pose

Result:
- Point cloud in WGS84 or local UTM coordinates
- Centimeter-level absolute accuracy
- True scale
```

### Method 2: Ground Control Points (Indoor/Outdoor)

```
Setup:
1. Place 4+ survey targets in scene
2. Measure target positions with total station or tape
3. Scan scene including targets
4. Post-process: align point cloud to control points

Result:
- Point cloud in local coordinate system
- Scale from known distances
- 1-5cm accuracy depending on measurement quality
```

### Method 3: Known Object (Quick & Dirty)

```
Setup:
1. Include object of known size in scan (meter stick, A4 paper)
2. After processing, measure object in point cloud
3. Scale entire cloud by correction factor

Result:
- Correct scale
- No absolute position
- 1-5% accuracy
```

---

## Drone Integration Notes

### Weight Budget (for DJI M300)

```
Max payload: 2.7kg

Your scanner:
├── Livox Mid-360:     265g
├── Camera + lens:     150g
├── Sync board:         20g
├── GPS module:         50g
├── Mounting plate:    100g
├── Cables:             50g
└── ─────────────────────────
    Total:             635g  ✓ Well under limit
```

### Vibration Isolation

```
Drone motors create vibration that degrades:
- Camera images (blur)
- IMU readings (noise)
- LiDAR accuracy (jitter)

Solutions:
1. Rubber dampers between mount and drone
2. Gimbal stabilization for camera
3. Software filtering for IMU
4. Post-process LiDAR noise removal
```

### Flight Planning for 3DGS

```
Optimal capture pattern:

    ┌─────────────────────────┐
    │    ↓    ↓    ↓    ↓    │  Nadir passes (looking down)
    │                         │
    │  ←  ←  ←  ←  ←  ←  ←  │  Return
    │                         │
    │    ↓    ↓    ↓    ↓    │
    └─────────────────────────┘

    Plus oblique passes at 45° angle
    for building facades, etc.

Overlap requirements:
- Forward: 80%
- Side: 70%
- Multiple altitudes if possible
```

---

## Summary: Your Build Path

### Start Here (Week 1-2)

1. **Order**: Livox Mid-360 ($1,000) + laptop cable
2. **Test**: Run Livox ROS2 driver, verify point clouds
3. **Add**: Existing camera or buy FLIR Blackfly ($500)

### Add Sync (Week 3-4)

4. **Build**: Teensy sync board ($50)
5. **Wire**: Connect camera trigger + LiDAR PPS
6. **Verify**: Timestamps align in ROS bag

### Calibrate (Week 4-5)

7. **Intrinsics**: Calibrate camera with checkerboard
8. **Extrinsics**: Run FAST-Calib for LiDAR-camera
9. **Test**: Project LiDAR onto image, verify alignment

### First Scans (Week 5-6)

10. **Indoor**: Test in controlled environment
11. **Process**: Run FAST-LIVO2, get poses + cloud
12. **Export**: Convert to COLMAP → PostShot → 3DGS

### Add GPS (Week 7+)

13. **Order**: RTK module ($200-500)
14. **Integrate**: Add GPS to ROS pipeline
15. **Georeference**: Align to world coordinates

### Drone (Week 8+)

16. **Mount**: Design lightweight mounting plate
17. **Test**: Ground tests with drone props running
18. **Fly**: Short flights, verify data quality

---

## Quick Reference: Key Parameters

```yaml
# FAST-LIVO2 config for your build
common:
    lid_topic: "/livox/lidar"
    imu_topic: "/livox/imu"

lidar:
    lidar_type: 1  # Livox
    scan_line: 4
    blind: 0.5

camera:
    camera_topic: "/camera/image_raw"
    camera_info_topic: "/camera/camera_info"

extrinsic:  # From calibration
    camera_lidar_rotation: [your_values]
    camera_lidar_translation: [your_values]
```

---

## Estimated Total Costs

| Configuration | Components | Cost |
|---------------|------------|------|
| Minimum viable | D455 only | $420 |
| Recommended | Mid-360 + camera + sync | $1,700 |
| With GPS | + RTK module | $2,200 |
| Drone-ready | + mount + compute | $3,000 |
| Maximum | Multi-camera + Hesai | $5,000+ |

All significantly less than XGRIDS ($5,000-30,000) with 70-90% of capability.
