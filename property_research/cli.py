"""
Command-line interface.

  python -m property_research.cli rank [--preset balanced|max-growth|home-first]
                                       [--config FILE] [--top N]
                                       [--max-flat 500000] [--max-house 600000]
                                       [--lisa] [--ftb-cap]
  python -m property_research.cli explain "Abbey Wood" [--preset ...]
  python -m property_research.cli sdlt 450000
  python -m property_research.cli sources
  python -m property_research.cli refresh "Abbey Wood" [--month 2026-01]
"""

import argparse
import os

from . import config as cfg
from . import datasources, scoring, sdlt
from . import factors as F

DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "areas.csv")


def _load_config(args):
    if getattr(args, "config", None):
        return cfg.load(path=args.config)
    return cfg.load(preset=getattr(args, "preset", "balanced"))


def _passes_budget(area, args):
    flat = area.meta.get("avg_flat_price")
    house = area.meta.get("avg_house_price")
    if args.max_flat and flat and flat > args.max_flat:
        # only fails if there is ALSO no house under the house cap
        if not (args.max_house and house and 0 < house <= args.max_house):
            return False
    if args.max_house and house and house > args.max_house and not (
        args.max_flat and flat and 0 < flat <= args.max_flat
    ):
        # both over their caps -> drop
        if args.max_flat and flat and flat > args.max_flat:
            return False
    return True


def cmd_rank(args):
    config = _load_config(args)
    areas = scoring.load_areas(DATA)
    ranked = scoring.score(areas, config)

    if args.max_flat or args.max_house:
        ranked = [a for a in ranked if _passes_budget(a, args)]
    if args.lisa:
        ranked = [a for a in ranked if (a.meta.get("avg_flat_price") or 1e9) <= sdlt.LISA_PRICE_CAP]

    tilt = config.get("growth_tilt")
    print(f"\nPreset/tilt: growth_tilt={tilt}  risk_penalty={config.get('risk_penalty_strength')}")
    print(f"(growth_tilt 0=liveability .. 1=growth)\n")
    hdr = f"{'#':>2}  {'Area':<16}{'Borough':<20}{'Flat£':>8}{'Comp':>6}{'Grow':>6}{'Live':>6}{'Risk':>6}"
    print(hdr)
    print("-" * len(hdr))
    for i, a in enumerate(ranked[: args.top], 1):
        flat = a.meta.get("avg_flat_price")
        flat_s = f"{flat/1000:.0f}k" if flat else "-"
        print(f"{i:>2}  {a.name:<16}{a.borough[:19]:<20}{flat_s:>8}"
              f"{a.composite:>6.1f}{a.growth_score:>6.1f}{a.liveability_score:>6.1f}{a.risk_score:>6.1f}")
    print("\nComp=composite (after risk)  Grow/Live=0-100 sub-scores  Risk=0-100 (higher=worse)")
    print("Use 'explain \"<Area>\"' for the per-factor breakdown.\n")


def cmd_explain(args):
    config = _load_config(args)
    areas = scoring.load_areas(DATA)
    scoring.score(areas, config)
    match = next((a for a in areas if a.name.lower() == args.area.lower()), None)
    if not match:
        print(f"Area '{args.area}' not found. Options: {', '.join(a.name for a in areas)}")
        return
    print(f"\n=== {match.name} ({match.borough}) ===")
    print(f"composite={match.composite}  growth={match.growth_score}  "
          f"liveability={match.liveability_score}  risk={match.risk_score}")
    notes = match.meta.get("notes")
    if notes:
        print(f"note: {notes}")
    print(f"\n{'factor':<26}{'bucket':<12}{'lead/lag':<9}{'evid':<9}{'raw':>7}{'norm':>7}{'wt':>6}")
    print("-" * 76)
    for r in scoring.explain(match, config):
        raw = r["raw"]
        raw_s = f"{raw:.1f}" if isinstance(raw, (int, float)) else "-"
        flag = "*" if r["imputed"] else ""
        print(f"{r['label'][:25]:<26}{r['bucket']:<12}{r['lead_lag']:<9}{r['evidence']:<9}"
              f"{raw_s:>7}{r['normalised']:>7.0f}{r['weight']:>6.1f}{flag}")
    print("\n* = value was missing and imputed to the column median.\n")


def cmd_sdlt(args):
    r = sdlt.assess(args.price)
    print(f"\nFirst-time-buyer cost @ £{r.price:,.0f}")
    print(f"  FTB SDLT          : £{r.ftb_sdlt:,.0f}")
    print(f"  Standard SDLT     : £{r.standard_sdlt:,.0f}")
    print(f"  FTB relief saving : £{r.ftb_relief_saving:,.0f}")
    print(f"  LISA eligible     : {'yes' if r.lisa_eligible else 'NO (>£450k)'}")
    print(f"  95% guarantee     : {'yes' if r.mortgage_guarantee_eligible else 'NO (>£600k)'}")
    for n in r.notes:
        print(f"  ! {n}")
    print()


def cmd_sources(args):
    print("\nDATA SOURCE CATALOG (factor <- dataset map)\n")
    datasources.print_catalog()
    print()


def cmd_refresh(args):
    areas = scoring.load_areas(DATA)
    match = next((a for a in areas if a.name.lower() == args.area.lower()), None)
    if not match:
        print(f"Area '{args.area}' not found.")
        return
    lat = scoring._to_float(match.meta.get("lat"))
    lon = scoring._to_float(match.meta.get("lon"))
    pc = match.meta.get("postcode_district")
    print(f"\nLive pull for {match.name} (lat={lat}, lon={lon}, pc={pc})")
    print("  (returns empty if the environment's network policy blocks egress)\n")
    counts, note = datasources.police_crime_count(lat, lon, args.month)
    print(f"  police.uk crime: {note}")
    for cat, n in sorted(counts.items(), key=lambda x: -x[1])[:5]:
        print(f"      {cat:<28}{n}")
    sales, note = datasources.land_registry_recent_sales(pc, limit=5)
    print(f"  land registry  : {note}")
    for s in sales[:5]:
        print(f"      £{s['price']}  {s['date']}  {s['type']}")
    ents, note = datasources.planning_entities(dataset="conservation-area", limit=3)
    print(f"  planning data  : {note}")
    print()


def main(argv=None):
    p = argparse.ArgumentParser(prog="property_research", description="UK/London property growth research system")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_cfg(sp):
        sp.add_argument("--preset", default="balanced", choices=list(cfg.PRESETS))
        sp.add_argument("--config", help="path to a weights JSON file")

    r = sub.add_parser("rank", help="rank areas by composite score")
    add_cfg(r)
    r.add_argument("--top", type=int, default=20)
    r.add_argument("--max-flat", type=float, default=None, help="max avg flat price filter")
    r.add_argument("--max-house", type=float, default=None, help="max avg house price filter")
    r.add_argument("--lisa", action="store_true", help="only areas where avg flat <= £450k (LISA cap)")
    r.set_defaults(func=cmd_rank)

    e = sub.add_parser("explain", help="per-factor breakdown for one area")
    add_cfg(e)
    e.add_argument("area")
    e.set_defaults(func=cmd_explain)

    s = sub.add_parser("sdlt", help="first-time-buyer cost for a price")
    s.add_argument("price", type=float)
    s.set_defaults(func=cmd_sdlt)

    c = sub.add_parser("sources", help="print the data-source catalog")
    c.set_defaults(func=cmd_sources)

    rf = sub.add_parser("refresh", help="live-pull open data for an area (needs egress)")
    rf.add_argument("area")
    rf.add_argument("--month", default=None, help="YYYY-MM for crime data")
    rf.set_defaults(func=cmd_refresh)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
