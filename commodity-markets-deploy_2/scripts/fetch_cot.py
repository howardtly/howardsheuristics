#!/usr/bin/env python3
"""
Fetch CFTC Commitments of Traders (Disaggregated, Futures+Options Combined) data.
Downloads yearly zip files from CFTC, parses for our commodities, and outputs cot.json.

Source: https://www.cftc.gov/files/dea/history/com_disagg_txt_{YYYY}.zip
Each zip contains a CSV with all weekly reports for that year.

Fetches 10+ years for historical band charts + current year for latest positions.

Two ways to run:

  python fetch_cot.py            Rebuild cot.json right now from whatever CFTC has.

  python fetch_cot.py --watch    Wait for CFTC to publish a report newer than the one
                                 already in cot.json, then rebuild immediately. Meant to
                                 be started ahead of the 3:30 PM ET release. If nothing
                                 new appears by the give-up time the file is left
                                 untouched. Makes no assumption about WHICH days CFTC
                                 publishes, so holiday-delayed and twice-weekly releases
                                 are picked up the same way.

Either way, cot.json is never overwritten with something older or less complete than
what is already published.
"""

import argparse, csv, io, json, os, sys, zipfile, urllib.request, urllib.error, time
from datetime import datetime, timedelta, timezone
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
    "WHEAT-HRW": "cot-kc-wheat",
    "WHEAT HRW": "cot-kc-wheat",
    "WHEAT-HRSPRING": "cot-mpls-wheat",
    "WHEAT HRSPRING": "cot-mpls-wheat",
    # Livestock (consistent names)
    "LIVE CATTLE": "cot-live-cattle",
    "FEEDER CATTLE": "cot-feeder-cattle",
    "LEAN HOGS": "cot-lean-hogs",
    # Dairy — CME Class III Milk and Cash-Settled Cheese
    # Current CFTC name: "MILK, Class III" (matched uppercase). Aliases guard old variants.
    "MILK, CLASS III": "cot-class3-milk",
    "MILK CLASS III": "cot-class3-milk",
    "CLASS III MILK": "cot-class3-milk",
    # Current CFTC name: "CHEESE (CASH-SETTLED)". Cheese futures launched mid-2010.
    "CHEESE (CASH-SETTLED)": "cot-cheese",
    "CHEESE (CASH SETTLED)": "cot-cheese",
    "CHEESE-CASH SETTLED": "cot-cheese",
    "CHEESE, CASH-SETTLED": "cot-cheese",
    # Crude oil — renamed post-2022
    # NOTE: "CRUDE OIL, LIGHT SWEET-WTI" is a different smaller contract — do NOT include
    "CRUDE OIL, LIGHT SWEET": "cot-crude-oil",
    "WTI-PHYSICAL": "cot-crude-oil",
    # Heating oil — name changed multiple times
    "NY HARBOR ULSD": "cot-heating-oil",
    "NO 2 HEATING OIL  NY HARBOR": "cot-heating-oil",
    "NO. 2 HEATING OIL, NY HARBOR": "cot-heating-oil",
    "NO. 2 HEATING OIL, N.Y. HARBOR": "cot-heating-oil",
    "#2 HEATING OIL, NY HARBOR-ULSD": "cot-heating-oil",
    "#2 HEATING OIL- NY HARBOR-ULSD": "cot-heating-oil",
    # Natural gas — renamed post-2022
    "NATURAL GAS": "cot-nat-gas",
    "HENRY HUB NATURAL GAS": "cot-nat-gas",
    "NAT GAS NYME": "cot-nat-gas",
    # NOTE: "HENRY HUB", "NAT GAS ICE LD1" are different contracts — do NOT include
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
    "cot-class3-milk":   {"label": "Class III Milk", "exchange": "CME",  "contract": "200,000 lbs"},
    "cot-cheese":        {"label": "Cash-Settled Cheese", "exchange": "CME", "contract": "20,000 lbs"},
    "cot-crude-oil":     {"label": "Crude Oil",      "exchange": "NYMEX","contract": "1,000 bbl"},
    "cot-heating-oil":   {"label": "Heating Oil",    "exchange": "NYMEX","contract": "42,000 gal"},
    "cot-nat-gas":       {"label": "Natural Gas",    "exchange": "NYMEX","contract": "10,000 MMBtu"},
}

CURRENT_YEAR = datetime.utcnow().year
START_YEAR = 2010  # CFTC disaggregated combined data starts 2010
BAND_YEARS = 10  # Use most recent N years for seasonal band charts


# Ask for an uncached copy when checking for a just-released report. If CFTC's
# servers ever reject the extra query string we notice and stop sending it.
_cache_bust_ok = True


def _fetch_year(year, fresh=False, validators=None, conditional=True, quiet=False):
    """Fetch one yearly CFTC zip. Returns (status, lines):

      "ok"            lines = the CSV as a list of lines
      "not_modified"  server says the file is unchanged since the last download
      "missing"       HTTP 404 (normal for a new year before its first report)
      "error"         anything else

    fresh       ask caches for the newest copy (cache-busting query + no-cache).
    validators  dict carrying ETag / Last-Modified between calls so repeat checks
                cost a few bytes instead of a full download. Updated in place.
    conditional send those validators (False = force a full download).
    """
    global _cache_bust_ok
    base_url = CFTC_URL.format(year=year)
    urls = []
    if fresh and _cache_bust_ok:
        urls.append((base_url + "?t=" + str(int(time.time())), True))
    urls.append((base_url, False))

    bust_failed = False
    err = "no attempt made"
    for url, busted in urls:
        headers = {"User-Agent": "Mozilla/5.0"}
        if fresh:
            headers["Cache-Control"] = "no-cache"
            headers["Pragma"] = "no-cache"
        if validators and conditional:
            if validators.get("etag"):
                headers["If-None-Match"] = validators["etag"]
            if validators.get("last_modified"):
                headers["If-Modified-Since"] = validators["last_modified"]
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                resp_headers = resp.headers
            zf = zipfile.ZipFile(io.BytesIO(data))
            # The zip contains one CSV file
            csv_name = zf.namelist()[0]
            csv_data = zf.read(csv_name).decode("utf-8", errors="replace")
            lines = csv_data.strip().split("\n")
            if validators is not None:
                validators["etag"] = resp_headers.get("ETag")
                validators["last_modified"] = resp_headers.get("Last-Modified")
            if bust_failed:
                _cache_bust_ok = False  # plain URL works, cache-busting one doesn't
            if not quiet:
                print(f"{len(data):,} bytes → {len(lines)-1} rows")
            return "ok", lines
        except urllib.error.HTTPError as e:
            if e.code == 304:
                return "not_modified", None
            if e.code == 404:
                if not quiet:
                    print("HTTP 404")
                return "missing", None
            err = f"HTTP {e.code}"
        except Exception as e:
            err = f"Error: {e}"
        if busted:
            bust_failed = True  # fall through and try the plain URL
    if not quiet:
        print(err)
    return "error", None


def download_cftc_zip(year, retries=3):
    """Download and extract CFTC disaggregated combined F+O zip for a given year.
    Returns the CSV as a list of lines, or None. Transient failures are retried;
    a 404 is final (the current year's file does not exist until its first report)."""
    for attempt in range(1, retries + 1):
        print(f"  Downloading {year}...", end=" ", flush=True)
        status, lines = _fetch_year(year)
        if status == "ok":
            return lines
        if status == "missing" or attempt == retries:
            return None
        wait = 3 * attempt
        print(f"    retrying {year} in {wait}s (attempt {attempt + 1} of {retries})")
        time.sleep(wait)
    return None


_unmatched_names = set()
_natgas_matches = set()
_heating_matches = set()
_crude_matches = set()
_crude_per_name_count = defaultdict(int)  # track how many records each crude name contributes

# Exchange-based routing for commodities with generic names in older files
# Key: (commodity_part, exchange_keyword) → cot_id
_EXCHANGE_MAP = {
    ("WHEAT", "CHICAGO"): "cot-chi-wheat",
    ("WHEAT", "CBOT"): "cot-chi-wheat",
    ("WHEAT", "KANSAS"): "cot-kc-wheat",
    ("WHEAT", "KCBT"): "cot-kc-wheat",
    ("WHEAT", "MINNEAPOLIS"): "cot-mpls-wheat",
    ("WHEAT", "MGEX"): "cot-mpls-wheat",
}

# Prefix fallback for commodities with many name variants
_PREFIX_MAP = [
    # NOTE: crude oil NOT here — handled by exact match + name-priority dedup
    ("NY HARBOR ULSD", "cot-heating-oil"),
    ("NO 2 HEATING OIL", "cot-heating-oil"),
    ("NO. 2 HEATING OIL", "cot-heating-oil"),
]

# Words that indicate a derivative/sub-product, not the main contract
_EXCLUDE_WORDS = {"OPTION", "SWAP", "SPREAD", "CALENDAR", "CAL ", "BASIS",
                  "CRACK", "FIN ", "FINANCIAL", "MINI", "AVG PRICE",
                  "LAST DAY", "BALMO", "BRENT", "DUBAI", "CANADIAN",
                  "EUR STYLE", "BIODIESEL", "GASOIL", "NET ENRGY", "RBOB"}

def identify_commodity(market_name):
    """Match CFTC market name to our commodity ID using exact + exchange-aware matching."""
    full_name = market_name.strip()
    full_upper = full_name.upper()
    
    # Extract commodity and exchange portions
    if " - " in full_name:
        parts = full_name.split(" - ", 1)
        commodity_part = parts[0].strip().upper()
        exchange_part = parts[1].strip().upper() if len(parts) > 1 else ""
    else:
        commodity_part = full_upper
        exchange_part = ""
    
    # 1. Try exact match on commodity portion
    if commodity_part in COMMODITY_MAP:
        result = COMMODITY_MAP[commodity_part]
        if result == "cot-nat-gas": _natgas_matches.add(commodity_part)
        if result == "cot-heating-oil": _heating_matches.add(commodity_part)
        if result == "cot-crude-oil":
            _crude_matches.add(commodity_part)
            _crude_per_name_count[commodity_part] += 1
        return result
    
    # 2. Exchange-aware routing (handles "WHEAT" → SRW/HRW/HRS based on exchange)
    for (name_key, exch_key), cot_id in _EXCHANGE_MAP.items():
        if commodity_part == name_key and exch_key in exchange_part:
            return cot_id
    
    # 3. Prefix fallback for energy names
    for prefix, cot_id in _PREFIX_MAP:
        if commodity_part.startswith(prefix):
            if any(excl in commodity_part for excl in _EXCLUDE_WORDS):
                break
            if cot_id == "cot-nat-gas": _natgas_matches.add(commodity_part)
            if cot_id == "cot-heating-oil": _heating_matches.add(commodity_part)
            if cot_id == "cot-crude-oil":
                _crude_matches.add(commodity_part)
                _crude_per_name_count[commodity_part] += 1
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

    # Energy name diagnostics disabled — all names identified

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
        source_name = market.split(" - ")[0].strip().upper() if " - " in market else market.strip().upper()
        records[cot_id].append({
            "date": date_str,
            "_source": source_name,  # track which CFTC name matched
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
        # Show which of our target commodities are missing
        target_ids = set(COMMODITY_META.keys())
        missing = sorted(target_ids - set(ids_found))
        missing_str = f" | MISSING: {', '.join(missing)}" if missing else ""
        print(f"    {year}: {matched_count} rows → {len(ids_found)} commodities{missing_str}")
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

    # Sort each commodity by date and deduplicate
    # When two records exist for the same date (e.g., "CRUDE OIL, LIGHT SWEET" and
    # "CRUDE OIL, LIGHT SWEET-WTI"), prefer the PRIMARY name (shorter/original).
    # Primary names are the main futures contracts; secondary are sub-contracts or renames.
    _PRIMARY_NAMES = {
        "cot-crude-oil": "CRUDE OIL, LIGHT SWEET",
        "cot-nat-gas": "NATURAL GAS",
        "cot-heating-oil": "NY HARBOR ULSD",
    }
    for cot_id in records:
        records[cot_id].sort(key=lambda r: r["date"])
        by_date = {}
        primary = _PRIMARY_NAMES.get(cot_id)
        for rec in records[cot_id]:
            d = rec["date"]
            if d not in by_date:
                by_date[d] = rec
            elif primary and rec.get("_source") == primary:
                by_date[d] = rec  # primary name always wins
            # else keep existing (first occurrence)
        # Remove _source from final records
        for d in by_date:
            by_date[d].pop("_source", None)
        records[cot_id] = [by_date[d] for d in sorted(by_date.keys())]

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


# ════════════════════════════════════════════════════════════════════════════
# Watch mode: wait for the release, publish the moment it lands
# ════════════════════════════════════════════════════════════════════════════

RELEASE_ET = (15, 30)          # CFTC publishes COT reports at 3:30 PM US Eastern
WATCH_LEAD_MIN = 1             # begin checking this many minutes before the release
WATCH_GIVE_UP_MIN = 45         # stop this many minutes after it
WATCH_MAX_PRE_WAIT_MIN = 240   # never sit idle longer than this ahead of a release


def _now_utc():
    return datetime.utcnow()


def _us_eastern_offset_hours(utc_dt):
    """UTC offset of US Eastern time: daylight time runs from 2:00 AM on the second
    Sunday of March to 2:00 AM on the first Sunday of November."""
    y = utc_dt.year
    mar = datetime(y, 3, 8)
    mar += timedelta(days=(6 - mar.weekday()) % 7)      # second Sunday of March
    nov = datetime(y, 11, 1)
    nov += timedelta(days=(6 - nov.weekday()) % 7)      # first Sunday of November
    dst_start = mar + timedelta(hours=7)                # 2:00 AM EST = 07:00 UTC
    dst_end = nov + timedelta(hours=6)                  # 2:00 AM EDT = 06:00 UTC
    return -4 if dst_start <= utc_dt < dst_end else -5


def now_et():
    """Current wall-clock time in US Eastern (naive datetime), DST-aware."""
    utc = _now_utc()
    try:
        from zoneinfo import ZoneInfo
        return utc.replace(tzinfo=timezone.utc).astimezone(ZoneInfo("America/New_York")).replace(tzinfo=None)
    except Exception:
        return utc + timedelta(hours=_us_eastern_offset_hours(utc))


def _clock(dt):
    """3:30:41 PM ET"""
    return dt.strftime("%I:%M:%S %p ET").lstrip("0")


def latest_report_date(parsed):
    """Newest report date across our commodities in one parsed yearly file."""
    dates = [recs[-1]["date"] for recs in parsed.values() if recs]
    return max(dates) if dates else None


def load_published(path):
    """What is already in the repo: (newest report date, {cot_id: latest_date})."""
    try:
        with open(path) as f:
            existing = json.load(f)
        per_id = {k: v.get("latest_date") for k, v in existing.get("data", {}).items() if v.get("latest_date")}
        return (max(per_id.values()) if per_id else None), per_id
    except Exception:
        return None, {}


def set_outputs(**pairs):
    """Hand results to the GitHub Actions workflow (no-op when run anywhere else)."""
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a") as f:
        for k, v in pairs.items():
            f.write(f"{k}={v}\n")


def _diag_snapshot():
    return (set(_unmatched_names), set(_natgas_matches), set(_heating_matches),
            set(_crude_matches), dict(_crude_per_name_count))


def _diag_restore(snap):
    for target, saved in zip((_unmatched_names, _natgas_matches, _heating_matches, _crude_matches), snap[:4]):
        target.clear()
        target.update(saved)
    _crude_per_name_count.clear()
    _crude_per_name_count.update(snap[4])


def watch_for_new_report(baseline):
    """Wait for CFTC to publish a report dated after `baseline`.

    Returns (date, preparsed) where preparsed is {year: parsed records} for every
    yearly file already downloaded while waiting, or (None, {}) if nothing new
    appeared by the give-up time.
    """
    et = now_et()
    release = et.replace(hour=RELEASE_ET[0], minute=RELEASE_ET[1], second=0, microsecond=0)
    hot_start = release - timedelta(minutes=WATCH_LEAD_MIN)
    give_up = release + timedelta(minutes=WATCH_GIVE_UP_MIN)

    # A report dated late December can be published in early January, into last
    # year's file, so in January keep an eye on both.
    probe_years = [CURRENT_YEAR] + ([CURRENT_YEAR - 1] if et.month == 1 else [])
    validators = {y: {} for y in probe_years}
    raw = {}       # {year: csv lines} newest copy of each watched file
    seen = {}      # {year: newest report date in that copy}
    preparsed = {}
    state = {"n": 0}

    def check():
        state["n"] += 1
        # Every third check is a full download even if the server answers "not
        # modified", so a misbehaving cache can't hide a new report for long.
        full = (state["n"] % 3 == 1)
        parts = []
        for y in probe_years:
            status, lines = _fetch_year(y, fresh=True, validators=validators[y],
                                        conditional=not full, quiet=True)
            if status == "ok":
                snap = _diag_snapshot()
                seen[y] = latest_report_date(parse_cftc_csv(lines))
                _diag_restore(snap)          # checks leave no trace in the diagnostics
                raw[y] = lines
                parts.append(f"{y} file: latest report {seen[y]}")
            elif status == "not_modified":
                parts.append(f"{y} file: unchanged")
            elif status == "missing":
                parts.append(f"{y} file: not published yet")
            else:
                parts.append(f"{y} file: fetch failed")
        dates = [d for d in seen.values() if d]
        newest = max(dates) if dates else None
        is_new = bool(newest) and (baseline is None or newest > baseline)
        print(f"  [{now_et():%H:%M:%S} ET] check #{state['n']}: {' | '.join(parts)}"
              + ("   <-- NEW REPORT" if is_new else ""), flush=True)
        return newest if is_new else None

    print("\n-- Watch mode --")
    print(f"  Published now: report dated {baseline or '(nothing yet)'}")
    print(f"  Now {et:%a %Y-%m-%d %H:%M:%S} ET | release {release:%H:%M} ET | give up {give_up:%H:%M} ET")

    found = check()   # always look once straight away: it may already be out

    if not found and et < give_up:
        pre_wait_min = (hot_start - et).total_seconds() / 60
        if pre_wait_min > WATCH_MAX_PRE_WAIT_MIN:
            print(f"  Release is {pre_wait_min:.0f} min away, too early to sit and wait. "
                  f"The scheduled run will handle it.")
            return None, {}

        if pre_wait_min > 3:
            # Use the quiet time to load the years that won't change, so that when
            # the report lands only the one new file stands between us and publishing.
            print("  Pre-loading history while we wait...")
            for year in range(START_YEAR, CURRENT_YEAR + 1):
                if year in probe_years:
                    continue
                lines = download_cftc_zip(year)
                if lines:
                    preparsed[year] = parse_cftc_csv(lines, year=year)
                time.sleep(0.5)

        announced_wait = False
        while not found:
            et = now_et()
            if et >= give_up:
                break
            if et < hot_start:
                wait = min((hot_start - et).total_seconds(), 600)
                if not announced_wait:
                    print(f"  Waiting until {hot_start:%H:%M} ET to start checking...", flush=True)
                    announced_wait = True
            elif et < release + timedelta(minutes=5):
                wait = 30
            elif et < release + timedelta(minutes=20):
                wait = 60
            else:
                wait = 300
            wait = min(wait, (give_up - et).total_seconds())
            time.sleep(max(1, wait))
            if now_et() < hot_start:
                continue
            found = check()

    if not found:
        return None, {}

    # Parse the file(s) holding the new report for real (same call the normal
    # run makes), reusing the exact bytes we just verified.
    for y in probe_years:
        if y in raw:
            preparsed[y] = parse_cftc_csv(raw[y], year=y)
    return found, preparsed


def main(argv=None):
    ap = argparse.ArgumentParser(description="Fetch CFTC COT data into data/cot.json")
    ap.add_argument("--watch", action="store_true",
                    help="wait for a report newer than the published one, then rebuild")
    args = ap.parse_args(argv)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "cot.json")
    baseline, published_ids = load_published(output_file)

    print("=" * 60)
    print("CFTC COT Data Fetch")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print(f"Full history: {START_YEAR} to {CURRENT_YEAR}")
    print(f"Band charts: last {BAND_YEARS} years")
    print("=" * 60)

    # Fetch all years from 2006
    all_years_parsed = {}  # {year: parsed_dict} for band building
    all_records = defaultdict(list)  # combined records across all years
    
    preparsed = {}
    detected_at = None
    if args.watch:
        detected, preparsed = watch_for_new_report(baseline)
        if not detected:
            print(f"\nNo report newer than {baseline} was published. cot.json left untouched.")
            print(f"::notice title=COT::No new COT report today (published data is dated {baseline}).")
            set_outputs(updated="false", latest_date=baseline or "")
            return 0
        detected_at = now_et()
        print(f"\n-- New report {detected} detected at {detected_at:%H:%M:%S} ET, building --")

    for year in range(START_YEAR, CURRENT_YEAR + 1):
        if year in preparsed:
            parsed = preparsed[year]
        else:
            lines = download_cftc_zip(year)
            parsed = parse_cftc_csv(lines, year=year) if lines else None
            time.sleep(0.5)
        if parsed is not None:
            all_years_parsed[year] = parsed
            for cot_id, recs in parsed.items():
                all_records[cot_id].extend(recs)

    if not all_records:
        print("ERROR: No data fetched")
        return 1

    # Never publish truncated history: every completed year must have downloaded.
    missing_years = [y for y in range(START_YEAR, CURRENT_YEAR) if y not in all_years_parsed]
    if missing_years:
        print(f"::error title=COT::Could not download CFTC history for {missing_years}; cot.json left untouched.")
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
                    yearly_out[yr_key] = {"_dates": [None] * NUM_SLOTS}
                    for f in fields_to_track:
                        yearly_out[yr_key][f] = [None] * NUM_SLOTS
                idx = iso_wk - 1  # week 1 → index 0
                if 0 <= idx < NUM_SLOTS:
                    yearly_out[yr_key]["_dates"][idx] = rec["date"]
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
        # Debug: verify crude oil and wheat 2010 data
        if cot_id == "cot-crude-oil" and "2010" in yearly_out:
            cl_10 = yearly_out["2010"]["mm_net"][:6]
            print(f"    Crude 2010 MM net wks 1-6: {cl_10}  (expect ~[157K, 176K, 173K, ...])")
        if cot_id == "cot-chi-wheat" and "2010" in yearly_out:
            w_10 = yearly_out["2010"]["mm_net"][:6]
            print(f"    Wheat 2010 MM net wks 1-6: {w_10}  (expect ~[-3K, -10K, -19K, ...])")

    # Debug: energy market names that matched
    print(f"\n  Energy name matches:")
    print(f"    Nat gas:     {sorted(_natgas_matches)}")
    print(f"    Heating oil: {sorted(_heating_matches)}")
    print(f"    Crude oil:   {sorted(_crude_matches)}")
    print(f"    Crude oil record counts per name: {dict(_crude_per_name_count)}")

    # Log unmatched commodity names (helps find CFTC name changes)
    if _unmatched_names:
        print(f"\n  Unmatched CFTC commodity names ({len(_unmatched_names)}):")
        # Prioritize energy-related unmatched names
        energy_kw = ["OIL", "GAS", "CRUDE", "HEAT", "PETROL", "FUEL", "ULSD", "WTI", "HENRY"]
        energy_unmatched = sorted([n for n in _unmatched_names if any(kw in n.upper() for kw in energy_kw)])
        other_unmatched = sorted([n for n in _unmatched_names if n not in energy_unmatched])
        if energy_unmatched:
            print(f"    Energy-related ({len(energy_unmatched)} total):")
            # Show ULSD, NATGAS, and HEATING specifically
            priority = [n for n in energy_unmatched if any(kw in n for kw in ["ULSD", "NATURAL GAS", "HEATING", "HENRY HUB", "RBOB"])]
            if priority:
                print(f"    ** Priority (ULSD/NATGAS/HEATING/HENRY):")
                for n in priority:
                    print(f"      >>> {n}")
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

    # Never replace published data with something older.
    new_ids = {k: v["latest_date"] for k, v in cot_output.items()}
    new_latest = max(new_ids.values()) if new_ids else None
    if baseline and (not new_latest or new_latest < baseline):
        print(f"::error title=COT::Built data ends {new_latest} but {baseline} is already published; cot.json left untouched.")
        return 1
    if args.watch and baseline and new_latest <= baseline:
        print(f"::error title=COT::A new report was detected but the build still ends {new_latest}; cot.json left untouched.")
        return 1

    # Heads-up (not fatal) if a market dropped out or didn't get the newest report:
    # usually means CFTC renamed it and COMMODITY_MAP needs a new alias.
    dropped = sorted(set(published_ids) - set(new_ids))
    lagging = sorted(k for k, d in new_ids.items() if d < new_latest)
    if dropped:
        print(f"::warning title=COT::Markets no longer found in CFTC data: {', '.join(dropped)}")
    if lagging:
        print(f"::warning title=COT::Markets missing the {new_latest} report: {', '.join(lagging)}")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")

    set_outputs(updated="true", latest_date=new_latest or "",
                detected_at=(_clock(detected_at) if detected_at else ""))
    if detected_at:
        print(f"::notice title=COT::Report dated {new_latest} detected at {_clock(detected_at)} (previously {baseline}).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
