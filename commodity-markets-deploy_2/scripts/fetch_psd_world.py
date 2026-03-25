#!/usr/bin/env python3
"""
Fetch world balance sheet data from USDA PSD Online API.
Uses psd_history.csv as historical baseline, fetches last 5 years from API.
Outputs world data into wasde.json alongside US data.
"""

import csv as csvmod
import json, os, sys, urllib.request, urllib.error, time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

API_BASE = "https://apps.fas.usda.gov/PSDOnlineDataServices/api/CommodityData/GetCommodityDataByYear"
API_KEY = os.environ.get("PSD_API_KEY", "")

COMMODITIES = {
    "corn":          "0440000",
    "soybeans":      "2222000",
    "wheat":         "0410000",
    "soybean_meal":  "0813100",
    "soybean_oil":   "4232000",
}

COUNTRIES = {
    "corn":         {"AR": "Argentina", "BR": "Brazil", "CH": "China", "UP": "Ukraine", "US": "United States"},
    "soybeans":     {"AR": "Argentina", "BR": "Brazil", "CH": "China", "PA": "Paraguay", "US": "United States"},
    "soybean_meal": {"AR": "Argentina", "BR": "Brazil", "CH": "China", "E4": "EU", "US": "United States"},
    "soybean_oil":  {"AR": "Argentina", "BR": "Brazil", "CH": "China", "IN": "India", "US": "United States"},
    "wheat":        {"AR": "Argentina", "AS": "Australia", "CA": "Canada", "CH": "China", "E4": "EU", "RS": "Russia", "UP": "Ukraine", "US": "United States"},
}

ATTR = {
    4:   "area_harvested",
    184: "yield",
    20:  "beginning_stocks",
    28:  "production",
    57:  "imports",
    86:  "total_supply",
    130: "feed_dom",
    192: "fsi_consumption",
    125: "total_consumption",
    88:  "exports",
    176: "ending_stocks",
    178: "total_distribution",
    7:   "crush",
    149: "food_use",
    161: "feed_waste",
}

COMMODITY_START_YEARS = {
    "corn": 1975, "soybeans": 1980, "wheat": 1984,
    "soybean_meal": 1980, "soybean_oil": 1980,
}
CURRENT_YEAR = 2025
REFRESH_YEARS_COUNT = 5


def fetch_psd(commodity_code, market_year):
    url = f"{API_BASE}?commodityCode={commodity_code}&marketYear={market_year}"
    req = urllib.request.Request(url, headers={"Accept": "application/json", "API_KEY": API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"    Error: {e}")
        return None


def parse_psd_response(records):
    result = {}
    for rec in records:
        cc = rec.get("CountryCode", "").strip()
        attr_id = rec.get("AttributeId")
        value = rec.get("Value")
        if attr_id not in ATTR: continue
        attr_name = ATTR[attr_id]
        if cc not in result: result[cc] = {}
        result[cc][attr_name] = value
    return result


def load_csv_baseline(csv_path):
    """Load psd_history.csv into {commodity_id: {market_year: {country_code: {attr_name: value}}}}"""
    result = {}
    if not os.path.exists(csv_path):
        print(f"  CSV not found: {csv_path}")
        return result
    attr_id_map = {str(k): v for k, v in ATTR.items()}
    with open(csv_path, "r") as f:
        reader = csvmod.DictReader(f)
        for row in reader:
            cid = row["commodity_id"]
            cc = row["country_code"]
            my = int(row["market_year"])
            attr_name = attr_id_map.get(row["attr_id"])
            if not attr_name: continue
            try:
                val = float(row["value"]) if row["value"] not in ("", "None", "null") else None
            except (ValueError, TypeError):
                val = None
            result.setdefault(cid, {}).setdefault(my, {}).setdefault(cc, {})[attr_name] = val
    for cid in result:
        years = sorted(result[cid].keys())
        print(f"  CSV {cid}: {len(years)} years ({years[0]}-{years[-1]})")
    return result


def to_mmt(v):
    return round(v / 1000, 1) if v is not None else None

def to_mha(v):
    return round(v / 1000, 1) if v is not None else None

def to_yield(v):
    return round(v, 2) if v is not None else None

def pct(num, den):
    return round(num / den * 100, 1) if num is not None and den is not None and den != 0 else None


# ══════════════════════════════════════════════════
# Row builders (identical logic for all modes)
# ══════════════════════════════════════════════════

def _val(data_by_year, yr, country_code, attr, conv=to_mmt):
    d = data_by_year.get(yr, {}).get(country_code, {})
    return conv(d.get(attr))

def _supply(bs, pr, im, fallback=None):
    if all(v is not None for v in [bs, pr, im]):
        return round(bs + pr + im, 1)
    return fallback

def _tu(dom, exp):
    if dom is not None and exp is not None:
        return round(dom + exp, 1)
    return None

def aggregate_world(data_by_year, attr, years, conv=to_mmt):
    result = []
    for y in years:
        total = 0; has = False
        for cc, attrs in data_by_year.get(y, {}).items():
            v = attrs.get(attr)
            if v is not None: total += v; has = True
        result.append(conv(total) if has else None)
    return result


def build_country_rows_corn(data_by_year, cc, years):
    def v(yr, attr, conv=to_mmt): return _val(data_by_year, yr, cc, attr, conv)
    rows = [
        {"label": "Area harvested", "values": [v(y, "area_harvested", to_mha) for y in years]},
        {"label": "Yield", "values": [v(y, "yield", to_yield) for y in years]},
        {"label": "Beginning stocks", "values": [v(y, "beginning_stocks") for y in years]},
        {"label": "Production", "values": [v(y, "production") for y in years]},
        {"label": "Imports", "values": [v(y, "imports") for y in years]},
        {"label": "Total supply", "values": [_supply(v(y,"beginning_stocks"),v(y,"production"),v(y,"imports"),v(y,"total_supply")) for y in years], "bold": True},
    ]
    feed=[v(y,"feed_dom") for y in years]; fsi=[v(y,"fsi_consumption") for y in years]; dom=[v(y,"total_consumption") for y in years]; exp=[v(y,"exports") for y in years]
    tu=[_tu(dom[i],exp[i]) for i in range(len(years))]; es=[v(y,"ending_stocks") for y in years]
    rows += [
        {"label": "Feed dom. consumption", "values": feed},
        {"label": "FSI consumption", "values": fsi},
        {"label": "Domestic consumption", "values": dom},
        {"label": "Exports", "values": exp},
        {"label": "Total usage", "values": tu, "bold": True},
        {"label": "Ending stocks", "values": es, "bold": True},
        {"label": "Stocks/use (%)", "values": [pct(es[i],tu[i]) for i in range(len(years))], "bold": True, "pct": True},
    ]
    return rows

def build_country_rows_soybeans(data_by_year, cc, years):
    def v(yr, attr, conv=to_mmt): return _val(data_by_year, yr, cc, attr, conv)
    rows = [
        {"label": "Area harvested", "values": [v(y, "area_harvested", to_mha) for y in years]},
        {"label": "Yield", "values": [v(y, "yield", to_yield) for y in years]},
        {"label": "Beginning stocks", "values": [v(y, "beginning_stocks") for y in years]},
        {"label": "Production", "values": [v(y, "production") for y in years]},
        {"label": "Imports", "values": [v(y, "imports") for y in years]},
        {"label": "Total supply", "values": [_supply(v(y,"beginning_stocks"),v(y,"production"),v(y,"imports"),v(y,"total_supply")) for y in years], "bold": True},
    ]
    crush=[v(y,"crush") for y in years]; food=[v(y,"food_use") for y in years]; feed=[v(y,"feed_waste") for y in years]
    dom=[v(y,"total_consumption") for y in years]; exp=[v(y,"exports") for y in years]
    tu=[_tu(dom[i],exp[i]) for i in range(len(years))]; es=[v(y,"ending_stocks") for y in years]
    rows += [
        {"label": "Crush", "values": crush},
        {"label": "Food use", "values": food},
        {"label": "Feed", "values": feed},
        {"label": "Domestic consumption", "values": dom},
        {"label": "Exports", "values": exp},
        {"label": "Total usage", "values": tu, "bold": True},
        {"label": "Ending stocks", "values": es, "bold": True},
        {"label": "Stocks/use (%)", "values": [pct(es[i],tu[i]) for i in range(len(years))], "bold": True, "pct": True},
    ]
    return rows

def build_country_rows_wheat(data_by_year, cc, years):
    def v(yr, attr, conv=to_mmt): return _val(data_by_year, yr, cc, attr, conv)
    rows = [
        {"label": "Area harvested", "values": [v(y, "area_harvested", to_mha) for y in years]},
        {"label": "Yield", "values": [v(y, "yield", to_yield) for y in years]},
        {"label": "Beginning stocks", "values": [v(y, "beginning_stocks") for y in years]},
        {"label": "Production", "values": [v(y, "production") for y in years]},
        {"label": "Imports", "values": [v(y, "imports") for y in years]},
        {"label": "Total supply", "values": [_supply(v(y,"beginning_stocks"),v(y,"production"),v(y,"imports"),v(y,"total_supply")) for y in years], "bold": True},
    ]
    fsi=[v(y,"fsi_consumption") for y in years]; feed=[v(y,"feed_dom") for y in years]
    dom=[v(y,"total_consumption") for y in years]; exp=[v(y,"exports") for y in years]
    tu=[_tu(dom[i],exp[i]) for i in range(len(years))]; es=[v(y,"ending_stocks") for y in years]
    rows += [
        {"label": "FSI consumption", "values": fsi},
        {"label": "Feed consumption", "values": feed},
        {"label": "Domestic consumption", "values": dom},
        {"label": "Exports", "values": exp},
        {"label": "Total usage", "values": tu, "bold": True},
        {"label": "Ending stocks", "values": es, "bold": True},
        {"label": "Stocks/use (%)", "values": [pct(es[i],tu[i]) for i in range(len(years))], "bold": True, "pct": True},
    ]
    return rows

def build_country_rows_simple(data_by_year, cc, years):
    def v(yr, attr, conv=to_mmt): return _val(data_by_year, yr, cc, attr, conv)
    dom=[v(y,"total_consumption") for y in years]; exp=[v(y,"exports") for y in years]
    tu=[_tu(dom[i],exp[i]) for i in range(len(years))]; es=[v(y,"ending_stocks") for y in years]
    return [
        {"label": "Beginning stocks", "values": [v(y, "beginning_stocks") for y in years]},
        {"label": "Production", "values": [v(y, "production") for y in years]},
        {"label": "Imports", "values": [v(y, "imports") for y in years]},
        {"label": "Domestic consumption", "values": dom},
        {"label": "Exports", "values": exp},
        {"label": "Total usage", "values": tu, "bold": True},
        {"label": "Ending stocks", "values": es, "bold": True},
    ]

def build_world_rows_corn(dby, years):
    a=aggregate_world(dby,"area_harvested",years,to_mha); yp=aggregate_world(dby,"production",years,lambda v:v); ya=aggregate_world(dby,"area_harvested",years,lambda v:v)
    yld=[round(yp[i]/ya[i],2) if ya[i] and yp[i] else None for i in range(len(years))]
    bs=aggregate_world(dby,"beginning_stocks",years); p=aggregate_world(dby,"production",years); im=aggregate_world(dby,"imports",years)
    sup=[round(bs[i]+p[i]+im[i],1) if all(v is not None for v in [bs[i],p[i],im[i]]) else None for i in range(len(years))]
    f=aggregate_world(dby,"feed_dom",years); fsi=aggregate_world(dby,"fsi_consumption",years); d=aggregate_world(dby,"total_consumption",years)
    e=aggregate_world(dby,"exports",years); tu=[_tu(d[i],e[i]) for i in range(len(years))]; es=aggregate_world(dby,"ending_stocks",years)
    return [{"label":"Area harvested","values":a},{"label":"Yield","values":yld},
        {"label":"Beginning stocks","values":bs},{"label":"Production","values":p},{"label":"Imports","values":im},{"label":"Total supply","values":sup,"bold":True},
        {"label":"Feed dom. consumption","values":f},{"label":"FSI consumption","values":fsi},{"label":"Domestic consumption","values":d},{"label":"Exports","values":e},{"label":"Total usage","values":tu,"bold":True},
        {"label":"Ending stocks","values":es,"bold":True},{"label":"Stocks/use (%)","values":[pct(es[i],tu[i]) for i in range(len(years))],"bold":True,"pct":True}]

def build_world_rows_soybeans(dby, years):
    a=aggregate_world(dby,"area_harvested",years,to_mha); yp=aggregate_world(dby,"production",years,lambda v:v); ya=aggregate_world(dby,"area_harvested",years,lambda v:v)
    yld=[round(yp[i]/ya[i],2) if ya[i] and yp[i] else None for i in range(len(years))]
    bs=aggregate_world(dby,"beginning_stocks",years); p=aggregate_world(dby,"production",years); im=aggregate_world(dby,"imports",years)
    sup=[round(bs[i]+p[i]+im[i],1) if all(v is not None for v in [bs[i],p[i],im[i]]) else None for i in range(len(years))]
    cr=aggregate_world(dby,"crush",years); fo=aggregate_world(dby,"food_use",years); fe=aggregate_world(dby,"feed_waste",years)
    d=aggregate_world(dby,"total_consumption",years); e=aggregate_world(dby,"exports",years)
    tu=[_tu(d[i],e[i]) for i in range(len(years))]; es=aggregate_world(dby,"ending_stocks",years)
    return [{"label":"Area harvested","values":a},{"label":"Yield","values":yld},
        {"label":"Beginning stocks","values":bs},{"label":"Production","values":p},{"label":"Imports","values":im},{"label":"Total supply","values":sup,"bold":True},
        {"label":"Crush","values":cr},{"label":"Food use","values":fo},{"label":"Feed","values":fe},{"label":"Domestic consumption","values":d},{"label":"Exports","values":e},{"label":"Total usage","values":tu,"bold":True},
        {"label":"Ending stocks","values":es,"bold":True},{"label":"Stocks/use (%)","values":[pct(es[i],tu[i]) for i in range(len(years))],"bold":True,"pct":True}]

def build_world_rows_wheat(dby, years):
    a=aggregate_world(dby,"area_harvested",years,to_mha); yp=aggregate_world(dby,"production",years,lambda v:v); ya=aggregate_world(dby,"area_harvested",years,lambda v:v)
    yld=[round(yp[i]/ya[i],2) if ya[i] and yp[i] else None for i in range(len(years))]
    bs=aggregate_world(dby,"beginning_stocks",years); p=aggregate_world(dby,"production",years); im=aggregate_world(dby,"imports",years)
    sup=[round(bs[i]+p[i]+im[i],1) if all(v is not None for v in [bs[i],p[i],im[i]]) else None for i in range(len(years))]
    fsi=aggregate_world(dby,"fsi_consumption",years); fe=aggregate_world(dby,"feed_dom",years); d=aggregate_world(dby,"total_consumption",years)
    e=aggregate_world(dby,"exports",years); tu=[_tu(d[i],e[i]) for i in range(len(years))]; es=aggregate_world(dby,"ending_stocks",years)
    return [{"label":"Area harvested","values":a},{"label":"Yield","values":yld},
        {"label":"Beginning stocks","values":bs},{"label":"Production","values":p},{"label":"Imports","values":im},{"label":"Total supply","values":sup,"bold":True},
        {"label":"FSI consumption","values":fsi},{"label":"Feed consumption","values":fe},{"label":"Domestic consumption","values":d},{"label":"Exports","values":e},{"label":"Total usage","values":tu,"bold":True},
        {"label":"Ending stocks","values":es,"bold":True},{"label":"Stocks/use (%)","values":[pct(es[i],tu[i]) for i in range(len(years))],"bold":True,"pct":True}]

def build_world_rows_simple(dby, years):
    bs=aggregate_world(dby,"beginning_stocks",years); p=aggregate_world(dby,"production",years); im=aggregate_world(dby,"imports",years)
    d=aggregate_world(dby,"total_consumption",years); e=aggregate_world(dby,"exports",years); es=aggregate_world(dby,"ending_stocks",years)
    return [{"label":"Beginning stocks","values":bs},{"label":"Production","values":p},{"label":"Imports","values":im},
        {"label":"Domestic consumption","values":d},{"label":"Exports","values":e},{"label":"Ending stocks","values":es,"bold":True}]

WORLD_BUILDERS = {
    "corn": (build_world_rows_corn, build_country_rows_corn),
    "soybeans": (build_world_rows_soybeans, build_country_rows_soybeans),
    "wheat": (build_world_rows_wheat, build_country_rows_wheat),
    "soybean_meal": (build_world_rows_simple, build_country_rows_simple),
    "soybean_oil": (build_world_rows_simple, build_country_rows_simple),
}


def main():
    if not API_KEY:
        print("ERROR: PSD_API_KEY not set.")
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")
    csv_baseline = os.path.join(OUTPUT_DIR, "psd_history.csv")

    existing = {}
    if os.path.exists(output_file):
        try:
            with open(output_file) as f: existing = json.load(f)
            print(f"Loaded wasde.json: us={list(existing.get('us',{}).keys())}")
        except: pass

    print("=" * 60)
    print("PSD World Balance Sheet Fetch")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)

    print("\n-- Loading CSV baseline --")
    csv_data = load_csv_baseline(csv_baseline)

    refresh_years = list(range(CURRENT_YEAR - REFRESH_YEARS_COUNT + 1, CURRENT_YEAR + 1))
    print(f"\n-- API refresh: {refresh_years} ({REFRESH_YEARS_COUNT} years) --")

    world_data = {}
    for comm_id, comm_code in COMMODITIES.items():
        start = COMMODITY_START_YEARS.get(comm_id, 2015)
        all_years = list(range(start, CURRENT_YEAR + 1))
        year_labels = [f"{y}/{str(y+1)[-2:]}" for y in all_years]
        print(f"\n-- {comm_id.upper()} ({len(all_years)} years: {year_labels[0]}..{year_labels[-1]}) --")

        # Load CSV baseline
        data_by_year = {}
        if comm_id in csv_data:
            for my in all_years:
                if my in csv_data[comm_id]: data_by_year[my] = csv_data[comm_id][my]
        print(f"  CSV: {len(data_by_year)} years")

        # API refresh for recent years
        api_years = [y for y in refresh_years if y >= start]
        for my in api_years:
            print(f"  API MY {my}...", end=" ", flush=True)
            records = fetch_psd(comm_code, my)
            if records:
                data_by_year[my] = parse_psd_response(records)
                print(f"{len(records)} records")
            else: print("no data")
            time.sleep(0.3)

        if not data_by_year: continue

        world_builder, country_builder = WORLD_BUILDERS[comm_id]
        world_rows = world_builder(data_by_year, all_years)
        countries_list = []
        for cc, name in COUNTRIES[comm_id].items():
            if any(cc in data_by_year.get(my, {}) for my in all_years):
                countries_list.append({"label": name, "rows": country_builder(data_by_year, cc, all_years)})
        print(f"  World: {len(world_rows)} rows, {len(countries_list)} countries")

        world_data[comm_id] = {
            "label": comm_id.replace("_", " ").title(), "id": comm_id, "years": year_labels,
            "sections": [{"header": "World total", "unit": "million metric tons", "rows": world_rows}],
            "countries": countries_list,
        }

    result = existing.copy()
    result["world"] = world_data
    result["world_fetched_at"] = datetime.utcnow().isoformat() + "Z"

    print(f"\n{'='*60}")
    print(f"RESULTS: {len(world_data)} commodities")
    for cid, d in world_data.items():
        nr = sum(len(s["rows"]) for s in d["sections"])
        print(f"  {cid}: {len(d['years'])} yrs, {nr} world rows, {len(d.get('countries',[]))} countries")
        for r in d["sections"][0]["rows"][:3]:
            print(f"    {r['label']}: ...{r['values'][-3:]}")

    with open(output_file, "w") as f: json.dump(result, f)
    print(f"\nWrote {os.path.getsize(output_file):,} bytes")
    return 0

if __name__ == "__main__":
    sys.exit(main())
