#!/usr/bin/env python3
"""
WASDE Data Fetch v10
- Wheat: Table01 area + Table06 S&D, both filtered to "All wheat" rows
- Corn: area from Table01 with carry-forward
- Soybeans: area from tab02 converted to million acres
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
    return round(v) if v is not None else None

def r1(v):
    return round(v, 1) if v is not None else None

def pct(num, den):
    if num is not None and den is not None and den != 0:
        return round(num / den * 100, 1)
    return None


# ═══════════════════════════════════════════════════════════
# CORN
# ═══════════════════════════════════════════════════════════

def parse_corn(wb_data):
    import openpyxl
    wb = openpyxl.load_workbook(BytesIO(wb_data), read_only=True, data_only=True)

    # Area from Table01: col0=Commodity, col1=MY, col2=Planted, col3=Harvested, col4=Production, col5=Yield
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

    # S&D from Table04
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


# ═══════════════════════════════════════════════════════════
# SOYBEANS
# ═══════════════════════════════════════════════════════════

def parse_soybeans(wb):
    ws02 = wb["tab02"]
    rows02 = list(ws02.iter_rows(values_only=True))
    area_data = {}
    for i in range(4, len(rows02)):
        row = rows02[i]
        if not row: continue
        try: yr = int(str(row[0]).strip())
        except (ValueError, TypeError): continue
        my = f"{yr}/{str(yr+1)[-2:]}"
        planted = to_float(row[1])
        harvested = to_float(row[2])
        area_data[my] = {
            "planted": round(planted / 1000, 1) if planted else None,
            "harvested": round(harvested / 1000, 1) if harvested else None,
            "yield": r1(to_float(row[3])),
        }
    print(f"  Soy area: {len(area_data)} years")

    ws03 = wb["tab3"]
    rows03 = list(ws03.iter_rows(values_only=True))
    sd_labels = ["Beginning stocks", "Production", "Imports", "Total supply", "Crush", "Exports", "Seed, feed, and residual", "Total disappearance", "Ending stocks"]
    years, sd = [], []
    for i in range(7, len(rows03)):
        row = rows03[i]
        if not row: continue
        my = str(row[0]).strip() if row[0] else ""
        if "/" not in my or len(my) < 6: continue
        try: int(my[:4])
        except ValueError: continue
        years.append(my)
        sd.append([to_float(row[1 + c]) for c in range(len(sd_labels))])
    print(f"  Soy S&D: {len(years)} years")

    rows_out = [
        {"label": "Area planted", "values": [area_data.get(y, {}).get("planted") for y in years]},
        {"label": "Area harvested", "values": [area_data.get(y, {}).get("harvested") for y in years]},
        {"label": "Yield per harvested acre", "values": [area_data.get(y, {}).get("yield") for y in years]},
    ]
    renames = {"Total disappearance": "Total usage"}
    for ci, label in enumerate(sd_labels):
        display = renames.get(label, label)
        rd = {"label": display, "values": [ri(sd[yi][ci]) for yi in range(len(years))]}
        if "total" in display.lower() or "ending" in display.lower(): rd["bold"] = True
        if label == "Beginning stocks": rd["spaceBefore"] = True
        rows_out.append(rd)

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
        rd = {"label": display, "values": [ri(sd[yi][ci]) for yi in range(len(years))]}
        if "total" in display.lower() or "ending" in display.lower(): rd["bold"] = True
        rows_out.append(rd)

    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

    return {"id": "soybean_oil", "label": "Soybean Oil", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "million pounds", "rows": rows_out}]}


# ═══════════════════════════════════════════════════════════
# WHEAT — Table01 (area, filtered to "All wheat") + Table06 (S&D, filtered to "All wheat")
# ═══════════════════════════════════════════════════════════

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

    # --- Area from Table01, filtered to "All wheat" ---
    # Format: col0=Class, col1=Marketing year, col2=Planted (million acres), col3=Harvested (million acres), col4=Production, col5=Yield
    area_data = {}
    try:
        df = pd.read_excel(xls, sheet_name="Table01", header=None)
        rows = [tuple(r) for r in df.values.tolist()]
        print(f"  Wheat area: Table01, {len(rows)} rows")
        # Print header for reference
        print(f"    Header: {[str(c)[:30] if pd.notna(c) else '' for c in rows[1][:6]]}")

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
        print(f"    All wheat: {len(area_data)} years")
        if area_data:
            sample = list(area_data.keys())[-1]
            print(f"    Sample {sample}: {area_data[sample]}")
    except Exception as e:
        print(f"    Area error: {e}")

    # --- S&D from Table06, filtered to "All wheat" ---
    # Table06 has multiple wheat classes. We need rows where the class column = "All wheat"
    # Format may be: col0=Class/label, col1=MY, then S&D columns
    # OR: col0=MY with class rows interspersed
    # Let's detect the format
    try:
        df = pd.read_excel(xls, sheet_name="Table06", header=None)
        rows = [tuple(r) for r in df.values.tolist()]
        print(f"  Wheat S&D: Table06, {len(rows)} rows")
        # Print first 8 rows for debugging
        for i in range(min(8, len(rows))):
            print(f"    Row {i}: {[str(c)[:25] if pd.notna(c) else '' for c in rows[i][:12]]}")

        # Determine format: does it have a class column?
        # Check if any of the first data rows have "All wheat" or a wheat class name
        has_class_col = False
        header_idx = None
        for i in range(min(10, len(rows))):
            for c_idx, cell in enumerate(rows[i]):
                s = str(cell).strip().lower() if pd.notna(cell) else ""
                if s == "all wheat":
                    has_class_col = True
                    break
            # Find the header row (has "Beginning stocks" or "Marketing year")
            row_str = " ".join(str(c).lower() if pd.notna(c) else "" for c in rows[i])
            if "beginning stocks" in row_str or "marketing year" in row_str:
                header_idx = i

        print(f"    Has class column: {has_class_col}, Header at row: {header_idx}")

        if has_class_col and header_idx is not None:
            # Format with class column: col0=Class, col1=MY, col2+=S&D data
            # Get column labels from header row
            col_labels = []
            for c in range(2, 14):
                if c < len(rows[header_idx]):
                    val = str(rows[header_idx][c]).strip() if pd.notna(rows[header_idx][c]) else ""
                    if val: col_labels.append(val)
                    else: break
                else: break
            print(f"    S&D columns: {col_labels}")

            years, sd_data = [], []
            for i in range(header_idx + 1, len(rows)):
                row = rows[i]
                cls = str(row[0]).strip().lower() if pd.notna(row[0]) else ""
                if cls != "all wheat": continue
                my = str(row[1]).strip() if pd.notna(row[1]) else ""
                if "/" not in my or len(my) < 6: continue
                try: int(my[:4])
                except ValueError: continue
                years.append(my)
                sd_data.append([to_float(row[2 + c]) for c in range(len(col_labels))])

        else:
            # Format without class column: col0=MY, col1+=S&D data
            # Need to find "All wheat" section boundaries
            col_labels = []
            if header_idx is not None:
                for c in range(1, 13):
                    if c < len(rows[header_idx]):
                        val = str(rows[header_idx][c]).strip() if pd.notna(rows[header_idx][c]) else ""
                        if val: col_labels.append(val)
                        else: break
                    else: break
            print(f"    S&D columns: {col_labels}")

            # Find "All wheat" section
            in_all_wheat = False
            years, sd_data = [], []
            for i in range(len(rows)):
                row = rows[i]
                first = str(row[0]).strip().lower() if pd.notna(row[0]) else ""
                if first == "all wheat":
                    in_all_wheat = True
                    continue
                # Another class name ends the section
                if in_all_wheat and first and not any(c.isdigit() for c in first[:4]) and "/" not in first:
                    # Might be a new class
                    if any(w in first for w in ["hard red", "soft red", "white", "durum"]):
                        break
                if not in_all_wheat: continue
                my = str(row[0]).strip() if pd.notna(row[0]) else ""
                if "/" not in my or len(my) < 6: continue
                try: int(my[:4])
                except ValueError: continue
                years.append(my)
                sd_data.append([to_float(row[1 + c]) for c in range(len(col_labels))])

        if not years:
            print("    No All wheat data found in Table06")
            return None

        print(f"    All wheat S&D: {len(years)} years ({years[0]}..{years[-1]})")

        # Build output rows
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
            display = renames.get(lbl, lbl.replace(" 2/", "").replace(" 3/", "").replace(" 4/", ""))
            values = [ri(sd_data[yi][ci]) for yi in range(len(years))]
            rd = {"label": display, "values": values}
            if "total" in display.lower() or "ending" in display.lower(): rd["bold"] = True
            if "beginning" in display.lower(): rd["spaceBefore"] = True
            rows_out.append(rd)

        es = next((r for r in rows_out if "ending" in r["label"].lower()), None)
        tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
        if es and tu:
            rows_out.append({"label": "Stocks/use (%)", "values": [pct(es["values"][i], tu["values"][i]) for i in range(len(years))], "bold": True, "pct": True})

        print(f"    Final: {len(years)} years, {len(rows_out)} rows")
        return {"id": "wheat", "label": "Wheat", "years": years,
                "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}]}

    except Exception as e:
        print(f"  S&D error: {e}")
        import traceback; traceback.print_exc()
        return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    print("=" * 60)
    print("WASDE Data Fetch v10")
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
