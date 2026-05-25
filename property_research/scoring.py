"""
Scoring engine.

Pipeline:
  1. Load areas (raw feature values) from data/areas.csv.
  2. Auto-derive afford_headroom from price_to_earnings if not supplied.
  3. Min-max normalise every factor across the area set to 0-100 (inverting
     DOWN factors so that 100 is always "good for this factor").
  4. Weighted-average the normalised factors within each bucket -> growth_score,
     liveability_score, risk_score (risk_score: higher = worse).
  5. Blend growth + liveability via a tunable growth_tilt -> composite_base.
  6. Apply the risk penalty -> composite (final).

Everything is tunable via a config dict (see config.py / data/weights.default.json):
  - per-factor weight overrides
  - growth_tilt          (0.0 = pure liveability ... 1.0 = pure growth; 0.5 = balanced)
  - risk_penalty_strength (how hard risk_score drags the composite down)

Pure standard library — no third-party dependencies.
"""

import csv
import statistics
from dataclasses import dataclass, field

from . import factors as F

# London average price-to-earnings used to derive affordability headroom
# (ONS 2025: Greater London ~10.6x). Override in config if it moves.
LONDON_REFERENCE_PTE = 10.6


@dataclass
class Area:
    name: str
    borough: str
    raw: dict = field(default_factory=dict)   # factor_key -> float (or None)
    meta: dict = field(default_factory=dict)  # non-scored columns (notes, sources, lat/lon...)
    norm: dict = field(default_factory=dict)  # factor_key -> 0..100
    growth_score: float = 0.0
    liveability_score: float = 0.0
    risk_score: float = 0.0
    composite_base: float = 0.0
    composite: float = 0.0
    imputed: list = field(default_factory=list)  # factor keys that were missing


META_COLUMNS = {
    "name", "borough", "postcode_district", "lat", "lon", "zone",
    "avg_flat_price", "avg_house_price", "tenure_note", "data_confidence",
    "notes", "sources",
}


def _to_float(v):
    if v is None:
        return None
    s = str(v).strip()
    if s == "" or s.lower() in ("na", "n/a", "none", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def load_areas(csv_path):
    areas = []
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            raw, meta = {}, {}
            for col, val in row.items():
                if col in META_COLUMNS or col not in F.FACTORS_BY_KEY:
                    meta[col] = val
                else:
                    raw[col] = _to_float(val)
            # carry the numeric meta we want for filtering/display
            for k in ("avg_flat_price", "avg_house_price"):
                meta[k] = _to_float(meta.get(k))
            a = Area(name=row.get("name", "?"), borough=row.get("borough", ""), raw=raw, meta=meta)
            areas.append(a)
    return areas


def _derive(areas, config):
    ref_pte = config.get("london_reference_pte", LONDON_REFERENCE_PTE)
    for a in areas:
        # afford_headroom from price_to_earnings if not directly supplied.
        # price_to_earnings is informational (not a scored factor) so it arrives
        # in meta; coerce it here.
        if a.raw.get("afford_headroom") is None:
            pte = _to_float(a.meta.get("price_to_earnings"))
            if pte is not None:
                a.raw["afford_headroom"] = ref_pte - pte


def _normalise(areas):
    """Min-max each factor column to 0..100, inverting DOWN factors. Missing
    values are imputed to the column median and flagged on the area."""
    for f in F.FACTORS:
        vals = [a.raw.get(f.key) for a in areas]
        present = [v for v in vals if v is not None]
        if not present:
            for a in areas:
                a.norm[f.key] = 50.0
            continue
        med = statistics.median(present)
        lo, hi = min(present), max(present)
        span = hi - lo
        for a in areas:
            v = a.raw.get(f.key)
            if v is None:
                v = med
                a.imputed.append(f.key)
            if span == 0:
                s = 50.0
            else:
                s = (v - lo) / span * 100.0
            if f.direction == F.DOWN:
                s = 100.0 - s
            a.norm[f.key] = round(s, 2)


def _weight(config, key, default):
    return config.get("weights", {}).get(key, default)


def _bucket_score(area, bucket_factors, config):
    num = den = 0.0
    for f in bucket_factors:
        w = _weight(config, f.key, f.default_weight)
        if w <= 0:
            continue
        num += w * area.norm[f.key]
        den += w
    return round(num / den, 2) if den else 0.0


def score(areas, config=None):
    config = config or {}
    _derive(areas, config)
    _normalise(areas)

    growth_tilt = float(config.get("growth_tilt", 0.5))           # 0..1
    risk_strength = float(config.get("risk_penalty_strength", 0.4))  # 0..1

    for a in areas:
        a.growth_score = _bucket_score(a, F.GROWTH_FACTORS, config)
        a.liveability_score = _bucket_score(a, F.LIVEABILITY_FACTORS, config)
        # risk_score: 100 = worst. risk factors are DOWN-direction so a normalised
        # value of 100 means "low risk"; invert back so higher score = more risk.
        live_form = _bucket_score(a, F.RISK_FACTORS, config)
        a.risk_score = round(100.0 - live_form, 2)

        a.composite_base = round(
            growth_tilt * a.growth_score + (1 - growth_tilt) * a.liveability_score, 2
        )
        penalty = risk_strength * (a.risk_score / 100.0)
        a.composite = round(a.composite_base * (1 - penalty), 2)

    return sorted(areas, key=lambda x: x.composite, reverse=True)


def explain(area, config=None):
    """Return a per-factor contribution breakdown for one area (for transparency)."""
    config = config or {}
    rows = []
    for f in F.FACTORS:
        w = _weight(config, f.key, f.default_weight)
        rows.append({
            "key": f.key,
            "label": f.label,
            "bucket": f.bucket,
            "lead_lag": f.lead_lag,
            "evidence": f.evidence,
            "raw": area.raw.get(f.key),
            "normalised": area.norm.get(f.key),
            "weight": w,
            "imputed": f.key in area.imputed,
        })
    return rows
