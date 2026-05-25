"""
First-time-buyer cost calculator for England (SDLT) + scheme eligibility flags.

Rules encoded reflect the regime in force from 1 April 2025 (verify at point of
purchase; an end-2026 purchase sits near mooted LISA-reform dates).

Stamp Duty Land Tax (FTB relief, from 1 Apr 2025):
    * 0% on the portion up to £300,000
    * 5% on the portion £300,001-£500,000
    * If the purchase price is OVER £500,000, FTB relief is LOST ENTIRELY and
      standard residential rates apply to the whole price.

Standard residential SDLT bands (also used above the £500k FTB cap):
    * 0%  up to £125,000
    * 2%  £125,001-£250,000
    * 5%  £250,001-£925,000
    * 10% £925,001-£1,500,000
    * 12% above £1,500,000

Scheme caps (end-2026):
    * Lifetime ISA (LISA): 25% bonus, but property price cap of £450,000 —
      buying above this triggers a 25% withdrawal penalty (you lose the bonus
      plus ~6.25% of your own contributions).
    * Mortgage Guarantee / "Freedom to Buy": now permanent, 95% LTV, homes up
      to £600,000.
"""

from dataclasses import dataclass, field

FTB_NIL_BAND = 300_000
FTB_RELIEF_CAP = 500_000      # above this, no FTB relief at all
FTB_REDUCED_RATE = 0.05       # 300k-500k portion

LISA_PRICE_CAP = 450_000
MORTGAGE_GUARANTEE_CAP = 600_000

STANDARD_BANDS = [
    (125_000, 0.00),
    (250_000, 0.02),
    (925_000, 0.05),
    (1_500_000, 0.10),
    (float("inf"), 0.12),
]


def standard_sdlt(price):
    tax, last = 0.0, 0.0
    for threshold, rate in STANDARD_BANDS:
        if price > last:
            taxable = min(price, threshold) - last
            tax += taxable * rate
            last = threshold
        else:
            break
    return round(tax, 2)


def ftb_sdlt(price):
    """SDLT for an eligible first-time buyer."""
    if price > FTB_RELIEF_CAP:
        return standard_sdlt(price)  # relief lost -> standard rates on full price
    tax = 0.0
    if price > FTB_NIL_BAND:
        tax += (min(price, FTB_RELIEF_CAP) - FTB_NIL_BAND) * FTB_REDUCED_RATE
    return round(tax, 2)


@dataclass
class FtbCostResult:
    price: float
    ftb_sdlt: float
    standard_sdlt: float
    ftb_relief_saving: float
    over_ftb_cap: bool
    cliff_warning: str = ""
    lisa_eligible: bool = True
    lisa_warning: str = ""
    mortgage_guarantee_eligible: bool = True
    notes: list = field(default_factory=list)


def assess(price):
    f = ftb_sdlt(price)
    s = standard_sdlt(price)
    r = FtbCostResult(
        price=price,
        ftb_sdlt=f,
        standard_sdlt=s,
        ftb_relief_saving=round(s - f, 2),
        over_ftb_cap=price > FTB_RELIEF_CAP,
        lisa_eligible=price <= LISA_PRICE_CAP,
        mortgage_guarantee_eligible=price <= MORTGAGE_GUARANTEE_CAP,
    )

    # Cliff edge: just above £500k you both lose relief AND jump bands.
    if FTB_RELIEF_CAP < price <= 550_000:
        at_cap = ftb_sdlt(FTB_RELIEF_CAP)  # £10,000 at exactly £500k
        r.cliff_warning = (
            f"CLIFF EDGE: at £500,000 an FTB pays £{at_cap:,.0f}; at £{price:,.0f} "
            f"you pay £{f:,.0f} (relief lost). Pushing the price down to £500,000 "
            f"saves £{f - at_cap:,.0f} in SDLT alone."
        )
        r.notes.append(r.cliff_warning)

    if not r.lisa_eligible:
        r.lisa_warning = (
            f"LISA penalty: price £{price:,.0f} exceeds the £{LISA_PRICE_CAP:,.0f} "
            f"cap. Withdrawing the LISA to buy triggers a 25% penalty (you lose the "
            f"government bonus + ~6.25% of your own money). Stay <= £{LISA_PRICE_CAP:,.0f} "
            f"to keep the bonus."
        )
        r.notes.append(r.lisa_warning)

    if not r.mortgage_guarantee_eligible:
        r.notes.append(
            f"Above the £{MORTGAGE_GUARANTEE_CAP:,.0f} Mortgage Guarantee / "
            f"'Freedom to Buy' 95% LTV cap."
        )

    return r


# Useful planning thresholds for an FTB optimising around the rules.
KEY_THRESHOLDS = {
    "lisa_cap": LISA_PRICE_CAP,
    "ftb_relief_cap": FTB_RELIEF_CAP,
    "mortgage_guarantee_cap": MORTGAGE_GUARANTEE_CAP,
}
