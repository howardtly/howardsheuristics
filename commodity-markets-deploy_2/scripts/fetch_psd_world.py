#!/usr/bin/env python3
"""
Fetch world balance sheet data from USDA PSD Online API.
Adds world data to existing wasde.json.

API: https://apps.fas.usda.gov/PSDOnlineDataServices/api/CommodityData/GetCommodityDataByYear
API key passed in header as API_KEY.

PSD data is in 1000 MT (converted to MMT for display), 1000 HA (converted to M HA), MT/HA for yield.
"""

import json, os, sys, urllib.request, urllib.error, time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

API_BASE = "https://apps.fas.usda.gov/PSDOnlineDataServices/api/CommodityData/GetCommodityDataByYear"
API_KEY = os.environ.get("PSD_API_KEY", "")

# Commodity codes
COMMODITIES = {
    "corn":          "0440000",
    "soybeans":      "2222000",
    "wheat":         "0410000",
    "soybean_meal":  "0813100",
    "soybean_oil":   "4232000",
}

# Countries to include per commodity (PSD country codes)
# We also aggregate world totals from ALL countries
COUNTRIES = {
    "corn":         {"AR": "Argentina", "BR": "Brazil", "CH": "China", "UP": "Ukraine", "US": "United States"},
    "soybeans":     {"AR": "Argentina", "BR": "Brazil", "CH": "China", "PA": "Paraguay", "US": "United States"},
    "soybean_meal": {"AR": "Argentina", "BR": "Brazil", "CH": "China", "E4": "EU", "US": "United States"},
    "soybean_oil":  {"AR": "Argentina", "BR": "Brazil", "CH": "China", "IN": "India", "US": "United States"},
    "wheat":        {"AR": "Argentina", "AS": "Australia", "CA": "Canada", "CH": "China", "E4": "EU", "RS": "Russia", "UP": "Ukraine", "US": "United States"},
}

# PSD Attribute IDs
ATTR = {
    4:   "area_harvested",    # 1000 HA
    184: "yield",             # MT/HA
    20:  "beginning_stocks",  # 1000 MT
    28:  "production",        # 1000 MT
    57:  "imports",           # 1000 MT (MY Imports)
    86:  "total_supply",      # 1000 MT
    130: "feed_dom",          # 1000 MT
    192: "fsi_consumption",   # 1000 MT
    125: "total_consumption", # 1000 MT (domestic consumption)
    88:  "exports",           # 1000 MT (MY Exports)
    176: "ending_stocks",     # 1000 MT
    178: "total_distribution",# 1000 MT
}

# For soybeans, we also need crush (AttributeId 59)
SOYBEAN_EXTRA_ATTR = {
    59: "crush",  # 1000 MT
}

MARKET_YEARS = list(range(2015, 2026))  # 2015/16 through 2025/26


def fetch_psd(commodity_code, market_year):
    """Fetch PSD data for a commodity and market year."""
    url = f"{API_BASE}?commodityCode={commodity_code}&marketYear={market_year}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "API_KEY": API_KEY,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data
    except urllib.error.HTTPError as e:
        print(f"    HTTP {e.code} for {commodity_code} MY{market_year}")
        return None
    except Exception as e:
        print(f"    Error: {e}")
        return None


def parse_psd_response(records):
    """Parse PSD API response into a nested dict: {country_code: {attr_name: value}}."""
    result = {}
    all_attrs = {**ATTR, **SOYBEAN_EXTRA_ATTR}
    for rec in records:
        cc = rec.get("CountryCode", "").strip()
        attr_id = rec.get("AttributeId")
        value = rec.get("Value")
        if attr_id not in all_attrs:
            continue
        attr_name = all_attrs[attr_id]
        if cc not in result:
            result[cc] = {}
        result[cc][attr_name] = value
    return result


def to_mmt(v):
    """Convert 1000 MT to million metric tons, rounded to 1 decimal."""
    if v is None: return None
    return round(v / 1000, 1)

def to_mha(v):
    """Convert 1000 HA to million hectares, rounded to 1 decimal."""
    if v is None: return None
    return round(v / 1000, 1)

def to_yield(v):
    """Yield in MT/HA, rounded to 2 decimals."""
    if v is None: return None
    return round(v, 2)

def pct(num, den):
    if num is not None and den is not None and den != 0:
        return round(num / den * 100, 1)
    return None


def build_country_rows_corn(data_by_year, country_code, years):
    """Build corn country rows: area, yield, supply, feed/fsi/dom, exports, ending stocks."""
    rows = []
    def val(yr, attr, conv=to_mmt):
        d = data_by_year.get(yr, {}).get(country_code, {})
        return conv(d.get(attr))

    rows.append({"label": "Area harvested", "values": [val(y, "area_harvested", to_mha) for y in years]})
    rows.append({"label": "Yield", "values": [val(y, "yield", to_yield) for y in years]})
    rows.append({"label": "Beginning stocks", "values": [val(y, "beginning_stocks") for y in years], "spaceBefore": True})
    rows.append({"label": "Production", "values": [val(y, "production") for y in years]})
    rows.append({"label": "Imports", "values": [val(y, "imports") for y in years]})
    # Total supply
    supply = []
    for y in years:
        bs = val(y, "beginning_stocks")
        pr = val(y, "production")
        im = val(y, "imports")
        supply.append(round(bs + pr + im, 1) if all(v is not None for v in [bs, pr, im]) else val(y, "total_supply"))
    rows.append({"label": "Total supply", "values": supply, "bold": True})

    feed = [val(y, "feed_dom") for y in years]
    fsi = [val(y, "fsi_consumption") for y in years]
    dom = [val(y, "total_consumption") for y in years]
    rows.append({"label": "Feed dom. consumption", "values": feed, "spaceBefore": True})
    rows.append({"label": "FSI consumption", "values": fsi})
    rows.append({"label": "Domestic consumption", "values": dom})
    exp = [val(y, "exports") for y in years]
    rows.append({"label": "Exports", "values": exp})
    # Total usage = dom + exports
    tu = []
    for i in range(len(years)):
        if dom[i] is not None and exp[i] is not None:
            tu.append(round(dom[i] + exp[i], 1))
        else:
            tu.append(None)
    rows.append({"label": "Total usage", "values": tu, "bold": True})

    es = [val(y, "ending_stocks") for y in years]
    rows.append({"label": "Ending stocks", "values": es, "bold": True, "spaceBefore": True})
    rows.append({"label": "Stocks/use (%)", "values": [pct(es[i], tu[i]) for i in range(len(years))], "bold": True, "pct": True})
    return rows


def build_country_rows_soybeans(data_by_year, country_code, years):
    """Build soybean country rows with crush, food, feed breakdown."""
    rows = []
    def val(yr, attr, conv=to_mmt):
        d = data_by_year.get(yr, {}).get(country_code, {})
        return conv(d.get(attr))

    rows.append({"label": "Area harvested", "values": [val(y, "area_harvested", to_mha) for y in years]})
    rows.append({"label": "Yield", "values": [val(y, "yield", to_yield) for y in years]})
    rows.append({"label": "Beginning stocks", "values": [val(y, "beginning_stocks") for y in years], "spaceBefore": True})
    rows.append({"label": "Production", "values": [val(y, "production") for y in years]})
    rows.append({"label": "Imports", "values": [val(y, "imports") for y in years]})
    supply = []
    for y in years:
        bs, pr, im = val(y, "beginning_stocks"), val(y, "production"), val(y, "imports")
        supply.append(round(bs + pr + im, 1) if all(v is not None for v in [bs, pr, im]) else val(y, "total_supply"))
    rows.append({"label": "Total supply", "values": supply, "bold": True})

    crush = [val(y, "crush") for y in years]
    fsi = [val(y, "fsi_consumption") for y in years]
    feed = [val(y, "feed_dom") for y in years]
    dom = [val(y, "total_consumption") for y in years]
    rows.append({"label": "Crush", "values": crush, "spaceBefore": True})
    rows.append({"label": "Food use", "values": fsi})
    rows.append({"label": "Feed", "values": feed})
    rows.append({"label": "Domestic consumption", "values": dom})
    exp = [val(y, "exports") for y in years]
    rows.append({"label": "Exports", "values": exp})
    tu = [round(dom[i] + exp[i], 1) if dom[i] is not None and exp[i] is not None else None for i in range(len(years))]
    rows.append({"label": "Total usage", "values": tu, "bold": True})

    es = [val(y, "ending_stocks") for y in years]
    rows.append({"label": "Ending stocks", "values": es, "bold": True, "spaceBefore": True})
    rows.append({"label": "Stocks/use (%)", "values": [pct(es[i], tu[i]) for i in range(len(years))], "bold": True, "pct": True})
    return rows


def build_country_rows_wheat(data_by_year, country_code, years):
    """Build wheat country rows with FSI/feed breakdown."""
    rows = []
    def val(yr, attr, conv=to_mmt):
        d = data_by_year.get(yr, {}).get(country_code, {})
        return conv(d.get(attr))

    rows.append({"label": "Area harvested", "values": [val(y, "area_harvested", to_mha) for y in years]})
    rows.append({"label": "Yield", "values": [val(y, "yield", to_yield) for y in years]})
    rows.append({"label": "Beginning stocks", "values": [val(y, "beginning_stocks") for y in years], "spaceBefore": True})
    rows.append({"label": "Production", "values": [val(y, "production") for y in years]})
    rows.append({"label": "Imports", "values": [val(y, "imports") for y in years]})
    supply = []
    for y in years:
        bs, pr, im = val(y, "beginning_stocks"), val(y, "production"), val(y, "imports")
        supply.append(round(bs + pr + im, 1) if all(v is not None for v in [bs, pr, im]) else val(y, "total_supply"))
    rows.append({"label": "Total supply", "values": supply, "bold": True})

    fsi = [val(y, "fsi_consumption") for y in years]
    feed = [val(y, "feed_dom") for y in years]
    dom = [val(y, "total_consumption") for y in years]
    rows.append({"label": "FSI consumption", "values": fsi, "spaceBefore": True})
    rows.append({"label": "Feed consumption", "values": feed})
    rows.append({"label": "Domestic consumption", "values": dom})
    exp = [val(y, "exports") for y in years]
    rows.append({"label": "Exports", "values": exp})
    tu = [round(dom[i] + exp[i], 1) if dom[i] is not None and exp[i] is not None else None for i in range(len(years))]
    rows.append({"label": "Total usage", "values": tu, "bold": True})

    es = [val(y, "ending_stocks") for y in years]
    rows.append({"label": "Ending stocks", "values": es, "bold": True, "spaceBefore": True})
    rows.append({"label": "Stocks/use (%)", "values": [pct(es[i], tu[i]) for i in range(len(years))], "bold": True, "pct": True})
    return rows


def build_country_rows_simple(data_by_year, country_code, years):
    """Build simple country rows for meal/oil (no area/yield, no use breakdown)."""
    rows = []
    def val(yr, attr, conv=to_mmt):
        d = data_by_year.get(yr, {}).get(country_code, {})
        return conv(d.get(attr))

    rows.append({"label": "Beginning stocks", "values": [val(y, "beginning_stocks") for y in years]})
    rows.append({"label": "Production", "values": [val(y, "production") for y in years]})
    rows.append({"label": "Imports", "values": [val(y, "imports") for y in years]})
    dom = [val(y, "total_consumption") for y in years]
    rows.append({"label": "Domestic consumption", "values": dom})
    exp = [val(y, "exports") for y in years]
    rows.append({"label": "Exports", "values": exp})
    tu = [round(dom[i] + exp[i], 1) if dom[i] is not None and exp[i] is not None else None for i in range(len(years))]
    rows.append({"label": "Total usage", "values": tu, "bold": True})
    es = [val(y, "ending_stocks") for y in years]
    rows.append({"label": "Ending stocks", "values": es, "bold": True, "spaceBefore": True})
    return rows


def aggregate_world(data_by_year, attr, years, conv=to_mmt):
    """Sum an attribute across ALL countries for each year."""
    result = []
    for y in years:
        year_data = data_by_year.get(y, {})
        total = 0
        has_data = False
        for cc, attrs in year_data.items():
            v = attrs.get(attr)
            if v is not None:
                total += v
                has_data = True
        result.append(conv(total) if has_data else None)
    return result


def build_world_rows_corn(data_by_year, years):
    """Build world total rows for corn."""
    area = aggregate_world(data_by_year, "area_harvested", years, to_mha)
    yld_prod = aggregate_world(data_by_year, "production", years, lambda v: v)  # raw 1000 MT
    yld_area = aggregate_world(data_by_year, "area_harvested", years, lambda v: v)  # raw 1000 HA
    yld = [round(yld_prod[i] / yld_area[i], 2) if yld_area[i] and yld_prod[i] else None for i in range(len(years))]

    bs = aggregate_world(data_by_year, "beginning_stocks", years)
    prod = aggregate_world(data_by_year, "production", years)
    imp = aggregate_world(data_by_year, "imports", years)
    supply = [round(bs[i] + prod[i] + imp[i], 1) if all(v is not None for v in [bs[i], prod[i], imp[i]]) else None for i in range(len(years))]
    feed = aggregate_world(data_by_year, "feed_dom", years)
    fsi = aggregate_world(data_by_year, "fsi_consumption", years)
    dom = aggregate_world(data_by_year, "total_consumption", years)
    exp = aggregate_world(data_by_year, "exports", years)
    tu = [round(dom[i] + exp[i], 1) if dom[i] is not None and exp[i] is not None else None for i in range(len(years))]
    es = aggregate_world(data_by_year, "ending_stocks", years)

    return [
        {"label": "Area harvested", "values": area},
        {"label": "Yield", "values": yld},
        {"label": "Beginning stocks", "values": bs, "spaceBefore": True},
        {"label": "Production", "values": prod},
        {"label": "Imports", "values": imp},
        {"label": "Total supply", "values": supply, "bold": True},
        {"label": "Feed dom. consumption", "values": feed, "spaceBefore": True},
        {"label": "FSI consumption", "values": fsi},
        {"label": "Domestic consumption", "values": dom},
        {"label": "Exports", "values": exp},
        {"label": "Total usage", "values": tu, "bold": True},
        {"label": "Ending stocks", "values": es, "bold": True, "spaceBefore": True},
        {"label": "Stocks/use (%)", "values": [pct(es[i], tu[i]) for i in range(len(years))], "bold": True, "pct": True},
    ]


def build_world_rows_soybeans(data_by_year, years):
    bs = aggregate_world(data_by_year, "beginning_stocks", years)
    prod = aggregate_world(data_by_year, "production", years)
    imp = aggregate_world(data_by_year, "imports", years)
    supply = [round(bs[i] + prod[i] + imp[i], 1) if all(v is not None for v in [bs[i], prod[i], imp[i]]) else None for i in range(len(years))]
    area = aggregate_world(data_by_year, "area_harvested", years, to_mha)
    yld_prod = aggregate_world(data_by_year, "production", years, lambda v: v)
    yld_area = aggregate_world(data_by_year, "area_harvested", years, lambda v: v)
    yld = [round(yld_prod[i] / yld_area[i], 2) if yld_area[i] and yld_prod[i] else None for i in range(len(years))]
    crush = aggregate_world(data_by_year, "crush", years)
    fsi = aggregate_world(data_by_year, "fsi_consumption", years)
    feed = aggregate_world(data_by_year, "feed_dom", years)
    dom = aggregate_world(data_by_year, "total_consumption", years)
    exp = aggregate_world(data_by_year, "exports", years)
    tu = [round(dom[i] + exp[i], 1) if dom[i] is not None and exp[i] is not None else None for i in range(len(years))]
    es = aggregate_world(data_by_year, "ending_stocks", years)
    return [
        {"label": "Area harvested", "values": area},
        {"label": "Yield", "values": yld},
        {"label": "Beginning stocks", "values": bs, "spaceBefore": True},
        {"label": "Production", "values": prod},
        {"label": "Imports", "values": imp},
        {"label": "Total supply", "values": supply, "bold": True},
        {"label": "Crush", "values": crush, "spaceBefore": True},
        {"label": "Food use", "values": fsi},
        {"label": "Feed", "values": feed},
        {"label": "Domestic consumption", "values": dom},
        {"label": "Exports", "values": exp},
        {"label": "Total usage", "values": tu, "bold": True},
        {"label": "Ending stocks", "values": es, "bold": True, "spaceBefore": True},
        {"label": "Stocks/use (%)", "values": [pct(es[i], tu[i]) for i in range(len(years))], "bold": True, "pct": True},
    ]


def build_world_rows_wheat(data_by_year, years):
    area = aggregate_world(data_by_year, "area_harvested", years, to_mha)
    yld_prod = aggregate_world(data_by_year, "production", years, lambda v: v)
    yld_area = aggregate_world(data_by_year, "area_harvested", years, lambda v: v)
    yld = [round(yld_prod[i] / yld_area[i], 2) if yld_area[i] and yld_prod[i] else None for i in range(len(years))]
    bs = aggregate_world(data_by_year, "beginning_stocks", years)
    prod = aggregate_world(data_by_year, "production", years)
    imp = aggregate_world(data_by_year, "imports", years)
    supply = [round(bs[i] + prod[i] + imp[i], 1) if all(v is not None for v in [bs[i], prod[i], imp[i]]) else None for i in range(len(years))]
    fsi = aggregate_world(data_by_year, "fsi_consumption", years)
    feed = aggregate_world(data_by_year, "feed_dom", years)
    dom = aggregate_world(data_by_year, "total_consumption", years)
    exp = aggregate_world(data_by_year, "exports", years)
    tu = [round(dom[i] + exp[i], 1) if dom[i] is not None and exp[i] is not None else None for i in range(len(years))]
    es = aggregate_world(data_by_year, "ending_stocks", years)
    return [
        {"label": "Area harvested", "values": area},
        {"label": "Yield", "values": yld},
        {"label": "Beginning stocks", "values": bs, "spaceBefore": True},
        {"label": "Production", "values": prod},
        {"label": "Imports", "values": imp},
        {"label": "Total supply", "values": supply, "bold": True},
        {"label": "FSI consumption", "values": fsi, "spaceBefore": True},
        {"label": "Feed consumption", "values": feed},
        {"label": "Domestic consumption", "values": dom},
        {"label": "Exports", "values": exp},
        {"label": "Total usage", "values": tu, "bold": True},
        {"label": "Ending stocks", "values": es, "bold": True, "spaceBefore": True},
        {"label": "Stocks/use (%)", "values": [pct(es[i], tu[i]) for i in range(len(years))], "bold": True, "pct": True},
    ]


def build_world_rows_simple(data_by_year, years):
    """World total for meal/oil — simpler structure."""
    bs = aggregate_world(data_by_year, "beginning_stocks", years)
    prod = aggregate_world(data_by_year, "production", years)
    imp = aggregate_world(data_by_year, "imports", years)
    dom = aggregate_world(data_by_year, "total_consumption", years)
    exp = aggregate_world(data_by_year, "exports", years)
    es = aggregate_world(data_by_year, "ending_stocks", years)
    return [
        {"label": "Beginning stocks", "values": bs},
        {"label": "Production", "values": prod},
        {"label": "Imports", "values": imp},
        {"label": "Domestic consumption", "values": dom},
        {"label": "Exports", "values": exp},
        {"label": "Ending stocks", "values": es, "bold": True},
    ]


# Map commodity to row builders
WORLD_BUILDERS = {
    "corn": (build_world_rows_corn, build_country_rows_corn),
    "soybeans": (build_world_rows_soybeans, build_country_rows_soybeans),
    "wheat": (build_world_rows_wheat, build_country_rows_wheat),
    "soybean_meal": (build_world_rows_simple, build_country_rows_simple),
    "soybean_oil": (build_world_rows_simple, build_country_rows_simple),
}


def main():
    if not API_KEY:
        print("ERROR: PSD_API_KEY not set. Pass as environment variable.")
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    # Load existing data to preserve US balance sheets
    existing = {}
    if os.path.exists(output_file):
        try:
            with open(output_file) as f:
                existing = json.load(f)
            print(f"Loaded existing: us={list(existing.get('us', {}).keys())}")
        except: pass

    print("=" * 60)
    print("PSD World Balance Sheet Fetch")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print(f"Years: {MARKET_YEARS[0]}/{MARKET_YEARS[0]+1-2000} to {MARKET_YEARS[-1]}/{MARKET_YEARS[-1]+1-2000}")
    print("=" * 60)

    year_labels = [f"{y}/{str(y+1)[-2:]}" for y in MARKET_YEARS]
    world_data = {}

    for comm_id, comm_code in COMMODITIES.items():
        print(f"\n-- {comm_id.upper()} (code {comm_code}) --")
        data_by_year = {}  # {market_year: {country_code: {attr: value}}}

        for my in MARKET_YEARS:
            print(f"  Fetching MY {my}...", end=" ")
            records = fetch_psd(comm_code, my)
            if records:
                parsed = parse_psd_response(records)
                data_by_year[my] = parsed
                print(f"{len(records)} records, {len(parsed)} countries")
            else:
                print("no data")
            time.sleep(0.3)  # Rate limiting

        if not data_by_year:
            print(f"  No data fetched for {comm_id}")
            continue

        # Build world total and country tables
        world_builder, country_builder = WORLD_BUILDERS[comm_id]
        countries_config = COUNTRIES[comm_id]

        world_rows = world_builder(data_by_year, MARKET_YEARS)
        print(f"  World total: {len(world_rows)} rows")

        countries_list = []
        for cc, name in countries_config.items():
            # Check if this country has data
            has_data = any(cc in data_by_year.get(my, {}) for my in MARKET_YEARS)
            if not has_data:
                print(f"  {name} ({cc}): no data found")
                continue
            country_rows = country_builder(data_by_year, cc, MARKET_YEARS)
            countries_list.append({"label": name, "rows": country_rows})
            print(f"  {name}: {len(country_rows)} rows")

        world_data[comm_id] = {
            "label": comm_id.replace("_", " ").title(),
            "id": comm_id,
            "years": year_labels,
            "sections": [{"header": "World total", "unit": "million metric tons", "rows": world_rows}],
            "countries": countries_list,
        }

    # Merge with existing data
    result = existing.copy()
    result["world"] = world_data
    result["world_fetched_at"] = datetime.utcnow().isoformat() + "Z"

    print(f"\n{'='*60}")
    print(f"RESULTS: {len(world_data)} commodities")
    for cid, d in world_data.items():
        nr = sum(len(s["rows"]) for s in d["sections"])
        nc = len(d.get("countries", []))
        print(f"  {cid}: world={nr} rows, {nc} countries")
        # Print sample values
        for s in d["sections"]:
            for r in s["rows"][:3]:
                print(f"    {r['label']}: ...{r['values'][-3:]}")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
