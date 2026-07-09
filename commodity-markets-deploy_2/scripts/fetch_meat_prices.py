#!/usr/bin/env python3
"""
Fetch daily beef and pork cutout/primal prices from USDA AMS MPR Datamart.
Reports: 2453 (LM_XB403 beef cutout PM), 2451 (LM_XB401 boneless beef/trimmings PM),
2498 (LM_PK602 pork cutout PM), 2465 (LM_XB463 weekly comprehensive cutout)
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
            # Full volume breakdown (pounds + trimmings / ground beef loads).
            # Exact field names vary slightly across datamart reports, so scan keys.
            def _vol_field(sub_a, sub_b):
                for k, v in rec.items():
                    kl = str(k).lower()
                    if sub_a in kl and sub_b in kl:
                        return _f(v)
                return None
            result["choice_lbs"] = _vol_field("choice", "pound")
            result["select_lbs"] = _vol_field("select", "pound")
            result["trim_loads"] = _vol_field("trim", "load")
            result["trim_lbs"] = _vol_field("trim", "pound")
            gl = _vol_field("grind", "load")
            result["grind_loads"] = gl if gl is not None else _vol_field("ground", "load")
            gp = _vol_field("grind", "pound")
            result["grind_lbs"] = gp if gp is not None else _vol_field("ground", "pound")

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

        elif section == "Choice and Select Cuts":
            cuts = []
            for r in results:
                desc = r.get("trim_description", "")
                if desc:
                    cuts.append({
                        "name": desc,
                        "avg": _f(r.get("weighted_average")),
                        "low": _f(r.get("price_range_low")),
                        "high": _f(r.get("price_range_high")),
                        "trades": _i(r.get("number_trades")),
                        "lbs": _i(r.get("total_pounds")),
                    })
            result["choice_select_cuts"] = cuts

        elif section == "Ground Beef":
            grinds = []
            for r in results:
                desc = r.get("trim_description", "")
                if desc:
                    grinds.append({
                        "name": desc,
                        "avg": _f(r.get("weighted_average")),
                        "low": _f(r.get("price_range_low")),
                        "high": _f(r.get("price_range_high")),
                        "trades": _i(r.get("number_trades")),
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
                        "low": _f(r.get("price_range_low")),
                        "high": _f(r.get("price_range_high")),
                        "trades": _i(r.get("number_trades")),
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
            for key in ["Comp", "All", "Total", "Comprehensive", "All Fed"]:
                if key in grades:
                    result["cutout"] = grades[key]["cutout"]
                    break
            # If no explicit "All", try common variants
            if "cutout" not in result and grades:
                pass  # Grades checked
                # Use a weighted approach: if Choice and Select exist, weight them
                ch = grades.get("Choice", {}).get("cutout")
                se = grades.get("Select", {}).get("cutout")
                if ch and se:
                    # Approximate comprehensive as ~75% Choice + 25% Select
                    result["cutout"] = round(ch * 0.75 + se * 0.25, 2)
                elif ch:
                    result["cutout"] = ch
                else:
                    vals = [g["cutout"] for g in grades.values() if g.get("cutout")]
                    if vals:
                        result["cutout"] = round(sum(vals) / len(vals), 2)

    return result if result else None



def rebuild_comp_series(daily):
    """Rebuild the comprehensive-cutout series for every daily record.

    The comprehensive cutout is a WEEKLY figure. Anchors come from report 2465
    (authoritative — carries a 'grades' block) and the historical Urner Barry CSV;
    report 2465 wins for any week both cover. Each week's value is carried across
    that week's trading days, but only up to STALE_DAYS after the most recent
    anchor, so a stalled source shows a gap instead of a flat line frozen at its
    last value. Rich 2465 records are preserved; others get {cutout, source}."""
    import csv as csv_mod, bisect
    STALE_DAYS = 10

    def _dt(date_str):
        p = date_str.split("/")
        return datetime(int(p[2]), int(p[0]), int(p[1]))

    # Anchors already stored on daily records by report 2465 (have a 'grades' block)
    anchors = {}  # datetime -> (value, priority): 2 = report 2465, 1 = CSV
    api_n = 0
    for rec in daily:
        bc = rec.get("beef_comp")
        if bc and "grades" in bc and bc.get("cutout") is not None:
            anchors[_dt(rec["date"])] = (bc["cutout"], 2)
            api_n += 1

    # Historical CSV weekly anchors (report 2465 wins where both exist)
    csv_path = os.path.join(SCRIPT_DIR, "..", "data", "comp_cutout_historical.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "comp_cutout_historical.csv")
    csv_n = 0
    if os.path.exists(csv_path):
        with open(csv_path) as f:
            reader = csv_mod.reader(f)
            next(reader, None); next(reader, None)
            for row in reader:
                if not row or not row[0].strip() or "Reminder" in row[0]:
                    continue
                try:
                    dt = datetime.strptime(row[0].strip().replace(" 12:00:00 AM", ""), "%m/%d/%Y")
                    val = float(row[3].strip())
                except Exception:
                    continue
                if dt not in anchors:
                    anchors[dt] = (val, 1); csv_n += 1
    else:
        print("  comp_cutout_historical.csv not found")

    print(f"  comp anchors: {api_n} from report 2465, {csv_n} from CSV")
    if not anchors:
        return

    keys = sorted(anchors.keys())
    kept = filled = gaps = 0
    for rec in daily:
        bc = rec.get("beef_comp")
        if bc and "grades" in bc and bc.get("cutout") is not None:
            kept += 1
            continue  # preserve the authoritative 2465 record
        dt = _dt(rec["date"])
        i = bisect.bisect_right(keys, dt) - 1
        if i >= 0 and (dt - keys[i]).days <= STALE_DAYS:
            val, prio = anchors[keys[i]]
            rec["beef_comp"] = {"cutout": val, "source": "csv" if prio == 1 else "ffill"}
            filled += 1
        else:
            if rec.get("beef_comp"):
                rec["beef_comp"] = None
            gaps += 1
    print(f"  comp series: {kept} report-2465 days kept, {filled} forward-filled, {gaps} gaps (> {STALE_DAYS}d stale)")


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
    comp_val = comp_parsed.get("cutout") if comp_parsed else None
    comp_str = f", comp={comp_val}" if comp_val else ""
    print(f"beef={choice}, pork={carcass}{comp_str}")
    return record


def trading_days(start_date, end_date):
    """Generate trading days (Mon-Fri) between start and end."""
    d = start_date
    while d <= end_date:
        if d.weekday() < 5:  # Mon-Fri
            yield d
        d += timedelta(days=1)



def slim_daily_records(daily):
    """Remove verbose per-cut data from old records to reduce JSON size.
    Only keep individual cuts for the most recent 5 trading days."""
    if len(daily) < 10:
        return
    cut_keys = ["choice_cuts", "select_cuts", "choice_select_cuts", "ground_beef", "trimmings_2453",
                "loin_cuts", "butt_cuts", "picnic_cuts", "ham_cuts",
                "belly_cuts", "sparerib_cuts", "trim_cuts", "jowl_cuts",
                "variety_cuts", "added_ingredients_cuts"]
    keep_recent = 5
    for rec in daily[:-keep_recent]:
        beef = rec.get("beef", {})
        for k in cut_keys:
            beef.pop(k, None)
        pork = rec.get("pork", {})
        for k in cut_keys:
            pork.pop(k, None)
        # Slim beef_trimmings for old records but keep the Fresh 90% line —
        # it doubles as the "2451 already fetched" marker and preserves the
        # key FOB plant national boneless series in the raw daily history.
        bt = rec.get("beef_trimmings")
        if bt is not None and isinstance(bt.get("national"), list):
            keep = [it for it in bt["national"]
                    if it.get("name") and "Fresh" in it["name"] and "90%" in it["name"] and "92" not in it["name"]]
            bt["national"] = [{"name": it.get("name"), "avg": it.get("avg"), "lbs": it.get("lbs")} for it in keep]


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

    # Check earliest date in existing data
    earliest_date = None
    if existing.get("daily"):
        try:
            parts = existing["daily"][0]["date"].split("/")
            earliest_date = datetime(int(parts[2]), int(parts[0]), int(parts[1]))
        except: pass

    needs_deep_backfill = earliest_date is None or earliest_date > datetime(2021, 6, 1)
    if (cur_year_count < 200 and len(existing.get("daily", [])) < 1200) or needs_deep_backfill:
        # Backfill: fetch from Jan 2021 if data doesn't go back that far
        start = datetime(2021, 1, 4)
        print(f"\n  Backfill mode: fetching from {start.strftime('%m/%d/%Y')}")
        if earliest_date:
            print(f"  Current earliest record: {earliest_date.strftime('%m/%d/%Y')}")
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

    # ── Enrich older records with report 2451 (LM_XB401 boneless beef & trimmings) ──
    # The 2451 feed was added recently, so most historical records lack beef_trimmings.
    # Chip away at the gap each run (newest first, capped) so the FOB plant national
    # Fresh 90% series backfills across a few nightly runs without blowing up runtime.
    ENRICH_2451_CAP = 400
    _missing_2451 = [rec for rec in daily if (rec.get("beef_trimmings") or {}).get("national") is None]
    _missing_2451.sort(key=date_sort_key, reverse=True)
    if _missing_2451:
        _todo = _missing_2451[:ENRICH_2451_CAP]
        print(f"\n  Enriching {len(_todo)} of {len(_missing_2451)} records missing LM_XB401 trimmings...")
        _done = 0
        for rec in _todo:
            try:
                trims = fetch_report("2451", rec["date"])
                parsed = parse_beef_trimmings(trims)
                # Store an empty marker when the report had nothing for that date,
                # so we don't refetch it forever.
                rec["beef_trimmings"] = parsed if parsed else {"national": []}
                _done += 1
            except Exception as e:
                print(f"  ERROR enriching {rec['date']}: {e}")
            time.sleep(0.3)
        print(f"  Enriched {_done} records")

    # ── One-time grade rebuild ──
    # Old records are slimmed (no per-cut detail), so grade-separated seasonal
    # series can't be built for history from them directly. Re-fetch report 2453
    # once for those records; afterward the graded series persist via the seasonal
    # merge. Retries across runs until it completes (flag stored in seasonal).
    _ex_seasonal = existing.get("seasonal") or {}
    _grade_ready = bool(_ex_seasonal.get("cuts_beef_choice_complete"))
    if not _grade_ready:
        _stale = [r for r in daily if not (r.get("beef") or {}).get("choice_cuts")]
        if _stale:
            print(f"\n  One-time grade rebuild: re-fetching beef cut detail for {len(_stale)} records (report 2453)...")
            _ok = 0
            for r in _stale:
                try:
                    bp = parse_beef_cutout(fetch_report("2453", r["date"]))
                    if bp:
                        r.setdefault("beef", {})
                        for k in ("choice_cuts", "select_cuts", "choice_select_cuts", "ground_beef", "trimmings_2453"):
                            if bp.get(k):
                                r["beef"][k] = bp[k]
                        _ok += 1
                except Exception as e:
                    print(f"    ERROR rebuilding {r['date']}: {e}")
                time.sleep(0.15)
            print(f"  Grade rebuild: repopulated {_ok}/{len(_stale)} records")
            _grade_ready = _ok >= int(len(_stale) * 0.98)
        else:
            _grade_ready = True

    # Comprehensive cutout: rebuild the weekly series from report-2465 anchors
    # (preferred) and the historical CSV, forward-filled with a staleness cap.
    rebuild_comp_series(daily)

    # Build seasonal data for charts (pre-computed by year)
    # Pass existing seasonal so cut-level data survives incremental runs (historical records are slimmed)
    seasonal = build_seasonal_data(daily, existing.get("seasonal"))
    seasonal["cuts_beef_choice_complete"] = _grade_ready

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

    slim_daily_records(daily)
    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")
    return 0


def build_seasonal_data(daily, existing_seasonal=None):
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
    cut_codes = {}  # normalized cut name -> USDA/IMPS code (for the charting dropdown)

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

        # Beef primals (choice + select composites)
        for primal in ["Rib", "Chuck", "Round", "Loin", "Brisket", "Plate", "Flank"]:
            key = f"beef_{primal.lower()}"
            yr_data[key] = [
                r.get("beef", {}).get("primals", {}).get(primal, {}).get("choice")
                for r in yr_records
            ]
            yr_data[key + "_select"] = [
                r.get("beef", {}).get("primals", {}).get(primal, {}).get("select")
                for r in yr_records
            ]

        # Pork primals
        for primal in ["loin", "butt", "picnic", "rib", "ham", "belly"]:
            key = f"pork_{primal}"
            yr_data[key] = [r.get("pork", {}).get(primal) for r in yr_records]

        # ── Individual cut series (per-name arrays) ──
        # Normalize names to match how the app stores them in the table (strips " (xxx)" and leading IMPS prefix)
        import re as _re_cut
        def _norm_cut_name(name):
            if not name:
                return name
            # Drop trailing parenthesized group: "Round, outside round (171B 3)" -> "Round, outside round"
            n = _re_cut.sub(r"\s*\([^)]+\)", "", name)
            # Drop leading IMPS prefix like "123A 4 " that appears on choice_and_select items
            n = _re_cut.sub(r"^\s*\d+[A-Z]?\s+\d\s+", "", n)
            return n.strip()

        # Build a dict: name -> [value per day in this year] for beef and pork
        def build_item_series(yr_records, get_items_fn):
            """
            get_items_fn(record) returns a list of (name, avg) tuples for the record.
            Returns {name: [None or avg per day]}.
            """
            series = {}
            for idx, r in enumerate(yr_records):
                daily_map = {}
                for name, avg in get_items_fn(r):
                    if name and avg is not None:
                        daily_map[name] = avg
                for name, val in daily_map.items():
                    if name not in series:
                        series[name] = [None] * idx  # back-fill
                    series[name].append(val)
                # Missing names get None for this day
                seen = set(daily_map.keys())
                for name in list(series.keys()):
                    if name not in seen:
                        series[name].append(None)
            # Ensure all arrays have the same length as yr_records
            for name in series:
                while len(series[name]) < len(yr_records):
                    series[name].append(None)
            return series

        def beef_items(r):
            beef = r.get("beef", {}) or {}
            bt = r.get("beef_trimmings", {}) or {}
            out = []
            for section in ("choice_cuts", "select_cuts", "choice_select_cuts", "ground_beef", "trimmings_2453"):
                for it in beef.get(section, []) or []:
                    out.append((_norm_cut_name(it.get("name")), it.get("avg")))
            for it in bt.get("national", []) or []:
                out.append((_norm_cut_name(it.get("name")), it.get("avg")))
            return out

        def beef_items_graded(r):
            """Yield (name, grade, avg) where grade is 'choice', 'select', or 'both'.
            Ungraded items (combined C&S, ground beef, trimmings, boneless) count as
            'both' so they appear under either quality view."""
            beef = r.get("beef", {}) or {}
            bt = r.get("beef_trimmings", {}) or {}
            out = []
            for it in beef.get("choice_cuts", []) or []:
                out.append((_norm_cut_name(it.get("name")), "choice", it.get("avg")))
            for it in beef.get("select_cuts", []) or []:
                out.append((_norm_cut_name(it.get("name")), "select", it.get("avg")))
            for sec in ("choice_select_cuts", "ground_beef", "trimmings_2453"):
                for it in beef.get(sec, []) or []:
                    out.append((_norm_cut_name(it.get("name")), "both", it.get("avg")))
            for it in bt.get("national", []) or []:
                out.append((_norm_cut_name(it.get("name")), "both", it.get("avg")))
            return out

        def build_graded_series(yr_records):
            """Like build_item_series but splits beef into (choice, select) dicts."""
            choice, select = {}, {}
            def _add(series, idx, dmap):
                for name, val in dmap.items():
                    if name not in series:
                        series[name] = [None] * idx
                    series[name].append(val)
                seen = set(dmap.keys())
                for name in list(series.keys()):
                    if name not in seen:
                        series[name].append(None)
            for idx, r in enumerate(yr_records):
                cmap, smap = {}, {}
                for name, grade, avg in beef_items_graded(r):
                    if not name or avg is None:
                        continue
                    if grade in ("choice", "both"):
                        cmap[name] = avg
                    if grade in ("select", "both"):
                        smap[name] = avg
                _add(choice, idx, cmap)
                _add(select, idx, smap)
            for series in (choice, select):
                for name in series:
                    while len(series[name]) < len(yr_records):
                        series[name].append(None)
            return choice, select

        def pork_items(r):
            pork = r.get("pork", {}) or {}
            out = []
            for section in ("loin_cuts", "butt_cuts", "picnic_cuts", "ham_cuts",
                            "belly_cuts", "sparerib_cuts", "trim_cuts", "jowl_cuts",
                            "variety_cuts", "added_ingredients_cuts"):
                for it in pork.get(section, []) or []:
                    out.append((_norm_cut_name(it.get("name")), it.get("avg")))
            return out

        yr_data["cuts_beef"] = build_item_series(yr_records, beef_items)
        yr_data["cuts_pork"] = build_item_series(yr_records, pork_items)
        _cb_choice, _cb_select = build_graded_series(yr_records)
        yr_data["cuts_beef_choice"] = _cb_choice
        yr_data["cuts_beef_select"] = _cb_select

        # Capture USDA/IMPS codes from raw names (e.g. "112A  3") for the charting
        # dropdown. Best-effort now; complete after the one-time grade rebuild.
        for r in yr_records:
            beef = r.get("beef", {}) or {}
            for sec in ("choice_cuts", "select_cuts", "choice_select_cuts"):
                for it in beef.get(sec, []) or []:
                    raw = it.get("name") or ""
                    m = _re_cut.search(r"\(([^)]+)\)\s*$", raw)
                    if m:
                        nm = _norm_cut_name(raw)
                        if nm and nm not in cut_codes:
                            cut_codes[nm] = " ".join(m.group(1).split())

        # Keep trim_beef / trim_pork as aliases for backward compatibility with existing app code
        yr_data["trim_beef"] = yr_data["cuts_beef"]
        yr_data["trim_pork"] = yr_data["cuts_pork"]

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

    # ── Merge cuts_beef / cuts_pork from previous seasonal (historical cut data survives slimming) ──
    if existing_seasonal and isinstance(existing_seasonal.get("years"), list):
        # Build a lookup for the new seasonal by year
        new_yr_map = {y.get("year"): y for y in seasonal["years"] if isinstance(y.get("year"), int)}
        for old_y in existing_seasonal["years"]:
            if not isinstance(old_y.get("year"), int):
                continue
            yr = old_y["year"]
            new_y = new_yr_map.get(yr)
            if not new_y:
                continue
            # For each cut-item series map, merge day-by-day.
            # Align by date_label. If new record has a non-null value at a given day, use it;
            # otherwise carry forward the old value.
            for map_key in ("cuts_beef", "cuts_pork", "trim_beef", "trim_pork", "cuts_beef_choice", "cuts_beef_select"):
                old_map = old_y.get(map_key) or {}
                new_map = new_y.get(map_key) or {}
                # Use dates array for alignment
                old_dates = old_y.get("dates") or []
                new_dates = new_y.get("dates") or []
                merged = {}
                all_names = set(list(old_map.keys()) + list(new_map.keys()))
                for name in all_names:
                    old_arr = old_map.get(name, [None] * len(old_dates))
                    new_arr = new_map.get(name, [None] * len(new_dates))
                    # Build merged array aligned to new_dates (the current shape)
                    out = []
                    for i, d in enumerate(new_dates):
                        new_val = new_arr[i] if i < len(new_arr) else None
                        if new_val is not None:
                            out.append(new_val)
                        else:
                            # Find this date in old_dates
                            try:
                                j = old_dates.index(d)
                                out.append(old_arr[j] if j < len(old_arr) else None)
                            except ValueError:
                                out.append(None)
                    merged[name] = out
                new_y[map_key] = merged

    # Union cut codes with previously stored ones (fresh/rebuilt entries win)
    if existing_seasonal and isinstance(existing_seasonal.get("cut_codes"), dict):
        merged_codes = dict(existing_seasonal["cut_codes"])
        merged_codes.update(cut_codes)
        cut_codes = merged_codes
    seasonal["cut_codes"] = cut_codes

    return seasonal


if __name__ == "__main__":
    sys.exit(main())
