# CAD to WebGL Research

Research for building a retail layout space planning system that converts CAD floor plans into interactive WebGL experiences with automated test fit/space plan generation.

## Target Product

A system that:
1. **Imports** CAD floor plans (DWG/DXF)
2. **Generates** multiple retail layout options automatically
3. **Visualizes** in 2D/3D via WebGL
4. **Optimizes** for retail-specific metrics (customer flow, revenue/sqft)
5. **Exports** to CAD, PDF, 3D models

## Research Documents

| File | Description |
|------|-------------|
| [competitor-analysis-laiout.md](./competitor-analysis-laiout.md) | Deep dive on Laiout.co - tech stack, approach, reverse engineering |
| [technical-architecture.md](./technical-architecture.md) | System architecture, component design, data flow |
| [floor-plan-algorithms.md](./floor-plan-algorithms.md) | Academic research on generative floor plan algorithms |
| [cad-to-3d-pipeline.md](./cad-to-3d-pipeline.md) | **CAD → 3D model conversion** - wall extrusion, CSG, AI rendering |

## Competitor Summary

### Laiout.co (Primary Competitor)
- **Focus:** Commercial office layouts
- **Stack:** C#, Autodesk Platform Services, Revit, AI image generation
- **Approach:** Proprietary generative algorithms + constraint-aware rules
- **Performance:** 800-person office in <10 minutes

### TestFit (Market Leader)
- **Focus:** Real estate feasibility, site planning
- **Stack:** Proprietary, generative design
- **Approach:** Thousands of solves in seconds, zoning-aware

## Key Technologies Identified

### CAD Processing
- **Autodesk Platform Services** - Reliable DWG handling (paid)
- **libredwg-web** - WebAssembly DWG parser (open source)
- **dxf-parser** - JavaScript DXF parser (npm)

### 3D Visualization
- **Three.js** - Primary WebGL library
- **Blueprint3D** - Open source floor plan editor
- **xeogl** - CAD/BIM-focused WebGL engine

### Space Planning Algorithms
- **Constraint Programming** - Guarantee valid layouts
- **Genetic Algorithms** - Explore solution space
- **NSGA-II** - Multi-objective optimization
- **Graph-based methods** - Adjacency modeling

## Retail vs Commercial Differences

| Aspect | Commercial (Laiout) | Retail (Our Target) |
|--------|---------------------|---------------------|
| Zone types | Offices, meeting rooms, desks | Displays, checkout, fitting rooms |
| Optimization | Capacity, cost, carbon | Revenue/sqft, customer flow |
| Fixtures | Furniture | Shelving, gondolas, POS |
| Flow | Employee circulation | Customer journey |
| Metrics | Headcount, sq ft/person | Facings, dwell time |

## Implementation Phases

### Phase 1: CAD Parser
- [ ] Test dxf-parser with retail floor plans
- [ ] Evaluate libredwg-web for DWG support
- [ ] Build wall/boundary extraction pipeline
- [ ] Room detection algorithm

### Phase 2: Constraint Model
- [ ] Define retail zone types
- [ ] Create adjacency rules
- [ ] Implement area constraints
- [ ] Code compliance checks (ADA, fire egress)

### Phase 3: Layout Generator
- [ ] Grid discretization system
- [ ] Basic genetic algorithm
- [ ] Fitness functions for retail
- [ ] Multi-objective ranking

### Phase 4: 3D Viewer
- [ ] Three.js setup
- [ ] Wall extrusion from 2D
- [ ] Fixture library (5-10 items)
- [ ] Interactive camera controls

### Phase 5: Export
- [ ] DXF export
- [ ] PDF generation
- [ ] 3D model export (GLTF)
- [ ] Shareable web links

## Key Sources

- [Laiout](https://www.laiout.co) - Competitor
- [TestFit](https://www.testfit.io) - Market leader
- [AEC Magazine - Laiout](https://aecmag.com/cad/laiout-enhances-automated-floor-planning-software/)
- [Blueprint3D](https://github.com/furnishup/blueprint3d) - Open source reference
- [Evolving Floor Plans](https://www.joelsimon.net/evo_floorplans) - Algorithm research
- [dxf-parser](https://github.com/gdsestimating/dxf-parser) - JavaScript library
- [libredwg-web](https://github.com/mlightcad/libredwg-web) - WebAssembly DWG parser
