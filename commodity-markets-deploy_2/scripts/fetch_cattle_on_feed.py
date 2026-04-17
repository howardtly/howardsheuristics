#!/usr/bin/env python3
"""
Fetch USDA NASS Cattle on Feed data via QuickStats API.
Outputs cattle_on_feed.json with monthly data for:
  - On-feed inventory (1,000+ head capacity feedlots)
  - Placements
  - Marketings
  - Heifers & heifer calves as % of inventory (quarterly: Jan/Apr/Jul/Oct)

Covers 2021 through current year.
"""
import urllib.request, urllib.parse, json, os, sys
from datetime import datetime, timezone
from collections import defaultdict

API_KEY = os.environ.get("NASS_API_KEY", "03CFFAAE-9FAC-3F49-91D0-700A4F6DC970")
BASE = "https://quickstats.nass.usda.gov/api/api_GET/"
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

CUR_YEAR = datetime.now(timezone.utc).year
START_YEAR = 2021
FETCH_YEARS = list(range(START_YEAR, CUR_YEAR + 1))

# NASS short_desc mappings for COF 1,000+ head feedlots
SERIES = {
    "on_feed":    "CATTLE, ON FEED - INVENTORY, MEASURED IN HEAD",
    "placements": "CATTLE, ON FEED, PLACEMENTS - RECEIPTS, MEASURED IN HEAD",
    "marketings": "CATTLE, ON FEED, MARKETINGS - DISAPPEARANCE, MEASURED IN HEAD",
    "heifer_pct": "CATTLE, ON FEED, HEIFERS & HEIFER CALVES - INVENTORY, MEASURED IN PCT OF INVENTORY",
}

MONTH_MAP = {
    "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
    "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12,
}


def api_get(params, retries=2):
    params["key"] = API_KEY
    params["format"] = "json"
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8")).get("data", [])
        except Exception as e:
            if attempt >= retries:
                print(f"  API error: {e}")
                return []
            import time
            time.sleep(1.5 * (attempt + 1))
    return []


def parse_value(v):
    """Convert NASS value string to int/float. '(D)' = withheld, '(Z)' = <0.5"""
    if v is None or v == "" or v == "(D)" or v == "(NA)":
        return None
    if v == "(Z)":
        return 0
    try:
        return int(str(v).replace(",", ""))
    except ValueError:
        try:
            return float(str(v).replace(",", ""))
        except ValueError:
            return None


def fetch_series(short_desc, year):
    """Fetch NASS data for one series, one year. National level, 1,000+ head."""
    params = {
        "short_desc": short_desc,
        "year": str(year),
        "agg_level_desc": "NATIONAL",
    }
    rows = api_get(params)
    # Filter: want 1,000+ head capacity feedlots (domain_desc: FEEDLOTS, 1,000+ HEAD CAPACITY)
    # or where domain_desc is just TOTAL (national 1,000+ head is the default reported series)
    result = []
    for row in rows:
        dd = row.get("domain_desc", "")
        dc = row.get("domaincat_desc", "")
        # Target only 1,000+ head capacity series
        if dd == "FEEDLOTS" and "1,000+" in dc:
            result.append(row)
        elif dd == "TOTAL" and short_desc == SERIES["heifer_pct"]:
            # Heifer pct sometimes reported at TOTAL level
            result.append(row)
    # Fallback: if the strict filter returns nothing, take TOTAL
    if not result:
        for row in rows:
            if row.get("domain_desc") == "TOTAL":
                result.append(row)
    return result


def main():
    print(f"Fetching Cattle on Feed data {START_YEAR}-{CUR_YEAR}")
    print("=" * 60)

    # Structure: {series_key: {year: {month: value}}}
    data = {key: defaultdict(dict) for key in SERIES}

    for key, short_desc in SERIES.items():
        print(f"\nFetching {key}: {short_desc}")
        for year in FETCH_YEARS:
            rows = fetch_series(short_desc, year)
            count = 0
            for row in rows:
                # Reference period: "FIRST OF JAN" / "MAR 1" etc.
                ref = row.get("reference_period_desc", "").strip().upper()
                # Parse month from reference period
                month = None
                for m_name, m_num in MONTH_MAP.items():
                    if m_name in ref:
                        month = m_num
                        break
                if month is None:
                    continue
                val = parse_value(row.get("Value"))
                if val is None:
                    continue
                data[key][year][month] = val
                count += 1
            print(f"  {year}: {count} data points")

    # Build output structure matching CattleOnFeedPage expectations:
    # {
    #   last_updated: "...",
    #   years: [2021, 2022, ...],
    #   series: {
    #     onFeed:        { years: { "2021": [Jan..Dec], ... } },
    #     placements:    { years: { ... } },
    #     marketings:    { years: { ... } },
    #     heifersOnFeed: { years: { ... } }
    #   }
    # }
    SID_MAP = {
        "on_feed":    "onFeed",
        "placements": "placements",
        "marketings": "marketings",
        "heifer_pct": "heifersOnFeed",
    }

    series_out = {}
    all_years_seen = set()
    for key in SERIES:
        sid = SID_MAP[key]
        yearly = {}
        for year in FETCH_YEARS:
            arr = [data[key][year].get(m) for m in range(1, 13)]
            if any(v is not None for v in arr):
                yearly[str(year)] = arr
                all_years_seen.add(year)
        series_out[sid] = {"years": yearly}

    output = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "years": sorted(all_years_seen),
        "series": series_out,
    }

    # Write JSON
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "cattle_on_feed.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    # Summary
    print("\n" + "=" * 60)
    print(f"Wrote {out_path}")
    print(f"Years covered: {output['years'][0]}-{output['years'][-1]}" if output['years'] else "No data")
    for key in SERIES:
        sid = SID_MAP[key]
        yearly = output["series"][sid]["years"]
        years_covered = sorted(yearly.keys())
        if years_covered:
            latest_year = years_covered[-1]
            latest_vals = yearly[latest_year]
            last_non_null_idx = max((i for i, v in enumerate(latest_vals) if v is not None), default=-1)
            latest_val = latest_vals[last_non_null_idx] if last_non_null_idx >= 0 else None
            print(f"  {sid}: {len(years_covered)} years, latest {latest_year} M{last_non_null_idx+1}: {latest_val}")


if __name__ == "__main__":
    main()
