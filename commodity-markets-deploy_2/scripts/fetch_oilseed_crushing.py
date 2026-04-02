#!/usr/bin/env python3
"""
Fetch monthly oilseed crushing data from USDA NASS QuickStats API.

NASS parameters (discovered):
  Crush:         commodity=SOYBEANS, stat=CRUSHED, unit=TONS (agg_level=NATIONAL works)
  Meal produced: short_desc LIKE "CAKE & MEAL, SOYBEAN - PRODUCTION%"
  Oil produced:  short_desc LIKE "OIL, SOYBEAN, CRUDE - PRODUCTION%"
  Meal stocks:   short_desc LIKE "CAKE & MEAL, SOYBEAN - STOCKS%"
  Oil stocks:    short_desc LIKE "OIL, SOYBEAN, CRUDE - STOCKS%"

For meal/oil, we query by short_desc to ensure we get the right series,
and take the MAX value per month (national total, not state breakdowns).
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

MONTH_MAP = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04",
             "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
             "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}


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


def fetch_series(label, params, use_max=False):
    """Fetch a NASS monthly series. If use_max, take the largest value per month."""
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
            if use_max:
                # Take max value (national total > any individual state)
                if key not in seen or val > seen[key]:
                    seen[key] = val
            else:
                seen[key] = val
        result = [{"d": k, "v": round(v, 1)} for k, v in sorted(seen.items())]
        print(f"{len(result)} points", end="")
        if result:
            print(f" ({result[0]['d']} to {result[-1]['d']})")
            # Show latest values for verification
            for pt in result[-3:]:
                print(f"    {pt['d']}: {pt['v']:,.0f}")
        else:
            print()
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

    result = {"updated": datetime.now(timezone.utc).isoformat()}

    # 1. Soybeans crushed (tons) — NATIONAL works
    result["crush"] = fetch_series("Soybeans crushed", {
        "source_desc": "SURVEY",
        "commodity_desc": "SOYBEANS",
        "statisticcat_desc": "CRUSHED",
        "agg_level_desc": "NATIONAL",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    })
    time.sleep(0.5)

    # 2. Soybean meal produced — query by short_desc, take MAX per month
    result["meal_produced"] = fetch_series("Soybean meal produced", {
        "source_desc": "SURVEY",
        "short_desc": "CAKE & MEAL, SOYBEAN - PRODUCTION, MEASURED IN TONS",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }, use_max=True)
    time.sleep(0.5)

    # 3. Soybean oil produced — crude production
    result["oil_produced"] = fetch_series("Soybean oil produced", {
        "source_desc": "SURVEY",
        "short_desc": "OIL, SOYBEAN, CRUDE - PRODUCTION, MEASURED IN LB",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }, use_max=True)
    time.sleep(0.5)

    # 4. Soybean meal stocks
    result["meal_stocks"] = fetch_series("Soybean meal stocks", {
        "source_desc": "SURVEY",
        "short_desc": "CAKE & MEAL, SOYBEAN - STOCKS, MEASURED IN TONS",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }, use_max=True)
    time.sleep(0.5)

    # 5. Soybean oil stocks — crude stocks
    result["oil_stocks"] = fetch_series("Soybean oil stocks", {
        "source_desc": "SURVEY",
        "short_desc": "OIL, SOYBEAN, CRUDE - STOCKS, MEASURED IN LB",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }, use_max=True)

    # Write output
    with open(output_file, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    size = os.path.getsize(output_file)
    print(f"\nWriting {output_file}")
    print(f"  {size:,} bytes")
    for key in ["crush", "meal_produced", "oil_produced", "meal_stocks", "oil_stocks"]:
        print(f"  {key}: {len(result.get(key, []))} points")

    # Verification
    print("\n  --- Feb 2026 verification ---")
    for key in ["crush", "meal_produced", "oil_produced", "meal_stocks", "oil_stocks"]:
        pts = result.get(key, [])
        feb = [p for p in pts if p["d"] == "2026-02"]
        if feb:
            print(f"  {key}: {feb[0]['v']:,.0f}")
        else:
            print(f"  {key}: (no data)")


if __name__ == "__main__":
    main()
