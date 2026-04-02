#!/usr/bin/env python3
"""
Fetch weekly export sales data from USDA FAS ESR API.
Stores weekly totals (all countries) + per-country data for recent MYs.

API: https://api.fas.usda.gov/api/esr/exports/commodityCode/{code}/allCountries/marketYear/{my}
Auth: x-api-key header
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import HTTPError

API_KEY = os.environ.get("FAS_ESR_API_KEY", "")
OUTPUT_DIR = "commodity-markets-deploy_2/data"
BASE = "https://api.fas.usda.gov"

COMMODITIES = {
    "corn": {"code": 401, "myStart": 9},      # Sep
    "soybeans": {"code": 801, "myStart": 9},   # Sep
    "wheat": {"code": 107, "myStart": 6},      # Jun (All Wheat)
    "sorghum": {"code": 701, "myStart": 9},    # Sep
}

# How many MYs back to fetch
TOTAL_HISTORY = 11  # current + 10 prior
COUNTRY_HISTORY = 2  # store per-country data for recent MYs only


def api_get(url):
    req = Request(url)
    req.add_header("x-api-key", API_KEY)
    req.add_header("User-Agent", "HowardsHeuristics/1.0")
    req.add_header("Accept", "application/json")
    resp = urlopen(req, timeout=60)
    return json.loads(resp.read().decode("utf-8"))


def get_current_mys():
    """Get current marketing year for each commodity from datareleasedates."""
    data = api_get(f"{BASE}/api/esr/datareleasedates")
    my_map = {}
    for item in data:
        code = item["commodityCode"]
        my = item["marketYear"]
        my_map[code] = my
    return my_map


def fetch_commodity(name, code, current_my):
    """Fetch all MYs for a commodity, return totals + country data."""
    print(f"\n  {name} (code={code}, currentMY={current_my})")
    totals = []  # [{d, my, we, ae, ns, os, tc, nns, nos}, ...]
    by_country = {}  # {countryCode: [{d, my, ...}, ...]}

    for offset in range(TOTAL_HISTORY):
        my = current_my - offset
        url = f"{BASE}/api/esr/exports/commodityCode/{code}/allCountries/marketYear/{my}"
        print(f"    MY {my}...", end=" ", flush=True)
        try:
            rows = api_get(url)
            if not rows:
                print("empty")
                continue

            # Group by weekEndingDate, sum across countries
            weekly = {}  # {date: {we, ae, ns, os, tc, nns, nos}}
            for row in rows:
                d = row["weekEndingDate"][:10]
                if d not in weekly:
                    weekly[d] = {"we": 0, "ae": 0, "ns": 0, "os": 0, "tc": 0, "nns": 0, "nos": 0}
                w = weekly[d]
                w["we"] += row.get("weeklyExports", 0) or 0
                w["ae"] += row.get("accumulatedExports", 0) or 0
                w["ns"] += row.get("currentMYNetSales", 0) or 0
                w["os"] += row.get("outstandingSales", 0) or 0
                w["tc"] += row.get("currentMYTotalCommitment", 0) or 0
                w["nns"] += row.get("nextMYNetSales", 0) or 0
                w["nos"] += row.get("nextMYOutstandingSales", 0) or 0

                # Store per-country data for recent MYs
                if offset < COUNTRY_HISTORY:
                    cc = str(row["countryCode"])
                    if cc not in by_country:
                        by_country[cc] = []
                    by_country[cc].append({
                        "d": d, "my": my,
                        "we": row.get("weeklyExports", 0) or 0,
                        "ae": row.get("accumulatedExports", 0) or 0,
                        "ns": row.get("currentMYNetSales", 0) or 0,
                        "os": row.get("outstandingSales", 0) or 0,
                        "tc": row.get("currentMYTotalCommitment", 0) or 0,
                        "nns": row.get("nextMYNetSales", 0) or 0,
                        "nos": row.get("nextMYOutstandingSales", 0) or 0,
                    })

            # Add to totals
            for d in sorted(weekly.keys()):
                w = weekly[d]
                totals.append({"d": d, "my": my, **w})

            weeks = len(weekly)
            print(f"{len(rows)} rows -> {weeks} weeks")

        except HTTPError as e:
            print(f"HTTP {e.code}")
        except Exception as e:
            print(f"ERR: {e}")
        time.sleep(0.3)

    # Sort totals by date
    totals.sort(key=lambda x: x["d"])
    print(f"    Total: {len(totals)} weekly points, {len(by_country)} countries")
    return totals, by_country


def main():
    if not API_KEY:
        print("ERROR: FAS_ESR_API_KEY not set")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "export_sales.json")

    print("=" * 60)
    print("FAS Export Sales Fetch")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    # Get current MYs
    print("  Fetching current marketing years...")
    my_map = get_current_mys()

    # Get country list
    print("  Fetching country list...")
    countries_raw = api_get(f"{BASE}/api/esr/countries")
    countries = [{"c": c["countryCode"], "n": c["countryDescription"].strip()} for c in countries_raw]
    print(f"    {len(countries)} countries")

    result = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "countries": countries,
    }

    for name, cfg in COMMODITIES.items():
        code = cfg["code"]
        current_my = my_map.get(code, 2026)
        totals, by_country = fetch_commodity(name, code, current_my)
        result[name] = {"totals": totals, "byCountry": by_country}

    # Write output
    with open(output_file, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    size = os.path.getsize(output_file)
    print(f"\nWriting {output_file}")
    print(f"  {size:,} bytes ({size/1024/1024:.1f} MB)")
    for name in COMMODITIES:
        d = result[name]
        print(f"  {name}: {len(d['totals'])} weeks, {len(d['byCountry'])} countries")


if __name__ == "__main__":
    main()
