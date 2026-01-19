# Crux35 Autonomous 3DGS Capture System

## Your Build Specifications

| Component | Model | Weight |
|-----------|-------|--------|
| Frame | Happymodel Crux35 | 26g |
| Motors (x4) | T-Motor F1404 3800kv | 37.4g (9.34g each w/cable) |
| Props | HQProp T3.5x2.5x3 | ~5g |
| FC/ESC | MicoAir743-AIO-35A | ~10g |
| Battery | 4S 850mAh GNB HiLV | 75g |
| Wiring/misc | | ~5g |
| **Base Total** | | **~158g** |

## Payload Budget

```
Total limit:        250g
Base drone:        -158g
─────────────────────────
Available payload:   92g
```

---

## Requirements Analysis

### 1. Autonomous Position Hold + Waypoints
**Required:** GPS module (outdoor) or Optical Flow (indoor)

PX4 needs position feedback for:
- Stable hover (POSITION mode)
- Waypoint missions (AUTO.MISSION)
- Return to home (RTL)

### 2. Optimal 3DGS Capture Positions
**Required:** Pre-planned mission OR companion computer

Options:
- **A) Pre-planned in QGroundControl** - Define capture waypoints manually
- **B) Companion computer** - Pi Zero calculates optimal viewpoints
- **C) Hybrid** - Upload mission template, execute autonomously

### 3. High Quality Frames for Splats
**Required:** Good camera with known characteristics

Needs:
- Sufficient resolution (12MP+ ideal)
- Global shutter preferred (or very stable gimbal)
- Sharp optics
- Triggered capture at waypoints

### 4. Accurate Extrinsics (Camera Poses)
**Required:** Precise position + orientation

Sources:
- PX4 EKF2 state estimate (position, attitude)
- GPS for absolute position
- IMU for orientation
- Optional: RTK for cm-level accuracy

### 5. Camera Intrinsics
**Required:** Pre-calibration

- Calibrate camera before flights
- Store calibration file (focal length, principal point, distortion)
- Apply in COLMAP processing

---

## Payload Design

### Option A: Minimal Viable (~55g) ✓ RECOMMENDED

| Component | Weight | Cost | Purpose |
|-----------|--------|------|---------|
| Matek M10Q-5883 GPS | 8g | $25 | Position hold + heading |
| Arducam 16MP Global Shutter | 5g | $50 | Sharp images |
| Pololu 5V regulator | 1g | $5 | Camera power |
| Custom mount (3D print) | 5g | $2 | Integration |
| Wiring | 3g | - | |
| **Total** | **22g** | **$82** | |

**Remaining margin: 92 - 22 = 70g spare**

This leaves room for:
- Data logging (microSD in camera)
- Or companion computer later
- Or larger battery swap

### Option B: With Companion Computer (~65g)

| Component | Weight | Cost | Purpose |
|-----------|--------|------|---------|
| Matek M10Q-5883 GPS | 8g | $25 | Position hold |
| Arducam 16MP Global Shutter | 5g | $50 | Capture |
| **Seeed XIAO ESP32S3** | 3g | $15 | Companion (triggers + logging) |
| MicroSD module | 2g | $5 | Data storage |
| Wiring/mount | 7g | $5 | |
| **Total** | **25g** | **$100** | |

**Remaining margin: 92 - 25 = 67g spare**

### Option C: Maximum Capability (~70g)

| Component | Weight | Cost | Purpose |
|-----------|--------|------|---------|
| **u-blox ZED-F9P RTK** | 12g | $180 | cm-level position |
| RTK antenna (patch) | 8g | $30 | |
| Arducam 16MP GS | 5g | $50 | Capture |
| Seeed XIAO ESP32S3 | 3g | $15 | Companion |
| MicroSD | 2g | $5 | Storage |
| Wiring/mount | 10g | $10 | |
| **Total** | **40g** | **$290** | |

**Remaining margin: 92 - 40 = 52g spare**

---

## Recommended Configuration

### Hardware Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    CRUX35 3DGS CAPTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│     ┌─────────────────────────────────────────────────┐     │
│     │           Matek M10Q-5883 GPS (8g)              │     │
│     │    • u-blox M10 GNSS (2.5m CEP accuracy)        │     │
│     │    • QMC5883L compass                           │     │
│     │    • I2C + UART interface                       │     │
│     └─────────────────────────────────────────────────┘     │
│                            │                                 │
│                       UART + I2C                             │
│                            │                                 │
│     ┌─────────────────────────────────────────────────┐     │
│     │         MicoAir743-AIO-35A (PX4)                │     │
│     │    • STM32H743 @ 480MHz                         │     │
│     │    • BMI088 + BMI270 dual IMU                   │     │
│     │    • DPS310 barometer                           │     │
│     │    • 7x UART available                          │     │
│     └─────────────────────────────────────────────────┘     │
│                            │                                 │
│                     UART (MAVLink)                           │
│                            │                                 │
│     ┌─────────────────────────────────────────────────┐     │
│     │      Seeed XIAO ESP32S3 Companion (3g)          │     │
│     │    • Receives pose from PX4 via MAVLink         │     │
│     │    • Triggers camera at waypoints               │     │
│     │    • Logs pose + timestamp to SD                │     │
│     │    • Optional: WiFi telemetry                   │     │
│     └─────────────────────────────────────────────────┘     │
│                            │                                 │
│                       GPIO trigger                           │
│                            │                                 │
│     ┌─────────────────────────────────────────────────┐     │
│     │      Arducam 16MP Global Shutter (5g)           │     │
│     │    • IMX296 sensor                              │     │
│     │    • 1440 x 1080 @ 60fps (or 16MP stills)       │     │
│     │    • Global shutter - no motion blur            │     │
│     │    • External trigger input                     │     │
│     │    • Onboard ISP + microSD recording            │     │
│     └─────────────────────────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Weight Summary

| Component | Weight |
|-----------|--------|
| Crux35 frame | 26g |
| T-Motor F1404 x4 | 37g |
| HQProp T3.5x2.5x3 | 5g |
| MicoAir743-AIO-35A | 10g |
| GNB 4S 850mAh HiLV | 75g |
| Base wiring | 5g |
| **Base subtotal** | **158g** |
| | |
| Matek M10Q-5883 GPS | 8g |
| Arducam 16MP GS | 5g |
| XIAO ESP32S3 + SD | 5g |
| Payload wiring/mount | 8g |
| **Payload subtotal** | **26g** |
| | |
| **TOTAL** | **184g** ✓ |

**66g under limit** - plenty of margin for adjustments

---

## PX4 Configuration

### GPS Setup

```yaml
# QGroundControl Parameters

# GPS
GPS_1_CONFIG: TELEM2  # or whichever UART you use
GPS_1_GNSS: 127       # All constellations

# EKF2 (state estimation)
EKF2_GPS_CTRL: 7      # Use GPS for position + velocity
EKF2_HGT_REF: 1       # Use GPS for height reference
EKF2_MAG_TYPE: 1      # Use external compass

# Position controller
MPC_XY_P: 0.95        # Position P gain (tune for stability)
MPC_Z_P: 1.0          # Altitude P gain
MPC_XY_VEL_MAX: 5.0   # Max horizontal velocity (m/s)

# Mission settings
MIS_TAKEOFF_ALT: 5.0  # Default takeoff altitude
NAV_ACC_RAD: 2.0      # Waypoint acceptance radius (m)
```

### Flight Modes Needed

| Mode | Purpose | Trigger |
|------|---------|---------|
| POSITION | Stable hover at current location | RC switch |
| AUTO.MISSION | Execute waypoint mission | RC switch |
| AUTO.LOITER | Hold at waypoint during capture | Automatic |
| RTL | Return home | RC switch / failsafe |

---

## Autonomous 3DGS Capture Workflow

### Mission Planning (Pre-flight)

#### Step 1: Define Target Area

```
Target: Building or object to scan
Size: e.g., 10m x 10m x 5m tall

         N
         │
    ┌────┴────┐
    │         │
 W──┤ TARGET  ├──E
    │         │
    └────┬────┘
         │
         S
```

#### Step 2: Calculate Optimal Viewpoints

For 3DGS, you need:
- 360° coverage (or at least 180° for facades)
- Multiple altitude bands
- 70-80% image overlap
- Oblique angles (not just nadir)

**Hemispherical pattern example:**

```python
# generate_3dgs_waypoints.py
import math

def generate_hemisphere_waypoints(
    center_lat, center_lon,
    radius=10,           # meters from target
    altitude_start=3,    # meters AGL
    altitude_end=15,
    altitude_steps=4,
    azimuth_steps=12     # 30° increments = 12 positions per ring
):
    """
    Generate waypoints in hemisphere around target
    Returns list of (lat, lon, alt, yaw) tuples
    """
    waypoints = []

    for alt in np.linspace(altitude_start, altitude_end, altitude_steps):
        # Adjust radius based on altitude (closer at top)
        ring_radius = radius * (1 - (alt - altitude_start) / (altitude_end - altitude_start) * 0.5)

        for i in range(azimuth_steps):
            azimuth = (360 / azimuth_steps) * i

            # Calculate position
            dx = ring_radius * math.sin(math.radians(azimuth))
            dy = ring_radius * math.cos(math.radians(azimuth))

            # Convert to lat/lon (approximate for small distances)
            lat = center_lat + (dy / 111320)
            lon = center_lon + (dx / (111320 * math.cos(math.radians(center_lat))))

            # Yaw points toward center
            yaw = (azimuth + 180) % 360

            waypoints.append({
                'lat': lat,
                'lon': lon,
                'alt': alt,
                'yaw': yaw,
                'action': 'CAPTURE'
            })

    return waypoints

# Example: Generate 48 waypoints (4 altitudes × 12 azimuths)
waypoints = generate_hemisphere_waypoints(
    center_lat=51.5074,
    center_lon=-0.1278,
    radius=10,
    altitude_start=3,
    altitude_end=12,
    altitude_steps=4,
    azimuth_steps=12
)
```

#### Step 3: Export to QGroundControl Mission

```python
def export_to_qgc_plan(waypoints, filename="3dgs_mission.plan"):
    """Export waypoints to QGroundControl .plan format"""

    mission = {
        "fileType": "Plan",
        "geoFence": {"circles": [], "polygons": []},
        "groundStation": "QGroundControl",
        "mission": {
            "cruiseSpeed": 3,
            "firmwareType": 12,  # PX4
            "items": [],
            "plannedHomePosition": [waypoints[0]['lat'], waypoints[0]['lon'], 0]
        },
        "version": 1
    }

    # Add takeoff
    mission["mission"]["items"].append({
        "command": 22,  # NAV_TAKEOFF
        "coordinate": [waypoints[0]['lat'], waypoints[0]['lon'], 5],
        "type": "SimpleItem"
    })

    # Add waypoints with camera trigger
    for i, wp in enumerate(waypoints):
        # Waypoint
        mission["mission"]["items"].append({
            "command": 16,  # NAV_WAYPOINT
            "coordinate": [wp['lat'], wp['lon'], wp['alt']],
            "param4": wp['yaw'],  # Yaw angle
            "type": "SimpleItem"
        })

        # Hold and trigger camera
        mission["mission"]["items"].append({
            "command": 2000,  # DO_DIGICAM_TRIGGER (or MAV_CMD_IMAGE_START_CAPTURE)
            "type": "SimpleItem"
        })

    # Add RTL
    mission["mission"]["items"].append({
        "command": 20,  # NAV_RETURN_TO_LAUNCH
        "type": "SimpleItem"
    })

    with open(filename, 'w') as f:
        json.dump(mission, f, indent=2)

    return filename
```

### In-Flight Execution

```
┌──────────────────────────────────────────────────────────────┐
│                    FLIGHT SEQUENCE                            │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1. PRE-ARM                                                   │
│     └─► GPS lock acquired (>8 satellites)                    │
│     └─► Compass calibrated                                   │
│     └─► Battery check                                        │
│                                                               │
│  2. TAKEOFF (AUTO)                                           │
│     └─► Climb to mission start altitude                      │
│                                                               │
│  3. EXECUTE MISSION                                          │
│     For each waypoint:                                        │
│     ┌─────────────────────────────────────────────────────┐  │
│     │  a. Fly to waypoint position                        │  │
│     │  b. Rotate to target yaw                            │  │
│     │  c. LOITER (hold position)                          │  │
│     │  d. Wait for stability (1-2 seconds)                │  │
│     │  e. TRIGGER CAMERA                                  │  │
│     │  f. Log pose + timestamp                            │  │
│     │  g. Proceed to next waypoint                        │  │
│     └─────────────────────────────────────────────────────┘  │
│                                                               │
│  4. RTL                                                       │
│     └─► Return to launch point                               │
│     └─► Land                                                 │
│                                                               │
│  5. POST-FLIGHT                                              │
│     └─► Download images from camera SD                       │
│     └─► Download pose log from companion                     │
│     └─► Process in COLMAP with known poses                   │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Companion Computer Code (ESP32)

### Camera Trigger + Pose Logging

```cpp
// companion_3dgs.ino - ESP32S3 companion for PX4 3DGS capture

#include <MAVLink.h>
#include <SD.h>

#define CAMERA_TRIGGER_PIN 2
#define PX4_SERIAL Serial1
#define LOG_FILE "/poses.csv"

// Current pose from PX4
struct Pose {
    uint64_t timestamp_us;
    float lat, lon, alt;          // Position (GPS)
    float roll, pitch, yaw;       // Attitude (radians)
    float vx, vy, vz;             // Velocity
    uint32_t image_id;
} currentPose;

File logFile;
uint32_t imageCounter = 0;

void setup() {
    Serial.begin(115200);
    PX4_SERIAL.begin(57600);  // MAVLink default

    pinMode(CAMERA_TRIGGER_PIN, OUTPUT);
    digitalWrite(CAMERA_TRIGGER_PIN, LOW);

    // Initialize SD card
    if (!SD.begin()) {
        Serial.println("SD init failed!");
        return;
    }

    // Create log file with header
    logFile = SD.open(LOG_FILE, FILE_WRITE);
    logFile.println("image_id,timestamp_us,lat,lon,alt,roll,pitch,yaw,vx,vy,vz");
    logFile.close();
}

void loop() {
    // Read MAVLink messages from PX4
    while (PX4_SERIAL.available()) {
        mavlink_message_t msg;
        mavlink_status_t status;

        uint8_t c = PX4_SERIAL.read();
        if (mavlink_parse_char(MAVLINK_COMM_0, c, &msg, &status)) {
            handleMAVLinkMessage(&msg);
        }
    }
}

void handleMAVLinkMessage(mavlink_message_t* msg) {
    switch (msg->msgid) {
        case MAVLINK_MSG_ID_GLOBAL_POSITION_INT: {
            mavlink_global_position_int_t pos;
            mavlink_msg_global_position_int_decode(msg, &pos);

            currentPose.timestamp_us = pos.time_boot_ms * 1000;
            currentPose.lat = pos.lat / 1e7;
            currentPose.lon = pos.lon / 1e7;
            currentPose.alt = pos.alt / 1000.0;
            currentPose.vx = pos.vx / 100.0;
            currentPose.vy = pos.vy / 100.0;
            currentPose.vz = pos.vz / 100.0;
            break;
        }

        case MAVLINK_MSG_ID_ATTITUDE: {
            mavlink_attitude_t att;
            mavlink_msg_attitude_decode(msg, &att);

            currentPose.roll = att.roll;
            currentPose.pitch = att.pitch;
            currentPose.yaw = att.yaw;
            break;
        }

        case MAVLINK_MSG_ID_CAMERA_TRIGGER: {
            // PX4 commanded a camera trigger
            triggerCameraAndLog();
            break;
        }
    }
}

void triggerCameraAndLog() {
    // Trigger camera (pulse)
    digitalWrite(CAMERA_TRIGGER_PIN, HIGH);
    delayMicroseconds(100);  // 100μs pulse
    digitalWrite(CAMERA_TRIGGER_PIN, LOW);

    // Log pose with image ID
    currentPose.image_id = imageCounter++;

    logFile = SD.open(LOG_FILE, FILE_APPEND);
    logFile.printf("%u,%llu,%.7f,%.7f,%.3f,%.6f,%.6f,%.6f,%.3f,%.3f,%.3f\n",
        currentPose.image_id,
        currentPose.timestamp_us,
        currentPose.lat,
        currentPose.lon,
        currentPose.alt,
        currentPose.roll,
        currentPose.pitch,
        currentPose.yaw,
        currentPose.vx,
        currentPose.vy,
        currentPose.vz
    );
    logFile.close();

    Serial.printf("Captured image %u at %.7f, %.7f\n",
        currentPose.image_id, currentPose.lat, currentPose.lon);
}
```

---

## Post-Flight Processing

### Step 1: Convert Pose Log to COLMAP Format

```python
# poses_to_colmap.py
import csv
import numpy as np
from scipy.spatial.transform import Rotation
import pyproj

def poses_to_colmap(pose_csv, camera_yaml, output_dir):
    """
    Convert PX4 pose log + camera calibration to COLMAP format
    """

    # Load camera intrinsics
    with open(camera_yaml) as f:
        intrinsics = yaml.safe_load(f)

    fx = intrinsics['fx']
    fy = intrinsics['fy']
    cx = intrinsics['cx']
    cy = intrinsics['cy']
    width = intrinsics['width']
    height = intrinsics['height']
    k1, k2, p1, p2 = intrinsics['distortion']

    # Write cameras.txt
    with open(f"{output_dir}/cameras.txt", 'w') as f:
        f.write("# Camera list with one line of data per camera:\n")
        f.write("# CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]\n")
        f.write(f"1 OPENCV {width} {height} {fx} {fy} {cx} {cy} {k1} {k2} {p1} {p2}\n")

    # Convert GPS to local coordinates
    poses = []
    with open(pose_csv) as f:
        reader = csv.DictReader(f)
        poses = list(reader)

    # Use first pose as origin
    origin_lat = float(poses[0]['lat'])
    origin_lon = float(poses[0]['lon'])
    origin_alt = float(poses[0]['alt'])

    # Project to local ENU coordinates
    proj = pyproj.Proj(proj='aeqd', lat_0=origin_lat, lon_0=origin_lon)

    # Write images.txt
    with open(f"{output_dir}/images.txt", 'w') as f:
        f.write("# Image list with two lines of data per image:\n")
        f.write("# IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME\n")

        for pose in poses:
            img_id = int(pose['image_id'])

            # Convert GPS to local XYZ
            x, y = proj(float(pose['lon']), float(pose['lat']))
            z = float(pose['alt']) - origin_alt

            # Get rotation from roll/pitch/yaw
            roll = float(pose['roll'])
            pitch = float(pose['pitch'])
            yaw = float(pose['yaw'])

            # PX4 uses NED frame, convert to camera frame
            # This depends on your camera mounting orientation
            R_body = Rotation.from_euler('xyz', [roll, pitch, yaw])
            R_cam = R_body  # Adjust based on camera mount

            # COLMAP uses world-to-camera transform
            R_w2c = R_cam.inv()
            t_w2c = -R_w2c.as_matrix() @ np.array([x, y, z])

            # Quaternion (w, x, y, z)
            q = R_w2c.as_quat()  # Returns (x, y, z, w)
            qw, qx, qy, qz = q[3], q[0], q[1], q[2]

            f.write(f"{img_id} {qw} {qx} {qy} {qz} {t_w2c[0]} {t_w2c[1]} {t_w2c[2]} 1 IMG_{img_id:04d}.jpg\n")
            f.write("\n")  # Empty line for 2D points

    # Write empty points3D.txt (COLMAP will compute from images)
    with open(f"{output_dir}/points3D.txt", 'w') as f:
        f.write("# 3D point list (empty - will be computed by COLMAP)\n")

    print(f"Exported {len(poses)} poses to COLMAP format")

# Usage
poses_to_colmap(
    pose_csv="poses.csv",
    camera_yaml="arducam_16mp_calibration.yaml",
    output_dir="colmap_input/sparse/0"
)
```

### Step 2: Run COLMAP with Known Poses

```bash
# Use poses as initial estimate, refine with bundle adjustment

# Option A: Trust poses completely (skip feature matching)
colmap image_undistorter \
    --image_path images/ \
    --input_path colmap_input/sparse/0 \
    --output_path colmap_output/

# Option B: Use poses as prior, refine with BA (recommended)
colmap feature_extractor \
    --database_path database.db \
    --image_path images/

colmap exhaustive_matcher \
    --database_path database.db

colmap point_triangulator \
    --database_path database.db \
    --image_path images/ \
    --input_path colmap_input/sparse/0 \
    --output_path colmap_refined/sparse/0

colmap bundle_adjuster \
    --input_path colmap_refined/sparse/0 \
    --output_path colmap_refined/sparse/0
```

### Step 3: Train 3DGS

```bash
# Using refined COLMAP output
python train.py \
    -s colmap_refined/ \
    -m output/ \
    --iterations 30000
```

---

## Camera Calibration (One-Time Setup)

### Calibrate Arducam 16MP Global Shutter

```python
# calibrate_camera.py
import cv2
import numpy as np
import glob
import yaml

# Checkerboard dimensions
CHECKERBOARD = (9, 6)
SQUARE_SIZE = 0.025  # 25mm squares

# Termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE

objpoints = []  # 3D points
imgpoints = []  # 2D points

# Load calibration images
images = glob.glob('calibration_images/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

# Calibrate
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

# Calculate reprojection error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    mean_error += error

print(f"Reprojection error: {mean_error / len(objpoints):.4f} pixels")

# Save calibration
calibration = {
    'width': gray.shape[1],
    'height': gray.shape[0],
    'fx': float(mtx[0, 0]),
    'fy': float(mtx[1, 1]),
    'cx': float(mtx[0, 2]),
    'cy': float(mtx[1, 2]),
    'distortion': [float(d) for d in dist[0][:4]],  # k1, k2, p1, p2
    'reprojection_error': mean_error / len(objpoints)
}

with open('arducam_16mp_calibration.yaml', 'w') as f:
    yaml.dump(calibration, f)

print("Calibration saved to arducam_16mp_calibration.yaml")
```

---

## Parts List

| Part | Model | Weight | Price | Link |
|------|-------|--------|-------|------|
| GPS | Matek M10Q-5883 | 8g | $25 | [GetFPV](https://www.getfpv.com/matek-m10q-5883-gps-compass.html) |
| Camera | Arducam 16MP IMX519 AF | 5g | $30 | [Amazon](https://www.amazon.com/Arducam-Raspberry-Autofocus-Motorized-Megapixel/dp/B09SL5P2KT) |
| **OR Camera** | Arducam Global Shutter | 5g | $50 | [Arducam](https://www.arducam.com/product/arducam-2mp-global-shutter-ov2311-mono-camera-module-for-raspberry-pi/) |
| Companion | Seeed XIAO ESP32S3 | 3g | $15 | [Seeed](https://www.seeedstudio.com/XIAO-ESP32S3-p-5627.html) |
| SD Module | MicroSD breakout | 2g | $5 | Generic |
| Regulator | Pololu 5V 500mA | 1g | $5 | [Pololu](https://www.pololu.com/product/2843) |
| **Total** | | **~24g** | **~$80-100** | |

---

## Final Weight Check

| Component | Weight |
|-----------|--------|
| Crux35 frame | 26g |
| T-Motor F1404 x4 | 37g |
| HQProp T3.5x2.5x3 | 5g |
| MicoAir743-AIO-35A | 10g |
| GNB 4S 850mAh | 75g |
| Base wiring | 5g |
| GPS (M10Q-5883) | 8g |
| Camera (Arducam) | 5g |
| Companion (XIAO) | 5g |
| Payload wiring/mount | 8g |
| **TOTAL** | **184g** ✓ |

**66g under 250g limit** - mission accomplished!

---

## Upgrade Path

If you need more accuracy later:

| Upgrade | Weight Add | Cost | Benefit |
|---------|------------|------|---------|
| RTK GPS (F9P) | +7g | +$180 | cm-level position |
| 2nd camera (stereo) | +5g | +$30 | Depth estimation |
| Better camera | +0g | +$50 | Higher resolution |
| Pi Zero 2W | +10g | +$15 | More compute |

Even with all upgrades: ~206g - still under 250g
