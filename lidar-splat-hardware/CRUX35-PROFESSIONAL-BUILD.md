# Crux35 Professional 3DGS Capture System

## Requirements Summary

- **Stereo cameras** for better splat geometry
- **RTK GPS** for deterministic, repeatable extrinsics
- **Live FPV feed** for monitoring
- **Obstacle avoidance** with adaptive path replanning
- **PX4 autonomy** with companion computer control
- **Sub-250g** total weight

---

## System Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    CRUX35 PROFESSIONAL 3DGS SYSTEM                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         SENSOR SUITE                                 │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │   RTK GPS    │  │   Stereo     │  │   Optical    │              │   │
│  │  │   ZED-F9P    │  │   Cameras    │  │   Flow       │              │   │
│  │  │   + Antenna  │  │   2x OV2311  │  │   PMW3901    │              │   │
│  │  │              │  │              │  │   + VL53L1X  │              │   │
│  │  │  • 1-2cm     │  │  • Depth     │  │              │              │   │
│  │  │  • Absolute  │  │  • 3DGS      │  │  • Indoor    │              │   │
│  │  │    coords    │  │  • Obstacle  │  │  • Backup    │              │   │
│  │  │  • Scale     │  │    detect    │  │    depth     │              │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │   │
│  │         │                 │                 │                       │   │
│  └─────────┼─────────────────┼─────────────────┼───────────────────────┘   │
│            │                 │                 │                            │
│            │            CSI×2│            I2C/SPI                           │
│            │                 │                 │                            │
│  ┌─────────▼─────────────────▼─────────────────▼───────────────────────┐   │
│  │                      RASPBERRY PI CM5                                │   │
│  │                      (4GB + Piunora Carrier)                        │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │   ┌────────────────────────────────────────────────────────────┐   │   │
│  │   │                    SOFTWARE STACK                          │   │   │
│  │   ├────────────────────────────────────────────────────────────┤   │   │
│  │   │                                                            │   │   │
│  │   │  ROS2 Jazzy                                                │   │   │
│  │   │    │                                                       │   │   │
│  │   │    ├── Stereo depth node (disparity → depth)              │   │   │
│  │   │    │                                                       │   │   │
│  │   │    ├── Obstacle detection node                            │   │   │
│  │   │    │     • 3D occupancy grid                              │   │   │
│  │   │    │     • Collision prediction                           │   │   │
│  │   │    │                                                       │   │   │
│  │   │    ├── Path planner node                                  │   │   │
│  │   │    │     • Optimal 3DGS viewpoints                        │   │   │
│  │   │    │     • Obstacle-aware replanning                      │   │   │
│  │   │    │     • Sends waypoints to PX4                         │   │   │
│  │   │    │                                                       │   │   │
│  │   │    ├── Capture node                                       │   │   │
│  │   │    │     • Triggers stereo capture                        │   │   │
│  │   │    │     • Logs RTK pose + timestamp                      │   │   │
│  │   │    │     • Saves to SD                                    │   │   │
│  │   │    │                                                       │   │   │
│  │   │    └── MAVLink bridge                                     │   │   │
│  │   │          • MAVROS / px4_ros_com                           │   │   │
│  │   │          • Sends setpoints                                │   │   │
│  │   │          • Receives state                                 │   │   │
│  │   │                                                            │   │   │
│  │   └────────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  │   ┌────────────────────────────────────────────────────────────┐   │   │
│  │   │                    M.2 AI ACCELERATOR                      │   │   │
│  │   │                    (Coral TPU or Hailo-8L)                 │   │   │
│  │   │                                                            │   │   │
│  │   │    • Real-time stereo depth (RAFT-Stereo)                 │   │   │
│  │   │    • Obstacle classification                               │   │   │
│  │   │    • Semantic segmentation (optional)                      │   │   │
│  │   └────────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  └──────────────────────────────┬──────────────────────────────────────┘   │
│                                 │                                           │
│                            MAVLink                                          │
│                            (UART)                                           │
│                                 │                                           │
│  ┌──────────────────────────────▼──────────────────────────────────────┐   │
│  │                      MicoAir743-AIO-35A (PX4)                        │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                      │   │
│  │  • Receives position setpoints from CM5                             │   │
│  │  • Fuses RTK + IMU + baro for state estimation                     │   │
│  │  • Executes flight control                                          │   │
│  │  • Offboard mode for companion control                              │   │
│  │                                                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         FPV SYSTEM                                   │   │
│  │                                                                      │   │
│  │  Caddx Ant Lite ──► Analog VTX ──► Your goggles/monitor             │   │
│  │  (2g)               (1g)           (ground station)                  │   │
│  │                                                                      │   │
│  │  Purpose: Monitor mission, manual override if needed                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Why RTK Gives You Deterministic Extrinsics

### The Problem Without RTK

```
Flight 1:                          Flight 2:
┌─────────────────────┐            ┌─────────────────────┐
│ GPS says: 51.5074°N │            │ GPS says: 51.5074°N │
│ Actual:   51.50743° │            │ Actual:   51.50738° │
│ Error:    ~3 meters │            │ Error:    ~5 meters │
└─────────────────────┘            └─────────────────────┘
         │                                  │
         ▼                                  ▼
    Splat origin                       Splat origin
    at wrong place                     at DIFFERENT wrong place
         │                                  │
         └──────────┬───────────────────────┘
                    │
                    ▼
         Can't combine splats!
         Scale might differ!
         Positions don't match!
```

### The Solution With RTK

```
Flight 1:                          Flight 2:
┌─────────────────────┐            ┌─────────────────────┐
│ RTK says: 51.507432°│            │ RTK says: 51.507432°│
│ Actual:   51.507431°│            │ Actual:   51.507433°│
│ Error:    ~1-2 cm   │            │ Error:    ~1-2 cm   │
└─────────────────────┘            └─────────────────────┘
         │                                  │
         ▼                                  ▼
    Splat origin                       Splat origin
    at EXACT place                     at SAME exact place
         │                                  │
         └──────────┬───────────────────────┘
                    │
                    ▼
         ✓ Splats align perfectly
         ✓ Scale is always 1:1
         ✓ Can combine, update, re-splat
```

### What RTK Guarantees

| Property | Standard GPS | RTK GPS |
|----------|--------------|---------|
| Position accuracy | 2-5 meters | **1-2 centimeters** |
| Position repeatability | Poor (varies by day) | **Excellent (same every time)** |
| Scale | Unknown (COLMAP guesses) | **Exactly 1 unit = 1 meter** |
| Coordinate system | Arbitrary origin | **Real WGS84 coordinates** |
| Re-splat alignment | Manual, approximate | **Automatic, precise** |

---

## Why Stereo Improves Splats

### Single Camera 3DGS Pipeline

```
Images ──► COLMAP ──► Sparse points ──► 3DGS training
              │
              └── Estimates depth from feature matching
                  (fails in textureless areas)
                  (can create floaters)
```

### Stereo Camera 3DGS Pipeline

```
Left + Right ──► Stereo matching ──► Dense depth map
    │                                      │
    │                                      │ (depth supervision)
    │                                      ▼
    └──────────► COLMAP ──► Sparse points ──► 3DGS training
                                               │
                                               └── Depth loss constrains
                                                   Gaussians to real surfaces
```

### Measured Improvements (from research)

| Metric | Single Camera | Stereo | Improvement |
|--------|---------------|--------|-------------|
| PSNR | 28.5 dB | 30.9 dB | +2.4 dB |
| Geometric accuracy | Baseline | +31% | Significant |
| Floaters | Common | Rare | Much cleaner |
| Textureless surfaces | Fails | Works | Major benefit |

---

## Obstacle Avoidance + Adaptive Planning

### How It Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ADAPTIVE CAPTURE LOOP                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. GENERATE OPTIMAL VIEWPOINTS                                         │
│     │                                                                    │
│     │  Input: Target location, size                                     │
│     │  Output: 48 ideal camera positions (hemisphere pattern)           │
│     │                                                                    │
│     ▼                                                                    │
│  2. FOR EACH VIEWPOINT:                                                 │
│     │                                                                    │
│     ├──► Fly toward viewpoint                                           │
│     │                                                                    │
│     ├──► WHILE flying:                                                  │
│     │    │                                                               │
│     │    ├── Stereo cameras compute depth                               │
│     │    │                                                               │
│     │    ├── Build 3D occupancy grid                                    │
│     │    │                                                               │
│     │    ├── Check: Obstacle in path?                                   │
│     │    │    │                                                          │
│     │    │    ├── NO: Continue to viewpoint                             │
│     │    │    │                                                          │
│     │    │    └── YES: ─────────────────────────────┐                   │
│     │    │                                          │                   │
│     │    │         ┌────────────────────────────────▼────────────────┐  │
│     │    │         │         OBSTACLE RESPONSE                       │  │
│     │    │         ├─────────────────────────────────────────────────┤  │
│     │    │         │                                                 │  │
│     │    │         │  Option A: Path around obstacle                 │  │
│     │    │         │            (if clear route exists)              │  │
│     │    │         │                                                 │  │
│     │    │         │  Option B: Modify viewpoint                     │  │
│     │    │         │            (shift position slightly)            │  │
│     │    │         │                                                 │  │
│     │    │         │  Option C: Skip viewpoint                       │  │
│     │    │         │            (add compensating viewpoint later)   │  │
│     │    │         │                                                 │  │
│     │    │         │  Option D: Hover and wait                       │  │
│     │    │         │            (if obstacle is moving)              │  │
│     │    │         │                                                 │  │
│     │    │         └─────────────────────────────────────────────────┘  │
│     │    │                                                               │
│     │    └── Continue flight                                            │
│     │                                                                    │
│     ├──► Arrive at viewpoint (or modified position)                     │
│     │                                                                    │
│     ├──► Check: Can see target from here?                               │
│     │    │                                                               │
│     │    ├── YES: Capture stereo images + log RTK pose                  │
│     │    │                                                               │
│     │    └── NO: Viewpoint is occluded                                  │
│     │            Add to "need alternative" list                         │
│     │                                                                    │
│     └──► Next viewpoint                                                 │
│                                                                          │
│  3. AFTER PRIMARY PASS:                                                 │
│     │                                                                    │
│     ├── Review coverage gaps                                            │
│     ├── Generate additional viewpoints for missed areas                 │
│     └── Execute supplementary capture pass                              │
│                                                                          │
│  4. RTL when complete                                                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### PX4 Offboard Mode

```cpp
// Companion sends position setpoints to PX4
// PX4 handles low-level flight control

mavros_msgs::PositionTarget setpoint;
setpoint.coordinate_frame = FRAME_LOCAL_NED;
setpoint.type_mask = IGNORE_VX | IGNORE_VY | IGNORE_VZ | IGNORE_AFX | IGNORE_AFY | IGNORE_AFZ | IGNORE_YAW_RATE;

setpoint.position.x = target_x;  // meters, local frame
setpoint.position.y = target_y;
setpoint.position.z = target_z;
setpoint.yaw = target_yaw;       // radians

setpoint_pub.publish(setpoint);

// PX4 smoothly flies to this position
// Companion updates setpoint for obstacle avoidance
// Update rate: 10-50 Hz
```

---

## Complete Bill of Materials

### Flight System (Fixed)

| Part | Model | Weight | Cost | Notes |
|------|-------|--------|------|-------|
| Frame | Happymodel Crux35 | 26g | - | Your existing |
| Motors | T-Motor F1404 3800kv ×4 | 37g | - | Your existing |
| Props | HQProp T3.5x2.5x3 | 5g | - | Your existing |
| FC/ESC | MicoAir743-AIO-35A | 10g | - | Your existing |
| Battery | GNB 4S 850mAh HiLV | 75g | - | Your existing |
| Wiring | Base harness | 5g | - | |
| **Subtotal** | | **158g** | | |

### Payload System (New)

| Part | Model | Weight | Cost | Source |
|------|-------|--------|------|--------|
| RTK GPS | u-blox ZED-F9P | 10g | $150 | SparkFun |
| RTK Antenna | Taoglas AGGP25F | 6g | $30 | Mouser |
| Companion | Pi CM5 Lite 4GB | 15g | $45 | RPi |
| Carrier | Piunora Mini | 8g | $35 | Pimoroni |
| Camera L | Arducam OV2311 GS | 3g | $40 | Arducam |
| Camera R | Arducam OV2311 GS | 3g | $40 | Arducam |
| AI Accel | Coral M.2 TPU | 2g | $35 | Coral |
| Opt Flow | PMW3901 | 2g | $18 | Matek |
| ToF Range | VL53L1X | 1g | $12 | Pololu |
| FPV Cam | Caddx Ant Lite | 2g | $15 | GetFPV |
| FPV VTX | TBS Unify Pro Nano | 2g | $30 | GetFPV |
| SD Card | Samsung 128GB | 2g | $15 | Amazon |
| Carrier PCB | Custom | 5g | $25 | JLCPCB |
| Cables | FFC + JST | 5g | $15 | Various |
| Mount | 3D printed | 6g | $5 | Self |
| **Subtotal** | | **72g** | **$510** | |

### Total System

| | Weight | Cost |
|--|--------|------|
| Flight system | 158g | (existing) |
| Payload | 72g | $510 |
| **TOTAL** | **230g** ✓ | **$510** |

**20g under 250g limit**

---

## RTK Correction Options

### Option A: NTRIP (Easiest)

```
Internet ──► NTRIP Server ──► Cellular/WiFi ──► ZED-F9P
                │
                └── Free services: RTK2GO, Emlid Caster
                    Paid services: Point One Nav, Swift Nav
```

**Pros:** No extra hardware, works anywhere with coverage
**Cons:** Needs internet connection on drone or ground station

### Option B: Local Base Station (Best Accuracy)

```
┌─────────────────┐         ┌─────────────────┐
│   BASE STATION  │  Radio  │     ROVER       │
│   (on tripod)   │ ──────► │   (on drone)    │
│   ZED-F9P       │  915MHz │   ZED-F9P       │
│   + Antenna     │         │   + Antenna     │
└─────────────────┘         └─────────────────┘
```

**Additional cost:** ~$300 for base station kit
**Pros:** Best accuracy, no internet needed
**Cons:** Extra setup, need to transport base

### Option C: PPK Post-Processing (Recommended Start)

```
Flight:    Drone logs raw GNSS data
Post:      Download RINEX from nearby CORS station
Process:   RTKLIB computes precise positions
Result:    Same accuracy as RTK, no real-time link
```

**Pros:** No extra hardware, same accuracy
**Cons:** Positions computed after flight, not real-time

**Recommendation:** Start with PPK, add real-time RTK later if needed for obstacle avoidance.

---

## Software Stack

### ROS2 Packages Required

```yaml
# CM5 ROS2 Installation (Ubuntu 24.04 + Jazzy)

ros2_packages:
  - ros-jazzy-mavros              # PX4 communication
  - ros-jazzy-image-transport     # Camera streaming
  - ros-jazzy-cv-bridge           # OpenCV integration
  - ros-jazzy-stereo-image-proc   # Stereo processing
  - ros-jazzy-depth-image-proc    # Depth from stereo
  - ros-jazzy-octomap             # 3D occupancy mapping
  - ros-jazzy-navigation2         # Path planning

custom_packages:
  - capture_node                  # Stereo capture + pose logging
  - viewpoint_planner             # 3DGS optimal viewpoints
  - obstacle_avoidance            # Reactive avoidance
  - mission_controller            # High-level mission logic
```

### Node Graph

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ROS2 NODE GRAPH                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐          │
│  │ left_camera  │      │ right_camera │      │  rtk_gps     │          │
│  │   (driver)   │      │   (driver)   │      │  (driver)    │          │
│  └──────┬───────┘      └──────┬───────┘      └──────┬───────┘          │
│         │                     │                     │                    │
│         │ /left/image_raw     │ /right/image_raw   │ /gps/fix           │
│         │                     │                     │ /gps/rtk_status    │
│         ▼                     ▼                     │                    │
│  ┌────────────────────────────────────┐            │                    │
│  │         stereo_processor           │            │                    │
│  │  • Rectification                   │            │                    │
│  │  • Disparity computation           │            │                    │
│  │  • Depth map generation            │            │                    │
│  └──────────────┬─────────────────────┘            │                    │
│                 │                                   │                    │
│                 │ /stereo/depth                    │                    │
│                 │ /stereo/points2                  │                    │
│                 ▼                                   │                    │
│  ┌────────────────────────────────────┐            │                    │
│  │         obstacle_detector          │◄───────────┘                    │
│  │  • Point cloud to occupancy grid   │                                 │
│  │  • Obstacle tracking               │                                 │
│  │  • Collision prediction            │                                 │
│  └──────────────┬─────────────────────┘                                 │
│                 │                                                        │
│                 │ /obstacles                                            │
│                 │ /occupancy_grid                                       │
│                 ▼                                                        │
│  ┌────────────────────────────────────┐      ┌──────────────┐          │
│  │         mission_planner            │◄─────│  viewpoints  │          │
│  │  • Optimal 3DGS viewpoints         │      │  (config)    │          │
│  │  • Obstacle-aware path planning    │      └──────────────┘          │
│  │  • Adaptive replanning             │                                 │
│  └──────────────┬─────────────────────┘                                 │
│                 │                                                        │
│                 │ /setpoint_position                                    │
│                 ▼                                                        │
│  ┌────────────────────────────────────┐                                 │
│  │            mavros                  │                                 │
│  │  • Position setpoints to PX4       │                                 │
│  │  • State feedback from PX4         │                                 │
│  │  • Mode switching                  │                                 │
│  └──────────────┬─────────────────────┘                                 │
│                 │                                                        │
│                 │ MAVLink (UART)                                        │
│                 ▼                                                        │
│         ┌──────────────┐                                                │
│         │    PX4       │                                                │
│         │ (MicoAir743) │                                                │
│         └──────────────┘                                                │
│                                                                          │
│  ┌────────────────────────────────────┐                                 │
│  │         capture_logger             │                                 │
│  │  • Triggered at each viewpoint     │                                 │
│  │  • Saves stereo images             │                                 │
│  │  • Logs RTK pose + timestamp       │                                 │
│  │  • Writes to SD card               │                                 │
│  └────────────────────────────────────┘                                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Pose Logging Format (Deterministic Extrinsics)

### Log File Structure

```csv
# poses.csv - RTK-precision pose log
# Coordinate system: WGS84 (lat/lon) + EGM96 geoid height
# All orientations in radians (NED frame)
# Timestamp in microseconds since epoch

image_id,timestamp_us,lat,lon,alt_msl,roll,pitch,yaw,rtk_fix_type,hdop,satellites
0,1705123456789012,51.50743200,-0.12781500,45.234,0.012,-0.034,1.571,4,0.8,18
1,1705123458123456,51.50743850,-0.12780200,45.267,0.008,-0.029,1.623,4,0.7,19
2,1705123460456789,51.50744500,-0.12778900,45.301,0.015,-0.031,1.675,4,0.8,18
...
```

### RTK Fix Types

| Type | Meaning | Accuracy |
|------|---------|----------|
| 0 | No fix | N/A |
| 1 | Autonomous | ~3m |
| 2 | DGPS | ~1m |
| 4 | **RTK Fixed** | **1-2cm** |
| 5 | RTK Float | 10-50cm |

**Only capture images when rtk_fix_type == 4**

### Export to COLMAP

```python
# poses_to_colmap.py

def export_with_rtk_precision(poses_csv, output_dir):
    """
    Export RTK poses to COLMAP format
    Maintains cm-level precision in local frame
    """

    # Read poses
    poses = pd.read_csv(poses_csv)

    # Filter only RTK fixed solutions
    poses = poses[poses['rtk_fix_type'] == 4]

    # Use first pose as origin (for numerical stability)
    origin = {
        'lat': poses.iloc[0]['lat'],
        'lon': poses.iloc[0]['lon'],
        'alt': poses.iloc[0]['alt_msl']
    }

    # Convert to local ENU frame (preserves cm precision)
    poses['x'], poses['y'], poses['z'] = zip(*poses.apply(
        lambda p: geodetic_to_enu(p['lat'], p['lon'], p['alt_msl'], origin),
        axis=1
    ))

    # Write images.txt with precise poses
    with open(f"{output_dir}/images.txt", 'w') as f:
        for _, p in poses.iterrows():
            # Convert NED angles to camera rotation matrix
            R = ned_to_camera_rotation(p['roll'], p['pitch'], p['yaw'])
            q = rotation_to_quaternion(R)
            t = camera_translation(R, [p['x'], p['y'], p['z']])

            f.write(f"{p['image_id']} {q[0]} {q[1]} {q[2]} {q[3]} ")
            f.write(f"{t[0]:.6f} {t[1]:.6f} {t[2]:.6f} 1 ")
            f.write(f"IMG_{p['image_id']:04d}_L.jpg\n\n")

    # Save origin for georeferencing
    with open(f"{output_dir}/origin.json", 'w') as f:
        json.dump(origin, f)

    print(f"Exported {len(poses)} poses with RTK precision")
    print(f"Origin: {origin['lat']:.8f}, {origin['lon']:.8f}")
```

### Re-splat Alignment

When you re-fly and re-splat:

```python
# Both splats use same RTK coordinates
# Automatic alignment!

splat1_origin = load_json("splat1/origin.json")  # {lat: 51.50743, lon: -0.12781}
splat2_origin = load_json("splat2/origin.json")  # {lat: 51.50743, lon: -0.12781}

# Origins match within cm → splats align automatically
# No manual registration needed
```

---

## FPV Feed Setup

### Hardware

```
Caddx Ant Lite (AIO camera + VTX)
├── Weight: ~2-3g total
├── Resolution: 1200TVL
├── Latency: ~20ms
├── Power: 5V from FC
└── Frequency: 5.8GHz

Connects to: Your existing goggles or ground station monitor
```

### Why Separate from Capture Cameras?

| | FPV Camera | Stereo Capture Cameras |
|--|------------|------------------------|
| Purpose | You see where drone is | 3DGS image capture |
| Resolution | 1200TVL (low) | 2MP global shutter |
| Latency | ~20ms (critical) | ~100ms (doesn't matter) |
| Quality | Just needs to be visible | Maximum sharpness |
| Always on | Yes | Only at capture points |

**They serve completely different purposes - don't try to share.**

---

## Flight Modes

| Situation | PX4 Mode | Who Controls |
|-----------|----------|--------------|
| Taking off | AUTO.TAKEOFF | PX4 |
| Flying mission | OFFBOARD | CM5 sends setpoints |
| Capturing | OFFBOARD (hover) | CM5 holds position |
| Obstacle detected | OFFBOARD | CM5 replans |
| Emergency | POSITION | You (via RC) |
| Coming home | AUTO.RTL | PX4 |

### RC Override

Always have your RC ready with:
- **Position mode switch** - Stops CM5 control, you fly manually
- **Kill switch** - Emergency motor stop
- **RTL switch** - Automated return home

---

## Summary

| Requirement | Solution | Status |
|-------------|----------|--------|
| Stereo for better splats | 2× OV2311 global shutter | ✓ |
| Live feed | Caddx Ant Lite FPV | ✓ |
| Obstacle avoidance | Stereo depth + CM5 + ROS2 | ✓ |
| Adaptive planning | Custom ROS2 node | ✓ |
| Deterministic extrinsics | RTK GPS (ZED-F9P) | ✓ |
| Consistent scale | RTK = always 1:1 | ✓ |
| Re-splat alignment | Same RTK origin | ✓ |
| Sub-250g | 230g total | ✓ |

**Total cost: ~$510 for payload**
**Total weight: 230g (20g margin)**
