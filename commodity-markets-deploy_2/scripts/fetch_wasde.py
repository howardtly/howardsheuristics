#!/usr/bin/env python3
"""
WASDE Data Fetch v11
- Wheat Table06: col0=MY, col1=Type ("All wheat"), col2+=S&D data
- Oil crops: tries current URL, falls back to cached data
"""

import json, os, sys, urllib.request, urllib.error, zipfile
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


def fetch_url(url, timeout=60):
    print(f"  Trying: {url[:90]}...")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            print(f"  OK: {len(data):,} bytes")
            return data
    except Exception as e:
        print(f"  FAILED: {e}")
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

    years = sd_years
    rows_out = [
        {"label": "Area planted", "values": [r1(area_planted.get(y)) for y in years]},
        {"label": "Area harvested", "values": [r1(area_harvested.get(y)) for y in years]},
        {"label": "Yield per harvested acre", "values": [r1(yield_per_acre.get(y)) for y in years]},
    ]

    sd_map = [
        ("Beginning stocks", "Beginning stocks", True),
        ("Production", "Production", False),
        ("Imports", "Imports", False),
        ("Total supply", "Total supply", True),
        ("Food, alcohol, and industrial", "Food, alcohol, and industrial use", False),
        ("Seed use", "Seed use", False),
        ("Feed and residual", "Feed and residual use", False),
        ("Total domestic", "Total domestic use", True),
        ("Exports", "Exports", False),
        ("Total use", "Total usage", True),
        ("Ending stocks", "Ending stocks", True),
    ]
    for prefix, display, bold in sd_map:
        key = next((k for k in col_labels if k.lower().startswith(prefix.lower())), None)
        values = [ri(sd_data[yi].get(key)) if key else None for yi in range(len(years))]
        rd = {"label": display, "values": values}
        if bold: rd["bold"] = True
        if display == "Beginning stocks": rd["spaceBefore"] = True
        rows_out.append(rd)

    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

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
    for ci, label in enumerate(sd_labels):
        rd = {"label": label, "values": [ri(sd[yi][ci]) for yi in range(len(years))]}
        if "total" in label.lower() or "ending" in label.lower(): rd["bold"] = True
        if label == "Beginning stocks": rd["spaceBefore"] = True
        rows_out.append(rd)

    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

    return {"id": "soybeans", "label": "Soybeans", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}]}


def parse_soymeal(wb):
    ws = find_sheet(wb, "tab4", "Table04", "Table 04", "tab04")
    if not ws:
        print("  Soy meal sheet not found")
        return None
    rows = list(ws.iter_rows(values_only=True))
    labels = ["Beginning stocks", "Production", "Imports", "Total supply", "Domestic use", "Exports", "Total disappearance", "Ending stocks", "Price ($/short ton)"]
    years, sd = [], []
    for i in range(7, len(rows)):
        row = rows[i]
        if not row: continue
        my = str(row[0]).strip() if row[0] else ""
        if "/" not in my or len(my) < 6: continue
        try: int(my[:4])
        except ValueError: continue
        years.append(my)
        sd.append([to_float(row[1 + c]) for c in range(len(labels))])

    renames = {"Total disappearance": "Total usage"}
    rows_out = []
    for ci, label in enumerate(labels):
        display = renames.get(label, label)
        is_price = "price" in label.lower()
        rd = {"label": display, "values": [sd[yi][ci] if is_price else ri(sd[yi][ci]) for yi in range(len(years))]}
        if "total" in display.lower() or "ending" in display.lower(): rd["bold"] = True
        if is_price: rd["price"] = True
        rows_out.append(rd)

    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

    return {"id": "soybean_meal", "label": "Soybean Meal", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "1,000 short tons", "rows": rows_out}]}


def parse_soyoil(wb):
    ws = find_sheet(wb, "tab5", "Table05", "Table 05", "tab05")
    if not ws:
        print("  Soy oil sheet not found")
        return None
    rows = list(ws.iter_rows(values_only=True))
    labels = ["Beginning stocks", "Production", "Imports", "Total supply", "Domestic total", "Biofuel", "Exports", "Total disappearance", "Ending stocks"]
    years, sd = [], []
    for i in range(6, len(rows)):
        row = rows[i]
        if not row: continue
        my = str(row[0]).strip() if row[0] else ""
        if "/" not in my or len(my) < 6: continue
        try: int(my[:4])
        except ValueError: continue
        years.append(my)
        sd.append([to_float(row[1 + c]) for c in range(len(labels))])

    renames = {"Total disappearance": "Total usage"}
    rows_out = []
    for ci, label in enumerate(labels):
        display = renames.get(label, label)
        rd = {"label": display, "values": [ri(sd[yi][ci]) for yi in range(len(years))]}
        if "total" in display.lower() or "ending" in display.lower(): rd["bold"] = True
        rows_out.append(rd)

    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

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

        for ci, lbl in enumerate(col_labels):
            display = renames.get(lbl, lbl.replace(" 2/", "").replace(" 3/", "").replace(" 4/", "").strip())
            values = [ri(sd_data[yi][ci]) for yi in range(len(years))]
            rd = {"label": display, "values": values}
            if "total" in display.lower() or "ending" in display.lower(): rd["bold"] = True
            if "beginning" in display.lower(): rd["spaceBefore"] = True
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

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")
    return 0

if __name__ == "__main__":
    sys.exit(main())
