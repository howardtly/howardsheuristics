#!/usr/bin/env python3
"""
Fetch monthly oilseed crushing data from USDA NASS QuickStats API.
Outputs oilseed_crushing.json.

NASS parameter names (discovered):
  Crush:        commodity=SOYBEANS, stat=CRUSHED, unit=TONS
  Meal produced: commodity=CAKE & MEAL, class=SOYBEAN, stat=PRODUCTION, unit=TONS
  Oil produced:  commodity=OIL, class=SOYBEAN, stat=PRODUCTION, unit=LB
  Meal stocks:   commodity=CAKE & MEAL, class=SOYBEAN, stat=STOCKS, unit=TONS
  Oil stocks:    commodity=OIL, class=SOYBEAN, stat=STOCKS, unit=LB
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.parse import urlencode

API_KEY = os.environ.get("NASS_API_KEY", "")
OUTPUT_DIR = "commodity-markets-deploy_2/data"
BASE_URL = "https://quickstats.nass.usda.gov/api/api_GET/"
START_YEAR = 2014


def api_get(params):
    params["key"] = API_KEY
    params["format"] = "JSON"
    url = BASE_URL + "?" + urlencode(params)
    req = Request(url)
    req.add_header("User-Agent", "HowardsHeuristics/1.0")
    resp = urlopen(req, timeout=60)
    data = json.loads(resp.read().decode("utf-8"))
    return data.get("data", [])


def parse_value(val):
    if val is None:
        return None
    val = str(val).strip().replace(",", "")
    if val in ("", "(D)", "(NA)", "(S)", "(Z)", "(X)") or val.strip() == "":
        return None
    try:
        return float(val)
    except ValueError:
        return None


MONTH_MAP = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04",
             "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
             "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}


def fetch_series(label, params):
    """Fetch a NASS monthly series."""
    print(f"  {label}...", end=" ", flush=True)
    try:
        rows = api_get(params)
        seen = {}
        for row in rows:
            year = row.get("year", "")
            period = row.get("reference_period_desc", "").strip().upper()
            val = parse_value(row.get("Value"))
            mm = MONTH_MAP.get(period[:3], "")
            if not mm or not year or val is None:
                continue
            key = f"{year}-{mm}"
            seen[key] = val
        result = [{"d": k, "v": round(v, 1)} for k, v in sorted(seen.items())]
        print(f"{len(result)} points", end="")
        if result:
            print(f" ({result[0]['d']} to {result[-1]['d']})")
        else:
            print()
            # Debug
            units = set(r.get("unit_desc", "") for r in rows[:10])
            print(f"    DEBUG: {len(rows)} raw rows, units={units}")
        return result
    except Exception as e:
        print(f"ERROR: {e}")
        return []


def main():
    if not API_KEY:
        print("ERROR: NASS_API_KEY not set")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "oilseed_crushing.json")

    print("=" * 60)
    print("NASS Oilseed Crushing Fetch")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print(f"Start year: {START_YEAR}")
    print("=" * 60)

    base = {
        "source_desc": "SURVEY",
        "agg_level_desc": "NATIONAL",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }

    result = {"updated": datetime.now(timezone.utc).isoformat()}

    # 1. Soybeans crushed (tons)
    result["crush"] = fetch_series("Soybeans crushed", {
        **base, "commodity_desc": "SOYBEANS", "statisticcat_desc": "CRUSHED",
    })
    time.sleep(0.5)

    # 2. Soybean meal produced (tons)
    result["meal_produced"] = fetch_series("Soybean meal produced", {
        **base, "commodity_desc": "CAKE & MEAL", "class_desc": "SOYBEAN",
        "statisticcat_desc": "PRODUCTION",
    })
    time.sleep(0.5)

    # 3. Soybean oil produced (lbs)
    result["oil_produced"] = fetch_series("Soybean oil produced", {
        **base, "commodity_desc": "OIL", "class_desc": "SOYBEAN",
        "statisticcat_desc": "PRODUCTION",
    })
    time.sleep(0.5)

    # 4. Soybean meal stocks (tons)
    result["meal_stocks"] = fetch_series("Soybean meal stocks", {
        **base, "commodity_desc": "CAKE & MEAL", "class_desc": "SOYBEAN",
        "statisticcat_desc": "STOCKS",
    })
    time.sleep(0.5)

    # 5. Soybean oil stocks (lbs)
    result["oil_stocks"] = fetch_series("Soybean oil stocks", {
        **base, "commodity_desc": "OIL", "class_desc": "SOYBEAN",
        "statisticcat_desc": "STOCKS",
    })

    # Write output
    with open(output_file, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    size = os.path.getsize(output_file)
    print(f"\nWriting {output_file}")
    print(f"  {size:,} bytes")
    for key in ["crush", "meal_produced", "oil_produced", "meal_stocks", "oil_stocks"]:
        print(f"  {key}: {len(result.get(key, []))} points")


if __name__ == "__main__":
    main()
