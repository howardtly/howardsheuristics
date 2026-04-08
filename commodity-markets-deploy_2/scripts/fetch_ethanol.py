#!/usr/bin/env python3
"""
Fetch weekly ethanol data from EIA.
Primary: XLS scraper (https://ir.eia.gov/wpsr/psw09.xls) — available at report time.
Fallback: EIA API v2 — lags 30-60 min after report publication.

XLS structure (psw09.xls):
  Row 0: sheet title
  Row 1: "Sourcekey" in col 0, then source keys across columns
  Row 2: "Date" in col 0, then descriptions
  Row 3+: Excel date (type 3) in col 0, numeric values in data columns
  Lookup is by source key in row 1, NOT by column position.
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.parse import urlencode

API_KEY = os.environ.get("EIA_API_KEY", "")
OUTPUT_DIR = "commodity-markets-deploy_2/data"

XLS_URL = "https://ir.eia.gov/wpsr/psw09.xls"
BASE_URL = "https://api.eia.gov/v2/petroleum/sum/sndw/data/"

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


# ── XLS Scraper ──

def fetch_xls():
    """Download and parse psw09.xls using source key lookup."""
    try:
        import xlrd
    except ImportError:
        print("  xlrd not installed — skipping XLS scrape")
        return None

    print("  Downloading XLS from EIA...")
    try:
        req = Request(XLS_URL)
        req.add_header("User-Agent", "HowardsHeuristics/1.0")
        resp = urlopen(req, timeout=60)
        xls_data = resp.read()
        print(f"  Downloaded: {len(xls_data):,} bytes")
    except Exception as e:
        print(f"  XLS download failed: {e}")
        return None

    try:
        wb = xlrd.open_workbook(file_contents=xls_data)
    except Exception as e:
        print(f"  XLS parse failed: {e}")
        return None

    result = {}
    for series_name, source_key in SERIES.items():
        print(f"    {series_name} ({source_key})...", end=" ", flush=True)
        found = False

        for sheet_name in wb.sheet_names():
            sheet = wb.sheet_by_name(sheet_name)
            if sheet.nrows < 4:
                continue

            # Check if row 1 contains our source key
            target_col = None
            for col in range(sheet.ncols):
                try:
                    val = str(sheet.cell_value(1, col)).strip()
                    if val == source_key:
                        target_col = col
                        break
                except:
                    continue

            if target_col is None:
                continue

            # Found it — extract date + value pairs from row 3 onward
            points = []
            for row in range(3, sheet.nrows):
                try:
                    date_cell = sheet.cell_value(row, 0)
                    date_type = sheet.cell_type(row, 0)
                    data_val = sheet.cell_value(row, target_col)

                    # Parse date (Excel date type = 3, or float > 30000)
                    if date_type == 3 or (isinstance(date_cell, float) and date_cell > 30000):
                        dt = xlrd.xldate_as_tuple(date_cell, wb.datemode)
                        date_str = f"{dt[0]:04d}-{dt[1]:02d}-{dt[2]:02d}"
                    else:
                        continue

                    # Parse value (must be numeric and non-empty)
                    if isinstance(data_val, (int, float)) and data_val != 0:
                        points.append({"d": date_str, "v": round(data_val)})
                    elif data_val == 0:
                        # Zero can be valid for some series
                        points.append({"d": date_str, "v": 0})
                except:
                    continue

            # Filter out rows where value is empty string or None
            points = [p for p in points if p["v"] is not None]

            if points:
                result[series_name] = points
                latest = points[-1]
                print(f"sheet '{sheet_name}' col {target_col}, {len(points)} points, latest: {latest['d']} = {latest['v']}")
                found = True
                break

        if not found:
            print("NOT FOUND in any sheet")

    if len(result) == 0:
        print("  XLS: no series found")
        return None

    return result


# ── API Fallback ──

def fetch_series_api(series_id):
    """Fetch a single series from EIA API v2."""
    params = {
        "api_key": API_KEY,
        "data[]": "value",
        "facets[series][]": series_id,
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "offset": 0,
        "length": 5000,
    }
    url = BASE_URL + "?" + urlencode(params, doseq=True)
    req = Request(url)
    req.add_header("User-Agent", "HowardsHeuristics/1.0")
    resp = urlopen(req, timeout=60)
    data = json.loads(resp.read().decode("utf-8"))

    points = []
    for row in data.get("response", {}).get("data", []):
        d = row.get("period", "")
        v = row.get("value")
        if d and v is not None:
            try:
                points.append({"d": d, "v": round(float(v))})
            except (ValueError, TypeError):
                continue
    points.sort(key=lambda x: x["d"])
    return points


def fetch_api():
    """Fetch all series from EIA API."""
    if not API_KEY:
        print("  No EIA_API_KEY — skipping API fallback")
        return None

    print("  Fetching from EIA API (fallback)...")
    result = {}

    for series_name, series_id in SERIES.items():
        print(f"    {series_name} ({series_id})...", end=" ", flush=True)
        try:
            points = fetch_series_api(series_id)
            if points:
                result[series_name] = points
                print(f"{len(points)} points, latest: {points[-1]['d']} = {points[-1]['v']}")
            else:
                # Try fallbacks for exports
                if series_name == "exports":
                    for fb_id in EXPORT_FALLBACKS:
                        print(f"\n      trying fallback {fb_id}...", end=" ", flush=True)
                        points = fetch_series_api(fb_id)
                        if points:
                            result[series_name] = points
                            print(f"{len(points)} points")
                            break
                if series_name not in result:
                    print("empty")
        except Exception as e:
            print(f"ERROR: {e}")
        time.sleep(0.3)

    return result if result else None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "ethanol.json")

    print("=" * 60)
    print("EIA Ethanol Fetch")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    # Try XLS first (available at report time)
    print("\n── XLS Scrape (primary) ──")
    result = fetch_xls()

    if result and len(result) >= 3:
        source = "xls"
        print(f"\n  XLS: got {len(result)} series")
    else:
        # Fall back to API
        print("\n── API Fetch (fallback) ──")
        result = fetch_api()
        source = "api"
        if result:
            print(f"\n  API: got {len(result)} series")
        else:
            print("\n  ERROR: both XLS and API failed")
            sys.exit(1)

    # Merge: if XLS got some but not all, fill gaps from API
    if source == "xls":
        missing = [k for k in SERIES if k not in result]
        if missing:
            print(f"\n  Missing from XLS: {missing} — trying API for gaps")
            api_data = fetch_api()
            if api_data:
                for k in missing:
                    if k in api_data:
                        result[k] = api_data[k]
                        print(f"    Filled {k} from API ({len(api_data[k])} points)")

    # Add metadata
    result["source"] = source
    result["fetched_at"] = datetime.now(timezone.utc).isoformat()

    # Write output
    with open(output_file, "w") as f:
        json.dump(result, f, separators=(",", ":"))

    size = os.path.getsize(output_file)
    print(f"\nWritten to {output_file}")
    print(f"  Source: {source}")
    print(f"  Size: {size:,} bytes ({size/1024:.1f} KB)")
    for name in SERIES:
        pts = result.get(name, [])
        if pts:
            print(f"  {name}: {len(pts)} points, latest {pts[-1]['d']} = {pts[-1]['v']}")
        else:
            print(f"  {name}: MISSING")


if __name__ == "__main__":
    main()
