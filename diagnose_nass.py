#!/usr/bin/env python3
"""
Diagnostic: discover NASS crop progress data structure.
Run this first to find exact parameter values for the fetcher.
"""
import urllib.request, urllib.parse, json, sys

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

def show_sample(rows, label, n=3):
    print(f"\n  {label}: {len(rows)} rows")
    if rows:
        # Show unique values for key fields
        for field in ["short_desc", "unit_desc", "freq_desc", "reference_period_desc", "state_name", "year", "Value"]:
            vals = sorted(set(str(r.get(field, "")) for r in rows))
            if len(vals) <= 20:
                print(f"    {field}: {vals}")
            else:
                print(f"    {field}: {vals[:10]} ... ({len(vals)} unique)")
        # Show first few rows
        for r in rows[:n]:
            print(f"    Sample: year={r.get('year')}, week={r.get('reference_period_desc')}, desc={r.get('short_desc')}, val={r.get('Value')}, state={r.get('state_name')}")

print("=" * 70)
print("NASS Crop Progress API Diagnostic")
print("=" * 70)

# 1. Corn progress - planting, condition, harvest
print("\n--- CORN PROGRESS (2025, US) ---")
for desc_part in ["PLANTED", "SILKING", "DOUGH", "DENTED", "MATURE", "HARVESTED", "EMERGED"]:
    try:
        rows = query({
            "source_desc": "SURVEY",
            "sector_desc": "CROPS",
            "commodity_desc": "CORN",
            "statisticcat_desc": "PROGRESS",
            "unit_desc": "PCT PLANTED" if desc_part == "PLANTED" else "PCT " + desc_part,
            "freq_desc": "WEEKLY",
            "year": "2025",
            "state_alpha": "US",
        })
        if not rows:
            # Try without specific unit
            rows = query({
                "source_desc": "SURVEY",
                "commodity_desc": "CORN",
                "statisticcat_desc": "PROGRESS",
                "short_desc__LIKE": desc_part,
                "freq_desc": "WEEKLY",
                "year": "2025",
                "state_alpha": "US",
            })
        show_sample(rows, f"CORN {desc_part}")
    except Exception as e:
        print(f"  CORN {desc_part}: ERROR {e}")

# 2. Corn condition
print("\n--- CORN CONDITION (2025, US) ---")
try:
    rows = query({
        "source_desc": "SURVEY",
        "commodity_desc": "CORN",
        "statisticcat_desc": "CONDITION",
        "freq_desc": "WEEKLY",
        "year": "2025",
        "state_alpha": "US",
    })
    show_sample(rows, "CORN CONDITION")
except Exception as e:
    print(f"  ERROR: {e}")

# 3. Soybeans progress
print("\n--- SOYBEANS PROGRESS (2025, US) ---")
for desc_part in ["PLANTED", "EMERGED", "BLOOMING", "SETTING PODS", "DROPPING LEAVES", "HARVESTED"]:
    try:
        rows = query({
            "source_desc": "SURVEY",
            "commodity_desc": "SOYBEANS",
            "statisticcat_desc": "PROGRESS",
            "short_desc__LIKE": desc_part,
            "freq_desc": "WEEKLY",
            "year": "2025",
            "state_alpha": "US",
        })
        show_sample(rows, f"SOYBEANS {desc_part}")
    except Exception as e:
        print(f"  SOYBEANS {desc_part}: ERROR {e}")

# 4. Winter wheat progress
print("\n--- WINTER WHEAT PROGRESS (2025, US) ---")
for desc_part in ["PLANTED", "EMERGED", "HEADED", "HARVESTED"]:
    try:
        rows = query({
            "source_desc": "SURVEY",
            "commodity_desc": "WHEAT",
            "class_desc": "WINTER",
            "statisticcat_desc": "PROGRESS",
            "short_desc__LIKE": desc_part,
            "freq_desc": "WEEKLY",
            "year": "2025",
            "state_alpha": "US",
        })
        show_sample(rows, f"WINTER WHEAT {desc_part}")
    except Exception as e:
        print(f"  WINTER WHEAT {desc_part}: ERROR {e}")

# 5. Spring wheat progress
print("\n--- SPRING WHEAT PROGRESS (2025, US) ---")
for desc_part in ["PLANTED", "EMERGED", "HEADED", "HARVESTED"]:
    try:
        rows = query({
            "source_desc": "SURVEY",
            "commodity_desc": "WHEAT",
            "class_desc": "SPRING, (EXCL DURUM)",
            "statisticcat_desc": "PROGRESS",
            "short_desc__LIKE": desc_part,
            "freq_desc": "WEEKLY",
            "year": "2025",
            "state_alpha": "US",
        })
        if not rows:
            rows = query({
                "source_desc": "SURVEY",
                "commodity_desc": "WHEAT",
                "class_desc__LIKE": "SPRING",
                "statisticcat_desc": "PROGRESS",
                "short_desc__LIKE": desc_part,
                "freq_desc": "WEEKLY",
                "year": "2025",
                "state_alpha": "US",
            })
        show_sample(rows, f"SPRING WHEAT {desc_part}")
    except Exception as e:
        print(f"  SPRING WHEAT {desc_part}: ERROR {e}")

# 6. Pasture condition
print("\n--- PASTURE CONDITION (2025, US) ---")
try:
    rows = query({
        "source_desc": "SURVEY",
        "commodity_desc": "PASTURE",
        "statisticcat_desc": "CONDITION",
        "freq_desc": "WEEKLY",
        "year": "2025",
        "state_alpha": "US",
    })
    show_sample(rows, "PASTURE CONDITION")
except Exception as e:
    print(f"  ERROR: {e}")

# 7. Soil moisture
print("\n--- SOIL MOISTURE (2025, US) ---")
for soil_type in ["TOPSOIL", "SUBSOIL"]:
    try:
        rows = query({
            "source_desc": "SURVEY",
            "commodity_desc": soil_type,
            "statisticcat_desc": "MOISTURE",
            "freq_desc": "WEEKLY",
            "year": "2025",
            "state_alpha": "US",
        })
        if not rows:
            rows = query({
                "source_desc": "SURVEY",
                "short_desc__LIKE": soil_type + " MOISTURE",
                "freq_desc": "WEEKLY",
                "year": "2025",
                "state_alpha": "US",
            })
        show_sample(rows, f"{soil_type} MOISTURE")
    except Exception as e:
        print(f"  {soil_type}: ERROR {e}")

# 8. List available states for corn progress
print("\n--- AVAILABLE STATES (Corn Planted 2025) ---")
try:
    rows = query({
        "source_desc": "SURVEY",
        "commodity_desc": "CORN",
        "statisticcat_desc": "PROGRESS",
        "unit_desc": "PCT PLANTED",
        "freq_desc": "WEEKLY",
        "year": "2025",
    })
    states = sorted(set(r.get("state_alpha", "") + " - " + r.get("state_name", "") for r in rows))
    print(f"  States: {len(states)}")
    for s in states:
        print(f"    {s}")
except Exception as e:
    print(f"  ERROR: {e}")

# 9. Check what short_desc values exist for wheat classes
print("\n--- WHEAT CLASS VALUES ---")
try:
    rows = query({
        "source_desc": "SURVEY",
        "commodity_desc": "WHEAT",
        "statisticcat_desc": "PROGRESS",
        "freq_desc": "WEEKLY",
        "year": "2025",
        "state_alpha": "US",
    })
    descs = sorted(set(r.get("short_desc", "") for r in rows))
    classes = sorted(set(r.get("class_desc", "") for r in rows))
    print(f"  short_desc values: {descs}")
    print(f"  class_desc values: {classes}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE — share this output")
print("=" * 70)
