# 2026 Splat Pipeline Analysis

## Your Requirements
- Deterministic camera extrinsics/intrinsics
- Correct position and scale every time
- Depth integration where beneficial
- Final output to PlayCanvas splat-transform CLI
- Real-world capture AND synthetic CG renders

---

## Part 1: Structure-from-Motion (Sparse Point Cloud)

### 2026 Tool Landscape

| Tool | Speed | Accuracy | Scalability | Deterministic | Best For |
|------|-------|----------|-------------|---------------|----------|
| **COLMAP** | Slow (hours-days) | Excellent | Poor (>1000 imgs) | ✅ Yes | Gold standard, production |
| **GLOMAP** | Fast (10-100x) | Excellent | Good | ✅ Yes | Large scenes, faster iteration |
| **FastMap** | Fastest (GPU) | Good | Excellent | ⚠️ Less robust | Massive datasets (5000+ imgs) |
| **MASt3R-SfM** | Real-time | Moderate | Poor (<50 imgs) | ❌ No | Quick previews only |
| **VGGSfM** | Fast | Moderate | Poor (OOM >50) | ❌ No | Research |

### Recommendation: GLOMAP for Real-World, Skip SfM for Synthetic

**Real-world capture:**
```bash
# GLOMAP - 10-100x faster than COLMAP, same accuracy
glomap mapper \
    --database_path database.db \
    --image_path ./images \
    --output_path ./sparse
```

**Synthetic CG renders:**
You already HAVE ground truth cameras from your 3D software. Skip SfM entirely.

---

## Part 2: Dense Point Cloud / Depth

### Option A: MVS from COLMAP (Free, No Hardware)

```bash
# After sparse reconstruction
colmap patch_match_stereo \
    --workspace_path ./dense \
    --PatchMatchStereo.geom_consistency true

colmap stereo_fusion \
    --workspace_path ./dense \
    --output_path ./dense/fused.ply
```

### Option B: Stereo Depth (Your Hardware)

Your OV2311 stereo pair gives metric depth at capture time:
```python
# Real depth from stereo matching
depth = (baseline * focal_length) / disparity
```

### Option C: Monocular Depth (Depth Anything V2)

```bash
# Fast, good for regularization
python run.py --encoder vitl --img-path ./images --outdir ./depth
```

### Where Depth is Used

```
COLMAP (SfM) ─────────────► Camera poses (depth NOT used here)
                                    │
                                    ▼
                           3DGS Training ◄──── Depth maps (depth USED here)
                                    │
                                    ▼
                              Final splat
```

**Depth goes into the SPLAT TRAINING step, not COLMAP.**

---

## Part 3: Depth-Supervised 3DGS Tools (2026)

| Tool | Depth Support | Surface Quality | Speed | Production Ready |
|------|---------------|-----------------|-------|------------------|
| **PostShot** | ❌ None | Good | Fast | ✅ Yes |
| **DN-Splatter** | ✅ Native | Excellent | Medium | ✅ Yes |
| **2DGS** | ✅ Native | Best surfaces | Medium | ✅ Yes |
| **Nerfstudio** | ✅ Config | Good | Slow | ✅ Yes |
| **gsplat** | ✅ Custom | Flexible | Fast | ⚠️ Dev tool |

### DN-Splatter (Recommended for Depth)

```bash
# With stereo depth maps
python train.py \
    -s ./scene \
    --depth_path ./depth \
    --depth_weight 0.5 \
    --normal_weight 0.1
```

### 2DGS (Best for Clean Surfaces)

```bash
# 2D Gaussian Splatting - better geometry than 3DGS
git clone https://github.com/hbb1/2d-gaussian-splatting
python train.py -s ./scene --depth_ratio 0.5
```

---

## Part 4: The Dune: Prophecy Workflow (Deep EXR → Splat)

Rodeo FX's workflow for the Imperial Palace:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CG SCENE (Houdini)                           │
│                                                                  │
│  1. Set up 900 cameras (procedural hemisphere/orbital)          │
│  2. Render 3K images with Deep EXR (full depth per pixel)       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              GSOPs generate_training_data HDA                   │
│                                                                  │
│  Inputs:                                                         │
│  - Rendered images (PNG/EXR)                                     │
│  - Camera transforms from Houdini                                │
│                                                                  │
│  Outputs:                                                        │
│  - images/ folder (PNGs)                                         │
│  - sparse/0/cameras.txt (intrinsics)                             │
│  - sparse/0/images.txt (extrinsics)                              │
│  - sparse/0/points3D.txt (optional seed points)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Jawset PostShot                               │
│                                                                  │
│  - Trains ~16M splats in 3 hours on RTX 4090                    │
│  - Day/night variants                                            │
│  - 60-90 FPS real-time preview                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    .ply splat file
```

**Key insight:** They used Deep EXR for the RENDERS (full depth data in CG), but PostShot doesn't USE that depth. The depth was for compositing, not splat training.

---

## Part 5: Your Problem - Corona 3ds Max Can't Do Deep EXR

### The Issue

Deep EXR requires:
- Per-pixel depth samples (not just Z-depth)
- Requires specific renderer support (Mantra, Arnold, RenderMan)
- Corona doesn't support true Deep EXR output

### Solution A: Export to Houdini, Render There

```
3ds Max (modeling) → Alembic/USD → Houdini → Karma render → GSOPs → PostShot
```

### Solution B: Use Corona's Z-Depth + Camera Export

Corona CAN output:
- RGB images
- Z-depth pass (single depth per pixel)
- Camera data (via MaxScript)

```maxscript
-- Export camera data from 3ds Max
fn exportCamerasCOLMAP cam outputPath = (
    local f = createFile (outputPath + "cameras.txt")
    format "# Camera list with one line of data per camera:\n" to:f
    format "# CAMERA_ID, MODEL, WIDTH, HEIGHT, fx, fy, cx, cy\n" to:f
    format "1 PINHOLE % % % % % %\n" \
        renderWidth renderHeight \
        (cam.fov * renderWidth / 2) \  -- approximate focal length
        (cam.fov * renderWidth / 2) \
        (renderWidth / 2.0) \
        (renderHeight / 2.0) to:f
    close f
)
```

### Solution C: Blender Pipeline (Free, Full Control)

```
3ds Max → FBX → Blender → blender-3dgs-export addon → COLMAP format
                   ↓
            Cycles/Eevee render with depth
```

GitHub: [blender-3dgs-export](https://github.com/samuelm2/blender-3dgs-export)

### Solution D: Direct Point Cloud (No Splat Training)

If you have the CG scene, you can export geometry directly:
```
3ds Max → .OBJ → Houdini → Convert to Gaussians (GSOPs mesh_to_splats)
```

---

## Part 6: Optimal 2026 Workflows

### Workflow 1: Real-World Capture (Your Drone)

```
Stereo Camera + RTK
        │
        ├── Left images ──────────────────┐
        ├── Right images → Stereo depth   │
        └── RTK poses (optional prior)    │
                                          ▼
                                      GLOMAP
                                   (or COLMAP)
                                          │
                                          ▼
                              ┌───────────┴───────────┐
                              ▼                       ▼
                         PostShot               DN-Splatter
                        (fast, easy)          (with depth)
                              │                       │
                              └───────────┬───────────┘
                                          ▼
                                   splat-transform
                                          │
                                          ▼
                                     Final .ply
```

### Workflow 2: Synthetic CG (Houdini Native)

```
Houdini Scene
      │
      ▼
GSOPs generate_training_data
      │
      ├── images/ (Karma renders)
      ├── sparse/0/cameras.txt
      ├── sparse/0/images.txt
      └── sparse/0/points3D.txt
      │
      ▼
PostShot or DN-Splatter
      │
      ▼
splat-transform → Final .ply
```

### Workflow 3: Synthetic CG (3ds Max / Corona)

```
3ds Max Scene
      │
      ├── Export cameras (MaxScript → COLMAP txt)
      ├── Render images (Corona)
      └── Render Z-depth (Corona)
      │
      ▼
Manual COLMAP folder structure:
├── images/
│   ├── 0001.png
│   └── ...
├── depth/  (optional, for DN-Splatter)
│   ├── 0001.png (16-bit)
│   └── ...
└── sparse/0/
    ├── cameras.txt
    ├── images.txt
    └── points3D.txt (can be empty)
      │
      ▼
DN-Splatter (with depth) or PostShot (without)
      │
      ▼
splat-transform → Final .ply
```

### Workflow 4: Synthetic CG (Blender Bridge)

```
3ds Max → FBX export
              │
              ▼
Blender + blender-3dgs-export addon
              │
              ├── Renders images
              ├── Exports COLMAP cameras.txt
              ├── Exports COLMAP images.txt
              └── Optionally renders depth
              │
              ▼
DN-Splatter or PostShot
              │
              ▼
splat-transform → Final .ply
```

---

## Part 7: COLMAP Format Reference

For synthetic renders, you need to create these files:

### cameras.txt
```
# Camera list with one line of data per camera:
# CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]
# PINHOLE: fx, fy, cx, cy
1 PINHOLE 1920 1080 1000.0 1000.0 960.0 540.0
```

### images.txt
```
# Image list with two lines of data per image:
# IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
# POINTS2D[] as (X, Y, POINT3D_ID) - can be empty
1 0.707 0.0 0.707 0.0 0.0 0.0 5.0 1 0001.png

2 0.707 0.0 0.707 0.0 1.0 0.0 5.0 1 0002.png

```

### points3D.txt
```
# 3D point list (can be empty for synthetic)
# POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[]
```

### Quaternion Convention
COLMAP uses **world-to-camera** transforms:
```python
# Camera pose: world point → camera point
# p_cam = R @ p_world + t

# Quaternion order: [qw, qx, qy, qz]
# Translation: camera position in world coords = -R.T @ t
```

---

## Part 8: splat-transform Integration

Final step - prepare for web/engine use:

```bash
# Install
npm install -g splat-transform

# Convert and optimize
splat-transform input.ply \
    --format sog \
    --output optimized.sog

# With transformations
splat-transform input.ply \
    -s 0.01 \           # Scale to meters
    -r 0,90,0 \         # Rotate 90° around Y
    -t 0,0,0 \          # Translate
    output.ply

# Merge multiple splats
splat-transform scene1.ply scene2.ply merged.ply

# Generate LOD for streaming
splat-transform large_scene.ply --lod streaming_scene/
```

### Supported Formats

| Format | Read | Write | Notes |
|--------|------|-------|-------|
| PLY | ✅ | ✅ | Standard 3DGS |
| Compressed PLY | ✅ | ✅ | Smaller files |
| SOG | ✅ | ✅ | PlayCanvas optimized |
| SPLAT | ✅ | ❌ | Antimatter15 format |
| KSPLAT | ✅ | ❌ | Kevin Kwok format |
| SPZ | ✅ | ❌ | Niantic format |
| CSV | ❌ | ✅ | For analysis |

---

## Part 9: Recommended Tool Choices

### For Deterministic Extrinsics (Your Key Requirement)

| Source | Tool | Deterministic? |
|--------|------|----------------|
| Drone capture | GLOMAP or COLMAP | ✅ Yes |
| Synthetic CG | Direct export (no SfM) | ✅ Yes (ground truth) |
| Re-scanning | RTK alignment | ✅ Yes |

### For Best Splat Quality

| Scenario | Tool | Why |
|----------|------|-----|
| Quick iteration | PostShot | Fast, easy |
| Best geometry | 2DGS | Surface-aligned Gaussians |
| With depth data | DN-Splatter | Native depth supervision |
| Indoor scenes | DN-Splatter | Handles textureless regions |
| Large outdoor | PostShot + GLOMAP | Scale + speed |

### For Your Specific Needs

```
REAL CAPTURE:  GLOMAP → DN-Splatter (with stereo depth) → splat-transform
SYNTHETIC CG:  GSOPs (Houdini) or Blender export → PostShot → splat-transform
```

---

## Part 10: What You Don't Need

| You thought you needed | Reality |
|------------------------|---------|
| Deep EXR from Corona | Regular Z-depth works fine for depth supervision |
| RTK for splat quality | RTK is for geo-referencing, not splat quality |
| LiDAR | Stereo depth is sufficient for 3DGS |
| COLMAP for synthetic | Direct camera export is better (ground truth) |

---

## Summary

1. **SfM**: Use GLOMAP (fast) or COLMAP (robust) for real captures. Skip SfM for synthetic.

2. **Depth**: Your stereo cameras give true depth. Use in DN-Splatter training.

3. **Synthetic CG**:
   - Houdini: GSOPs generate_training_data
   - 3ds Max: Export cameras via MaxScript + Z-depth
   - Blender: Use blender-3dgs-export addon

4. **Training**:
   - Fast/easy: PostShot (no depth input)
   - Best quality: DN-Splatter or 2DGS (with depth)

5. **Final output**: splat-transform for format conversion and optimization

**The Dune workflow works because they're in Houdini.** For 3ds Max, you need a bridge (MaxScript export, Blender, or Houdini USD import).
