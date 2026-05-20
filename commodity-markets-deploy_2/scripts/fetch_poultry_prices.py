#!/usr/bin/env python3
"""
Fetch weekly chicken (3646) and turkey (3647) prices from USDA MARS / MyMarketNews API.

Endpoint:  https://marsapi.ams.usda.gov/services/v1.2/reports/{slug_id}/Report Detail
Auth:      HTTP Basic with API key as username + empty password
           (env var MMN_API_KEY; this is SEPARATE from AMS_API_KEY)

Output:    data/poultry_prices.json with this shape:
{
  "fetched_at": "...iso...",
  "weekly": [
    {
      "date": "MM/DD/YYYY",          # report_date (Monday)
      "chicken": {
        "whole_national": 123.40,    # National Composite Whole Bird Wtd Avg, cents/lb
        "parts": {
          "Breast - B/S": {"avg": 158.83, "low": 121.0, "high": 179.0, "volume": 1861},
          "Drumsticks":   {"avg": 61.35, ...},
          ...
        }
      },
      "turkey": {
        "whole": {
          "Whole Young Hen Fresh":  {"avg": 175.14, "volume": 7, ...},
          "Whole Young Hen Frozen": {"avg": 174.00, "volume": 30, ...},
          "Whole Young Tom Frozen": {"avg": 176.00, "volume": null, ...}
        },
        "parts": {
          "Breasts B/S Tom":            {"avg": 537.50, ...},
          "Drumsticks Tom":             {"avg": 173.50, ...},
          ...
        }
      }
    },
    ...
  ],
  "seasonal": {
    "years": [
      {
        "year": 2024,
        "dates": ["1/1", "1/8", ..., "12/30"],
        "chicken_whole":     [...weekly values...],
        "chicken_parts":     { "Breast - B/S": [...], "Drumsticks": [...], ... },
        "turkey_whole":      { "Whole Young Hen Fresh": [...], ... },
        "turkey_parts":      { "Breasts B/S Tom": [...], ... }
      },
      ...
      { "year": "5yr_avg", "dates": [...], ... }
    ]
  },
  "latest": {  # same shape as one weekly[] entry, for the most recent date with data
    "date": "...",
    "chicken": {...},
    "turkey": {...}
  }
}
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

API_KEY = os.environ.get("MMN_API_KEY", "")
BASE = "https://marsapi.ams.usda.gov/services/v1.2/reports"

_auth = base64.b64encode((API_KEY + ":").encode()).decode() if API_KEY else ""
HEADERS = {
    "Authorization": "Basic " + _auth,
    "Accept": "application/json",
    "User-Agent": "HowardsHeuristics/1.0",
}

# ── Item curation ────────────────────────────────────────────────────────────
# Chicken parts to keep (case-insensitive match against `item` field).
# Filter context: commodity='Chicken', region='National', trade_status='Domestic',
# condition='Fresh', freight='FOB' (parts) or 'Delivered' (whole bird).
CHICKEN_PARTS_WANTED = {
    # API name (verbatim from MARS)  -> display name (used as JSON key)
    "Breast - B/S":            "Breast - B/S",
    "Drumsticks":              "Drumsticks",
    "Leg quarters - Bulk":     "Leg Quarters - Bulk",
    "Legs - Bone-in":          "Legs - Bone-in",
    "MSC, 15-20% Fat Content": "MSC, 15-20% Fat Content",
    "Tenderloins":             "Tenderloins",
    "Thighs - B/S":            "Thighs - B/S",
    "Thighs - Bone-in":        "Thighs - Bone-in",
    "Wings - Whole":           "Wings - Whole",
}
# Chicken whole bird: National Composite Whole Bird (covers all WOG/Whole Body sizes).
# API rows for this:  primal='Whole', item='All Items' (or 'ALL Items'), region='National'.
CHICKEN_WHOLE_ITEM_NAMES_LC = {"all items"}  # case-insensitive match

# Turkey: curated list per user spec. Match key is (item, class, condition).
# `class` is 'Hen', 'Tom', or 'N/A'. The same item can appear in fresh and frozen.
# Display name is what users see in the UI table.
TURKEY_WANTED = [
    # (item_match_case_insensitive, class_match_or_None, condition_match_or_None, display_name, bucket)
    # bucket: "whole" or "parts"
    ("Whole Young",               "Hen", "Fresh",  "Whole Young Hen Fresh",  "whole"),
    ("Whole Young",               "Hen", "Frozen", "Whole Young Hen Frozen", "whole"),
    ("Whole Young",               "Tom", "Frozen", "Whole Young Tom Frozen", "whole"),
    ("Breasts,Boneless/Skinless", "Tom", None,     "Breasts B/S Tom",        "parts"),
    ("Drumsticks",                "Hen", None,     "Drumsticks Hen",         "parts"),
    ("Drumsticks",                "Tom", None,     "Drumsticks Tom",         "parts"),
    ("Mechanically Separated",    None,  None,     "MSC 15-20% Fat",         "parts"),  # legacy name; new API uses next line
    ("MSC, 15-20% Fat Content",   None,  None,     "MSC 15-20% Fat",         "parts"),
    ("Necks",                     "Hen", None,     "Necks Hen",              "parts"),
    ("Necks",                     "Tom", None,     "Necks Tom",              "parts"),
    ("Tails",                     None,  None,     "Tails",                  "parts"),
    ("Tenderloins,Destrapped",    None,  None,     "Tenderloins Destrapped", "parts"),
    ("Thigh Meat,Boneless Skinless", None, None,   "Thigh Meat B/S",         "parts"),
    ("Wings,V-Type",              "Tom", None,     "Wings V-Type Tom",       "parts"),
    ("Wings,Full-Cut",            "Hen", None,     "Wings Full-Cut Hen",     "parts"),
    ("Wings,Full-Cut",            "Tom", None,     "Wings Full-Cut Tom",     "parts"),
]


# ── Utilities ────────────────────────────────────────────────────────────────
def _f(v):
    """Parse float from API value."""
    if v is None:
        return None
    try:
        s = str(v).replace(",", "").strip()
        if not s:
            return None
        f = float(s)
        return round(f, 2) if f != 0 else None
    except Exception:
        return None


def _i(v):
    """Parse int from API value."""
    if v is None:
        return None
    try:
        s = str(v).replace(",", "").strip()
        if not s:
            return None
        return int(float(s))
    except Exception:
        return None


def _norm(s):
    return (s or "").strip().lower()


# ── API ──────────────────────────────────────────────────────────────────────
def fetch_report_detail(slug_id, report_date=None):
    """Call MARS API for the 'Report Detail' section. If report_date is None,
    returns the most recent N weeks the API gives back by default (~1 year)."""
    section = urllib.parse.quote("Report Detail")
    url = f"{BASE}/{slug_id}/{section}"
    if report_date:
        url += f"?q=report_date={report_date}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        # Response is a dict with reportSection / results
        if isinstance(data, dict):
            return data.get("results") or []
        if isinstance(data, list):
            # Older format: list of blocks; flatten the Report Detail section
            out = []
            for b in data:
                if isinstance(b, dict) and b.get("reportSection") == "Report Detail":
                    out.extend(b.get("results") or [])
            return out
        return []
    except Exception as e:
        print(f"  ERROR fetching {slug_id} date={report_date}: {e}", flush=True)
        return []


# ── Parsing per week ─────────────────────────────────────────────────────────
def _parse_row_prices(row):
    return {
        "avg": _f(row.get("wtd_avg_price")),
        "low": _f(row.get("low_price")),
        "high": _f(row.get("high_price")),
        "change": _f(row.get("price_change")),
        "volume": _i(row.get("volume")),
    }


def build_chicken_week(rows):
    """Given all chicken rows for a single report_date, return the curated dict."""
    out = {"whole_national": None, "parts": {}}
    for r in rows:
        if _norm(r.get("region")) != "national":
            continue
        if _norm(r.get("trade_status")) != "domestic":
            continue
        if _norm(r.get("condition")) != "fresh":
            continue

        primal = _norm(r.get("primal"))
        item = r.get("item") or ""
        item_lc = _norm(item)

        # Whole bird → National Composite Whole Bird (the 'All Items' aggregate)
        if primal == "whole" and item_lc in CHICKEN_WHOLE_ITEM_NAMES_LC:
            avg = _f(r.get("wtd_avg_price"))
            if avg is not None:
                # Prefer rows where size == 'N/A' (the national composite),
                # but accept any if that's all we have.
                if out["whole_national"] is None or _norm(r.get("size")) == "n/a":
                    out["whole_national"] = avg

        # Parts → curated list, FOB freight
        elif primal == "part" and _norm(r.get("freight")) == "fob":
            if item in CHICKEN_PARTS_WANTED:
                display = CHICKEN_PARTS_WANTED[item]
                prices = _parse_row_prices(r)
                # If duplicate row appears (unlikely), keep the one with higher volume
                existing = out["parts"].get(display)
                if (existing is None
                        or (prices["volume"] or 0) > (existing.get("volume") or 0)):
                    out["parts"][display] = prices
    return out


def build_turkey_week(rows):
    """Given all turkey rows for a single report_date, return curated dict."""
    out = {"whole": {}, "parts": {}}
    # Filter to domestic only (export rows are noise for the dashboard)
    domestic = [r for r in rows if _norm(r.get("trade_status")) == "domestic"
                                 and _norm(r.get("region")) == "national"]

    for spec in TURKEY_WANTED:
        item_m, class_m, cond_m, display, bucket = spec
        item_lc = _norm(item_m)
        for r in domestic:
            r_item = _norm(r.get("item"))
            # Item must match exactly (case-insensitive) to avoid 'Breeder Breasts' etc.
            if r_item != item_lc:
                continue
            if class_m is not None and _norm(r.get("class")) != _norm(class_m):
                continue
            if cond_m is not None and _norm(r.get("condition")) != _norm(cond_m):
                continue
            prices = _parse_row_prices(r)
            if prices["avg"] is None:
                continue
            # First match wins; later identical specs will not overwrite
            if display not in out[bucket]:
                out[bucket][display] = prices
            break
    return out


# ── Build full weekly history from one bulk fetch ────────────────────────────
def build_weekly_records(chicken_rows, turkey_rows):
    """Group rows by report_date and build per-week records."""
    # Group chicken
    ch_by_date = defaultdict(list)
    for r in chicken_rows:
        d = r.get("report_date")
        if d:
            ch_by_date[d].append(r)
    tk_by_date = defaultdict(list)
    for r in turkey_rows:
        d = r.get("report_date")
        if d:
            tk_by_date[d].append(r)

    all_dates = sorted(set(list(ch_by_date.keys()) + list(tk_by_date.keys())),
                       key=lambda ds: datetime.strptime(ds, "%m/%d/%Y"))

    weekly = []
    for ds in all_dates:
        rec = {"date": ds}
        if ds in ch_by_date:
            rec["chicken"] = build_chicken_week(ch_by_date[ds])
        if ds in tk_by_date:
            rec["turkey"] = build_turkey_week(tk_by_date[ds])
        weekly.append(rec)
    return weekly


# ── Build seasonal (per-year, day-of-year aligned) data ──────────────────────
def _date_to_md(ds):
    parts = ds.split("/")
    return f"{int(parts[0])}/{int(parts[1])}"


def build_seasonal(weekly):
    """Build per-year aligned arrays of prices for charts."""
    by_year = defaultdict(list)
    for rec in weekly:
        try:
            year = int(rec["date"].split("/")[2])
        except Exception:
            continue
        by_year[year].append(rec)

    years_sorted = sorted(by_year.keys())
    current_year = years_sorted[-1] if years_sorted else datetime.now().year

    # Compute the union of all chicken parts / turkey items seen across history
    all_chicken_parts = set()
    all_turkey_whole = set()
    all_turkey_parts = set()
    for rec in weekly:
        if "chicken" in rec:
            all_chicken_parts.update((rec["chicken"].get("parts") or {}).keys())
        if "turkey" in rec:
            all_turkey_whole.update((rec["turkey"].get("whole") or {}).keys())
            all_turkey_parts.update((rec["turkey"].get("parts") or {}).keys())

    year_objs = []
    for yr in years_sorted:
        yr_recs = by_year[yr]
        labels = [_date_to_md(r["date"]) for r in yr_recs]
        yo = {
            "year": yr,
            "dates": labels,
            "chicken_whole": [
                (r.get("chicken") or {}).get("whole_national") for r in yr_recs
            ],
            "chicken_parts": {},
            "turkey_whole": {},
            "turkey_parts": {},
        }
        for name in sorted(all_chicken_parts):
            yo["chicken_parts"][name] = [
                ((r.get("chicken") or {}).get("parts") or {}).get(name, {}).get("avg")
                for r in yr_recs
            ]
        for name in sorted(all_turkey_whole):
            yo["turkey_whole"][name] = [
                ((r.get("turkey") or {}).get("whole") or {}).get(name, {}).get("avg")
                for r in yr_recs
            ]
        for name in sorted(all_turkey_parts):
            yo["turkey_parts"][name] = [
                ((r.get("turkey") or {}).get("parts") or {}).get(name, {}).get("avg")
                for r in yr_recs
            ]
        year_objs.append(yo)

    # Compute 5-year average (aligned by index — weekly reports use the same
    # week-of-year position each year, so index-aligned is week-aligned)
    prior_years = [y for y in years_sorted if y < current_year][-5:]
    if prior_years:
        # Size to the longest prior year so charts have full Jan-Dec coverage
        longest_year = max(prior_years, key=lambda y: len(by_year[y]))
        longest_yo = next((yo for yo in year_objs if yo["year"] == longest_year), None)
        max_weeks = len(longest_yo["dates"]) if longest_yo else 0
        labels = longest_yo["dates"] if longest_yo else []
        avg_yo = {"year": "5yr_avg", "dates": labels, "chicken_parts": {},
                  "turkey_whole": {}, "turkey_parts": {}}
        # Average chicken_whole
        avg_yo["chicken_whole"] = _avg_array(
            year_objs, prior_years, lambda yo: yo.get("chicken_whole", []),
            max_weeks)
        for name in sorted(all_chicken_parts):
            avg_yo["chicken_parts"][name] = _avg_array(
                year_objs, prior_years,
                lambda yo, n=name: (yo.get("chicken_parts") or {}).get(n, []),
                max_weeks)
        for name in sorted(all_turkey_whole):
            avg_yo["turkey_whole"][name] = _avg_array(
                year_objs, prior_years,
                lambda yo, n=name: (yo.get("turkey_whole") or {}).get(n, []),
                max_weeks)
        for name in sorted(all_turkey_parts):
            avg_yo["turkey_parts"][name] = _avg_array(
                year_objs, prior_years,
                lambda yo, n=name: (yo.get("turkey_parts") or {}).get(n, []),
                max_weeks)
        year_objs.append(avg_yo)

    return {"years": year_objs}


def _avg_array(year_objs, prior_years, accessor, length):
    """Index-aligned mean across the given prior years for a series."""
    out = []
    for i in range(length):
        vals = []
        for yr in prior_years:
            yo = next((y for y in year_objs if y.get("year") == yr), None)
            if not yo:
                continue
            arr = accessor(yo) or []
            if i < len(arr) and arr[i] is not None:
                vals.append(arr[i])
        out.append(round(sum(vals) / len(vals), 2) if vals else None)
    return out


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Poultry Price Fetch")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    if not API_KEY:
        print("ERROR: MMN_API_KEY env var not set. "
              "Get one at https://mymarketnews.ams.usda.gov/ and add as a "
              "GitHub repo secret named MMN_API_KEY.")
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "poultry_prices.json")

    # Load existing data (if any) for merging
    existing = {"weekly": []}
    if os.path.exists(output_file):
        try:
            with open(output_file) as f:
                existing = json.load(f)
            print(f"Loaded existing: {len(existing.get('weekly', []))} weekly records")
        except Exception:
            pass

    existing_weekly = existing.get("weekly", []) or []
    existing_dates = {r["date"] for r in existing_weekly if r.get("date")}

    # ── Strategy ───────────────────────────────────────────────────────────
    # The MARS API "no date filter" call returns ~12 months of recent data
    # (which spans ~4 prior years' worth of overlapping weeks in our case —
    # the test pull showed 2022-2026). To get a full historical backfill we
    # also probe specific older Monday dates.

    print("\n--- Fetching chicken (3646) ---")
    chicken_rows = fetch_report_detail("3646", None)
    print(f"  Bulk pull: {len(chicken_rows)} rows")
    time.sleep(0.5)

    print("\n--- Fetching turkey (3647) ---")
    turkey_rows = fetch_report_detail("3647", None)
    print(f"  Bulk pull: {len(turkey_rows)} rows")

    # Build weekly records from the bulk pulls
    new_weekly = build_weekly_records(chicken_rows, turkey_rows)
    new_dates = {r["date"] for r in new_weekly}
    print(f"\nWeeks parsed from bulk pull: {len(new_weekly)}")

    # ── Merge with existing ──
    # New data wins (it's authoritative for the dates it covers).
    # Preserve existing data for older dates outside the bulk window.
    merged = []
    for old in existing_weekly:
        if old.get("date") and old["date"] not in new_dates:
            merged.append(old)
    merged.extend(new_weekly)

    # Sort by date
    merged.sort(key=lambda r: datetime.strptime(r["date"], "%m/%d/%Y"))

    # Identify any week with usable data for "latest"
    latest = None
    for r in reversed(merged):
        has_chicken = r.get("chicken", {}).get("whole_national") is not None or r.get("chicken", {}).get("parts")
        has_turkey = r.get("turkey", {}).get("whole") or r.get("turkey", {}).get("parts")
        if has_chicken or has_turkey:
            latest = r
            break

    print(f"\nTotal weeks after merge: {len(merged)}")
    if merged:
        print(f"  Date range: {merged[0]['date']} to {merged[-1]['date']}")
    if latest:
        print(f"  Latest with data: {latest['date']}")
        ch = latest.get("chicken", {})
        if ch.get("whole_national") is not None:
            print(f"    Chicken whole national: {ch['whole_national']}")
        if ch.get("parts"):
            sample = next(iter(ch["parts"].items()), None)
            if sample:
                print(f"    Sample chicken part: {sample[0]} = {sample[1].get('avg')}")
        tk = latest.get("turkey", {})
        n_w = len(tk.get("whole", {}) or {})
        n_p = len(tk.get("parts", {}) or {})
        print(f"    Turkey whole rows: {n_w}, turkey parts: {n_p}")

    # Build seasonal arrays
    print("\nBuilding seasonal arrays...")
    seasonal = build_seasonal(merged)
    years_emitted = [yo.get("year") for yo in seasonal.get("years", [])]
    print(f"  Years: {years_emitted}")

    result = {
        "fetched_at": datetime.now().isoformat(),
        "weekly": merged,
        "seasonal": seasonal,
        "latest": latest,
    }

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
