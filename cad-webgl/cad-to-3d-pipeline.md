# CAD to 3D Model Pipeline

Deep dive into how Laiout and similar tools convert 2D CAD floor plans into interactive 3D models.

---

## Laiout's 3D Flow (Reverse Engineered)

Based on their product descriptions and job postings:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           LAIOUT'S PIPELINE                                  │
└─────────────────────────────────────────────────────────────────────────────┘

Step 1: CAD INPUT
─────────────────
DWG/DXF floor plan → Autodesk Platform Services (cloud)
                          │
                          ▼
                   Parse geometry
                   Extract walls, doors, columns
                   Identify building envelope

Step 2: ZONE GENERATION (2D)
────────────────────────────
Building envelope → Generative algorithm → 100s of zone layouts
                         │
                         ├── Code-aware spacing rules
                         ├── Adjacency constraints
                         └── Area optimization

Step 3: FURNITURE POPULATION
────────────────────────────
Zone layout → Furniture placement algorithm → Furnished 2D plan
                    │
                    ├── 100+ furniture blocks library
                    ├── Density parameters
                    └── Clearance rules

Step 4: 3D EXTRUSION
────────────────────
2D furnished plan → 3D mesh generation → Interactive 3D model
                          │
                          ├── Wall extrusion (height parameter)
                          ├── Floor/ceiling planes
                          ├── 3D furniture models
                          └── Door/window openings

Step 5: AI RENDERING
────────────────────
3D model → Text-to-render AI → Photorealistic images
                │
                ├── "High-quality images in seconds"
                ├── Style customization
                └── Material/lighting variations
```

---

## Technical Deep Dive: 2D to 3D Conversion

### Step 1: Wall Extrusion

The core operation - converting 2D wall lines to 3D geometry.

```typescript
// Input: 2D wall represented as line segment with thickness
interface Wall2D {
  start: { x: number; y: number };
  end: { x: number; y: number };
  thickness: number;  // wall thickness in meters
  openings: Opening[]; // doors, windows
}

interface Opening {
  type: 'door' | 'window';
  position: number;    // 0-1 along wall length
  width: number;
  height: number;
  sillHeight: number;  // 0 for doors
}

// Output: 3D mesh
function extrudeWall(wall: Wall2D, height: number): THREE.Mesh {
  // 1. Create wall profile (cross-section)
  const profile = createWallProfile(wall);

  // 2. Extrude to height
  const extrudeSettings = {
    steps: 1,
    depth: height,
    bevelEnabled: false
  };

  let geometry = new THREE.ExtrudeGeometry(profile, extrudeSettings);

  // 3. Cut openings using CSG (Constructive Solid Geometry)
  wall.openings.forEach(opening => {
    const openingBox = createOpeningGeometry(wall, opening);
    geometry = CSG.subtract(geometry, openingBox);
  });

  return new THREE.Mesh(geometry, wallMaterial);
}

function createWallProfile(wall: Wall2D): THREE.Shape {
  const shape = new THREE.Shape();

  // Calculate perpendicular offset for wall thickness
  const dx = wall.end.x - wall.start.x;
  const dy = wall.end.y - wall.start.y;
  const len = Math.sqrt(dx * dx + dy * dy);
  const nx = -dy / len * wall.thickness / 2;
  const ny = dx / len * wall.thickness / 2;

  // Create rectangular profile
  shape.moveTo(wall.start.x + nx, wall.start.y + ny);
  shape.lineTo(wall.end.x + nx, wall.end.y + ny);
  shape.lineTo(wall.end.x - nx, wall.end.y - ny);
  shape.lineTo(wall.start.x - nx, wall.start.y - ny);
  shape.closePath();

  return shape;
}
```

### Step 2: Opening Subtraction (CSG)

Doors and windows are carved out using boolean operations.

```typescript
import { CSG } from 'three-csg-ts';

function createOpeningGeometry(wall: Wall2D, opening: Opening): THREE.Mesh {
  // Position along wall
  const t = opening.position;
  const x = wall.start.x + (wall.end.x - wall.start.x) * t;
  const y = wall.start.y + (wall.end.y - wall.start.y) * t;

  // Create box for subtraction
  const boxGeometry = new THREE.BoxGeometry(
    opening.width,
    opening.height,
    wall.thickness + 0.1  // slightly larger to ensure clean cut
  );

  const box = new THREE.Mesh(boxGeometry);
  box.position.set(x, opening.sillHeight + opening.height / 2, y);

  // Rotate to align with wall
  const wallAngle = Math.atan2(
    wall.end.y - wall.start.y,
    wall.end.x - wall.start.x
  );
  box.rotation.y = wallAngle;

  return box;
}

// Boolean subtraction
function subtractOpening(wallMesh: THREE.Mesh, openingMesh: THREE.Mesh): THREE.Mesh {
  const wallCSG = CSG.fromMesh(wallMesh);
  const openingCSG = CSG.fromMesh(openingMesh);
  const resultCSG = wallCSG.subtract(openingCSG);
  return CSG.toMesh(resultCSG, wallMesh.matrix, wallMesh.material);
}
```

### Step 3: Floor & Ceiling Generation

```typescript
function generateFloor(boundary: Point2D[]): THREE.Mesh {
  // Create shape from boundary polygon
  const shape = new THREE.Shape();
  shape.moveTo(boundary[0].x, boundary[0].y);
  boundary.slice(1).forEach(p => shape.lineTo(p.x, p.y));
  shape.closePath();

  // Simple plane geometry (or extruded for thickness)
  const geometry = new THREE.ShapeGeometry(shape);
  const material = new THREE.MeshStandardMaterial({
    color: 0xcccccc,
    side: THREE.DoubleSide
  });

  const floor = new THREE.Mesh(geometry, material);
  floor.rotation.x = -Math.PI / 2;  // Lay flat
  floor.position.y = 0;

  return floor;
}

function generateCeiling(boundary: Point2D[], height: number): THREE.Mesh {
  const ceiling = generateFloor(boundary);
  ceiling.position.y = height;
  ceiling.rotation.x = Math.PI / 2;  // Face down
  return ceiling;
}
```

### Step 4: Furniture/Fixture Placement

```typescript
interface Fixture3D {
  id: string;
  modelUrl: string;        // GLB/GLTF path
  position: { x: number; y: number; z: number };
  rotation: number;        // Y-axis rotation in radians
  scale: number;
}

class FixtureLoader {
  private loader = new GLTFLoader();
  private cache = new Map<string, THREE.Object3D>();

  async loadFixture(fixture: Fixture3D): Promise<THREE.Object3D> {
    // Check cache
    if (!this.cache.has(fixture.modelUrl)) {
      const gltf = await this.loader.loadAsync(fixture.modelUrl);
      this.cache.set(fixture.modelUrl, gltf.scene);
    }

    // Clone from cache
    const model = this.cache.get(fixture.modelUrl)!.clone();

    // Apply transforms
    model.position.set(fixture.position.x, fixture.position.z, fixture.position.y);
    model.rotation.y = fixture.rotation;
    model.scale.setScalar(fixture.scale);

    return model;
  }
}
```

---

## The AI Rendering Layer

Laiout's "text-to-render" feature (from their Generative AI Specialist role):

### How It Likely Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI RENDERING PIPELINE                        │
└─────────────────────────────────────────────────────────────────┘

Option A: Diffusion Model Approach
──────────────────────────────────
3D scene → Render to 2D view → img2img diffusion → Styled output
              │                      │
              │                      ├── ControlNet (depth/edge guidance)
              │                      ├── Style prompt ("modern office...")
              │                      └── Stable Diffusion / SDXL
              │
              └── Low-poly render as input conditioning

Option B: Neural Rendering
──────────────────────────
3D scene → NeRF/3D Gaussian Splatting → Photorealistic views
                    │
                    └── Trained on interior photography dataset

Option C: Traditional + AI Hybrid
─────────────────────────────────
3D scene → PBR render → AI upscale/enhance → Final image
              │                │
              │                ├── Real-ESRGAN (upscaling)
              │                └── Style transfer model
              │
              └── Three.js with realistic materials
```

### Implementation Example (Option A)

```typescript
// Generate rendered view from 3D scene
async function generateAIRender(
  scene: THREE.Scene,
  camera: THREE.Camera,
  style: string
): Promise<Blob> {
  // 1. Render base image from Three.js
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(1024, 1024);
  renderer.render(scene, camera);
  const baseImage = renderer.domElement.toDataURL('image/png');

  // 2. Generate depth map for ControlNet
  const depthMaterial = new THREE.MeshDepthMaterial();
  scene.overrideMaterial = depthMaterial;
  renderer.render(scene, camera);
  const depthImage = renderer.domElement.toDataURL('image/png');
  scene.overrideMaterial = null;

  // 3. Call AI rendering API
  const response = await fetch('/api/ai-render', {
    method: 'POST',
    body: JSON.stringify({
      baseImage,
      depthImage,
      prompt: `${style}, interior photography, professional lighting, 8k`,
      negativePrompt: 'blurry, distorted, low quality',
      strength: 0.7  // How much to modify original
    })
  });

  return response.blob();
}
```

---

## Complete 3D Generation Pipeline

```typescript
class FloorPlan3DGenerator {
  scene: THREE.Scene;
  fixtureLoader: FixtureLoader;

  async generate(
    floorPlan: ParsedFloorPlan,
    layout: GeneratedLayout,
    options: GenerationOptions
  ): Promise<THREE.Scene> {
    this.scene = new THREE.Scene();

    // 1. Create floor
    const floor = generateFloor(floorPlan.boundary);
    this.scene.add(floor);

    // 2. Extrude walls with openings
    for (const wall of floorPlan.walls) {
      const wallMesh = extrudeWall(wall, options.wallHeight);
      this.scene.add(wallMesh);
    }

    // 3. Add ceiling (optional)
    if (options.showCeiling) {
      const ceiling = generateCeiling(floorPlan.boundary, options.wallHeight);
      this.scene.add(ceiling);
    }

    // 4. Create zone visualizations (colored floor areas)
    for (const zone of layout.zones) {
      const zoneMesh = createZoneOverlay(zone);
      this.scene.add(zoneMesh);
    }

    // 5. Place fixtures
    for (const fixture of layout.fixtures) {
      const fixtureModel = await this.fixtureLoader.loadFixture(fixture);
      this.scene.add(fixtureModel);
    }

    // 6. Add lighting
    this.addLighting(options.lightingMode);

    // 7. Add structural elements (columns)
    for (const column of floorPlan.columns) {
      const columnMesh = createColumn(column, options.wallHeight);
      this.scene.add(columnMesh);
    }

    return this.scene;
  }

  addLighting(mode: 'realistic' | 'schematic') {
    if (mode === 'realistic') {
      // Ambient
      this.scene.add(new THREE.AmbientLight(0xffffff, 0.4));

      // Directional (sun)
      const sun = new THREE.DirectionalLight(0xffffff, 0.8);
      sun.position.set(10, 20, 10);
      sun.castShadow = true;
      this.scene.add(sun);

      // Point lights for interior
      // ... add based on ceiling layout
    } else {
      // Simple even lighting for schematic view
      this.scene.add(new THREE.AmbientLight(0xffffff, 1.0));
    }
  }
}
```

---

## Low-Poly Mesh Optimization

For web performance, Laiout likely uses simplified geometry:

```typescript
// Simplify mesh for web delivery
import { SimplifyModifier } from 'three/examples/jsm/modifiers/SimplifyModifier';

function optimizeMesh(mesh: THREE.Mesh, targetReduction: number): THREE.Mesh {
  const modifier = new SimplifyModifier();
  const originalCount = mesh.geometry.attributes.position.count;
  const targetCount = Math.floor(originalCount * (1 - targetReduction));

  const simplified = modifier.modify(mesh.geometry, targetCount);
  return new THREE.Mesh(simplified, mesh.material);
}

// LOD (Level of Detail) for large scenes
function createLOD(mesh: THREE.Mesh): THREE.LOD {
  const lod = new THREE.LOD();

  lod.addLevel(mesh, 0);                           // Full detail at close range
  lod.addLevel(optimizeMesh(mesh, 0.5), 20);      // 50% reduction at 20 units
  lod.addLevel(optimizeMesh(mesh, 0.8), 50);      // 80% reduction at 50 units

  return lod;
}
```

---

## Export Formats

### To DWG (via Autodesk services)

```typescript
async function exportToDWG(scene: THREE.Scene): Promise<Blob> {
  // Convert Three.js scene to Autodesk-compatible format
  const sceneData = serializeScene(scene);

  // Call Autodesk Design Automation API
  const response = await fetch('https://developer.api.autodesk.com/...', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${autodeskToken}` },
    body: JSON.stringify({
      input: sceneData,
      outputFormat: 'dwg'
    })
  });

  return response.blob();
}
```

### To GLTF/GLB (native Three.js)

```typescript
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter';

function exportToGLTF(scene: THREE.Scene): Promise<ArrayBuffer> {
  return new Promise((resolve, reject) => {
    const exporter = new GLTFExporter();
    exporter.parse(
      scene,
      (result) => resolve(result as ArrayBuffer),
      (error) => reject(error),
      { binary: true }  // GLB format
    );
  });
}
```

---

## Key Algorithms Summary

| Stage | Algorithm | Purpose |
|-------|-----------|---------|
| Wall extrusion | THREE.ExtrudeGeometry | 2D shape → 3D solid |
| Opening cuts | CSG (Boolean subtract) | Doors/windows in walls |
| Floor/ceiling | THREE.ShapeGeometry | Boundary → plane mesh |
| Mesh simplification | SimplifyModifier | Performance optimization |
| Fixture placement | GLTFLoader + transforms | 3D model positioning |
| AI rendering | ControlNet + Diffusion | Photorealistic output |

---

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Initial 3D generation | <2 seconds | Excludes fixture loading |
| Fixture loading | <500ms each | With caching |
| Frame rate | 60 FPS | On mid-range hardware |
| Memory | <500MB | For typical retail layout |
| Export to GLTF | <5 seconds | Full scene |

---

## Sources

- [Three.js Documentation](https://threejs.org/docs/)
- [three-csg-ts](https://github.com/samalexander/three-csg-ts) - CSG for Three.js
- [Plan2Scene](https://3dlg-hcvc.github.io/plan2scene/) - Academic floor plan to 3D
- [3DPlanNet](https://www.mdpi.com/2079-9292/10/22/2729) - ML-based 3D generation
- [Blueprint3D](https://github.com/furnishup/blueprint3d) - Open source reference
