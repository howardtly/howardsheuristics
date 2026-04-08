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


def fetch_url(url, timeout=60, retries=3, delay=30):
    for attempt in range(1, retries + 1):
        print(f"  Attempt {attempt}/{retries}: {url[:90]}...")
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
                print(f"  OK: {len(data):,} bytes")
                return data
        except Exception as e:
            print(f"  FAILED: {e}")
            if attempt < retries:
                wait = delay * attempt
                print(f"  Retrying in {wait}s...")
                time.sleep(wait)
    print(f"  All {retries} attempts failed for {url[:90]}")
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
# PSD WORLD DATA
# ══════════════════════════════════════════════════════════════

def psd_my_label(year_int):
    return f"{year_int}/{str(year_int + 1)[-2:]}"

"""
PSD World Data Fetcher - adds world/foreign balance sheets to wasde.json
Fetches from USDA FAS PSD API for corn, soybeans, soybean meal, soybean oil, wheat.
"""

PSD_API_KEY = os.environ.get("PSD_API_KEY", "9B50B342-EA13-4269-BFC8-77E9E9903161")
PSD_BASE = "https://apps.fas.usda.gov/PSDOnlineDataServices/api/CommodityData/GetCommodityDataByYear"
HEADERS = {"API_KEY": PSD_API_KEY, "User-Agent": "HowardsHeuristics/1.0", "Accept": "application/json"}

# Commodity codes
PSD_COMMODITIES = {
    "corn":         {"code": "0440000", "label": "Corn"},
    "soybeans":     {"code": "2222000", "label": "Soybeans"},
    "soybean_meal": {"code": "0813100", "label": "Soybean Meal"},
    "soybean_oil":  {"code": "4232000", "label": "Soybean Oil"},
    "wheat":        {"code": "0410000", "label": "Wheat"},
}

# Key countries to extract per commodity
KEY_COUNTRIES = {
    "corn":         ["United States", "China", "Brazil", "European Union", "Argentina", "Mexico", "Ukraine", "India"],
    "soybeans":     ["United States", "Brazil", "Argentina", "China", "European Union", "Paraguay", "India"],
    "soybean_meal": ["United States", "Brazil", "Argentina", "China", "European Union", "India"],
    "soybean_oil":  ["United States", "Brazil", "Argentina", "China", "European Union", "India", "Indonesia"],
    "wheat":        ["United States", "China", "European Union", "Russia", "India", "Australia", "Canada", "Ukraine", "Argentina"],
}

# Attributes we want (PSD attribute descriptions -> our labels)
# We'll discover exact IDs from data, matching by description keywords
ATTR_MAP = {
    "Area Harvested":        {"label": "Area harvested", "bold": False},
    "Beginning Stocks":      {"label": "Beginning stocks", "bold": False},
    "Production":            {"label": "Production", "bold": False},
    "MY Imports":            {"label": "Imports", "bold": False},
    "Total Supply":          {"label": "Total supply", "bold": True},
    "Feed Dom. Consumption": {"label": "Feed domestic use", "bold": False},
    "FSI Consumption":       {"label": "Food, seed, industrial", "bold": False},
    "Total Dom. Consumption":{"label": "Domestic consumption", "bold": True},
    "MY Exports":            {"label": "Exports", "bold": False},
    "Total Use":             {"label": "Total use", "bold": True},
    "Ending Stocks":         {"label": "Ending stocks", "bold": True},
    "TY Imports":            {"label": "Imports", "bold": False},
    "TY Exports":            {"label": "Exports", "bold": False},
    "Crush":                 {"label": "Crush", "bold": False},
    "Extr. Rate, 999.9999":  {"label": "Extraction rate", "bold": False},
    "Dom. Cons., Use":       {"label": "Domestic consumption", "bold": True},
}

def fetch_psd_year(commodity_code, market_year, retries=3, delay=10):
    """Fetch PSD data for one commodity and one marketing year."""
    url = f"{PSD_BASE}?commodityCode={commodity_code}&marketYear={market_year}"
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data
        except Exception as e:
            if attempt < retries:
                time.sleep(delay * attempt)
            else:
                print(f"    PSD fetch failed for {commodity_code}/{market_year}: {e}")
    return None


def parse_psd_commodity(commodity_id, commodity_info, year_range):
    """Fetch and parse PSD data for one commodity across all years."""
    code = commodity_info["code"]
    label = commodity_info["label"]
    key_countries = KEY_COUNTRIES.get(commodity_id, [])
    
    print(f"\n  PSD: {label} ({code})")
    
    # Collect all data: {year: {country: {attr_desc: value}}}
    all_data = {}
    for yr in year_range:
        records = fetch_psd_year(code, yr)
        if not records:
            continue
        year_data = {}
        for rec in records:
            country = rec.get("countryDescription", "Unknown")
            attr = rec.get("attributeDescription", "")
            val = rec.get("value")
            if country not in year_data:
                year_data[country] = {}
            year_data[country][attr] = val
        all_data[yr] = year_data
        # Small delay to be polite to the API
        time.sleep(0.3)
    
    if not all_data:
        print(f"    No PSD data retrieved")
        return None
    
    years_with_data = sorted(all_data.keys())
    years = [psd_my_label(y) for y in years_with_data]
    print(f"    Years: {years[0]} to {years[-1]} ({len(years)} years)")
    
    # Discover available attributes from first year with data
    sample_year = years_with_data[-1]
    sample_countries = all_data[sample_year]
    # Get attributes from "World" or first available country
    sample_attrs = set()
    for country_data in sample_countries.values():
        sample_attrs.update(country_data.keys())
    print(f"    Available attributes: {sorted(sample_attrs)[:15]}...")
    
    # Build world total rows
    # PSD has a "World" country entry for most commodities
    world_rows = []
    # Define which attributes to show for world total
    world_attrs_order = [
        "Area Harvested", "Beginning Stocks", "Production", 
        "MY Imports", "TY Imports",
        "Total Supply",
        "Feed Dom. Consumption", "FSI Consumption", "Crush",
        "Total Dom. Consumption", "Dom. Cons., Use",
        "MY Exports", "TY Exports",
        "Total Use",
        "Ending Stocks"
    ]
    
    for attr_name in world_attrs_order:
        if attr_name not in sample_attrs:
            continue
        info = ATTR_MAP.get(attr_name, {"label": attr_name, "bold": False})
        values = []
        for yr in years_with_data:
            world_data = all_data[yr].get("World", {})
            v = world_data.get(attr_name)
            # PSD values in 1000 MT/HA; convert to million MT/HA for display
            values.append(r1(v / 1000) if v is not None else None)
        # Skip if all None
        if all(v is None for v in values):
            continue
        row = {"label": info["label"], "values": values}
        if info["bold"]:
            row["bold"] = True
        world_rows.append(row)
    
    # Add stocks/use ratio
    es_row = next((r for r in world_rows if r["label"] == "Ending stocks"), None)
    tu_row = next((r for r in world_rows if r["label"] in ("Total use", "Domestic consumption")), None)
    if es_row and tu_row:
        world_rows.append({
            "label": "Stocks/use (%)",
            "values": [pct(es_row["values"][i], tu_row["values"][i]) for i in range(len(years))],
            "bold": True, "pct": True
        })
    
    print(f"    World rows: {len(world_rows)}")
    
    # Build country data
    countries = []
    for country_name in key_countries:
        country_rows = []
        # Country-level attributes
        country_attrs = [
            "Area Harvested", "Beginning Stocks", "Production",
            "MY Imports", "TY Imports",
            "Total Supply",
            "Feed Dom. Consumption", "FSI Consumption", "Crush",
            "Total Dom. Consumption", "Dom. Cons., Use",
            "MY Exports", "TY Exports",
            "Ending Stocks"
        ]
        for attr_name in country_attrs:
            if attr_name not in sample_attrs:
                continue
            info = ATTR_MAP.get(attr_name, {"label": attr_name, "bold": False})
            values = []
            for yr in years_with_data:
                cd = all_data[yr].get(country_name, {})
                v = cd.get(attr_name)
                values.append(r1(v / 1000) if v is not None else None)
            if all(v is None for v in values):
                continue
            row = {"label": info["label"], "values": values}
            if info["bold"]:
                row["bold"] = True
            country_rows.append(row)
        
        if country_rows:
            countries.append({"label": country_name, "rows": country_rows})
    
    print(f"    Countries: {len(countries)}")
    
    # Determine unit based on commodity
    unit_map = {
        "corn": "million metric tons / million hectares",
        "soybeans": "million metric tons / million hectares", 
        "soybean_meal": "million metric tons",
        "soybean_oil": "million metric tons",
        "wheat": "million metric tons / million hectares",
    }
    
    return {
        "id": commodity_id,
        "label": label,
        "years": years,
        "sections": [{"header": "World total", "unit": unit_map.get(commodity_id, "1,000 metric tons"), "rows": world_rows}],
        "countries": countries,
    }


def fetch_psd_world_data():
    """Fetch world data for all commodities from PSD API."""
    import datetime
    # Marketing year range: last 25 years
    current_year = datetime.datetime.now().year
    # PSD uses start year of MY (2024 = 2024/25)
    end_year = current_year  # current MY
    start_year = end_year - 24  # 25 years of data
    year_range = list(range(start_year, end_year + 1))
    
    print(f"\nFetching PSD world data: {psd_my_label(start_year)} to {psd_my_label(end_year)}")
    
    world = {}
    for cid, cinfo in PSD_COMMODITIES.items():
        result = parse_psd_commodity(cid, cinfo, year_range)
        if result:
            world[cid] = result
    
    return world


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    # Try to load existing data to preserve commodities that fail to fetch
    existing = {}
    if os.path.exists(output_file):
        try:
            with open(output_file) as f:
                old = json.load(f)
            if old.get("us"):
                existing = old["us"]
                print(f"Loaded existing data: {list(existing.keys())}")
        except: pass

    print("=" * 60)
    print("WASDE Data Fetch v11")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)

    result = {"fetched_at": datetime.utcnow().isoformat() + "Z", "us": {}}

    print("\n-- CORN --")
    data = fetch_url(CORN_URL)
    if data:
        r = parse_corn(data)
        if r: result["us"]["corn"] = r

    print("\n-- OIL CROPS --")
    data = fetch_with_fallbacks(OILCROPS_URLS)
    if data:
        try:
            import openpyxl
            wb = None
            # Try opening as xlsx directly first
            try:
                wb = openpyxl.load_workbook(BytesIO(data), read_only=True, data_only=True)
                print(f"  Opened as xlsx, sheets: {wb.sheetnames[:10]}")
            except Exception:
                # Try as zip (old format)
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
                    if r: result["us"][fn] = r
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print("  All URLs failed — preserving existing soy data")

    print("\n-- WHEAT --")
    data = fetch_url(WHEAT_URL)
    if data:
        r = parse_wheat(data)
        if r: result["us"]["wheat"] = r

    # Preserve any commodities that failed to fetch this time
    for cid in ["corn", "soybeans", "soybean_meal", "soybean_oil", "wheat"]:
        if cid not in result["us"] and cid in existing:
            result["us"][cid] = existing[cid]
            print(f"  Preserved existing {cid} data")

    print(f"\n{'='*60}")
    print(f"RESULTS: {len(result['us'])} / 5")
    for cid, d in result["us"].items():
        total = sum(len(s["rows"]) for s in d["sections"])
        print(f"  {cid}: {len(d['years'])} years, {total} rows")
        for s in d["sections"]:
            for r in s["rows"][:5]:
                print(f"    {r['label']}: ...{r['values'][-3:]}")

    # ── PSD World Data ──
    print("\n── PSD WORLD DATA ──")
    try:
        world_data = fetch_psd_world_data()
        if world_data:
            result["world"] = world_data
            print(f"  World data: {len(world_data)} commodities")
        else:
            print("  No world data — preserving existing")
            if existing.get("world"):
                result["world"] = existing["world"]
    except Exception as e:
        print(f"  PSD world error: {e}")
        if existing.get("world"):
            result["world"] = existing["world"]
            print("  Preserved existing world data")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")
    return 0

if __name__ == "__main__":
    sys.exit(main())
