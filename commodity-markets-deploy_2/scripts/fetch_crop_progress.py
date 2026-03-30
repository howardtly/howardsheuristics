#!/usr/bin/env python3
"""
Fetch USDA NASS Crop Progress data via QuickStats API.
Outputs crop_progress.json with weekly progress/condition data for:
  - Corn, Soybeans, Winter Wheat, Spring Wheat (progress stages + condition)
  - Pasture condition (poor + very poor %)
  - Soil moisture (topsoil/subsoil adequate + surplus %)

Fetches current year, previous year, and computes 5-year average from 5 prior years.
State-level data included for current + previous year.
"""
import urllib.request, urllib.parse, json, os, sys, time
from datetime import datetime, timezone
from collections import defaultdict

API_KEY = os.environ.get("NASS_API_KEY", "03CFFAAE-9FAC-3F49-91D0-700A4F6DC970")
BASE = "https://quickstats.nass.usda.gov/api/api_GET/"
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

CUR_YEAR = datetime.now(timezone.utc).year

# ── Crop stage definitions ──
CROPS = {
    "corn": {
        "label": "Corn",
        "commodity_desc": "CORN",
        "class_desc": None,
        "stages": [
            {"id": "planted",   "unit": "PCT PLANTED"},
            {"id": "emerged",   "unit": "PCT EMERGED"},
            {"id": "silking",   "unit": "PCT SILKING"},
            {"id": "dough",     "unit": "PCT DOUGH"},
            {"id": "dented",    "unit": "PCT DENTED"},
            {"id": "mature",    "unit": "PCT MATURE"},
        ],
        "harvest_short_desc": "CORN, GRAIN - PROGRESS, MEASURED IN PCT HARVESTED",
    },
    "soybeans": {
        "label": "Soybeans",
        "commodity_desc": "SOYBEANS",
        "class_desc": None,
        "stages": [
            {"id": "planted",       "unit": "PCT PLANTED"},
            {"id": "emerged",       "unit": "PCT EMERGED"},
            {"id": "blooming",      "unit": "PCT BLOOMING"},
            {"id": "setting_pods",  "unit": "PCT SETTING PODS"},
            {"id": "dropping_leaves","unit": "PCT DROPPING LEAVES"},
        ],
        "harvest_short_desc": "SOYBEANS - PROGRESS, MEASURED IN PCT HARVESTED",
    },
    "winter_wheat": {
        "label": "Winter Wheat",
        "commodity_desc": "WHEAT",
        "class_desc": "WINTER",
        "stages": [
            {"id": "planted",  "unit": "PCT PLANTED"},
            {"id": "emerged",  "unit": "PCT EMERGED"},
            {"id": "headed",   "unit": "PCT HEADED"},
        ],
        "harvest_short_desc": "WHEAT, WINTER - PROGRESS, MEASURED IN PCT HARVESTED",
    },
    "spring_wheat": {
        "label": "Spring Wheat",
        "commodity_desc": "WHEAT",
        "class_desc": "SPRING, (EXCL DURUM)",
        "stages": [
            {"id": "planted",  "unit": "PCT PLANTED"},
            {"id": "emerged",  "unit": "PCT EMERGED"},
            {"id": "headed",   "unit": "PCT HEADED"},
        ],
        "harvest_short_desc": "WHEAT, SPRING, (EXCL DURUM) - PROGRESS, MEASURED IN PCT HARVESTED",
    },
}

# Years to fetch for 5yr avg computation
AVG_YEARS = list(range(CUR_YEAR - 5, CUR_YEAR))  # e.g., 2021-2025 for 2026
FETCH_YEARS = list(range(CUR_YEAR - 5, CUR_YEAR + 1))  # e.g., 2021-2026


def api_get(params, retries=2):
    """Call NASS API with retry."""
    params["key"] = API_KEY
    params["format"] = "json"
    url = BASE + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            resp = urllib.request.urlopen(req, timeout=45)
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", [])
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
            else:
                raise e


def parse_week(ref_period):
    """Extract week number from 'WEEK #14' -> 14."""
    if ref_period and ref_period.startswith("WEEK #"):
        try:
            return int(ref_period.replace("WEEK #", ""))
        except:
            pass
    return None


def parse_value(val):
    """Parse NASS value string to int, handling commas and special chars."""
    if val is None:
        return None
    val = str(val).strip().replace(",", "")
    if val in ("", "(D)", "(NA)", "(Z)", "(S)"):
        return None
    try:
        return int(float(val))
    except:
        return None


def rows_to_weekly(rows, filter_unit=None):
    """Convert API rows to {state: {year: {week: value}}} structure."""
    result = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        if filter_unit and r.get("unit_desc") != filter_unit:
            continue
        state = r.get("state_alpha", "US")
        year = str(r.get("year", ""))
        week = parse_week(r.get("reference_period_desc"))
        val = parse_value(r.get("Value"))
        if week and val is not None:
            result[state][year][week] = val
    return result


def compute_5yr_avg(weekly_by_state, avg_years):
    """Compute 5-year average per week per state."""
    avg_result = {}
    yr_strs = [str(y) for y in avg_years]
    for state, by_year in weekly_by_state.items():
        all_weeks = set()
        for yr in yr_strs:
            if yr in by_year:
                all_weeks.update(by_year[yr].keys())
        avg_weeks = {}
        for wk in sorted(all_weeks):
            vals = [by_year[yr][wk] for yr in yr_strs if yr in by_year and wk in by_year[yr]]
            if vals:
                avg_weeks[wk] = round(sum(vals) / len(vals))
        if avg_weeks:
            avg_result[state] = avg_weeks
    return avg_result


def weekly_to_points(week_dict):
    """Convert {week: value} to sorted [{w: week, v: value}] list."""
    return [{"w": w, "v": v} for w, v in sorted(week_dict.items())]


def fetch_progress_stage(crop_cfg, stage_unit, years_str):
    """Fetch a single progress stage for all states."""
    params = {
        "source_desc": "SURVEY",
        "commodity_desc": crop_cfg["commodity_desc"],
        "statisticcat_desc": "PROGRESS",
        "unit_desc": stage_unit,
        "freq_desc": "WEEKLY",
        "year__GE": str(min(FETCH_YEARS)),
        "year__LE": str(max(FETCH_YEARS)),
    }
    if crop_cfg.get("class_desc"):
        params["class_desc"] = crop_cfg["class_desc"]
    return api_get(params)


def fetch_harvest(crop_cfg):
    """Fetch harvest data using short_desc (needed for 'CORN, GRAIN' distinction)."""
    params = {
        "source_desc": "SURVEY",
        "short_desc": crop_cfg["harvest_short_desc"],
        "freq_desc": "WEEKLY",
        "year__GE": str(min(FETCH_YEARS)),
        "year__LE": str(max(FETCH_YEARS)),
    }
    return api_get(params)


def fetch_condition(commodity_desc, class_desc=None):
    """Fetch condition data (current year only has CONDITION, but NASS provides 5yr avg and prev year)."""
    params = {
        "source_desc": "SURVEY",
        "commodity_desc": commodity_desc,
        "statisticcat_desc": "CONDITION",
        "freq_desc": "WEEKLY",
        "year__GE": str(min(FETCH_YEARS)),
        "year__LE": str(max(FETCH_YEARS)),
    }
    if class_desc:
        params["class_desc"] = class_desc
    return api_get(params)


def process_condition_rows(rows):
    """Process condition rows into good+excellent % per state/year/week."""
    # Group by state, year, week
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for r in rows:
        state = r.get("state_alpha", "US")
        year = str(r.get("year", ""))
        week = parse_week(r.get("reference_period_desc"))
        unit = r.get("unit_desc", "")
        val = parse_value(r.get("Value"))
        if week and val is not None:
            grouped[state][year][week][unit] = val

    # Sum good + excellent
    result = defaultdict(lambda: defaultdict(dict))
    for state in grouped:
        for year in grouped[state]:
            for week in grouped[state][year]:
                vals = grouped[state][year][week]
                good = vals.get("PCT GOOD", 0)
                exc = vals.get("PCT EXCELLENT", 0)
                result[state][year][week] = good + exc

    return dict(result)


def process_condition_with_builtins(rows):
    """Process condition rows, separating current/prev/5yr_avg using statisticcat_desc."""
    current = []
    prev_year = []
    avg_5yr = []
    for r in rows:
        cat = r.get("statisticcat_desc", "")
        if "5 YEAR AVG" in cat:
            avg_5yr.append(r)
        elif "PREVIOUS YEAR" in cat:
            prev_year.append(r)
        else:
            current.append(r)
    return current, prev_year, avg_5yr


def build_state_output(weekly_by_state, avg_by_state, cur_year, last_year):
    """Build final output structure: {state: {cur_year: [...], last_year: [...], 5yr_avg: [...]}}."""
    out = {}
    cur_str = str(cur_year)
    last_str = str(last_year)
    all_states = set(weekly_by_state.keys()) | set(avg_by_state.keys())
    for state in sorted(all_states):
        state_out = {}
        by_year = weekly_by_state.get(state, {})
        if cur_str in by_year:
            state_out[cur_str] = weekly_to_points(by_year[cur_str])
        if last_str in by_year:
            state_out[last_str] = weekly_to_points(by_year[last_str])
        if state in avg_by_state:
            state_out["5yr_avg"] = weekly_to_points(avg_by_state[state])
        if state_out:
            out[state] = state_out
    return out


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "crop_progress.json")

    print("=" * 60)
    print("USDA NASS Crop Progress Fetch")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}")
    print(f"Years: {FETCH_YEARS[0]}-{FETCH_YEARS[-1]}")
    print(f"5yr avg: {AVG_YEARS[0]}-{AVG_YEARS[-1]}")
    print("=" * 60)

    result = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "current_year": CUR_YEAR,
        "crops": {},
        "pasture": {},
        "soil": {},
        "states": [],
    }

    # ── Fetch crop progress + condition ──
    for crop_id, cfg in CROPS.items():
        print(f"\n  {cfg['label']}:")
        crop_out = {"label": cfg["label"], "stages": {}}

        # Progress stages
        for stage in cfg["stages"]:
            stage_id = stage["id"]
            print(f"    {stage_id}...", end=" ", flush=True)
            try:
                rows = fetch_progress_stage(cfg, stage["unit"], FETCH_YEARS)
                weekly = rows_to_weekly(rows)
                avg = compute_5yr_avg(weekly, AVG_YEARS)
                crop_out["stages"][stage_id] = build_state_output(weekly, avg, CUR_YEAR, CUR_YEAR - 1)
                us_cur = len(weekly.get("US", {}).get(str(CUR_YEAR), {}))
                print(f"{len(rows)} rows, US {CUR_YEAR}: {us_cur} weeks")
            except Exception as e:
                print(f"ERROR: {e}")
            time.sleep(0.3)

        # Harvest (uses short_desc)
        print(f"    harvested...", end=" ", flush=True)
        try:
            rows = fetch_harvest(cfg)
            weekly = rows_to_weekly(rows)
            avg = compute_5yr_avg(weekly, AVG_YEARS)
            crop_out["stages"]["harvested"] = build_state_output(weekly, avg, CUR_YEAR, CUR_YEAR - 1)
            us_cur = len(weekly.get("US", {}).get(str(CUR_YEAR), {}))
            print(f"{len(rows)} rows, US {CUR_YEAR}: {us_cur} weeks")
        except Exception as e:
            print(f"ERROR: {e}")
        time.sleep(0.3)

        # Condition (good + excellent %)
        print(f"    condition...", end=" ", flush=True)
        try:
            rows = fetch_condition(cfg["commodity_desc"], cfg.get("class_desc"))
            cond_weekly = process_condition_rows(rows)
            avg = compute_5yr_avg(cond_weekly, AVG_YEARS)
            crop_out["stages"]["condition"] = build_state_output(cond_weekly, avg, CUR_YEAR, CUR_YEAR - 1)
            us_cur = len(cond_weekly.get("US", {}).get(str(CUR_YEAR), {}))
            print(f"{len(rows)} rows, US {CUR_YEAR}: {us_cur} weeks")
        except Exception as e:
            print(f"ERROR: {e}")
        time.sleep(0.3)

        result["crops"][crop_id] = crop_out

    # ── Pasture condition (poor + very poor %) ──
    print(f"\n  Pasture:")
    print(f"    condition...", end=" ", flush=True)
    try:
        rows = api_get({
            "source_desc": "SURVEY",
            "commodity_desc": "PASTURELAND",
            "freq_desc": "WEEKLY",
            "year__GE": str(min(FETCH_YEARS)),
            "year__LE": str(max(FETCH_YEARS)),
        })
        # Separate current, prev year, 5yr avg
        current_rows, prev_rows, avg_rows = process_condition_with_builtins(rows)

        # Process poor + very poor
        def sum_poor(row_list):
            grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
            for r in row_list:
                state = r.get("state_alpha", "US")
                year = str(r.get("year", ""))
                week = parse_week(r.get("reference_period_desc"))
                unit = r.get("unit_desc", "")
                val = parse_value(r.get("Value"))
                if week and val is not None:
                    grouped[state][year][week][unit] = val
            result = defaultdict(lambda: defaultdict(dict))
            for state in grouped:
                for year in grouped[state]:
                    for week in grouped[state][year]:
                        v = grouped[state][year][week]
                        result[state][year][week] = v.get("PCT POOR", 0) + v.get("PCT VERY POOR", 0)
            return dict(result)

        cur_weekly = sum_poor(current_rows)
        avg_weekly = compute_5yr_avg(cur_weekly, AVG_YEARS)
        result["pasture"]["poor_very_poor"] = build_state_output(cur_weekly, avg_weekly, CUR_YEAR, CUR_YEAR - 1)

        # Also get built-in 5yr avg from NASS
        if avg_rows:
            nass_avg = sum_poor(avg_rows)
            # Override computed avg with NASS-provided avg for US
            if "US" in nass_avg and str(CUR_YEAR) in nass_avg["US"]:
                result["pasture"]["poor_very_poor"].setdefault("US", {})["5yr_avg"] = weekly_to_points(nass_avg["US"][str(CUR_YEAR)])

        us_cur = len(cur_weekly.get("US", {}).get(str(CUR_YEAR), {}))
        print(f"{len(rows)} rows, US {CUR_YEAR}: {us_cur} weeks")
    except Exception as e:
        print(f"ERROR: {e}")
    time.sleep(0.3)

    # ── Soil moisture (adequate + surplus %) ──
    print(f"\n  Soil Moisture:")
    for soil_class in ["TOPSOIL", "SUBSOIL"]:
        soil_key = soil_class.lower() + "_adequate_surplus"
        print(f"    {soil_class}...", end=" ", flush=True)
        try:
            rows = api_get({
                "source_desc": "SURVEY",
                "commodity_desc": "SOIL",
                "class_desc": soil_class,
                "statisticcat_desc": "MOISTURE",
                "freq_desc": "WEEKLY",
                "year__GE": str(min(FETCH_YEARS)),
                "year__LE": str(max(FETCH_YEARS)),
            })
            # Sum adequate + surplus
            grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
            for r in rows:
                state = r.get("state_alpha", "US")
                year = str(r.get("year", ""))
                week = parse_week(r.get("reference_period_desc"))
                unit = r.get("unit_desc", "")
                val = parse_value(r.get("Value"))
                if week and val is not None:
                    grouped[state][year][week][unit] = val

            weekly = defaultdict(lambda: defaultdict(dict))
            for state in grouped:
                for year in grouped[state]:
                    for week in grouped[state][year]:
                        v = grouped[state][year][week]
                        weekly[state][year][week] = v.get("PCT ADEQUATE", 0) + v.get("PCT SURPLUS", 0)

            avg = compute_5yr_avg(weekly, AVG_YEARS)
            result["soil"][soil_key] = build_state_output(weekly, avg, CUR_YEAR, CUR_YEAR - 1)
            us_cur = len(weekly.get("US", {}).get(str(CUR_YEAR), {}))
            print(f"{len(rows)} rows, US {CUR_YEAR}: {us_cur} weeks")
        except Exception as e:
            print(f"ERROR: {e}")
        time.sleep(0.3)

    # Collect available states
    all_states = set()
    for crop in result["crops"].values():
        for stage_data in crop.get("stages", {}).values():
            all_states.update(stage_data.keys())
    all_states.discard("US")
    result["states"] = sorted(all_states)

    # Write output
    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    size = os.path.getsize(output_file)
    print(f"  {size:,} bytes")
    print(f"  {len(result['crops'])} crops, {len(result['states'])} states")
    print(f"  Pasture: {'poor_very_poor' in result['pasture']}")
    print(f"  Soil: {list(result['soil'].keys())}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
