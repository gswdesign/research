# Technical Architecture: CAD to WebGL Space Planning System

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  CAD Upload  │  │  2D Editor   │  │  3D Viewer   │  │   Metrics    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            CAD PROCESSING LAYER                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  DWG/DXF Parser → Geometry Extraction → Normalization → Grid System  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SPACE PLANNING ENGINE                                │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐                 │
│  │   Constraint   │  │    Genetic     │  │   Multi-Obj    │                 │
│  │    Solver      │──│   Algorithm    │──│   Optimizer    │                 │
│  └────────────────┘  └────────────────┘  └────────────────┘                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          3D GENERATION LAYER                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Extrusion   │  │   Fixture    │  │   Material   │  │   WebGL      │     │
│  │   Engine     │  │   Placement  │  │   System     │  │   Renderer   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             EXPORT LAYER                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │     DWG      │  │     PDF      │  │     CSV      │  │   3D Model   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component 1: CAD Processing Layer

### DWG/DXF Parsing Options

| Library | Type | DWG | DXF | Notes |
|---------|------|-----|-----|-------|
| **Autodesk Platform Services** | Cloud API | ✅ | ✅ | Most reliable, costs $ |
| **libredwg-web** | WebAssembly | ✅ | ✅ | Open source, browser-native |
| **dxf-parser** | JavaScript | ❌ | ✅ | Simple, 39 npm dependents |
| **three-dxf** | JavaScript | ❌ | ✅ | Renders to Three.js directly |
| **dxf-viewer** | JavaScript | ❌ | ✅ | WebGL-based, performance optimized |

### Recommended Approach for Retail

```javascript
// Hybrid approach
const processCAD = async (file) => {
  const extension = file.name.split('.').pop().toLowerCase();

  if (extension === 'dwg') {
    // Option 1: Autodesk Platform Services (reliable)
    return await autodeskCloudConvert(file);

    // Option 2: libredwg-web (free, browser-native)
    // return await libredwgParse(file);
  }

  if (extension === 'dxf') {
    // Use dxf-parser directly
    const parser = new DxfParser();
    return parser.parseSync(await file.text());
  }
};
```

### Geometry Extraction Pipeline

```
Raw CAD Data
     │
     ▼
┌─────────────────┐
│ Entity Filter   │  → Keep: LWPOLYLINE, LINE, ARC, CIRCLE, INSERT
│                 │  → Discard: TEXT, DIMENSION, HATCH (optional)
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ Layer Analysis  │  → Identify wall layers (naming conventions)
│                 │  → Identify door/window layers
│                 │  → Identify column/structural layers
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ Wall Detection  │  → Trace closed polylines
│                 │  → Detect parallel line pairs (wall thickness)
│                 │  → Identify openings (doors, windows)
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ Room Detection  │  → Find enclosed spaces
│                 │  → Calculate areas
│                 │  → Generate room graph
└─────────────────┘
     │
     ▼
┌─────────────────┐
│ Grid Generation │  → Discretize into cells (e.g., 0.5m x 0.5m)
│                 │  → Mark walkable/non-walkable
│                 │  → Mark structural constraints
└─────────────────┘
```

---

## Component 2: Space Planning Engine

### Core Algorithm: Constraint-Genetic Hybrid

Based on research paper: "Floor plan generation through a mixed constraint programming-genetic optimization approach"

#### Phase 1: Constraint Definition

```typescript
interface SpaceRequirement {
  id: string;
  name: string;
  minArea: number;      // sqft
  maxArea: number;
  aspectRatio: { min: number; max: number };
  adjacentTo: string[]; // required neighbors
  awayFrom: string[];   // must not be adjacent
  needsExterior: boolean;
  needsAccess: boolean;
}

// Retail example
const retailZones: SpaceRequirement[] = [
  {
    id: 'entrance',
    name: 'Entrance Zone',
    minArea: 100,
    maxArea: 300,
    aspectRatio: { min: 0.5, max: 2.0 },
    adjacentTo: ['checkout'],
    awayFrom: ['backstock'],
    needsExterior: true,
    needsAccess: true
  },
  {
    id: 'checkout',
    name: 'Checkout Area',
    minArea: 150,
    maxArea: 400,
    aspectRatio: { min: 0.3, max: 1.5 },
    adjacentTo: ['entrance', 'impulse'],
    awayFrom: ['backstock'],
    needsExterior: false,
    needsAccess: true
  },
  // ... more zones
];
```

#### Phase 2: Genetic Algorithm

```typescript
interface LayoutChromosome {
  zones: ZonePlacement[];
  fitness: number;
}

interface ZonePlacement {
  zoneId: string;
  x: number;
  y: number;
  width: number;
  height: number;
  rotation: 0 | 90 | 180 | 270;
}

class GeneticOptimizer {
  population: LayoutChromosome[];
  populationSize = 100;
  generations = 500;
  mutationRate = 0.1;
  crossoverRate = 0.7;

  evolve(): LayoutChromosome[] {
    for (let gen = 0; gen < this.generations; gen++) {
      // Evaluate fitness
      this.population.forEach(p => p.fitness = this.evaluate(p));

      // Selection (tournament)
      const parents = this.select();

      // Crossover
      const children = this.crossover(parents);

      // Mutation
      this.mutate(children);

      // Replace
      this.population = this.selectSurvivors([...this.population, ...children]);
    }

    return this.getTopN(10); // Return best 10 layouts
  }

  evaluate(layout: LayoutChromosome): number {
    let score = 0;

    // Adjacency satisfaction
    score += this.adjacencyScore(layout) * 0.3;

    // Area efficiency
    score += this.areaEfficiencyScore(layout) * 0.2;

    // Customer flow optimization (retail-specific)
    score += this.customerFlowScore(layout) * 0.25;

    // Code compliance
    score += this.complianceScore(layout) * 0.15;

    // Revenue potential (retail-specific)
    score += this.revenueScore(layout) * 0.1;

    return score;
  }
}
```

#### Phase 3: Multi-Objective Optimization (NSGA-II)

For generating diverse options rather than single "best":

```typescript
interface ObjectiveScores {
  customerFlow: number;      // Maximize
  revenuePerSqft: number;    // Maximize
  staffEfficiency: number;   // Maximize
  complianceMargin: number;  // Maximize
  constructionCost: number;  // Minimize
}

// NSGA-II produces Pareto-optimal set
// User can then choose based on priorities
```

---

## Component 3: 3D Generation Layer

### Three.js-Based Architecture

```typescript
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

class RetailLayoutViewer {
  scene: THREE.Scene;
  camera: THREE.PerspectiveCamera;
  renderer: THREE.WebGLRenderer;

  constructor(container: HTMLElement) {
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    this.renderer = new THREE.WebGLRenderer({ antialias: true });

    this.setupLighting();
    this.setupControls();
  }

  generateFromLayout(layout: LayoutChromosome, floorPlan: ParsedFloorPlan) {
    // 1. Create floor
    this.addFloor(floorPlan.bounds);

    // 2. Extrude walls
    floorPlan.walls.forEach(wall => {
      this.extrudeWall(wall, 3.0); // 3m height
    });

    // 3. Add zone indicators
    layout.zones.forEach(zone => {
      this.addZoneVisualization(zone);
    });

    // 4. Place fixtures from library
    layout.fixtures?.forEach(fixture => {
      this.placeFixture(fixture);
    });

    // 5. Add ceiling (optional)
    this.addCeiling(floorPlan.bounds, 3.0);
  }

  extrudeWall(wall: Wall, height: number) {
    const shape = new THREE.Shape();
    // ... create wall shape from 2D coordinates

    const extrudeSettings = {
      steps: 1,
      depth: height,
      bevelEnabled: false
    };

    const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
    const material = new THREE.MeshStandardMaterial({ color: 0xffffff });
    const mesh = new THREE.Mesh(geometry, material);

    mesh.rotation.x = -Math.PI / 2;
    this.scene.add(mesh);
  }
}
```

### Fixture Library System

```typescript
interface FixtureDefinition {
  id: string;
  name: string;
  category: 'shelving' | 'display' | 'checkout' | 'signage' | 'fitting';
  dimensions: { width: number; depth: number; height: number };
  modelPath: string; // GLB/GLTF file
  variants: FixtureVariant[];
  clearanceRequired: { front: number; back: number; sides: number };
  canRotate: boolean;
  snapToGrid: boolean;
}

const retailFixtures: FixtureDefinition[] = [
  {
    id: 'gondola-4ft',
    name: '4ft Gondola Shelving',
    category: 'shelving',
    dimensions: { width: 1.22, depth: 0.45, height: 1.8 },
    modelPath: '/fixtures/gondola-4ft.glb',
    variants: [
      { id: 'single-sided', modelPath: '/fixtures/gondola-4ft-single.glb' },
      { id: 'double-sided', modelPath: '/fixtures/gondola-4ft-double.glb' }
    ],
    clearanceRequired: { front: 0.9, back: 0.3, sides: 0 },
    canRotate: true,
    snapToGrid: true
  },
  // ... more fixtures
];
```

---

## Component 4: Retail-Specific Features

### Customer Flow Simulation

```typescript
class CustomerFlowSimulator {
  grid: FlowCell[][];
  entryPoints: Point[];
  attractionPoints: { point: Point; strength: number }[];

  simulate(layout: LayoutChromosome): FlowMetrics {
    // Agent-based simulation
    const agents: CustomerAgent[] = [];

    for (let i = 0; i < 1000; i++) {
      const agent = new CustomerAgent(this.randomEntry());

      while (!agent.hasExited) {
        // Move toward attractions
        // Avoid obstacles
        // Record path
        agent.step();
      }

      agents.push(agent);
    }

    return {
      avgDwellTime: this.calcAvgDwellTime(agents),
      coverageMap: this.generateHeatmap(agents),
      deadZones: this.identifyDeadZones(agents),
      congestionPoints: this.findCongestion(agents),
      avgPathLength: this.calcAvgPathLength(agents)
    };
  }
}
```

### Revenue Optimization Metrics

```typescript
interface RetailMetrics {
  totalSalesFloor: number;           // sqft
  productiveSalesFloor: number;      // excludes circulation
  linearFeetOfDisplay: number;
  facingsCapacity: number;
  impulsePurchaseZoneCoverage: number;
  checkoutQueueCapacity: number;
  avgCustomerPathLength: number;
  estimatedRevenuePerSqft: number;
}
```

---

## Data Flow Summary

```
User uploads DWG
        │
        ▼
Parse CAD → Extract walls, doors, columns
        │
        ▼
User sets parameters:
  - Zone types & sizes
  - Adjacency requirements
  - Optimization priorities
        │
        ▼
Generate 100+ layout options (genetic algorithm)
        │
        ▼
Rank by multi-objective fitness
        │
        ▼
Display top options with metrics
        │
        ▼
User selects/refines zones
        │
        ▼
Add fixtures from library
        │
        ▼
Run customer flow simulation
        │
        ▼
Generate 3D preview (Three.js)
        │
        ▼
Export: DWG, PDF, CSV, 3D model, interactive link
```

---

## Technology Recommendations

### Frontend
- **React/Vue/Svelte** - UI framework
- **Three.js** - 3D rendering
- **Fabric.js or Konva** - 2D canvas editing
- **Web Workers** - Offload heavy computation

### Backend (if needed)
- **Node.js** or **Python (FastAPI)**
- **Autodesk Platform Services** - CAD processing
- **Redis** - Caching generated layouts
- **PostgreSQL** - Store projects, layouts, metrics

### Algorithms (consider WebAssembly for performance)
- **Rust** compiled to WASM for constraint solver
- **JavaScript** genetic algorithm (or Rust/WASM)

### Libraries to Evaluate
- [dxf-parser](https://github.com/gdsestimating/dxf-parser)
- [libredwg-web](https://github.com/mlightcad/libredwg-web)
- [blueprint3d](https://github.com/furnishup/blueprint3d)
- [three.js](https://threejs.org/)

---

## Next Steps

1. **Prototype CAD parser** - Test dxf-parser with sample retail floor plans
2. **Build constraint model** - Define retail zone requirements
3. **Implement basic genetic algorithm** - Generate layout variations
4. **Create minimal 3D viewer** - Three.js wall extrusion
5. **Integrate fixture library** - Start with 5-10 common retail fixtures
