# DIY 3DGS Scanner - Component Shopping List

Organized by build tier with purchase links and alternatives.

---

## Tier 1: Budget Build (~$600-800)

### Core Components

| Component | Model | Price | Link |
|-----------|-------|-------|------|
| **Processing** | Raspberry Pi 5 8GB | $80 | [raspberrypi.com](https://www.raspberrypi.com/products/raspberry-pi-5/) |
| **Depth Camera** | Intel RealSense D435i | $350 | [intelrealsense.com](https://www.intelrealsense.com/depth-camera-d435i/) |
| **Display** | Waveshare 7" DSI | $55 | [waveshare.com](https://www.waveshare.com/7inch-dsi-lcd.htm) |
| **Cooling** | Pi 5 Active Cooler | $5 | [raspberrypi.com](https://www.raspberrypi.com/products/active-cooler/) |
| **Power** | Anker 737 (140W) | $85 | Amazon |
| **Storage** | Samsung T7 500GB SSD | $55 | Amazon |

### Enclosure & Mounting

| Component | Description | Price |
|-----------|-------------|-------|
| 3D Printed Case | Custom design | $20-40 (filament) |
| 1/4-20 Mounting | Tripod compatibility | $10 |
| Cables | USB-C, HDMI | $20 |

### Budget Build Total: ~$680

---

## Tier 2: Enhanced Build (~$2,000-2,500)

### Core Components

| Component | Model | Price | Link |
|-----------|-------|-------|------|
| **Processing** | NVIDIA Jetson Orin Nano 8GB | $500 | [nvidia.com](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) |
| **Depth Camera** | Intel RealSense D455 | $400 | [intelrealsense.com](https://www.intelrealsense.com/depth-camera-d455/) |
| **LiDAR** | Livox Mid-360 | $1,000 | [livoxtech.com](https://www.livoxtech.com/mid-360) |
| **IMU** | Adafruit BNO085 | $30 | [adafruit.com](https://www.adafruit.com/product/4754) |

### Cameras (Additional Views)

| Component | Model | Price |
|-----------|-------|-------|
| Wide Camera 1 | Arducam 16MP IMX519 | $40 |
| Wide Camera 2 | Arducam 16MP IMX519 | $40 |
| Fisheye Lens | 180° M12 lens | $20 each |

### Power System

| Component | Model | Price |
|-----------|-------|-------|
| LiPo Battery | 6S 5000mAh | $80 |
| BMS/Charger | 6S balance charger | $50 |
| DC-DC Converter | 5V/12V outputs | $25 |

### Structure

| Component | Description | Price |
|-----------|-------------|-------|
| Aluminum Extrusion | 20x20mm frame | $50 |
| 3D Printed Parts | Mounts, brackets | $30 |
| Hardware | Bolts, nuts, standoffs | $25 |

### Enhanced Build Total: ~$2,290

---

## Tier 3: Near-Commercial (~$8,000-12,000)

### Core Components

| Component | Model | Price |
|-----------|-------|-------|
| **Processing** | Jetson AGX Orin 32GB | $2,000 |
| **LiDAR** | Hesai XT32 | $4,000 |
| **Cameras** | 2x FLIR BFS-U3-51S5C | $1,000 |
| **Fisheye Lenses** | 2x Entaniya 220° | $400 |
| **IMU** | Analog Devices ADIS16470 | $500 |

### Power & Connectivity

| Component | Description | Price |
|-----------|-------------|-------|
| Industrial Battery | 24V 20Ah Li-ion | $400 |
| Power Management | Custom board | $200 |
| Connectors | Industrial waterproof | $150 |

### Enclosure

| Component | Description | Price |
|-----------|-------------|-------|
| Custom Machined | Aluminum housing | $500 |
| Thermal Management | Heat pipes, fans | $150 |
| Sealing | IP54 gaskets | $50 |

### Near-Commercial Total: ~$9,350

---

## Alternative Components

### LiDAR Options (By Budget)

| Model | Points/s | Range | Price | Notes |
|-------|----------|-------|-------|-------|
| Slamtec RPLIDAR A1 | 8k | 12m | $99 | 2D only, good for start |
| Slamtec RPLIDAR A2M12 | 12k | 25m | $300 | 2D, better range |
| Livox Mid-40 (used) | 100k | 260m | $400-600 | 3D, eBay |
| Livox Mid-360 | 200k | 40m | $1,000 | 3D, wide FOV |
| Velodyne VLP-16 (used) | 300k | 100m | $1,500-3,000 | 3D, industry standard |
| Hesai Pandar40P (used) | 720k | 200m | $200-400 | eBay deals |

### Depth Camera Alternatives

| Model | Resolution | Range | IMU | Price |
|-------|-----------|-------|-----|-------|
| Intel D415 | 1280x720 | 10m | No | $250 |
| Intel D435 | 1280x720 | 10m | No | $300 |
| Intel D435i | 1280x720 | 10m | Yes | $350 |
| Intel D455 | 1280x720 | 6m | Yes | $400 |
| Azure Kinect | 1024x1024 | 5.5m | Yes | $400 |
| Orbbec Femto Bolt | 1024x1024 | 10m | Yes | $600 |

### Processing Options

| Model | CPU | GPU | RAM | Price | Best For |
|-------|-----|-----|-----|-------|----------|
| Raspberry Pi 5 | A76 | - | 8GB | $80 | Budget, offline |
| Jetson Nano | A57 | 128 CUDA | 4GB | $150 | Light SLAM |
| Jetson Orin Nano | A78 | 1024 CUDA | 8GB | $500 | Real-time SLAM |
| Jetson Orin NX | A78 | 2048 CUDA | 16GB | $900 | Heavy processing |
| Jetson AGX Orin | A78 | 2048 CUDA | 32GB | $2,000 | Full real-time |

---

## Recommended Vendors

### Electronics
- **Adafruit** - Sensors, Pi accessories, reliable
- **SparkFun** - IMUs, breakout boards
- **Seeed Studio** - Jetson carriers, industrial
- **Arrow Electronics** - Professional components

### LiDAR
- **Livox Direct** - Best prices for new units
- **eBay** - Used Hesai, Velodyne deals
- **RobotShop** - Slamtec, hobby LiDAR

### Cameras
- **Intel RealSense Store** - Direct purchase
- **FLIR/Teledyne** - Industrial cameras
- **Arducam** - Budget multi-camera

### Mechanical
- **Misumi** - Aluminum extrusion
- **McMaster-Carr** - Hardware, fasteners
- **SendCutSend** - Custom laser cutting

### 3D Printing Services
- **JLCPCB** - Cheap international shipping
- **PCBWay** - Good quality
- **Shapeways** - Premium materials

---

## Sample Amazon Cart (Tier 1)

```
Raspberry Pi 5 8GB                    $79.99
Intel RealSense D435i                $349.00
Waveshare 7" DSI LCD                  $54.99
Pi 5 Active Cooler                     $5.00
Samsung T7 500GB                      $54.99
Anker 737 Power Bank                  $84.99
USB-C cables (3-pack)                 $12.99
1/4-20 tripod mount                    $8.99
                                    ────────
                             Subtotal: $650.94
                                  Tax: ~$52
                                Total: ~$703
```

---

## Multi-Camera Array Components

For studio setups (price per camera station):

| Component | Model | Price |
|-----------|-------|-------|
| Camera | Canon R100 | $479 |
| Lens | 18-45mm kit | included |
| USB Cable | 5m USB 3.0 | $15 |
| Mount | Ball head + clamp | $25 |
| **Per Station** | | **~$520** |

### Control System (Shared)

| Component | Description | Price |
|-----------|-------------|-------|
| Raspberry Pi 5 | 1 per 4 cameras | $80 |
| USB Hub | 4-port powered | $30 |
| Network Switch | Gigabit 8-port | $30 |
| Xangle License | Camera Server | $200 |

### 20-Camera System Total

```
20x Camera stations    $10,400
5x Pi controllers        $400
5x USB hubs              $150
2x Network switches       $60
Frame structure          $500
Lighting                 $300
Xangle license           $200
                       ──────
                Total: $12,010
```

---

## Software Licenses

| Software | Type | Price |
|----------|------|-------|
| PostShot | Commercial | ~$200/yr |
| COLMAP | Open Source | Free |
| Nerfstudio | Open Source | Free |
| Houdini Indie | Commercial | $269/yr |
| GSOPs | Open Source | Free |
| RTAB-Map | Open Source | Free |
| Xangle Camera Server | Commercial | ~$200 |
| XGRIDS LCC (if using XGRIDS) | Commercial | €2,000/yr or €5,000 perpetual |

---

## Notes

1. **Start Small**: Build Tier 1 first, verify workflow works
2. **Upgrade Path**: D435i → D455 → Add LiDAR → Jetson
3. **Used Market**: Check eBay for LiDAR deals (50-90% off)
4. **Calibration**: Budget time for sensor calibration
5. **Enclosure**: 3D print first, machine later if needed
