# Crux35 3DGS Capture - Three-Tier Modular Build

## Design Philosophy

All three tiers share:
- **Common connector system** - Same pinout for swapping modules
- **Modular mounting plate** - 3D printed, accepts different payloads
- **Unified software stack** - Same PX4 + MAVLink interface
- **Future-proof expansion** - AI accelerator headers built-in

```
┌─────────────────────────────────────────────────────────────────┐
│                    MODULAR ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   TIER 1 (Cheap)     TIER 2 (Medium)      TIER 3 (Premium)      │
│   ┌──────────┐       ┌──────────┐         ┌──────────┐          │
│   │ Basic GPS│       │ M9N GPS  │         │ RTK F9P  │          │
│   └────┬─────┘       └────┬─────┘         └────┬─────┘          │
│        │                  │                    │                 │
│        ▼                  ▼                    ▼                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              UNIVERSAL CARRIER BOARD                     │   │
│   │   • Standard connectors (JST-SH 1.0mm)                  │   │
│   │   • I2C / SPI / UART headers                            │   │
│   │   • AI accelerator slot (M.2 / USB)                     │   │
│   │   • Camera CSI / USB interface                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│        │                  │                    │                 │
│        ▼                  ▼                    ▼                 │
│   ┌──────────┐       ┌──────────┐         ┌──────────┐          │
│   │  ESP32   │       │ Pi Zero  │         │ CM5 Lite │          │
│   │  $15     │       │ 2W $15   │         │ + carrier │          │
│   └──────────┘       └──────────┘         └──────────┘          │
│        │                  │                    │                 │
│        ▼                  ▼                    ▼                 │
│   ┌──────────┐       ┌──────────┐         ┌──────────┐          │
│   │ 16MP Cam │       │ GS Cam   │         │ Dual GS  │          │
│   │  $30     │       │  $50     │         │ Stereo   │          │
│   └──────────┘       └──────────┘         └──────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Weight Budget (All Tiers)

| Component | Weight | All Tiers |
|-----------|--------|-----------|
| Crux35 frame | 26g | ✓ |
| T-Motor F1404 x4 | 37g | ✓ |
| HQProp T3.5x2.5x3 | 5g | ✓ |
| MicoAir743-AIO-35A | 10g | ✓ |
| GNB 4S 850mAh | 75g | ✓ |
| Base wiring | 5g | ✓ |
| **Base Total** | **158g** | |
| **Payload Budget** | **92g** | |

---

## Tier 1: Budget Build (~$100)

### Purpose
- Learn the workflow
- Prove the concept
- Outdoor photogrammetry
- Offline processing only

### Components

| Part | Model | Weight | Cost |
|------|-------|--------|------|
| GPS | Matek M10Q-5883 | 8g | $25 |
| Companion | Seeed XIAO ESP32S3 | 3g | $15 |
| Camera | Arducam 16MP IMX519 | 5g | $30 |
| SD Module | MicroSD breakout | 2g | $5 |
| Carrier PCB | Custom (see below) | 4g | $15 |
| Wiring/mount | JST cables + 3D print | 6g | $10 |
| **Total Payload** | | **28g** | **$100** |

### Total Weight: **186g** ✓ (64g margin)

### Capabilities

| Feature | Status |
|---------|--------|
| GPS position hold | ✓ |
| Waypoint missions | ✓ |
| Image capture | ✓ 16MP rolling shutter |
| Pose logging | ✓ via ESP32 |
| Extrinsics export | ✓ GPS + IMU poses |
| Intrinsics | ✓ Pre-calibrated |
| Real-time processing | ✗ |
| Indoor flight | ✗ (no optical flow) |
| RTK accuracy | ✗ |
| AI inference | ✗ |

### Expansion Headers (Built-in for future)

```
┌─────────────────────────────────────────┐
│           TIER 1 CARRIER PCB            │
├─────────────────────────────────────────┤
│                                         │
│  [GPS]────UART1────[ESP32S3]            │
│                        │                │
│  [CAM]────USB/SPI──────┤                │
│                        │                │
│  [PX4]────UART0────────┤                │
│           (MAVLink)    │                │
│                        │                │
│  ┌─────────────────────┴──────┐         │
│  │     EXPANSION HEADERS      │         │
│  │  • I2C (for sensors)       │         │
│  │  • SPI (for AI module)     │         │
│  │  • USB (for upgrade)       │         │
│  │  • 5V/3.3V power rails     │         │
│  └────────────────────────────┘         │
│                                         │
└─────────────────────────────────────────┘
```

### Bill of Materials

```
TIER 1 BOM
──────────────────────────────────────────────────────────────
Qty  Part                          Supplier        Price
──────────────────────────────────────────────────────────────
1    Matek M10Q-5883 GPS           GetFPV          $25
1    Seeed XIAO ESP32S3            Seeed Studio    $15
1    Arducam 16MP IMX519           Amazon          $30
1    MicroSD module                Amazon          $5
1    Custom carrier PCB            JLCPCB          $15 (5pcs)
1    JST-SH cable set              Amazon          $8
1    3D printed mount              Self            $2
──────────────────────────────────────────────────────────────
                                   TOTAL:          $100
```

---

## Tier 2: Mid-Range Build (~$250)

### Purpose
- Production-quality captures
- Indoor + outdoor capability
- Global shutter for motion
- Better position accuracy
- Path to AI acceleration

### Components

| Part | Model | Weight | Cost |
|------|-------|--------|------|
| GPS | u-blox M9N (SAM-M9N) | 5g | $50 |
| Compass | IST8310 (separate) | 1g | $8 |
| Companion | Raspberry Pi Zero 2W | 12g | $15 |
| Camera | Arducam 2MP Global Shutter OV2311 | 3g | $50 |
| Optical Flow | PMW3901 + VL53L1X | 3g | $25 |
| SD Card | In Pi Zero | 0g | $0 |
| Carrier PCB | Custom v2 | 5g | $20 |
| Wiring/mount | | 8g | $15 |
| **Total Payload** | | **37g** | **$183** |

### Optional Add-ons (Modular)

| Add-on | Weight | Cost | Purpose |
|--------|--------|------|---------|
| Coral USB Accelerator | +5g | $60 | Edge AI |
| 2nd camera (stereo) | +3g | $50 | Depth |
| Barometer (external) | +1g | $10 | Better altitude |
| **With all options** | **46g** | **$303** | |

### Total Weight: **195g base / 204g full** ✓

### Capabilities

| Feature | Status |
|---------|--------|
| GPS position hold | ✓ Better accuracy (1.5m CEP) |
| Waypoint missions | ✓ |
| Image capture | ✓ 2MP global shutter |
| Pose logging | ✓ via Pi Zero |
| Extrinsics export | ✓ Higher precision |
| Intrinsics | ✓ Pre-calibrated |
| Real-time preview | ✓ (limited) |
| Indoor flight | ✓ Optical flow |
| RTK accuracy | ✗ (upgrade path) |
| AI inference | ✓ With Coral TPU |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TIER 2 SYSTEM                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐     ┌──────────────────────────────────────┐  │
│  │  M9N GPS │────►│                                      │  │
│  └──────────┘     │         RASPBERRY PI ZERO 2W         │  │
│                   │                                      │  │
│  ┌──────────┐     │   • ROS2 (minimal)                   │  │
│  │ PMW3901  │────►│   • MAVLink interface                │  │
│  │ Opt Flow │     │   • Camera capture                   │  │
│  └──────────┘     │   • Pose logging                     │  │
│                   │   • Mission management               │  │
│  ┌──────────┐     │                                      │  │
│  │ VL53L1X  │────►│   ┌────────────────────────────┐    │  │
│  │ ToF      │     │   │    EXPANSION SLOT          │    │  │
│  └──────────┘     │   │  ┌──────────────────────┐  │    │  │
│                   │   │  │   Coral USB TPU      │  │    │  │
│  ┌──────────┐     │   │  │   (optional $60)     │  │    │  │
│  │ OV2311   │────►│   │  └──────────────────────┘  │    │  │
│  │ GS Cam   │     │   └────────────────────────────┘    │  │
│  └──────────┘     │                                      │  │
│                   └──────────────────────────────────────┘  │
│                              │                               │
│                         MAVLink                              │
│                              │                               │
│                   ┌──────────▼──────────┐                   │
│                   │  MicoAir743 (PX4)   │                   │
│                   └─────────────────────┘                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Bill of Materials

```
TIER 2 BOM (Base)
──────────────────────────────────────────────────────────────
Qty  Part                          Supplier        Price
──────────────────────────────────────────────────────────────
1    u-blox SAM-M9N module         Mouser          $50
1    IST8310 compass breakout      AliExpress      $8
1    Raspberry Pi Zero 2W          RPi/Adafruit    $15
1    Arducam OV2311 Global Shutter Arducam         $50
1    PMW3901 optical flow          Matek/GetFPV    $18
1    VL53L1X ToF rangefinder       Pololu          $12
1    Custom carrier PCB v2         JLCPCB          $20
1    MicroSD 64GB                  Amazon          $10
1    JST/FFC cables                Amazon          $10
1    3D printed mount v2           Self            $5
──────────────────────────────────────────────────────────────
                                   TOTAL:          $198

OPTIONAL ADD-ONS
──────────────────────────────────────────────────────────────
1    Google Coral USB Accelerator  Coral           $60
1    2nd OV2311 (stereo)           Arducam         $50
──────────────────────────────────────────────────────────────
                                   WITH OPTIONS:   $308
```

### Why Global Shutter Matters (Even at 2MP)

| Scenario | Rolling Shutter 16MP | Global Shutter 2MP |
|----------|---------------------|-------------------|
| Hovering | Good | Good |
| Slow flight | OK (some skew) | Perfect |
| Fast maneuver | Jello/blur | Perfect |
| COLMAP matching | May fail | Reliable |
| 3DGS quality | Artifacts | Clean geometry |

**For 3DGS, sharp 2MP > blurry 16MP**

---

## Tier 3: Premium Build (~$500-700)

### Purpose
- Professional-quality results
- RTK centimeter positioning
- Real-time SLAM capability
- Full AI acceleration
- Research/development platform

### Components

| Part | Model | Weight | Cost |
|------|-------|--------|------|
| GPS | u-blox ZED-F9P RTK | 10g | $180 |
| RTK Antenna | Tallysman patch | 8g | $40 |
| Companion | Pi CM5 Lite 4GB + Piunora | 25g | $75 |
| Camera 1 | Arducam OV2311 GS | 3g | $50 |
| Camera 2 | Arducam OV2311 GS (stereo) | 3g | $50 |
| AI Accelerator | Coral M.2 TPU | 2g | $35 |
| Optical Flow | PMW3901 + VL53L1X | 3g | $25 |
| Carrier PCB | Custom v3 | 6g | $30 |
| Wiring/mount | | 10g | $20 |
| **Total Payload** | | **70g** | **$505** |

### Optional Add-ons

| Add-on | Weight | Cost | Purpose |
|--------|--------|------|---------|
| Hailo-8L M.2 | +3g | $70 | 13 TOPS AI |
| IMU upgrade (ICM-42688) | +1g | $15 | Better fusion |
| 2nd RTK antenna (heading) | +8g | $40 | Dual-antenna RTK |
| **Max config** | **82g** | **$630** | |

### Total Weight: **228g base / 240g full** ✓

### Capabilities

| Feature | Status |
|---------|--------|
| GPS position hold | ✓ RTK (1-3cm accuracy) |
| Waypoint missions | ✓ Precise |
| Image capture | ✓ Stereo global shutter |
| Pose logging | ✓ cm-level |
| Extrinsics export | ✓ Survey-grade |
| Intrinsics | ✓ Pre-calibrated stereo |
| Real-time SLAM | ✓ (with AI assist) |
| Indoor flight | ✓ Optical flow + stereo |
| RTK accuracy | ✓ 1-3cm |
| AI inference | ✓ Coral/Hailo onboard |
| Depth estimation | ✓ Stereo + AI |
| Edge 3DGS | ✓ (experimental) |

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TIER 3 SYSTEM                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────┐                                                 │
│  │  ZED-F9P RTK   │─────────────────────────────┐                  │
│  │  + Patch Ant   │                             │                  │
│  └────────────────┘                             │                  │
│                                                 │                  │
│  ┌────────────────┐     ┌───────────────────────▼────────────────┐ │
│  │    PMW3901     │────►│                                        │ │
│  │   + VL53L1X    │     │         RASPBERRY PI CM5               │ │
│  └────────────────┘     │         (on Piunora carrier)           │ │
│                         │                                        │ │
│  ┌────────────────┐     │   • Ubuntu 24.04 / ROS2 Jazzy          │ │
│  │   OV2311 #1    │────►│   • FAST-LIO2 / Stereo SLAM            │ │
│  │   (Left cam)   │     │   • Real-time pose estimation          │ │
│  └────────────────┘     │   • MAVLink ↔ PX4                      │ │
│                         │   • Mission planning                   │ │
│  ┌────────────────┐     │                                        │ │
│  │   OV2311 #2    │────►│   ┌──────────────────────────────────┐ │ │
│  │   (Right cam)  │     │   │         M.2 SLOT                 │ │ │
│  └────────────────┘     │   │  ┌────────────────────────────┐  │ │ │
│                         │   │  │     Coral Edge TPU         │  │ │ │
│                         │   │  │     (or Hailo-8L)          │  │ │ │
│                         │   │  │                            │  │ │ │
│                         │   │  │  • Depth estimation        │  │ │ │
│                         │   │  │  • Object detection        │  │ │ │
│                         │   │  │  • Semantic segmentation   │  │ │ │
│                         │   │  │  • 3DGS preprocessing      │  │ │ │
│                         │   │  └────────────────────────────┘  │ │ │
│                         │   └──────────────────────────────────┘ │ │
│                         │                                        │ │
│                         └────────────────────────────────────────┘ │
│                                        │                           │
│                                   MAVLink                          │
│                                        │                           │
│                         ┌──────────────▼──────────────┐           │
│                         │     MicoAir743 (PX4)        │           │
│                         │                             │           │
│                         │  External pose input from   │           │
│                         │  CM5 (visual-inertial)     │           │
│                         └─────────────────────────────┘           │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### RTK Setup Options

```
OPTION A: NTRIP (Internet-based corrections)
──────────────────────────────────────────────
• Requires cellular/WiFi connection on drone
• Free or low-cost NTRIP services available
• ~1-3cm accuracy within 30km of base

OPTION B: Local Base Station
──────────────────────────────────────────────
• Set up your own base (~$300 extra)
• Radio link to rover (900MHz or 2.4GHz)
• Best accuracy, no internet needed
• Portable for field work

OPTION C: Post-Processed Kinematic (PPK)
──────────────────────────────────────────────
• Log raw GNSS on drone
• Process with RINEX data after flight
• Same accuracy as RTK
• No real-time link needed
• Recommended for reliability
```

### Bill of Materials

```
TIER 3 BOM (Base)
──────────────────────────────────────────────────────────────
Qty  Part                          Supplier        Price
──────────────────────────────────────────────────────────────
1    u-blox ZED-F9P module         SparkFun        $180
1    Tallysman TW4722 antenna      Mouser          $40
1    Raspberry Pi CM5 Lite 4GB     RPi             $45
1    Piunora carrier board         Pimoroni        $30
1    Arducam OV2311 GS (x2)        Arducam         $100
1    Google Coral M.2 TPU          Coral           $35
1    PMW3901 + VL53L1X combo       Matek           $30
1    Custom carrier PCB v3         JLCPCB          $30
1    MicroSD 128GB                 Amazon          $15
1    Cables and connectors         Various         $20
1    3D printed mount v3           Self            $5
──────────────────────────────────────────────────────────────
                                   TOTAL:          $530

OPTIONAL UPGRADES
──────────────────────────────────────────────────────────────
1    Hailo-8L M.2 (instead of Coral)              $70
1    2nd RTK antenna (heading)                    $40
1    ICM-42688 IMU module                         $15
1    RTK base station kit                         $300
──────────────────────────────────────────────────────────────
```

### CM5 vs Alternatives

| Option | Weight | Compute | AI Ready | Cost |
|--------|--------|---------|----------|------|
| Pi Zero 2W | 12g | Low | USB only | $15 |
| **CM5 Lite + Piunora** | **25g** | **High** | **M.2 slot** | **$75** |
| Jetson Orin Nano | 60g+ | Very High | Built-in | $500 |
| Orange Pi 5 | 40g | High | M.2 slot | $80 |

**CM5 is the sweet spot** for sub-250g with AI capability.

---

## Modular Carrier PCB Design

### Universal Connector Pinout

All tiers use the same connector system for interchangeability:

```
MAIN CONNECTOR (JST-SH 10-pin)
─────────────────────────────────────
Pin  Signal      Description
─────────────────────────────────────
1    VCC         5V power
2    GND         Ground
3    TX          UART TX (to PX4)
4    RX          UART RX (from PX4)
5    SDA         I2C data
6    SCL         I2C clock
7    TRIG        Camera trigger
8    SYNC        Time sync pulse
9    GPIO1       General purpose
10   GPIO2       General purpose
─────────────────────────────────────

GPS CONNECTOR (JST-SH 6-pin)
─────────────────────────────────────
Pin  Signal      Description
─────────────────────────────────────
1    VCC         3.3V power
2    GND         Ground
3    TX          GPS TX
4    RX          GPS RX
5    PPS         Pulse per second
6    INT         Interrupt (optional)
─────────────────────────────────────

CAMERA CONNECTOR (FFC 15-pin CSI or USB)
─────────────────────────────────────
Tier 1: USB to ESP32
Tier 2: CSI to Pi Zero
Tier 3: Dual CSI to CM5
─────────────────────────────────────

AI EXPANSION (M.2 Key E or USB)
─────────────────────────────────────
Tier 1: USB header (for future Coral USB)
Tier 2: USB-A port (Coral USB plugs in)
Tier 3: M.2 Key E slot (Coral/Hailo)
─────────────────────────────────────
```

### PCB Specifications

```
CARRIER PCB v1/v2/v3
─────────────────────────────────────
Size:        30mm x 30mm (stack compatible)
Layers:      4-layer
Thickness:   0.8mm
Weight:      ~4-6g
Mounting:    M2 holes, 20x20mm and 25x25mm patterns
Power:       5V input, 3.3V regulator onboard
```

---

## Upgrade Paths

### Tier 1 → Tier 2

| Swap | Remove | Add | Weight Δ | Cost |
|------|--------|-----|----------|------|
| GPS | M10Q (8g) | M9N (5g) | -3g | +$25 |
| Companion | ESP32 (3g) | Pi Zero (12g) | +9g | +$0 |
| Camera | 16MP rolling (5g) | 2MP GS (3g) | -2g | +$20 |
| Add | - | Optical flow (3g) | +3g | +$30 |
| **Net** | | | **+7g** | **+$75** |

### Tier 2 → Tier 3

| Swap | Remove | Add | Weight Δ | Cost |
|------|--------|-----|----------|------|
| GPS | M9N (5g) | F9P+ant (18g) | +13g | +$170 |
| Companion | Pi Zero (12g) | CM5+carrier (25g) | +13g | +$60 |
| Camera | 1x GS (3g) | 2x GS stereo (6g) | +3g | +$50 |
| AI | Coral USB (5g) | Coral M.2 (2g) | -3g | -$25 |
| **Net** | | | **+26g** | **+$255** |

### Adding AI to Any Tier

| Tier | AI Option | Weight | Cost | TOPS |
|------|-----------|--------|------|------|
| 1 | Coral USB | +5g | +$60 | 4 |
| 2 | Coral USB | +5g | +$60 | 4 |
| 3 | Coral M.2 | +2g | +$35 | 4 |
| 3 | Hailo-8L M.2 | +3g | +$70 | 13 |

---

## Comparison Summary

| Feature | Tier 1 ($100) | Tier 2 ($200) | Tier 3 ($530) |
|---------|---------------|---------------|---------------|
| **Weight** | 28g | 37g | 70g |
| **Total AUW** | 186g | 195g | 228g |
| **Margin** | 64g | 55g | 22g |
| | | | |
| **GPS Accuracy** | 2.5m | 1.5m | 1-3cm |
| **Position Hold** | Good | Better | Excellent |
| **Indoor Flight** | No | Yes | Yes |
| | | | |
| **Camera** | 16MP rolling | 2MP global | 2MP stereo GS |
| **Motion Tolerance** | Low | High | High |
| **Depth** | COLMAP only | COLMAP+AI | Stereo+AI |
| | | | |
| **Companion** | ESP32 | Pi Zero 2W | CM5 |
| **Real-time** | No | Limited | Yes |
| **AI Ready** | Header only | USB Coral | M.2 Coral/Hailo |
| **SLAM** | Offline | Basic | Full |
| | | | |
| **3DGS Quality** | Good | Better | Best |
| **Georeferencing** | ~3m | ~2m | ~3cm |
| **Use Case** | Learning | Production | Professional |

---

## Recommended Starting Point

### If Budget Constrained: **Start Tier 1**
- Prove the concept works
- Learn the workflow
- Upgrade to Tier 2 camera first (+$20, better results)
- Add optical flow when needed (+$30, indoor capability)

### If Serious About Quality: **Start Tier 2**
- Global shutter is worth it
- Indoor capability from day one
- Add Coral TPU for AI experiments
- Upgrade to RTK later if needed

### If Professional/Research: **Go Tier 3**
- RTK is essential for survey work
- Stereo gives best depth
- CM5 handles real-time processing
- Future-proof for advanced AI

---

## Files Included

```
lidar-splat-hardware/
├── CRUX35-3DGS-BUILD.md          # This document
├── pcb/
│   ├── carrier-v1-esp32.kicad    # Tier 1 PCB
│   ├── carrier-v2-pizero.kicad   # Tier 2 PCB
│   └── carrier-v3-cm5.kicad      # Tier 3 PCB
├── cad/
│   ├── mount-tier1.stl           # 3D print files
│   ├── mount-tier2.stl
│   └── mount-tier3.stl
├── firmware/
│   ├── tier1-esp32/              # ESP32 companion code
│   ├── tier2-pizero/             # Pi Zero ROS2 setup
│   └── tier3-cm5/                # CM5 full stack
└── scripts/
    ├── generate_waypoints.py     # Mission planning
    ├── poses_to_colmap.py        # Post-processing
    └── calibrate_camera.py       # Camera calibration
```

---

## Quick Decision Matrix

```
Budget < $150?
    └─► TIER 1

Need indoor flight?
    └─► TIER 2 minimum (optical flow)

Need cm-level accuracy?
    └─► TIER 3 (RTK)

Want AI experiments?
    └─► TIER 2 + Coral USB, or TIER 3

Want real-time SLAM?
    └─► TIER 3 (CM5 required)

Want best 3DGS quality?
    └─► TIER 3 (stereo + AI depth)

Just want to learn?
    └─► TIER 1, upgrade later
```
