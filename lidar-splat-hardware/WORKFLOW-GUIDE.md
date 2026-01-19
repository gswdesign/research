# COLMAP → Houdini → PostShot Workflow Guide

Complete pipeline for DIY 3D Gaussian Splatting capture.

## Overview

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   CAPTURE    │──▶│   COLMAP     │──▶│   POSTSHOT   │──▶│   HOUDINI    │
│              │   │              │   │              │   │              │
│ Images/Video │   │ SfM + Poses  │   │ Train 3DGS   │   │ Edit + Render│
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

## Phase 1: Capture

### Image Requirements for Quality 3DGS

| Parameter | Requirement | Notes |
|-----------|-------------|-------|
| **Image Count** | 50-200 | More = better quality |
| **Resolution** | 2K-8K | Higher helps fine details |
| **Format** | PNG or JPG | PNG preferred for quality |
| **Motion Blur** | Minimal | Use fast shutter speed |
| **Depth of Field** | Deep | f/8+ recommended |
| **Overlap** | 60-80% | Between consecutive images |
| **Coverage** | 360° if possible | All angles of subject |

### Capture Techniques

**Handheld Scanning (Moving Camera):**
```
1. Walk slowly around subject
2. Keep camera steady (use gimbal if possible)
3. Vary height - low, eye-level, high angles
4. Overlap frames significantly
5. Avoid motion blur - use 1/500s+ shutter
```

**Turntable (Rotating Subject):**
```
1. Fixed camera position
2. Rotate subject 5-10° per capture
3. Multiple height passes
4. Consistent lighting
5. Use remote trigger to avoid shake
```

**Multi-Camera Array:**
```
1. Synchronized shutter trigger
2. Known camera positions (calibrated)
3. Single instant capture
4. Export camera intrinsics/extrinsics
5. Use Xangle or similar for sync
```

### Video Capture

If using video instead of stills:
- 4K minimum resolution
- 30+ fps
- Minimal compression (ProRes, h.265)
- Slow, steady camera movement
- Extract frames at 2-5fps typically

**Frame Extraction:**
```bash
# Extract frames at 3fps
ffmpeg -i input.mp4 -vf "fps=3" -q:v 2 frames/frame_%04d.jpg

# Extract keyframes only
ffmpeg -i input.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr frames/keyframe_%04d.png
```

---

## Phase 2: COLMAP Processing

### Installation

```bash
# Ubuntu/Debian
sudo apt install colmap

# macOS (Homebrew)
brew install colmap

# Or build from source for GPU support
git clone https://github.com/colmap/colmap.git
cd colmap
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

### Directory Structure

```
project/
├── images/           # Your input images
│   ├── IMG_0001.jpg
│   ├── IMG_0002.jpg
│   └── ...
├── sparse/           # COLMAP will create this
├── dense/            # Optional dense reconstruction
└── database.db       # COLMAP database
```

### Automatic Reconstruction

```bash
# Full automatic pipeline
colmap automatic_reconstructor \
    --workspace_path /path/to/project \
    --image_path /path/to/project/images \
    --camera_model OPENCV \
    --single_camera 1

# This runs:
# 1. Feature extraction
# 2. Feature matching
# 3. Sparse reconstruction
# 4. (Optionally) Dense reconstruction
```

### Manual Pipeline (More Control)

```bash
# 1. Feature extraction
colmap feature_extractor \
    --database_path database.db \
    --image_path images \
    --ImageReader.camera_model OPENCV \
    --ImageReader.single_camera 1 \
    --SiftExtraction.use_gpu 1

# 2. Feature matching
colmap exhaustive_matcher \
    --database_path database.db \
    --SiftMatching.use_gpu 1

# 3. Sparse reconstruction
mkdir -p sparse
colmap mapper \
    --database_path database.db \
    --image_path images \
    --output_path sparse

# 4. (Optional) Undistort images
colmap image_undistorter \
    --image_path images \
    --input_path sparse/0 \
    --output_path undistorted \
    --output_type COLMAP
```

### COLMAP Output Files

After successful reconstruction:
```
sparse/0/
├── cameras.bin      # Camera intrinsics
├── images.bin       # Camera poses (extrinsics)
├── points3D.bin     # Sparse point cloud
├── cameras.txt      # Text version
├── images.txt       # Text version
└── points3D.txt     # Text version
```

### Verify Results

```bash
# Open COLMAP GUI to visualize
colmap gui
# File → Import model → Select sparse/0
```

---

## Phase 3: PostShot Training

### PostShot Setup

PostShot is commercial software for 3DGS training. Alternative free options:
- **Nerfstudio** (gsplat backend)
- **Original 3DGS** (research implementation)

### Directory Prep for PostShot

PostShot expects COLMAP format:
```
input/
├── images/
│   ├── IMG_0001.jpg
│   └── ...
└── sparse/0/
    ├── cameras.bin
    ├── images.bin
    └── points3D.bin
```

### PostShot CLI Training

```bash
# Basic training
postshot train \
    --input /path/to/colmap/output \
    --output /path/to/output \
    --iterations 30000

# With quality settings
postshot train \
    --input /path/to/input \
    --output /path/to/output \
    --iterations 50000 \
    --sh-degree 3 \
    --densify-grad-threshold 0.0002
```

### Alternative: Nerfstudio (Free)

```bash
# Install
pip install nerfstudio

# Process data
ns-process-data images \
    --data /path/to/images \
    --output-dir /path/to/processed

# Or use existing COLMAP
ns-process-data colmap \
    --data /path/to/colmap/sparse \
    --output-dir /path/to/processed

# Train
ns-train splatfacto \
    --data /path/to/processed \
    --output-dir /path/to/output
```

### Alternative: Original 3DGS

```bash
# Clone repo
git clone https://github.com/graphdeco-inria/gaussian-splatting.git
cd gaussian-splatting

# Train
python train.py \
    -s /path/to/colmap/data \
    -m /path/to/output \
    --iterations 30000
```

### Training Output

After training you'll have:
```
output/
├── point_cloud/
│   └── iteration_30000/
│       └── point_cloud.ply    # Gaussian splat data
├── cameras.json               # Camera definitions
└── cfg_args                   # Training config
```

---

## Phase 4: Houdini Integration (GSOPs)

### GSOPs Installation

```bash
# Clone GSOPs
git clone https://github.com/cgnomads/GSOPs.git

# Add to Houdini packages
# Create file: ~/houdini20.5/packages/GSOPs.json
{
    "env": [
        {"GSOPS": "/path/to/GSOPs"}
    ],
    "path": "$GSOPS"
}
```

### Import 3DGS into Houdini

1. **Open Houdini** (20.5+ recommended)

2. **Create Gaussian Splats SOP**
   - Tab menu → Search "Gaussian"
   - Add "Gaussian Splats Import" node

3. **Load .ply file**
   - Point to your `point_cloud.ply`
   - Node will parse Gaussian attributes

### GSOPs Node Types

| Node | Purpose |
|------|---------|
| `gaussian_splats_import` | Load .ply or .splat files |
| `gaussian_splats_export` | Save to various formats |
| `gaussian_splats_render` | Real-time viewport rendering |
| `gaussian_splats_edit` | Modify splat attributes |
| `gaussian_splats_convert` | Convert between GSOPs/native formats |
| `gaussian_splats_generate_training_data` | Create synthetic training data |

### Basic Workflow in Houdini

```
File SOP (load .ply)
        │
        ▼
Gaussian Splats Import
        │
        ▼
Transform SOP (position/scale)
        │
        ▼
Attribute Wrangle (edit splats)
        │
        ▼
Gaussian Splats Render (preview)
        │
        ▼
Gaussian Splats Export (.splat, .ply)
```

### Editing Gaussian Splats

**VEX for modifying splats:**
```c
// Scale all splats
f@scale *= 0.5;

// Adjust opacity
f@opacity *= chf("opacity_mult");

// Color correction
v@color = pow(v@color, chf("gamma"));

// Remove floaters by size
if(f@scale > chf("max_scale")) {
    removepoint(0, @ptnum);
}
```

### Export for Other Engines

```
GSOPs Export Options:
├── .ply      → Universal, works with most viewers
├── .splat    → Web viewers (SuperSplat, etc.)
├── Unity     → Via custom importer
└── Unreal    → Via Lumen plugin
```

---

## Phase 5: Rendering & Output

### Houdini Rendering Options

1. **Viewport Render** (GSOPs native)
   - Real-time preview
   - Good for iteration
   - Limited compositing

2. **Mantra/Karma** (Bake to geometry)
   - Convert splats to instanced spheres
   - Standard rendering pipeline
   - Full compositing

3. **Export to Engine**
   - Unity with Gaussian Splatting plugin
   - Unreal Engine 5.3+ with Lumen
   - Web viewer (SuperSplat)

### Web Viewer Export

For quick sharing:
```bash
# Convert to .splat format
# Use GSOPs export or:
python convert_ply_to_splat.py input.ply output.splat

# Upload to SuperSplat or self-host
```

### Quality Checklist

- [ ] No obvious floaters
- [ ] Clean edges on objects
- [ ] Accurate colors
- [ ] Appropriate level of detail
- [ ] Reasonable file size
- [ ] Renders correctly in target engine

---

## Troubleshooting

### COLMAP Issues

| Problem | Solution |
|---------|----------|
| Few images registered | Add more images with overlap |
| Sparse reconstruction | Increase feature count, lower threshold |
| Wrong scale | Add known measurements or markers |
| Drift/misalignment | Ensure loop closure images |

### PostShot/3DGS Issues

| Problem | Solution |
|---------|----------|
| Floaters | More training iterations, better images |
| Blurry results | Higher resolution images, more overlap |
| Memory errors | Reduce image resolution or batch size |
| Slow training | Enable CUDA, use faster GPU |

### Houdini/GSOPs Issues

| Problem | Solution |
|---------|----------|
| Import fails | Check .ply format, use ASCII if needed |
| Slow viewport | Reduce splat count, use LOD |
| Wrong orientation | Transform/rotate after import |
| Missing attributes | Check GSOPs version compatibility |

---

## Quick Reference Commands

```bash
# === CAPTURE ===
# Extract video frames
ffmpeg -i video.mp4 -vf "fps=3" frames/%04d.jpg

# === COLMAP ===
# Quick automatic reconstruction
colmap automatic_reconstructor \
    --workspace_path . --image_path images

# === 3DGS TRAINING ===
# Nerfstudio
ns-train splatfacto --data processed/

# Original 3DGS
python train.py -s data/ -m output/

# === CONVERSION ===
# PLY to SPLAT (if needed)
# Use GSOPs or online converters
```

---

## Resources

- [COLMAP Documentation](https://colmap.github.io/)
- [Nerfstudio Docs](https://docs.nerf.studio/)
- [GSOPs GitHub](https://github.com/cgnomads/GSOPs)
- [Original 3DGS](https://github.com/graphdeco-inria/gaussian-splatting)
- [PostShot Documentation](https://docs.postshot.io/)
