"""
Scoring configuration: tunable presets + loader.

A config is a plain dict:
    {
      "growth_tilt": 0.5,            # 0 = pure liveability, 1 = pure growth
      "risk_penalty_strength": 0.4, # how hard risk drags the composite
      "london_reference_pte": 10.6,
      "weights": { "<factor_key>": <float>, ... }  # overrides factor defaults
    }

Anything omitted falls back to the per-factor default_weight in factors.py.
Presets below let you flip the model's personality in one flag; load a JSON
file to fully customise.
"""

import json

from . import factors as F


def _base_weights():
    return {f.key: f.default_weight for f in F.FACTORS}


# Balanced: equal-ish weight to growth and liveability, defaults respected.
BALANCED = {
    "growth_tilt": 0.5,
    "risk_penalty_strength": 0.4,
    "weights": _base_weights(),
}

# Max capital growth: tilt hard to growth, downweight pure-liveability comforts,
# punish risk harder (you're optimising for resale, not just living there).
MAX_GROWTH = {
    "growth_tilt": 0.8,
    "risk_penalty_strength": 0.55,
    "weights": {**_base_weights(),
                "infra_pipeline": 2.0,
                "regen_pipeline": 1.6,
                "gentrification_momentum": 1.5,
                "afford_headroom": 1.8,
                "gross_yield": 1.2,
                "volume_trend": 1.1,
                # comforts matter less for a pure-growth bet
                "amenity_supermarket": 0.2,
                "amenity_highstreet": 0.3,
                "greenspace": 0.4},
}

# Home-first: you'll live there. Liveability leads; growth is a bonus; risk
# (cladding/flood) still matters a lot because it's your home + resale.
HOME_FIRST = {
    "growth_tilt": 0.3,
    "risk_penalty_strength": 0.45,
    "weights": {**_base_weights(),
                "schools": 1.4,
                "safety": 1.3,
                "greenspace": 1.1,
                "amenity_highstreet": 1.0,
                "mins_to_central": 1.0,
                "ptal": 1.2},
}

PRESETS = {"balanced": BALANCED, "max-growth": MAX_GROWTH, "home-first": HOME_FIRST}


def load(path=None, preset="balanced"):
    if path:
        with open(path, encoding="utf-8") as fh:
            cfg = json.load(fh)
        # merge over base so partial files work
        merged = {**BALANCED, **cfg}
        merged["weights"] = {**_base_weights(), **cfg.get("weights", {})}
        return merged
    return PRESETS.get(preset, BALANCED)
