#!/usr/bin/env python3
"""
Fetch CFTC Commitments of Traders (Disaggregated, Futures+Options Combined) data.
Downloads yearly zip files from CFTC, parses for our commodities, and outputs cot.json.

Source: https://www.cftc.gov/files/dea/history/com_disagg_txt_{YYYY}.zip
Each zip contains a CSV with all weekly reports for that year.

Fetches 10+ years for historical band charts + current year for latest positions.
"""

import csv, io, json, os, sys, zipfile, urllib.request, urllib.error, time
from datetime import datetime, timedelta
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

CFTC_URL = "https://www.cftc.gov/files/dea/history/com_disagg_txt_{year}.zip"

# Map CFTC Market_and_Exchange_Names to our IDs
# The CFTC CSV has the commodity name and exchange in one field
COMMODITY_MAP = {
    "CORN": "cot-corn",
    "WHEAT-SRW": "cot-chi-wheat",
    "SOYBEANS": "cot-soybeans",
    "WHEAT-HRW": "cot-kc-wheat",
    "WHEAT-HRSPRING": "cot-mpls-wheat",
    "SOYBEAN OIL": "cot-oil",
    "SOYBEAN MEAL": "cot-meal",
    "LIVE CATTLE": "cot-live-cattle",
    "FEEDER CATTLE": "cot-feeder-cattle",
    "LEAN HOGS": "cot-lean-hogs",
    "CRUDE OIL, LIGHT SWEET": "cot-crude-oil",
    "NY HARBOR ULSD": "cot-heating-oil",
    "NATURAL GAS": "cot-nat-gas",
}

COMMODITY_META = {
    "cot-corn":          {"label": "Corn",           "exchange": "CBOT", "contract": "5,000 bu"},
    "cot-chi-wheat":     {"label": "Wheat (SRW)",    "exchange": "CBOT", "contract": "5,000 bu"},
    "cot-soybeans":      {"label": "Soybeans",       "exchange": "CBOT", "contract": "5,000 bu"},
    "cot-kc-wheat":      {"label": "KC Wheat (HRW)", "exchange": "KCBT", "contract": "5,000 bu"},
    "cot-mpls-wheat":    {"label": "MN Wheat (HRS)", "exchange": "MGEX", "contract": "5,000 bu"},
    "cot-oil":           {"label": "Soybean Oil",    "exchange": "CBOT", "contract": "60,000 lbs"},
    "cot-meal":          {"label": "Soybean Meal",   "exchange": "CBOT", "contract": "100 tons"},
    "cot-live-cattle":   {"label": "Live Cattle",    "exchange": "CME",  "contract": "40,000 lbs"},
    "cot-feeder-cattle": {"label": "Feeder Cattle",  "exchange": "CME",  "contract": "50,000 lbs"},
    "cot-lean-hogs":     {"label": "Lean Hogs",      "exchange": "CME",  "contract": "40,000 lbs"},
    "cot-crude-oil":     {"label": "Crude Oil",      "exchange": "NYMEX","contract": "1,000 bbl"},
    "cot-heating-oil":   {"label": "Heating Oil",    "exchange": "NYMEX","contract": "42,000 gal"},
    "cot-nat-gas":       {"label": "Natural Gas",    "exchange": "NYMEX","contract": "10,000 MMBtu"},
}

CURRENT_YEAR = datetime.utcnow().year
START_YEAR = 2006  # First year of CFTC disaggregated report
BAND_YEARS = 10  # Use most recent N years for seasonal band charts


def download_cftc_zip(year):
    """Download and extract CFTC disaggregated combined F+O zip for a given year."""
    url = CFTC_URL.format(year=year)
    print(f"  Downloading {year}...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
            print(f"{len(data):,} bytes", end=" ", flush=True)
            zf = zipfile.ZipFile(io.BytesIO(data))
            # The zip contains one CSV file
            csv_name = zf.namelist()[0]
            csv_data = zf.read(csv_name).decode("utf-8", errors="replace")
            lines = csv_data.strip().split("\n")
            print(f"→ {len(lines)-1} rows")
            return lines
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def identify_commodity(market_name):
    """Match CFTC market name to our commodity ID."""
    name_upper = market_name.upper().strip()
    # Try exact prefix match
    for cftc_name, cot_id in COMMODITY_MAP.items():
        if name_upper.startswith(cftc_name):
            return cot_id
    return None


def parse_cftc_csv(lines):
    """Parse CFTC CSV lines into weekly records per commodity.
    Returns: {cot_id: [{date, prod_long, prod_short, swap_long, swap_short,
                        mm_long, mm_short, other_long, other_short, oi}, ...]}
    sorted by date ascending.
    """
    reader = csv.DictReader(lines)
    records = defaultdict(list)

    for row in reader:
        market = row.get("Market_and_Exchange_Names", "")
        cot_id = identify_commodity(market)
        if not cot_id:
            continue

        # Parse the report date
        date_str = row.get("Report_Date_as_YYYY-MM-DD", row.get("As_of_Date_In_Form_YYYYMMDD", ""))
        if not date_str:
            continue

        try:
            prod_long = int(row.get("Prod_Merc_Positions_Long_All", 0))
            prod_short = int(row.get("Prod_Merc_Positions_Short_All", 0))
            swap_long = int(row.get("Swap_Positions_Long_All", row.get("Swap__Positions_Long_All", 0)))
            swap_short = int(row.get("Swap_Positions_Short_All", row.get("Swap__Positions_Short_All", 0)))
            mm_long = int(row.get("M_Money_Positions_Long_All", 0))
            mm_short = int(row.get("M_Money_Positions_Short_All", 0))
            other_long = int(row.get("Other_Rept_Positions_Long_All", 0))
            other_short = int(row.get("Other_Rept_Positions_Short_All", 0))
            oi = int(row.get("Open_Interest_All", 0))
        except (ValueError, TypeError):
            continue

        records[cot_id].append({
            "date": date_str,
            "prod_long": prod_long,
            "prod_short": prod_short,
            "prod_net": prod_long - prod_short,
            "swap_long": swap_long,
            "swap_short": swap_short,
            "swap_net": swap_long - swap_short,
            "mm_long": mm_long,
            "mm_short": mm_short,
            "mm_net": mm_long - mm_short,
            "other_long": other_long,
            "other_short": other_short,
            "other_net": other_long - other_short,
            "oi": oi,
        })

    # Sort each commodity by date
    for cot_id in records:
        records[cot_id].sort(key=lambda r: r["date"])

    return dict(records)


def compute_week_number(date_str):
    """Convert date to ISO week number (1-52/53)."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.isocalendar()[1]
    except:
        return None


def build_bands(all_years_data, cot_id, field):
    """Build min/max/median bands from historical data for a given field.
    Groups by ISO week number across all years.
    Returns: {week_num: {min, max, median}} for weeks 1-52.
    """
    by_week = defaultdict(list)
    for year_records in all_years_data:
        for rec in year_records.get(cot_id, []):
            wk = compute_week_number(rec["date"])
            if wk and wk <= 52:
                by_week[wk].append(rec[field])

    bands = {}
    for wk in range(1, 53):
        vals = sorted(by_week.get(wk, []))
        if vals:
            bands[wk] = {
                "min": vals[0],
                "max": vals[-1],
                "median": vals[len(vals) // 2],
            }
    return bands


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "cot.json")

    print("=" * 60)
    print("CFTC COT Data Fetch")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print(f"Full history: {START_YEAR} to {CURRENT_YEAR}")
    print(f"Band charts: last {BAND_YEARS} years")
    print("=" * 60)

    # Fetch all years from 2006
    all_years_parsed = {}  # {year: parsed_dict} for band building
    all_records = defaultdict(list)  # combined records across all years
    
    for year in range(START_YEAR, CURRENT_YEAR + 1):
        lines = download_cftc_zip(year)
        if lines:
            parsed = parse_cftc_csv(lines)
            all_years_parsed[year] = parsed
            for cot_id, recs in parsed.items():
                all_records[cot_id].extend(recs)
        time.sleep(0.5)

    if not all_records:
        print("ERROR: No data fetched")
        return 1

    # Sort combined records
    for cot_id in all_records:
        all_records[cot_id].sort(key=lambda r: r["date"])

    # Build output
    print(f"\n-- Building COT output --")

    # How many recent weeks to include in the weekly series
    RECENT_WEEKS = 52  # ~1 year of weekly data for the summary table and charts

    cot_output = {}
    for cot_id, meta in COMMODITY_META.items():
        recs = all_records.get(cot_id, [])
        if not recs:
            print(f"  {cot_id}: no data")
            continue

        # Recent weekly series (last N weeks)
        recent = recs[-RECENT_WEEKS:] if len(recs) > RECENT_WEEKS else recs

        # Latest and previous for change calculation
        latest = recent[-1] if recent else None
        prev = recent[-2] if len(recent) >= 2 else None

        if not latest:
            continue

        # Week-over-week changes
        prod_chg = latest["prod_net"] - prev["prod_net"] if prev else 0
        swap_chg = latest["swap_net"] - prev["swap_net"] if prev else 0
        mm_chg = latest["mm_net"] - prev["mm_net"] if prev else 0
        other_chg = latest["other_net"] - prev["other_net"] if prev else 0
        oi_chg = latest["oi"] - prev["oi"] if prev else 0

        # Weekly series arrays (for charts)
        dates = [r["date"] for r in recent]
        mm_net_series = [r["mm_net"] for r in recent]
        mm_long_series = [r["mm_long"] for r in recent]
        mm_short_series = [r["mm_short"] for r in recent]
        prod_net_series = [r["prod_net"] for r in recent]
        prod_long_series = [r["prod_long"] for r in recent]
        prod_short_series = [r["prod_short"] for r in recent]
        swap_net_series = [r["swap_net"] for r in recent]
        swap_long_series = [r["swap_long"] for r in recent]
        swap_short_series = [r["swap_short"] for r in recent]
        other_net_series = [r["other_net"] for r in recent]
        other_long_series = [r["other_long"] for r in recent]
        other_short_series = [r["other_short"] for r in recent]
        oi_series = [r["oi"] for r in recent]

        # Build yearly data for multi-year line charts
        # Group records by calendar year, then assign ordinal position within year
        yearly = defaultdict(list)
        fields_to_track = ["mm_net", "mm_long", "mm_short", "prod_net", "prod_long", "prod_short",
                           "swap_net", "swap_long", "swap_short", "other_net", "other_long", "other_short", "oi"]
        by_year_recs = defaultdict(list)
        for rec in recs:
            try:
                dt = datetime.strptime(rec["date"], "%Y-%m-%d")
                by_year_recs[dt.year].append(rec)
            except: pass

        for yr in by_year_recs:
            by_year_recs[yr].sort(key=lambda r: r["date"])

        # Build yearly data using simple day-of-year week index on Tuesday cutoff
        # week_index = (day_of_year - 1) // 7 → 0-52
        # Jan 1-7 = index 0, Jan 8-14 = index 1, ..., Dec 25-31 = index 51 or 52
        def get_tuesday(report_date):
            """Get the Tuesday of the report week (data cutoff day)."""
            days_since_tue = (report_date.weekday() - 1) % 7
            return report_date - timedelta(days=days_since_tue)

        def week_index(dt):
            """Simple week index: (day_of_year - 1) // 7 → 0-52."""
            return (dt.timetuple().tm_yday - 1) // 7

        NUM_SLOTS = 53  # indices 0-52

        yearly_out = {}
        for yr, yr_recs in sorted(by_year_recs.items()):
            by_week = {}
            for rec in yr_recs:
                try:
                    dt = datetime.strptime(rec["date"], "%Y-%m-%d")
                    tue = get_tuesday(dt)
                    # Use the Tuesday's year for indexing (handles late-Dec edge cases)
                    if tue.year != yr:
                        continue  # skip if Tuesday falls in different year
                    wi = min(week_index(tue), NUM_SLOTS - 1)
                    by_week[wi] = rec
                except: pass

            year_data = {}
            for f in fields_to_track:
                year_data[f] = [by_week[w].get(f) if w in by_week else None for w in range(NUM_SLOTS)]
            yearly_out[str(yr)] = year_data

        # Build median from ALL years
        medians = {}
        all_years_list = sorted(yearly_out.keys())
        for f in fields_to_track:
            by_week = defaultdict(list)
            for yr_key in all_years_list:
                vals = yearly_out[yr_key].get(f, [])
                for w, v in enumerate(vals):
                    if v is not None:
                        by_week[w].append(v)
            med_vals = []
            for w in range(NUM_SLOTS):
                vals = sorted(by_week.get(w, []))
                med_vals.append(vals[len(vals)//2] if vals else None)
            medians[f] = med_vals

        # Compute record long and short from ALL history (back to 2006)
        all_mm_long = [r["mm_long"] for r in recs]
        all_mm_short = [r["mm_short"] for r in recs]
        rec_long = max(all_mm_long) if all_mm_long else latest["mm_long"]
        rec_short = min([-s for s in all_mm_short]) if all_mm_short else -abs(latest["mm_short"])
        # rec_short stored as negative (short position convention)

        cot_output[cot_id] = {
            **meta,
            "latest_date": latest["date"],
            "producer": {
                "net": prod_net_series, "long": prod_long_series, "short": prod_short_series,
                "chg": prod_chg,
            },
            "swap": {
                "net": swap_net_series, "long": swap_long_series, "short": swap_short_series,
                "chg": swap_chg,
            },
            "managed": {
                "net": mm_net_series, "long": mm_long_series, "short": mm_short_series,
                "chg": mm_chg,
                "recLong": rec_long,
                "recShort": rec_short,
            },
            "other": {
                "net": other_net_series, "long": other_long_series, "short": other_short_series,
                "chg": other_chg,
            },
            "oi": {
                "net": oi_series,
                "chg": oi_chg,
            },
            "dates": dates,
            "yearly": yearly_out,
            "medians": medians,
            "available_years": sorted(yearly_out.keys()),
        }

        print(f"  {cot_id}: {len(recent)} wks, {len(yearly_out)} yrs, latest {latest['date']}, MM net={latest['mm_net']:,}, recL={rec_long:,}, recS={rec_short:,}")

    # Output
    result = {
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "weeks": dates[-20:] if dates else [],  # last 20 week labels for summary
        "data": cot_output,
    }

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")

    return 0


if __name__ == "__main__":
    sys.exit(main())
