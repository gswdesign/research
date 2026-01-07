# Floor Plan Generation Algorithms Research

## Overview of Approaches

Academic research and commercial implementations use several algorithm families for automated floor plan generation. This document summarizes key approaches relevant to retail layout optimization.

---

## 1. Constraint Programming + Genetic Optimization (Hybrid)

**Reference:** [Floor plan generation through a mixed constraint programming-genetic optimization approach](https://www.sciencedirect.com/science/article/abs/pii/S0926580520310712)

### How It Works

1. **Discretize** the floor space into a grid based on architectural constraints
2. **Reduce** problem to cell assignment (which zone owns which cell)
3. **Solve** using coupled constraint programming + genetic optimization

### Strengths
- Architecturally and functionally valid outputs
- ~1 minute generation time for typical layouts
- Handles complex constraint combinations

### Retail Application
- Define zone types (checkout, display, storage, fitting rooms)
- Set area constraints per zone
- Define adjacency requirements
- Let algorithm find valid configurations

```
Grid cells → Zone assignment → Constraint satisfaction → Genetic refinement
```

---

## 2. Evolutionary/Genetic Algorithms

**Reference:** [Evolving Floor Plans](https://www.joelsimon.net/evo_floorplans)

### How It Works

1. **Encode** layout as chromosome (zone positions, dimensions, rotations)
2. **Evaluate** fitness based on multiple objectives
3. **Select** best performers
4. **Crossover** parent solutions to create children
5. **Mutate** for diversity
6. **Repeat** for N generations

### Fitness Functions for Retail

```python
def retail_fitness(layout):
    score = 0.0

    # Customer flow efficiency (minimize walking distance)
    score += flow_score(layout) * 0.25

    # Adjacency satisfaction
    score += adjacency_score(layout) * 0.20

    # Area utilization (maximize productive floor space)
    score += area_efficiency(layout) * 0.15

    # Impulse purchase zone coverage
    score += impulse_zone_score(layout) * 0.15

    # ADA/accessibility compliance
    score += compliance_score(layout) * 0.10

    # Sightlines (visibility of key displays)
    score += sightline_score(layout) * 0.10

    # Staff efficiency (minimize travel)
    score += staff_efficiency(layout) * 0.05

    return score
```

### Key Operators

**Crossover:**
- Single-point: swap zones after random point
- Uniform: randomly pick zones from each parent
- Geometry-aware: preserve zone clusters

**Mutation:**
- Zone resize (grow/shrink within constraints)
- Zone swap (exchange positions)
- Zone rotation
- Zone displacement (small position shift)

---

## 3. Graph-Based Methods

**Reference:** [GenFloor: Interactive generative space layout system via encoded tree graphs](https://www.sciencedirect.com/science/article/pii/S2095263521000443)

### How It Works

1. **Model** zones as graph nodes
2. **Model** adjacencies as graph edges
3. **Apply** graph layout algorithms
4. **Convert** graph positions to floor plan geometry

### Algorithms
- **Graph contraction** - visually appealing layouts
- **Force-directed placement** - nodes repel, edges attract
- **Tree-based encoding** - hierarchical zone relationships

### Retail Graph Example

```
                    [ENTRANCE]
                        │
              ┌─────────┼─────────┐
              ▼         ▼         ▼
         [IMPULSE] [CHECKOUT] [MAIN FLOOR]
                        │         │
                        │    ┌────┴────┐
                        │    ▼         ▼
                        │ [DISPLAY] [DISPLAY]
                        │    │         │
                        └────┴────┬────┘
                                  ▼
                            [BACKSTOCK]
```

---

## 4. Physics-Inspired Methods

**Reference:** [Automated architectural space layout planning using a physics-inspired approach](https://arxiv.org/pdf/2406.14840)

### How It Works

1. Rooms "compete" to occupy area inside building envelope
2. Each room has a "field" that pushes against neighbors
3. Rooms adjust positions and field parameters iteratively
4. Pathway generation algorithm ensures circulation
5. NSGA-II multi-objective optimization selects best solutions

### Forces
- **Attraction**: Preferred adjacencies pull rooms together
- **Repulsion**: Non-adjacent zones push apart
- **Boundary**: Building envelope constrains expansion
- **Circulation**: Pathways create structure

---

## 5. Rule-Based/Transformation Systems

**Reference:** [Generative Design of Housing Spatial Layout Based on Rectangular Spaces](https://onlinelibrary.wiley.com/doi/10.1155/2023/1142371)

### How It Works

1. Start with bounding rectangle
2. Apply transformation rules to subdivide
3. Rules encoded from architectural best practices
4. Constraints: adjacency matrix, aspect ratios, minimum areas

### Rule Examples

```
Rule: SUBDIVIDE_HORIZONTAL
  If zone.width > 2 * zone.min_width
  Then split into two horizontal children

Rule: ASSIGN_ZONE
  If cell.adjacent_to('entrance') AND cell.near('window')
  Then cell.zone = 'checkout'

Rule: ENFORCE_CIRCULATION
  If no_path_exists(zone_a, zone_b)
  Then insert_corridor(zone_a, zone_b)
```

---

## 6. Machine Learning Approaches

### Generative Adversarial Networks (GANs)

Train on existing floor plans to generate new ones:

```
Latent vector → Generator → Fake floor plan
                    ↑
              Discriminator ← Real floor plans
```

**Challenges:**
- Requires large training dataset
- May not satisfy hard constraints
- "Hallucination" of invalid layouts

### Graph Neural Networks

Encode floor plan as graph, use GNN to predict optimal layouts:

```
Zone requirements → GNN → Predicted adjacency graph → Layout solver
```

### Reinforcement Learning

Agent learns to place zones sequentially:

```
State: Current partial layout
Action: Place next zone at position/rotation
Reward: Fitness improvement
```

---

## Algorithm Selection for Retail Layouts

### Recommended: Hybrid Constraint-Genetic Approach

**Why:**
1. Guarantees constraint satisfaction (code compliance, area requirements)
2. Explores large solution space efficiently
3. Produces diverse options for user selection
4. Well-documented in academic literature
5. Implementable without ML training data

### Implementation Priority

| Phase | Algorithm | Purpose |
|-------|-----------|---------|
| 1 | Grid discretization | Convert CAD to workable format |
| 2 | Constraint propagation | Eliminate invalid placements early |
| 3 | Genetic algorithm | Generate layout population |
| 4 | NSGA-II | Multi-objective ranking |
| 5 | Local search | Refine top solutions |

---

## Retail-Specific Considerations

### Zone Types

| Zone | Constraints | Optimization Goals |
|------|-------------|-------------------|
| Entrance | Must be at building entry | Maximize visibility, flow |
| Checkout | Near entrance, accessible | Queue capacity, impulse exposure |
| Main Floor | Largest area | Product density, customer flow |
| Fitting Rooms | Away from entrance | Privacy, staff sightlines |
| Stockroom | Near delivery, away from customer | Staff efficiency |
| Window Displays | At perimeter windows | Street visibility |

### Retail Metrics to Optimize

1. **Sales floor ratio** - productive vs. total floor area
2. **Linear feet of display** - total merchandise exposure
3. **Customer path length** - time in store → purchases
4. **Impulse zone coverage** - high-traffic areas near checkout
5. **Staff travel distance** - operational efficiency
6. **Accessibility compliance** - ADA path widths, turning radius

---

## Pseudocode: Retail Layout Generator

```python
def generate_retail_layouts(floor_plan, requirements, n_layouts=100):
    # 1. Parse and discretize
    grid = discretize(floor_plan, cell_size=0.5)  # 0.5m cells
    mark_structural_cells(grid, floor_plan.walls, floor_plan.columns)

    # 2. Initialize population
    population = []
    for _ in range(n_layouts):
        layout = random_valid_layout(grid, requirements)
        population.append(layout)

    # 3. Evolve
    for generation in range(500):
        # Evaluate fitness
        for layout in population:
            layout.fitness = evaluate_retail_fitness(layout)

        # Select parents
        parents = tournament_selection(population, k=3)

        # Crossover
        children = []
        for p1, p2 in pairs(parents):
            if random() < 0.7:
                c1, c2 = crossover(p1, p2)
                children.extend([c1, c2])

        # Mutate
        for child in children:
            if random() < 0.1:
                mutate(child)

        # Validate constraints
        children = [c for c in children if is_valid(c, requirements)]

        # Replace
        population = select_survivors(population + children, n_layouts)

    # 4. Return diverse top solutions
    pareto_front = nsga2_rank(population)
    return pareto_front[:10]
```

---

## Open Source Implementations to Study

1. **[Evolving Floor Plans](https://github.com/joelsimon/evo_floorplans)** - JavaScript evolutionary approach
2. **[PlanFinder](https://github.com/)** - Academic floor plan generation
3. **[SpaceSyntax](https://github.com/SpaceGroupUCL/depthmapX)** - Space analysis toolkit
4. **[Blueprint3D](https://github.com/furnishup/blueprint3d)** - 2D/3D floor plan editor

---

## Performance Considerations

| Operation | Typical Time | Optimization |
|-----------|--------------|--------------|
| CAD parsing | 1-5 seconds | Web Worker |
| Grid discretization | <1 second | - |
| Initial population | 1-2 seconds | Parallel generation |
| Fitness evaluation | 10-50ms/layout | WebAssembly |
| Full evolution (500 gen) | 30-60 seconds | Web Worker + WASM |
| 3D rendering | <1 second | GPU/WebGL |

**Total target: <2 minutes from upload to 100 layout options**
