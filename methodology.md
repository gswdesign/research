# How Professionals Predict Residential Price Growth — and How This System Encodes It

This is the research foundation behind the tooling in `property_research/`. It
answers your core question: *what actually makes a good prediction — quantitative,
qualitative, future tube stops, the Waitrose effect, or what?*

Short answer: **all of them, but in a specific hierarchy.** The single most
important distinction the pros make — and the one amateurs get wrong — is
**leading vs lagging signals**. A Waitrose, an Outstanding school, an open
Elizabeth line station are *real* price premiums, but they are **already priced
in**. They tell you an area has *arrived*, not that it's about to move. The alpha
is in signals that move *before* price.

---

## 1. The professional workflow (top-down, then bottom-up)

Forecasters like **Savills** and **Knight Frank** build a **top-down macro
forecast, then disaggregate**:

1. Take an independent macro baseline (consensus / Oxford Economics) for **base
   rate, mortgage rates, wage growth, GDP, inflation**.
2. Translate it into a national **affordability / borrowing-capacity** path.
3. Allocate growth across regions and price tiers using a **housing-cycle**
   framework, then rebase quarterly against actual rate moves.

Current published view (late-2025 / early-2026): UK mainstream **~17-24%
cumulative to 2029/30**, but **Greater London only ~13-15%** (affordability-
capped), and **Prime Central London ~8%** off a low base after a *decade* of
stagnation. The cycle currently favours **affordable outer/regional** markets
over prime — directly relevant to a sub-£600k FTB.

Quant desks (lenders' AVMs, BTL funds) then go **bottom-up** at the
postcode/LSOA level using the factor model below.

---

## 2. The factor model — what actually drives growth

### Macro / fundamental (drives ~80% of *regional* forecast variance)
- **Interest-rate-adjusted affordability** — the *best-evidenced* driver. A BoE
  working paper attributes nearly all the 1985-2018 real house-price rise to the
  sustained fall in real rates. Model the **mortgage payment as a % of income**,
  not just headline price-to-earnings (England ~7.5-8x; London ~10.6x).
- **Mortgage credit availability** — IMF: +10pp mortgage-credit/GDP ≈ +16pp real
  house-price growth. The relaxation of the 6.5% stress test is a live 2025-29
  tailwind.
- **Wages, employment, supply** (net delivery vs household formation).

### Local / micro (drives *relative* outperformance within a region)
Strength-of-evidence ranking (from the research):

| Signal | Evidence | Lead/Lag | Magnitude |
|---|---|---|---|
| **New transport (announced)** | Strong | **Leading** | 6-14% (Crossrail stations); >50% (Jubilee ext.) — capitalises *from announcement* |
| Affordability headroom / ripple proximity | Strong | Leading | catch-up to adjacent hot areas |
| School catchment (Outstanding) | Strong | **Lagging** | +7-13% — but priced in |
| Conservation area | Strong | Static | +9% (+spillover ~3% within 600m) |
| Crime (per increment) | Strong | Lagging | −1% to −3%, distance-decayed |
| New food/drink openings (*rate*) | Moderate | Leading | +3.4-3.7% cumulative over 4-5yr (siting is endogenous) |
| Green/blue space | Moderate | Static | +1-2% |
| **Supermarket ("Waitrose effect")** | Weak-Moderate | **Lagging** | +~12% / +£43.5k — *confirming, not causal* |
| Craft breweries, cycle lanes, gyms | Weak / folklore | — | no credible causal evidence |

### Risk / drag (penalties — often the most quantifiable)
- **Cladding / EWS1** (post-Grenfell): "red" buildings −24% to −33%, volumes
  −67-85%, many flats unsaleable. The biggest *new* drag — a **hard filter**.
- **Flood risk**: ~−8% and worsening with climate repricing.
- **Ex-local-authority** stigma: ~−20% *and* weaker appreciation.
- **New-build flat oversupply** (Nine Elms-type glut): caps capital growth.

---

## 3. Quantitative techniques the pros use

- **Hedonic regression** — decomposes price into implicit prices of attributes
  (floor area, beds, type, location, EPC). Underpins the ONS UK HPI and first-gen
  AVMs.
- **Repeat-sales indices** (Case-Shiller style) — track the *same* property
  across sales to strip out quality/composition (HM Land Registry's index).
- **Mix-adjustment** — reweights monthly transactions to a fixed property mix.
- **ML AVMs** — modern automated valuation models (Hometrack, used by 17 of the
  top-20 UK lenders; Rightmove and Zoopla each run their own) use **gradient-
  boosted trees / random forests**, outputting an estimate + a **confidence
  band**. Lenders gate decisions on that confidence score.
- **Spatial / ripple-effect modelling** — a well-evidenced UK phenomenon: shocks
  start in London/SE and **diffuse outward with a lag**. Used to time regional and
  intra-London bets (when a hot zone slows, the adjacent cheaper one catches up).

**This system is deliberately *not* a black-box ML model.** With ~20 areas and
heterogeneous public data, a transparent **weighted, normalised, multi-factor
score** is more honest and more *tunable* than an overfit regression. The ML
techniques above are what you'd graduate to once you've joined Land Registry ↔
EPC into a 100k+ row training set (see §6).

---

## 4. Leading vs lagging — the heart of it

> **Lagging/confirming (use for valuation & risk, low growth weight):** existing
> premium supermarket, existing Outstanding-school catchment, conservation area,
> open transport line, green space. These say an area *has arrived*.

> **Leading (where the alpha is):** committed/announced new transport;
> affordability headroom + ripple proximity; **rate-of-change** of new
> business/F&B formation; private-rent growth outpacing sale prices; Census
> demographic shift; planning-application momentum; school-rating *upgrades*;
> falling crime; rising transaction volumes / shrinking days-to-sell.

> **Persistent negative flags (risk filter):** cladding/EWS1 high-rise, flood
> zone, ex-LA, oversupply glut.

Concrete answers to your specific questions:

- **Future tube stops or reliable existing ones?** *Future, but only funded
  ones.* The uplift capitalises at **announcement**, not opening — so by the time
  a line opens it's largely banked (Elizabeth line West London: ~50-58% gains,
  now weak momentum). The trade is buying a **funded-but-not-open** catalyst. As
  of 2026 that means **DLR-to-Thamesmead** (funded Nov 2025, ~£1.62bn, opening
  early 2030s) — *not* Bakerloo extension (~2040, unfunded) or Crossrail 2
  (mothballed, reassessment due late 2026). Don't pay a premium today for an
  unfunded 15-year option.
- **Waitrose / M&S effect?** Real (~12%, +£43.5k) but it's a **lagging
  confirmation** — the grocer's site-selection team opened where the money
  *already is*. Weight it low and treat it as a *quality* signal, not a buy
  signal. The only leading nuance: a *newly announced* budget grocer (Aldi/Lidl)
  in a currently-cheap area.
- **Purely quantitative or qualitative too?** Both — but qualitative signals are
  only useful as **change/rate** measures (new-business *formation rate*, rent-
  to-price *divergence*, demographic *shift*), not as levels. Levels are already
  in the price.

---

## 5. How the scoring model encodes all this

`property_research/factors.py` is the single source of truth. Every factor is
tagged with **bucket** (growth / liveability / risk), **lead_lag**, **evidence
strength**, **direction**, and a **default weight**. The engine
(`scoring.py`):

1. Min-max normalises each factor across the area set to 0-100 (inverting
   "lower-is-better" factors).
2. Weighted-averages within each bucket → **growth_score**, **liveability_score**,
   **risk_score**.
3. Blends growth + liveability via a tunable **growth_tilt** (0 = pure
   liveability … 1 = pure growth).
4. Applies a tunable **risk penalty** so cladding/flood/oversupply drag the
   composite down.

Design choices that fall straight out of the research:
- **Leading growth factors carry the highest default weights** (transport
  pipeline 1.5, affordability headroom 1.4, regen 1.2, gentrification momentum
  1.1). The Waitrose factor is deliberately weak (0.5) and sits in *liveability*,
  not *growth*.
- **Cladding risk is the single heaviest risk weight (1.6)** — it's the biggest
  modern value-killer and the most quantifiable.
- Everything is overridable via `data/weights.default.json` or the presets
  (`balanced`, `max-growth`, `home-first`) so you can flex the model's
  personality, exactly as you asked.

---

## 6. Roadmap to a "real" quant pipeline

The current dataset is a **curated seed** (illustrative values from the 2025-26
research, refreshable via the open clients in `datasources.py`). To industrialise:

1. **Join HM Land Registry Price Paid ↔ EPC on address** → gives **£/m²**, the
   single most comparable price metric and the input for proper hedonic models.
2. Pull **leading features programmatically**: planning.data.gov.uk
   (planning_momentum, conservation, regen), data.police.uk (safety trend), ONS
   Private Rents (rent_growth + yield), Census 2021 (demographic shift).
3. **Backtest** the under-evidenced leading signals (rents-lead-prices, planning
   density, F&B formation rate) on your own 2015-2025 Land Registry panel before
   trusting their weights — the literature flags these as plausible but
   unvalidated.
4. Graduate to **gradient-boosted trees** for £/m² prediction once you have the
   joined dataset, keeping this transparent score as the *interpretable overlay*.

---

## Key sources

**Forecasts & methodology**
- Savills mainstream forecasts 2025-2029/30 — savills.co.uk/research_articles/229130/379365-0
- Knight Frank UK Housing Market Forecast (Sept 2025) — knightfrank.co.uk/research
- ONS — single official UK House Price Index methodology — ons.gov.uk
- BoE / IMF affordability & credit evidence (via en.wikipedia.org/wiki/Affordability_of_housing_in_the_United_Kingdom)
- Ripple effect: ScienceDirect S0094119010000501; Emerald ijhma-09-2023-0118
- AVMs / gradient boosting: en.wikipedia.org/wiki/Automated_valuation_model; T&F 10.1080/09599916.2022.2070525

**Local-factor evidence**
- Crossrail Property Impact Study — learninglegacy.crossrail.co.uk
- School catchment premiums (ONS via pauzible.com); conservation areas (LSE/Historic England)
- Crime: Springer s11146-024-09997-w
- "Waitrose effect": Lloyds Bank (loveproperty.com / henleystandard.co.uk)
- Food/drink entry event-study: arXiv 2603.03260 (siting endogeneity caveat)
- Green/blue space: ONS hedonic ML study
- Cladding/EWS1: House of Commons Library CBP-10763; flood: Bayes Business School 2023

**Data sources** — see `property_research/datasources.py` for the full machine-
readable catalog with endpoints.
