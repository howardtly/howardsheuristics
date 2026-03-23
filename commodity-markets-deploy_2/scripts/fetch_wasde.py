#!/usr/bin/env python3
"""
Fetch WASDE / S&D balance sheet data from USDA ERS.
v6: Targets exact sheet formats identified from debug run.
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

CORN_URL = "https://www.ers.usda.gov/media/5764/feed-grains-yearbook-tables-all-years.xlsx?v=77939"
OILCROPS_URL = "https://www.ers.usda.gov/media/5219/all-tables-oil-crops-yearbook-complete-data-set-in-compressed-zip-file.zip?v=11593"
WHEAT_URL = "https://www.ers.usda.gov/media/5706/wheat-data-all-years.xlsx?v=53976"


def fetch_url(url, timeout=60):
    print(f"  Fetching: {url[:90]}...")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            print(f"  OK: {len(data):,} bytes")
            return data
    except Exception as e:
        print(f"  FAILED: {e}")
        return None


def to_float(v):
    if v is None:
        return None
    s = str(v).strip()
    if s in ("", "--", "NA", "N/A", "nan", "None"):
        return None
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


# ═══════════════════════════════════════════════════════════
# CORN — FGYearbookTable04
# Quarterly data. We want only the "MY September-August" rows
# which contain the annual totals.
# Row 1: headers (Marketing year, Quarter, Beg stocks, Prod, Imports, Total supply, FSI, Seed, Feed, Total domestic)
# Then need to also get: Exports, Ending stocks from remaining columns
# ═══════════════════════════════════════════════════════════

def parse_corn(wb_data):
    import openpyxl
    wb = openpyxl.load_workbook(BytesIO(wb_data), read_only=True, data_only=True)
    ws = wb["FGYearbookTable04"]
    rows = list(ws.iter_rows(values_only=True))

    # Row 0: title
    # Row 1: headers
    # Find all columns from header row
    header = rows[1]
    print(f"  Corn headers: {[str(c)[:30] if c else '' for c in header]}")

    # Find column count by checking how many columns have data
    ncols = len(header)

    # Extract marketing year annual rows (where Quarter contains "MY" or "MY September-August")
    years = []
    data_rows = []

    for i in range(2, len(rows)):
        row = rows[i]
        if not row or len(row) < 2:
            continue
        my = str(row[0]).strip() if row[0] else ""
        quarter = str(row[1]).strip() if row[1] else ""

        # Annual row: quarter starts with "MY" 
        if quarter.startswith("MY"):
            if "/" in my and len(my) >= 7:
                years.append(my)
                vals = [to_float(row[c]) for c in range(2, ncols)]
                data_rows.append(vals)

    if not years:
        print("  No annual rows found")
        return None

    # Build column labels from header (skip first 2: Marketing year, Quarter)
    col_labels = []
    for c in range(2, ncols):
        label = str(header[c]).strip() if header[c] else f"Col{c}"
        # Clean up multiline headers
        label = label.replace("\n", " ").strip()
        col_labels.append(label)

    print(f"  Corn: {len(years)} years ({years[0]}..{years[-1]}), {len(col_labels)} columns")
    print(f"  Columns: {col_labels}")

    # Build sections - single section with all line items
    section_rows = []
    for ci, label in enumerate(col_labels):
        values = [data_rows[yi][ci] for yi in range(len(years))]
        row_data = {"label": label, "values": values}

        lower = label.lower()
        if "total supply" in lower or "total domestic" in lower:
            row_data["bold"] = True
        if "ending stocks" in lower:
            row_data["bold"] = True

        section_rows.append(row_data)

    return {
        "id": "corn", "label": "Corn",
        "years": years,
        "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": section_rows}],
    }


# ═══════════════════════════════════════════════════════════
# SOYBEANS — Soy.xlsx tab3
# Headers span rows 1-5, data starts at row 7
# Row 7: "1980/81", values...
# Columns: Beg stocks, Production, Imports, Total, Crush, Exports, Seed/feed/residual, Total, Ending stocks
# ═══════════════════════════════════════════════════════════

def parse_soy_annual(wb, sheet_name, comm_id, label, col_labels, data_start_row=7, year_col=0):
    """Parse annual S&D from soy workbook sheets (tab3, tab4, tab5)."""
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))

    print(f"  {label}: sheet '{sheet_name}', {len(rows)} rows")
    print(f"  Row headers (0-6):")
    for i in range(min(7, len(rows))):
        print(f"    Row {i}: {[str(c)[:25] if c else '' for c in (rows[i] or [])][:10]}")

    # Find data columns: skip the year column, take the rest
    # Determine how many data columns we expect
    ncols = len(col_labels)

    years = []
    data_rows = []

    for i in range(data_start_row, len(rows)):
        row = rows[i]
        if not row:
            continue
        year_val = str(row[year_col]).strip() if row[year_col] else ""
        if "/" not in year_val:
            continue
        # Must be a marketing year like "1980/81"
        if len(year_val) < 6:
            continue
        try:
            int(year_val[:4])
        except ValueError:
            continue

        years.append(year_val)
        # Data columns start after the year column
        vals = [to_float(row[year_col + 1 + c]) for c in range(ncols)]
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
        if "total" in lower:
            row_data["bold"] = True
        if "ending" in lower:
            row_data["bold"] = True
        if "price" in lower:
            row_data["price"] = True
        section_rows.append(row_data)

    return {
        "id": comm_id, "label": label,
        "years": years,
        "sections": [{"header": "Supply and disappearance", "unit": "", "rows": section_rows}],
    }


# ═══════════════════════════════════════════════════════════
# WHEAT — needs pandas+calamine due to broken XML
# ═══════════════════════════════════════════════════════════

def parse_wheat(wb_data):
    """Parse wheat data using pandas with calamine engine."""
    try:
        import pandas as pd
    except ImportError:
        print("  pandas not installed, skipping wheat")
        return None

    # Try calamine engine first (handles broken XML), fall back to others
    xls = None
    for engine in ["calamine", "openpyxl", None]:
        try:
            xls = pd.ExcelFile(BytesIO(wb_data), engine=engine)
            print(f"  Wheat opened with engine: {engine or 'default'}")
            print(f"  Sheets: {xls.sheet_names[:15]}")
            break
        except Exception as e:
            print(f"  Engine {engine} failed: {str(e)[:60]}")

    if xls is None:
        print("  Could not open wheat workbook")
        return None

    # Look for the supply/disappearance sheet
    # Based on wheat data products, look for sheets with S&D keywords
    for sn in xls.sheet_names:
        if sn.lower() == "contents":
            continue
        try:
            df = pd.read_excel(xls, sheet_name=sn, header=None)
            rows = [tuple(r) for r in df.values.tolist()]

            # Check first 15 rows for marketing year pattern
            header_idx = None
            for i, row in enumerate(rows[:20]):
                for cell in row:
                    s = str(cell).strip() if pd.notna(cell) else ""
                    if "/" in s and len(s) == 7:
                        try:
                            yr = int(s[:4])
                            if 1980 <= yr <= 2030:
                                header_idx = i
                                break
                        except ValueError:
                            pass
                if header_idx is not None:
                    break

            if header_idx is None:
                continue

            # Check if this has S&D content
            sd_keywords = ["production", "imports", "supply", "food", "feed", "exports", "stocks"]
            matches = 0
            for i in range(max(0, header_idx-5), min(len(rows), header_idx+10)):
                for cell in rows[i]:
                    s = str(cell).strip().lower() if pd.notna(cell) else ""
                    if any(k in s for k in sd_keywords):
                        matches += 1

            if matches < 3:
                continue

            print(f"  Found wheat S&D in sheet '{sn}'")
            print(f"  First rows:")
            for i in range(min(8, len(rows))):
                cells = [str(c)[:25] if pd.notna(c) else "" for c in rows[i][:10]]
                print(f"    Row {i}: {cells}")

            # This looks like S&D data - extract it
            # Check if years are in the first column (annual format) or across columns
            # Try: years in column 0, line items across columns (like corn quarterly)
            # Or: line items in column 0, years across top (transposed)

            # Check if first data column has marketing years
            first_col_years = []
            for i in range(header_idx, min(len(rows), header_idx + 60)):
                s = str(rows[i][0]).strip() if pd.notna(rows[i][0]) else ""
                if "/" in s and len(s) >= 6:
                    try:
                        int(s[:4])
                        first_col_years.append((i, s))
                    except ValueError:
                        pass

            if first_col_years:
                # Years in first column - similar to soy format
                print(f"  Format: years in rows ({len(first_col_years)} found)")

                # Get column headers from rows above data
                col_labels = []
                header_row = rows[header_idx - 1] if header_idx > 0 else rows[header_idx]
                for c in range(1, len(header_row)):
                    lbl = str(header_row[c]).strip() if pd.notna(header_row[c]) else ""
                    if lbl:
                        col_labels.append(lbl)
                    else:
                        break

                if not col_labels:
                    # Try the header_idx row itself
                    for c in range(1, len(rows[header_idx])):
                        lbl = str(rows[header_idx][c]).strip() if pd.notna(rows[header_idx][c]) else ""
                        if lbl:
                            col_labels.append(lbl)
                        else:
                            break

                print(f"  Column labels: {col_labels[:10]}")

                years = []
                data_rows_list = []
                for row_idx, year_str in first_col_years:
                    years.append(year_str)
                    vals = [to_float(rows[row_idx][c]) for c in range(1, 1 + len(col_labels))]
                    data_rows_list.append(vals)

                if not years or not col_labels:
                    continue

                section_rows = []
                for ci, lbl in enumerate(col_labels):
                    values = [data_rows_list[yi][ci] for yi in range(len(years))]
                    row_data = {"label": lbl, "values": values}
                    lower = lbl.lower()
                    if "total" in lower:
                        row_data["bold"] = True
                    if "ending" in lower or "stocks" in lower:
                        row_data["bold"] = True
                    if "price" in lower:
                        row_data["price"] = True
                    section_rows.append(row_data)

                total_rows = len(section_rows)
                if total_rows >= 3:
                    print(f"  Wheat: {len(years)} years, {total_rows} rows")
                    return {
                        "id": "wheat", "label": "Wheat",
                        "years": years,
                        "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": section_rows}],
                    }

            else:
                # Years might be across the top (line items in rows)
                # Find the row with marketing years
                year_row = rows[header_idx]
                years = []
                year_cols = []
                for j, cell in enumerate(year_row):
                    s = str(cell).strip() if pd.notna(cell) else ""
                    if "/" in s and len(s) >= 6:
                        try:
                            int(s[:4])
                            years.append(s)
                            year_cols.append(j)
                        except ValueError:
                            pass

                if len(years) < 5:
                    continue

                print(f"  Format: years across top ({len(years)} found)")

                section_rows = []
                for i in range(header_idx + 1, len(rows)):
                    row = rows[i]
                    lbl = str(row[0]).strip() if pd.notna(row[0]) else ""
                    if not lbl or lbl.startswith("Source") or lbl.startswith("Note") or lbl.startswith("1/"):
                        continue
                    values = [to_float(row[j]) for j in year_cols]
                    non_null = sum(1 for v in values if v is not None)
                    if non_null < 3:
                        continue
                    row_data = {"label": lbl, "values": values}
                    lower = lbl.lower()
                    if "total" in lower:
                        row_data["bold"] = True
                    if "ending" in lower:
                        row_data["bold"] = True
                    if "price" in lower:
                        row_data["price"] = True
                    section_rows.append(row_data)

                if len(section_rows) >= 3:
                    print(f"  Wheat: {len(years)} years, {len(section_rows)} rows")
                    return {
                        "id": "wheat", "label": "Wheat",
                        "years": years,
                        "sections": [{"header": "Supply and disappearance", "unit": "million bushels", "rows": section_rows}],
                    }

        except Exception as e:
            print(f"  Error processing sheet '{sn}': {e}")

    print("  Could not find wheat S&D data in any sheet")
    return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    print("=" * 60)
    print("WASDE Data Fetch v6")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)

    result = {
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "us": {},
    }

    # ── CORN ──
    print("\n-- CORN --")
    data = fetch_url(CORN_URL)
    if data:
        corn = parse_corn(data)
        if corn:
            result["us"]["corn"] = corn
            total = sum(len(s["rows"]) for s in corn["sections"])
            print(f"  SUCCESS: {len(corn['years'])} years, {total} rows")

    # ── SOYBEANS, MEAL, OIL ──
    print("\n-- OIL CROPS --")
    data = fetch_url(OILCROPS_URL)
    if data:
        try:
            import openpyxl
            zf = zipfile.ZipFile(BytesIO(data))

            # Use Soy.xlsx for all three
            if "Soy.xlsx" in zf.namelist():
                soy_data = zf.read("Soy.xlsx")
                wb = openpyxl.load_workbook(BytesIO(soy_data), read_only=True, data_only=True)

                # tab3: Soybeans S&D
                # Columns: Beginning stocks, Production, Imports, Total, Crush, Exports, Seed/feed/residual, Total, Ending stocks
                soy = parse_soy_annual(wb, "tab3", "soybeans", "Soybeans",
                    ["Beginning stocks", "Production", "Imports", "Total supply", "Crush", "Exports", "Seed, feed, and residual", "Total disappearance", "Ending stocks"],
                    data_start_row=7)
                if soy:
                    result["us"]["soybeans"] = soy
                    print(f"  SUCCESS soybeans: {len(soy['years'])} years")

                # tab4: Soybean Meal S&D
                # Columns: Beg stocks, Production, Imports, Total, Domestic, Exports, Total, Ending stocks, Price
                meal = parse_soy_annual(wb, "tab4", "soybean_meal", "Soybean Meal",
                    ["Beginning stocks", "Production", "Imports", "Total supply", "Domestic use", "Exports", "Total disappearance", "Ending stocks", "Price ($/short ton)"],
                    data_start_row=7)
                if meal:
                    result["us"]["soybean_meal"] = meal
                    print(f"  SUCCESS soybean meal: {len(meal['years'])} years")

                # tab5: Soybean Oil S&D
                # Columns: Beg stocks, Production, Imports, Total, Domestic total, Biofuel, Exports, Total, Ending stocks
                oil = parse_soy_annual(wb, "tab5", "soybean_oil", "Soybean Oil",
                    ["Beginning stocks", "Production", "Imports", "Total supply", "Domestic total", "Biofuel", "Exports", "Total disappearance", "Ending stocks"],
                    data_start_row=6)
                if oil:
                    result["us"]["soybean_oil"] = oil
                    print(f"  SUCCESS soybean oil: {len(oil['years'])} years")

        except Exception as e:
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()

    # ── WHEAT ──
    print("\n-- WHEAT --")
    data = fetch_url(WHEAT_URL)
    if data:
        wheat = parse_wheat(data)
        if wheat:
            result["us"]["wheat"] = wheat
            total = sum(len(s["rows"]) for s in wheat["sections"])
            print(f"  SUCCESS: {len(wheat['years'])} years, {total} rows")

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print(f"RESULTS: {len(result['us'])} / 5 commodities")
    for cid, d in result["us"].items():
        total = sum(len(s["rows"]) for s in d["sections"])
        print(f"  {cid}: {len(d['years'])} years, {total} rows")
        # Print first few row labels
        for s in d["sections"]:
            for r in s["rows"][:3]:
                print(f"    - {r['label']}: {r['values'][-3:]} (last 3 years)")

    missing = [c for c in ["corn", "soybeans", "wheat", "soybean_meal", "soybean_oil"] if c not in result["us"]]
    if missing:
        print(f"\n  MISSING: {missing}")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  Wrote {os.path.getsize(output_file):,} bytes")
    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
