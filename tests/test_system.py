"""Plain-stdlib sanity tests. Run: python3 tests/test_system.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from property_research import config, scoring, sdlt
from property_research import factors as F

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "areas.csv")


def check(name, cond):
    print(("PASS" if cond else "FAIL") + "  " + name)
    assert cond, name


def test_sdlt():
    # Worked examples verified against HMRC FTB rules (from 1 Apr 2025).
    check("FTB SDLT @300k == 0", sdlt.ftb_sdlt(300_000) == 0)
    check("FTB SDLT @450k == 7500", sdlt.ftb_sdlt(450_000) == 7_500)
    check("FTB SDLT @500k == 10000", sdlt.ftb_sdlt(500_000) == 10_000)
    check("FTB relief lost >500k == standard", sdlt.ftb_sdlt(550_000) == sdlt.standard_sdlt(550_000))
    check("Standard SDLT @550k == 17500", sdlt.standard_sdlt(550_000) == 17_500)
    r = sdlt.assess(550_000)
    check("cliff warning fires 500-550k", bool(r.cliff_warning))
    check("LISA ineligible >450k", not sdlt.assess(460_000).lisa_eligible)
    check("LISA eligible <=450k", sdlt.assess(450_000).lisa_eligible)


def test_factor_csv_alignment():
    import csv
    with open(DATA, newline="", encoding="utf-8") as fh:
        cols = set(next(csv.reader(fh)))
    missing = [f.key for f in F.FACTORS if f.key not in cols and f.key != "afford_headroom"]
    check("every factor (bar derived afford_headroom) has a CSV column", not missing)


def test_scoring():
    areas = scoring.load_areas(DATA)
    ranked = scoring.score(areas, config.BALANCED)
    check("all areas loaded", len(ranked) == 20)
    check("scores in 0..100", all(0 <= a.composite <= 100 for a in ranked))
    check("ranking is sorted desc", all(ranked[i].composite >= ranked[i+1].composite for i in range(len(ranked)-1)))
    # Tilt changes the order: growth-tilt should rank Abbey Wood (huge growth) higher than under liveability tilt.
    g = scoring.score(scoring.load_areas(DATA), config.MAX_GROWTH)
    l = scoring.score(scoring.load_areas(DATA), config.HOME_FIRST)
    aw_g = next(i for i, a in enumerate(g) if a.name == "Abbey Wood")
    aw_l = next(i for i, a in enumerate(l) if a.name == "Abbey Wood")
    check("growth tilt ranks Abbey Wood higher than home-first tilt", aw_g <= aw_l)
    # Nine Elms (oversupply) should carry high risk.
    ne = next(a for a in ranked if a.name == "Nine Elms")
    check("Nine Elms flagged high risk", ne.risk_score >= 50)


if __name__ == "__main__":
    test_sdlt()
    test_factor_csv_alignment()
    test_scoring()
    print("\nAll checks passed.")
