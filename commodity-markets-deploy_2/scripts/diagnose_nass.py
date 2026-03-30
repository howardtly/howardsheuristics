#!/usr/bin/env python3
"""Targeted diagnostic for pasture condition and soil moisture NASS queries."""
import urllib.request, urllib.parse, json

API_KEY = "03CFFAAE-9FAC-3F49-91D0-700A4F6DC970"
BASE = "https://quickstats.nass.usda.gov/api/api_GET/"

def query(params):
    params["key"] = API_KEY
    params["format"] = "json"
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read().decode("utf-8"))
    return data.get("data", [])

def show(rows, label):
    print(f"\n  {label}: {len(rows)} rows")
    if rows:
        for f in ["commodity_desc","short_desc","unit_desc","statisticcat_desc","class_desc","domain_desc"]:
            vals = sorted(set(str(r.get(f,"")) for r in rows))
            if len(vals) <= 15: print(f"    {f}: {vals}")
            else: print(f"    {f}: {vals[:8]}... ({len(vals)} unique)")
        for r in rows[:3]:
            print(f"    Sample: week={r.get('reference_period_desc')}, desc={r.get('short_desc')}, val={r.get('Value')}")

print("=" * 70)
print("PASTURE & SOIL MOISTURE DIAGNOSTIC")
print("=" * 70)

# Try various approaches for pasture
print("\n--- PASTURE APPROACHES ---")

for commodity in ["PASTURE", "PASTURE & RANGE", "HAY & PASTURE"]:
    try:
        rows = query({"source_desc":"SURVEY","commodity_desc":commodity,"freq_desc":"WEEKLY","year":"2025","state_alpha":"US"})
        show(rows, f"commodity={commodity}")
    except Exception as e:
        print(f"  commodity={commodity}: {e}")

# Try broader search
try:
    rows = query({"source_desc":"SURVEY","short_desc__LIKE":"PASTURE","freq_desc":"WEEKLY","year":"2025","state_alpha":"US"})
    show(rows, "short_desc LIKE PASTURE")
except Exception as e:
    print(f"  short_desc LIKE PASTURE: {e}")

# Try with group_desc
try:
    rows = query({"source_desc":"SURVEY","group_desc":"CROP TOTALS","short_desc__LIKE":"PASTURE","year":"2025","state_alpha":"US"})
    show(rows, "group=CROP TOTALS, LIKE PASTURE")
except Exception as e:
    print(f"  group CROP TOTALS: {e}")

# Try FIELD CROPS
try:
    rows = query({"source_desc":"SURVEY","group_desc":"FIELD CROPS","short_desc__LIKE":"PASTURE","year":"2025","state_alpha":"US"})
    show(rows, "group=FIELD CROPS, LIKE PASTURE")
except Exception as e:
    print(f"  group FIELD CROPS: {e}")

# Soil moisture approaches
print("\n--- SOIL MOISTURE APPROACHES ---")

for commodity in ["SOIL", "TOPSOIL", "SUBSOIL"]:
    try:
        rows = query({"source_desc":"SURVEY","commodity_desc":commodity,"freq_desc":"WEEKLY","year":"2025","state_alpha":"US"})
        show(rows, f"commodity={commodity}")
    except Exception as e:
        print(f"  commodity={commodity}: {e}")

# Broader search
for term in ["TOPSOIL", "SUBSOIL", "MOISTURE"]:
    try:
        rows = query({"source_desc":"SURVEY","short_desc__LIKE":term,"freq_desc":"WEEKLY","year":"2025","state_alpha":"US"})
        show(rows, f"short_desc LIKE {term}")
    except Exception as e:
        print(f"  short_desc LIKE {term}: {e}")

# Try getting all weekly survey items to find pasture/moisture
print("\n--- ALL WEEKLY SURVEY COMMODITIES (2025, US) ---")
try:
    # Get unique commodity_desc values from weekly survey
    rows = query({"source_desc":"SURVEY","freq_desc":"WEEKLY","year":"2025","state_alpha":"US","statisticcat_desc":"CONDITION"})
    commodities = sorted(set(r.get("commodity_desc","") for r in rows))
    print(f"  Commodities with CONDITION data: {commodities}")
except Exception as e:
    print(f"  ERROR: {e}")

try:
    rows = query({"source_desc":"SURVEY","freq_desc":"WEEKLY","year":"2025","state_alpha":"US","statisticcat_desc":"MOISTURE"})
    commodities = sorted(set(r.get("commodity_desc","") for r in rows))
    print(f"  Commodities with MOISTURE data: {commodities}")
except Exception as e:
    print(f"  MOISTURE search: {e}")

# Try without statisticcat
try:
    rows = query({"source_desc":"SURVEY","freq_desc":"WEEKLY","year":"2025","state_alpha":"US","short_desc__LIKE":"TOPSOIL"})
    show(rows, "TOPSOIL broad search")
except Exception as e:
    print(f"  TOPSOIL broad: {e}")

try:
    rows = query({"source_desc":"SURVEY","freq_desc":"WEEKLY","year":"2025","state_alpha":"US","commodity_desc__LIKE":"PASTURE"})
    show(rows, "commodity LIKE PASTURE")
except Exception as e:
    print(f"  commodity LIKE PASTURE: {e}")

print("\n" + "=" * 70)
print("DONE — share this output")
print("=" * 70)
