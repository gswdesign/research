# Sub-250g UK Autonomous Drone Hardware Research

## Overview

This document researches hardware choices for a sub-250g autonomous drone build targeting UK regulations, with a focus on computer vision and edge AI capabilities for autonomous flight.

**Target Weight Budget:** <250g (UK sub-250g category benefits)

---

## 1. Base Platform Components (User-Specified)

### 1.1 Frame: Happymodel Crux35

| Specification | Value |
|---------------|-------|
| Weight | **26g** |
| Material | 3K Carbon Fiber |
| Wheelbase | 150mm |
| Bottom Plate | 3mm thick |
| FC Mounting | 25.5×25.5mm and 20×20mm (M2) |
| Camera Mount | Nano size (14mm) |
| Motor Mount | 9mm M2 |

**Notes:** The Crux35 is an ultralight 3.5" frame designed for micro freestyle builds. Its dual FC mounting pattern provides flexibility for different flight controllers.

**Source:** [Happymodel Official](https://www.happymodel.cn/index.php/2021/07/20/crux35-crux35-hd-3-5inch-fpv-racer-drone-frame-kit/)

---

### 1.2 Motors: T-Motor F1404 3800KV (×4)

| Specification | Value |
|---------------|-------|
| Weight (motor only) | **7.75g** |
| Weight (with cable) | **9.34g** |
| Max Power (60s) | 304W |
| Prop Compatibility | 2.5" - 4" |
| KV Rating | 3800KV |

**Total Motor Weight:** 4 × 9.34g = **37.36g**

**Notes:** The F1404 3800KV is optimized for 3" micro long-range builds, offering excellent balance between power and efficiency. The 3800KV variant pairs well with 3.5" props on 4S.

**Source:** [Pyrodrone](https://pyrodrone.com/products/t-motor-f1404-micro-long-range-motors-3800kv)

---

### 1.3 Propellers: HQProp T3.5×2.5×3 (×4)

| Specification | Value |
|---------------|-------|
| Weight | **1.55g** per prop |
| Diameter | 3.5 inch |
| Pitch | 2.5 |
| Blades | 3 (tri-blade) |
| Material | Polycarbonate |
| Hub Diameter | 10mm |

**Total Prop Weight:** 4 × 1.55g = **6.2g**

**Notes:** Tri-blade design offers good thrust for freestyle maneuvers while maintaining efficiency.

**Source:** [HQProp Official](https://www.hqprop.com/hqprop-t35x25x3-2cw2ccw-poly-carbonate-p0354.html)

---

### 1.4 Flight Controller: MicoAir743-AIO-35A (PX4)

| Specification | Value |
|---------------|-------|
| MCU | STM32H743VIH6, 480MHz, 2MB Flash |
| IMU | BMI088 + BMI270 (Dual IMU) |
| Barometer | DPS310 |
| ESC | 35A × 4, AM32 firmware |
| Voltage Support | 3-6S (8.5V-27V) |
| Mounting | 25×25mm |
| BEC Output | 5V/2A + 12V/2A |
| Firmware Support | **PX4**, ArduPilot, Betaflight, INAV |
| Weight | **~10-12g** (estimated) |

**Key Features:**
- Official PX4 support from v1.16.0
- Dual IMU for redundancy
- USB Type-C
- TF Card slot for logging
- 7× UART for companion computer, GPS, telemetry

**Notes:** The AIO design integrates FC and ESC, saving weight and wiring complexity. PX4 support is critical for autonomous operations including waypoint navigation, offboard control, and companion computer integration.

**Source:** [MicoAir Official](https://micoair.com/flightcontroller_micoair743_aio_35a/)

**MicoAir YouTube Tutorials:**
- [Setup Optical Flow & Lidar (MTF-01) for ArduPilot/PX4](https://youtube.com/watch?v=D-ooFHEtQoo)
- [Setup Optical Flow & Lidar (MTF-01) for INAV6](https://youtube.com/watch?v=bEKm-PGRnks)

---

### 1.4a MicoAir MTF-01 Optical Flow & Lidar Sensor (Recommended Add-on)

| Specification | Value |
|---------------|-------|
| Weight | **4.5g** |
| Dimensions | 29 × 16.5 × 15mm |
| Optical Flow Sensor | PMW3901 |
| Range Sensor | TOF (Time of Flight) |
| Range Distance | 0.02-8m (±2% accuracy) |
| Ambient Light Resistance | Up to 70K Lux |
| Min Height | 8cm |
| Max Speed | 7 m/s @ 1m altitude |
| Optical Flow FoV | 42° |
| Min Light Required | 60 Lux |
| Operating Voltage | 4.0-5.5V |
| Interface | UART |
| Protocol Support | **ArduPilot, PX4, INAV** |

**Key Features:**
- 2-in-1 sensor combining optical flow + lidar rangefinder
- Works in outdoor sunlight (70K Lux resistance)
- Direct UART connection to MicoAir743 flight controller
- No complex development - plug and configure
- MicoAssistant software for protocol switching

**Why Essential for Autonomous Flight:**
- Enables precise indoor hovering without GPS
- Provides altitude hold via TOF sensor
- Ground-relative velocity for position hold
- Critical for landing pad detection and precision landing

**Configuration Notes:**
- For indoor-only flight, configure EK3_SRC1 parameters
- INAV users: Use v7.1.2+ (v7.1.1 has bugs with this sensor)
- Switch protocols via USB-TTL programmer + MicoAssistant

**Source:** [MicoAir MTF-01](https://micoair.com/optical_range_sensor_mtf-01/)

---

### 1.4b MicoAir MTF-01P (Extended Range Variant)

| Specification | Value |
|---------------|-------|
| Weight | **~5g** (estimated) |
| Range Distance | 0.02-12m |
| Other specs | Same as MTF-01 |

**Notes:** The MTF-01P offers 50% more range (12m vs 8m) for applications requiring greater altitude sensing. Slightly heavier but useful for outdoor autonomous operations.

**Source:** [MicoAir MTF-01P](https://micoair.com/optical_range_sensor_mtf-01p/)

---

### 1.5 Battery: GNB 4S 850mAh HV (60C Long Range)

| Specification | Value |
|---------------|-------|
| Capacity | 850mAh |
| Voltage | 15.2V (4S HV LiPo) |
| C-Rating | 60C continuous / 120C burst |
| Dimensions | 32×18×73mm |
| Weight | **73g** (±2g) |
| Connector | XT30 |

**Notes:** The 60C "long range" variant is lighter (73g) compared to the 120C variant (88g). HV cells provide slightly higher voltage for improved efficiency.

**Source:** [Pyrodrone](https://pyrodrone.com/products/gaoneng-gnb-850mah-4s-15-2v-60c-120c-xt30)

---

## 2. Weight Budget Analysis

### Base Platform Total

| Component | Weight |
|-----------|--------|
| Frame (Crux35) | 26g |
| Motors (4× F1404) | 37g |
| Props (4× T3.5×2.5×3) | 6g |
| Flight Controller (MicoAir743-AIO) | ~11g |
| Optical Flow/Lidar (MTF-01) | 4.5g |
| Battery (GNB 4S 850mAh) | 73g |
| **Subtotal** | **~157.5g** |

### Remaining Budget for CV/AI System

```
Target Max Weight:     250g
Base Platform:        -157.5g
Wiring/Misc (~5g):     -5g
━━━━━━━━━━━━━━━━━━━━━━━━━━━
CV/AI Budget:          ~87.5g
```

**Available weight for camera + companion computer + AI accelerator: ~85-90g**

**Note:** The MTF-01 optical flow/lidar provides basic autonomous hover capability without needing a companion computer. Add CV/AI only if you need object detection, tracking, or advanced autonomy beyond GPS waypoints.

---

## 3. CV Camera Options

### 3.1 Raspberry Pi Camera Module 3 (Recommended for Pi Zero 2W)

| Specification | Value |
|---------------|-------|
| Weight | **~14.5g** (gross) |
| Sensor | Sony IMX708 |
| Resolution | 12MP (4608×2592) |
| Video | 1080p@50fps, 720p@120fps |
| FoV | 75° (standard) / 120° (wide) |
| Features | HDR, Phase-detect autofocus |

**Pros:** High resolution, autofocus, HDR, official Pi support
**Cons:** Rolling shutter, larger size, autofocus may not be needed for CV

**Source:** [Raspberry Pi](https://www.raspberrypi.com/products/camera-module-3/)

---

### 3.2 ArduCam OV9281 Global Shutter (Recommended for CV)

| Specification | Value |
|---------------|-------|
| Weight | **~3-5g** (module dependent) |
| Sensor | OmniVision OV9281 |
| Resolution | 1MP (1280×800) |
| Frame Rate | Up to 100fps (USB) / 60fps (MIPI) |
| Shutter | **Global Shutter** |
| Interface | MIPI CSI / USB |

**Pros:** Global shutter eliminates motion blur, high frame rate, excellent for AprilTag/marker detection, lightweight
**Cons:** Monochrome only (ideal for CV), lower resolution

**Best For:** Optical flow, AprilTag detection, high-speed tracking, SLAM

**Source:** [ArduCam](https://www.arducam.com/product/mini-ov9281-mono-global-shutter-for-pi/)

---

### 3.3 OpenMV Camera Sensors (for OpenMV H7)

| Sensor | Resolution | Shutter | Weight |
|--------|------------|---------|--------|
| OV5640 (default H7+) | 5MP | Rolling | Included |
| OV7725 (default H7) | VGA | Global | Included |
| MT9V034 (optional) | VGA | Global | ~2g module |

**Source:** [OpenMV](https://openmv.io/products/openmv-cam-h7-plus)

---

### 3.4 Intel RealSense D430 Depth Module (MicoAir Reference Setup)

| Specification | Value |
|---------------|-------|
| Weight | **13g** (module only) |
| Dimensions | 70.5 × 10.3 × 13.8mm |
| Depth Resolution | **1280×800** (~1.02MP equivalent) |
| Depth FPS | 30fps @ 1280×720, 90fps @ 848×480 |
| Shutter | **Global Shutter** (stereo) |
| Field of View | 91.2° × 65.5° × 100.6° (H×V×D) |
| Baseline | 50mm |
| Operating Range | 0.2m - 10m |
| Technology | Active IR Stereoscopic |
| Interface | 50-pin Board-to-Board connector |
| Power | <1.5W |

**Requires Vision Processor D4 Board:**

| Specification | Value |
|---------------|-------|
| Weight | **~5-8g** (estimated) |
| Dimensions | 73 × 16 × 4mm |
| Interface | USB 3.0 Type-C |
| Function | Depth processing, USB output |

**Combined D430 + D4 Board Weight: ~18-21g**

**Key Features:**
- True depth sensing (not just optical flow)
- Global shutter eliminates motion artifacts
- Works in low-light with IR projector
- Designed for robotics and drone applications
- Indoor optimized (outdoor use limited)

**Why Use for Autonomous Drones:**
- 3D obstacle avoidance
- SLAM (Simultaneous Localization and Mapping)
- Precise landing with depth perception
- Object distance measurement
- Works with ROS and PX4 via companion computer

**Limitations:**
- Indoor use primarily (struggles in direct sunlight)
- Requires companion computer (Pi CM5/Jetson) for processing
- USB interface needs processor board

**Source:** [Intel RealSense D430](https://www.intel.com/content/www/us/en/products/sku/98320/intel-realsense-depth-module-d430/specifications.html)

---

### 3.5 D430 Alternatives Comparison (2025/2026)

| Depth Camera | Weight | Resolution | Range | On-device AI | Interface | Notes |
|--------------|--------|------------|-------|--------------|-----------|-------|
| **Intel D430 + D4** | **~19g** | 1280×800 | 0.2-10m | No | USB 3.0 | Proven, indoor-optimized |
| Intel D421 | ~25-30g | 1280×800 | 0.2-10m | No | USB 3.0 | All-in-one module, newer |
| OAK-D Lite | **~61g** | 640×480 stereo | 0.2-19m | **4 TOPS** | USB 3.0 | On-device NN, heavier |
| OAK-D SR | 72g | 1MP stereo | 0.3-1m | 4 TOPS | USB 3.0 | Short-range only |
| OAK-FFC 4P (no case) | ~41g + cams | Flexible | Varies | 4 TOPS | USB 3.0 | Modular, customizable |
| Arducam TOF | ~15-20g (est.) | 240×180 | 0.02-4m | No | MIPI CSI | Low-res, Pi-native |
| PMD pico flexx | **8g** | 224×171 | 0.1-4m | No | USB | **Discontinued** |
| Terabee Evo 3D | ~12g | 80×60 (8×8 zones) | 0.1-5m | No | I2C/UART | Low-res depth zones |

**Key Findings:**

1. **D430 + D4 at ~19g is hard to beat** for true stereo depth at this weight
2. **PMD pico flexx was 8g** but discontinued - successor flexx2 heavier
3. **OAK-D Lite** adds on-device AI but 3× heavier (~61g)
4. **Arducam TOF** is lighter but much lower resolution (240×180 vs 1280×800)

**Best Alternatives by Use Case:**

| Use Case | Best Option | Weight | Why |
|----------|-------------|--------|-----|
| **Lightest depth** | Intel D430 + D4 | ~19g | Best resolution/weight ratio |
| **On-device AI + depth** | OAK-FFC 4P (bare) | ~45g | 4 TOPS neural inference built-in |
| **Ultra-light TOF** | Arducam TOF | ~15g | If 240×180 is sufficient |
| **Zone-based depth** | Terabee Evo 3D | ~12g | 64-zone depth map, very light |

**2026 Watch List:**
- **Luxonis OAK-D Lite v2** - rumored lighter version
- **Intel D421** - all-in-one may get lighter variants
- **Arducam stereo modules** - new global shutter stereo options

**Source:** [Luxonis OAK Comparison](https://docs.luxonis.com/hardware/platform/comparison/vs-realsense/)

---

### Camera Recommendation Summary

| Use Case | Recommended Camera | Weight | Resolution |
|----------|-------------------|--------|------------|
| General CV/SLAM | ArduCam OV9281 (global shutter) | ~4g | 1MP (1280×800) |
| Object Detection | Pi Camera 3 or OV5640 | ~14g | 12MP / 5MP |
| AprilTag/Markers | ArduCam OV9281 | ~4g | 1MP |
| Low-light | Pi Camera 3 NoIR | ~14g | 12MP |
| **3D Depth/SLAM** | **Intel D430 + D4 board** | **~20g** | **1MP depth (1280×800)** |
| Obstacle Avoidance | Intel D430 + D4 board | ~20g | 1MP depth |

---

## 4. Companion Computer Options

### 4.1 Raspberry Pi Zero 2W (Best Balance)

| Specification | Value |
|---------------|-------|
| Weight | **10g** |
| Dimensions | 65×30mm |
| CPU | Quad-core Cortex-A53 @ 1GHz |
| RAM | 512MB LPDDR2 |
| Wireless | WiFi 802.11 b/g/n, BT 4.2/BLE |
| Camera | MIPI CSI-2 connector |
| GPIO | 40-pin HAT-compatible |
| Power | ~1.5-2.5W typical |

**Pros:**
- Lightest option with full Linux support
- Native PX4/ArduPilot MAVROS integration
- Large software ecosystem
- CSI camera interface
- WiFi for telemetry/video streaming

**Cons:**
- Limited to 512MB RAM
- No onboard AI acceleration
- Requires external AI accelerator for neural networks

**Best For:** Basic CV, telemetry relay, simple autonomous missions

**Source:** [Raspberry Pi](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)

---

### 4.1a Raspberry Pi CM5 + Carrier (MicoAir Reference Setup)

| Specification | Value |
|---------------|-------|
| CM5 Module Weight | **~12-14g** (same form factor as CM4) |
| Carrier Board Weight | **15-40g** (varies by carrier) |
| CPU | Quad-core Cortex-A76 @ 2.4GHz |
| RAM | 2GB/4GB/8GB LPDDR4X |
| Storage | 0GB (Lite) / 16GB / 32GB / 64GB eMMC |
| Wireless | WiFi 5, BT 5.0 (wireless variants) |
| PCIe | PCIe 2.0 x1 (for NVMe/AI accelerator) |
| Camera | 2× 4-lane MIPI CSI-2 |
| USB | USB 3.0 |

**Compact Carrier Options:**

| Carrier | Weight | Features |
|---------|--------|----------|
| CM5 MINIMA (Seeed) | ~25g (est.) | M.2 for Hailo/SSD, CSI, Ethernet |
| Custom minimal | ~15g (est.) | USB, power, CSI only |
| Piunora | ~20g (est.) | M.2 B-Key, USB-C |

**Total System Weight (CM5 + Minimal Carrier): ~27-40g**

**Why CM5 for Autonomous Drones:**
- **Full Pi 5 performance** in compact module
- PCIe for M.2 AI accelerators (Hailo-8L, Coral)
- Dual CSI camera ports for stereo/depth
- ROS2 + RealSense SDK support
- PX4 MAVROS companion computer ready
- USB 3.0 for Intel RealSense D430

**Compared to Pi Zero 2W:**
- 5× faster CPU (A76 vs A53)
- Up to 16× more RAM (8GB vs 512MB)
- PCIe for AI accelerators
- But 3-4× heavier with carrier

**Best For:** RealSense depth cameras, ROS2/SLAM, AI inference with Hailo/Coral, advanced autonomy

**MicoAir Reference Configuration:**
- CM5 (4GB) + minimal carrier: ~30g
- Intel RealSense D430 + D4 board: ~20g
- **Total CV system: ~50g**

**Source:** [Raspberry Pi CM5](https://www.raspberrypi.com/products/compute-module-5/)

---

### 4.2 Radxa Zero 3W (Best Performance/Weight)

| Specification | Value |
|---------------|-------|
| Weight | **~10-12g** (estimated, same form factor as Pi Zero) |
| Dimensions | 65×30mm |
| CPU | Quad-core Cortex-A55 @ 1.6GHz |
| RAM | 1GB/2GB/4GB/8GB LPDDR4 |
| NPU | **0.8 TOPS** (built-in) |
| Wireless | WiFi 6, BT 5.4 |
| Video | 4K60 decode, 1080p100 encode |
| Storage | eMMC option + microSD |

**Pros:**
- **Built-in 0.8 TOPS NPU** for basic AI inference
- More RAM options (up to 8GB)
- Faster CPU than Pi Zero 2W
- WiFi 6 for better connectivity
- Same Pi Zero form factor

**Cons:**
- Smaller software ecosystem than Raspberry Pi
- May need more power tuning
- NPU software support still maturing

**Best For:** On-device inference, object detection, autonomous navigation

**Source:** [Radxa](https://radxa.com/products/zeros/zero3w/)

---

### 4.3 Seeed XIAO ESP32S3 Sense (Ultra-Lightweight)

| Specification | Value |
|---------------|-------|
| Weight | **~5-7g** (estimated with camera board) |
| Dimensions | Thumb-sized (~21×17mm main board) |
| CPU | Dual-core Xtensa LX7 @ 240MHz |
| RAM | 8MB PSRAM |
| Flash | 8MB |
| Camera | OV2640/OV3660 (1600×1200) |
| Wireless | WiFi, BLE 5.0 |
| Features | Built-in microphone, SD card slot |

**Pros:**
- **Smallest/lightest option**
- Integrated camera module
- TinyML support via Edge Impulse
- Battery charging built-in
- Ultra-low sleep power (14μA)

**Cons:**
- No Linux (Arduino/MicroPython only)
- Limited processing power
- Not suitable for complex CV pipelines

**Best For:** Simple object detection, streaming camera, weight-critical builds

**Source:** [Seeed Studio](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html)

---

### 4.4 LuckFox Pico Mini (Best NPU/Weight Ratio)

| Specification | Value |
|---------------|-------|
| Weight | **~5g** (estimated) |
| Dimensions | Ultra-compact |
| CPU | Cortex-A7 @ 1.2GHz + RISC-V MCU |
| NPU | **0.5 TOPS** (int8), 1.0 TOPS (int4) |
| RAM | 64MB DDR2 |
| ISP | Built-in, 4MP@30fps input |
| Camera | MIPI CSI 2-lane |
| Features | Fast boot (250ms to capture) |

**Pros:**
- **Excellent NPU for the weight**
- Built-in ISP for camera processing
- Linux support (Buildroot)
- RISC-V MCU for low-power tasks
- Castellated holes for integration

**Cons:**
- Only 64MB RAM
- Limited I/O
- Smaller ecosystem/community
- No WiFi (needs external module)

**Best For:** Dedicated vision processing, face detection, lightweight AI inference

**Source:** [LuckFox](https://www.luckfox.com/Luckfox-Pico-Mini-A)

---

### 4.5 OpenMV H7 Plus (All-in-One Vision)

| Specification | Value |
|---------------|-------|
| Weight | **17g** (complete with camera) |
| CPU | STM32H743 Cortex-M7 @ 480MHz |
| RAM | 32MB SDRAM |
| Flash | 32MB external + 2MB internal |
| Camera | OV5640 5MP (swappable) |
| Features | MicroPython, TensorFlow Lite |

**Pros:**
- **Complete vision system** (camera + processor)
- Purpose-built for machine vision
- Easy MicroPython programming
- Swappable camera modules (global shutter available)
- Built-in CV algorithms (face detection, AprilTag, QR codes)
- Direct PWM/servo output for control

**Cons:**
- No Linux
- Limited general-purpose computing
- No wireless (needs shield)
- Higher cost

**Best For:** Marker tracking, face/object following, landing pad detection

**Source:** [OpenMV](https://openmv.io/products/openmv-cam-h7-plus)

---

### Companion Computer Comparison

| Board | Weight | CPU | RAM | NPU | Wireless | Best For |
|-------|--------|-----|-----|-----|----------|----------|
| **Pi Zero 2W** | 10g | A53×4 @1GHz | 512MB | None | WiFi/BT | General autonomy |
| **Radxa Zero 3W** | ~11g | A55×4 @1.6GHz | 1-8GB | 0.8 TOPS | WiFi 6/BT 5.4 | On-device AI |
| **XIAO ESP32S3** | ~6g | LX7×2 @240MHz | 8MB | None | WiFi/BLE | Ultra-light streaming |
| **LuckFox Pico Mini** | ~5g | A7 @1.2GHz | 64MB | 0.5 TOPS | None | Dedicated vision |
| **OpenMV H7+** | 17g | M7 @480MHz | 32MB | None | Optional | Complete vision system |

---

## 5. Edge AI Accelerator Options

### 5.1 Google Coral USB Accelerator

| Specification | Value |
|---------------|-------|
| Weight | **~25g** (estimated with cable) |
| Performance | **4 TOPS** |
| Power | 2 TOPS/W (0.5W per TOPS) |
| Interface | USB 3.0 |
| Compatibility | Linux, Windows, Raspberry Pi |

**Pros:** High performance, well-supported, TensorFlow Lite compatible
**Cons:** Heavy for this build, USB overhead, power hungry under load

**Source:** [Google Coral](https://www.coral.ai/products/)

---

### 5.2 Hailo-8L M.2 Module

| Specification | Value |
|---------------|-------|
| Weight | **~5g** (estimated, M.2 2230/2242) |
| Performance | **13 TOPS** |
| Efficiency | 8 TOPS/W |
| Interface | M.2 Key A+E (2230) or B+M (2242) |
| Form Factor | 22×30mm or 22×42mm |

**Pros:** Excellent performance/weight ratio, low power, compact
**Cons:** Requires M.2 slot (Pi 5 only, not Zero 2W), cost

**Note:** Not compatible with Pi Zero 2W. Would need Pi 5 or custom carrier.

**Source:** [Hailo](https://hailo.ai/products/ai-accelerators/hailo-8l-m-2-ai-acceleration-module-for-ai-light-applications/)

---

### 5.3 Built-in NPU Options

| Board | NPU Performance | Notes |
|-------|-----------------|-------|
| Radxa Zero 3W | 0.8 TOPS | Built-in, no extra weight |
| LuckFox Pico Mini | 0.5-1.0 TOPS | Built-in, int4/int8/int16 |

**Best lightweight option:** Use a board with integrated NPU to avoid additional weight.

---

## 5A. Hailo Alternatives & Equivalents (Edge AI Accelerators)

This section compares dedicated edge AI accelerators suitable for lightweight drone builds, focusing on alternatives to the Hailo-8L.

### Comparison Overview

| Accelerator | Performance | Power | Weight (est.) | Interface | Form Factor | Price (est.) |
|-------------|-------------|-------|---------------|-----------|-------------|--------------|
| **Hailo-8L** | 13 TOPS | ~1.5W | ~5g | M.2 | 22×30mm | £65 |
| **Google Coral USB** | 4 TOPS | ~2W | ~18g | USB 3.0 | 65×30mm | £50 |
| **Coral M.2 Dual TPU** | 8 TOPS | ~4W | ~5g | M.2 A+E | 22×30mm | £35 |
| **Kneron KL720** | 1.5 TOPS | ~1.2W | ~3g | USB/MIPI | Module | £40 |
| **MemryX MX3** | 5 TFLOPS | 0.5-2W | ~8g | M.2/PCIe | 22×80mm | £80 |
| **Axera AX630C** | 3.2 TOPS | ~1.5W | ~10g | SoC | Module | £35 |
| **Axera AX8850** | 24 TOPS | ~3W | ~8g | M.2 | 22×42mm | £60 |

---

### 5A.1 Google Coral TPU (USB & M.2)

#### USB Accelerator

| Specification | Value |
|---------------|-------|
| Weight | **~18g** (with short cable) |
| Performance | **4 TOPS** (INT8) |
| Power | 2W typical, 2.5W peak |
| Interface | USB 3.0 (USB 2.0 compatible) |
| Dimensions | 65×30×8mm |
| Frameworks | TensorFlow Lite |

**Pros:**
- Plug-and-play, no carrier board needed
- Mature software ecosystem
- Wide model support (MobileNet, EfficientDet, etc.)
- Works with Pi Zero 2W via USB

**Cons:**
- Heavier than M.2 alternatives
- USB overhead reduces effective throughput
- 4 TOPS is dated compared to newer options
- Getting harder to source (discontinued rumors)

#### M.2 Dual Edge TPU

| Specification | Value |
|---------------|-------|
| Weight | **~5g** (module only) |
| Performance | **8 TOPS** (4 TOPS × 2) |
| Power | 4W (both TPUs active) |
| Interface | M.2 A+E Key |
| Dimensions | 22×30mm (2230) |

**Pros:**
- Compact and lightweight
- Double the performance of USB version
- Lower cost ($40 USD)

**Cons:**
- Requires M.2 carrier board (adds weight)
- Not compatible with Pi Zero 2W
- Higher power than single TPU

**Best For:** Prototyping, proven ecosystem, if weight isn't critical

**Source:** [Google Coral](https://www.coral.ai/products/)

---

### 5A.2 Kneron KL720 (Best Power Efficiency)

| Specification | Value |
|---------------|-------|
| Weight | **~3-5g** (bare module) |
| Performance | **1.5 TOPS** @ 1.2W |
| Efficiency | **1.25 TOPS/W** |
| Interface | USB 3.0, USB 2.0, MIPI CSI |
| Memory | 128MB LPDDR3 |
| Video | 4K image, 1080p video |
| CPU | ARM Cortex-M4 |

**Key Features:**
- 2-4× more power-efficient than competitors
- Built-in MIPI CSI camera interface
- Supports full natural language processing
- On-chip image signal processor (ISP)
- Runs popular CNN models (TinyYOLO, MobileNet, ResNet)

**Available Modules:**
- **AAEON M2AI-2280-720:** M.2 2280 form factor
- **AAEON MINI-AI-720:** Ultra-compact standalone module

**Pros:**
- Excellent power efficiency for battery-powered drones
- Direct camera connection (no separate ISP needed)
- Compact form factor options
- Lower cost than Hailo

**Cons:**
- Lower raw performance (1.5 TOPS vs 13 TOPS)
- Smaller software ecosystem
- Less community support

**Best For:** Power-constrained builds, direct camera integration, long flight times

**Source:** [Kneron KL720](https://www.kneron.com/KL720)

---

### 5A.3 MemryX MX3 (Best Developer Experience)

| Specification | Value |
|---------------|-------|
| Weight | **~8g** (M.2 module) |
| Performance | **5 TFLOPS** (BFloat16) |
| Power | 0.5-2W (model dependent) |
| Interface | M.2 M-Key, PCIe Gen 3 x2/x4 |
| Form Factor | 22×80mm (2280) |
| On-chip Memory | ~40MB (across 4 cores) |
| Temperature | -40°C to +85°C industrial |

**Key Features:**
- 10-100× smaller than competing GPU cores
- Fanless operation possible
- Supports TensorFlow, PyTorch, ONNX, Keras, LiteRT
- Widest operator support among NPUs
- Real-time video obstacle detection
- Edge Impulse integration

**Pros:**
- **Most developer-friendly NPU** - easiest to adopt
- Excellent framework compatibility
- Low power consumption
- Industrial temperature range
- Good for autonomous navigation

**Cons:**
- Requires M.2 slot (needs carrier board)
- On-chip memory limits large transformer models
- 2280 form factor is longer than 2230/2242

**Best For:** Rapid prototyping, CV model deployment, developers new to NPUs

**Source:** [MemryX](https://memryx.com/products/)

---

### 5A.4 Axera AX630C (Best Value SoC)

| Specification | Value |
|---------------|-------|
| Weight | **~10g** (with carrier, varies) |
| NPU Performance | **3.2 TOPS** (INT8), 12.8 TOPS (INT4) |
| Power | **~1.5W** operating |
| Memory | 4GB LPDDR4 (1GB user, 3GB HW accel) |
| Storage | 32GB eMMC |
| Camera | Dual MIPI CSI, 4K AI-ISP |
| Display | MIPI DSI |

**Key Features:**
- **Night vision AI-ISP** built-in
- Dual camera support with stitching
- Comparable to Jetson Orin Nano at fraction of price/power
- Pre-installed LLM support (Qwen2.5-0.5B)
- YOLO11, MobileNet, ResNet support
- Speech: KWS, ASR, TTS built-in

**Available Products:**
- **M5Stack LLM630:** Complete kit with AX630C
- Various SoM modules from Chinese vendors

**Pros:**
- Excellent price/performance ratio
- Built-in night vision ISP
- Complete SoC (no separate camera processor needed)
- Low power consumption
- LLM capability is a bonus

**Cons:**
- Smaller Western ecosystem/documentation
- Most products from Chinese vendors
- May need translation for some documentation

**Best For:** Night vision drones, budget builds, dual-camera setups

**Source:** [Axera AX630C](https://en.axera-tech.com/Product/126.html)

---

### 5A.5 Axera AX8850 (Highest Performance)

| Specification | Value |
|---------------|-------|
| Weight | **~8g** (M.2 module) |
| Performance | **24 TOPS** (INT8) |
| Power | ~3W |
| Interface | M.2 M-Key (2242) |
| Form Factor | 22×42mm |

**Key Features:**
- Highest TOPS in compact M.2 form factor
- Nearly 2× Hailo-8L performance
- Available from Radxa (AICore AX-M1) and M5Stack

**Available Products:**
- **Radxa AICore AX-M1:** M.2 2242 module
- **M5Stack LLM-8850:** M.2 AI accelerator card

**Pros:**
- Best raw performance for the weight
- Compact 2242 form factor
- Multiple vendor options

**Cons:**
- Higher power consumption than Hailo-8L
- Requires M.2 carrier board
- Newer, less mature ecosystem

**Best For:** Complex multi-model inference, high-FPS object detection

**Source:** [Radxa AICore AX-M1](https://radxa.com/products/)

---

### 5A.6 Rockchip RK3588 NPU (Integrated Option)

| Specification | Value |
|---------------|-------|
| NPU Performance | **6 TOPS** |
| CPU | 4× A76 + 4× A55 |
| GPU | Mali G610 |
| Power | 5-15W (full SoC) |

**Available Compact Modules:**
- **Turing RK1:** SODIMM form factor, Jetson Nano compatible
- **ArmSoM AIM7:** 260-pin, Jetson Nano carrier compatible
- **Various SoMs:** From Firefly, Forlinx, Radxa

**Pros:**
- Integrated NPU + powerful CPU + GPU
- 6 TOPS is competitive
- Jetson-compatible options available
- Strong Linux support

**Cons:**
- Full SoC is power-hungry for this drone build
- Modules are heavier (15-25g typical)
- Overkill for simple CV tasks

**Best For:** If you need general compute + AI, not weight-optimized

**Source:** [Rockchip RK3588](https://www.rock-chips.com/uploads/pdf/2022.8.26/192/RK3588%20Brief%20Datasheet.pdf)

---

### 5A.7 Hailo Alternatives Summary

#### For Sub-250g Drone (Weight Priority)

| Priority | Recommendation | Why |
|----------|----------------|-----|
| **Best Overall** | **Kneron KL720** | Lightest (~3g), lowest power (1.2W), direct MIPI camera |
| **Best Performance** | **Axera AX630C SoC** | 3.2 TOPS, night vision ISP, complete solution |
| **Best Ecosystem** | **Google Coral USB** | Mature software, works with Pi Zero 2W |
| **Best Dev Experience** | **MemryX MX3** | Easiest framework support, good docs |
| **Highest TOPS** | **Axera AX8850** | 24 TOPS in M.2 2242, if you have carrier |

#### Weight-Optimized Recommendations

For your ~92g CV/AI budget:

1. **Lightest AI Option (~18g total):**
   - Kneron KL720 module (~4g) + MIPI camera (~4g) + Pi Zero 2W (10g)
   - 1.5 TOPS, excellent power efficiency

2. **Best Performance/Weight (~25g total):**
   - LuckFox Pico Mini (5g, 0.5 TOPS built-in) + external Kneron KL720 (4g) + camera (4g) + wiring
   - Dual NPU approach: LuckFox for preprocessing, KL720 for inference

3. **Simplest Integration (~20g total):**
   - Axera AX630C module (~10g) + MIPI camera (~4g) + wiring
   - Complete SoC with NPU, ISP, and camera interface

#### Hailo vs Alternatives Decision Matrix

| Factor | Hailo-8L | Coral USB | Kneron KL720 | MemryX MX3 | Axera AX630C |
|--------|----------|-----------|--------------|------------|--------------|
| Raw TOPS | 13 | 4 | 1.5 | 5 | 3.2 |
| Weight | ~5g | ~18g | ~4g | ~8g | ~10g |
| Power | 1.5W | 2W | 1.2W | 0.5-2W | 1.5W |
| Pi Zero 2W Compatible | ❌ | ✅ | ✅ | ❌ | ❌ |
| Camera Interface | None | None | MIPI CSI | None | Dual MIPI |
| Software Maturity | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Availability | Good | Declining | Good | Good | Good |
| Price | £65 | £50 | £40 | £80 | £35 |

---

## 6. Proposed CV/AI Combinations

### Option A: Lightweight Autonomous (Recommended)

**Total CV/AI Weight: ~25g**

| Component | Model | Weight | Purpose |
|-----------|-------|--------|---------|
| Companion Computer | Raspberry Pi Zero 2W | 10g | MAVLink, mission control |
| Camera | ArduCam OV9281 (CSI) | 4g | Global shutter CV |
| AI Processing | CPU-based (TFLite) | 0g | Basic inference |
| Extras | GPS (BN-180), wiring | ~10g | Navigation |

**Total Drone Weight: ~178g**

**Capabilities:**
- Optical flow / visual odometry
- AprilTag landing pad detection
- Basic object tracking
- Waypoint missions via PX4
- WiFi telemetry and video streaming

**Power Consumption:** ~2-3W

---

### Option B: Enhanced AI Vision

**Total CV/AI Weight: ~35g**

| Component | Model | Weight | Purpose |
|-----------|-------|--------|---------|
| Companion Computer | Radxa Zero 3W (2GB) | 11g | Linux + NPU inference |
| Camera | Pi Camera 3 (Wide) | 14g | High-res color vision |
| GPS | BN-180 or similar | 5g | Positioning |
| Extras | Wiring, mounts | 5g | Integration |

**Total Drone Weight: ~188g**

**Capabilities:**
- 0.8 TOPS NPU for real-time inference
- Object detection (YOLO-tiny, MobileNet)
- Person/vehicle tracking
- Advanced autonomous behaviors
- WiFi 6 for high-bandwidth video

**Power Consumption:** ~3-4W

---

### Option C: Dedicated Vision Processor

**Total CV/AI Weight: ~30g**

| Component | Model | Weight | Purpose |
|-----------|-------|--------|---------|
| Vision System | OpenMV H7 Plus | 17g | All-in-one CV |
| Companion (optional) | XIAO ESP32S3 | 6g | WiFi bridge, logging |
| GPS | Micro GPS module | 5g | Positioning |
| Extras | Wiring | 2g | Integration |

**Total Drone Weight: ~183g**

**Capabilities:**
- Fast marker/AprilTag tracking
- Face detection and following
- Color blob tracking
- Landing pad detection
- MicroPython scripting

**Power Consumption:** ~1.5-2.5W

---

### Option D: Ultra-Lightweight (Maximum Flight Time)

**Total CV/AI Weight: ~15g**

| Component | Model | Weight | Purpose |
|-----------|-------|--------|---------|
| Vision System | LuckFox Pico Mini | 5g | NPU + camera ISP |
| Camera | MIPI CSI camera | 4g | Vision input |
| WiFi Module | ESP-01S or similar | 3g | Telemetry |
| Extras | Wiring | 3g | Integration |

**Total Drone Weight: ~168g**

**Capabilities:**
- 0.5 TOPS NPU inference
- Basic object detection
- Fast boot for quick missions
- Lowest power consumption
- Maximum flight time

**Power Consumption:** ~1-2W

---

### Option E: RealSense Depth + CM5 (MicoAir Reference - Advanced SLAM)

**Total CV/AI Weight: ~55g**

| Component | Model | Weight | Purpose |
|-----------|-------|--------|---------|
| Companion Computer | Raspberry Pi CM5 (4GB) | 12g | ROS2, SLAM processing |
| Carrier Board | Minimal custom/CM5 MINIMA | 20g | USB3, power |
| Depth Camera | Intel RealSense D430 | 13g | 3D depth sensing |
| Vision Processor | D4 Board | 6g | Depth USB output |
| Extras | Wiring, mounts | 4g | Integration |

**Total Drone Weight: ~212g** (with MTF-01 base)

**Capabilities:**
- True 3D depth perception (0.2-10m range)
- Full SLAM (ROS2 + RTAB-Map)
- Obstacle avoidance with depth
- Indoor autonomous navigation
- Global shutter stereo vision
- PX4 offboard control via MAVROS

**Power Consumption:** ~4-6W

**Notes:**
- This is the MicoAir reference setup for advanced autonomous flight
- D430 is indoor-optimized (IR struggles in sunlight)
- Requires USB 3.0 bandwidth for depth streaming
- Can add Hailo-8L via M.2 for object detection (+5g, +13 TOPS)

**Source:** [MicoAir YouTube Tutorials](https://www.youtube.com/@MicoAirTech)

---

## 7. Weight Summary by Configuration

| Configuration | Base | CV/AI | Total | Under 250g |
|--------------|------|-------|-------|------------|
| **Option A** (Pi Zero 2W + OV9281) | 157.5g | 25g | **182.5g** | ✅ 67g margin |
| **Option B** (Radxa Zero 3W + Pi Cam 3) | 157.5g | 35g | **192.5g** | ✅ 57g margin |
| **Option C** (OpenMV H7+ + XIAO) | 157.5g | 30g | **187.5g** | ✅ 62g margin |
| **Option D** (LuckFox Ultra-light) | 157.5g | 15g | **172.5g** | ✅ 77g margin |
| **Option E** (CM5 + RealSense D430) | 157.5g | 55g | **212.5g** | ✅ 37g margin |

All options provide comfortable margin for:
- Additional sensors (optical flow, rangefinder)
- Larger battery upgrade
- Protective bumpers
- Antenna/receiver

---

## 8. UK Regulatory Considerations

### Sub-250g Benefits (2025)

- **Registration:** Operator ID required (camera equipped) - £9/year
- **Flight Privileges:** Can fly closer to people (<50m allowed)
- **Overflight:** Can fly over people (not crowds)
- **Residential Areas:** No 150m distance restriction
- **Night Flying:** Permitted with appropriate lighting
- **Altitude Limit:** 400ft (120m) - applies to all drones

### Autonomous/BVLOS Operations

For fully autonomous operations beyond visual line of sight (BVLOS):
- Likely requires CAA Operational Authorisation
- May need additional safety features (geo-fencing, return-to-home)
- Remote ID becoming mandatory from 2026

### Recommendation

Stay under 250g and maintain visual line of sight for hobby operations. For commercial autonomous work, consult CAA for specific authorisations.

**Sources:**
- [UK CAA Drone Code](https://register-drones.caa.co.uk/drone-code/where-you-can-fly)
- [HireDronePilot UK Laws Guide](https://hiredronepilot.uk/blog/sub-250g-drone-laws-uk)

---

## 9. Recommended Build

For a **balanced autonomous drone** prioritizing reliability and capability:

### Primary Recommendation: Option A+

| Component | Choice | Weight | Cost (Est.) |
|-----------|--------|--------|-------------|
| Frame | Happymodel Crux35 | 26g | £15 |
| Motors | T-Motor F1404 3800KV ×4 | 37g | £60 |
| Props | HQProp T3.5×2.5×3 ×4 | 6g | £5 |
| Flight Controller | MicoAir743-AIO-35A | 11g | £45 |
| Battery | GNB 4S 850mAh 60C | 73g | £20 |
| Companion Computer | Raspberry Pi Zero 2W | 10g | £15 |
| Camera | ArduCam OV9281 Global Shutter | 4g | £25 |
| GPS | BN-180 or Beitian equivalent | 5g | £15 |
| Receiver | ELRS (if not using WiFi) | 2g | £15 |
| Wiring/Misc | Cables, mounts, spacers | 5g | £10 |
| **TOTAL** | | **179g** | **~£225** |

### Why This Configuration

1. **PX4 Support:** MicoAir743 with PX4 enables proper autonomous modes
2. **MAVLink Integration:** Pi Zero 2W runs MAVROS for offboard control
3. **Global Shutter:** OV9281 eliminates motion blur for CV algorithms
4. **Weight Margin:** 71g remaining for upgrades/additions
5. **Proven Ecosystem:** Raspberry Pi has extensive documentation
6. **Low Power:** Efficient components maximize flight time

### Upgrade Path

- **More AI:** Swap Pi Zero 2W → Radxa Zero 3W (+1g, gain 0.8 TOPS NPU)
- **Better Camera:** Add Pi Camera 3 for color detection (+10g)
- **More Endurance:** Upgrade to 1000mAh battery (+15g)
- **Optical Flow:** Add PMW3901 sensor for indoor positioning (+2g)

---

## 10. References

### Frame & Motors
- [Happymodel Crux35](https://www.happymodel.cn/index.php/2021/07/20/crux35-crux35-hd-3-5inch-fpv-racer-drone-frame-kit/)
- [T-Motor F1404](https://pyrodrone.com/products/t-motor-f1404-micro-long-range-motors-3800kv)
- [HQProp T3.5×2.5×3](https://www.hqprop.com/hqprop-t35x25x3-2cw2ccw-poly-carbonate-p0354.html)

### Flight Controller, Sensors & Battery
- [MicoAir743-AIO-35A](https://micoair.com/flightcontroller_micoair743_aio_35a/)
- [MicoAir MTF-01 Optical Flow & Lidar](https://micoair.com/optical_range_sensor_mtf-01/)
- [MicoAir MTF-01P (12m range)](https://micoair.com/optical_range_sensor_mtf-01p/)
- [MicoAir YouTube - MTF-01 ArduPilot/PX4 Setup](https://youtube.com/watch?v=D-ooFHEtQoo)
- [MicoAir YouTube - MTF-01 INAV Setup](https://youtube.com/watch?v=bEKm-PGRnks)
- [GNB 4S 850mAh](https://pyrodrone.com/products/gaoneng-gnb-850mah-4s-15-2v-60c-120c-xt30)
- [Oscar Liang - Optical Flow Setup Guide](https://oscarliang.com/setup-optical-flow-rangefinder-inav/)

### Companion Computers
- [Raspberry Pi Zero 2W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
- [Raspberry Pi CM5](https://www.raspberrypi.com/products/compute-module-5/)
- [Raspberry Pi CM5 Datasheet](https://pip.raspberrypi.com/documents/RP-008180-DS-cm5-datasheet.pdf)
- [CM5 MINIMA Carrier Board](https://www.seeedstudio.com/CM5-MINIMA-p-6485.html)
- [Radxa Zero 3W](https://radxa.com/products/zeros/zero3w/)
- [Seeed XIAO ESP32S3 Sense](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html)
- [LuckFox Pico Mini](https://www.luckfox.com/Luckfox-Pico-Mini-A)
- [OpenMV H7 Plus](https://openmv.io/products/openmv-cam-h7-plus)

### Cameras
- [Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/)
- [ArduCam OV9281](https://www.arducam.com/product/mini-ov9281-mono-global-shutter-for-pi/)
- [Intel RealSense D430 Depth Module](https://www.intel.com/content/www/us/en/products/sku/98320/intel-realsense-depth-module-d430/specifications.html)
- [Intel RealSense D400 Series Datasheet](https://cdrdv2-public.intel.com/841984/Intel-RealSense-D400-Series-Datasheet.pdf)
- [Intel RealSense Vision Processor D4](https://www.intel.com/content/www/us/en/products/sku/126367/intel-realsense-vision-processor-d4/specifications.html)

### AI Accelerators
- [Google Coral](https://www.coral.ai/products/)
- [Hailo-8L](https://hailo.ai/products/ai-accelerators/hailo-8l-m-2-ai-acceleration-module-for-ai-light-applications/)
- [Kneron KL720](https://www.kneron.com/KL720)
- [MemryX MX3](https://memryx.com/products/)
- [Axera AX630C](https://en.axera-tech.com/Product/126.html)
- [Radxa AICore AX-M1 (AX8850)](https://radxa.com/products/)
- [M5Stack LLM-8850](https://shop.m5stack.com/products/ai-8850-llm-accleration-m-2-module-ax8850)
- [Rockchip RK3588 Datasheet](https://www.rock-chips.com/uploads/pdf/2022.8.26/192/RK3588%20Brief%20Datasheet.pdf)
- [Seeed Hailo vs Coral Comparison](https://www.seeedstudio.com/blog/2024/07/16/raspberry-pi-ai-kit-vs-coral-usb-accelerator-vs-coral-m-2-accelerator-with-dual-edge-tpu/)

### Regulations
- [UK CAA Drone Code](https://register-drones.caa.co.uk/drone-code/where-you-can-fly)
- [UK Sub-250g Laws 2025](https://hiredronepilot.uk/blog/sub-250g-drone-laws-uk)

---

*Document generated: January 2025*
*Target: Sub-250g UK Autonomous Drone Build*
