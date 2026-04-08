#!/usr/bin/env python3
"""
WASDE Data Fetch v11
- Wheat Table06: col0=MY, col1=Type ("All wheat"), col2+=S&D data
- Oil crops: tries current URL, falls back to cached data
"""

import json, os, sys, time, urllib.request, urllib.error, zipfile
from io import BytesIO
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

CORN_URL = "https://www.ers.usda.gov/media/5764/feed-grains-yearbook-tables-all-years.xlsx?v=77939"
OILCROPS_URLS = [
    "https://www.ers.usda.gov/media/5220/all-tables-oil-crops-yearbook.xlsx?v=57591",
    "https://www.ers.usda.gov/media/5220/all-tables-oil-crops-yearbook.xlsx",
    "https://www.ers.usda.gov/media/5219/all-tables-oil-crops-yearbook-complete-data-set-in-compressed-zip-file.zip?v=11593",
]
WHEAT_URL = "https://www.ers.usda.gov/media/5706/wheat-data-all-years.xlsx?v=53976"


def fetch_url(url, timeout=60, retries=3, delay=10):
    for attempt in range(1, retries + 1):
        print(f"  {'Try' if attempt==1 else 'Retry '+str(attempt)}: {url[:90]}...")
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
                print(f"  OK: {len(data):,} bytes")
                return data
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code}")
            if e.code in (404, 403, 410):
                return None  # Not found / forbidden — no point retrying
            if attempt < retries:
                time.sleep(delay)
        except Exception as e:
            print(f"  {e}")
            if attempt < retries:
                time.sleep(delay)
    return None

def fetch_with_fallbacks(urls, timeout=60):
    for url in urls:
        data = fetch_url(url, timeout)
        if data and len(data) > 100: return data
    return None

def to_float(v):
    if v is None: return None
    s = str(v).strip()
    if s in ("", "--", "NA", "N/A", "nan", "None"): return None
    try: return float(s.replace(",", ""))
    except ValueError: return None

def ri(v):
    return round(v) if v is not None else None

def r1(v):
    return round(v, 1) if v is not None else None

def pct(num, den):
    if num is not None and den is not None and den != 0:
        return round(num / den * 100, 1)
    return None


def parse_corn(wb_data):
    import openpyxl
    wb = openpyxl.load_workbook(BytesIO(wb_data), read_only=True, data_only=True)

    ws01 = wb["FGYearbookTable01"]
    rows01 = list(ws01.iter_rows(values_only=True))
    area_planted, area_harvested, yield_per_acre = {}, {}, {}
    in_corn = False
    for i in range(2, len(rows01)):
        row = rows01[i]
        if not row: continue
        commodity = str(row[0]).strip() if row[0] else ""
        if commodity == "Corn": in_corn = True
        elif commodity and in_corn: break
        if not in_corn: continue
        my = str(row[1]).strip() if row[1] else ""
        if "/" not in my or len(my) < 7: continue
        area_planted[my] = to_float(row[2])
        area_harvested[my] = to_float(row[3])
        yield_per_acre[my] = to_float(row[5])
    print(f"  Corn area: {len(area_planted)} years")

    ws04 = wb["FGYearbookTable04"]
    rows04 = list(ws04.iter_rows(values_only=True))
    header = rows04[1]
    ncols = len([c for c in header if c is not None])
    col_labels = [str(header[c]).strip().replace("\n", " ") if header[c] else f"Col{c}" for c in range(2, ncols)]

    current_my = None
    sd_years, sd_data = [], []
    for i in range(2, len(rows04)):
        row = rows04[i]
        if not row or len(row) < 2: continue
        col0 = str(row[0]).strip() if row[0] else ""
        if "/" in col0 and len(col0) >= 7: current_my = col0
        quarter = str(row[1]).strip() if row[1] else ""
        if quarter.startswith("MY") and current_my:
            sd_years.append(current_my)
            sd_data.append({label: to_float(row[2 + ci]) for ci, label in enumerate(col_labels)})
    print(f"  Corn S&D: {len(sd_years)} years")

    # --- Ethanol from Table31 ---
    # Table31: Corn FSI detail. Quarterly format like Table04.
    # Headers: Market year, Quarter, HFCS, Glucose/dextrose, Starch, Alcohol for fuel, Alcohol for beverages, Cereals/other, Seed, Total FSI
    ethanol_data = {}
    try:
        ws31 = wb["FGYearbookTable31"]
        rows31 = list(ws31.iter_rows(values_only=True))
        h31 = rows31[1]
        h31_labels = [str(h31[c]).strip().replace("\n", " ") if h31[c] else "" for c in range(2, len(h31))]
        print(f"  Table31 headers: {h31_labels}")
        # Find the "Alcohol for fuel" column index
        ethanol_col = None
        for ci, lbl in enumerate(h31_labels):
            if "alcohol for fuel" in lbl.lower() or "fuel" in lbl.lower():
                ethanol_col = ci
                break
        if ethanol_col is not None:
            print(f"  Ethanol column index: {ethanol_col}")
            current_my31 = None
            for i in range(2, len(rows31)):
                row = rows31[i]
                if not row or len(row) < 2: continue
                col0 = str(row[0]).strip() if row[0] else ""
                if "/" in col0 and len(col0) >= 7: current_my31 = col0
                quarter = str(row[1]).strip() if row[1] else ""
                if quarter.startswith("MY") and current_my31:
                    ethanol_data[current_my31] = to_float(row[2 + ethanol_col])
            print(f"  Ethanol: {len(ethanol_data)} years")
        else:
            print("  Ethanol column not found in Table31")
    except Exception as e:
        print(f"  Table31 error: {e}")

    years = sd_years
    rows_out = [
        {"label": "Area planted", "values": [r1(area_planted.get(y)) for y in years]},
        {"label": "Area harvested", "values": [r1(area_harvested.get(y)) for y in years]},
        {"label": "Yield per harvested acre", "values": [r1(yield_per_acre.get(y)) for y in years]},
    ]

    # Helper to get S&D values by column prefix
    def get_sd(prefix):
        key = next((k for k in col_labels if k.lower().startswith(prefix.lower())), None)
        return [ri(sd_data[yi].get(key)) if key else None for yi in range(len(years))]

    # Supply
    rows_out.append({"label": "Beginning stocks", "values": get_sd("Beginning stocks")})
    rows_out.append({"label": "Production", "values": get_sd("Production")})
    rows_out.append({"label": "Imports", "values": get_sd("Imports")})
    rows_out.append({"label": "Total supply", "values": get_sd("Total supply"), "bold": True})

    # Use — reordered: Feed/residual, FSI (=food/alcohol/industrial + seed), Ethanol (indent), Seed (indent), Total domestic
    fsi_raw = get_sd("Food, alcohol, and industrial")
    seed_vals = get_sd("Seed use")
    # FSI = food/alcohol/industrial + seed
    fsi_vals = []
    for i in range(len(years)):
        f, s = fsi_raw[i], seed_vals[i]
        if f is not None and s is not None:
            fsi_vals.append(f + s)
        elif f is not None:
            fsi_vals.append(f)
        else:
            fsi_vals.append(None)

    rows_out.append({"label": "Feed and residual", "values": get_sd("Feed and residual")})
    rows_out.append({"label": "Food, seed & industrial", "values": fsi_vals})
    rows_out.append({"label": "Ethanol", "values": [ri(ethanol_data.get(y)) for y in years], "indent": True})
    rows_out.append({"label": "Seed", "values": seed_vals, "indent": True})
    rows_out.append({"label": "Total domestic use", "values": get_sd("Total domestic"), "bold": True})
    rows_out.append({"label": "Exports", "values": get_sd("Exports")})
    rows_out.append({"label": "Total usage", "values": get_sd("Total use"), "bold": True})

    # Ending stocks
    es_vals = get_sd("Ending stocks")
    tu_vals = get_sd("Total use")
    rows_out.append({"label": "Ending stocks", "values": es_vals, "bold": True})
    rows_out.append({"label": "Stocks/use (%)", "values": [pct(es_vals[i], tu_vals[i]) for i in range(len(years))], "bold": True, "pct": True})

    return {"id": "corn", "label": "Corn", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}]}


def find_sheet(wb, *candidates):
    """Find a sheet by trying multiple name candidates."""
    for name in candidates:
        if name in wb.sheetnames:
            return wb[name]
    # Case-insensitive fallback
    for name in candidates:
        for sn in wb.sheetnames:
            if sn.lower() == name.lower():
                return wb[sn]
    return None


def parse_soybeans(wb):
    # Area: tab02 or Table02
    ws02 = find_sheet(wb, "tab02", "Table02", "Table 02")
    area_data = {}
    if not ws02:
        print("  Soy area sheet not found")
    else:
        rows02 = list(ws02.iter_rows(values_only=True))
        print(f"  Soy area sheet: {len(rows02)} rows")
        # Print first rows for debugging
        for i in range(min(6, len(rows02))):
            print(f"    Row {i}: {[str(c)[:25] if c else '' for c in (rows02[i] or [])][:7]}")
        
        for i in range(2, len(rows02)):
            row = rows02[i]
            if not row: continue
            year_val = str(row[0]).strip() if row[0] else ""
            
            # Try marketing year format first (1980/81)
            if "/" in year_val and len(year_val) >= 6:
                my = year_val
                planted = to_float(row[1])
                harvested = to_float(row[2])
                yld = to_float(row[3])
                # Check units: if planted > 500, it's in 1,000 acres, convert to million
                if planted and planted > 500:
                    planted = round(planted / 1000, 1)
                if harvested and harvested > 500:
                    harvested = round(harvested / 1000, 1)
                area_data[my] = {"planted": r1(planted), "harvested": r1(harvested), "yield": r1(yld)}
            else:
                # Try calendar year format (1980 -> 1980/81)
                try:
                    yr = int(year_val)
                    my = f"{yr}/{str(yr+1)[-2:]}"
                    planted = to_float(row[1])
                    harvested = to_float(row[2])
                    yld = to_float(row[3])
                    if planted and planted > 500:
                        planted = round(planted / 1000, 1)
                    if harvested and harvested > 500:
                        harvested = round(harvested / 1000, 1)
                    area_data[my] = {"planted": r1(planted), "harvested": r1(harvested), "yield": r1(yld)}
                except (ValueError, TypeError):
                    continue
    print(f"  Soy area: {len(area_data)} years")
    if area_data:
        s = list(area_data.keys())[-1]
        print(f"    Sample {s}: {area_data[s]}")

    # S&D: tab3 or Table03
    ws03 = find_sheet(wb, "tab3", "Table03", "Table 03", "tab03")
    if not ws03:
        print("  Soy S&D sheet not found")
        return None
    rows03 = list(ws03.iter_rows(values_only=True))
    print(f"  Soy S&D sheet: {len(rows03)} rows")
    # Print first data rows for format detection
    for i in range(min(8, len(rows03))):
        print(f"    Row {i}: {[str(c)[:20] if c else '' for c in (rows03[i] or [])][:11]}")

    # Find first data row (has marketing year in col 0)
    data_start = None
    for i in range(len(rows03)):
        row = rows03[i]
        if not row: continue
        val = str(row[0]).strip() if row[0] else ""
        if "/" in val and len(val) >= 6:
            try:
                int(val[:4])
                data_start = i
                break
            except ValueError:
                pass
    
    if data_start is None:
        print("  Could not find soy S&D data start")
        return None

    print(f"  Soy S&D data starts row {data_start}")
    if data_start < len(rows03):
        fr = rows03[data_start]
        print(f"    First data: {[str(c)[:15] if c else '' for c in (fr or [])][:12]}")

    years, sd = [], []
    for i in range(data_start, len(rows03)):
        row = rows03[i]
        if not row: continue
        my = str(row[0]).strip() if row[0] else ""
        if "/" not in my or len(my) < 6: continue
        try: int(my[:4])
        except ValueError: continue
        years.append(my)
        # Hardcoded: Table03 columns B through K (indices 1-10)
        # B=Beg stocks, C=Production, D=Imports, E=Total supply,
        # F=Crush, G=Seed use, H=Feed and residual, I=Exports, J=Total usage, K=Ending stocks
        sd.append([to_float(row[c]) if c < len(row) else None for c in range(1, 11)])

    print(f"  Soy S&D: {len(years)} years")

    # Explicit labels matching columns B through K (indices 1-10)
    sd_labels = [
        "Beginning stocks", "Production", "Imports", "Total supply",
        "Crush", "Seed use", "Feed and residual use", "Exports",
        "Total usage", "Ending stocks"
    ]

    rows_out = [
        {"label": "Area planted", "values": [area_data.get(y, {}).get("planted") for y in years]},
        {"label": "Area harvested", "values": [area_data.get(y, {}).get("harvested") for y in years]},
        {"label": "Yield per harvested acre", "values": [area_data.get(y, {}).get("yield") for y in years]},
    ]

    # Build S&D rows with proper spacing and calculated total domestic use
    # Supply section
    rows_out.append({"label": "Beginning stocks", "values": [ri(sd[yi][0]) for yi in range(len(years))]})
    rows_out.append({"label": "Production", "values": [ri(sd[yi][1]) for yi in range(len(years))]})
    rows_out.append({"label": "Imports", "values": [ri(sd[yi][2]) for yi in range(len(years))]})
    rows_out.append({"label": "Total supply", "values": [ri(sd[yi][3]) for yi in range(len(years))], "bold": True})

    # Use section
    crush_vals = [ri(sd[yi][4]) for yi in range(len(years))]
    seed_vals = [ri(sd[yi][5]) for yi in range(len(years))]
    feed_vals = [ri(sd[yi][6]) for yi in range(len(years))]
    # Calculate total domestic use = crush + seed + feed/residual
    dom_vals = []
    for yi in range(len(years)):
        c, s, f = crush_vals[yi], seed_vals[yi], feed_vals[yi]
        if c is not None and s is not None and f is not None:
            dom_vals.append(c + s + f)
        elif c is not None:
            dom_vals.append(c + (s or 0) + (f or 0))
        else:
            dom_vals.append(None)

    rows_out.append({"label": "Crush", "values": crush_vals})
    rows_out.append({"label": "Seed", "values": seed_vals})
    rows_out.append({"label": "Feed and residual", "values": feed_vals})
    rows_out.append({"label": "Total domestic use", "values": dom_vals, "bold": True})
    rows_out.append({"label": "Exports", "values": [ri(sd[yi][7]) for yi in range(len(years))]})
    rows_out.append({"label": "Total usage", "values": [ri(sd[yi][8]) for yi in range(len(years))], "bold": True})

    # Ending stocks + stocks/use
    es_vals = [ri(sd[yi][9]) for yi in range(len(years))]
    tu_vals = [ri(sd[yi][8]) for yi in range(len(years))]
    rows_out.append({"label": "Ending stocks", "values": es_vals, "bold": True})
    rows_out.append({"label": "Stocks/use (%)", "values": [pct(es_vals[i], tu_vals[i]) for i in range(len(years))], "bold": True, "pct": True})

    return {"id": "soybeans", "label": "Soybeans", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}]}


def parse_soymeal(wb):
    ws = find_sheet(wb, "tab4", "Table04", "Table 04", "tab04")
    if not ws:
        print("  Soy meal sheet not found")
        return None
    rows = list(ws.iter_rows(values_only=True))
    print(f"  Soy meal sheet: {len(rows)} rows")
    for i in range(min(8, len(rows))):
        print(f"    Row {i}: {[str(c)[:20] if c else '' for c in (rows[i] or [])][:11]}")

    # Find first data row
    data_start = None
    for i in range(len(rows)):
        row = rows[i]
        if not row: continue
        val = str(row[0]).strip() if row[0] else ""
        if "/" in val and len(val) >= 6:
            try:
                int(val[:4])
                data_start = i
                break
            except ValueError: pass
    if data_start is None:
        print("  Could not find meal data start")
        return None

    print(f"  Meal data starts row {data_start}")
    fr = rows[data_start]
    print(f"    First: {[str(c)[:15] if c else '' for c in (fr or [])][:11]}")

    years, sd = [], []
    for i in range(data_start, len(rows)):
        row = rows[i]
        if not row: continue
        my = str(row[0]).strip() if row[0] else ""
        if "/" not in my or len(my) < 6: continue
        try: int(my[:4])
        except ValueError: continue
        years.append(my)
        # Read columns B through J (indices 1-9)
        sd.append([to_float(row[c]) if c < len(row) else None for c in range(1, 10)])
    print(f"  Soy meal: {len(years)} years")

    # Table04 columns: B=Beg stocks, C=Production, D=Imports, E=Total supply,
    # F=Domestic use, G=Exports, H=Total disappearance(usage), I=Ending stocks, J=Price
    rows_out = []
    rows_out.append({"label": "Beginning stocks", "values": [ri(sd[yi][0]) for yi in range(len(years))]})
    rows_out.append({"label": "Production", "values": [ri(sd[yi][1]) for yi in range(len(years))]})
    rows_out.append({"label": "Imports", "values": [ri(sd[yi][2]) for yi in range(len(years))]})
    rows_out.append({"label": "Total supply", "values": [ri(sd[yi][3]) for yi in range(len(years))], "bold": True})

    rows_out.append({"label": "Domestic use", "values": [ri(sd[yi][4]) for yi in range(len(years))]})
    rows_out.append({"label": "Exports", "values": [ri(sd[yi][5]) for yi in range(len(years))]})
    rows_out.append({"label": "Total usage", "values": [ri(sd[yi][6]) for yi in range(len(years))], "bold": True})

    es_vals = [ri(sd[yi][7]) for yi in range(len(years))]
    rows_out.append({"label": "Ending stocks", "values": es_vals, "bold": True})

    return {"id": "soybean_meal", "label": "Soybean Meal", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "1,000 short tons", "rows": rows_out}]}


def parse_soyoil(wb):
    ws = find_sheet(wb, "tab5", "Table05", "Table 05", "tab05")
    if not ws:
        print("  Soy oil sheet not found")
        return None
    rows = list(ws.iter_rows(values_only=True))
    print(f"  Soy oil sheet: {len(rows)} rows")
    for i in range(min(8, len(rows))):
        print(f"    Row {i}: {[str(c)[:20] if c else '' for c in (rows[i] or [])][:11]}")

    # Find first data row
    data_start = None
    for i in range(len(rows)):
        row = rows[i]
        if not row: continue
        val = str(row[0]).strip() if row[0] else ""
        if "/" in val and len(val) >= 6:
            try:
                int(val[:4])
                data_start = i
                break
            except ValueError: pass
    if data_start is None:
        print("  Could not find oil data start")
        return None

    print(f"  Oil data starts row {data_start}")
    fr = rows[data_start]
    print(f"    First: {[str(c)[:15] if c else '' for c in (fr or [])][:11]}")

    years, sd = [], []
    for i in range(data_start, len(rows)):
        row = rows[i]
        if not row: continue
        my = str(row[0]).strip() if row[0] else ""
        if "/" not in my or len(my) < 6: continue
        try: int(my[:4])
        except ValueError: continue
        years.append(my)
        # Read columns B through K (indices 1-10)
        sd.append([to_float(row[c]) if c < len(row) else None for c in range(1, 11)])
    print(f"  Soy oil: {len(years)} years")

    # Table05 columns: B=Beg stocks, C=Production, D=Imports, E=Total supply,
    # F=Domestic total, G=Biofuel, H=Food/feed/other industrial, I=Exports, J=Total disappearance(usage), K=Ending stocks
    rows_out = []
    rows_out.append({"label": "Beginning stocks", "values": [ri(sd[yi][0]) for yi in range(len(years))]})
    rows_out.append({"label": "Production", "values": [ri(sd[yi][1]) for yi in range(len(years))]})
    rows_out.append({"label": "Imports", "values": [ri(sd[yi][2]) for yi in range(len(years))]})
    rows_out.append({"label": "Total supply", "values": [ri(sd[yi][3]) for yi in range(len(years))], "bold": True})

    rows_out.append({"label": "Domestic total", "values": [ri(sd[yi][4]) for yi in range(len(years))]})
    rows_out.append({"label": "Biofuel", "values": [ri(sd[yi][5]) for yi in range(len(years))], "indent": True})
    rows_out.append({"label": "Food, feed, and other industrial", "values": [ri(sd[yi][6]) for yi in range(len(years))], "indent": True})
    rows_out.append({"label": "Exports", "values": [ri(sd[yi][7]) for yi in range(len(years))]})
    rows_out.append({"label": "Total usage", "values": [ri(sd[yi][8]) for yi in range(len(years))], "bold": True})

    es_vals = [ri(sd[yi][9]) for yi in range(len(years))]
    rows_out.append({"label": "Ending stocks", "values": es_vals, "bold": True})

    return {"id": "soybean_oil", "label": "Soybean Oil", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "million pounds", "rows": rows_out}]}


def parse_wheat(wb_data):
    try:
        import pandas as pd
    except ImportError:
        print("  pandas not installed")
        return None

    xls = None
    for engine in ["calamine", "openpyxl", None]:
        try:
            xls = pd.ExcelFile(BytesIO(wb_data), engine=engine)
            print(f"  Wheat opened with: {engine}")
            break
        except: pass
    if xls is None: return None

    # Area from Table01: col0=Class, col1=MY, col2=Planted, col3=Harvested, col4=Production, col5=Yield
    # Filter for "All wheat"
    area_data = {}
    try:
        df = pd.read_excel(xls, sheet_name="Table01", header=None)
        rows = [tuple(r) for r in df.values.tolist()]
        print(f"  Wheat area: Table01, {len(rows)} rows")
        for i in range(2, len(rows)):
            row = rows[i]
            cls = str(row[0]).strip().lower() if pd.notna(row[0]) else ""
            if cls != "all wheat": continue
            my = str(row[1]).strip() if pd.notna(row[1]) else ""
            if "/" not in my or len(my) < 6: continue
            try: int(my[:4])
            except ValueError: continue
            area_data[my] = {
                "planted": r1(to_float(row[2])),
                "harvested": r1(to_float(row[3])),
                "yield": r1(to_float(row[5])),
            }
        print(f"    All wheat area: {len(area_data)} years")
        if area_data:
            s = list(area_data.keys())[-1]
            print(f"    Sample {s}: {area_data[s]}")
    except Exception as e:
        print(f"    Area error: {e}")

    # S&D from Table06: col0=MY, col1=Type ("All wheat"), col2+=S&D data
    try:
        df = pd.read_excel(xls, sheet_name="Table06", header=None)
        rows = [tuple(r) for r in df.values.tolist()]
        print(f"  Wheat S&D: Table06, {len(rows)} rows")

        # Header is row 1: col0=MY label, col1=Type label, col2+=S&D column names
        header = rows[1]
        col_labels = []
        for c in range(2, len(header)):
            val = str(header[c]).strip() if pd.notna(header[c]) else ""
            if val:
                col_labels.append(val)
            else:
                break
        print(f"    Columns ({len(col_labels)}): {col_labels}")

        # Data rows: col0=MY, col1=Type, col2+=values
        # Filter for rows where col1 = "All wheat"
        years, sd_data = [], []
        for i in range(2, len(rows)):
            row = rows[i]
            wheat_type = str(row[1]).strip().lower() if pd.notna(row[1]) else ""
            if wheat_type != "all wheat": continue
            my = str(row[0]).strip() if pd.notna(row[0]) else ""
            if "/" not in my or len(my) < 6: continue
            try: int(my[:4])
            except ValueError: continue
            years.append(my)
            sd_data.append([to_float(row[2 + c]) for c in range(len(col_labels))])

        print(f"    All wheat S&D: {len(years)} years ({years[0] if years else '?'}..{years[-1] if years else '?'})")

        if not years:
            print("    No All wheat S&D found")
            return None

        # Build output
        rows_out = []
        if area_data:
            rows_out.append({"label": "Area planted", "values": [area_data.get(y, {}).get("planted") for y in years]})
            rows_out.append({"label": "Area harvested", "values": [area_data.get(y, {}).get("harvested") for y in years]})
            rows_out.append({"label": "Yield per harvested acre", "values": [area_data.get(y, {}).get("yield") for y in years]})

        renames = {}
        for lbl in col_labels:
            lower = lbl.lower()
            if "total disappearance" in lower: renames[lbl] = "Total usage"
            elif "total supply" in lower: renames[lbl] = "Total supply"
            elif "total domestic" in lower: renames[lbl] = "Total domestic use"
            elif lower.strip() == "food use": renames[lbl] = "Food"
            elif "seed use" in lower: renames[lbl] = "Seed"
            elif "feed and residual use" in lower: renames[lbl] = "Feed and residual"

        for ci, lbl in enumerate(col_labels):
            display = renames.get(lbl, lbl.replace(" 2/", "").replace(" 3/", "").replace(" 4/", "").strip())
            values = [ri(sd_data[yi][ci]) for yi in range(len(years))]
            rd = {"label": display, "values": values}
            if "total" in display.lower() or "ending" in display.lower(): rd["bold"] = True
            rows_out.append(rd)

        es = next((r for r in rows_out if "ending" in r["label"].lower()), None)
        tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
        if es and tu:
            rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

        sample_rows = rows_out[:5]
        for r in sample_rows:
            print(f"    {r['label']}: ...{r['values'][-3:]}")

        return {"id": "wheat", "label": "Wheat", "years": years,
                "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}]}

    except Exception as e:
        print(f"  S&D error: {e}")
        import traceback; traceback.print_exc()
        return None


# ══════════════════════════════════════════════════════════════
# LIVESTOCK BALANCE SHEETS — ERS Yearbook Data
# ══════════════════════════════════════════════════════════════

# ERS Livestock & Meat Domestic Data (beef, pork)
# ERS Poultry Yearbook (broiler, turkey)
# Multiple URL fallbacks since ERS periodically changes paths
LIVESTOCK_URLS = [
    "https://www.ers.usda.gov/webdocs/DataFiles/51875/MeatSDPFull.xlsx",
    "https://www.ers.usda.gov/webdocs/DataFiles/51875/MeatSDPFullHist.xlsx",
    "https://www.ers.usda.gov/webdocs/DataFiles/51875/MtMeatSDP.xlsx",
]
POULTRY_URLS = [
    "https://www.ers.usda.gov/webdocs/DataFiles/48006/PoultryYearbook.xlsx",
    "https://www.ers.usda.gov/webdocs/DataFiles/48006/PYAll.xlsx",
    "https://www.ers.usda.gov/webdocs/DataFiles/48006/PoultryYearbookFull.xlsx",
]


def parse_livestock_sheet(wb, sheet_names, species_label, min_year=1990):
    """Parse an ERS livestock S&D sheet. Tries sheet_names in order.
    Returns dict with id, label, years, sections or None."""
    import openpyxl
    ws = None
    for name in sheet_names:
        if name in wb.sheetnames:
            ws = wb[name]
            break
        # Case-insensitive search
        for sn in wb.sheetnames:
            if name.lower() in sn.lower():
                ws = wb[sn]
                break
        if ws: break

    if not ws:
        print(f"  {species_label}: sheet not found (tried {sheet_names})")
        print(f"  Available sheets: {wb.sheetnames[:15]}")
        return None

    rows_data = list(ws.iter_rows(values_only=True))
    print(f"  {species_label}: sheet '{ws.title}', {len(rows_data)} rows")

    # Print first few rows for debugging column discovery
    for i in range(min(6, len(rows_data))):
        cells = [str(c)[:25] if c else '' for c in (rows_data[i] or [])]
        print(f"    Row {i}: {cells[:12]}")

    # Discover header row — look for row containing "Production" or "Supply"
    header_row = None
    header_idx = None
    for i in range(min(10, len(rows_data))):
        row = rows_data[i]
        if not row: continue
        row_str = ' '.join(str(c).lower() for c in row if c)
        if 'production' in row_str and ('supply' in row_str or 'stock' in row_str or 'import' in row_str):
            header_row = row
            header_idx = i
            break

    if header_row is None:
        # Alternative: look for a row with multiple relevant keywords
        for i in range(min(15, len(rows_data))):
            row = rows_data[i]
            if not row: continue
            labels = [str(c).strip().lower() for c in row if c]
            matches = sum(1 for l in labels if any(k in l for k in ['begin', 'prod', 'import', 'export', 'stock', 'supply']))
            if matches >= 3:
                header_row = row
                header_idx = i
                break

    # Column mapping — discover by header labels
    col_map = {}
    if header_row:
        for ci, cell in enumerate(header_row):
            if not cell: continue
            label = str(cell).strip().lower()
            if 'begin' in label and 'stock' in label:
                col_map['beginning_stocks'] = ci
            elif 'commercial' in label and 'prod' in label:
                col_map['production'] = ci
            elif ('total' in label and 'prod' in label) or (label == 'production'):
                if 'production' not in col_map:
                    col_map['production'] = ci
            elif 'import' in label:
                col_map['imports'] = ci
            elif 'total' in label and 'supply' in label:
                col_map['total_supply'] = ci
            elif 'export' in label:
                col_map['exports'] = ci
            elif 'end' in label and 'stock' in label:
                col_map['ending_stocks'] = ci
            elif 'total' in label and ('disappear' in label or 'use' in label):
                col_map['total_use'] = ci
            elif 'per capita' in label or 'percapita' in label:
                col_map['per_capita'] = ci
            elif label in ('disappearance', 'total disappearance'):
                col_map['total_use'] = ci

    print(f"  Column map: {col_map}")

    if not col_map or 'production' not in col_map:
        # Fallback: assume standard column order
        # Year | Beg Stocks | Production | Imports | Total Supply | Exports | End Stocks | Total Use | Per Capita
        print(f"  Using fallback column order")
        col_map = {
            'beginning_stocks': 1, 'production': 2, 'imports': 3,
            'total_supply': 4, 'exports': 5, 'ending_stocks': 6,
            'total_use': 7, 'per_capita': 8
        }
        if header_idx is None:
            header_idx = 0

    # Parse data rows
    years = []
    data = {k: [] for k in col_map}
    data_start = (header_idx + 1) if header_idx is not None else 1

    for i in range(data_start, len(rows_data)):
        row = rows_data[i]
        if not row: continue
        year_val = row[0]
        if year_val is None: continue
        # Try to extract year
        try:
            yr = int(float(str(year_val).strip().split('.')[0].split('/')[0]))
        except (ValueError, TypeError):
            continue
        if yr < min_year or yr > 2030: continue

        years.append(yr)
        for key, ci in col_map.items():
            if ci < len(row) and row[ci] is not None:
                try:
                    v = float(row[ci])
                    data[key].append(round(v, 1))
                except (ValueError, TypeError):
                    data[key].append(None)
            else:
                data[key].append(None)

    if not years:
        print(f"  {species_label}: no data rows found")
        return None

    print(f"  {species_label}: {len(years)} years ({years[0]}..{years[-1]})")

    # Build output rows
    label_map = [
        ('beginning_stocks', 'Beginning stocks', False),
        ('production', 'Production', False),
        ('imports', 'Imports', False),
        ('total_supply', 'Total supply', True),
        ('exports', 'Exports', False),
        ('ending_stocks', 'Ending stocks', True),
        ('total_use', 'Total use', True),
        ('per_capita', 'Per capita disappearance (lbs)', False),
    ]

    rows_out = []
    for key, label, bold in label_map:
        if key not in data or all(v is None for v in data[key]):
            continue
        rd = {"label": label, "values": data[key]}
        if bold: rd["bold"] = True
        rows_out.append(rd)

    # Calculate stocks/use if we have the data
    es = data.get('ending_stocks', [])
    tu = data.get('total_use', [])
    if es and tu and len(es) == len(tu):
        su = []
        for i in range(len(es)):
            if es[i] is not None and tu[i] is not None and tu[i] != 0:
                su.append(round(es[i] / tu[i] * 100, 1))
            else:
                su.append(None)
        if not all(v is None for v in su):
            rows_out.append({"label": "Stocks/use (%)", "values": su, "bold": True, "pct": True})

    year_labels = [str(y) for y in years]

    return {
        "id": species_label.lower().replace(" ", "_"),
        "label": species_label,
        "years": year_labels,
        "sections": [{"header": "Supply and disappearance", "unit": "million lbs (carcass weight)", "rows": rows_out}],
    }


def fetch_livestock_data(fetch_url_fn, fetch_fallbacks_fn, existing):
    """Fetch and parse all livestock species. Returns dict of results."""
    import openpyxl
    from io import BytesIO
    results = {}

    # Red meat (beef, pork)
    print("\n-- RED MEAT --")
    data = fetch_fallbacks_fn(LIVESTOCK_URLS) if hasattr(fetch_fallbacks_fn, '__call__') else None
    if not data:
        # Try individual URLs
        for url in LIVESTOCK_URLS:
            data = fetch_url_fn(url)
            if data: break

    if data:
        try:
            wb = openpyxl.load_workbook(BytesIO(data), read_only=True, data_only=True)
            print(f"  Sheets: {wb.sheetnames[:20]}")

            # Beef
            beef = parse_livestock_sheet(wb,
                ["Beef SDP", "BeefSDP", "Beef", "beef", "BfSDP", "Table5"],
                "Beef")
            if beef: results["beef"] = beef

            # Pork
            pork = parse_livestock_sheet(wb,
                ["Pork SDP", "PorkSDP", "Pork", "pork", "PkSDP", "Table20"],
                "Pork")
            if pork: results["pork"] = pork

        except Exception as e:
            print(f"  Red meat parse error: {e}")
    else:
        print("  Red meat: all URLs failed")

    # Poultry (broiler, turkey)
    print("\n-- POULTRY --")
    data = None
    for url in POULTRY_URLS:
        data = fetch_url_fn(url)
        if data: break

    if data:
        try:
            wb = openpyxl.load_workbook(BytesIO(data), read_only=True, data_only=True)
            print(f"  Sheets: {wb.sheetnames[:20]}")

            # Broiler
            broiler = parse_livestock_sheet(wb,
                ["Broiler SDP", "BroilerSDP", "Broiler", "broiler", "BrSDP"],
                "Broiler")
            if broiler: results["broiler"] = broiler

            # Turkey
            turkey = parse_livestock_sheet(wb,
                ["Turkey SDP", "TurkeySDP", "Turkey", "turkey", "TkSDP"],
                "Turkey")
            if turkey: results["turkey"] = turkey

        except Exception as e:
            print(f"  Poultry parse error: {e}")
    else:
        print("  Poultry: all URLs failed")

    # Preserve existing data for any species that failed
    for species in ["beef", "pork", "broiler", "turkey"]:
        if species not in results and species in existing:
            results[species] = existing[species]
            print(f"  Preserved existing {species} data")

    return results


# ══════════════════════════════════════════════════════════════
# TIER 1: Monthly WASDE Report (USDA OCE)
# Released ~noon ET on the 9th-12th of each month
# Contains latest 2-3 MY estimates for all commodities
# ══════════════════════════════════════════════════════════════

import datetime

def build_wasde_report_urls():
    """Generate URL candidates for the current month's WASDE report."""
    now = datetime.datetime.utcnow()
    urls = []
    # Try current month and previous month
    for delta in [0, -1]:
        d = now.replace(day=1) + datetime.timedelta(days=32 * delta)
        mm = f"{d.month:02d}"
        yy = f"{d.year % 100:02d}"
        yyyy = str(d.year)
        # Multiple URL patterns USDA has used
        urls.append(f"https://www.usda.gov/oce/commodity/wasde/wasde{mm}{yy}.xlsx")
        urls.append(f"https://www.usda.gov/sites/default/files/documents/oce-wasde-{yyyy}-{mm}.xlsx")
        urls.append(f"https://usda.library.cornell.edu/apod/wasde{mm}{yy}.xlsx")
    return urls


def parse_wasde_report(wb_data):
    """Parse the monthly WASDE report Excel file.
    Returns dict: {commodity_id: {years: [...], rows: [...]}}
    """
    import openpyxl
    from io import BytesIO
    wb = openpyxl.load_workbook(BytesIO(wb_data), read_only=True, data_only=True)
    
    print(f"  WASDE report sheets: {wb.sheetnames[:20]}")
    
    results = {}
    
    # Map commodity searches to their parsers
    # Each entry: (commodity_id, search_keywords_in_title, row_label_mapping)
    COMMODITY_CONFIGS = {
        "corn": {
            "title_keywords": ["corn", "feed grain"],
            "section_marker": "corn",  # Look for "Corn" section within feed grains table
            "labels": [
                ("Area planted", ["area planted"]),
                ("Area harvested", ["area harvested"]),
                ("Yield per harvested acre", ["yield"]),
                ("Beginning stocks", ["beginning stocks", "beg. stocks"]),
                ("Production", ["production"]),
                ("Imports", ["imports"]),
                ("Total supply", ["supply, total", "total supply"]),
                ("Feed and residual", ["feed and residual"]),
                ("Food, seed & industrial", ["food, seed", "food,seed", "food, seed, and ind"]),
                ("Ethanol", ["ethanol"]),
                ("Seed", ["seed"]),
                ("Total domestic use", ["domestic, total", "total domestic"]),
                ("Exports", ["exports"]),
                ("Total use", ["use, total", "total use"]),
                ("Ending stocks", ["ending stocks"]),
            ],
            "bold_rows": ["Total supply", "Total domestic use", "Total use", "Ending stocks"],
            "indent_rows": ["Ethanol", "Seed"],
        },
        "soybeans": {
            "title_keywords": ["soybean"],
            "section_marker": None,
            "labels": [
                ("Area planted", ["area planted"]),
                ("Area harvested", ["area harvested"]),
                ("Yield per harvested acre", ["yield"]),
                ("Beginning stocks", ["beginning stocks", "beg. stocks"]),
                ("Production", ["production"]),
                ("Imports", ["imports"]),
                ("Total supply", ["supply, total", "total supply"]),
                ("Crush", ["crushings", "crush"]),
                ("Exports", ["exports"]),
                ("Seed", ["seed"]),
                ("Residual", ["residual"]),
                ("Total use", ["use, total", "total use", "total disappearance"]),
                ("Ending stocks", ["ending stocks"]),
            ],
            "bold_rows": ["Total supply", "Total use", "Ending stocks"],
            "indent_rows": [],
        },
        "wheat": {
            "title_keywords": ["wheat"],
            "section_marker": "all wheat",
            "labels": [
                ("Area planted", ["area planted"]),
                ("Area harvested", ["area harvested"]),
                ("Yield per harvested acre", ["yield"]),
                ("Beginning stocks", ["beginning stocks", "beg. stocks"]),
                ("Production", ["production"]),
                ("Imports", ["imports"]),
                ("Total supply", ["supply, total", "total supply"]),
                ("Food", ["food"]),
                ("Seed", ["seed"]),
                ("Feed and residual", ["feed and residual"]),
                ("Total domestic use", ["domestic, total", "total domestic"]),
                ("Exports", ["exports"]),
                ("Total use", ["use, total", "total use"]),
                ("Ending stocks", ["ending stocks"]),
            ],
            "bold_rows": ["Total supply", "Total domestic use", "Total use", "Ending stocks"],
            "indent_rows": [],
        },
        "beef": {
            "title_keywords": ["beef"],
            "section_marker": None,
            "labels": [
                ("Beginning stocks", ["beginning", "beg."]),
                ("Production", ["production", "total production", "commercial prod"]),
                ("Imports", ["imports"]),
                ("Total supply", ["supply, total", "total supply"]),
                ("Exports", ["exports"]),
                ("Ending stocks", ["ending"]),
                ("Total use", ["use, total", "total use", "total disappearance"]),
                ("Per capita disappearance (lbs)", ["per capita"]),
            ],
            "bold_rows": ["Total supply", "Total use", "Ending stocks"],
            "indent_rows": [],
        },
        "pork": {
            "title_keywords": ["pork"],
            "section_marker": None,
            "labels": [
                ("Beginning stocks", ["beginning", "beg."]),
                ("Production", ["production", "total production", "commercial prod"]),
                ("Imports", ["imports"]),
                ("Total supply", ["supply, total", "total supply"]),
                ("Exports", ["exports"]),
                ("Ending stocks", ["ending"]),
                ("Total use", ["use, total", "total use", "total disappearance"]),
                ("Per capita disappearance (lbs)", ["per capita"]),
            ],
            "bold_rows": ["Total supply", "Total use", "Ending stocks"],
            "indent_rows": [],
        },
        "broiler": {
            "title_keywords": ["broiler"],
            "section_marker": None,
            "labels": [
                ("Beginning stocks", ["beginning", "beg."]),
                ("Production", ["production"]),
                ("Imports", ["imports"]),
                ("Total supply", ["supply, total", "total supply"]),
                ("Exports", ["exports"]),
                ("Ending stocks", ["ending"]),
                ("Total use", ["use, total", "total use", "total disappearance"]),
                ("Per capita disappearance (lbs)", ["per capita"]),
            ],
            "bold_rows": ["Total supply", "Total use", "Ending stocks"],
            "indent_rows": [],
        },
        "turkey": {
            "title_keywords": ["turkey"],
            "section_marker": None,
            "labels": [
                ("Beginning stocks", ["beginning", "beg."]),
                ("Production", ["production"]),
                ("Imports", ["imports"]),
                ("Total supply", ["supply, total", "total supply"]),
                ("Exports", ["exports"]),
                ("Ending stocks", ["ending"]),
                ("Total use", ["use, total", "total use", "total disappearance"]),
                ("Per capita disappearance (lbs)", ["per capita"]),
            ],
            "bold_rows": ["Total supply", "Total use", "Ending stocks"],
            "indent_rows": [],
        },
    }
    
    for comm_id, config in COMMODITY_CONFIGS.items():
        parsed = _parse_wasde_commodity(wb, config, comm_id)
        if parsed:
            results[comm_id] = parsed
    
    return results


def _find_wasde_sheet(wb, keywords):
    """Find a worksheet whose content matches the given keywords."""
    for ws in wb.worksheets:
        # Check first 15 rows for keyword matches
        try:
            rows = []
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i >= 15: break
                rows.append(row)
            
            text = ' '.join(str(c).lower() for row in rows for c in row if c)
            if all(kw.lower() in text for kw in keywords):
                return ws, rows
        except:
            continue
    return None, None


def _parse_wasde_commodity(wb, config, comm_id):
    """Parse a single commodity from the WASDE report."""
    ws, preview_rows = _find_wasde_sheet(wb, config["title_keywords"])
    if not ws:
        print(f"  {comm_id}: sheet not found")
        return None
    
    print(f"  {comm_id}: found sheet '{ws.title}'")
    
    # Read all rows
    all_rows = list(ws.iter_rows(values_only=True))
    
    # Find the header row with marketing year labels (e.g., "2024/25", "2025/26")
    header_row_idx = None
    year_cols = {}  # {col_index: year_label}
    
    for i, row in enumerate(all_rows):
        if not row: continue
        for ci, cell in enumerate(row):
            if cell is None: continue
            s = str(cell).strip()
            # Look for marketing year patterns: "2024/25" or "2024-25" or "2024/2025"
            if '/' in s and len(s) >= 5:
                try:
                    parts = s.replace(" ", "").split('/')
                    yr = int(parts[0][:4])
                    if 1990 <= yr <= 2030:
                        year_cols[ci] = s.split('\n')[0].strip()  # Remove any Est./Proj. suffix from newlines
                except (ValueError, IndexError):
                    pass
        if len(year_cols) >= 2:
            header_row_idx = i
            break
    
    if header_row_idx is None or not year_cols:
        print(f"  {comm_id}: no year headers found")
        # Debug: print first 10 rows
        for i in range(min(10, len(all_rows))):
            cells = [str(c)[:30] if c else '' for c in (all_rows[i] or [])]
            print(f"    Row {i}: {cells[:8]}")
        return None
    
    # Clean year labels - extract just the MY part
    clean_years = {}
    for ci, raw in sorted(year_cols.items()):
        # Extract "YYYY/YY" from strings like "2024/25 Est." or "2025/26\nApr"
        parts = raw.replace('\n', ' ').split()
        my = parts[0] if parts else raw
        # Normalize: "2024/25" stays, "2024/2025" -> "2024/25"
        if len(my) > 7 and '/' in my:
            yr1 = my.split('/')[0]
            yr2 = my.split('/')[1][-2:]
            my = f"{yr1}/{yr2}"
        clean_years[ci] = my
    
    sorted_cols = sorted(clean_years.keys())
    years = [clean_years[ci] for ci in sorted_cols]
    print(f"  {comm_id}: years = {years} (cols {sorted_cols})")
    
    # Parse data rows after the header
    rows_out = []
    in_section = config["section_marker"] is None  # If no section marker, parse everything
    
    for i in range(header_row_idx + 1, len(all_rows)):
        row = all_rows[i]
        if not row: continue
        
        # Get the row label (usually column 0 or 1)
        label = None
        for ci in range(min(3, len(row))):
            if row[ci] is not None:
                label = str(row[ci]).strip()
                if label and len(label) > 1:
                    break
        if not label: continue
        
        label_lower = label.lower().replace('\n', ' ')
        
        # Section detection for multi-commodity sheets (e.g., feed grains has corn + sorghum)
        if config["section_marker"] and not in_section:
            if config["section_marker"].lower() in label_lower:
                in_section = True
            continue
        
        # Stop at next section header or blank region
        if in_section and config["section_marker"]:
            # Check if we've hit a new section (e.g., "Sorghum" after "Corn")
            if label_lower and not any(kw in label_lower for pair in config["labels"] for kw in pair[1]):
                # Could be a section break - check if it looks like a header
                if all(row[ci] is None for ci in sorted_cols if ci < len(row)):
                    if any(c and str(c).strip() for c in row[:3]):
                        # Non-data row with no values in year columns - might be new section
                        pass  # Continue looking
        
        # Try to match this row to one of our target labels
        for out_label, search_terms in config["labels"]:
            if any(term in label_lower for term in search_terms):
                # Extract values from year columns
                values = []
                for ci in sorted_cols:
                    if ci < len(row) and row[ci] is not None:
                        try:
                            v = float(str(row[ci]).replace(',', '').strip())
                            values.append(round(v, 1))
                        except (ValueError, TypeError):
                            values.append(None)
                    else:
                        values.append(None)
                
                if any(v is not None for v in values):
                    rd = {"label": out_label, "values": values}
                    if out_label in config.get("bold_rows", []):
                        rd["bold"] = True
                    if out_label in config.get("indent_rows", []):
                        rd["indent"] = True
                    # Avoid duplicates
                    if not any(r["label"] == out_label for r in rows_out):
                        rows_out.append(rd)
                break
    
    if not rows_out:
        print(f"  {comm_id}: no data rows matched")
        return None
    
    # Add stocks/use ratio
    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] in ("Total use",)), None)
    if es and tu:
        su = []
        for i in range(len(years)):
            e = es["values"][i] if i < len(es["values"]) else None
            t = tu["values"][i] if i < len(tu["values"]) else None
            if e is not None and t is not None and t != 0:
                su.append(round(e / t * 100, 1))
            else:
                su.append(None)
        rows_out.append({"label": "Stocks/use (%)", "values": su, "bold": True, "pct": True})
    
    print(f"  {comm_id}: {len(rows_out)} rows, {len(years)} years")
    for r in rows_out:
        print(f"    {r['label']}: {r['values']}")
    
    # Determine unit
    is_livestock = comm_id in ("beef", "pork", "broiler", "turkey")
    unit = "million lbs" if is_livestock else "million bushels / million acres"
    
    return {
        "years": years,
        "rows": rows_out,
        "unit": unit,
    }


def merge_wasde_into_existing(existing_commodity, wasde_data, comm_id):
    """Merge WASDE report data (2-3 years) into existing yearbook data (full history).
    WASDE data overwrites matching years; non-matching years preserved."""
    if not existing_commodity or not wasde_data:
        return existing_commodity
    
    ex_years = existing_commodity.get("years", [])
    ex_sections = existing_commodity.get("sections", [])
    if not ex_years or not ex_sections:
        return existing_commodity
    
    wasde_years = wasde_data["years"]
    wasde_rows = wasde_data["rows"]
    
    # Build a map of label -> wasde row data
    wasde_map = {}
    for wr in wasde_rows:
        wasde_map[wr["label"]] = wr
    
    # For each year in WASDE data, find or append it in existing
    for wi, wy in enumerate(wasde_years):
        if wy in ex_years:
            # Overwrite existing values
            yi = ex_years.index(wy)
            for section in ex_sections:
                for row in section.get("rows", []):
                    if row["label"] in wasde_map:
                        wr = wasde_map[row["label"]]
                        if wi < len(wr["values"]) and wr["values"][wi] is not None:
                            while len(row["values"]) <= yi:
                                row["values"].append(None)
                            row["values"][yi] = wr["values"][wi]
        else:
            # Append new year
            ex_years.append(wy)
            yi = len(ex_years) - 1
            for section in ex_sections:
                for row in section.get("rows", []):
                    if row["label"] in wasde_map:
                        wr = wasde_map[row["label"]]
                        val = wr["values"][wi] if wi < len(wr["values"]) else None
                    else:
                        val = None
                    while len(row["values"]) < yi:
                        row["values"].append(None)
                    row["values"].append(val)
    
    existing_commodity["years"] = ex_years
    print(f"  {comm_id}: merged WASDE data, now {len(ex_years)} years")
    return existing_commodity


def main():
    from datetime import datetime
    import openpyxl
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    # Load existing data
    existing = {}
    if os.path.exists(output_file):
        try:
            with open(output_file) as f:
                existing = json.load(f)
            print(f"Loaded existing: us={list(existing.get('us', {}).keys())}")
        except: pass

    print("=" * 60)
    print("WASDE Data Fetch — Two-Tier Architecture")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)

    result = {"fetched_at": datetime.utcnow().isoformat() + "Z", "us": {}}
    
    # Start with existing data as base
    if "us" in existing:
        result["us"] = existing["us"].copy()
    
    # Preserve world data if present
    if "world" in existing:
        result["world"] = existing["world"]
    if "world_fetched_at" in existing:
        result["world_fetched_at"] = existing["world_fetched_at"]

    # ══════════════════════════════════════════════════════════
    # TIER 1: Monthly WASDE Report (primary, time-sensitive)
    # ══════════════════════════════════════════════════════════
    print("\n" + "═" * 60)
    print("TIER 1: Monthly WASDE Report")
    print("═" * 60)
    
    wasde_urls = build_wasde_report_urls()
    wasde_data = None
    wasde_source = None
    
    for url in wasde_urls:
        data = fetch_url(url)
        if data:
            wasde_data = data
            wasde_source = url
            break
    
    if wasde_data:
        print(f"\n  WASDE report downloaded: {len(wasde_data):,} bytes")
        print(f"  Source: {wasde_source}")
        try:
            wasde_parsed = parse_wasde_report(wasde_data)
            print(f"  Parsed {len(wasde_parsed)} commodities from WASDE report")
            
            for comm_id, wdata in wasde_parsed.items():
                if comm_id in result["us"]:
                    # Merge WASDE data into existing yearbook data
                    result["us"][comm_id] = merge_wasde_into_existing(
                        result["us"][comm_id], wdata, comm_id)
                else:
                    # No existing data — create new entry from WASDE alone
                    is_livestock = comm_id in ("beef", "pork", "broiler", "turkey")
                    label_map = {
                        "corn": "Corn", "soybeans": "Soybeans", "wheat": "Wheat",
                        "soybean_meal": "Soybean Meal", "soybean_oil": "Soybean Oil",
                        "beef": "Beef", "pork": "Pork", "broiler": "Broiler", "turkey": "Turkey",
                    }
                    result["us"][comm_id] = {
                        "id": comm_id,
                        "label": label_map.get(comm_id, comm_id.title()),
                        "years": wdata["years"],
                        "sections": [{"header": "Supply and disappearance",
                                      "unit": wdata["unit"],
                                      "rows": wdata["rows"]}],
                    }
                    print(f"  {comm_id}: created new entry ({len(wdata['years'])} years)")
            
            result["wasde_report_source"] = wasde_source
            result["wasde_report_fetched_at"] = datetime.utcnow().isoformat() + "Z"
        except Exception as e:
            print(f"  WASDE report parse error: {e}")
            import traceback; traceback.print_exc()
    else:
        print("  WASDE report: not available (all URLs failed)")
        print("  This is normal if the report hasn't been released yet today.")

    # ══════════════════════════════════════════════════════════
    # TIER 2: ERS Yearbook Data (historical back-series)
    # ══════════════════════════════════════════════════════════
    print("\n" + "═" * 60)
    print("TIER 2: ERS Yearbook Data (historical)")
    print("═" * 60)
    
    print("\n-- CORN --")
    data = fetch_url(CORN_URL)
    if data:
        r = parse_corn(data)
        if r:
            if "corn" in result["us"] and len(result["us"]["corn"].get("years", [])) > len(r["years"]):
                # Existing data (with WASDE overlay) has more years — merge yearbook as base
                _merge_yearbook_base(result["us"]["corn"], r)
            else:
                result["us"]["corn"] = r

    print("\n-- OIL CROPS --")
    data = fetch_with_fallbacks(OILCROPS_URLS)
    if data:
        try:
            wb = None
            try:
                wb = openpyxl.load_workbook(BytesIO(data), read_only=True, data_only=True)
                print(f"  Opened as xlsx, sheets: {wb.sheetnames[:10]}")
            except Exception:
                try:
                    zf = zipfile.ZipFile(BytesIO(data))
                    if "Soy.xlsx" in zf.namelist():
                        wb = openpyxl.load_workbook(BytesIO(zf.read("Soy.xlsx")), read_only=True, data_only=True)
                        print(f"  Opened Soy.xlsx from zip, sheets: {wb.sheetnames[:10]}")
                except Exception as e2:
                    print(f"  Could not open as xlsx or zip: {e2}")

            if wb:
                for fn, parser in [("soybeans", parse_soybeans), ("soybean_meal", parse_soymeal), ("soybean_oil", parse_soyoil)]:
                    r = parser(wb)
                    if r:
                        if fn in result["us"] and len(result["us"][fn].get("years", [])) > len(r["years"]):
                            _merge_yearbook_base(result["us"][fn], r)
                        else:
                            result["us"][fn] = r
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print("  All URLs failed — preserving existing soy data")

    print("\n-- WHEAT --")
    data = fetch_url(WHEAT_URL)
    if data:
        r = parse_wheat(data)
        if r:
            if "wheat" in result["us"] and len(result["us"]["wheat"].get("years", [])) > len(r["years"]):
                _merge_yearbook_base(result["us"]["wheat"], r)
            else:
                result["us"]["wheat"] = r

    # ── LIVESTOCK (ERS yearbooks as fallback) ──
    print("\n-- LIVESTOCK (ERS yearbooks) --")
    existing_livestock = {}
    for sp in ["beef", "pork", "broiler", "turkey"]:
        if sp in existing.get("us", {}):
            existing_livestock[sp] = existing["us"][sp]
    try:
        livestock_results = fetch_livestock_data(fetch_url, fetch_with_fallbacks, existing_livestock)
        for sp, ldata in livestock_results.items():
            if sp in result["us"] and len(result["us"][sp].get("years", [])) > len(ldata.get("years", [])):
                _merge_yearbook_base(result["us"][sp], ldata)
            else:
                result["us"][sp] = ldata
            print(f"  {sp}: {len(result['us'].get(sp, {}).get('years', []))} years")
    except Exception as e:
        print(f"  Livestock error: {e}")

    # Preserve any commodities that failed entirely
    for cid in ["corn", "soybeans", "soybean_meal", "soybean_oil", "wheat", "beef", "pork", "broiler", "turkey"]:
        if cid not in result["us"] and cid in existing.get("us", {}):
            result["us"][cid] = existing["us"][cid]
            print(f"  Preserved existing {cid} data")

    # ══════════════════════════════════════════════════════════
    # RESULTS
    # ══════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print(f"RESULTS: {len(result['us'])} commodities")
    for cid, d in result["us"].items():
        yrs = d.get("years", [])
        total = sum(len(s.get("rows", [])) for s in d.get("sections", []))
        print(f"  {cid}: {len(yrs)} years ({yrs[0] if yrs else '?'}..{yrs[-1] if yrs else '?'}), {total} rows")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")
    return 0


def _merge_yearbook_base(existing_entry, yearbook_entry):
    """Merge yearbook historical data as the base for an existing entry.
    Yearbook provides years that don't exist in existing; existing data takes precedence."""
    if not yearbook_entry or not existing_entry:
        return
    
    ex_years = existing_entry.get("years", [])
    yb_years = yearbook_entry.get("years", [])
    
    # Find yearbook years not in existing
    new_years = [y for y in yb_years if y not in ex_years]
    if not new_years:
        return
    
    # Build label -> values map from yearbook
    yb_rows_map = {}
    for section in yearbook_entry.get("sections", []):
        for row in section.get("rows", []):
            yb_rows_map[row["label"]] = {yb_years[i]: row["values"][i] 
                                          for i in range(min(len(yb_years), len(row["values"])))}
    
    # Prepend new years to existing
    combined_years = [y for y in yb_years if y not in ex_years] + ex_years
    combined_years_sorted = sorted(combined_years, key=lambda y: y.split('/')[0] if '/' in y else y)
    
    for section in existing_entry.get("sections", []):
        for row in section.get("rows", []):
            old_vals = {ex_years[i]: row["values"][i] for i in range(min(len(ex_years), len(row["values"])))}
            yb_vals = yb_rows_map.get(row["label"], {})
            # Build combined values: yearbook for old years, existing for recent
            new_vals = []
            for y in combined_years_sorted:
                if y in old_vals and old_vals[y] is not None:
                    new_vals.append(old_vals[y])
                elif y in yb_vals:
                    new_vals.append(yb_vals[y])
                else:
                    new_vals.append(None)
            row["values"] = new_vals
    
    existing_entry["years"] = combined_years_sorted


if __name__ == "__main__":
    sys.exit(main())
