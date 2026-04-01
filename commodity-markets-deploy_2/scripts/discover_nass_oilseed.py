#!/usr/bin/env python3
"""Discover available NASS series for soybean meal and oil."""
import json
import os
from urllib.request import urlopen, Request
from urllib.parse import urlencode

API_KEY = os.environ.get("NASS_API_KEY", "03CFFAAE-9FAC-3F49-91D0-700A4F6DC970")
BASE_URL = "https://quickstats.nass.usda.gov/api/api_GET/"


def api_get(params):
    params["key"] = API_KEY
    params["format"] = "JSON"
    url = BASE_URL + "?" + urlencode(params)
    req = Request(url)
    req.add_header("User-Agent", "HowardsHeuristics/1.0")
    resp = urlopen(req, timeout=60)
    data = json.loads(resp.read().decode("utf-8"))
    return data.get("data", [])


# Search for anything soybean-related that's monthly
print("=" * 70)
print("SEARCHING FOR SOYBEAN CRUSHING-RELATED MONTHLY DATA")
print("=" * 70)

# Try various commodity names
searches = [
    {"commodity_desc": "SOYBEANS", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"},
    {"commodity_desc": "MEAL, SOYBEAN", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"},
    {"commodity_desc": "OIL, SOYBEAN", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"},
    {"commodity_desc": "SOYBEAN MEAL", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"},
    {"commodity_desc": "SOYBEAN OIL", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"},
    {"commodity_desc": "SOYBEANS", "statisticcat_desc": "PRODUCTION", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"},
    {"commodity_desc": "SOYBEANS", "statisticcat_desc": "STOCKS", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"},
]

for params in searches:
    label = " & ".join(f"{k}={v}" for k, v in params.items() if k not in ("key", "format", "year", "source_desc"))
    print(f"\n--- {label} ---")
    try:
        rows = api_get(params)
        if not rows:
            print("  (no results)")
            continue
        # Group by commodity + statisticcat + unit
        combos = {}
        for row in rows:
            key = (
                row.get("commodity_desc", ""),
                row.get("class_desc", ""),
                row.get("statisticcat_desc", ""),
                row.get("unit_desc", ""),
                row.get("short_desc", ""),
            )
            if key not in combos:
                combos[key] = {"count": 0, "sample_value": None, "sample_period": None}
            combos[key]["count"] += 1
            if row.get("Value") and combos[key]["sample_value"] is None:
                combos[key]["sample_value"] = row.get("Value")
                combos[key]["sample_period"] = row.get("reference_period_desc")

        print(f"  {len(rows)} rows, {len(combos)} unique combos:")
        for (comm, cls, stat, unit, short), info in sorted(combos.items()):
            print(f"    commodity={comm} | class={cls} | stat={stat} | unit={unit}")
            print(f"      short_desc: {short}")
            print(f"      count={info['count']} sample={info['sample_value']} ({info['sample_period']})")
    except Exception as e:
        print(f"  ERROR: {e}")

# Also try searching by group_desc
print("\n\n--- Searching by group_desc=OILSEEDS ---")
try:
    rows = api_get({"group_desc": "OILSEEDS", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"})
    combos = {}
    for row in rows:
        key = (row.get("commodity_desc", ""), row.get("statisticcat_desc", ""), row.get("unit_desc", ""))
        if key not in combos:
            combos[key] = 0
        combos[key] += 1
    print(f"  {len(rows)} rows:")
    for (comm, stat, unit), cnt in sorted(combos.items()):
        print(f"    {comm} | {stat} | {unit} ({cnt} rows)")
except Exception as e:
    print(f"  ERROR: {e}")
