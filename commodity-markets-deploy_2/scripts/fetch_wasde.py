#!/usr/bin/env python3
"""
Fetch WASDE / S&D balance sheet data from USDA ERS.
v7: Fixed corn parser to carry forward marketing year across quarters.
Outputs: data/wasde.json
"""

import json
import os
import sys
import urllib.request
import urllib.error
import zipfile
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


def parse_corn(wb_data):
    """Parse corn from FGYearbookTable04. Quarterly data — extract MY annual rows."""
    import openpyxl
    wb = openpyxl.load_workbook(BytesIO(wb_data), read_only=True, data_only=True)
    ws = wb["FGYearbookTable04"]
    rows = list(ws.iter_rows(values_only=True))

    header = rows[1]
    ncols = len([c for c in header if c is not None])
    print(f"  Corn header ({ncols} cols): {[str(c)[:30] if c else '' for c in header[:ncols]]}")

    # The marketing year is in column 0 but only on the first quarter row.
    # Subsequent quarters have empty column 0. The "MY" row also has empty column 0.
    # We need to carry forward the current marketing year.
    current_my = None
    years = []
    data_rows = []

    for i in range(2, len(rows)):
        row = rows[i]
        if not row or len(row) < 2:
            continue

        # Update marketing year if column 0 has a value
        col0 = str(row[0]).strip() if row[0] else ""
        if "/" in col0 and len(col0) >= 7:
            current_my = col0

        quarter = str(row[1]).strip() if row[1] else ""

        # Annual total row: quarter starts with "MY"
        if quarter.startswith("MY") and current_my:
            years.append(current_my)
            vals = [to_float(row[c]) for c in range(2, ncols)]
            data_rows.append(vals)

    if not years:
        print("  No annual MY rows found")
        return None

    # Column labels from header row (skip first 2)
    col_labels = []
    for c in range(2, ncols):
        label = str(header[c]).strip().replace("\n", " ") if header[c] else f"Col{c}"
        col_labels.append(label)

    print(f"  Corn: {len(years)} years ({years[0]}..{years[-1]})")
    print(f"  Columns: {col_labels}")

    section_rows = []
    for ci, label in enumerate(col_labels):
        values = [data_rows[yi][ci] for yi in range(len(years))]
        row_data = {"label": label, "values": values}
        lower = label.lower()
        if "total supply" in lower or "total domestic" in lower or "total use" in lower:
            row_data["bold"] = True
        if "ending stocks" in lower:
            row_data["bold"] = True
        section_rows.append(row_data)

    return {
        "id": "corn", "label": "Corn", "years": years,
        "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": section_rows}],
    }


def parse_soy_annual(wb, sheet_name, comm_id, label, col_labels, data_start_row=7):
    """Parse annual S&D from soy workbook sheets."""
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    ncols = len(col_labels)

    years = []
    data_rows = []

    for i in range(data_start_row, len(rows)):
        row = rows[i]
        if not row: continue
        year_val = str(row[0]).strip() if row[0] else ""
        if "/" not in year_val or len(year_val) < 6: continue
        try: int(year_val[:4])
        except ValueError: continue

        years.append(year_val)
        vals = [to_float(row[1 + c]) for c in range(ncols)]
        data_rows.append(vals)

    if not years:
        print(f"  No data rows found for {label}")
        return None

    print(f"  {label}: {len(years)} years ({years[0]}..{years[-1]})")

    section_rows = []
    for ci, lbl in enumerate(col_labels):
        values = [data_rows[yi][ci] for yi in range(len(years))]
        row_data = {"label": lbl, "values": values}
        lower = lbl.lower()
        if "total" in lower: row_data["bold"] = True
        if "ending" in lower: row_data["bold"] = True
        if "price" in lower: row_data["price"] = True
        section_rows.append(row_data)

    return {"id": comm_id, "label": label, "years": years,
            "sections": [{"header": "Supply and disappearance", "unit": "", "rows": section_rows}]}


def parse_wheat(wb_data):
    """Parse wheat using pandas+calamine."""
    try:
        import pandas as pd
    except ImportError:
        print("  ERROR: pandas not installed. Add to workflow: pip install pandas python-calamine")
        return None

    xls = None
    for engine in ["calamine", "openpyxl", None]:
        try:
            xls = pd.ExcelFile(BytesIO(wb_data), engine=engine)
            print(f"  Wheat opened with engine: {engine}")
            print(f"  Sheets: {xls.sheet_names[:15]}")
            break
        except Exception as e:
            print(f"  Engine {engine} failed: {str(e)[:60]}")

    if xls is None:
        return None

    for sn in xls.sheet_names:
        if sn.lower() == "contents": continue
        try:
            df = pd.read_excel(xls, sheet_name=sn, header=None)
            rows = [tuple(r) for r in df.values.tolist()]

            # Look for marketing year pattern in column 0
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

            # Check for S&D keywords in header rows above first data row
            first_data = my_rows[0][0]
            sd_words = 0
            header_labels = []
            for i in range(max(0, first_data - 6), first_data):
                for c in range(1, min(12, len(rows[i]))):
                    val = str(rows[i][c]).strip() if pd.notna(rows[i][c]) else ""
                    if val:
                        lower = val.lower()
                        if any(k in lower for k in ["stocks", "production", "imports", "supply", "food", "feed", "exports", "domestic"]):
                            sd_words += 1

            if sd_words < 3: continue

            # Build column labels from the header rows
            # The header is typically split across multiple rows - combine them
            col_labels = []
            for c in range(1, 12):
                parts = []
                for i in range(max(0, first_data - 5), first_data):
                    if i < len(rows) and c < len(rows[i]):
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
            print(f"  Sample: {my_rows[0][1]} -> {[str(rows[my_rows[0][0]][c])[:15] for c in range(1, 1+len(col_labels))]}")

            years = [yr for _, yr in my_rows]
            data_list = []
            for row_idx, _ in my_rows:
                vals = [to_float(rows[row_idx][c]) for c in range(1, 1 + len(col_labels))]
                data_list.append(vals)

            section_rows = []
            for ci, lbl in enumerate(col_labels):
                values = [data_list[yi][ci] for yi in range(len(years))]
                row_data = {"label": lbl, "values": values}
                lower = lbl.lower()
                if "total" in lower: row_data["bold"] = True
                if "ending" in lower or ("stocks" in lower and "beginning" not in lower): row_data["bold"] = True
                if "price" in lower: row_data["price"] = True
                section_rows.append(row_data)

            if len(section_rows) >= 3:
                return {"id": "wheat", "label": "Wheat", "years": years,
                        "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": section_rows}]}

        except Exception as e:
            print(f"  Sheet '{sn}' error: {e}")

    return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    print("=" * 60)
    print("WASDE Data Fetch v7")
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
            print(f"  OK: {len(corn['years'])} years")

    # OIL CROPS
    print("\n-- OIL CROPS --")
    data = fetch_url(OILCROPS_URL)
    if data:
        try:
            import openpyxl
            zf = zipfile.ZipFile(BytesIO(data))
            if "Soy.xlsx" in zf.namelist():
                wb = openpyxl.load_workbook(BytesIO(zf.read("Soy.xlsx")), read_only=True, data_only=True)

                soy = parse_soy_annual(wb, "tab3", "soybeans", "Soybeans",
                    ["Beginning stocks", "Production", "Imports", "Total supply", "Crush", "Exports", "Seed, feed, and residual", "Total disappearance", "Ending stocks"], 7)
                if soy: result["us"]["soybeans"] = soy

                meal = parse_soy_annual(wb, "tab4", "soybean_meal", "Soybean Meal",
                    ["Beginning stocks", "Production", "Imports", "Total supply", "Domestic use", "Exports", "Total disappearance", "Ending stocks", "Price ($/short ton)"], 7)
                if meal: result["us"]["soybean_meal"] = meal

                oil = parse_soy_annual(wb, "tab5", "soybean_oil", "Soybean Oil",
                    ["Beginning stocks", "Production", "Imports", "Total supply", "Domestic total", "Biofuel", "Exports", "Total disappearance", "Ending stocks"], 6)
                if oil: result["us"]["soybean_oil"] = oil
        except Exception as e:
            print(f"  Error: {e}")
            import traceback; traceback.print_exc()

    # WHEAT
    print("\n-- WHEAT --")
    data = fetch_url(WHEAT_URL)
    if data:
        wheat = parse_wheat(data)
        if wheat:
            result["us"]["wheat"] = wheat
            print(f"  OK: {len(wheat['years'])} years")

    # Summary
    print(f"\n{'='*60}")
    print(f"RESULTS: {len(result['us'])} / 5 commodities")
    for cid, d in result["us"].items():
        total = sum(len(s["rows"]) for s in d["sections"])
        print(f"  {cid}: {len(d['years'])} years, {total} rows")
        for s in d["sections"]:
            for r in s["rows"][:3]:
                print(f"    {r['label']}: ...{r['values'][-3:]}")

    missing = [c for c in ["corn","soybeans","wheat","soybean_meal","soybean_oil"] if c not in result["us"]]
    if missing: print(f"  MISSING: {missing}")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  {os.path.getsize(output_file):,} bytes")
    return 0

if __name__ == "__main__":
    sys.exit(main())
