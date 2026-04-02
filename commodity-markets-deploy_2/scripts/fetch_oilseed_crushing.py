#!/usr/bin/env python3
"""
Fetch monthly oilseed crushing data from USDA NASS QuickStats API.

Target series (Feb 2026 verification values):
  Crush:         SOYBEANS - CRUSHED (NATIONAL, TOTAL)                        = 6,426,352 tons
  Meal produced: CAKE & MEAL, SOYBEAN - PRODUCTION (TOTAL)                   = 4,752,577 tons
  Oil produced:  OIL, SOYBEAN, CRUDE - PRODUCTION (CRUSHER)                  = 2,478,751,000 lbs
  Meal stocks:   CAKE & MEAL, SOYBEAN - STOCKS (TOTAL)                       = 418,594 tons
  Oil stocks:    OIL, SOYBEAN, ONSITE & OFFSITE, CRUDE - STOCKS (ALL LOCS)   = 2,106,781,000 lbs
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
    """Fetch a NASS monthly series with optional domain filtering."""
    print(f"  {label}...", end=" ", flush=True)
    try:
        rows = api_get(params)
        seen = {}
        for row in rows:
            # Apply domain filters
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
            key = f"{year}-{mm}"
            seen[key] = val

        result = [{"d": k, "v": round(v, 1)} for k, v in sorted(seen.items())]
        print(f"{len(result)} points", end="")
        if result:
            print(f" ({result[0]['d']} to {result[-1]['d']})")
            for pt in result[-2:]:
                print(f"    {pt['d']}: {pt['v']:,.0f}")
        else:
            print()
            # Debug: show domains found
            domains = set()
            domcats = set()
            for row in rows[:30]:
                domains.add(row.get("domain_desc", ""))
                domcats.add(row.get("domaincat_desc", ""))
            print(f"    Domains: {domains}")
            print(f"    DomainCats: {domcats}")
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

    # 1. Soybeans crushed (tons)
    result["crush"] = fetch_series("Soybeans crushed", {
        "source_desc": "SURVEY",
        "commodity_desc": "SOYBEANS",
        "statisticcat_desc": "CRUSHED",
        "agg_level_desc": "NATIONAL",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }, domain_filter="TOTAL")
    time.sleep(0.5)

    # 2. Soybean meal produced (tons) — domain=TOTAL
    result["meal_produced"] = fetch_series("Soybean meal produced", {
        "source_desc": "SURVEY",
        "short_desc": "CAKE & MEAL, SOYBEAN - PRODUCTION, MEASURED IN TONS",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }, domain_filter="TOTAL")
    time.sleep(0.5)

    # 3. Soybean oil produced at crushers (lbs) — crude, crusher operation
    result["oil_produced"] = fetch_series("Soybean oil produced (crusher)", {
        "source_desc": "SURVEY",
        "short_desc": "OIL, SOYBEAN, CRUDE - PRODUCTION, MEASURED IN LB",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }, domaincat_filter="(CRUSHER)")
    time.sleep(0.5)

    # 4. Soybean meal stocks (tons) — domain=TOTAL
    result["meal_stocks"] = fetch_series("Soybean meal stocks", {
        "source_desc": "SURVEY",
        "short_desc": "CAKE & MEAL, SOYBEAN - STOCKS, MEASURED IN TONS",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }, domain_filter="TOTAL")
    time.sleep(0.5)

    # 5. Soybean oil stocks — crude, ALL locations (crusher+refiner+warehouse)
    result["oil_stocks"] = fetch_series("Soybean oil stocks (all locations)", {
        "source_desc": "SURVEY",
        "short_desc": "OIL, SOYBEAN, ONSITE & OFFSITE, CRUDE - STOCKS, MEASURED IN LB",
        "freq_desc": "MONTHLY",
        "year__GE": str(START_YEAR),
    }, domaincat_filter="CRUSHER OR REFINER OR WAREHOUSE")

    # Write output
    with open(output_file, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    size = os.path.getsize(output_file)
    print(f"\nWriting {output_file}")
    print(f"  {size:,} bytes")

    print("\n  --- Feb 2026 verification ---")
    expected = {"crush": 6426352, "meal_produced": 4752577,
                "oil_produced": 2478751000, "meal_stocks": 418594,
                "oil_stocks": 2106781000}
    for key in ["crush", "meal_produced", "oil_produced", "meal_stocks", "oil_stocks"]:
        pts = result.get(key, [])
        feb = [p for p in pts if p["d"] == "2026-02"]
        if feb:
            val = feb[0]["v"]
            exp = expected.get(key, 0)
            match = "✓" if abs(val - exp) < 100 else "✗"
            print(f"  {match} {key}: {val:,.0f} (expected {exp:,.0f})")
        else:
            print(f"  ? {key}: no Feb 2026 data")


if __name__ == "__main__":
    main()
