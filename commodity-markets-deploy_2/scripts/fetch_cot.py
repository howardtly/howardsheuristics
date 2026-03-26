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
# We match the commodity portion (before " - EXCHANGE") exactly.
# Multiple aliases handle name changes over the years.
COMMODITY_MAP = {
    # Grains (consistent names)
    "CORN": "cot-corn",
    "SOYBEANS": "cot-soybeans",
    "SOYBEAN OIL": "cot-oil",
    "SOYBEAN MEAL": "cot-meal",
    "WHEAT-SRW": "cot-chi-wheat",
    "WHEAT SRW": "cot-chi-wheat",
    "WHEAT": "cot-chi-wheat",          # pre-2013 files use just "WHEAT"
    "WHEAT-HRW": "cot-kc-wheat",
    "WHEAT HRW": "cot-kc-wheat",
    "WHEAT-HRSPRING": "cot-mpls-wheat",
    "WHEAT HRSPRING": "cot-mpls-wheat",
    # Livestock (consistent names)
    "LIVE CATTLE": "cot-live-cattle",
    "FEEDER CATTLE": "cot-feeder-cattle",
    "LEAN HOGS": "cot-lean-hogs",
    # Crude oil — name changed ~2023 (prefix fallback handles variants)
    "CRUDE OIL, LIGHT SWEET": "cot-crude-oil",
    "CRUDE OIL, LIGHT SWEET (WTI)": "cot-crude-oil",
    # Heating oil — name changed ~2013
    "NY HARBOR ULSD": "cot-heating-oil",
    "NO 2 HEATING OIL  NY HARBOR": "cot-heating-oil",
    "NO. 2 HEATING OIL, NY HARBOR": "cot-heating-oil",
    # Natural gas — name changed ~2023
    # NOTE: "NATURAL GAS ICE HENRY HUB" is a different ICE contract, do NOT include
    "NATURAL GAS": "cot-nat-gas",
    "HENRY HUB NATURAL GAS": "cot-nat-gas",
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
START_YEAR = 2010  # CFTC disaggregated combined data starts 2010
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


_unmatched_names = set()
_natgas_matches = set()  # Track what market names match nat gas

# Prefix fallback for commodities with many name variants
_PREFIX_MAP = [
    ("CRUDE OIL", "cot-crude-oil"),
    ("NO 2 HEATING OIL", "cot-heating-oil"),
    ("NO. 2 HEATING OIL", "cot-heating-oil"),
    ("HEATING OIL", "cot-heating-oil"),
    ("HENRY HUB NAT", "cot-nat-gas"),       # catches "HENRY HUB NATURAL GAS", "HENRY HUB NAT GAS", etc.
    ("HENRY HUB NG", "cot-nat-gas"),
    ("NATURAL GAS", "cot-nat-gas"),        # catches NYMEX variants but ICE excluded below
]

# Words that indicate a derivative/sub-product, not the main contract
_EXCLUDE_WORDS = {"OPTION", "SWAP", "SPREAD", "CALENDAR", "CAL ", "BASIS",
                  "CRACK", "FIN ", "FINANCIAL", "MINI", "AVG PRICE",
                  "LAST DAY", "ICE", "BALMO", "BRENT", "DUBAI", "CANADIAN",
                  "EUR STYLE", "BIODIESEL", "GASOIL", "FUEL OIL", "NET ENRGY"}

def identify_commodity(market_name):
    """Match CFTC market name to our commodity ID using exact commodity name matching."""
    full_name = market_name.strip()
    full_upper = full_name.upper()
    
    # First try exact match on full name
    if full_upper in COMMODITY_MAP:
        return COMMODITY_MAP[full_upper]
    
    # Extract commodity portion (before " - EXCHANGE")
    if " - " in full_name:
        commodity_part = full_name.split(" - ")[0].strip().upper()
    else:
        commodity_part = full_upper
    
    # Exact match on commodity portion
    if commodity_part in COMMODITY_MAP:
        result = COMMODITY_MAP[commodity_part]
        if result == "cot-nat-gas":
            _natgas_matches.add(commodity_part)
        return result
    
    # Prefix fallback for energy names that vary across years
    for prefix, cot_id in _PREFIX_MAP:
        if commodity_part.startswith(prefix):
            # Exclude derivative products (options, swaps, spreads, etc.)
            if any(excl in commodity_part for excl in _EXCLUDE_WORDS):
                break
            if cot_id == "cot-nat-gas":
                _natgas_matches.add(commodity_part)
            return cot_id
    
    # Track unmatched for debugging
    if commodity_part not in _unmatched_names and len(_unmatched_names) < 200:
        _unmatched_names.add(commodity_part)
    
    return None


def parse_cftc_csv(lines, year=None):
    """Parse CFTC CSV lines into weekly records per commodity.
    Handles column name differences between old (2006-2012) and new (2013+) CFTC files.
    Returns: {cot_id: [{date, prod_long, prod_short, ...}, ...]}
    """
    # Normalize headers: strip whitespace from the header line
    if lines:
        lines[0] = ",".join(h.strip() for h in lines[0].split(","))

    reader = csv.DictReader(lines)
    records = defaultdict(list)

    # Get actual column names from the CSV header
    fieldnames = reader.fieldnames or []

    # Helper to find a column by trying multiple names
    def find_col(row, *candidates):
        for c in candidates:
            val = row.get(c)
            if val is not None and val != "":
                return val
        return None

    # Log column names for first year to help debug
    if year and year <= 2007:
        matching_cols = [c for c in fieldnames if any(kw in c.lower() for kw in ["money", "prod", "swap", "date", "market", "open_int"])]
        print(f"    Key columns ({year}): {matching_cols[:15]}")

    matched_count = 0
    for row in reader:
        # Market name column
        market = find_col(row, "Market_and_Exchange_Names", "Market and Exchange Names",
                          "Market_and_Exchange_Names ", "Contract_Market_Name")
        if not market:
            continue
        cot_id = identify_commodity(market)
        if not cot_id:
            continue

        # Date column — different names across eras
        # 2010-2012: Report_Date_as_MM_DD_YYYY (underscores), As_of_Date_In_Form_YYMMDD (6-digit)
        # 2013+: Report_Date_as_YYYY-MM-DD (dashes)
        date_str = find_col(row, "Report_Date_as_YYYY-MM-DD", "Report_Date_as_MM_DD_YYYY",
                            "Report_Date_as_MM-DD-YYYY",
                            "As_of_Date_In_Form_YYYYMMDD", "As_of_Date_In_Form_YYYY-MM-DD",
                            "As_of_Date_In_Form_YYMMDD",
                            "Report_Date_as_YYYY_MM_DD")
        if not date_str:
            continue

        # Normalize date format to YYYY-MM-DD
        date_str = date_str.strip()
        if len(date_str) == 10 and date_str[2] in "-_/" and date_str[5] in "-_/":
            # MM-DD-YYYY or MM_DD_YYYY -> YYYY-MM-DD
            date_str = date_str[6:10] + "-" + date_str[0:2] + "-" + date_str[3:5]
        elif len(date_str) == 8 and date_str.isdigit():
            # YYYYMMDD -> YYYY-MM-DD
            date_str = date_str[0:4] + "-" + date_str[4:6] + "-" + date_str[6:8]
        elif len(date_str) == 6 and date_str.isdigit():
            # YYMMDD -> YYYY-MM-DD
            yy = int(date_str[0:2])
            century = "20" if yy < 50 else "19"
            date_str = century + date_str[0:2] + "-" + date_str[2:4] + "-" + date_str[4:6]

        try:
            # Position columns — try multiple name variants
            prod_long = int(find_col(row, "Prod_Merc_Positions_Long_All", "Prod_Merc_Positions_Long_ALL",
                                      "Prod_Merc_Positions_Long_Other") or 0)
            prod_short = int(find_col(row, "Prod_Merc_Positions_Short_All", "Prod_Merc_Positions_Short_ALL",
                                       "Prod_Merc_Positions_Short_Other") or 0)
            swap_long = int(find_col(row, "Swap_Positions_Long_All", "Swap__Positions_Long_All",
                                      "Swap_Positions_Long_ALL", "Swap__Positions_Long_ALL") or 0)
            swap_short = int(find_col(row, "Swap_Positions_Short_All", "Swap__Positions_Short_All",
                                       "Swap_Positions_Short_ALL", "Swap__Positions_Short_ALL") or 0)
            mm_long = int(find_col(row, "M_Money_Positions_Long_All", "M_Money_Positions_Long_ALL") or 0)
            mm_short = int(find_col(row, "M_Money_Positions_Short_All", "M_Money_Positions_Short_ALL") or 0)
            other_long = int(find_col(row, "Other_Rept_Positions_Long_All", "Other_Rept_Positions_Long_ALL") or 0)
            other_short = int(find_col(row, "Other_Rept_Positions_Short_All", "Other_Rept_Positions_Short_ALL") or 0)
            oi = int(find_col(row, "Open_Interest_All", "Open_Interest_ALL", "Open_Interest_All ") or 0)
        except (ValueError, TypeError):
            continue

        matched_count += 1
        records[cot_id].append({
            "date": date_str,
            "prod_long": prod_long, "prod_short": prod_short,
            "prod_net": prod_long - prod_short,
            "swap_long": swap_long, "swap_short": swap_short,
            "swap_net": swap_long - swap_short,
            "mm_long": mm_long, "mm_short": mm_short,
            "mm_net": mm_long - mm_short,
            "other_long": other_long, "other_short": other_short,
            "other_net": other_long - other_short,
            "oi": oi,
        })

    if year:
        ids_found = sorted(set(records.keys()))
        print(f"    {year}: {matched_count} matched rows → {len(ids_found)} commodities: {', '.join(ids_found[:8])}{'...' if len(ids_found) > 8 else ''}")
        if matched_count == 0:
            print(f"    WARNING: 0 matches for {year}! All column names: {fieldnames[:20]}")
            # Also show a sample market name from the file
            reader2 = csv.DictReader(lines)
            sample_markets = set()
            for i, row2 in enumerate(reader2):
                m = None
                for cand in ["Market_and_Exchange_Names", "Market and Exchange Names", "Contract_Market_Name"]:
                    m = row2.get(cand)
                    if m: break
                if m and len(sample_markets) < 5:
                    sample_markets.add(m.split(" - ")[0].strip())
                if i > 50: break
            print(f"    Sample commodity names: {sample_markets}")

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
            parsed = parse_cftc_csv(lines, year=year)
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

        # Build yearly data using ISO week numbering (matches Excel's isocalendar / ISOWEEKNUM)
        # The ISO year handles year boundaries correctly:
        #   Dec 30, 2024 → ISO year 2025, week 1
        #   Dec 28, 2025 → ISO year 2025, week 52
        # CFTC report dates are already Tuesdays (data cutoff day)
        fields_to_track = ["mm_net", "mm_long", "mm_short", "prod_net", "prod_long", "prod_short",
                           "swap_net", "swap_long", "swap_short", "other_net", "other_long", "other_short", "oi"]
        NUM_SLOTS = 53  # ISO weeks 1-53, stored at indices 0-52

        yearly_out = {}
        for rec in recs:
            try:
                dt = datetime.strptime(rec["date"], "%Y-%m-%d")
                iso_yr, iso_wk, _ = dt.isocalendar()
                yr_key = str(iso_yr)
                if yr_key not in yearly_out:
                    yearly_out[yr_key] = {}
                    for f in fields_to_track:
                        yearly_out[yr_key][f] = [None] * NUM_SLOTS
                idx = iso_wk - 1  # week 1 → index 0
                if 0 <= idx < NUM_SLOTS:
                    for f in fields_to_track:
                        yearly_out[yr_key][f][idx] = rec.get(f)
            except: pass

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

        # Compute record long and short from ALL history
        # Record long = highest net long (most positive mm_net)
        # Record short = deepest net short (most negative mm_net)
        all_mm_net = [r["mm_net"] for r in recs]
        rec_long = max(all_mm_net) if all_mm_net else latest["mm_net"]
        rec_short = min(all_mm_net) if all_mm_net else latest["mm_net"]

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

        # Debug: print corn 2025 first 12 weeks for verification
        if cot_id == "cot-corn" and "2025" in yearly_out:
            corn_25 = yearly_out["2025"]["mm_net"][:12]
            print(f"    Corn 2025 MM net wks 1-12: {corn_25}")

    # Debug: nat gas market names that matched
    if _natgas_matches:
        print(f"\n  Nat gas matched market names: {sorted(_natgas_matches)}")

    # Log unmatched commodity names (helps find CFTC name changes)
    if _unmatched_names:
        print(f"\n  Unmatched CFTC commodity names ({len(_unmatched_names)}):")
        # Prioritize energy-related unmatched names
        energy_kw = ["OIL", "GAS", "CRUDE", "HEAT", "PETROL", "FUEL", "ULSD", "WTI", "HENRY"]
        energy_unmatched = sorted([n for n in _unmatched_names if any(kw in n.upper() for kw in energy_kw)])
        other_unmatched = sorted([n for n in _unmatched_names if n not in energy_unmatched])
        if energy_unmatched:
            print(f"    Energy-related ({len(energy_unmatched)} total):")
            for n in energy_unmatched[:30]:
                print(f"      {n}")
        for n in other_unmatched[:15]:
            print(f"    {n}")

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
