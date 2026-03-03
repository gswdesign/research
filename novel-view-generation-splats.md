# Novel View Generation & Gaussian Splatting for Real Estate 3D Sales Apps

## Research Date: March 2026

---

## 1. The Problem

You have a single image (e.g., an architectural render or listing photo) and want to:
1. Generate novel views from different angles
2. Convert those into a navigable 3D Gaussian Splat
3. Clean up any artifacts/errors in the result

The core challenge: single-image 3D reconstruction is inherently ill-posed — there's no real geometric data for occluded surfaces, so everything unseen must be hallucinated by AI.

---

## 2. Why ML-Sharp (Apple SHARP) Only Works Close to Camera

You're right about ML-Sharp. Apple's [SHARP](https://github.com/apple/ml-sharp) (released Dec 2025, open-source) generates a 3DGS from a single image in under a second via a feedforward neural network. However:

- **It's designed for "nearby views" only** — small camera movements from the original viewpoint
- Large displacements, strong occlusion, and extreme angle changes cause quality degradation
- All depth/structure is inferred from a single monocular image — there's no real multi-view constraint
- Reflections, transparent objects, and repetitive textures are especially prone to artifacts

This is a **fundamental limitation of single-image monocular splat approaches** — they can only infer what's plausibly behind/around objects based on learned priors, not real geometry.

---

## 3. Can Nano Banana Pro Generate Novel Views for a Splat Pipeline?

**Short answer: Yes, this is a viable emerging workflow, but with caveats.**

### What Nano Banana Pro Is
[Nano Banana Pro](https://blog.google/innovation-and-ai/products/nano-banana-pro/) is Google DeepMind's Gemini 3 Pro image generation/editing model. It's not a 3D tool — it generates and edits 2D images. But it has a key capability:

- **Novel view synthesis via prompting**: Upload a single image and prompt for front, side, back, and three-quarter views. It intelligently understands depth and perspective.
- **Multi-view consistency**: Its multiplanar projection workflow generates views with consistent proportions, lighting, and details across angles.
- **Up to 14 reference images**: Can blend multiple inputs while maintaining consistency.

### The Pipeline: Nano Banana Pro → Multi-View → Splat

**Step 1: Generate multi-view images with Nano Banana Pro**
- Upload your architectural image/render
- Prompt: *"Generate front, three-quarter left, three-quarter right, side left, side right, and rear views of this building. Keep proportions realistic, lighting consistent, and maintain architectural details."*
- This gives you ~4-8 consistent view images

**Step 2: Convert multi-view images to 3D**
Several options:

| Tool | Method | Output | Cost |
|------|--------|--------|------|
| **Tripo AI** | Image-to-3D (integrated with Nano Banana) | OBJ/GLB/FBX/STL | Free tier + paid |
| **Meshy** | Multi-image to 3D mesh | OBJ/FBX/GLB/USDZ | Freemium |
| **KIRI Engine** | Multi-view 3DGS reconstruction | Gaussian Splat .ply | Free + paid |
| **Postshot** (Jawset) | Local NeRF/GS from images | Gaussian Splat | €17/mo |
| **Polycam** | Cloud-based photogrammetry/GS | Gaussian Splat .ply | Free tier + $17.99/mo |

**Step 3: Clean up artifacts** (see Section 5 below)

### Critical Caveats

1. **AI-generated views are hallucinated** — Nano Banana Pro "invents" what the back of the building looks like. For architectural renders where you have the 3D model, this may be unnecessary (just render more views from the model).
2. **Consistency isn't perfect** — even with good prompting, there will be geometric inconsistencies between generated views that cause splat artifacts.
3. **For real listing photos**, this is genuinely useful because you can't go back and take more photos.
4. **The more real multi-view data you have, the better** — if you can capture even 5-10 real photos, that will massively outperform AI-generated views.

---

## 4. Better Alternatives to Consider

### A. World Labs Marble (Best for Single Image → Explorable 3D)

[World Labs Marble](https://www.worldlabs.ai/blog/marble-world-model) is probably the **most directly relevant tool** for your use case:

- Takes a **single image** and generates a full, explorable 3D environment
- **Imagines what's out of frame** — not just nearby views, but the entire surrounding space
- Exports as **Gaussian splats, meshes, or videos**
- Has a **3D editor (Chisel)** for adjusting spatial layouts with text prompts
- Real-time generation via RTFM at interactive framerates
- **API coming in 2026** for integration into apps
- Founded by Fei-Fei Li, backed by $230M VC

Their open-source [Spark renderer](https://www.worldlabs.ai/case-studies/memory-house) integrates Gaussian splats into Three.js for web-based 3D experiences — works on desktop, mobile, and VR.

**For real estate**: Upload a listing photo → get an explorable 3D space → export as splat → embed in your sales app.

### B. SplatDiff (SIGGRAPH 2025 — Best Academic Result)

[SplatDiff](https://dl.acm.org/doi/10.1145/3721238.3730669) uses pixel-splatting-guided video diffusion for geometry-consistent novel view synthesis. Key insight: simple pixel splatting better preserves appearance than 3DGS under single/sparse input, since estimating accurate Gaussian parameters from limited observations is extremely hard.

### C. Complete Gaussian Splats via Diffusion (arXiv Aug 2025)

[This paper](https://arxiv.org/abs/2508.21542) proposes a latent diffusion model that reconstructs a complete 3D scene with Gaussian splats — including occluded parts — from a single image. Uses a generative approach to learn a distribution of plausible 3D scenes conditioned on the input.

### D. SVG3D (Nature, May 2025)

[SVG3D](https://www.nature.com/articles/s41598-025-03200-7) uses monocular depth estimation + U-Net to predict Gaussian ellipsoid parameters per pixel, with refinement via depth/normal constraints and diffusion priors.

---

## 5. Cleaning Errors and Artifacts

Yes, errors can be cleaned. There are both automated and manual approaches:

### Automated Methods (State of the Art)

| Method | Year | Approach | Result |
|--------|------|----------|--------|
| **[Clean-GS](https://github.com/smlab-niser/clean-gs)** | Jan 2026 | Semantic mask-guided pruning — uses as few as 3 segmentation masks to identify/remove floaters | 60-80% model compression, 2-5 min on CPU |
| **[EFA-GS](https://arxiv.org/abs/2508.02493)** | Aug 2025 | Frequency-aware Gaussian expansion — prevents over-shrinking that causes floaters | +1.68 dB PSNR improvement |
| **[TIDI-GS](https://arxiv.org/html/2601.09291)** | Jan 2026 | Evidence/context/detail-aware training framework for indoor scenes | Geometrically reliable digital twins |
| **FreeSplat++** | 2025 | Depth-weighted floater removal + fine-tuning | Built into generalizable pipeline |

### Manual/Interactive Tools

- **[SuperSplat](https://playcanvas.com/supersplat/editor)** — Web-based editor for cleaning Gaussian models. Very versatile for manual floater removal.
- **CloudCompare** — Open-source point cloud editor. Can trim splats viewed as point clouds and generate approximate meshes.
- **Postshot** — Has built-in editing tools for cropping and cleaning splats.
- **Unity/Unreal GS plugins** — Interactive selection and deletion of floaters in-engine.

### Recommended Cleanup Pipeline

1. **First pass**: Run Clean-GS (automated, 2-5 min) to remove 60-80% of floaters
2. **Second pass**: Use SuperSplat for manual cleanup of remaining artifacts
3. **Final pass**: Crop bounding volume to remove distant noise

---

## 6. Recommended Pipeline for Your Use Case

### For Architectural Renders (you have the 3D model)

If you're building sales apps from architectural renders, you already have the 3D model. The best approach:

1. **Render 100-200 views** from the 3D model (spiral pattern, multiple heights)
2. **Feed into Postshot or Polycam** for high-quality Gaussian splat generation
3. **Clean with Clean-GS + SuperSplat**
4. **Serve via Spark (Three.js)** or native viewer

This avoids all the single-image limitations entirely.

### For Single Listing Photos (no 3D model)

1. **World Labs Marble** — single image → full explorable 3D → export as splat
   - Best quality for "imagining" unseen parts of a scene
   - API coming 2026 for app integration

2. **Nano Banana Pro + Reconstruction Pipeline**:
   - Generate 6-8 consistent views via Nano Banana Pro
   - Feed into KIRI Engine or Postshot for splat reconstruction
   - Clean with Clean-GS + SuperSplat
   - More control over the process, but more steps and potential for inconsistency

3. **Apple SHARP** — for quick "2.5D" previews (nearby views only)
   - Good for a subtle parallax effect on listing photos
   - Not suitable for full 360 exploration

### For Physical Properties (can visit the site)

1. **Capture 200-500 photos** with a smartphone (lock exposure, 70-80% overlap)
2. **Process with Postshot** (local, best quality) or **Polycam** (cloud, easiest)
3. **Clean with Clean-GS + SuperSplat**
4. This gives the best results by far — real multi-view data always beats AI hallucination

---

## 7. Industry Context (Real Estate + 3DGS in 2026)

- **Zillow** shipped Gaussian Splatting in SkyTours (first major RE platform)
- **Apartments.com** (CoStar) added exterior 3DGS via Matterport 3D Exteriors
- **Khronos Group** announced [glTF Gaussian Splatting standard](https://architosh.com/2026/02/the-khronos-group-announces-gltf-gaussian-splatting-standard/) (Feb 2026)
- **3DVista 2025.0** added GS support — models 10x lighter than GLB
- **Esri ArcGIS Pro 2.6** added GS support
- **DJI Terra** added GS support for drone captures
- **OTOY OctaneRender 2026** ships full path-traced Gaussian splats
- Three.js/Babylon.js 8.0 enable performant browser-based GS rendering

The consensus: 2025 was when 3DGS moved from research to production. 2026 is the inflection point where it becomes a standard tool.

---

## 8. Key Takeaways

1. **ML-Sharp/SHARP limitation is fundamental** — single-image monocular approaches can only do nearby views. This is a physics problem, not a software bug.

2. **Nano Banana Pro can generate multi-view images** that feed into a splat pipeline, but the views are hallucinated — expect geometric inconsistencies and artifacts that need cleanup.

3. **World Labs Marble is probably your best bet** for single-image → explorable 3D, as it's purpose-built for this and exports native splats.

4. **Artifacts CAN be cleaned** — Clean-GS (automated) + SuperSplat (manual) is the current best practice. Expect 60-80% of floaters removed automatically.

5. **If you can capture real photos or render from a 3D model, always do that** — it will massively outperform any single-image AI approach.

6. **The ecosystem is maturing fast** — glTF standardization, major platform adoption (Zillow, Apartments.com), and browser rendering (Three.js/Spark) mean splats are becoming a viable production format for real estate apps in 2026.

---

## Sources

- [Apple ML-Sharp (SHARP) — GitHub](https://github.com/apple/ml-sharp)
- [Nano Banana Pro — Google DeepMind](https://blog.google/innovation-and-ai/products/nano-banana-pro/)
- [World Labs Marble](https://www.worldlabs.ai/blog/marble-world-model)
- [Clean-GS — Semantic Mask-Guided Pruning](https://github.com/smlab-niser/clean-gs)
- [EFA-GS — Eliminating Floating Artifacts](https://arxiv.org/abs/2508.02493)
- [TIDI-GS — Floater Suppression for Indoor Scenes](https://arxiv.org/html/2601.09291)
- [SVG3D — Single View 3D Reconstruction](https://www.nature.com/articles/s41598-025-03200-7)
- [SplatDiff — SIGGRAPH 2025](https://dl.acm.org/doi/10.1145/3721238.3730669)
- [Complete Gaussian Splats from Single Image via Diffusion](https://arxiv.org/abs/2508.21542)
- [3DGS Complete Guide 2026 — Utsubo](https://www.utsubo.com/blog/gaussian-splatting-guide)
- [glTF Gaussian Splatting Standard — Khronos](https://architosh.com/2026/02/the-khronos-group-announces-gltf-gaussian-splatting-standard/)
- [Gaussian Splatting for AEC — AEC Magazine](https://aecmag.com/technology/introducing-gaussian-splats-for-aec/)
- [Nano Banana + Tripo AI Pipeline](https://www.tripo3d.ai/blog/how-to-use-nano-banana-in-tripo-studio)
- [KIRI Engine — Single Image to 4D GS](https://www.kiriengine.app/blog/SingleImagesTo4DGS)
- [2025 Gaussian Splatting Paper List](https://github.com/Lee-JaeWon/2025-Arxiv-Paper-List-Gaussian-Splatting)
