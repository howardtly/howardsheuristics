#!/usr/bin/env python3
"""
Fetch monthly oilseed crushing data from USDA NASS QuickStats API.
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


def fetch_series(label, params, domain_filter=None, domaincat_filter=None):
    print(f"  {label}...", end=" ", flush=True)
    try:
        rows = api_get(params)
        seen = {}
        for row in rows:
            if domain_filter and row.get("domain_desc", "") != domain_filter:
                continue
            if domaincat_filter and domaincat_filter not in row.get("domaincat_desc", ""):
                continue
            year = row.get("year", "")
            period = row.get("reference_period_desc", "").strip().upper()
            val = parse_value(row.get("Value"))
            mm = MONTH_MAP.get(period[:3], "")
            if not mm or not year or val is None:
                continue
            seen[f"{year}-{mm}"] = val

        result = [{"d": k, "v": round(v, 1)} for k, v in sorted(seen.items())]
        print(f"{len(result)} points", end="")
        if result:
            print(f" ({result[0]['d']} to {result[-1]['d']})")
            for pt in result[-2:]:
                print(f"    {pt['d']}: {pt['v']:,.0f}")
        else:
            print()
            domains = set(r.get("domain_desc", "") for r in rows[:20])
            domcats = set(r.get("domaincat_desc", "") for r in rows[:20])
            aggs = set(r.get("agg_level_desc", "") for r in rows[:20])
            print(f"    Domains: {domains}")
            print(f"    DomainCats: {domcats}")
            print(f"    AggLevels: {aggs}")
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
    print("=" * 60)

    result = {"updated": datetime.now(timezone.utc).isoformat()}

    # All queries use NATIONAL + short_desc for precision
    base = {
        "source_desc": "SURVEY",
        "agg_level_desc": "NATIONAL",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }

    # 1. Crush (tons) — domain=TOTAL
    result["crush"] = fetch_series("Soybeans crushed", {
        **base,
        "short_desc": "SOYBEANS - CRUSHED, MEASURED IN TONS",
    }, domain_filter="TOTAL")
    time.sleep(0.5)

    # 2. Meal produced (tons) — domain=TOTAL
    result["meal_produced"] = fetch_series("Soybean meal produced", {
        **base,
        "short_desc": "CAKE & MEAL, SOYBEAN - PRODUCTION, MEASURED IN TONS",
    }, domain_filter="TOTAL")
    time.sleep(0.5)

    # 3. Oil produced at crushers (lbs) — domaincat=(CRUSHER)
    result["oil_produced"] = fetch_series("Soybean oil produced", {
        **base,
        "short_desc": "OIL, SOYBEAN, CRUDE - PRODUCTION, MEASURED IN LB",
    }, domaincat_filter="(CRUSHER)")
    time.sleep(0.5)

    # 4. Meal stocks (tons) — domain=TOTAL
    result["meal_stocks"] = fetch_series("Soybean meal stocks", {
        **base,
        "short_desc": "CAKE & MEAL, SOYBEAN - STOCKS, MEASURED IN TONS",
    }, domain_filter="TOTAL")
    time.sleep(0.5)

    # 5. Oil stocks all locations (lbs) — domaincat=(CRUSHER OR REFINER OR WAREHOUSE)
    result["oil_stocks"] = fetch_series("Soybean oil stocks", {
        **base,
        "short_desc": "OIL, SOYBEAN, ONSITE & OFFSITE, CRUDE - STOCKS, MEASURED IN LB",
    }, domaincat_filter="CRUSHER OR REFINER OR WAREHOUSE")

    with open(output_file, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    size = os.path.getsize(output_file)
    print(f"\nWriting {output_file}")
    print(f"  {size:,} bytes")

    print("\n  --- Feb 2026 verification ---")
    expected = {"crush": 6426352, "meal_produced": 4752577,
                "oil_produced": 2478751000, "meal_stocks": 418594,
                "oil_stocks": 2106781000}
    for key, exp in expected.items():
        pts = result.get(key, [])
        feb = [p for p in pts if p["d"] == "2026-02"]
        if feb:
            val = feb[0]["v"]
            match = "PASS" if abs(val - exp) < 100 else "FAIL"
            print(f"  {match} {key}: {val:,.0f} (expected {exp:,.0f})")
        else:
            print(f"  MISS {key}: no Feb 2026 data")


if __name__ == "__main__":
    main()
