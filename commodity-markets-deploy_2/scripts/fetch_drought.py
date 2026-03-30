#!/usr/bin/env python3
"""
Fetch USDA 'Commodities in Drought' data from agindrought.unl.edu JSON API.
Downloads weekly D1-D4 drought percentages for 6 commodities, outputs drought.json.

API endpoint: Home.aspx/ReturnCropData2020
Parameters: ctype (commodity), ltype (1=US), loc (location code)
"""
import urllib.request, urllib.parse, json, os, sys, time
from datetime import datetime, timezone
from collections import defaultdict

COMMODITIES = {
    "corn":         {"ctype": "corn",         "label": "Corn",         "color": "#D4A017"},
    "soybeans":     {"ctype": "soybeans",     "label": "Soybeans",     "color": "#1D9E75"},
    "winter_wheat": {"ctype": "winter wheat", "label": "Winter Wheat", "color": "#A32D2D"},
    "spring_wheat": {"ctype": "spring wheat", "label": "Spring Wheat", "color": "#D85A30"},
    "cattle":       {"ctype": "cattle",       "label": "Cattle",       "color": "#378ADD"},
    "hay":          {"ctype": "hay",          "label": "Hay",          "color": "#8B5CF6"},
}

BASE_URL = "https://agindrought.unl.edu/Home.aspx/ReturnCropData2020"
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def fetch_commodity(ctype):
    """Fetch all drought data for a commodity. Returns list of {Date, None, D0, D1, D2, D3, D4}."""
    params = urllib.parse.urlencode({
        "ctype": f'"{ctype}"',
        "ltype": '"1"',
        "loc": '"0"',
    })
    url = f"{BASE_URL}?{params}"
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
    })
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read().decode("utf-8"))
    return data.get("d", [])


def process_commodity(raw_rows):
    """Process raw API rows into structured yearly data."""
    by_year = defaultdict(list)
    for row in raw_rows:
        date_str = row.get("Date", "")
        d1_d4 = row.get("D1")
        if not date_str or d1_d4 is None:
            continue
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            by_year[dt.year].append({
                "date": date_str,
                "d1_d4": int(d1_d4),
                "d2_d4": int(row.get("D2", 0)),
                "d3_d4": int(row.get("D3", 0)),
                "d4": int(row.get("D4", 0)),
                "none": int(row.get("None", 0)),
                "d0_d4": int(row.get("D0", 0)),
            })
        except (ValueError, TypeError):
            continue

    for yr in by_year:
        by_year[yr].sort(key=lambda r: r["date"])

    return dict(by_year)


def build_seasonal(by_year, cur_year):
    """Build seasonal arrays with {x: doy, y: d1_d4} points and 5yr avg."""
    seasonal = {}
    for yr, rows in sorted(by_year.items()):
        points = []
        for r in rows:
            dt = datetime.strptime(r["date"], "%Y-%m-%d")
            doy = dt.timetuple().tm_yday - 1
            points.append({"x": doy, "y": r["d1_d4"], "date": r["date"]})
        seasonal[str(yr)] = points

    # 5-year average
    avg_years = [y for y in range(cur_year - 5, cur_year) if y in by_year]
    if avg_years:
        by_week = defaultdict(list)
        for yr in avg_years:
            for r in by_year[yr]:
                dt = datetime.strptime(r["date"], "%Y-%m-%d")
                week = dt.timetuple().tm_yday // 7
                by_week[week].append(r["d1_d4"])
        avg_points = []
        for week in sorted(by_week.keys()):
            vals = by_week[week]
            avg_val = round(sum(vals) / len(vals))
            doy = week * 7 + 3
            avg_points.append({"x": doy, "y": avg_val})
        seasonal["5yr_avg"] = avg_points

    return seasonal


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "drought.json")

    print("=" * 60)
    print("USDA Commodities in Drought Fetch")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    cur_year = datetime.now(timezone.utc).year
    result = {"fetched_at": datetime.now(timezone.utc).isoformat(), "data": {}}

    for com_id, meta in COMMODITIES.items():
        print(f"\n  Fetching {meta['label']} ({meta['ctype']})...")
        try:
            raw = fetch_commodity(meta["ctype"])
            print(f"    {len(raw)} rows returned")

            if not raw:
                print(f"    WARNING: no data")
                continue

            by_year = process_commodity(raw)
            years = sorted(by_year.keys())
            print(f"    Years: {years[0]}-{years[-1]} ({len(years)} years)")

            latest_yr = max(years)
            latest_row = by_year[latest_yr][-1]
            print(f"    Latest: {latest_row['date']}, D1-D4={latest_row['d1_d4']}%")

            seasonal = build_seasonal(by_year, cur_year)

            result["data"][com_id] = {
                "label": meta["label"],
                "color": meta["color"],
                "latest_date": latest_row["date"],
                "latest_d1_d4": latest_row["d1_d4"],
                "seasonal": seasonal,
                "available_years": [str(y) for y in years],
            }

        except Exception as e:
            print(f"    ERROR: {e}")

        time.sleep(0.5)

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")
    print(f"  {len(result['data'])} commodities")

    return 0


if __name__ == "__main__":
    sys.exit(main())
