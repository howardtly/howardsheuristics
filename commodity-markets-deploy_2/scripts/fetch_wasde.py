#!/usr/bin/env python3
"""
WASDE Data Fetch v8
- Adds area planted, area harvested, yield from separate ERS tables
- Rounds supply/use/stocks values to integers
- Calculates stocks/use %
- Adds spaceBefore markers for UI spacing
Outputs: data/wasde.json
"""

import json, os, sys, urllib.request, urllib.error, zipfile, math
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


def round_int(v):
    """Round to integer for supply/use/stocks fields."""
    if v is None: return None
    return round(v)


def round1(v):
    """Round to 1 decimal for area/yield fields."""
    if v is None: return None
    return round(v, 1)


def round_pct(v):
    """Round to 1 decimal for percentage."""
    if v is None: return None
    return round(v, 1)


# ═══════════════════════════════════════════════════════════
# CORN
# ═══════════════════════════════════════════════════════════

def parse_corn(wb_data):
    import openpyxl
    wb = openpyxl.load_workbook(BytesIO(wb_data), read_only=True, data_only=True)

    # --- Area/Yield from Table01 ---
    ws01 = wb["FGYearbookTable01"]
    rows01 = list(ws01.iter_rows(values_only=True))
    # Row 1: headers. Row 2+: Corn rows have "Corn" in col 0, MY in col 1
    area_planted = {}  # keyed by marketing year
    area_harvested = {}
    yield_per_acre = {}
    for i in range(2, len(rows01)):
        row = rows01[i]
        if not row: continue
        commodity = str(row[0]).strip() if row[0] else ""
        if commodity != "Corn" and commodity != "": continue
        if commodity == "" and not area_planted: continue  # skip non-corn
        if commodity != "Corn": continue
        my = str(row[1]).strip() if row[1] else ""
        if "/" not in my: continue
        area_planted[my] = to_float(row[2])
        area_harvested[my] = to_float(row[3])
        yield_per_acre[my] = to_float(row[5])  # col 5 is yield

    print(f"  Corn area: {len(area_planted)} years")

    # --- S&D from Table04 ---
    ws04 = wb["FGYearbookTable04"]
    rows04 = list(ws04.iter_rows(values_only=True))
    header = rows04[1]
    ncols = len([c for c in header if c is not None])

    current_my = None
    sd_years = []
    sd_data = []  # list of dicts keyed by column label

    col_labels = []
    for c in range(2, ncols):
        label = str(header[c]).strip().replace("\n", " ") if header[c] else f"Col{c}"
        col_labels.append(label)

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

    # --- Merge: use sd_years as the master year list ---
    years = sd_years
    
    # Build rows in desired order
    rows_out = []

    # Area planted
    rows_out.append({"label": "Area planted", "values": [round1(area_planted.get(y)) for y in years]})
    # Area harvested
    rows_out.append({"label": "Area harvested", "values": [round1(area_harvested.get(y)) for y in years]})
    # Yield
    rows_out.append({"label": "Yield per harvested acre", "values": [round1(yield_per_acre.get(y)) for y in years]})

    # S&D rows (rounded to int)
    sd_labels_ordered = [
        ("Beginning stocks", True, False),
        ("Production", False, False),
        ("Imports", False, False),
        ("Total supply 2/", True, True),  # bold, rename
        ("Food, alcohol, and industrial use", False, False),
        ("Seed use", False, False),
        ("Feed and residual use", False, False),
        ("Total domestic use 2/", True, True),
        ("Exports", False, False),
        ("Total use 2/", True, True),
        ("Ending stocks", True, False),
    ]

    # Clean up label names
    label_renames = {
        "Total supply 2/": "Total supply",
        "Total domestic use 2/": "Total domestic use",
        "Total use 2/": "Total usage",
    }

    for sd_label, bold, _ in sd_labels_ordered:
        display_label = label_renames.get(sd_label, sd_label)
        # Find matching column (fuzzy match on start)
        matched_key = None
        for k in col_labels:
            if k.startswith(sd_label[:20]):
                matched_key = k
                break
        if not matched_key:
            # Try exact
            for k in col_labels:
                if sd_label.lower().replace(" 2/", "") in k.lower():
                    matched_key = k
                    break

        if matched_key:
            values = [round_int(sd_data[yi].get(matched_key)) for yi in range(len(years))]
        else:
            values = [None] * len(years)
            print(f"    WARNING: could not find '{sd_label}' in columns")

        row_data = {"label": display_label, "values": values}
        if bold:
            row_data["bold"] = True
        # Add spaceBefore for beginning stocks (after yield)
        if sd_label == "Beginning stocks":
            row_data["spaceBefore"] = True
        rows_out.append(row_data)

    # Stocks/use %
    ending_idx = next((i for i, r in enumerate(rows_out) if r["label"] == "Ending stocks"), None)
    total_use_idx = next((i for i, r in enumerate(rows_out) if r["label"] == "Total usage"), None)
    if ending_idx is not None and total_use_idx is not None:
        es_vals = rows_out[ending_idx]["values"]
        tu_vals = rows_out[total_use_idx]["values"]
        su_vals = []
        for i in range(len(years)):
            if es_vals[i] is not None and tu_vals[i] is not None and tu_vals[i] != 0:
                su_vals.append(round_pct(es_vals[i] / tu_vals[i] * 100))
            else:
                su_vals.append(None)
        rows_out.append({"label": "Stocks/use (%)", "values": su_vals, "bold": True, "pct": True})

    return {
        "id": "corn", "label": "Corn", "years": years,
        "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}],
    }


# ═══════════════════════════════════════════════════════════
# SOYBEANS
# ═══════════════════════════════════════════════════════════

def parse_soybeans(wb):
    # Area/yield from tab02: Year, Planted, Harvested, Yield, Production, Value, Loan
    # Calendar years (1980, 1981...) — need to map to marketing years (1980/81)
    ws02 = wb["tab02"]
    rows02 = list(ws02.iter_rows(values_only=True))
    area_data = {}  # keyed by marketing year
    for i in range(5, len(rows02)):  # data starts around row 5
        row = rows02[i]
        if not row: continue
        year_val = str(row[0]).strip() if row[0] else ""
        try:
            yr = int(year_val)
        except ValueError:
            continue
        my = f"{yr}/{str(yr+1)[-2:]}"  # e.g., 1980 -> 1980/81
        area_data[my] = {
            "planted": to_float(row[1]),
            "harvested": to_float(row[2]),
            "yield": to_float(row[3]),
        }
    print(f"  Soy area: {len(area_data)} years")

    # S&D from tab3
    ws03 = wb["tab3"]
    rows03 = list(ws03.iter_rows(values_only=True))
    # Data starts at row 7, columns: Beg stocks, Production, Imports, Total, Crush, Exports, Seed/feed/residual, Total, Ending stocks
    sd_col_labels = ["Beginning stocks", "Production", "Imports", "Total supply", "Crush", "Exports", "Seed, feed, and residual", "Total disappearance", "Ending stocks"]

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
        vals = [to_float(row[1 + c]) for c in range(len(sd_col_labels))]
        sd_data.append(vals)

    print(f"  Soy S&D: {len(years)} years ({years[0]}..{years[-1]})")

    rows_out = []
    # Area rows (convert planted/harvested from 1000 acres to million acres)
    rows_out.append({"label": "Area planted", "values": [round1(area_data.get(y, {}).get("planted")) for y in years]})
    rows_out.append({"label": "Area harvested", "values": [round1(area_data.get(y, {}).get("harvested")) for y in years]})
    rows_out.append({"label": "Yield per harvested acre", "values": [round1(area_data.get(y, {}).get("yield")) for y in years]})

    # S&D rows
    for ci, label in enumerate(sd_col_labels):
        values = [round_int(sd_data[yi][ci]) for yi in range(len(years))]
        row_data = {"label": label, "values": values}
        if "total" in label.lower() or "ending" in label.lower():
            row_data["bold"] = True
        if label == "Beginning stocks":
            row_data["spaceBefore"] = True
        # Rename
        if label == "Total disappearance":
            row_data["label"] = "Total usage"
        rows_out.append(row_data)

    # Stocks/use
    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        su = []
        for i in range(len(years)):
            if es["values"][i] is not None and tu["values"][i] is not None and tu["values"][i] != 0:
                su.append(round_pct(es["values"][i] / tu["values"][i] * 100))
            else:
                su.append(None)
        rows_out.append({"label": "Stocks/use (%)", "values": su, "bold": True, "pct": True})

    return {"id": "soybeans", "label": "Soybeans", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}]}


# ═══════════════════════════════════════════════════════════
# SOYBEAN MEAL
# ═══════════════════════════════════════════════════════════

def parse_soymeal(wb):
    ws = wb["tab4"]
    rows = list(ws.iter_rows(values_only=True))
    col_labels = ["Beginning stocks", "Production", "Imports", "Total supply", "Domestic use", "Exports", "Total disappearance", "Ending stocks", "Price ($/short ton)"]

    years = []
    sd_data = []
    for i in range(7, len(rows)):
        row = rows[i]
        if not row: continue
        my = str(row[0]).strip() if row[0] else ""
        if "/" not in my or len(my) < 6: continue
        try: int(my[:4])
        except ValueError: continue
        years.append(my)
        vals = [to_float(row[1 + c]) for c in range(len(col_labels))]
        sd_data.append(vals)

    rows_out = []
    for ci, label in enumerate(col_labels):
        is_price = "price" in label.lower()
        values = [to_float(sd_data[yi][ci]) if is_price else round_int(sd_data[yi][ci]) for yi in range(len(years))]
        row_data = {"label": label, "values": values}
        if "total" in label.lower() or "ending" in label.lower():
            row_data["bold"] = True
        if is_price:
            row_data["price"] = True
        if label == "Total disappearance":
            row_data["label"] = "Total usage"
        rows_out.append(row_data)

    # Stocks/use
    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        su = []
        for i in range(len(years)):
            if es["values"][i] is not None and tu["values"][i] is not None and tu["values"][i] != 0:
                su.append(round_pct(es["values"][i] / tu["values"][i] * 100))
            else:
                su.append(None)
        rows_out.append({"label": "Stocks/use (%)", "values": su, "bold": True, "pct": True})

    return {"id": "soybean_meal", "label": "Soybean Meal", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "1,000 short tons", "rows": rows_out}]}


# ═══════════════════════════════════════════════════════════
# SOYBEAN OIL
# ═══════════════════════════════════════════════════════════

def parse_soyoil(wb):
    ws = wb["tab5"]
    rows = list(ws.iter_rows(values_only=True))
    col_labels = ["Beginning stocks", "Production", "Imports", "Total supply", "Domestic total", "Biofuel", "Exports", "Total disappearance", "Ending stocks"]

    years = []
    sd_data = []
    for i in range(6, len(rows)):  # data starts row 6
        row = rows[i]
        if not row: continue
        my = str(row[0]).strip() if row[0] else ""
        if "/" not in my or len(my) < 6: continue
        try: int(my[:4])
        except ValueError: continue
        years.append(my)
        vals = [to_float(row[1 + c]) for c in range(len(col_labels))]
        sd_data.append(vals)

    rows_out = []
    for ci, label in enumerate(col_labels):
        values = [round_int(sd_data[yi][ci]) for yi in range(len(years))]
        row_data = {"label": label, "values": values}
        if "total" in label.lower() or "ending" in label.lower():
            row_data["bold"] = True
        if label == "Total disappearance":
            row_data["label"] = "Total usage"
        rows_out.append(row_data)

    # Stocks/use
    es = next((r for r in rows_out if r["label"] == "Ending stocks"), None)
    tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
    if es and tu:
        su = []
        for i in range(len(years)):
            if es["values"][i] is not None and tu["values"][i] is not None and tu["values"][i] != 0:
                su.append(round_pct(es["values"][i] / tu["values"][i] * 100))
            else:
                su.append(None)
        rows_out.append({"label": "Stocks/use (%)", "values": su, "bold": True, "pct": True})

    return {"id": "soybean_oil", "label": "Soybean Oil", "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "million pounds", "rows": rows_out}]}


# ═══════════════════════════════════════════════════════════
# WHEAT (pandas + calamine)
# ═══════════════════════════════════════════════════════════

def parse_wheat(wb_data):
    try:
        import pandas as pd
    except ImportError:
        print("  ERROR: pandas not installed")
        return None

    xls = None
    for engine in ["calamine", "openpyxl", None]:
        try:
            xls = pd.ExcelFile(BytesIO(wb_data), engine=engine)
            print(f"  Wheat opened with: {engine}")
            break
        except Exception:
            pass
    if xls is None:
        return None

    # Look for area/yield table and S&D table
    area_data = {}
    sd_result = None

    for sn in xls.sheet_names:
        if sn.lower() == "contents": continue
        try:
            df = pd.read_excel(xls, sheet_name=sn, header=None)
            rows = [tuple(r) for r in df.values.tolist()]

            # Check title row for content type
            title = str(rows[0][0]).lower() if rows and pd.notna(rows[0][0]) else ""

            # Area/yield table: title contains "acreage" or "planted"
            if "acreage" in title or "planted" in title or "area" in title:
                print(f"  Wheat area in sheet '{sn}'")
                for i in range(2, len(rows)):
                    row = rows[i]
                    my = str(row[0]).strip() if pd.notna(row[0]) else ""
                    if "/" not in my: continue
                    try: int(my[:4])
                    except ValueError: continue
                    area_data[my] = {
                        "planted": to_float(row[1]) if len(row) > 1 else None,
                        "harvested": to_float(row[2]) if len(row) > 2 else None,
                        "yield": to_float(row[3]) if len(row) > 3 else None,
                    }
                print(f"    Found {len(area_data)} years")
                continue

            # S&D table: look for marketing year rows with supply/disappearance keywords
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

            if len(my_rows) < 10: continue

            # Check header rows for S&D keywords
            first_data = my_rows[0][0]
            sd_words = 0
            for i in range(max(0, first_data - 6), first_data):
                for c in range(1, min(12, len(rows[i]))):
                    val = str(rows[i][c]).lower() if pd.notna(rows[i][c]) else ""
                    if any(k in val for k in ["stocks", "production", "supply", "food", "feed", "exports"]):
                        sd_words += 1
            if sd_words < 3: continue

            # Build column labels
            col_labels = []
            for c in range(1, 12):
                parts = []
                for i in range(max(0, first_data - 5), first_data):
                    if c < len(rows[i]):
                        val = str(rows[i][c]).strip() if pd.notna(rows[i][c]) else ""
                        if val and val != "nan" and not val.startswith("Million") and not val.startswith("---"):
                            parts.append(val)
                combined = " ".join(parts).strip()
                if combined:
                    col_labels.append(combined)
                else:
                    break

            if len(col_labels) < 3: continue

            print(f"  Wheat S&D in sheet '{sn}': {len(my_rows)} years, {len(col_labels)} cols")
            print(f"  Columns: {col_labels}")

            years = [yr for _, yr in my_rows]
            data_list = []
            for row_idx, _ in my_rows:
                vals = [to_float(rows[row_idx][c]) for c in range(1, 1 + len(col_labels))]
                data_list.append(vals)

            # Build rows
            rows_out = []

            # Area rows from area_data
            if area_data:
                rows_out.append({"label": "Area planted", "values": [round1(area_data.get(y, {}).get("planted")) for y in years]})
                rows_out.append({"label": "Area harvested", "values": [round1(area_data.get(y, {}).get("harvested")) for y in years]})
                rows_out.append({"label": "Yield per harvested acre", "values": [round1(area_data.get(y, {}).get("yield")) for y in years]})

            # S&D rows
            for ci, lbl in enumerate(col_labels):
                values = [round_int(data_list[yi][ci]) for yi in range(len(years))]
                row_data = {"label": lbl, "values": values}
                lower = lbl.lower()
                if "total" in lower: row_data["bold"] = True
                if "ending" in lower: row_data["bold"] = True
                if "price" in lower: row_data["price"] = True
                if "beginning" in lower: row_data["spaceBefore"] = True
                # Rename
                if "total disappearance" in lower:
                    row_data["label"] = "Total usage"
                rows_out.append(row_data)

            # Stocks/use
            es = next((r for r in rows_out if "ending" in r["label"].lower()), None)
            tu = next((r for r in rows_out if r["label"] == "Total usage"), None)
            if not tu:
                tu = next((r for r in rows_out if "total disappearance" in r["label"].lower()), None)
            if es and tu:
                su = []
                for i in range(len(years)):
                    if es["values"][i] is not None and tu["values"][i] is not None and tu["values"][i] != 0:
                        su.append(round_pct(es["values"][i] / tu["values"][i] * 100))
                    else:
                        su.append(None)
                rows_out.append({"label": "Stocks/use (%)", "values": su, "bold": True, "pct": True})

            if len(rows_out) >= 5:
                sd_result = {"id": "wheat", "label": "Wheat", "years": years,
                            "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": rows_out}]}
                print(f"  OK: {len(years)} years, {len(rows_out)} rows")

        except Exception as e:
            print(f"  Sheet '{sn}' error: {e}")

    return sd_result


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    print("=" * 60)
    print("WASDE Data Fetch v8")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)

    result = {"fetched_at": datetime.utcnow().isoformat() + "Z", "us": {}}

    # CORN
    print("\n-- CORN --")
    data = fetch_url(CORN_URL)
    if data:
        corn = parse_corn(data)
        if corn:
            result["us"]["corn"] = corn
            print(f"  OK: {len(corn['years'])} years, {sum(len(s['rows']) for s in corn['sections'])} rows")

    # OIL CROPS
    print("\n-- OIL CROPS --")
    data = fetch_url(OILCROPS_URL)
    if data:
        try:
            import openpyxl
            zf = zipfile.ZipFile(BytesIO(data))
            if "Soy.xlsx" in zf.namelist():
                wb = openpyxl.load_workbook(BytesIO(zf.read("Soy.xlsx")), read_only=True, data_only=True)

                soy = parse_soybeans(wb)
                if soy: result["us"]["soybeans"] = soy

                meal = parse_soymeal(wb)
                if meal: result["us"]["soybean_meal"] = meal

                oil = parse_soyoil(wb)
                if oil: result["us"]["soybean_oil"] = oil
        except Exception as e:
            print(f"  Error: {e}")
            import traceback; traceback.print_exc()

    # WHEAT
    print("\n-- WHEAT --")
    data = fetch_url(WHEAT_URL)
    if data:
        wheat = parse_wheat(data)
        if wheat: result["us"]["wheat"] = wheat

    # Summary
    print(f"\n{'='*60}")
    print(f"RESULTS: {len(result['us'])} / 5 commodities")
    for cid, d in result["us"].items():
        total = sum(len(s["rows"]) for s in d["sections"])
        print(f"  {cid}: {len(d['years'])} years, {total} rows")
        for s in d["sections"]:
            for r in s["rows"][:5]:
                last3 = r["values"][-3:]
                print(f"    {r['label']}: ...{last3}")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")
    return 0

if __name__ == "__main__":
    sys.exit(main())
