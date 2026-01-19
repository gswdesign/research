# Sub-250g Scanning Drone Build Analysis

## Your Target Setup
- Pi CM5 module
- Rotating LiDAR (360°)
- RGB camera
- PX4 with MicoAir 743 AIO 35A

## Weight Budget Reality Check

### Total Budget: 250g

**Base Drone (unavoidable):**
| Component | Weight | Notes |
|-----------|--------|-------|
| Frame (3" micro) | 40-60g | Carbon fiber |
| Motors x4 (1404-1507) | 28-40g | ~7-10g each |
| Props x4 | 4-6g | ~1-1.5g each |
| MicoAir 743 AIO 35A | 10-12g | With ESCs integrated |
| Battery (3S 450-650mAh) | 45-75g | Flight time tradeoff |
| Wiring/misc | 5-10g | |
| **Subtotal** | **132-203g** | |

**Remaining for payload: 47-118g**

---

## The Problem

Your desired payload:
| Component | Weight | Notes |
|-----------|--------|-------|
| Pi CM5 module | ~15g | Module only |
| CM5 carrier board | 10-40g | Minimal custom vs off-shelf |
| LD19 rotating LiDAR | **47g** | This is the killer |
| Pi Camera v3 | 3g | |
| GPS module | 5-10g | For georeferencing |
| Mounting/cables | 10-15g | |
| **Subtotal** | **90-130g** | |

**Total: 222-333g** - Borderline to impossible

---

## Option A: True Sub-250g (Compromised Scanning)

**Drop the rotating LiDAR, use single-point + camera only**

| Component | Weight |
|-----------|--------|
| Frame (2.5" micro) | 35g |
| Motors x4 (1303) | 24g |
| Props | 4g |
| MicoAir 743 AIO | 10g |
| Battery (3S 450mAh) | 45g |
| **Pi Zero 2W** | 12g |
| Pi Camera v3 | 3g |
| **TFmini-S** (single point) | 5g |
| GPS (u-blox M10) | 5g |
| Wiring/mount | 10g |
| **Total** | **153g** ✓ |

**Capability:**
- RGB images for photogrammetry → COLMAP → 3DGS
- Single-point altitude LiDAR (not 3D scanning)
- GPS for georeferencing
- Lightweight enough for sub-250g

**Limitation:** No 360° LiDAR point cloud - relies on photogrammetry only

---

## Option B: Lightweight Scanning (~280-320g)

**Keep rotating LiDAR, exceed 250g slightly**

| Component | Weight |
|-----------|--------|
| Frame (3" micro) | 45g |
| Motors x4 (1404) | 32g |
| Props | 5g |
| MicoAir 743 AIO | 10g |
| Battery (4S 550mAh) | 65g |
| **Pi Zero 2W** | 12g |
| Pi Camera v3 wide | 3g |
| **LD06/LD19** | 47g |
| GPS (u-blox M10) | 5g |
| Custom mount | 15g |
| Wiring | 8g |
| **Total** | **247g** ✓ (barely!) |

**This might actually work!** But it's razor thin margins.

**Trade-offs:**
- Pi Zero 2W instead of CM5 (much less compute)
- Small battery = ~5-8 min flight time
- Need to process data offline (Zero 2W can't run SLAM in real-time)

---

## Option C: Full Capability (~400-500g)

**What you actually need for real-time SLAM scanning**

| Component | Weight |
|-----------|--------|
| Frame (5" freestyle) | 100g |
| Motors x4 (2306) | 120g |
| Props | 12g |
| MicoAir 743 AIO | 10g |
| Battery (4S 1300mAh) | 180g |
| **Pi CM5 + minimal carrier** | 40g |
| Global shutter camera | 30g |
| **LD19** | 47g |
| GPS + IMU | 15g |
| Mount/wiring | 20g |
| **Total** | **574g** |

This is what you need for your full vision but requires:
- Drone registration in most countries
- Remote ID compliance
- More substantial airframe

---

## Option D: Hybrid Approach (Recommended)

**Two-drone strategy:**

### Drone 1: Sub-250g Scout
- Photogrammetry only (no LiDAR)
- Quick flights, no registration hassle
- RGB images → COLMAP → initial 3DGS

### Drone 2: 400-600g Mapping Rig
- Full LiDAR + camera + RTK
- Registered, compliant
- Precision scanning when needed

---

## Component Details for Sub-250g Attempt

### Compute: Pi Zero 2W vs CM5

| Spec | Pi Zero 2W | Pi CM5 |
|------|-----------|--------|
| Weight | **12g** | ~15g + carrier |
| CPU | Quad A53 1GHz | Quad A76 2.4GHz |
| RAM | 512MB | 2-8GB |
| Real-time SLAM | No | Yes |
| Record to SD | Yes | Yes |
| Power | 0.5-1W | 3-8W |
| **Total system** | **~15g** | **~40-60g** |

**For sub-250g: Use Pi Zero 2W, process offline**

### LiDAR Options

| Model | Weight | Type | Range | Price |
|-------|--------|------|-------|-------|
| TFmini-S | **5g** | Single point | 12m | $30 |
| TFmini Plus | **11g** | Single point | 12m | $45 |
| LD06 | ~45g | 360° rotating | 12m | $80 |
| LD19 | **47g** | 360° rotating | 12m | $99 |
| Livox Mid-360 | **265g** | 360° solid-state | 40m | $1000 |

**For sub-250g with 360°: LD06/LD19 is your only option**

### Cameras

| Model | Weight | Shutter | Resolution |
|-------|--------|---------|------------|
| Pi Camera v3 | **3g** | Rolling | 12MP |
| Pi Camera v3 Wide | **3g** | Rolling | 12MP |
| Pi Global Shutter | **3g** | **Global** | 1.6MP |
| Arducam 16MP | 5g | Rolling | 16MP |

**For motion: Pi Global Shutter camera (lower res but no blur)**

### GPS

| Model | Weight | Accuracy |
|-------|--------|----------|
| u-blox M10 | **5g** | 2.5m CEP |
| u-blox M9N | 8g | 2m CEP |
| u-blox F9P (RTK) | 15g+ | 1cm |

---

## Minimal Viable Sub-250g Build

```
┌─────────────────────────────────────────────────┐
│          SUB-250g SCANNING DRONE                │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │           LD19 LiDAR (47g)              │   │
│  │         [Mounted on top]                │   │
│  └─────────────────────────────────────────┘   │
│                      │                          │
│  ┌─────────┐    ┌────┴────┐    ┌─────────┐    │
│  │ Motor   │    │  Frame  │    │ Motor   │    │
│  │ (8g)    │    │  (40g)  │    │ (8g)    │    │
│  └─────────┘    └────┬────┘    └─────────┘    │
│                      │                          │
│         ┌────────────┴────────────┐            │
│         │                         │            │
│  ┌──────┴──────┐          ┌──────┴──────┐     │
│  │ Pi Zero 2W  │          │   Camera    │     │
│  │ (12g)       │          │   (3g)      │     │
│  └─────────────┘          └─────────────┘     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │    MicoAir 743 AIO 35A (10g)            │   │
│  │    + GPS module (5g)                    │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │         3S 450mAh LiPo (45g)            │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Motors: 1303/1404 class (~8g each)            │
│  Frame: 2.5-3" carbon micro                    │
│                                                 │
│  TOTAL: ~240-250g                              │
└─────────────────────────────────────────────────┘
```

---

## Data Flow (Offline Processing)

```
                    ON DRONE                         ON DESKTOP
┌─────────────────────────────────┐    ┌─────────────────────────────┐
│                                 │    │                             │
│  LD19 ────► Pi Zero 2W         │    │    Process with             │
│             │                   │    │    FAST-LIO / LIO-SAM       │
│  Camera ───►│ Record to SD     │───►│           │                 │
│             │ (rosbag2)        │    │           ▼                 │
│  IMU ──────►│                  │    │    Export to COLMAP         │
│  GPS ──────►│                  │    │           │                 │
│                                 │    │           ▼                 │
└─────────────────────────────────┘    │    PostShot / 3DGS         │
                                       │           │                 │
                                       │           ▼                 │
                                       │    Houdini / GSOPs         │
                                       └─────────────────────────────┘
```

**Pi Zero 2W role:** Data logger only (not real-time processing)
- Records LiDAR scans to SD
- Records camera frames
- Records IMU/GPS data
- Timestamps everything

**Desktop role:** All heavy processing
- SLAM reconstruction
- Point cloud generation
- 3DGS training

---

## Software Setup for Pi Zero 2W

```bash
# Install minimal ROS2 (no desktop)
# On Pi Zero 2W with Ubuntu Server 22.04

# LD19 driver
git clone https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2
cd ldlidar_stl_ros2
colcon build

# Recording script
ros2 bag record \
    /scan \
    /camera/image_raw \
    /imu/data \
    /gps/fix \
    -o flight_$(date +%Y%m%d_%H%M%S)
```

---

## Honest Assessment

| Goal | Feasible? | Notes |
|------|-----------|-------|
| Sub-250g with 360° LiDAR | **Barely** | ~247g with Zero 2W, tiny battery |
| Sub-250g with CM5 | **No** | CM5 + carrier too heavy |
| Sub-250g with real-time SLAM | **No** | Need more compute = more weight |
| ~300g with good capability | **Yes** | Sweet spot for DIY scanning |
| Full XGRIDS equivalent | **No** | Need 400-600g minimum |

---

## My Recommendation

1. **Build the 247g version first** with Pi Zero 2W + LD19
2. **Test if data quality is sufficient** for your 3DGS workflow
3. **If you need more**, build a second 400g+ rig with CM5

The sub-250g limit is regulatory convenience, not a physics requirement. If you're doing professional scanning work, the registration overhead of a 400g drone is worth the capability gain.

---

## Parts List: Sub-250g Attempt

| Part | Model | Weight | Price | Link |
|------|-------|--------|-------|------|
| Frame | iFlight Titan DC2 2.5" | 40g | $25 | iFlight |
| Motors | EMAX RS1306 | 32g (x4) | $40 | GetFPV |
| FC/ESC | MicoAir 743 AIO 35A | 10g | $80 | MicoAir |
| Props | Gemfan 2540 | 4g | $5 | GetFPV |
| Battery | GNB 450mAh 3S | 45g | $15 | RDQ |
| Compute | Pi Zero 2W | 12g | $15 | RPi |
| Camera | Pi Global Shutter | 3g | $50 | RPi |
| LiDAR | LD19 | 47g | $99 | Amazon |
| GPS | Beitian BN-180 | 5g | $15 | Amazon |
| SD Card | Samsung 128GB | 2g | $15 | Amazon |
| Mount | 3D printed | 10g | $5 | - |
| Wiring | - | 8g | $10 | - |
| **Total** | | **~233g** | **~$374** | |

**Buffer: 17g** for unforeseen additions

---

## Sources

- [Pi Zero 2W Specs](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
- [LD19 Datasheet](https://www.ldrobot.com/images/2023/05/23/LDROBOT_LD19_Datasheet_EN_v2.6_Q1JXIRVq.pdf)
- [MicoAir 743 AIO](https://micoair.com/flightcontroller_micoair743_aio_35a/)
- [TFmini-S Specs](https://en.benewake.com/TFminiS/index.html)
- [Ochin CM4 Carrier](https://www.hackster.io/news/flavio-ansovini-s-ochin-raspberry-pi-cm4-carrier-takes-aim-at-drones-robots-the-iot-and-more-638081254def)
