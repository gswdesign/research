"""
Refresh avg_flat_price / avg_house_price in data/areas.csv with LIVE HM Land
Registry Price Paid medians, and stamp provenance.

Usage:
    python3 scripts/refresh_prices.py            # refresh all areas
    python3 scripts/refresh_prices.py --dry-run  # show what would change, write nothing

Strategy: for each area, pull recent transactions for its local-authority
DISTRICT (paginated), filter client-side to the area's POSTCODE PREFIX, and take
median flat / house prices. Only overwrite a value when we have >= MIN_SAMPLES
real sales (otherwise keep the seed value and say so). District records are
cached so shared boroughs are fetched once.
"""

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from property_research import datasources as ds

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "areas.csv")
MIN_SAMPLES = 4

# area name -> (Land Registry local-authority district, postcode prefix)
AREA_MAP = {
    "Abbey Wood": ("GREENWICH", "SE2"),
    "Thamesmead": ("GREENWICH", "SE28"),
    "Woolwich": ("GREENWICH", "SE18"),
    "Barking": ("BARKING AND DAGENHAM", "IG11"),
    "Dagenham": ("BARKING AND DAGENHAM", "RM10"),
    "Manor Park": ("NEWHAM", "E12"),
    "Forest Gate": ("NEWHAM", "E7"),
    "Royal Docks": ("NEWHAM", "E16"),
    "Walthamstow": ("WALTHAM FOREST", "E17"),
    "Leyton": ("WALTHAM FOREST", "E10"),
    "Tottenham Hale": ("HARINGEY", "N17"),
    "Lewisham": ("LEWISHAM", "SE13"),
    "Catford": ("LEWISHAM", "SE6"),
    "Croydon": ("CROYDON", "CR0"),
    "Bexleyheath": ("BEXLEY", "DA6"),
    "Southall": ("EALING", "UB1"),
    "Canada Water": ("SOUTHWARK", "SE16"),
    "Old Kent Road": ("SOUTHWARK", "SE15"),
    "Ealing": ("EALING", "W5"),
    "Nine Elms": ("WANDSWORTH", "SW8"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--pages", type=int, default=4)
    args = ap.parse_args()

    with open(DATA, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames
        rows = list(reader)

    district_cache = {}
    latest_seen = None
    print(f"{'Area':<16}{'flat seed':>11}{'flat live':>11}{'house seed':>12}{'house live':>12}  n(f/h)")
    print("-" * 78)

    for row in rows:
        name = row["name"]
        if name not in AREA_MAP:
            continue
        district, prefix = AREA_MAP[name]
        if district not in district_cache:
            recs, note = ds.land_registry_district_records(district, pages=args.pages)
            district_cache[district] = recs
            if not recs:
                print(f"{name:<16}  -- no data ({note})")
        recs = district_cache[district]
        m = ds.area_price_medians(recs, prefix)
        latest_seen = latest_seen or m["latest_date"]

        f_seed = row.get("avg_flat_price", "")
        h_seed = row.get("avg_house_price", "")
        f_live = m["flat_median"] if m["n_flat"] >= MIN_SAMPLES else None
        h_live = m["house_median"] if m["n_house"] >= MIN_SAMPLES else None

        if f_live:
            row["avg_flat_price"] = str(f_live)
        if h_live:
            row["avg_house_price"] = str(h_live)
        if f_live or h_live:
            row["data_confidence"] = "live"
            date = (m["latest_date"] or "").split(",")[-1].strip()
            tag = f" [LR live {prefix} flats n={m['n_flat']} houses n={m['n_house']}, to {date}]"
            note = row.get("notes", "")
            if "[LR live" not in note:
                row["notes"] = note + tag

        print(f"{name:<16}{f_seed:>11}{(str(f_live) if f_live else 'kept'):>11}"
              f"{h_seed:>12}{(str(h_live) if h_live else 'kept'):>12}"
              f"  {m['n_flat']}/{m['n_house']}")

    if args.dry_run:
        print("\n[dry-run] no file written.")
        return

    with open(DATA, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"\nWrote live Land Registry medians to {DATA} (latest sale seen: {latest_seen}).")


if __name__ == "__main__":
    main()
