#!/usr/bin/env python3
"""
WASDE Data Fetch v9
Fixes: corn area carry-forward, soy area unit conversion, wheat picks first S&D sheet only
"""

import json, os, sys, urllib.request, urllib.error, zipfile
from io import BytesIO
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

CORN_URL = "https://www.ers.usda.gov/media/5764/feed-grains-yearbook-tables-all-years.xlsx?v=77939"
OILCROPS_URL = "https://www.ers.usda.gov/media/5219/all-tables-oil-crops-yearbook-complete-data-set-in-compressed-zip-file.zip?v=11593"
WHEAT_URL = "https://www.ers.usda.gov/media/5706/wheat-data-all-years.xlsx?v=53976"


def fetch_url(url, timeout=60):
    print(f"  Fetching: {url[:90]}...")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception as e:
        print(f"  FAILED: {e}")
        return None


def to_float(v):
    if v is None: return None
    s = str(v).strip()
    if s in ("", "--", "NA", "N/A", "nan", "None"): return None
    try: return float(s.replace(",", ""))
    except ValueError: return None

def ri(v):
    """Round to int."""
    return round(v) if v is not None else None

def r1(v):
    """Round to 1 decimal."""
    return round(v, 1) if v is not None else None

def pct(num, den):
    """Calculate percentage, rounded to 1 decimal."""
    if num is not None and den is not None and den != 0:
        return round(num / den * 100, 1)
    return None


def parse_corn(wb_data):
    import openpyxl
    wb = openpyxl.load_workbook(BytesIO(wb_data), read_only=True, data_only=True)

    # --- Area/Yield from Table01 ---
    # Format: col0=Commodity (only on first row per commodity, then blank), col1=Marketing year,
    # col2=Area planted, col3=Area harvested, col4=Production, col5=Yield
    ws01 = wb["FGYearbookTable01"]
    rows01 = list(ws01.iter_rows(values_only=True))
    
    area_planted = {}
    area_harvested = {}
    yield_per_acre = {}
    
    in_corn = False
    for i in range(2, len(rows01)):
        row = rows01[i]
        if not row: continue
        commodity = str(row[0]).strip() if row[0] else ""
        
        # Start of corn section
        if commodity == "Corn":
            in_corn = True
        # Another commodity starts = end of corn
        elif commodity and commodity != "Corn" and in_corn:
            break
        
        if not in_corn:
            continue
            
        my = str(row[1]).strip() if row[1] else ""
        if "/" not in my or len(my) < 7:
            continue
            
        area_planted[my] = to_float(row[2])
        area_harvested[my] = to_float(row[3])
        yield_per_acre[my] = to_float(row[5])

    print(f"  Corn area: {len(area_planted)} years")
    if area_planted:
        sample_yr = list(area_planted.keys())[-1]
        print(f"    Sample {sample_yr}: planted={area_planted[sample_yr]}, harvested={area_harvested.get(sample_yr)}, yield={yield_per_acre.get(sample_yr)}")

    # --- S&D from Table04 (quarterly, extract MY annual rows) ---
    ws04 = wb["FGYearbookTable04"]
    rows04 = list(ws04.iter_rows(values_only=True))
    header = rows04[1]
    ncols = len([c for c in header if c is not None])

    col_labels = []
    for c in range(2, ncols):
        label = str(header[c]).strip().replace("\n", " ") if header[c] else f"Col{c}"
        col_labels.append(label)

    current_my = None
    sd_years = []
    sd_data = []

    for i in range(2, len(rows04)):
        row = rows04[i]
        if not row or len(row) < 2: continue
        col0 = str(row[0]).strip() if row[0] else ""
        if "/" in col0 and len(col0) >= 7:
            current_my = col0
        quarter = str(row[1]).strip() if row[1] else ""
        if quarter.startswith("MY") and current_my:
            sd_years.append(current_my)
            vals = {}
            for ci, label in enumerate(col_labels):
                vals[label] = to_float(row[2 + ci])
            sd_data.append(vals)

    print(f"  Corn S&D: {len(sd_years)} years ({sd_years[0]}..{sd_years[-1]})")

    years = sd_years
    rows_out = []

    # Area rows
    rows_out.append({"label": "Area planted", "values": [r1(area_planted.get(y)) for y in years]})
    rows_out.append({"label": "Area harvested", "values": [r1(area_harvested.get(y)) for y in years]})
    rows_out.append({"label": "Yield per harvested acre", "values": [r1(yield_per_acre.get(y)) for y in years]})

    # S&D rows
    label_map = [
        ("Beginning stocks", "Beginning stocks", True, False),
        ("Production", "Production", False, False),
        ("Imports", "Imports", False, False),
        ("Total supply", "Total supply", True, True),
        ("Food, alcohol, and industrial", "Food, alcohol, and industrial use", False, False),
        ("Seed use", "Seed use", False, False),
        ("Feed and residual", "Feed and residual use", False, False),
        ("Total domestic", "Total domestic use", True, True),
        ("Exports", "Exports", False, False),
        ("Total use", "Total usage", True, True),
        ("Ending stocks", "Ending stocks", True, False),
    ]

    for prefix, display, bold, _ in label_map:
        matched_key = None
        for k in col_labels:
            if k.lower().startswith(prefix.lower()):
                matched_key = k
                break
        values = [ri(sd_data[yi].get(matched_key)) if matched_key else None for yi in range(len(years))]
        row_data = {"label": display, "values": values}
        if bold: row_data["bold"] = True
        if display == "Beginning stocks": row_data["spaceBefore"] = True
        rows_out.append(row_data)

    # Stocks/use
    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

    return {"id": "corn", "label": "Corn", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}]}


def parse_soybeans(wb):
    # Area from tab02: calendar years, columns: Planted, Harvested, Yield, Production (in 1,000 acres / bushels / 1,000 bushels)
    ws02 = wb["tab02"]
    rows02 = list(ws02.iter_rows(values_only=True))
    area_data = {}
    for i in range(4, len(rows02)):
        row = rows02[i]
        if not row: continue
        year_val = str(row[0]).strip() if row[0] else ""
        try: yr = int(year_val)
        except ValueError: continue
        my = f"{yr}/{str(yr+1)[-2:]}"
        planted = to_float(row[1])
        harvested = to_float(row[2])
        yld = to_float(row[3])
        # planted/harvested are in 1,000 acres — convert to million acres
        area_data[my] = {
            "planted": round(planted / 1000, 1) if planted else None,
            "harvested": round(harvested / 1000, 1) if harvested else None,
            "yield": r1(yld),
        }
    print(f"  Soy area: {len(area_data)} years")
    if area_data:
        sample = list(area_data.keys())[-1]
        print(f"    Sample {sample}: {area_data[sample]}")

    # S&D from tab3
    ws03 = wb["tab3"]
    rows03 = list(ws03.iter_rows(values_only=True))
    sd_labels = ["Beginning stocks", "Production", "Imports", "Total supply", "Crush", "Exports", "Seed, feed, and residual", "Total disappearance", "Ending stocks"]

    years = []
    sd_data = []
    for i in range(7, len(rows03)):
        row = rows03[i]
        if not row: continue
        my = str(row[0]).strip() if row[0] else ""
        if "/" not in my or len(my) < 6: continue
        try: int(my[:4])
        except ValueError: continue
        years.append(my)
        sd_data.append([to_float(row[1 + c]) for c in range(len(sd_labels))])

    print(f"  Soy S&D: {len(years)} years")

    rows_out = []
    rows_out.append({"label": "Area planted", "values": [area_data.get(y, {}).get("planted") for y in years]})
    rows_out.append({"label": "Area harvested", "values": [area_data.get(y, {}).get("harvested") for y in years]})
    rows_out.append({"label": "Yield per harvested acre", "values": [area_data.get(y, {}).get("yield") for y in years]})

    renames = {"Total disappearance": "Total usage"}
    for ci, label in enumerate(sd_labels):
        display = renames.get(label, label)
        values = [ri(sd_data[yi][ci]) for yi in range(len(years))]
        row_data = {"label": display, "values": values}
        if "total" in display.lower() or "ending" in display.lower(): row_data["bold"] = True
        if label == "Beginning stocks": row_data["spaceBefore"] = True
        rows_out.append(row_data)

    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

    return {"id": "soybeans", "label": "Soybeans", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}]}


def parse_soymeal(wb):
    ws = wb["tab4"]
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
        values = [sd[yi][ci] if is_price else ri(sd[yi][ci]) for yi in range(len(years))]
        row_data = {"label": display, "values": values}
        if "total" in display.lower() or "ending" in display.lower(): row_data["bold"] = True
        if is_price: row_data["price"] = True
        rows_out.append(row_data)

    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

    return {"id": "soybean_meal", "label": "Soybean Meal", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "1,000 short tons", "rows": rows_out}]}


def parse_soyoil(wb):
    ws = wb["tab5"]
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
        values = [ri(sd[yi][ci]) for yi in range(len(years))]
        row_data = {"label": display, "values": values}
        if "total" in display.lower() or "ending" in display.lower(): row_data["bold"] = True
        rows_out.append(row_data)

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

    # --- Area/Yield ---
    # Table02 has wheat area data. Format: col0=MY, col1=planted, col2=harvested, col3=yield, col4=production
    # Units are million acres and bushels per acre
    area_data = {}
    for sn in xls.sheet_names:
        try:
            df = pd.read_excel(xls, sheet_name=sn, header=None)
            rows = [tuple(r) for r in df.values.tolist()]
            title = str(rows[0][0]).lower() if rows and pd.notna(rows[0][0]) else ""
            if "acreage" not in title and "planted" not in title and "area" not in title:
                continue
            print(f"  Wheat area: sheet '{sn}'")
            # Print first data rows to see format
            for i in range(min(5, len(rows))):
                print(f"    Row {i}: {[str(c)[:20] if pd.notna(c) else '' for c in rows[i][:6]]}")
            
            # Find header row and data start
            for i in range(len(rows)):
                my = str(rows[i][0]).strip() if pd.notna(rows[i][0]) else ""
                if "/" in my and len(my) >= 6:
                    try:
                        int(my[:4])
                        # This is a data row
                        planted = to_float(rows[i][1])
                        harvested = to_float(rows[i][2])
                        yld = to_float(rows[i][3])
                        area_data[my] = {"planted": r1(planted), "harvested": r1(harvested), "yield": r1(yld)}
                    except ValueError:
                        pass
            if area_data:
                sample = list(area_data.keys())[-1]
                print(f"    Found {len(area_data)} years, sample {sample}: {area_data[sample]}")
                break
        except Exception as e:
            print(f"    Error: {e}")

    # --- S&D: use Table07 specifically (All wheat supply and disappearance) ---
    # Stop after first good S&D sheet
    target_sheet = "Table07"
    sd_result = None
    
    try:
        df = pd.read_excel(xls, sheet_name=target_sheet, header=None)
        rows = [tuple(r) for r in df.values.tolist()]
        print(f"  Wheat S&D: sheet '{target_sheet}', {len(rows)} rows")
        
        # Print first rows
        for i in range(min(6, len(rows))):
            print(f"    Row {i}: {[str(c)[:25] if pd.notna(c) else '' for c in rows[i][:12]]}")

        # Find marketing year rows
        my_rows = []
        for i, row in enumerate(rows):
            s = str(row[0]).strip() if pd.notna(row[0]) else ""
            if "/" in s and len(s) >= 6:
                try:
                    yr = int(s[:4])
                    if 1980 <= yr <= 2030:
                        my_rows.append((i, s))
                except ValueError:
                    pass

        if not my_rows:
            print("    No marketing years found")
            return None

        # Build column labels from header rows above first data row
        first_data = my_rows[0][0]
        col_labels = []
        for c in range(1, 12):
            parts = []
            for i in range(max(0, first_data - 5), first_data):
                if c < len(rows[i]):
                    val = str(rows[i][c]).strip() if pd.notna(rows[i][c]) else ""
                    if val and val != "nan" and not val.startswith("Million") and not val.startswith("---") and not val.startswith("1,000"):
                        parts.append(val)
            combined = " ".join(parts).strip()
            if combined:
                col_labels.append(combined)
            else:
                break

        print(f"    Cols: {col_labels}")

        years = [yr for _, yr in my_rows]
        data_list = [[to_float(rows[idx][c]) for c in range(1, 1 + len(col_labels))] for idx, _ in my_rows]

        rows_out = []
        if area_data:
            rows_out.append({"label": "Area planted", "values": [area_data.get(y, {}).get("planted") for y in years]})
            rows_out.append({"label": "Area harvested", "values": [area_data.get(y, {}).get("harvested") for y in years]})
            rows_out.append({"label": "Yield per harvested acre", "values": [area_data.get(y, {}).get("yield") for y in years]})

        renames = {}
        for lbl in col_labels:
            lower = lbl.lower()
            if "total disappearance" in lower or "total disappearance 3/" in lower:
                renames[lbl] = "Total usage"
            elif "total supply" in lower:
                renames[lbl] = "Total supply"
            elif "total domestic" in lower:
                renames[lbl] = "Total domestic use"

        for ci, lbl in enumerate(col_labels):
            display = renames.get(lbl, lbl.replace(" 2/", "").replace(" 3/", "").replace(" 4/", ""))
            values = [ri(data_list[yi][ci]) for yi in range(len(years))]
            row_data = {"label": display, "values": values}
            if "total" in display.lower() or "ending" in display.lower(): row_data["bold"] = True
            if "beginning" in display.lower(): row_data["spaceBefore"] = True
            rows_out.append(row_data)

        es = next((r for r in rows_out if "ending" in r["label"].lower()), None)
        tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
        if not tu:
            tu = next((r for r in rows_out if "total disappearance" in r["label"].lower()), None)
        if es and tu:
            rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

        print(f"    OK: {len(years)} years, {len(rows_out)} rows")
        return {"id": "wheat", "label": "Wheat", "years": years,
                "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}]}

    except Exception as e:
        print(f"  Error: {e}")
        import traceback; traceback.print_exc()
        return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    print("=" * 60)
    print("WASDE Data Fetch v9")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)

    result = {"fetched_at": datetime.utcnow().isoformat() + "Z", "us": {}}

    print("\n-- CORN --")
    data = fetch_url(CORN_URL)
    if data:
        r = parse_corn(data)
        if r: result["us"]["corn"] = r

    print("\n-- OIL CROPS --")
    data = fetch_url(OILCROPS_URL)
    if data:
        try:
            import openpyxl
            zf = zipfile.ZipFile(BytesIO(data))
            if "Soy.xlsx" in zf.namelist():
                wb = openpyxl.load_workbook(BytesIO(zf.read("Soy.xlsx")), read_only=True, data_only=True)
                for fn, parser in [("soybeans", parse_soybeans), ("soybean_meal", parse_soymeal), ("soybean_oil", parse_soyoil)]:
                    r = parser(wb)
                    if r: result["us"][fn] = r
        except Exception as e:
            print(f"  Error: {e}")
            import traceback; traceback.print_exc()

    print("\n-- WHEAT --")
    data = fetch_url(WHEAT_URL)
    if data:
        r = parse_wheat(data)
        if r: result["us"]["wheat"] = r

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
