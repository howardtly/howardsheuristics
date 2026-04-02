#!/usr/bin/env python3
"""
Fetch weekly export inspection data from FGIS CSV files.
Aggregates shipment-level data into weekly totals by commodity.

Source: https://fgisonline.ams.usda.gov/ExportGrainReport/CY{year}.csv
Columns used: Thursday (week-ending), Grain, Metric Ton
"""
import csv
import io
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request

OUTPUT_DIR = "commodity-markets-deploy_2/data"
BASE_URL = "https://fgisonline.ams.usda.gov/ExportGrainReport/CY{year}.csv"

# Fetch current year + previous 12 years for deep history
CURRENT_YEAR = datetime.now().year
FETCH_YEARS = list(range(CURRENT_YEAR - 12, CURRENT_YEAR + 1))

COMMODITIES = {"CORN", "SOYBEANS", "WHEAT", "SORGHUM"}


def fetch_csv(year):
    """Download and parse a single year's CSV."""
    url = BASE_URL.format(year=year)
    print(f"  CY{year}...", end=" ", flush=True)
    try:
        req = Request(url)
        req.add_header("User-Agent", "HowardsHeuristics/1.0")
        resp = urlopen(req, timeout=60)
        raw = resp.read().decode("utf-8", errors="replace")
        reader = csv.reader(io.StringIO(raw))
        headers = next(reader)

        # Find column indices
        def find_col(name):
            for i, h in enumerate(headers):
                if h.strip().upper() == name.upper():
                    return i
            return None

        thursday_col = find_col("Thursday")
        grain_col = find_col("Grain")
        mt_col = find_col("Metric Ton")
        bu_col = find_col("1000 Bushels")

        if thursday_col is None or grain_col is None:
            print(f"MISSING COLUMNS (thursday={thursday_col}, grain={grain_col})")
            return {}

        # Aggregate by week + commodity
        weekly = {}  # {(date_str, commodity): metric_tons}
        row_count = 0
        for row in reader:
            if len(row) <= max(thursday_col, grain_col):
                continue
            thu = row[thursday_col].strip().strip('"')
            grain = row[grain_col].strip().upper()
            if grain not in COMMODITIES:
                continue

            # Parse metric tons
            mt_val = 0
            if mt_col is not None and mt_col < len(row):
                try:
                    mt_val = float(row[mt_col].strip().replace(",", ""))
                except (ValueError, IndexError):
                    pass

            # If no metric ton, try converting from pounds
            if mt_val == 0:
                pounds_col = find_col("Pounds")
                if pounds_col is not None and pounds_col < len(row):
                    try:
                        lbs = float(row[pounds_col].strip().replace(",", ""))
                        mt_val = lbs / 2204.62
                    except (ValueError, IndexError):
                        pass

            if mt_val <= 0:
                continue

            # Convert Thursday date YYYYMMDD -> YYYY-MM-DD
            if len(thu) == 8:
                date_str = f"{thu[:4]}-{thu[4:6]}-{thu[6:8]}"
            else:
                continue

            key = (date_str, grain)
            weekly[key] = weekly.get(key, 0) + mt_val
            row_count += 1

        # Convert to per-commodity lists
        by_commodity = {}
        for (date_str, grain), mt in sorted(weekly.items()):
            if grain not in by_commodity:
                by_commodity[grain] = []
            by_commodity[grain].append({"d": date_str, "v": round(mt, 1)})

        weeks = len(set(d for d, _ in weekly.keys()))
        print(f"{row_count} rows -> {weeks} weeks, {', '.join(f'{g}:{len(pts)}' for g, pts in sorted(by_commodity.items()))}")
        return by_commodity

    except Exception as e:
        print(f"ERROR: {e}")
        return {}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "export_inspections.json")

    print("=" * 60)
    print("FGIS Export Inspections Fetch")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print(f"Years: {FETCH_YEARS[0]}-{FETCH_YEARS[-1]}")
    print("=" * 60)

    # Merge all years
    merged = {}  # {commodity: [{d, v}, ...]}
    for year in FETCH_YEARS:
        by_comm = fetch_csv(year)
        for grain, pts in by_comm.items():
            if grain not in merged:
                merged[grain] = {}
            for pt in pts:
                # Use date as key to handle overlaps between CY files
                merged[grain][pt["d"]] = pt["v"]
        time.sleep(0.3)

    # Convert to sorted lists
    result = {"updated": datetime.now(timezone.utc).isoformat()}
    for grain in ["CORN", "SOYBEANS", "WHEAT", "SORGHUM"]:
        if grain in merged:
            pts = [{"d": k, "v": v} for k, v in sorted(merged[grain].items())]
            result[grain.lower()] = pts
            print(f"\n  {grain}: {len(pts)} weeks ({pts[0]['d']} to {pts[-1]['d']})")
            # Show latest 3
            for pt in pts[-3:]:
                print(f"    {pt['d']}: {pt['v']:,.0f} MT")
        else:
            result[grain.lower()] = []
            print(f"\n  {grain}: no data")

    with open(output_file, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    size = os.path.getsize(output_file)
    print(f"\nWriting {output_file}")
    print(f"  {size:,} bytes")


if __name__ == "__main__":
    main()
