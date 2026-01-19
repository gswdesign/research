# XGRIDS Hardware Reverse Engineering Analysis

Detailed analysis of XGRIDS scanner architecture for DIY replication.

## PortalCam Deep Dive

### Camera System Architecture

The PortalCam uses a **4-camera array** with specific roles:

```
                    ┌─────────────────┐
                    │   TOP VIEW      │
                    └─────────────────┘

        ┌───────┐               ┌───────┐
        │FISHEYE│               │FISHEYE│
        │ LEFT  │               │ RIGHT │
        │200°x  │               │200°x  │
        │200°   │               │200°   │
        └───┬───┘               └───┬───┘
            │                       │
            │   ┌───────────────┐   │
            │   │    LiDAR      │   │
            │   │  180° x 180°  │   │
            │   └───────────────┘   │
            │                       │
        ┌───┴───┐               ┌───┴───┐
        │ FRONT │               │ FRONT │
        │ LEFT  │               │ RIGHT │
        │100°x  │               │100°x  │
        │ 85°   │               │ 85°   │
        └───────┘               └───────┘
```

### DIY Equivalent Camera Setup

**Option A: Dual Fisheye + Dual Standard**
```
2x Insta360 One RS 1-inch sensor modules  (~$400 total)
2x Arducam 16MP IMX519 with 100° lens     (~$80 total)
```

**Option B: Single 360° + Stereo Pair**
```
1x Ricoh Theta Z1 (API accessible)        (~$1,000)
1x Intel RealSense D455 (stereo depth)    (~$400)
```

**Option C: Budget Multi-Camera**
```
4x Raspberry Pi Camera Module 3 Wide      (~$140 total)
1x Custom sync board (Pi Pico)            (~$10)
```

### Camera Specifications to Match

| Parameter | PortalCam Spec | DIY Target |
|-----------|---------------|------------|
| Image Resolution | 4000 x 3000 | 4056 x 3040 (IMX519) |
| Sensor Size | 1/2" | 1/2.3" (close) |
| Shutter | Rolling | Rolling (acceptable) |
| Combined FOV | 360° + detail | Similar with fisheye |

### LiDAR Analysis

**PortalCam LiDAR Specs:**
- 856,000 points/second
- 60m range
- 180° x 180° FOV
- Solid-state (no rotating parts visible)

**Likely Internal Component:**
Based on specs, this appears similar to:
- Livox Mid-40/Mid-70 architecture
- Or custom Hesai solid-state module

**DIY Alternatives:**

| Module | Points/s | Range | FOV | Price |
|--------|----------|-------|-----|-------|
| Livox Mid-360 | 200k | 40m | 360°x59° | $1,000 |
| Livox Avia | 240k | 450m | 70.4°x77.2° | $1,500 |
| Used Livox Mid-40 | 100k | 260m | 38.4°x38.4° | $400-600 |

### IMU + Processing

**PortalCam:**
- Integrated 6DOF IMU
- Onboard GPU for real-time processing
- Custom SLAM firmware

**DIY Equivalent:**
```
BNO085 9DOF IMU               $30
  - Accelerometer
  - Gyroscope
  - Magnetometer
  - Sensor fusion built-in

Jetson Orin Nano              $500
  - 1024 CUDA cores
  - Real-time SLAM capable
  - ROS2 compatible
```

---

## Lixel L2 Pro Deep Dive

### Multi-Channel LiDAR System

The L2 Pro uses rotating multi-channel LiDAR (likely Hesai XT series):

```
         ┌─────────────────────────┐
         │    ROTATING HEAD       │
         │  ┌─────────────────┐   │
         │  │ 16/32 Channel   │   │
         │  │ Laser Array     │   │
         │  │                 │   │
         │  │  905nm Class 1  │   │
         │  └─────────────────┘   │
         │        ↓↑              │
         │   360° Rotation       │
         └─────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌────────┐   ┌────────┐   ┌────────┐
│PANORAMIC│  │PANORAMIC│  │  IMU   │
│CAM LEFT │  │CAM RIGHT│  │ 6DOF   │
│ 48MP    │  │ 48MP    │  │        │
│190°x190°│  │190°x190°│  │        │
└────────┘   └────────┘   └────────┘
```

### LiDAR Module Identification

**Spec Match Analysis:**
- 320k-640k pts/s → Hesai XT16/XT32
- 120-300m range → Hesai XT series
- 905nm wavelength → Standard automotive class

**Hesai XT32 Specs (likely module):**
- 32 channels
- 640,000 pts/s
- 120m @ 10% reflectivity
- 0.5cm accuracy
- ~$3,000-5,000

**Budget Alternative:**
- Used Velodyne VLP-16: ~$1,000-2,000
- Hesai Pandar40P (eBay): ~$200-300

### Panoramic Camera System

**L2 Pro Cameras:**
- 2x 48MP sensors
- 190° x 190° FOV each
- Combined 360° coverage

**DIY Options:**

| Option | Resolution | FOV | Price |
|--------|-----------|-----|-------|
| 2x Insta360 One RS | 48MP | 200° | $500 |
| 2x Kodak PIXPRO SP360 | 12MP | 214° | $400 |
| Custom fisheye rigs | varies | 180°+ | $200+ |

### SLAM Algorithm Architecture

Based on XGRIDS marketing ("Multi-SLAM"), the system likely uses:

```
┌─────────────────────────────────────────────────────┐
│                  MULTI-SLAM FUSION                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐                                   │
│  │ Visual      │──┐                                │
│  │ Odometry    │  │                                │
│  │ (ORB/FAST)  │  │                                │
│  └─────────────┘  │                                │
│                   │   ┌─────────────────────┐      │
│  ┌─────────────┐  ├──▶│  Factor Graph      │      │
│  │ LiDAR       │  │   │  Optimization      │      │
│  │ Odometry    │──┤   │  (GTSAM/Ceres)     │      │
│  │ (LOAM/FAST) │  │   └─────────┬───────────┘      │
│  └─────────────┘  │             │                  │
│                   │             ▼                  │
│  ┌─────────────┐  │   ┌─────────────────────┐      │
│  │ IMU         │──┤   │  Loop Closure       │      │
│  │ Integration │  │   │  Detection          │      │
│  │ (Preint.)   │──┘   └─────────┬───────────┘      │
│  └─────────────┘                │                  │
│                                 ▼                  │
│                   ┌─────────────────────────┐      │
│                   │  Globally Consistent    │      │
│                   │  Pose Graph + Map       │      │
│                   └─────────────────────────┘      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Open-Source Equivalents:**
- **LIO-SAM**: LiDAR-Inertial odometry via smoothing
- **FAST-LIO2**: Fast LiDAR-Inertial odometry
- **LVI-SAM**: LiDAR-Visual-Inertial SLAM
- **RTAB-Map**: Visual SLAM with loop closure

---

## DIY Replication Strategy

### Tier 1: Functional Equivalent ($500-800)

**Goal:** Basic 3D capture for static scenes

```
Components:
- Intel RealSense D455          $400
- Raspberry Pi 5 8GB            $80
- Pi Camera Module 3 (2nd view) $35
- BNO085 IMU                    $30
- 3D printed case               $30
- Battery + power               $50
- Misc                          $75
                               ─────
                        Total: ~$700

Software:
- RTAB-Map for SLAM
- Export to COLMAP format
- PostShot for 3DGS training
```

### Tier 2: Enhanced Scanner ($2,000-3,000)

**Goal:** LiDAR-enhanced capture with real-time preview

```
Components:
- Jetson Orin Nano              $500
- Intel RealSense D455          $400
- Livox Mid-40 (used)           $500
- 2x Arducam 16MP Wide          $80
- BNO085 IMU                    $30
- Custom aluminum frame         $200
- LiPo battery system           $150
- Power management              $100
- Misc                          $200
                               ─────
                        Total: ~$2,160

Software:
- ROS2 Humble
- FAST-LIO2 or LVI-SAM
- Custom COLMAP pipeline
- PostShot/Nerfstudio
```

### Tier 3: Near-Commercial ($8,000-12,000)

**Goal:** Quality approaching L2 Pro

```
Components:
- Jetson AGX Orin               $2,000
- Hesai XT16 or XT32            $3,000-5,000
- 2x Industrial 48MP camera     $1,000
- 2x 200° fisheye lenses        $400
- High-precision IMU (ADIS)     $500
- Custom machined enclosure     $500
- Professional battery system   $300
- Industrial connectors/cables  $300
                               ─────
                        Total: ~$8,000-10,000

Software:
- Custom multi-modal SLAM
- Real-time point cloud streaming
- Direct 3DGS generation pipeline
```

---

## Key Insights for Replication

### What Makes XGRIDS Work

1. **Tight Sensor Sync**: All sensors triggered simultaneously
   - DIY: Use hardware trigger lines or precision time protocol (PTP)

2. **High-Quality Cameras**: 48MP with good low-light
   - DIY: IMX586/IMX766 sensors in industrial cameras

3. **Real-Time Processing**: Onboard compute for immediate results
   - DIY: Jetson Orin series provides equivalent capability

4. **Calibration**: Factory-calibrated sensor positions
   - DIY: Use Kalibr or custom calibration targets

5. **Software Integration**: Unified data pipeline
   - DIY: ROS2 provides framework for sensor fusion

### What You Can't Easily Replicate

1. **Form Factor**: XGRIDS has custom molded housings
   - Workaround: 3D printing, but less durable

2. **Thermal Management**: Integrated cooling in sealed unit
   - Workaround: Active cooling, accept larger size

3. **Battery Efficiency**: Optimized power management
   - Workaround: Larger batteries, shorter runtime

4. **Locked Software**: XGRIDS LCC is proprietary
   - Workaround: Open-source alternatives (work, but more setup)

---

## Recommended DIY Starting Point

For your **COLMAP → Houdini → PostShot** workflow, I recommend:

### Hardware
```
1x Intel RealSense D455         $400  (depth + RGB + IMU)
1x Jetson Orin Nano             $500  (real-time processing)
1x Wide-angle camera (IMX519)   $40   (additional view angle)
1x 3D printed rig               $30   (holds everything)
1x USB-C PD battery             $50   (portable power)
                               ─────
                        Total: ~$1,020
```

### Why This Configuration

1. **D455** provides:
   - Stereo depth for initial point cloud
   - RGB for color/texture
   - IMU for motion tracking
   - USB 3.1 single-cable connection

2. **Jetson** provides:
   - Real-time SLAM (not possible on Pi)
   - GPU for preview rendering
   - ROS2 ecosystem support

3. **Additional camera** provides:
   - Different perspective for better COLMAP results
   - Can capture during SLAM for multi-view

### Data Flow
```
Capture Session
      │
      ▼
┌─────────────────┐
│ Jetson + D455   │
│ Running ROS2    │
│ + RTAB-Map      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Point Cloud     │
│ + Camera Poses  │
│ + RGB Images    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ COLMAP Import   │──▶ Sparse reconstruction
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PostShot        │──▶ 3DGS training
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GSOPs Houdini   │──▶ Edit & render
└─────────────────┘
```

---

## Sources

- [XGRIDS PortalCam Store](https://store.xgrids.com/products/portalcam)
- [Lixel L2 Pro - Decagon](https://decagonltd.com/en/product/lixel-l2-pro/)
- [Geo Week News - XGRIDS L2](https://www.geoweeknews.com/news/xgrids-l2-scanner-reality-capture-mobile-mapping-real-time-point-clouds-gaussian-splats)
- [VP-Land - PortalCam](https://www.vp-land.com/p/xgrids-portalcam-delivers-pro-spatial-capture-for-5k)
- [Radiance Fields - PortalCam](https://radiancefields.com/xgrids-announces-spatial-camera-portalcam)
