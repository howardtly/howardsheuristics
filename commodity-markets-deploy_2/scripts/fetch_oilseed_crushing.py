#!/usr/bin/env python3
"""
Fetch monthly oilseed crushing data from USDA NASS QuickStats API.
Outputs oilseed_crushing.json with crush, meal/oil production, meal/oil stocks.

Data source: NASS "Fats and Oils: Oilseed Crushings" monthly report.
Marketing year: Oct 1 - Sep 30 (soybean marketing year).
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

# Fetch 12 years of data
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
    if val in ("", "(D)", "(NA)", "(S)", "(Z)", "(X)"):
        return None
    try:
        return float(val)
    except ValueError:
        return None


def fetch_series(label, params, unit_filter=None):
    """Fetch a NASS series and return list of {d: "YYYY-MM", v: value}."""
    print(f"  {label}...", end=" ", flush=True)
    try:
        rows = api_get(params)
        points = []
        for row in rows:
            year = row.get("year", "")
            # reference_period_desc is like "JAN", "FEB", etc. for monthly
            period = row.get("reference_period_desc", "").strip().upper()
            unit = row.get("unit_desc", "")
            val = parse_value(row.get("Value"))

            if unit_filter and unit_filter.upper() not in unit.upper():
                continue

            # Map period to month number
            month_map = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04",
                         "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
                         "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}
            mm = month_map.get(period[:3], "")
            if not mm or not year or val is None:
                continue
            points.append({"d": f"{year}-{mm}", "v": round(val, 1)})

        # Deduplicate and sort
        seen = {}
        for p in points:
            seen[p["d"]] = p["v"]
        result = [{"d": k, "v": v} for k, v in sorted(seen.items())]
        print(f"{len(result)} points ({result[0]['d']} to {result[-1]['d']})" if result else "0 points")
        if not result:
            # Debug: show what we got
            units_found = set()
            periods_found = set()
            for row in rows[:20]:
                units_found.add(row.get("unit_desc", ""))
                periods_found.add(row.get("reference_period_desc", ""))
            if units_found:
                print(f"    Units found: {units_found}")
            if periods_found:
                print(f"    Periods found: {periods_found}")
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

    base_params = {
        "source_desc": "SURVEY",
        "agg_level_desc": "NATIONAL",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }

    # 1. Soybeans crushed (1,000 bushels)
    result["crush"] = fetch_series("Soybeans crushed", {
        **base_params,
        "commodity_desc": "SOYBEANS",
        "statisticcat_desc": "CRUSHED",
    })
    time.sleep(0.5)

    # 2. Soybean meal produced (1,000 short tons)
    result["meal_produced"] = fetch_series("Soybean meal produced", {
        **base_params,
        "commodity_desc": "MEAL, SOYBEAN",
        "statisticcat_desc": "PRODUCTION",
    })
    time.sleep(0.5)

    # 3. Soybean oil produced (million lbs)
    result["oil_produced"] = fetch_series("Soybean oil produced", {
        **base_params,
        "commodity_desc": "OIL, SOYBEAN",
        "statisticcat_desc": "PRODUCTION",
    }, unit_filter="LB")
    time.sleep(0.5)

    # 4. Soybean meal stocks (1,000 short tons)
    result["meal_stocks"] = fetch_series("Soybean meal stocks", {
        **base_params,
        "commodity_desc": "MEAL, SOYBEAN",
        "statisticcat_desc": "STOCKS",
    })
    time.sleep(0.5)

    # 5. Soybean oil stocks (million lbs)
    result["oil_stocks"] = fetch_series("Soybean oil stocks", {
        **base_params,
        "commodity_desc": "OIL, SOYBEAN",
        "statisticcat_desc": "STOCKS",
    }, unit_filter="LB")
    time.sleep(0.5)

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
