#!/usr/bin/env python3
"""
Fetch weekly ethanol data from EIA API v2.
Outputs ethanol.json with production, stocks, and exports.
Offtake is calculated on the frontend.

Series:
  Production: W_EPOOXE_YOP_NUS_MBBLD (thousand barrels/day)
  Stocks:     W_EPOOXE_SAE_NUS_MBBL  (thousand barrels)
  Exports:    W_EPOOXE_EEX_NUS_MBBLD (thousand barrels/day)
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.parse import urlencode

API_KEY = os.environ.get("EIA_API_KEY", "")
OUTPUT_DIR = "commodity-markets-deploy_2/data"
BASE_URL = "https://api.eia.gov/v2/petroleum/sum/sndw/data/"

# Fetch 12 years of history (supports 10-year view with buffer)
START_DATE = "2014-09-01"

SERIES = {
    "production": "W_EPOOXE_YOP_NUS_MBBLD",
    "stocks": "W_EPOOXE_SAE_NUS_MBBL",
    "exports": "W_EPOOXE_EEX_NUS-Z00_MBBLD",
    "gasoline_demand": "WGFUPUS2",
}

# Fallback series IDs for exports if primary returns empty
EXPORT_FALLBACKS = [
    "W_EPOOXE_EEX_NUS_MBBLD",
    "WCEEXUS2",
]


def fetch_series(series_id):
    """Fetch a single EIA series."""
    params = {
        "api_key": API_KEY,
        "frequency": "weekly",
        "data[0]": "value",
        "facets[series][]": series_id,
        "start": START_DATE,
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "length": "5000",
    }
    url = BASE_URL + "?" + urlencode(params)
    req = Request(url)
    req.add_header("User-Agent", "HowardsHeuristics/1.0")

    resp = urlopen(req, timeout=30)
    data = json.loads(resp.read().decode("utf-8"))

    if "response" not in data or "data" not in data["response"]:
        print(f"  WARNING: No data in response for {series_id}")
        print(f"  Response keys: {list(data.keys())}")
        if "error" in data:
            print(f"  Error: {data['error']}")
        return []

    rows = data["response"]["data"]
    points = []
    for row in rows:
        period = row.get("period", "")
        value = row.get("value")
        if period and value is not None:
            try:
                points.append({"d": period, "v": round(float(value), 1)})
            except (ValueError, TypeError):
                continue

    return points


def main():
    if not API_KEY:
        print("ERROR: EIA_API_KEY not set")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "ethanol.json")

    print("=" * 60)
    print("EIA Ethanol Data Fetch")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print(f"Start date: {START_DATE}")
    print("=" * 60)

    result = {"updated": datetime.now(timezone.utc).isoformat()}

    for name, series_id in SERIES.items():
        print(f"  {name} ({series_id})...", end=" ", flush=True)
        try:
            points = fetch_series(series_id)
            # If exports came back empty, try fallbacks
            if name == "exports" and len(points) == 0:
                for fb in EXPORT_FALLBACKS:
                    print(f"\n    Trying fallback {fb}...", end=" ", flush=True)
                    points = fetch_series(fb)
                    if len(points) > 0:
                        break
            result[name] = points
            print(f"{len(points)} points")
            if points:
                print(f"    Range: {points[0]['d']} to {points[-1]['d']}")
        except Exception as e:
            print(f"ERROR: {e}")
            result[name] = []
        time.sleep(0.5)

    # Write output
    with open(output_file, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    size = os.path.getsize(output_file)
    print(f"\nWriting {output_file}")
    print(f"  {size:,} bytes")
    for name in SERIES:
        print(f"  {name}: {len(result.get(name, []))} points")


if __name__ == "__main__":
    main()
