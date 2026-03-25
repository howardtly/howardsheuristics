#!/usr/bin/env python3
"""
One-time: Fetch full PSD historical data and save as CSV baseline.
Run this once to build the historical foundation.
After this, the regular fetch_psd_world.py only needs to fetch the last 5 years.

Usage: python fetch_psd_history.py
Requires PSD_API_KEY environment variable.

Outputs: data/psd_history.csv
"""

import csv, json, os, sys, urllib.request, urllib.error, time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

API_BASE = "https://apps.fas.usda.gov/PSDOnlineDataServices/api/CommodityData/GetCommodityDataByYear"
API_KEY = os.environ.get("PSD_API_KEY", "")

COMMODITIES = {
    "corn":          {"code": "0440000", "start": 1975},
    "soybeans":      {"code": "2222000", "start": 1980},
    "wheat":         {"code": "0410000", "start": 1984},
    "soybean_meal":  {"code": "0813100", "start": 1980},
    "soybean_oil":   {"code": "4232000", "start": 1980},
}

CURRENT_YEAR = 2025

# All attribute IDs we care about
ATTR_IDS = {4, 7, 20, 28, 57, 86, 88, 125, 130, 149, 161, 176, 178, 184, 192}


def fetch_psd(commodity_code, market_year):
    url = f"{API_BASE}?commodityCode={commodity_code}&marketYear={market_year}"
    req = urllib.request.Request(url, headers={"Accept": "application/json", "API_KEY": API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"    Error: {e}")
        return None


def main():
    if not API_KEY:
        print("ERROR: PSD_API_KEY not set")
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "psd_history.csv")

    print("=" * 60)
    print("PSD Historical Data Fetch (ONE-TIME)")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)

    # CSV columns: commodity_id, country_code, country_name, market_year, attr_id, attr_name, value
    rows = []
    total_calls = 0

    for comm_id, info in COMMODITIES.items():
        code = info["code"]
        start = info["start"]
        years = list(range(start, CURRENT_YEAR + 1))
        print(f"\n-- {comm_id.upper()} ({code}) — {len(years)} years ({start}-{CURRENT_YEAR}) --")

        for my in years:
            print(f"  MY {my}...", end=" ", flush=True)
            records = fetch_psd(code, my)
            total_calls += 1
            if records:
                count = 0
                for rec in records:
                    attr_id = rec.get("AttributeId")
                    if attr_id not in ATTR_IDS:
                        continue
                    rows.append({
                        "commodity_id": comm_id,
                        "commodity_code": code,
                        "country_code": rec.get("CountryCode", "").strip(),
                        "country_name": rec.get("CountryName", "").strip(),
                        "market_year": my,
                        "attr_id": attr_id,
                        "attr_name": rec.get("AttributeDescription", "").strip(),
                        "unit": rec.get("UnitDescription", "").strip(),
                        "value": rec.get("Value"),
                    })
                    count += 1
                print(f"{count} records")
            else:
                print("no data")
            time.sleep(0.3)

    print(f"\n{'='*60}")
    print(f"Total API calls: {total_calls}")
    print(f"Total CSV rows: {len(rows):,}")

    # Write CSV
    print(f"\nWriting {output_file}")
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "commodity_id", "commodity_code", "country_code", "country_name",
            "market_year", "attr_id", "attr_name", "unit", "value"
        ])
        writer.writeheader()
        writer.writerows(rows)

    file_size = os.path.getsize(output_file)
    print(f"  {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")

    # Summary
    from collections import Counter
    comm_counts = Counter(r["commodity_id"] for r in rows)
    for cid, cnt in sorted(comm_counts.items()):
        country_count = len(set(r["country_code"] for r in rows if r["commodity_id"] == cid))
        year_count = len(set(r["market_year"] for r in rows if r["commodity_id"] == cid))
        print(f"  {cid}: {cnt:,} records, {country_count} countries, {year_count} years")

    print("\nDone! Now update fetch_psd_world.py to use psd_history.csv as baseline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
