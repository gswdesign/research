# London FTB Shortlist — Sub-£600k, End-2026 Purchase

Applied output of the system in `property_research/`. Methodology and evidence
are in `methodology.md`. **Seed-data demonstration — refresh with live data
before acting; not financial advice.**

The market backdrop favours you: London was **~3.3% down YoY to Feb 2026**,
forecasters expect only **+0–3% in 2026**, mortgage rates are easing
(~4.6% 2yr / ~5.7% 5yr), and **FTBs are ~50% of London buyers** — a relatively
soft, buyer-friendly entry point.

---

## How to read the rankings

Each area gets three 0-100 sub-scores and a composite:
- **Growth** — weighted *leading* signals (funded transport, affordability
  headroom, regen, gentrification momentum, yield).
- **Liveability** — current quality of place (mostly *priced-in*: schools,
  amenities, green space, existing transport, safety).
- **Risk** — cladding/EWS1, flood, oversupply/ex-LA (higher = worse; drags the
  composite).
- **Composite** — blended via your chosen `growth_tilt`, then risk-penalised.

The interesting tension: the **highest-growth** areas (Abbey Wood, Thamesmead)
are also the **highest-risk** (riverside flood, new-build flat/cladding
exposure). The model surfaces that trade-off rather than hiding it — which is
exactly the decision you have to make.

---

## Ranked output (seed data)

**Balanced** (`growth_tilt=0.5`). **Flat£ = live HM Land Registry median, to ~March 2026** (refreshed via `scripts/refresh_prices.py`):

| # | Area | Borough | Flat£ (live) | Comp | Grow | Live | Risk |
|---|------|---------|-------:|-----:|-----:|-----:|-----:|
| 1 | Walthamstow | Waltham Forest | 436k | 67.0 | 49.8 | 84.3 | 0 |
| 2 | Forest Gate | Newham | 260k | 61.4 | 60.2 | 62.7 | 0 |
| 3 | Manor Park | Newham | 230k | 59.9 | 60.1 | 59.6 | 0 |
| 4 | Leyton | Waltham Forest | 418k | 55.3 | 50.1 | 67.1 | 14 |
| 5 | Abbey Wood | Greenwich/Bexley | 255k | 54.0 | 80.3 | 54.8 | 50 |
| 6 | Ealing | Ealing | 465k | 48.7 | 22.7 | 84.5 | 23 |
| 7 | Tottenham Hale | Haringey | 316k | 48.7 | 69.6 | 67.8 | 73 |
| 8 | Bexleyheath | Bexley | 272k | 47.3 | 29.9 | 64.8 | 0 |

> **Live-data note:** Land Registry flat medians came in *below* the original
> seed estimates across east/SE London (Forest Gate £260k, Manor Park £230k,
> Abbey Wood £255k, Barking £235k) — i.e. **the best risk-adjusted areas are
> even more affordable than headline averages suggest, and sit comfortably under
> the £450k LISA cap.** Note these are flat medians; house medians are markedly
> higher (Forest Gate ~£597k, Walthamstow ~£710k, Lewisham ~£773k), so the
> "houses now above budget" caveat is real. Croydon/Nine Elms kept seed values
> (too few in-window samples for those postcode prefixes).

**Max-growth** (`growth_tilt=0.8`, risk punished harder): Forest Gate, Manor
Park, Walthamstow, **Abbey Wood**, Leyton, Dagenham, Barking, Thamesmead rise to
the top — the **funded-catalyst + low-cladding-risk** plays.

Regenerate any time with `python3 -m property_research.cli rank --preset ...`.

---

## The four theses (and which fits which buyer)

### 1. The funded-catalyst bet — **Abbey Wood / Thamesmead**
The cleanest *leading* play on the board. Elizabeth line already open **plus** the
**DLR-to-Thamesmead extension** — funded in the Nov 2025 Budget (£1.62bn, TWAO
late-2026, opening early 2030s). Layered on the **Thamesmead Waterfront "New
Town"** (15,000 homes, Peabody/Lendlease). Cheapest riverside entry in London;
live LR Abbey Wood flat median ~£255k, Thamesmead ~£256k — both well under the £450k LISA cap.
- **Top growth sub-scores (80+).** This is buying a funded-but-not-open catalyst —
  the textbook professional trade.
- **Risk to weigh:** Thames-side **flood**, **new-build flat/cladding** exposure,
  large ex-LA estates. Favour houses or long-lease resale over off-plan flats;
  verify EWS1 + flood zone. Thamesmead's weak transport *today* (low PTAL) is the
  whole point — it's the leading bet, not the arrived one.
- **Best for:** growth-tilted buyers comfortable doing cladding/flood due diligence.

### 2. The Elizabeth-line catch-up — **Manor Park & Forest Gate (Newham)**
The line is open and uplift is *mostly banked* line-wide — but these two
**lagged then caught up** (Manor Park: ~11-17% of its 10-yr gain in the last two
years; Forest Gate outperformed Newham by ~9%). Crucially: **Victorian terraces =
low cladding/oversupply risk**, so they score well on *both* growth and risk.
- **Best for:** balanced buyers who want momentum without the new-build flat
  baggage. Forest Gate/Manor Park are the model's standout risk-adjusted picks.

### 3. The arrived-but-compounding — **Walthamstow / Leyton (Waltham Forest)**
Tops the *balanced* and *home-first* rankings on **liveability** (Victoria line,
Wetlands, strong high street, gentrified). The catalyst is largely *priced in*, so
growth is momentum-driven, not catalyst-driven. Houses now breach budget; flats
fit. **Leyton** is the cheaper ripple-effect neighbour.
- **Best for:** home-first buyers prioritising somewhere genuinely nice to live now.

### 4. The deep-value entry — **Barking & Dagenham**
London's **cheapest** borough (live LR flat medians ~£235k Barking / ~£228k
Dagenham), **highest yield (~6.2%)**, Barking Riverside (10k homes, Overground
live since 2022). Dagenham house median ~£380k — about the only sub-£400k houses
left in London.
- **Risk to weigh:** ex-LA stigma, slower transport, lighter near-term catalyst.
- **Best for:** maximum budget headroom, income/yield, or wanting an actual house.

---

## Caution list (the model penalises these — and so should you)

- **Nine Elms / Vauxhall** — luxury-flat **oversupply** case study: empty units,
  multi-year listings, price cuts, ~3.5% yield. The model's bottom-ranked "what
  NOT to buy" comparator.
- **Woolwich / Royal Docks / Southall** — strong regen *but* heavy **concurrent
  new-build flat supply** (Royal Arsenal, Green Quarter ~3,750 homes) caps capital
  growth and stacks cladding risk. Be selective; resale/houses over off-plan.
- **Croydon** — cheap and high-yield, but Westfield regen is a **perpetual-delay**
  story (no planning application until mid-2026, 8+ years late). Don't pay a regen
  premium that may never arrive.
- **Old Kent Road** — £10-15bn / 20k-home regen, but its Bakerloo stations are
  **safeguarded, not funded** (~2040). A 10-15yr option, not an imminent catalyst.
- **Ealing / Acton / Hayes (West Elizabeth line)** — uplift **largely banked**,
  weak recent momentum. Great to live in (Waitrose/M&S), weak growth bet — the
  model's "arrived/priced-in" comparator.
- **Anything on a Crossrail 2 thesis** — mothballed; reassessment due late 2026.
  Do not buy on it.

**Cross-cutting flat risk:** verify **EWS1/cladding**, **lease length**, and
**service-charge history** on any flat. Post-Grenfell remediation, escalating
service charges, and short leases are actively killing flat liquidity in 2026.
This is why period houses/maisonettes screen better in the risk bucket.

---

## The FTB tax & scheme playbook (end-2026)

Run `python3 -m property_research.cli sdlt <price>` for any figure. Key facts
(regime from 1 Apr 2025 — verify at purchase):

| Threshold | Why it matters |
|---|---|
| **£300,000** | 0% SDLT up to here for FTBs. |
| **£450,000** | **LISA property cap.** Buy above and withdrawing your Lifetime ISA triggers a 25% penalty (lose the bonus + ~6.25% of your own money). |
| **£500,000** | **FTB SDLT relief cliff.** Above this you lose FTB relief *entirely* and pay standard rates on the whole price. |
| **£600,000** | Mortgage Guarantee / "Freedom to Buy" 95%-LTV cap. |

**Worked examples:**
- **£450,000:** FTB SDLT **£7,500** (vs £12,500 standard — £5,000 saved). LISA-safe.
- **£500,000:** FTB SDLT **£10,000**. Still LISA-*ineligible* (>£450k) but no SDLT cliff yet.
- **£550,000:** SDLT jumps to **£17,500** — the same as a non-FTB. Crossing £500k
  costs **£7,500 extra SDLT alone**, on top of losing the LISA bonus.

**Optimisation rules that fall straight out of this:**
1. **If you hold a LISA, cap your purchase at £450,000** to keep the bonus —
   achievable for 1-2 bed flats in Barking & Dagenham, Abbey Wood/Thamesmead,
   Dagenham, Croydon, Bexleyheath, and parts of Newham/Lewisham (`rank --lisa`).
2. **Never buy between £500k and ~£540k** — you pay full SDLT for a marginal size
   gain. Either stay at/under £500k or jump decisively higher.
3. **The £300-500k sweet spot maximises relief**, keeps the 95% scheme open, and
   covers nearly every area on the shortlist.

**Timing for end-2026:** the soft market (+0-3% forecast, prices down YoY) and
record FTB share mean **negotiating leverage is with the buyer** — lean into it.
But note end-2026 sits near a mooted LISA reform / "First-Time Buyer ISA"
consultation; confirm the cap still applies before you complete.

---

## Bottom line

For a **balanced** buyer: **Forest Gate / Manor Park** are the standout
risk-adjusted picks — Elizabeth-line catch-up momentum in low-cladding-risk
period terraces. For **maximum growth** with eyes open on risk: **Abbey
Wood/Thamesmead** (the funded-DLR catalyst). For **living there now**:
**Walthamstow / Leyton**. For **deepest value / a house / yield**: **Barking &
Dagenham**.

Keep the purchase **at or under £500k** (ideally **£450k** if you hold a LISA) to
stay tax-efficient, and treat every flat as guilty of cladding/lease/service-
charge risk until proven innocent.
