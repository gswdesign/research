"""
Data-source catalog + lightweight, no-auth open-data clients.

Two things live here:

1. CATALOG — a documented register of the public UK datasets that feed the
   model: what each contains, the predictive signal it carries, access method,
   and which factor(s) in factors.py it refreshes. This is the "where do I get
   the data" map for future exploration.

2. Runnable clients (stdlib urllib only) for the genuinely open, key-free APIs:
     * HM Land Registry Price Paid (SPARQL) -> sold prices / £-per-area inputs
     * Police.uk street-level crime      -> the `safety` factor
     * planning.data.gov.uk entities      -> `planning_momentum` / regen pipeline
   These let you pull live values to update data/areas.csv. They degrade
   gracefully (return [] and a note) if the network policy blocks egress.

Heavier sources (EPC, ONS, TfL PTAL, Ofsted, Census) are documented in the
catalog with their endpoints; wire them in as needed — several need a (free)
API key or bulk-CSV download rather than a simple GET.
"""

import json
import urllib.parse
import urllib.request

USER_AGENT = "uk-property-research/1.0 (+research tool)"
TIMEOUT = 20


CATALOG = [
    {
        "name": "HM Land Registry Price Paid Data",
        "signal": "Ground-truth sold prices, property type, new-build flag, tenure (lagging target).",
        "access": "Free. Bulk CSV + SPARQL/Linked Data at landregistry.data.gov.uk.",
        "feeds": ["price_momentum_3yr", "afford_headroom", "volume_trend"],
        "url": "https://landregistry.data.gov.uk/",
        "auth": "none",
    },
    {
        "name": "ONS / UK House Price Index",
        "signal": "Mix-adjusted hedonic index down to LSOA; the headline benchmark and growth target.",
        "access": "Free CSV/API.",
        "feeds": ["price_momentum_3yr"],
        "url": "https://www.gov.uk/government/collections/uk-house-price-index-reports",
        "auth": "none",
    },
    {
        "name": "ONS house-price-to-earnings (affordability ratios)",
        "signal": "Affordability headroom — the best-evidenced macro driver.",
        "access": "Free annual CSV by local authority.",
        "feeds": ["afford_headroom"],
        "url": "https://www.ons.gov.uk/peoplepopulationandcommunity/housing/bulletins/housingaffordabilityinenglandandwales/latest",
        "auth": "none",
    },
    {
        "name": "EPC register (domestic certificates)",
        "signal": "Floor area (m2) — the ONLY free source enabling £/m², the most comparable price metric. Join to Price Paid on address.",
        "access": "Free with registration; bulk CSV + REST API. Migrating to 'Get energy performance of buildings data' by 30 May 2026.",
        "feeds": ["afford_headroom"],
        "url": "https://epc.opendatacommunities.org/",
        "auth": "free api key",
    },
    {
        "name": "TfL PTAL / WebCAT",
        "signal": "Public Transport Accessibility Level (0-6b) grid — current accessibility.",
        "access": "Free download / WebCAT tool.",
        "feeds": ["ptal", "mins_to_central"],
        "url": "https://www.tfl.gov.uk/info-for/urban-planning-and-construction/planning-with-webcat/webcat",
        "auth": "none",
    },
    {
        "name": "Police.uk street-level crime",
        "signal": "Crime by lat/long + outcomes, monthly. Falling crime is the leading version of the safety signal.",
        "access": "Free REST API, no key.",
        "feeds": ["safety"],
        "url": "https://data.police.uk/docs/",
        "auth": "none",
    },
    {
        "name": "planning.data.gov.uk",
        "signal": "Planning applications, brownfield-land registers, conservation areas, listed buildings — the regeneration-pipeline signal.",
        "access": "Free REST API + bulk, no key.",
        "feeds": ["planning_momentum", "regen_pipeline", "greenspace"],
        "url": "https://www.planning.data.gov.uk/docs",
        "auth": "none",
    },
    {
        "name": "GLA Opportunity Areas",
        "signal": "Designated large-scale regeneration zones + housing/jobs capacity.",
        "access": "Free (London Datastore / london.gov.uk).",
        "feeds": ["regen_pipeline"],
        "url": "https://www.london.gov.uk/programmes-strategies/planning/implementing-london-plan/londons-opportunity-areas",
        "auth": "none",
    },
    {
        "name": "Ofsted inspection ratings",
        "signal": "School quality / catchment premium. NB: single-word judgements replaced by report cards from 2025.",
        "access": "Free open data CSV.",
        "feeds": ["schools"],
        "url": "https://www.gov.uk/government/collections/ofsted-inspection-outcomes-management-information",
        "auth": "none",
    },
    {
        "name": "ONS Private Rents + Census 2021",
        "signal": "Rent growth (leading) and demographic shift (education/occupation) for gentrification momentum.",
        "access": "Free CSV/API.",
        "feeds": ["rent_growth", "gentrification_momentum", "gross_yield"],
        "url": "https://www.ons.gov.uk/census",
        "auth": "none",
    },
    {
        "name": "Environment Agency flood risk",
        "signal": "Flood zones — the flood-risk drag.",
        "access": "Free API / map.",
        "feeds": ["risk_flood"],
        "url": "https://environment.data.gov.uk/",
        "auth": "none",
    },
    {
        "name": "Rightmove / Zoopla (asking prices, time-on-market)",
        "signal": "LEADING features: asking-vs-sold gap, days-to-sell, listing volumes, % reductions.",
        "access": "No free official API; Zoopla has a limited API. Portal data/scrape.",
        "feeds": ["volume_trend", "gentrification_momentum"],
        "url": "https://www.zoopla.co.uk/",
        "auth": "varies",
    },
]


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---------------------------------------------------------------------------
# Runnable open clients (no key required). Each returns (data, note).
# ---------------------------------------------------------------------------

def police_crime_count(lat, lon, year_month=None):
    """Street-level crime count near a point (1-mile radius). year_month='2026-01'.
    Returns (count_by_category: dict, note)."""
    base = "https://data.police.uk/api/crimes-street/all-crime"
    q = {"lat": lat, "lng": lon}
    if year_month:
        q["date"] = year_month
    url = base + "?" + urllib.parse.urlencode(q)
    try:
        data = _get(url)
    except Exception as e:  # network blocked / no data
        return {}, f"police.uk request failed ({e}); is egress allowed?"
    counts = {}
    for c in data:
        cat = c.get("category", "other")
        counts[cat] = counts.get(cat, 0) + 1
    return counts, f"{len(data)} crimes near ({lat},{lon}) for {year_month or 'latest'}"


def planning_entities(dataset="planning-application", limit=10, **filters):
    """Query planning.data.gov.uk entities. e.g. dataset='conservation-area'.
    Returns (entities: list, note)."""
    base = "https://www.planning.data.gov.uk/entity.json"
    q = {"dataset": dataset, "limit": limit}
    q.update(filters)
    url = base + "?" + urllib.parse.urlencode(q)
    try:
        data = _get(url)
    except Exception as e:
        return [], f"planning.data.gov.uk request failed ({e}); is egress allowed?"
    entities = data.get("entities", data if isinstance(data, list) else [])
    return entities, f"{len(entities)} '{dataset}' entities"


LR_BASE = "https://landregistry.data.gov.uk/data/ppi/transaction-record.json"


def _lr_type(item):
    """Property type from the record's _about URL (terraced / semi-detached /
    detached / flat-maisonette / other)."""
    about = (item.get("propertyType", {}) or {}).get("_about", "")
    return about.rsplit("/", 1)[-1] if about else ""


def land_registry_recent_sales(postcode, limit=20):
    """Recent Price Paid transactions for an EXACT postcode. Returns (list, note)."""
    pc = urllib.parse.quote(postcode.upper())
    url = f"{LR_BASE}?propertyAddress.postcode={pc}&_pageSize={limit}&_sort=-transactionDate"
    try:
        data = _get(url)
    except Exception as e:
        return [], f"Land Registry request failed ({e}); is egress allowed?"
    items = data.get("result", {}).get("items", [])
    out = [{"price": it.get("pricePaid"), "date": it.get("transactionDate"),
            "type": _lr_type(it), "postcode": (it.get("propertyAddress", {}) or {}).get("postcode")}
           for it in items]
    return out, f"{len(out)} recent sales for {postcode}"


def land_registry_district_records(district, pages=3, page_size=200):
    """Pull recent Price Paid records for a local-authority district (e.g.
    'NEWHAM'), most-recent first, across several pages. Returns (records, note).
    Each record: {price, date, type, postcode}."""
    out = []
    for page in range(pages):
        q = {"propertyAddress.district": district.upper(), "_sort": "-transactionDate",
             "_pageSize": page_size, "_page": page}
        try:
            data = _get(LR_BASE + "?" + urllib.parse.urlencode(q))
        except Exception as e:
            return out, f"Land Registry request failed ({e}); is egress allowed?"
        items = data.get("result", {}).get("items", [])
        if not items:
            break
        for it in items:
            out.append({"price": it.get("pricePaid"), "date": it.get("transactionDate"),
                        "type": _lr_type(it),
                        "postcode": (it.get("propertyAddress", {}) or {}).get("postcode", "") or ""})
    return out, f"{len(out)} records for {district}"


def area_price_medians(records, postcode_prefix):
    """Median flat / house / all-type prices for records whose postcode starts
    with `postcode_prefix` (e.g. 'E7', 'SE2'). Returns a dict."""
    import statistics
    pref = postcode_prefix.upper()
    flats, houses, allp = [], [], []
    latest = None
    for r in records:
        if not (r["postcode"] or "").upper().startswith(pref):
            continue
        p = r["price"]
        if not p:
            continue
        allp.append(p)
        if "flat" in r["type"]:
            flats.append(p)
        elif r["type"] in ("terraced", "semi-detached", "detached"):
            houses.append(p)
        latest = latest or r["date"]
    med = lambda xs: int(statistics.median(xs)) if xs else None
    return {"flat_median": med(flats), "house_median": med(houses), "all_median": med(allp),
            "n_flat": len(flats), "n_house": len(houses), "n_all": len(allp), "latest_date": latest}


def print_catalog():
    for d in CATALOG:
        print(f"\n## {d['name']}  [auth: {d['auth']}]")
        print(f"   signal : {d['signal']}")
        print(f"   access : {d['access']}")
        print(f"   feeds  : {', '.join(d['feeds'])}")
        print(f"   url    : {d['url']}")
