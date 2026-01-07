# Competitor Analysis: Laiout.co

## Overview

**Company:** Laiout (Norwegian proptech)
**Product:** AI-powered instant space planning platform for offices
**Target Market:** Commercial real estate (landlords, tenants, brokers, designers)
**Markets:** UK, EU, US

Your target adaptation: **Retail layouts** instead of commercial offices

---

## What They Do

### Core Value Proposition
- Generate multiple test fit options from blank/messy CAD plans in seconds
- Move from "weeks of back and forth to a single meeting" for floor plan decisions
- 60-80% time savings in early planning stages

### Workflow (4 clicks to populated floor plan)
1. **Upload** - Simple building outline (CAD file)
2. **Generate** - AI produces hundreds of layout options with detailed statistics
3. **Refine** - Select areas to keep, regenerate others
4. **Export** - DWG, PDF, CSV, or interactive shareable link

### Key Features
- Real-time metrics: capacity, cost, carbon emissions
- Adjustable parameters: program, adjacencies, densities, clearances
- Code-aware spacing and practice rules
- 100+ high-detail furniture library blocks
- AI-powered text-to-render image generation
- Side-by-side scenario comparison
- No viewer licenses required for stakeholders

---

## Tech Stack (Reverse Engineered)

### From Careers Page

| Role | Technology |
|------|------------|
| Revit Developer | **C#, Autodesk Platform Services** |
| Full-Stack Developer | Web development (frontend/backend) |
| Generative AI Specialist | Image augmentation & stylization |

### Inferred Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT (Web-based)                        │
├─────────────────────────────────────────────────────────────────┤
│  - Cloud/SaaS platform (Windows, Mac, Web)                      │
│  - 2D Floor plan editor                                          │
│  - 3D WebGL visualization                                        │
│  - Real-time metrics dashboard                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GENERATION ENGINE                           │
├─────────────────────────────────────────────────────────────────┤
│  - Proprietary generative design algorithms                      │
│  - Constraint-aware rule system                                  │
│  - Regulation compliance checking                                │
│  - Multi-solution optimization                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AUTODESK INTEGRATION                          │
├─────────────────────────────────────────────────────────────────┤
│  - Autodesk Platform Services (cloud APIs)                       │
│  - Revit integration (C#)                                        │
│  - DWG import/export                                             │
│  - BIM data processing                                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       AI/ML LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  - Text-to-render image generation                               │
│  - Image augmentation & stylization                              │
│  - Architectural logic constraints                               │
└─────────────────────────────────────────────────────────────────┘
```

### Team Composition (Clues to Tech Depth)
- **CTO:** PhD in Particle Physics (algorithmic/optimization background)
- **Staff:** PhDs in Astrophysics, Geophysics (computational expertise)
- **Architects:** 10+ years CAD experience
- **Developers:** Full-stack, backend, cloud architects (7-15+ years)
- **Open source contributors** on the team

---

## Competitor: TestFit (Market Leader)

**Funding:** $20M+ (Prologis Ventures, Perot Jain, Parkway VC)
**Users:** 7,700+ evaluating 3,200+ deals/week
**Focus:** Real estate feasibility, site planning, urban development

### TestFit's Approach
- Generative Design launched June 2024
- Generates thousands of solves in seconds
- Constraint parameters: FAR, dwelling units/acre, parking ratios, setbacks
- Real-time iteration with instant updates
- Combined AI + human editing workflow

### Key Difference from Laiout
- TestFit = Site-level/building massing (macro)
- Laiout = Interior floor plan layouts (micro)

---

## How They Likely Work (Technical Deep Dive)

### 1. CAD Input Processing

**Supported Flow:**
```
DWG/DXF Input → Parse → Extract Geometry → Normalize → Grid Discretization
```

**Key Challenge:** DWG is proprietary (Autodesk). Solutions:
- **Autodesk Platform Services** (cloud API) - what Laiout uses
- Open-source parsers (libredwg, limited reliability)
- Convert to DXF first (open format)

### 2. Space Planning Algorithm

Based on academic research, they likely use a **hybrid approach**:

#### A. Constraint Programming
- Define rooms with area requirements
- Define adjacency relationships
- Define circulation paths
- Discretize into grid cells
- Solve as constraint satisfaction problem

#### B. Genetic/Evolutionary Optimization
```
Population of layouts → Evaluate fitness → Selection → Crossover → Mutation → Repeat
```

**Fitness criteria:**
- Walking distance minimization
- Adjacency satisfaction
- Area efficiency
- Daylight access
- Circulation flow
- Code compliance

#### C. Graph-Based Methods
- Room adjacency as graph
- Graph contraction algorithms for layout
- Ant-colony optimization for pathfinding

### 3. 3D Generation

**From 2D to 3D:**
```
Floor plan geometry → Extrude walls (height parameter)
                   → Add ceiling plane
                   → Place furniture from library (positioned items)
                   → Apply materials/textures
                   → Render via WebGL
```

---

## Performance Benchmarks (From Marketing)

| Task | Traditional | With Laiout |
|------|-------------|-------------|
| 800-person office layout | Days/weeks | <10 minutes |
| Early planning phase | Weeks | Single session |
| Options explored | Few | Hundreds |

---

## Export Capabilities

- **DWG** - AutoCAD native format
- **PDF** - Polished drawing packs
- **CSV** - Schedules (counts, areas)
- **Interactive links** - Shareable web viewer
- **3D snapshots** - Rendered images

---

## Pricing Model

- No public pricing (enterprise/custom)
- No free trial
- Demo required
- Contact: cristiano@laiout.co

---

## Key Takeaways for Retail Adaptation

### What to Replicate
1. Simple 4-click workflow
2. Hundreds of options generated instantly
3. Real-time metrics (adapt for retail: foot traffic, revenue/sqft, etc.)
4. Interactive stakeholder sharing
5. CAD export (critical for implementation)

### Retail-Specific Considerations
- Different optimization goals (customer flow, product visibility, impulse purchase zones)
- Planogram integration
- Fixture library vs furniture library
- Retail codes (ADA, fire egress, emergency lighting)
- Seasonal layout variations
- POS/checkout optimization

### Technology Choices
- Use Autodesk Platform Services for reliable DWG handling
- Three.js for WebGL (most documentation, largest community)
- Constraint solver + genetic algorithm hybrid
- Consider WebAssembly for performance-critical algorithms

---

## Sources

- [laiout.co](https://www.laiout.co)
- [laiout careers](https://www.laiout.co/careers)
- [AEC Magazine - Laiout enhances automated floor planning](https://aecmag.com/cad/laiout-enhances-automated-floor-planning-software/)
- [AEC+Tech - laiout profile](https://www.aecplustech.com/tools/laiout)
- [TestFit](https://www.testfit.io)
