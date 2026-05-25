"""
Factor taxonomy — the single source of truth for the scoring model.

Every predictive/quality/risk factor used by the system is declared here once.
The scoring engine, the CSV schema, and the documentation all derive from this
list, so adding or re-weighting a factor is a one-line change.

Design principle (see methodology.md):
  * GROWTH factors should overweight *leading* signals (things that move BEFORE
    price: regeneration/transport pipeline at announcement stage, gentrification
    momentum, yield compression, transaction-volume and time-on-market trends).
  * "Arrived" amenities (a Waitrose, an Outstanding-school catchment, a
    conservation area) are treated as LAGGING / CONFIRMING signals. They are
    real premiums but they are already *priced in*, so they belong in the
    LIVEABILITY bucket (quality of place) and valuation accuracy, NOT in the
    growth-alpha bucket. Mistaking a confirming signal for a buy signal is the
    classic way to buy at the top.
  * RISK factors are penalties / hard filters, not growth drivers.
"""

from dataclasses import dataclass


# Buckets
GROWTH = "growth"            # predicts future appreciation
LIVEABILITY = "liveability"  # current quality of place (mostly priced-in)
RISK = "risk"                # drag / penalty / filter

# Leading vs lagging
LEADING = "leading"          # moves before price -> the alpha
LAGGING = "lagging"          # confirms an area has already arrived
STATIC = "static"            # fixed attribute (e.g. flood zone)

# Direction: does a HIGHER raw value mean a BETTER (higher) score?
UP = "higher_is_better"
DOWN = "lower_is_better"

# Evidence strength of the factor's link to price growth (from the research).
STRONG = "strong"
MODERATE = "moderate"
WEAK = "weak"


@dataclass(frozen=True)
class Factor:
    key: str            # must match the column name in data/areas.csv
    label: str
    bucket: str         # GROWTH | LIVEABILITY | RISK
    lead_lag: str       # LEADING | LAGGING | STATIC
    direction: str      # UP | DOWN
    evidence: str       # STRONG | MODERATE | WEAK
    default_weight: float
    scale_hint: str     # human note on the raw input scale
    rationale: str      # why it's in the model and how to read it


FACTORS = [
    # ---------------- GROWTH: leading signals (the alpha) ----------------
    Factor(
        "afford_headroom", "Affordability headroom", GROWTH, LEADING, UP, STRONG, 1.4,
        "0-100. Derived: how far BELOW the London avg price-to-earnings this area "
        "sits (cheap relative to incomes = more room to rise). Auto-computed from "
        "price_to_earnings if left blank.",
        "Interest-rate-adjusted affordability is the best-evidenced macro driver "
        "(BoE/IMF). Cheap-relative-to-income areas have the most catch-up room as "
        "the ripple effect pushes growth outward from hot zones.",
    ),
    Factor(
        "infra_pipeline", "Transport pipeline (committed/announced)", GROWTH, LEADING, UP, STRONG, 1.5,
        "0-5. Strength + certainty of NEW transport coming (5 = transformational & "
        "funded, e.g. a new Elizabeth-line-class link; 0 = nothing in pipeline).",
        "Transport uplift (6-14% for Crossrail station postcodes; >50% for the "
        "Jubilee extension historically) capitalises FROM ANNOUNCEMENT, years "
        "before opening. The announcement is the trade, not the ribbon-cutting.",
    ),
    Factor(
        "regen_pipeline", "Regeneration / Opportunity Area pipeline", GROWTH, LEADING, UP, MODERATE, 1.2,
        "0-5. Scale + maturity of committed regeneration (GLA Opportunity Area "
        "status, large consented housing/jobs pipeline, brownfield delivery).",
        "Large regen schemes reshape an area's price ceiling. Best read alongside "
        "planning_momentum so you catch it while consented but not yet built out.",
    ),
    Factor(
        "planning_momentum", "Planning-application momentum", GROWTH, LEADING, UP, WEAK, 0.7,
        "0-5. Rate-of-change of planning activity (conversions, extensions, new "
        "units) vs the area's baseline. Refreshable from planning.data.gov.uk.",
        "Logically leading and cheap to measure, but under-validated in UK "
        "literature — keep weight modest and backtest before trusting.",
    ),
    Factor(
        "gentrification_momentum", "Gentrification momentum (rate-of-change)", GROWTH, LEADING, UP, MODERATE, 1.1,
        "0-5. Composite of CHANGE signals: new independent F&B / business "
        "formation rate, demographic shift (rising education/occupation mix), "
        "renovation activity. Measured as acceleration, not level.",
        "The London F&B event-study finds ~3.4-3.7% cumulative uplift over 4-5yrs "
        "after new food/drink entry — but siting is endogenous, so use the RATE "
        "of new openings, not the mere presence of cafes.",
    ),
    Factor(
        "rent_growth", "Private-rent growth (5yr)", GROWTH, LEADING, UP, MODERATE, 0.9,
        "% cumulative private-rent growth over ~5yr.",
        "Rents reprice faster than the sticky sale market; rent strength ahead of "
        "sale prices is a classic (if under-formalised) leading indicator.",
    ),
    Factor(
        "gross_yield", "Gross rental yield", GROWTH, LEADING, UP, MODERATE, 0.9,
        "% gross yield. HIGH yield = relatively cheap capital value = value + "
        "income cushion; yield compression later confirms capital catching up.",
        "High/rising yield flags value; falling yield (compression) is a "
        "late-cycle 'capital getting ahead' signal. Outer/east London leads on yield.",
    ),
    Factor(
        "price_momentum_3yr", "Recent price momentum (3yr)", GROWTH, LAGGING, UP, MODERATE, 0.6,
        "% price growth over ~3yr.",
        "Momentum persists short-term but is partly lagging — keep modest so you "
        "don't simply chase what already ran.",
    ),
    Factor(
        "volume_trend", "Transaction volume & time-on-market trend", GROWTH, LEADING, UP, MODERATE, 0.8,
        "-2..+2. Rising transaction volumes / falling days-to-sell / shrinking "
        "asking-vs-sold discount = +2; the reverse = -2.",
        "Volumes and liquidity lead prices; mortgage approvals lead closed sales "
        "by ~30-60 days. Best early read on demand turning.",
    ),

    # ---------------- LIVEABILITY: mostly priced-in / confirming ----------------
    Factor(
        "ptal", "Transport access now (PTAL)", LIVEABILITY, LAGGING, UP, STRONG, 1.0,
        "0-8 numeric mapping of TfL PTAL (0=worst, 6b=best mapped to 8).",
        "Existing accessibility is largely capitalised already — quality-of-life "
        "and valuation input, not growth alpha (the NEW link is the alpha).",
    ),
    Factor(
        "mins_to_central", "Journey time to central London", LIVEABILITY, LAGGING, DOWN, MODERATE, 0.7,
        "Typical minutes to a central hub (e.g. Bank/Oxford Circus).",
        "Commute time underpins demand depth. Lower is better.",
    ),
    Factor(
        "schools", "School quality / catchment", LIVEABILITY, LAGGING, UP, STRONG, 0.9,
        "0-5. Density of Good/Outstanding Ofsted catchments.",
        "Outstanding catchments command ~7-13% premiums (ONS) — strongly "
        "evidenced but already priced in. The GROWTH event is a rating UPGRADE.",
    ),
    Factor(
        "amenity_supermarket", "Premium-grocer / amenity tier", LIVEABILITY, LAGGING, UP, WEAK, 0.5,
        "0-4: 4=Waitrose/M&S Food, 3=Sainsbury's, 2=Tesco, 1=Aldi/Lidl, 0=none.",
        "The 'Waitrose effect' (~12%, +£43.5k) is REAL but a CONFIRMING marker — "
        "the grocer's site team opened where money already is. Low weight; a "
        "*newly announced* budget grocer in a cheap area is the weak leading nuance.",
    ),
    Factor(
        "amenity_highstreet", "High-street / F&B amenity level", LIVEABILITY, LAGGING, UP, WEAK, 0.5,
        "0-5. Current depth/quality of high street, restaurants, gyms.",
        "Quality-of-life input. The LEVEL is confirming; the rate-of-change lives "
        "in gentrification_momentum.",
    ),
    Factor(
        "greenspace", "Green / blue space & conservation", LIVEABILITY, STATIC, UP, MODERATE, 0.6,
        "0-5. Parks/river proximity and conservation-area coverage.",
        "Green space ~1-2% premium; conservation areas ~9% (LSE/Historic England) "
        "with spillover. Stable amenity premium — valuation, not growth timing.",
    ),
    Factor(
        "safety", "Safety (inverse crime rate)", LIVEABILITY, LAGGING, DOWN, MODERATE, 0.7,
        "Crime rate per 1,000 residents (LOWER is better). Refreshable from "
        "data.police.uk.",
        "Crime carries ~-1% to -3% per increment, sharply distance-decayed. "
        "Improving (falling) crime is the leading version of this signal.",
    ),

    # ---------------- RISK: penalties / hard filters ----------------
    Factor(
        "risk_cladding", "Cladding / EWS1 high-rise exposure", RISK, STATIC, DOWN, STRONG, 1.6,
        "0-3: 0=none (houses/low-rise), 3=high exposure (post-2000 high-rise flat stock).",
        "The biggest NEW drag: 'red' EWS1 buildings saw -24% to -33% prices and "
        "67-85% volume collapse; many flats unsaleable. Treat as a hard risk flag.",
    ),
    Factor(
        "risk_flood", "Flood risk", RISK, STATIC, DOWN, MODERATE, 1.0,
        "0-3 flood exposure (Environment Agency zones).",
        "~8% average discount for flood-affected stock, worsening with climate "
        "repricing and insurance cost.",
    ),
    Factor(
        "risk_oversupply_exla", "New-build glut / ex-LA / leasehold drag", RISK, STATIC, DOWN, MODERATE, 0.9,
        "0-3 composite: flat oversupply (e.g. Nine Elms-type glut), ex-local-"
        "authority stigma, high service-charge / short-lease exposure.",
        "Ex-LA ~20% discount AND weaker appreciation; new-build premium decays; "
        "service-charge escalation erodes value. A genuine growth drag.",
    ),
]


# --- convenience lookups ---
FACTORS_BY_KEY = {f.key: f for f in FACTORS}
GROWTH_FACTORS = [f for f in FACTORS if f.bucket == GROWTH]
LIVEABILITY_FACTORS = [f for f in FACTORS if f.bucket == LIVEABILITY]
RISK_FACTORS = [f for f in FACTORS if f.bucket == RISK]


def factor_keys():
    return [f.key for f in FACTORS]
