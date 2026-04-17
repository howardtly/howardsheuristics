#!/usr/bin/env python3
"""
Fetch USDA NASS Cattle on Feed monthly data via QuickStats API.
Outputs cattle_on_feed.json with monthly data for:
  - On-feed inventory (1,000+ head capacity lots, national)
  - Placements (total placements, national)
  - Marketings (sales for slaughter, national)
  - Heifers on feed (% of on-feed total, computed from quarterly heifer inventory)

Cattle on Feed is released monthly (~23rd of each month for the prior month).
Data is fetched from 2000 through present.
"""
import urllib.request, urllib.parse, json, os, time
from datetime import datetime, timezone
from collections import defaultdict

API_KEY = os.environ.get("NASS_API_KEY", "03CFFAAE-9FAC-3F49-91D0-700A4F6DC970")
BASE = "https://quickstats.nass.usda.gov/api/api_GET/"
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Fetch from 2000 through current year
START_YEAR = 2000
CUR_YEAR = datetime.now(timezone.utc).year
FETCH_YEARS = list(range(START_YEAR, CUR_YEAR + 1))

MONTH_LABELS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
# NASS period values for inventory (dated as "FIRST OF <MONTH>")
INV_PERIODS = ["FIRST OF JAN","FIRST OF FEB","FIRST OF MAR","FIRST OF APR","FIRST OF MAY","FIRST OF JUN",
               "FIRST OF JUL","FIRST OF AUG","FIRST OF SEP","FIRST OF OCT","FIRST OF NOV","FIRST OF DEC"]
# NASS period values for flow (placements/marketings) are month abbreviations
FLOW_PERIODS = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]


def api_get(params, retries=2):
    """Call NASS API with retry."""
    params["key"] = API_KEY
    params["format"] = "json"
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            resp = urllib.request.urlopen(req, timeout=60)
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", [])
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
            else:
                print(f"    ERROR after {retries} retries: {e}")
                return []


def parse_value(v):
    if v is None: return None
    s = str(v).strip()
    if s in ("", "(D)", "(NA)", "(Z)", "-"): return None
    try:
        return int(float(s.replace(",", "")))
    except:
        return None


def period_to_month_idx(period):
    """Map period string to 0-11 month index."""
    p = (period or "").upper().strip()
    for i, iv in enumerate(INV_PERIODS):
        if p == iv: return i
    for i, fp in enumerate(FLOW_PERIODS):
        if p == fp: return i
    return None


def fetch_on_feed_inventory():
    """Fetch on-feed inventory for 1,000+ head capacity lots, national, monthly."""
    print("\n  Fetching on-feed inventory (1,000+ head capacity)...")
    params = {
        "source_desc": "SURVEY",
        "commodity_desc": "CATTLE",
        "short_desc": "CATTLE, ON FEED - INVENTORY",
        "agg_level_desc": "NATIONAL",
        "domain_desc": "CAPACITY",
        "domaincat_desc": "CAPACITY: (1,000 OR MORE HEAD)",
        "year__GE": str(START_YEAR),
        "year__LE": str(CUR_YEAR),
    }
    rows = api_get(params)
    print(f"    Got {len(rows)} records")
    return rows


def fetch_placements():
    """Fetch placements (monthly flow)."""
    print("\n  Fetching placements...")
    params = {
        "source_desc": "SURVEY",
        "commodity_desc": "CATTLE",
        "short_desc": "CATTLE, ON FEED - PLACEMENTS, MEASURED IN HEAD",
        "agg_level_desc": "NATIONAL",
        "year__GE": str(START_YEAR),
        "year__LE": str(CUR_YEAR),
    }
    rows = api_get(params)
    print(f"    Got {len(rows)} records")
    return rows


def fetch_marketings():
    """Fetch marketings / sales for slaughter (monthly flow)."""
    print("\n  Fetching marketings...")
    params = {
        "source_desc": "SURVEY",
        "commodity_desc": "CATTLE",
        "short_desc": "CATTLE, ON FEED - SALES FOR SLAUGHTER, MEASURED IN HEAD",
        "agg_level_desc": "NATIONAL",
        "year__GE": str(START_YEAR),
        "year__LE": str(CUR_YEAR),
    }
    rows = api_get(params)
    print(f"    Got {len(rows)} records")
    return rows


def fetch_heifers_on_feed():
    """Fetch heifers/heifer calves on feed inventory (quarterly)."""
    print("\n  Fetching heifers on feed (quarterly)...")
    params = {
        "source_desc": "SURVEY",
        "commodity_desc": "CATTLE",
        "short_desc": "CATTLE, HEIFERS & HEIFER CALVES, ON FEED - INVENTORY",
        "agg_level_desc": "NATIONAL",
        "year__GE": str(START_YEAR),
        "year__LE": str(CUR_YEAR),
    }
    rows = api_get(params)
    print(f"    Got {len(rows)} records")
    return rows


def fetch_total_on_feed():
    """Fetch total on-feed inventory (all capacity) — used as denominator for heifers %."""
    print("\n  Fetching total on-feed inventory (for heifers % calc)...")
    params = {
        "source_desc": "SURVEY",
        "commodity_desc": "CATTLE",
        "short_desc": "CATTLE, ON FEED - INVENTORY",
        "agg_level_desc": "NATIONAL",
        "domain_desc": "TOTAL",
        "year__GE": str(START_YEAR),
        "year__LE": str(CUR_YEAR),
    }
    rows = api_get(params)
    print(f"    Got {len(rows)} records")
    return rows


def rows_to_yearly(rows):
    """Convert rows to {year_str: [12 slots Jan-Dec]}."""
    out = defaultdict(lambda: [None] * 12)
    for r in rows:
        try:
            yr = int(r.get("year"))
        except:
            continue
        mi = period_to_month_idx(r.get("reference_period_desc"))
        if mi is None:
            continue
        val = parse_value(r.get("Value"))
        if val is None:
            continue
        out[str(yr)][mi] = val
    return dict(out)


def compute_heifers_pct(heifers_inv, total_inv):
    """Compute heifers % of on-feed = heifers_inv / total_inv * 100 by year/month."""
    out = defaultdict(lambda: [None] * 12)
    for yr_str, heifers_arr in heifers_inv.items():
        tot_arr = total_inv.get(yr_str, [None] * 12)
        for mi in range(12):
            h = heifers_arr[mi]
            t = tot_arr[mi]
            if h is not None and t not in (None, 0):
                out[yr_str][mi] = round(h / t * 100, 2)
    return dict(out)


def build_output():
    result = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "months": MONTH_LABELS,
        "years": FETCH_YEARS,
        "series": {},
    }

    # On-feed inventory (1,000+ head capacity)
    of_rows = fetch_on_feed_inventory()
    of_yearly = rows_to_yearly(of_rows)
    result["series"]["onFeed"] = {
        "label": "Cattle on Feed (1,000+ head capacity)",
        "years": {str(y): of_yearly.get(str(y), [None] * 12) for y in FETCH_YEARS},
    }

    # Placements
    pl_rows = fetch_placements()
    pl_yearly = rows_to_yearly(pl_rows)
    result["series"]["placements"] = {
        "label": "Placements",
        "years": {str(y): pl_yearly.get(str(y), [None] * 12) for y in FETCH_YEARS},
    }

    # Marketings
    mk_rows = fetch_marketings()
    mk_yearly = rows_to_yearly(mk_rows)
    result["series"]["marketings"] = {
        "label": "Marketings",
        "years": {str(y): mk_yearly.get(str(y), [None] * 12) for y in FETCH_YEARS},
    }

    # Heifers % — compute from heifers inventory / total on-feed inventory
    hf_rows = fetch_heifers_on_feed()
    hf_yearly = rows_to_yearly(hf_rows)
    tot_rows = fetch_total_on_feed()
    tot_yearly = rows_to_yearly(tot_rows)
    heifers_pct = compute_heifers_pct(hf_yearly, tot_yearly)
    result["series"]["heifersOnFeed"] = {
        "label": "Heifers on Feed (%)",
        "years": {str(y): heifers_pct.get(str(y), [None] * 12) for y in FETCH_YEARS},
    }

    # Summary
    for sid, sdata in result["series"].items():
        populated = sum(1 for arr in sdata["years"].values() for v in arr if v is not None)
        print(f"    {sid}: {populated} data points across {len(sdata['years'])} years")

    return result


def main():
    print("=" * 60)
    print("USDA NASS Cattle on Feed Fetcher")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print(f"Years: {START_YEAR}-{CUR_YEAR}")
    print("=" * 60)

    result = build_output()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "cattle_on_feed.json")
    with open(output_file, "w") as f:
        json.dump(result, f, separators=(",", ":"))
    size = os.path.getsize(output_file)
    print(f"\nWrote {output_file} ({size:,} bytes)")


if __name__ == "__main__":
    main()
