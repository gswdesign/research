# Final Hardware Specification: Crux35 Autonomous 3DGS Capture

## Summary of Requirements

| Requirement | Solution |
|-------------|----------|
| RTK positioning | **Required** - for deterministic extrinsics |
| Autonomous flight | **PX4 Offboard mode** + companion computer |
| Obstacle avoidance | **Stereo depth** + path replanning |
| Image quality vs DJI | **Achievable** with right camera |
| Intrinsics/extrinsics | **Pre-calibrated** + RTK logged |
| Sub-250g | **Yes** - 232g total |

---

## RTK: Do You Need a Ground Station?

### Three Options

| Method | Ground Hardware | Accuracy | Cost | Complexity |
|--------|-----------------|----------|------|------------|
| **NTRIP** | None (internet) | 1-3cm | $0-50/mo | Easy |
| **Own Base** | Base station | 1-2cm | +$300 | Medium |
| **PPK** | None (post-process) | 1-2cm | $0 | Easy |

### Recommended: Start with NTRIP

```
Your phone hotspot ──► Drone WiFi ──► CM5 ──► NTRIP client ──► RTK corrections
         │
    (or 4G module on drone)
```

**Free NTRIP services:**
- RTK2GO (community base stations)
- Your country's survey network (many are free)

**No ground station needed** if you have cell coverage. Only add a base station if:
- Flying in areas with no cell coverage
- Need guaranteed <1cm accuracy
- Flying frequently in same location

### How RTK Works

```
WITHOUT RTK:
  GPS satellite ──► Drone receiver ──► Position (±3-5m error)

WITH RTK (NTRIP):
  GPS satellite ──► Drone receiver ──► Raw position
                         │
  GPS satellite ──► NTRIP base (known location) ──► Corrections
                         │
                         ▼
                  Corrected position (±1-3cm error)
```

---

## Camera Setup: Splat vs CV

### Answer: Use Stereo Cameras for BOTH

```
┌─────────────────────────────────────────────────────────────┐
│                   DUAL-PURPOSE STEREO                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   LEFT CAMERA              RIGHT CAMERA                      │
│   (OV2311 GS)              (OV2311 GS)                       │
│        │                        │                            │
│        └──────────┬─────────────┘                            │
│                   │                                          │
│                   ▼                                          │
│        ┌─────────────────────┐                               │
│        │    STEREO PAIR      │                               │
│        └─────────────────────┘                               │
│                   │                                          │
│         ┌────────┴────────┐                                  │
│         │                 │                                  │
│         ▼                 ▼                                  │
│   ┌──────────┐     ┌──────────────┐                         │
│   │   3DGS   │     │   OBSTACLE   │                         │
│   │ CAPTURE  │     │  AVOIDANCE   │                         │
│   │          │     │              │                         │
│   │ • Images │     │ • Depth map  │                         │
│   │ • Poses  │     │ • Collision  │                         │
│   │          │     │   detection  │                         │
│   └──────────┘     └──────────────┘                         │
│                                                              │
│   SAME CAMERAS DO BOTH JOBS                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Why Not Separate Cameras?

| Separate Cameras | Single Stereo Pair |
|------------------|-------------------|
| +10g weight | Saves weight |
| More complexity | Simpler |
| Sync issues | Already synced |
| Different FOV | Same FOV |
| Extra calibration | One calibration |

**The stereo pair for 3DGS is the same stereo pair for obstacle avoidance.**

### But What About Resolution?

| Camera | Resolution | For 3DGS | For CV |
|--------|------------|----------|--------|
| OV2311 (2MP GS) | 1600×1200 | Good | Excellent |
| IMX296 (1.6MP GS) | 1456×1088 | OK | Excellent |
| IMX477 (12MP RS) | 4056×3040 | Better | Blur issues |

**Trade-off:** Global shutter (sharp) vs high resolution (detailed)

**For drone at speed:** Sharp 2MP > Blurry 12MP

### Optional: Separate FPV Camera

```
FPV camera (for you to see) ≠ Capture cameras (for 3DGS)

FPV: Caddx Ant Lite (2g, $15) - just for monitoring
Capture: Stereo OV2311 (6g, $80) - for data
```

---

## Image Quality vs DJI

### Honest Comparison

| Spec | DJI Mini 5 Pro | Your Build |
|------|----------------|------------|
| Sensor | 1" CMOS | 1/2.9" CMOS |
| Resolution | 50MP | 2MP |
| Pixel size | 2.4μm | 3.0μm |
| Shutter | **Rolling** | **Global** |
| Stabilization | 3-axis gimbal | None |
| Dynamic range | 12.8 stops | ~10 stops |
| Low light | Excellent | Moderate |

### Where You WIN

| Factor | DJI | Your Build |
|--------|-----|------------|
| Motion blur | Can happen | **None (global shutter)** |
| Rolling shutter skew | Yes | **None** |
| COLMAP success rate | Good | **Better** |
| Geometric accuracy | Good | **Better** |
| RTK positioning | No | **Yes (cm-level)** |
| Obstacle avoidance | Fixed | **Adaptive** |
| Customization | None | **Full** |

### Where DJI WINS

| Factor | DJI | Your Build |
|--------|-----|------------|
| Raw image quality | **Excellent** | Good |
| Low light | **Excellent** | Moderate |
| Dynamic range | **Better** | Good |
| Ease of use | **Simple** | Complex |
| Texture detail | **Higher res** | Lower res |

### For 3DGS Specifically

**Your build will produce BETTER splats because:**
1. Global shutter = no geometric distortion
2. RTK = perfect extrinsics
3. Stereo = depth supervision
4. More capture positions (smaller, more agile)

**DJI produces prettier individual photos, but your build produces better 3D.**

---

## Final Hardware Specification

### Drone Base (Your Existing)

| Part | Model | Weight |
|------|-------|--------|
| Frame | Happymodel Crux35 | 26g |
| Motors | T-Motor F1404 3800kv ×4 | 37g |
| Props | HQProp T3.5x2.5x3 | 5g |
| FC/ESC | MicoAir743-AIO-35A (PX4) | 10g |
| Battery | GNB 4S 850mAh HiLV | 75g |
| Wiring | | 5g |
| **Subtotal** | | **158g** |

### Payload (New)

| Part | Model | Weight | Cost | Purpose |
|------|-------|--------|------|---------|
| **RTK GPS** | u-blox ZED-F9P | 10g | $150 | Deterministic position |
| **RTK Antenna** | Taoglas AGGP25F | 6g | $30 | Signal reception |
| **Companion** | Pi CM5 Lite 4GB | 15g | $45 | Compute + autonomy |
| **Carrier** | Piunora Mini | 8g | $35 | CM5 interface |
| **Left Camera** | Arducam OV2311 GS | 3g | $40 | Stereo + capture |
| **Right Camera** | Arducam OV2311 GS | 3g | $40 | Stereo + capture |
| **AI Accelerator** | Hailo-8L M.2 | 3g | $70 | Real-time depth |
| **Optical Flow** | PMW3901 | 2g | $18 | Indoor + low alt |
| **ToF Range** | VL53L1X | 1g | $12 | Height hold |
| **FPV Camera** | Caddx Ant Lite | 2g | $15 | Monitoring |
| **Storage** | MicroSD 128GB | 2g | $15 | Data logging |
| **Carrier PCB** | Custom | 5g | $25 | Integration |
| **Cables/Mount** | | 9g | $20 | |
| **Subtotal** | | **74g** | **$515** | |

### Total System

| | Weight | Cost |
|--|--------|------|
| Drone base | 158g | (existing) |
| Payload | 74g | $515 |
| **TOTAL** | **232g** ✓ | **$515** |

**18g under 250g limit**

---

## Autonomous System Architecture

### Software Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    RASPBERRY PI CM5                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ROS2 Jazzy                                                     │
│  ├── mavros (PX4 communication)                                 │
│  ├── stereo_image_proc (depth from stereo)                      │
│  ├── rtk_driver (ZED-F9P + NTRIP client)                       │
│  ├── obstacle_detector (depth → occupancy grid)                │
│  ├── viewpoint_planner (optimal 3DGS positions)                │
│  ├── path_planner (obstacle-aware navigation)                  │
│  └── capture_node (image + pose logging)                       │
│                                                                  │
│  Hailo Runtime                                                  │
│  └── RAFT-Stereo model (real-time depth)                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                         MAVLink
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    MicoAir743 (PX4)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  • OFFBOARD mode (accepts setpoints from CM5)                   │
│  • EKF2 sensor fusion (RTK + IMU + baro)                       │
│  • Position/velocity control                                    │
│  • Failsafe handling                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Autonomous Mission Flow

```
1. STARTUP
   ├── Boot CM5
   ├── Connect to NTRIP (via phone hotspot or 4G)
   ├── Wait for RTK FIX (rtk_fix_type == 4)
   └── Arm when ready

2. TAKEOFF
   └── PX4 AUTO.TAKEOFF to mission altitude

3. FOR EACH CAPTURE POSITION:
   │
   ├── CM5 calculates path to next position
   │
   ├── WHILE navigating:
   │   │
   │   ├── Stereo cameras → Hailo → depth map (30fps)
   │   │
   │   ├── Depth → obstacle detection
   │   │
   │   ├── IF obstacle detected:
   │   │   ├── Replan path around obstacle
   │   │   └── OR modify capture position
   │   │
   │   └── Send position setpoint to PX4 (50Hz)
   │
   ├── ARRIVE at position
   │   ├── Hold for 1-2 seconds (stabilize)
   │   ├── Verify RTK FIX
   │   └── Verify no obstacle blocking view
   │
   ├── CAPTURE
   │   ├── Trigger stereo cameras
   │   ├── Log RTK pose (lat, lon, alt, roll, pitch, yaw)
   │   ├── Log timestamp
   │   └── Save to SD
   │
   └── NEXT position

4. RTL
   └── Return home and land

5. POST-FLIGHT
   ├── Download images
   ├── Download pose log
   └── Process: COLMAP → Depth Anything → 3DGS
```

---

## Intrinsics / Extrinsics Capture

### Intrinsics (Camera Calibration) - ONE TIME

```bash
# Before first flight, calibrate stereo pair
# Print checkerboard, capture 30+ image pairs

python calibrate_stereo.py \
    --left_images /calibration/left/ \
    --right_images /calibration/right/ \
    --board_size 9x6 \
    --square_size 0.025 \
    --output stereo_calibration.yaml
```

**Output (stored on CM5):**
```yaml
# stereo_calibration.yaml
left_camera:
  fx: 800.0
  fy: 800.0
  cx: 800.0
  cy: 600.0
  distortion: [-0.1, 0.05, 0.0, 0.0]

right_camera:
  fx: 800.0
  fy: 800.0
  cx: 800.0
  cy: 600.0
  distortion: [-0.1, 0.05, 0.0, 0.0]

stereo:
  baseline: 0.06  # 6cm between cameras
  R: [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
  T: [0.06, 0, 0]
```

### Extrinsics (Per-Frame Pose) - EVERY CAPTURE

```csv
# pose_log.csv - logged at each capture
image_id,timestamp_us,lat,lon,alt,roll,pitch,yaw,rtk_fix,hdop,sats
0,1705000000000,51.50743200,-0.12781500,45.234,0.012,-0.034,1.571,4,0.8,18
1,1705000002000,51.50743850,-0.12780200,45.267,0.008,-0.029,1.623,4,0.7,19
...
```

**RTK guarantees:**
- Position: ±1-3cm
- Repeatability: Same coordinates every flight
- Scale: Exactly 1 unit = 1 meter

---

## RTK Setup Options (Detailed)

### Option 1: NTRIP (Recommended Start)

**What you need:**
- Phone with data plan (hotspot)
- OR 4G module on drone (~$30, 15g)

**Setup:**
```bash
# On CM5, run NTRIP client
str2str -in ntrip://user:pass@rtk2go.com:2101/MOUNTPOINT \
        -out serial://ttyUSB0:115200
```

**Free NTRIP sources:**
- rtk2go.com (community)
- Your national geodetic survey (many countries offer free)

**Cost:** $0-50/month
**Accuracy:** 1-3cm (within 30km of base)

### Option 2: Own Base Station

**What you need:**
- Second ZED-F9P + antenna (~$200)
- Tripod
- Radio link (915MHz or 2.4GHz, ~$100)

**Setup:**
```
BASE STATION              RADIO LINK              ROVER (DRONE)
ZED-F9P ──► Radio TX ════════════════► Radio RX ──► ZED-F9P
(known position)                                    (corrected)
```

**Cost:** ~$300 extra
**Accuracy:** 1-2cm
**Benefit:** Works without cell coverage

### Option 3: PPK (Post-Processed)

**What you need:**
- Nothing extra (same hardware)

**How it works:**
1. Drone logs raw GNSS observations
2. Download RINEX data from nearby CORS station (free)
3. Process with RTKLIB after flight

**Cost:** $0
**Accuracy:** Same as RTK (1-2cm)
**Downside:** Not real-time (process after flight)

### Recommendation

**Start with NTRIP:**
- No extra hardware
- Works immediately
- Good enough for most locations

**Add base station later if:**
- Flying in remote areas (no cell)
- Need maximum reliability
- Flying same location repeatedly

---

## Parts List (Complete)

### From Your Existing Build

| Part | Status |
|------|--------|
| Happymodel Crux35 frame | ✓ Have |
| T-Motor F1404 3800kv ×4 | ✓ Have |
| HQProp T3.5x2.5x3 | ✓ Have |
| MicoAir743-AIO-35A | ✓ Have |
| GNB 4S 850mAh HiLV | ✓ Have |

### New Parts to Order

| Part | Model | Source | Price |
|------|-------|--------|-------|
| RTK GPS | SparkFun GPS-RTK-SMA (ZED-F9P) | SparkFun | $275 |
| RTK Antenna | SparkFun GNSS Multi-Band L1/L2 | SparkFun | $40 |
| Compute | Raspberry Pi CM5 Lite 4GB | RPi/Adafruit | $45 |
| Carrier | Piunora Lite | Pimoroni | $35 |
| Camera L | Arducam OV2311 2MP Global Shutter | Arducam | $40 |
| Camera R | Arducam OV2311 2MP Global Shutter | Arducam | $40 |
| AI Accel | Raspberry Pi AI Kit (Hailo-8L) | RPi | $70 |
| Opt Flow | Matek 3901-L0X | GetFPV | $30 |
| FPV | Caddx Ant Lite | GetFPV | $15 |
| MicroSD | Samsung EVO 128GB | Amazon | $15 |
| Cables | FFC + JST kit | Amazon | $20 |
| **Total** | | | **~$625** |

**Note:** SparkFun ZED-F9P includes antenna connector. Cheaper F9P modules available from AliExpress (~$150) but less support.

---

## Summary

| Question | Answer |
|----------|--------|
| RTK ground station needed? | **No - use NTRIP** (add base later if needed) |
| Separate CV vs splat camera? | **No - stereo pair does both** |
| Image quality vs DJI? | **Different trade-off: sharp > high-res for 3DGS** |
| Intrinsics? | **Pre-calibrate once, store on CM5** |
| Extrinsics? | **RTK pose logged at each capture** |
| Obstacle avoidance? | **Stereo depth → Hailo → path replan** |
| Total weight? | **232g (under 250g)** |
| Total cost? | **~$625 for payload** |
