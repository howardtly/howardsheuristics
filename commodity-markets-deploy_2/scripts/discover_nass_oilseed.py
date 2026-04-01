#!/usr/bin/env python3
"""Broader discovery for soybean meal/oil data in NASS."""
import json
import os
from urllib.request import urlopen, Request
from urllib.parse import urlencode

API_KEY = os.environ.get("NASS_API_KEY", "")
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


print("=" * 70)
print("BROAD SEARCH FOR SOYBEAN PRODUCT DATA")
print("=" * 70)

searches = [
    ("short_desc LIKE SOY% monthly", {"short_desc__LIKE": "SOY%", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"}),
    ("commodity LIKE OIL%", {"commodity_desc__LIKE": "OIL%", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"}),
    ("commodity LIKE MEAL%", {"commodity_desc__LIKE": "MEAL%", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"}),
    ("group LIKE %OIL%", {"group_desc__LIKE": "%OIL%", "freq_desc": "MONTHLY", "year": "2025", "source_desc": "SURVEY"}),
    ("sector=CROPS stat=PRODUCTION monthly", {"sector_desc": "CROPS", "freq_desc": "MONTHLY", "statisticcat_desc": "PRODUCTION", "year": "2025", "source_desc": "SURVEY"}),
    ("sector=CROPS stat=STOCKS monthly", {"sector_desc": "CROPS", "freq_desc": "MONTHLY", "statisticcat_desc": "STOCKS", "year": "2025", "source_desc": "SURVEY"}),
]

for label, params in searches:
    print(f"\n--- {label} ---")
    try:
        rows = api_get(params)
        if not rows:
            print("  (no results)")
            continue
        combos = {}
        for row in rows:
            key = (row.get("commodity_desc", ""), row.get("class_desc", ""), row.get("statisticcat_desc", ""), row.get("unit_desc", ""))
            short = row.get("short_desc", "")
            if key not in combos:
                combos[key] = {"count": 0, "short": short, "val": None}
            combos[key]["count"] += 1
            if row.get("Value") and combos[key]["val"] is None:
                combos[key]["val"] = row.get("Value")
        print(f"  {len(rows)} rows, {len(combos)} combos:")
        for (comm, cls, stat, unit), info in sorted(combos.items()):
            print(f"    {comm} | {cls} | {stat} | {unit} | val={info['val']}")
            print(f"      >> {info['short']}")
    except Exception as e:
        print(f"  ERROR: {e}")

# Check available commodity names with SOY/MEAL/OIL
print("\n\n--- Available commodity_desc values containing SOY/MEAL/OIL ---")
try:
    url = f"https://quickstats.nass.usda.gov/api/get_param_values/?key={API_KEY}&param=commodity_desc&format=JSON"
    req = Request(url)
    req.add_header("User-Agent", "HowardsHeuristics/1.0")
    resp = urlopen(req, timeout=60)
    data = json.loads(resp.read().decode("utf-8"))
    commodities = data.get("commodity_desc", [])
    matches = [c for c in commodities if any(k in c.upper() for k in ["SOY", "MEAL", "OIL, S"])]
    print(f"  Found {len(matches)} matching:")
    for comm in sorted(matches):
        print(f"    {comm}")
except Exception as e:
    print(f"  ERROR: {e}")
