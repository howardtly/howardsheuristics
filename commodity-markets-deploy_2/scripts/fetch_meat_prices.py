#!/usr/bin/env python3
"""
Fetch daily beef and pork cutout/primal prices from USDA AMS MPR Datamart.
Reports: 2453 (beef cutout PM), 2451 (boneless beef/trimmings PM), 2498 (pork cutout PM)
Accumulates daily history in meat_prices.json.
"""
import json, os, sys, time, urllib.request, urllib.error, urllib.parse
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

API_KEY = os.environ.get("AMS_API_KEY", "")
BASE = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"

HEADERS = {"Authorization": API_KEY, "Accept": "application/json", "User-Agent": "HowardsHeuristics/1.0"}


def fetch_report(report_id, date_str):
    """Fetch a single date from a report with allSections=true."""
    url = f"{BASE}/{report_id}?q=report_date={date_str}&allSections=true"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return None


def parse_beef_cutout(data):
    """Parse beef report 2453 response into clean dict."""
    if not data: return None
    blocks = data if isinstance(data, list) else [data]
    result = {}
    for block in blocks:
        if not isinstance(block, dict): continue
        section = block.get("reportSection", "")
        results = block.get("results", [])
        if not results: continue
        rec = results[0]

        if section == "Current Cutout Values":
            result["choice"] = _f(rec.get("choice_600_900_current"))
            result["select"] = _f(rec.get("select_600_900_current"))

        elif section == "Change From Prior Day":
            result["choice_chg"] = _f(rec.get("choice_600_900_change"))
            result["select_chg"] = _f(rec.get("select_600_900_change"))

        elif section == "Composite Primal Values":
            primals = {}
            for r in results:
                name = r.get("primal_desc", "").replace("Primal ", "")
                if name:
                    primals[name] = {
                        "choice": _f(r.get("choice_600_900")),
                        "select": _f(r.get("select_600_900")),
                    }
            result["primals"] = primals

        elif section == "Current Volume":
            result["choice_loads"] = _f(rec.get("choice_volume_loads"))
            result["select_loads"] = _f(rec.get("select_volume_loads"))

        elif section == "Choice Cuts":
            cuts = []
            for r in results:
                desc = r.get("item_description", "")
                if desc:
                    cuts.append({
                        "name": desc,
                        "avg": _f(r.get("weighted_average")),
                        "low": _f(r.get("price_range_low")),
                        "high": _f(r.get("price_range_high")),
                        "trades": _i(r.get("number_trades")),
                        "lbs": _i(r.get("total_pounds")),
                    })
            result["choice_cuts"] = cuts

        elif section == "Select Cuts":
            cuts = []
            for r in results:
                desc = r.get("item_description", "")
                if desc:
                    cuts.append({
                        "name": desc,
                        "avg": _f(r.get("weighted_average")),
                        "low": _f(r.get("price_range_low")),
                        "high": _f(r.get("price_range_high")),
                        "trades": _i(r.get("number_trades")),
                        "lbs": _i(r.get("total_pounds")),
                    })
            result["select_cuts"] = cuts

        elif section == "Ground Beef":
            grinds = []
            for r in results:
                desc = r.get("trim_description", "")
                if desc:
                    grinds.append({
                        "name": desc,
                        "avg": _f(r.get("weighted_average")),
                        "lbs": _i(r.get("total_pounds")),
                    })
            result["ground_beef"] = grinds

        elif section == "Beef Trimmings":
            trims = []
            for r in results:
                desc = r.get("trim_description", "")
                if desc:
                    trims.append({
                        "name": desc,
                        "avg": _f(r.get("weighted_average")),
                        "lbs": _i(r.get("total_pounds")),
                    })
            result["trimmings_2453"] = trims

    return result if result else None


def parse_beef_trimmings(data):
    """Parse boneless beef report 2451 response."""
    if not data: return None
    blocks = data if isinstance(data, list) else [data]
    result = {}
    for block in blocks:
        if not isinstance(block, dict): continue
        section = block.get("reportSection", "")
        results = block.get("results", [])
        if section == "National":
            items = []
            for r in results:
                desc = r.get("item_desc", "")
                if desc:
                    items.append({
                        "name": desc,
                        "avg": _f(r.get("price_range_avg")),
                        "low": _f(r.get("price_range_low")),
                        "high": _f(r.get("price_range_high")),
                        "trades": _i(r.get("number_trades")),
                        "lbs": _i(r.get("total_pounds")),
                    })
            result["national"] = items
    return result if result else None


def parse_pork_cutout(data):
    """Parse pork report 2498 response."""
    if not data: return None
    blocks = data if isinstance(data, list) else [data]
    result = {}
    for block in blocks:
        if not isinstance(block, dict): continue
        section = block.get("reportSection", "")
        results = block.get("results", [])
        if not results: continue
        rec = results[0]

        if section == "Cutout and Primal Values":
            result["carcass"] = _f(rec.get("pork_carcass"))
            result["loin"] = _f(rec.get("pork_loin"))
            result["butt"] = _f(rec.get("pork_butt"))
            result["picnic"] = _f(rec.get("pork_picnic"))
            result["rib"] = _f(rec.get("pork_rib"))
            result["ham"] = _f(rec.get("pork_ham"))
            result["belly"] = _f(rec.get("pork_belly"))
            result["loads"] = _f(rec.get("total_loads_date_1"))

        elif section == "Change From Prior Day":
            result["carcass_chg"] = _f(rec.get("chg_prev_carcass"))
            result["loin_chg"] = _f(rec.get("chg_prev_loin"))
            result["butt_chg"] = _f(rec.get("chg_prev_butt"))
            result["belly_chg"] = _f(rec.get("chg_prev_belly"))

        elif section in ("Loin Cuts", "Butt Cuts", "Picnic Cuts", "Ham Cuts",
                         "Belly Cuts", "Sparerib Cuts", "Trim Cuts"):
            primal_key = section.replace(" Cuts", "").lower()
            cuts = []
            for r in results:
                desc = r.get("Item_Description", "")
                if desc:
                    cuts.append({
                        "name": desc,
                        "avg": _f(r.get("weighted_average")),
                        "low": _f(r.get("price_range_low")),
                        "high": _f(r.get("price_range_high")),
                        "lbs": _i(r.get("total_pounds")),
                    })
            result[primal_key + "_cuts"] = cuts

    return result if result else None



def parse_beef_comprehensive(data):
    """Parse beef comprehensive weekly report 2465 response."""
    if not data: return None
    blocks = data if isinstance(data, list) else [data]
    result = {}
    for block in blocks:
        if not isinstance(block, dict): continue
        section = block.get("reportSection", "")
        results = block.get("results", [])

        if section == "Summary":
            if results:
                rec = results[0]
                result["total_loads"] = _i(rec.get("total_loads"))
                result["choice_loads"] = _i(rec.get("choice_loads"))
                result["select_loads"] = _i(rec.get("select_loads"))
                result["prime_loads"] = _i(rec.get("prime_loads"))

        elif section == "Subset Quality":
            grades = {}
            for r in results:
                name = r.get("report_name", "").strip()
                if name:
                    grades[name] = {
                        "cutout": _f(r.get("weekly_cutout_value")),
                        "rib": _f(r.get("primal_rib")),
                        "chuck": _f(r.get("primal_chuck")),
                        "round": _f(r.get("primal_round")),
                        "loin": _f(r.get("primal_loin")),
                        "brisket": _f(r.get("primal_brisket")),
                        "plate": _f(r.get("primal_plate")),
                        "flank": _f(r.get("primal_flank")),
                    }
            result["grades"] = grades
            # The comprehensive (all-grade) cutout - try different names
            for key in ["All", "Total", "Comprehensive", "All Fed"]:
                if key in grades:
                    result["cutout"] = grades[key]["cutout"]
                    break
            # If no explicit "All", compute weighted avg from Choice loads
            if "cutout" not in result and grades:
                # Use the first grade's cutout as fallback, or average
                vals = [g["cutout"] for g in grades.values() if g["cutout"]]
                if vals:
                    result["cutout"] = round(sum(vals) / len(vals), 2)

    return result if result else None


def _f(v):
    """Parse float from API value."""
    if v is None: return None
    try:
        s = str(v).replace(",", "").strip()
        f = float(s)
        return round(f, 2) if f != 0 else None
    except: return None

def _i(v):
    """Parse int from API value."""
    if v is None: return None
    try: return int(str(v).replace(",", "").strip())
    except: return None


def fetch_date(date_str):
    """Fetch all three reports for a single date."""
    print(f"  Fetching {date_str}...", end=" ")

    beef = fetch_report("2453", date_str)
    beef_parsed = parse_beef_cutout(beef)

    trims = fetch_report("2451", date_str)
    trims_parsed = parse_beef_trimmings(trims)

    pork = fetch_report("2498", date_str)
    pork_parsed = parse_pork_cutout(pork)

    # Weekly comprehensive (only on Fridays / report dates)
    comp = fetch_report("2465", date_str)
    comp_parsed = parse_beef_comprehensive(comp)

    if not beef_parsed and not pork_parsed:
        print("no data (holiday?)")
        return None

    record = {"date": date_str}
    if beef_parsed:
        record["beef"] = beef_parsed
    if trims_parsed:
        record["beef_trimmings"] = trims_parsed
    if pork_parsed:
        record["pork"] = pork_parsed
    if comp_parsed:
        record["beef_comp"] = comp_parsed

    choice = beef_parsed.get("choice") if beef_parsed else None
    carcass = pork_parsed.get("carcass") if pork_parsed else None
    print(f"beef={choice}, pork={carcass}")
    return record


def trading_days(start_date, end_date):
    """Generate trading days (Mon-Fri) between start and end."""
    d = start_date
    while d <= end_date:
        if d.weekday() < 5:  # Mon-Fri
            yield d
        d += timedelta(days=1)


def main():
    if not API_KEY:
        print("ERROR: AMS_API_KEY not set")
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "meat_prices.json")

    # Load existing data
    existing = {}
    if os.path.exists(output_file):
        try:
            with open(output_file) as f:
                existing = json.load(f)
            print(f"Loaded existing: {len(existing.get('daily', []))} daily records")
        except: pass

    existing_dates = set()
    for rec in existing.get("daily", []):
        existing_dates.add(rec["date"])

    print("=" * 60)
    print("Meat Price Fetch")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)

    # Determine date range to fetch
    # If backfilling (fewer than 250 records for current year), fetch from Jan 1
    # Otherwise just fetch the last 5 trading days to catch up
    today = datetime.now()
    current_year = today.year

    # Count records for current year
    cur_year_count = sum(1 for d in existing_dates if d.endswith(f"/{current_year}"))

    if cur_year_count < 200 or len(existing.get("daily", [])) < 1000:
        # Backfill: fetch from Jan 1 of the current year and prior year
        start = datetime(current_year - 4, 1, 2)
        print(f"\n  Backfill mode: fetching from {start.strftime('%m/%d/%Y')}")
    else:
        # Incremental: just last 5 trading days
        start = today - timedelta(days=8)
        print(f"\n  Incremental mode: fetching from {start.strftime('%m/%d/%Y')}")

    end = today
    dates_to_fetch = []
    for d in trading_days(start, end):
        ds = d.strftime("%m/%d/%Y")
        if ds not in existing_dates:
            dates_to_fetch.append(ds)

    print(f"  {len(dates_to_fetch)} new dates to fetch")

    # Fetch
    daily = existing.get("daily", [])
    new_count = 0
    for ds in dates_to_fetch:
        try:
            record = fetch_date(ds)
            if record:
                daily.append(record)
                new_count += 1
        except Exception as e:
            print(f"  ERROR on {ds}: {e}")
        time.sleep(0.3)  # Rate limit

    # Sort by date
    def date_sort_key(rec):
        parts = rec["date"].split("/")
        return f"{parts[2]}/{parts[0]}/{parts[1]}"
    daily.sort(key=date_sort_key)

    # Build seasonal data for charts (pre-computed by year)
    seasonal = build_seasonal_data(daily)

    # Build latest snapshot
    latest = daily[-1] if daily else None

    result = {
        "fetched_at": datetime.now().isoformat(),
        "daily": daily,
        "seasonal": seasonal,
        "latest": latest,
    }

    print(f"\n{'='*60}")
    print(f"RESULTS: {len(daily)} total daily records, {new_count} new")
    if latest:
        b = latest.get("beef", {})
        p = latest.get("pork", {})
        print(f"  Latest: {latest['date']}")
        print(f"  Beef Choice: {b.get('choice')}, Select: {b.get('select')}")
        print(f"  Pork Carcass: {p.get('carcass')}")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")
    return 0


def build_seasonal_data(daily):
    """Pre-compute seasonal (day-of-year aligned) data for charting."""
    from collections import defaultdict

    # Group by year
    by_year = defaultdict(list)
    for rec in daily:
        parts = rec["date"].split("/")
        year = int(parts[2])
        by_year[year].append(rec)

    current_year = max(by_year.keys()) if by_year else datetime.now().year
    years = sorted(by_year.keys())

    # Build day-of-year index for each year
    # Map each date to its day-of-year (1-366)
    def doy(date_str):
        parts = date_str.split("/")
        d = datetime(int(parts[2]), int(parts[0]), int(parts[1]))
        return d.timetuple().tm_yday

    def date_label(date_str):
        parts = date_str.split("/")
        return f"{int(parts[0])}/{int(parts[1])}"

    # Build aligned arrays per year for beef choice cutout
    seasonal = {"years": [], "labels": []}

    # Use current year's dates as the label template
    if current_year in by_year:
        seasonal["labels"] = [date_label(r["date"]) for r in by_year[current_year]]

    for yr in years:
        yr_records = by_year[yr]
        yr_data = {
            "year": yr,
            "dates": [date_label(r["date"]) for r in yr_records],
            "beef_choice": [r.get("beef", {}).get("choice") for r in yr_records],
            "beef_select": [r.get("beef", {}).get("select") for r in yr_records],
            "pork_carcass": [r.get("pork", {}).get("carcass") for r in yr_records],
        }

        # Beef comprehensive cutout (weekly, from 2465)
        yr_data["beef_comp"] = [r.get("beef_comp", {}).get("cutout") for r in yr_records]

        # Beef primals
        for primal in ["Rib", "Chuck", "Round", "Loin", "Brisket", "Plate", "Flank"]:
            key = f"beef_{primal.lower()}"
            yr_data[key] = [
                r.get("beef", {}).get("primals", {}).get(primal, {}).get("choice")
                for r in yr_records
            ]

        # Pork primals
        for primal in ["loin", "butt", "picnic", "rib", "ham", "belly"]:
            key = f"pork_{primal}"
            yr_data[key] = [r.get("pork", {}).get(primal) for r in yr_records]

        seasonal["years"].append(yr_data)

    # Compute 5-year average (aligned by trading day index)
    prior_years = [y for y in years if y < current_year][-5:]
    if prior_years:
        max_days = max(len(by_year[y]) for y in prior_years)
        avg = {"year": "5yr_avg", "dates": seasonal.get("labels", [])}
        for field in ["beef_choice", "beef_select", "beef_comp", "pork_carcass",
                       "beef_rib", "beef_chuck", "beef_round", "beef_loin",
                       "beef_brisket", "beef_plate", "beef_flank",
                       "pork_loin", "pork_butt", "pork_picnic", "pork_rib", "pork_ham", "pork_belly"]:
            avg_vals = []
            for di in range(max_days):
                vals = []
                for yr in prior_years:
                    yr_data_entry = next((yd for yd in seasonal["years"] if yd["year"] == yr), None)
                    if yr_data_entry and di < len(yr_data_entry.get(field, [])):
                        v = yr_data_entry[field][di]
                        if v is not None:
                            vals.append(v)
                avg_vals.append(round(sum(vals) / len(vals), 2) if vals else None)
            avg[field] = avg_vals
        seasonal["years"].append(avg)

    return seasonal


if __name__ == "__main__":
    sys.exit(main())
