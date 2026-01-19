# DIY 3D Gaussian Splat Generator - Hardware Research

A comprehensive reverse engineering analysis of commercial 3DGS capture hardware and DIY build guide for COLMAP/Houdini/PostShot workflow integration.

## Table of Contents
1. [Commercial Hardware Analysis](#commercial-hardware-analysis)
2. [DIY Build Options](#diy-build-options)
3. [Component Specifications](#component-specifications)
4. [Software Pipeline](#software-pipeline)
5. [Build Guides](#build-guides)

---

## Commercial Hardware Analysis

### XGRIDS Product Line

#### PortalCam (~$5,000)
**The first dedicated handheld 3DGS capture device**

| Component | Specification |
|-----------|--------------|
| **Cameras** | 4-camera array (2x Fisheye + 2x Front) |
| **Image Resolution** | 4000 x 3000 px per camera |
| **Sensor** | 1/2" CMOS, Rolling Shutter |
| **Fisheye FOV** | 200° x 200° each |
| **Front Camera FOV** | 100° x 85° each |
| **LiDAR Rate** | 856,000 pts/s |
| **LiDAR Range** | 60m |
| **LiDAR FOV** | 180° x 180° |
| **Weight** | <900g |
| **Battery** | 23.04 Wh removable Li-ion |
| **Runtime** | 60 min continuous |
| **Processing** | Onboard AI (IMU + GPU) |

**Reverse Engineering Notes:**
- Uses dual fisheye for 360° coverage + dual front for detail
- Real-time SLAM with sensor fusion
- Locked to XGRIDS LCC software (additional €2,000/yr or €5,000 perpetual)

#### Lixel L2 Pro (~$28,000-32,000)
**Professional handheld LiDAR + 3DGS scanner**

| Component | Specification |
|-----------|--------------|
| **LiDAR Laser** | Class 1, 905nm |
| **LiDAR Channels** | 16 or 32 (XT16/XT32/XT32M2X) |
| **Scan Rate** | 320,000-640,000 pts/s |
| **Range** | 120m (XT16/XT32) / 300m (XT32M2X) |
| **LiDAR FOV** | 280° H x 360° V |
| **LiDAR Accuracy** | 0.5cm |
| **Cameras** | Dual 48MP panoramic (190° x 190° each) |
| **IMU** | 6DOF high-precision |
| **Storage** | 1TB SSD |
| **Connectivity** | USB 3.1 Gen2, WiFi, Bluetooth |
| **Weight** | 1.7kg (without battery) |
| **Size** | 180 x 130 x 400mm |
| **IP Rating** | IP54 |
| **Operating Temp** | -20°C to +50°C |

**Accuracy Specs:**
- Real-time: ±3cm absolute (H/V), ±2cm relative
- Processed: 0.5cm point cloud thickness, ±1cm relative

**Key Technologies:**
- Multi-SLAM algorithm with camera/LiDAR/IMU fusion
- Real-time Gaussian Splatting conversion
- True-color point cloud generation

---

## DIY Build Options

### Option 1: Budget Handheld Scanner ($300-600)

**Core Components:**
- Raspberry Pi 5 (8GB) - ~$80
- Intel RealSense D435i or D455 - ~$300-400
- IMU (built into D435i/D455)
- 3D printed enclosure
- 7" touchscreen display - ~$50
- Battery pack (USB-C PD) - ~$30
- Active cooling fan - ~$10

**Software Stack:**
- RTAB-Map (SLAM)
- Open3D (point cloud processing)
- Export to COLMAP format

**Limitations:**
- Lower resolution RGB than commercial units
- Limited range (~10m practical)
- Slower processing (not real-time 3DGS)

### Option 2: Enhanced Handheld (~$1,500-3,000)

**Core Components:**
- NVIDIA Jetson Orin Nano - ~$500
- Intel RealSense D455 - ~$400
- Livox Mid-360 LiDAR - ~$1,000
- External IMU (BNO085) - ~$30
- Wide-angle camera module - ~$50-100
- Custom enclosure
- LiPo battery system

**Software Stack:**
- ROS2 with SLAM Toolbox
- LiDAR-Visual-Inertial fusion (LVI-SAM)
- COLMAP export pipeline

### Option 3: Multi-Camera Array (~$10,000-50,000+)

**For studio/controlled capture environments:**

| Configuration | Cameras | Use Case |
|--------------|---------|----------|
| Head Scan | 110 | Facial detail, portraits |
| Full Body | 176-205 | Character capture |
| Modular Wall | 30-400+ | Scalable environments |

**Camera Options:**
- Canon R100 / Sony a6400 - ~$600-900 each
- Synchronized via USB (Xangle system)
- Raspberry Pi cluster for triggering

**Structure:**
- 12ft diameter x 10ft height typical
- Extruded aluminum or pipe frame
- ~$1,000/camera all-in budget

---

## Component Specifications

### LiDAR Modules (Affordable Options)

| Model | Type | Range | Rate | Price |
|-------|------|-------|------|-------|
| **Livox Mid-360** | Non-repetitive | 40m | 200k pts/s | ~$1,000 |
| **Livox HAP** | Automotive | 150m | - | $1,599 |
| **Hesai JT16** | Mechanical ToF | 60m | - | ~$585 |
| **Slamtec RPLIDAR A1** | 2D spinning | 12m | 8k pts/s | ~$100 |
| **Velodyne Puck (VLP-16)** | 16-ch spinning | 100m | 300k pts/s | ~$4,000 (new) |
| **Used Hesai Pandar40P** | 40-ch spinning | 200m | - | ~$200-300 (eBay) |

### Depth Cameras

| Model | Resolution | Range | IMU | Interface | Price |
|-------|-----------|-------|-----|-----------|-------|
| **Intel RealSense D455** | 1280x720 depth | 6m | Yes | USB 3.1 | ~$400 |
| **Intel RealSense D435i** | 1280x720 depth | 10m | Yes | USB 3.0 | ~$350 |
| **Intel RealSense D415** | 1280x720 depth | 10m | No | USB 3.0 | ~$250 |
| **Azure Kinect** | 1024x1024 depth | 5.5m | Yes | USB 3.0 | ~$400 |

### Processing Platforms

| Platform | CPU | GPU | RAM | Price | Use Case |
|----------|-----|-----|-----|-------|----------|
| **Raspberry Pi 5** | Cortex-A76 | - | 8GB | $80 | Budget, limited |
| **Jetson Orin Nano** | Cortex-A78 | Ampere GPU | 8GB | $500 | Real-time SLAM |
| **Jetson AGX Orin** | Cortex-A78 | Ampere GPU | 32GB | $2,000 | Full 3DGS |

### Cameras for Multi-Camera Rigs

| Model | Resolution | Trigger | Price |
|-------|-----------|---------|-------|
| **Canon R100** | 24.2MP | USB | ~$480 |
| **Sony a6400** | 24.2MP | USB | ~$900 |
| **Canon SL1/100D** | 18MP (5K RAW) | USB | ~$200 used |

---

## Software Pipeline

### Capture → 3DGS Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CAPTURE   │────▶│   COLMAP    │────▶│  TRAINING   │────▶│   OUTPUT    │
│             │     │             │     │             │     │             │
│ - Images    │     │ - SfM       │     │ - PostShot  │     │ - .ply      │
│ - Depth     │     │ - Poses     │     │ - Nerfstudio│     │ - .splat    │
│ - LiDAR     │     │ - Sparse PC │     │ - Original  │     │ - Unity     │
└─────────────┘     └─────────────┘     │   3DGS impl │     │ - Unreal    │
                                        └─────────────┘     │ - Houdini   │
                                                            └─────────────┘
```

### COLMAP Requirements
- 20-200 images (PNG/JPG) or video (MP4)
- Minimal motion blur
- Avoid shallow depth of field
- Consistent lighting preferred

### Houdini Integration (GSOPs)
- **GSOPs 2.0**: Gaussian Splat Operators for Houdini
- Import/export 3DGS content
- Real-time viewport renderer
- COLMAP txt export
- PNG with alpha mask support for PostShot
- Compatible with Houdini 20.5+

### PostShot Workflow
- Accepts COLMAP sparse point clouds
- Batch processing available (PostShot Batch Trainer)
- Export to Unity, Unreal, Blender

### Key Software Tools
| Tool | Purpose | Link |
|------|---------|------|
| **COLMAP** | Structure from Motion | [GitHub](https://github.com/colmap/colmap) |
| **PostShot** | 3DGS training (commercial) | postshot.io |
| **Nerfstudio** | 3DGS training (open source) | [GitHub](https://github.com/nerfstudio-project/nerfstudio) |
| **GSOPs** | Houdini operators | [GitHub](https://github.com/cgnomads/GSOPs) |
| **RTAB-Map** | Real-time SLAM | [GitHub](https://github.com/introlab/rtabmap) |
| **Original 3DGS** | Reference implementation | [GitHub](https://github.com/graphdeco-inria/gaussian-splatting) |

---

## Build Guides

### Build 1: Minimal Viable Scanner

**Bill of Materials:**
```
1x Raspberry Pi 5 (8GB)              $80
1x Intel RealSense D435i             $350
1x Official Pi 5 Active Cooler       $5
1x 7" Touchscreen                    $50
1x USB-C PD Battery (65W+)           $40
1x 3D Printed Enclosure              $20 (filament)
   Misc (cables, mounting)           $30
                                    ─────
                            TOTAL:  ~$575
```

**Software Setup:**
1. Install Ubuntu 22.04 on Pi 5
2. Build librealsense2 from source
3. Install RTAB-Map
4. Configure for handheld scanning mode
5. Export point clouds → COLMAP → PostShot

### Build 2: Enhanced LiDAR Scanner

**Bill of Materials:**
```
1x NVIDIA Jetson Orin Nano          $500
1x Intel RealSense D455             $400
1x Livox Mid-360                    $1,000
1x BNO085 IMU                       $30
1x Wide-angle USB camera            $80
1x LiPo Battery (6S, 5000mAh)       $80
1x Power management board           $50
1x Custom 3D printed enclosure      $50
   Misc hardware                    $100
                                   ─────
                           TOTAL:  ~$2,290
```

**Software Stack:**
1. JetPack 6.0 with ROS2 Humble
2. Livox ROS2 driver
3. LVI-SAM for LiDAR-Visual-Inertial SLAM
4. Custom pipeline to export COLMAP format
5. PostShot/Nerfstudio for 3DGS training

### Build 3: Portable Capture Rig (Multi-Camera)

**For 20-camera starter system:**
```
20x Canon R100 cameras              $9,600
20x 18mm lenses (kit)               (included)
5x Raspberry Pi 5                   $400
2x Network switches                 $100
1x Aluminum frame structure         $500
1x Lighting system                  $300
1x Xangle Camera Server license     $200
   Cables and mounting              $300
                                   ─────
                           TOTAL:  ~$11,400
```

---

## Reverse Engineering Insights

### XGRIDS Design Patterns

1. **Sensor Fusion**: All XGRIDS devices use tight integration of:
   - Multiple cameras (wide + detail)
   - LiDAR (where applicable)
   - High-precision 6DOF IMU
   - Real-time sensor fusion algorithms

2. **Dual-FOV Camera Strategy**:
   - Wide fisheye cameras for environment context
   - Narrow front cameras for texture detail
   - This could be replicated with dual-camera setups

3. **Real-time Processing**:
   - Onboard GPU/NPU for immediate SLAM
   - Edge processing reduces data transfer needs
   - Jetson Orin replicates this capability

4. **Multi-SLAM Algorithm**:
   - Combines visual odometry, LiDAR odometry, and IMU
   - Open-source equivalents: LVI-SAM, FAST-LIO2

### DIY Equivalent Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DIY SLAM SCANNER                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐           │
│  │ Fisheye   │  │   Depth   │  │   LiDAR   │           │
│  │ Camera    │  │  Camera   │  │  Module   │           │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘           │
│        │              │              │                   │
│        ▼              ▼              ▼                   │
│  ┌─────────────────────────────────────────────┐        │
│  │            Sensor Fusion (EKF/Factor Graph) │        │
│  │                      IMU                     │        │
│  └─────────────────────┬───────────────────────┘        │
│                        │                                 │
│                        ▼                                 │
│  ┌─────────────────────────────────────────────┐        │
│  │            SLAM Engine (LVI-SAM)            │        │
│  │         - Visual Odometry                   │        │
│  │         - LiDAR Odometry                    │        │
│  │         - Loop Closure                      │        │
│  └─────────────────────┬───────────────────────┘        │
│                        │                                 │
│                        ▼                                 │
│  ┌─────────────────────────────────────────────┐        │
│  │              Point Cloud Export             │        │
│  │         → COLMAP → PostShot → 3DGS          │        │
│  └─────────────────────────────────────────────┘        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Sources & References

### Commercial Products
- [XGRIDS Main Site](https://www.xgrids.com/)
- [XGRIDS PortalCam](https://store.xgrids.com/products/portalcam)
- [PortalCam Review - Design4Real](https://design4real.de/en/portalcam-review-xgrids-scanner-gaussian-splatting/)
- [Lixel L2 Pro - Heliguy](https://www.heliguy.com/products/lixel-l2-pro/)
- [XGRIDS L2 Scanner - Geo Week News](https://www.geoweeknews.com/news/xgrids-l2-scanner-reality-capture-mobile-mapping-real-time-point-clouds-gaussian-splats)

### DIY Builds
- [Handheld 3D Scanner with Pi 4 - Hackaday](https://hackaday.com/2020/03/31/handheld-3d-scanning-using-raspberry-pi-4-and-intel-realsense-camera/)
- [SLAM on Raspberry Pi - GitHub](https://github.com/AdroitAnandAI/SLAM-on-Raspberry-Pi)
- [Building 100-Camera Rig - Xangle](https://xanglecs.com/blog/where-to-start-100-cameras-photogrammetry-station-starting-from-scratch)

### Software & Tools
- [GSOPs for Houdini - GitHub](https://github.com/cgnomads/GSOPs)
- [Original 3DGS Implementation - GitHub](https://github.com/graphdeco-inria/gaussian-splatting)
- [Awesome 3D Gaussian Splatting - GitHub](https://github.com/MrNeRF/awesome-3D-gaussian-splatting)
- [Intel RealSense SLAM Wiki](https://github.com/IntelRealSense/realsense-ros/wiki/SLAM-with-D435i)

### Hardware
- [Livox LiDAR](https://www.livoxtech.com/)
- [Intel RealSense D455](https://www.realsenseai.com/products/real-sense-depth-camera-d455f/)
- [Xangle Studio Gaussian Splatting](https://xanglestudio.com/gaussian-splatting)

---

*Last Updated: January 2026*
