#!/usr/bin/env python3
"""
Fetch WASDE / S&D balance sheet data from USDA ERS data products.
v5: Handles tab-numbered sheet names, XML-broken Excel files.
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
    "Accept": "*/*",
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
            ct = resp.headers.get("Content-Type", "")
            print(f"  OK: {len(data):,} bytes ({ct[:50]})")
            return data
    except Exception as e:
        print(f"  FAILED: {e}")
        return None


def open_workbook(data, filename=""):
    """Try openpyxl first, fall back to xlrd for broken files."""
    # Try openpyxl
    try:
        import openpyxl
        wb = openpyxl.load_workbook(BytesIO(data), read_only=True, data_only=True)
        print(f"  Sheets (openpyxl): {wb.sheetnames[:15]}")
        return wb, "openpyxl"
    except Exception as e:
        print(f"  openpyxl failed: {str(e)[:100]}")

    # Try openpyxl without stylesheet validation
    try:
        import openpyxl
        from copy import copy
        import warnings
        warnings.filterwarnings("ignore")
        # Try with different options
        wb = openpyxl.load_workbook(BytesIO(data), read_only=True, data_only=True, keep_links=False)
        print(f"  Sheets (openpyxl relaxed): {wb.sheetnames[:15]}")
        return wb, "openpyxl"
    except Exception:
        pass

    # Try pandas as fallback
    try:
        import pandas as pd
        xls = pd.ExcelFile(BytesIO(data), engine="openpyxl")
        print(f"  Sheets (pandas/openpyxl): {xls.sheet_names[:15]}")
        return xls, "pandas"
    except Exception:
        pass

    try:
        import pandas as pd
        xls = pd.ExcelFile(BytesIO(data), engine="calamine")
        print(f"  Sheets (pandas/calamine): {xls.sheet_names[:15]}")
        return xls, "pandas"
    except Exception:
        pass

    print(f"  Could not open workbook with any method")
    return None, None


def get_sheet_rows(wb, wb_type, sheet_name):
    """Get rows from a sheet, handling different workbook types."""
    if wb_type == "openpyxl":
        ws = wb[sheet_name]
        return list(ws.iter_rows(values_only=True))
    elif wb_type == "pandas":
        import pandas as pd
        df = pd.read_excel(wb, sheet_name=sheet_name, header=None)
        return [tuple(row) for row in df.values.tolist()]
    return []


def get_sheet_names(wb, wb_type):
    if wb_type == "openpyxl":
        return wb.sheetnames
    elif wb_type == "pandas":
        return wb.sheet_names
    return []


def find_header_row(rows, max_scan=30):
    for i, row in enumerate(rows[:max_scan]):
        if row is None:
            continue
        for cell in row:
            s = str(cell).strip() if cell else ""
            if "/" in s and len(s) == 7:
                try:
                    yr = int(s[:4])
                    if 1980 <= yr <= 2030:
                        return i
                except ValueError:
                    pass
    return None


def extract_years(header_row):
    years = []
    year_cols = []
    for j, cell in enumerate(header_row or []):
        s = str(cell).strip() if cell else ""
        if "/" in s and len(s) == 7:
            try:
                yr = int(s[:4])
                if 1980 <= yr <= 2030:
                    years.append(s)
                    year_cols.append(j)
            except ValueError:
                pass
    return years, year_cols


def parse_sheet(rows, header_idx, years, year_cols):
    sections = []
    current_section = None

    for i in range(header_idx + 1, len(rows)):
        row = rows[i]
        if not row:
            continue

        label = None
        for cell in row[:4]:
            if cell is not None and str(cell).strip():
                label = str(cell).strip()
                break
        if not label:
            continue
        # Skip footnote rows
        if label.startswith("1/") or label.startswith("2/") or label.startswith("Source") or label.startswith("Note"):
            continue

        values = [row[j] if j < len(row) else None for j in year_cols]
        non_null = sum(1 for v in values if v is not None and str(v).strip() not in ("", "--", "NA", "N/A", "nan"))

        if non_null < max(3, len(years) * 0.15):
            if current_section and current_section["rows"]:
                sections.append(current_section)
            current_section = {"header": label, "unit": "", "rows": []}
            continue

        if current_section is None:
            current_section = {"header": "Data", "unit": "", "rows": []}

        parsed = []
        for v in values:
            sv = str(v).strip() if v is not None else ""
            if sv in ("", "--", "NA", "N/A", "nan", "None"):
                parsed.append(None)
            else:
                try:
                    parsed.append(float(sv.replace(",", "")))
                except ValueError:
                    parsed.append(None)

        row_data = {"label": label, "values": parsed}
        lower = label.lower()
        if "total" in lower and ("supply" in lower or "use" in lower or "usage" in lower or "disappearance" in lower or "commitment" in lower):
            row_data["bold"] = True
        if "ending stocks" in lower:
            row_data["bold"] = True
        if "stocks/use" in lower or "stocks-to-use" in lower:
            row_data["pct"] = True
        if "price" in lower or "$/bu" in lower or "$/ton" in lower or "cents per" in lower:
            row_data["price"] = True

        current_section["rows"].append(row_data)

    if current_section and current_section["rows"]:
        sections.append(current_section)

    return sections


def scan_all_sheets(wb, wb_type, comm_id, label, keywords):
    """Scan every sheet looking for S&D data matching keywords in row labels."""
    for sn in get_sheet_names(wb, wb_type):
        if sn.lower() == "contents":
            continue
        try:
            rows = get_sheet_rows(wb, wb_type, sn)
            hi = find_header_row(rows)
            if hi is None:
                continue
            years, yc = extract_years(rows[hi])
            if len(years) < 5:
                continue

            # Check first 15 data rows for keyword matches
            matches = 0
            for r in rows[hi+1:hi+15]:
                if r:
                    lbl = str(r[0]).strip().lower() if r[0] else ""
                    if any(k in lbl for k in keywords):
                        matches += 1

            if matches >= 2:
                sections = parse_sheet(rows, hi, years, yc)
                total_rows = sum(len(s["rows"]) for s in sections)
                if total_rows >= 3:
                    print(f"    Found {comm_id} in sheet '{sn}': {len(years)} years, {total_rows} rows")
                    return {
                        "id": comm_id, "label": label,
                        "years": years, "sections": sections,
                    }
        except Exception as e:
            continue
    return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    print("=" * 60)
    print("WASDE Data Fetch v5")
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
        wb, wbt = open_workbook(data)
        if wb:
            # The corn S&D is in a sheet with tab-style naming
            # Look for sheets with supply/demand keywords
            corn_keywords = ["planted", "harvested", "production", "beginning", "supply", "feed", "ending stocks", "total"]
            d = scan_all_sheets(wb, wbt, "corn", "Corn", corn_keywords)
            if d:
                result["us"]["corn"] = d

    # ── SOYBEANS, MEAL, OIL ──
    print("\n-- OIL CROPS --")
    data = fetch_url(OILCROPS_URL)
    if data:
        try:
            zf = zipfile.ZipFile(BytesIO(data))
            print(f"  ZIP files: {[f for f in zf.namelist() if f.endswith('.xlsx')]}")

            # Soy.xlsx should have soybeans data
            soy_keywords = ["planted", "harvested", "crush", "production", "beginning", "supply", "ending stocks"]
            meal_keywords = ["production", "beginning", "supply", "exports", "domestic", "ending stocks"]
            oil_keywords = ["production", "beginning", "supply", "exports", "domestic", "ending stocks"]

            for fname in zf.namelist():
                if not fname.endswith(".xlsx"):
                    continue

                fname_lower = fname.lower()
                try:
                    file_data = zf.read(fname)
                    wb, wbt = open_workbook(file_data, fname)
                    if not wb:
                        continue

                    # Determine what to look for based on filename
                    if "soy" in fname_lower and "soybeans" not in result["us"]:
                        print(f"\n  Scanning {fname} for soybeans...")
                        d = scan_all_sheets(wb, wbt, "soybeans", "Soybeans", soy_keywords)
                        if d:
                            result["us"]["soybeans"] = d

                        # Also look for meal and oil in same file
                        if "soybean_meal" not in result["us"]:
                            print(f"  Scanning {fname} for soybean meal...")
                            d = scan_all_sheets(wb, wbt, "soybean_meal", "Soybean Meal", meal_keywords)
                            if d:
                                result["us"]["soybean_meal"] = d

                        if "soybean_oil" not in result["us"]:
                            print(f"  Scanning {fname} for soybean oil...")
                            d = scan_all_sheets(wb, wbt, "soybean_oil", "Soybean Oil", oil_keywords)
                            if d:
                                result["us"]["soybean_oil"] = d

                    elif "oilcrops" in fname_lower or "alltable" in fname_lower:
                        # This might have all three
                        for cid, lbl, kw in [("soybeans", "Soybeans", soy_keywords), ("soybean_meal", "Soybean Meal", meal_keywords), ("soybean_oil", "Soybean Oil", oil_keywords)]:
                            if cid not in result["us"]:
                                print(f"  Scanning {fname} for {cid}...")
                                d = scan_all_sheets(wb, wbt, cid, lbl, kw)
                                if d:
                                    result["us"][cid] = d

                except Exception as e:
                    print(f"  Error with {fname}: {e}")

            # If still missing, brute force every xlsx/every sheet
            for cid, lbl, kw in [("soybeans", "Soybeans", soy_keywords), ("soybean_meal", "Soybean Meal", meal_keywords), ("soybean_oil", "Soybean Oil", oil_keywords)]:
                if cid in result["us"]:
                    continue
                print(f"\n  Brute-force scan for {cid}...")
                for fname in zf.namelist():
                    if not fname.endswith(".xlsx"):
                        continue
                    try:
                        file_data = zf.read(fname)
                        wb, wbt = open_workbook(file_data, fname)
                        if wb:
                            d = scan_all_sheets(wb, wbt, cid, lbl, kw)
                            if d:
                                result["us"][cid] = d
                                break
                    except Exception:
                        pass

        except Exception as e:
            print(f"  ZIP error: {e}")

    # ── WHEAT ──
    print("\n-- WHEAT --")
    data = fetch_url(WHEAT_URL)
    if data:
        wb, wbt = open_workbook(data)
        if wb:
            wheat_keywords = ["planted", "harvested", "production", "beginning", "supply", "food", "feed", "ending stocks"]
            d = scan_all_sheets(wb, wbt, "wheat", "Wheat", wheat_keywords)
            if d:
                result["us"]["wheat"] = d
        else:
            # openpyxl failed - try saving and reopening with pandas+calamine
            print("  Trying pandas fallback...")
            try:
                import pandas as pd
                # Try different engines
                for engine in ["calamine", "openpyxl", None]:
                    try:
                        eng_label = engine or "default"
                        print(f"    Trying engine: {eng_label}")
                        xls = pd.ExcelFile(BytesIO(data), engine=engine)
                        print(f"    Sheets: {xls.sheet_names[:15]}")

                        wheat_kw = ["planted", "harvested", "production", "beginning", "supply", "food", "feed", "ending stocks"]
                        for sn in xls.sheet_names:
                            if sn.lower() == "contents":
                                continue
                            try:
                                df = pd.read_excel(xls, sheet_name=sn, header=None)
                                rows = [tuple(row) for row in df.values.tolist()]
                                hi = find_header_row(rows)
                                if hi is None:
                                    continue
                                years, yc = extract_years(rows[hi])
                                if len(years) < 5:
                                    continue
                                matches = 0
                                for r in rows[hi+1:hi+15]:
                                    if r:
                                        lbl = str(r[0]).strip().lower() if r[0] else ""
                                        if any(k in lbl for k in wheat_kw):
                                            matches += 1
                                if matches >= 2:
                                    sections = parse_sheet(rows, hi, years, yc)
                                    total_rows = sum(len(s["rows"]) for s in sections)
                                    if total_rows >= 3:
                                        result["us"]["wheat"] = {
                                            "id": "wheat", "label": "Wheat",
                                            "years": years, "sections": sections,
                                        }
                                        print(f"    Found wheat in '{sn}': {len(years)} years, {total_rows} rows")
                                        break
                            except Exception:
                                continue
                        if "wheat" in result["us"]:
                            break
                    except Exception as e:
                        print(f"    Engine {eng_label} failed: {str(e)[:80]}")
            except ImportError:
                print("  pandas not available")

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print(f"RESULTS: {len(result['us'])} commodities")
    for comm_id, d in result["us"].items():
        total_rows = sum(len(s["rows"]) for s in d["sections"])
        print(f"  {comm_id}: {len(d['years'])} years, {len(d['sections'])} sections, {total_rows} rows")

    if not result["us"]:
        print("\nWARNING: No data parsed.")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  Wrote {os.path.getsize(output_file):,} bytes")
    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
