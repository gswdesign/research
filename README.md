# UK Property Growth Research System — London FTB Edition

A transparent, tunable system for predicting residential price growth and
shortlisting London areas for a **first-time buyer with a £300k–£600k budget,
targeting an end-2026 purchase**.

It encodes how professional forecasters actually work (see **`methodology.md`**):
a multi-factor score that separates **leading** signals (where the growth alpha
is) from **lagging/confirming** ones (the Waitrose, the open tube line, the
Outstanding school — real premiums, but already priced in), plus a risk penalty
for the modern value-killers (cladding/EWS1, flood, oversupply).

Pure Python standard library — **no installs required**.

## Documents
| File | What it is |
|---|---|
| `methodology.md` | The research: how pros predict growth, the factor model, leading vs lagging, the Waitrose/tube logic, data sources. **Read this first.** |
| `london-shortlist.md` | The applied analysis: ranked sub-£600k London areas + the FTB tax/scheme playbook for end-2026. |
| `README.md` | This file — how to run the tooling. |

## The tooling

```
property_research/
  factors.py      # factor taxonomy — the single source of truth (edit to add/retag factors)
  scoring.py      # the tunable scoring engine (normalise -> weight -> blend -> risk penalty)
  config.py       # weight presets: balanced | max-growth | home-first  (+ JSON loader)
  sdlt.py         # first-time-buyer SDLT + LISA/Mortgage-Guarantee calculator
  datasources.py  # open-data CATALOG + runnable clients (Land Registry, Police.uk, planning.data.gov.uk)
  cli.py          # command-line interface
data/
  areas.csv            # 20 seeded London areas (refreshable via datasources)
  weights.default.json # copy + edit to fully customise the model
tests/
  test_system.py       # sanity checks (SDLT worked examples, scoring invariants)
```

## Quick start

```bash
# Rank areas (balanced weighting)
python3 -m property_research.cli rank --preset balanced --top 10

# Optimise for capital growth, or for living there
python3 -m property_research.cli rank --preset max-growth
python3 -m property_research.cli rank --preset home-first

# Constrain to your budget / keep the LISA bonus (flats <= £450k)
python3 -m property_research.cli rank --max-flat 500000 --max-house 600000
python3 -m property_research.cli rank --lisa

# Why did an area score that way? Per-factor breakdown (with lead/lag + evidence)
python3 -m property_research.cli explain "Abbey Wood" --preset max-growth

# First-time-buyer cost + scheme warnings for a price
python3 -m property_research.cli sdlt 450000
python3 -m property_research.cli sdlt 550000     # shows the £500k cliff + LISA penalty

# The data-source catalog (factor <- dataset map)
python3 -m property_research.cli sources

# Live-pull open data for an area (needs network egress)
python3 -m property_research.cli refresh "Abbey Wood" --month 2026-01

# Run the tests
python3 tests/test_system.py
```

## Tuning the model

Three ways, increasing in power:

1. **Presets** — `--preset balanced|max-growth|home-first`.
2. **A custom JSON** — copy `data/weights.default.json`, edit, pass with
   `--config myweights.json`. Set per-factor weights, the `growth_tilt`
   (0 = pure liveability … 1 = pure growth), and `risk_penalty_strength`.
3. **The factor taxonomy** — edit `property_research/factors.py` to add a factor,
   change its bucket/weight, or retag leading vs lagging. The CSV column name
   must match the factor `key`.

## Updating the data

`data/areas.csv` ships with **curated seed values** from the 2025-26 research
(see the `notes` column and `methodology.md`). They're illustrative — refresh
them with live open data via `datasources.py`:

- `police_crime_count(lat, lon, "2026-01")` → the `safety` factor (no key)
- `land_registry_recent_sales("SE2 9XY")` → price inputs (full postcode, no key)
- `planning_entities(dataset="conservation-area")` → regen/planning signals (no key)

EPC, ONS, TfL PTAL, Ofsted and Census are documented in the catalog (`cli.py
sources`) — wire them in as you scale toward the joined Land-Registry↔EPC
pipeline described in `methodology.md` §6.

## Important caveats

- The seed dataset is **illustrative**, not a live valuation. Treat the rankings
  as a *framework demonstration* and refresh with real data before acting.
- Tax rules (SDLT bands, the £450k LISA cap, the Mortgage Guarantee scheme)
  reflect the **regime from 1 April 2025** and mooted end-2026 reforms — **verify
  at point of purchase** with a solicitor/IFA.
- This is a research aid, **not financial advice**.
