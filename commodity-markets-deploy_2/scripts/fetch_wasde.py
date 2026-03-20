#!/usr/bin/env python3
"""
Fetch WASDE / S&D balance sheet data from USDA ERS data products.
Uses confirmed working URLs as of March 2026.
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

# Confirmed working URLs (March 2026)
CORN_URL = "https://www.ers.usda.gov/media/5764/feed-grains-yearbook-tables-all-years.xlsx?v=77939"
OILCROPS_URL = "https://www.ers.usda.gov/media/5219/all-tables-oil-crops-yearbook-complete-data-set-in-compressed-zip-file.zip?v=11593"
WHEAT_URL = "https://www.ers.usda.gov/media/5706/wheat-data-all-years.xlsx?v=53976"


def fetch_url(url, timeout=60):
    """Fetch a URL, return bytes or None."""
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
    """Open an Excel workbook from bytes. Returns openpyxl Workbook or None."""
    import openpyxl
    try:
        wb = openpyxl.load_workbook(BytesIO(data), read_only=True, data_only=True)
        print(f"  Sheets: {wb.sheetnames[:15]}")
        return wb
    except Exception as e:
        print(f"  Failed to open as Excel: {e}")
        return None


def find_header_row(rows, max_scan=30):
    """Find the row index containing marketing year headers (YYYY/YY pattern)."""
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
    """Extract marketing year strings and column indices from a header row."""
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
    """Parse S&D data rows into sections."""
    sections = []
    current_section = None

    for i in range(header_idx + 1, len(rows)):
        row = rows[i]
        if not row:
            continue

        # Get label
        label = None
        for cell in row[:4]:
            if cell and str(cell).strip():
                label = str(cell).strip()
                break
        if not label:
            continue

        # Get values
        values = [row[j] if j < len(row) else None for j in year_cols]
        non_null = sum(1 for v in values if v is not None and str(v).strip() not in ("", "--", "NA", "N/A", "1/"))

        # Section header: mostly empty numeric columns
        if non_null < max(3, len(years) * 0.15):
            if current_section and current_section["rows"]:
                sections.append(current_section)
            current_section = {"header": label, "unit": "", "rows": []}
            continue

        if current_section is None:
            current_section = {"header": "Data", "unit": "", "rows": []}

        # Parse values
        parsed = []
        for v in values:
            if v is None or str(v).strip() in ("", "--", "NA", "N/A", "1/", "2/"):
                parsed.append(None)
            else:
                try:
                    parsed.append(float(str(v).replace(",", "")))
                except ValueError:
                    parsed.append(None)

        row_data = {"label": label, "values": parsed}
        lower = label.lower()
        if "total" in lower and ("supply" in lower or "use" in lower or "usage" in lower or "disappearance" in lower):
            row_data["bold"] = True
        if "ending stocks" in lower:
            row_data["bold"] = True
        if "stocks/use" in lower or "stocks-to-use" in lower or "percent" in lower:
            row_data["pct"] = True
        if "price" in lower or "$/bu" in lower or "$/ton" in lower or "cents per" in lower:
            row_data["price"] = True

        current_section["rows"].append(row_data)

    if current_section and current_section["rows"]:
        sections.append(current_section)

    return sections


def process_workbook(wb, target_sheets):
    """
    Process a workbook looking for specific commodity sheets.
    target_sheets: dict mapping commodity_id -> list of possible sheet name patterns
    Returns dict of commodity data.
    """
    results = {}

    for comm_id, patterns in target_sheets.items():
        # Find matching sheet
        sheet_name = None
        for p in patterns:
            # Exact match first
            if p in wb.sheetnames:
                sheet_name = p
                break
        if not sheet_name:
            # Case-insensitive partial match
            for sn in wb.sheetnames:
                for p in patterns:
                    if p.lower() in sn.lower():
                        sheet_name = sn
                        break
                if sheet_name:
                    break

        if not sheet_name:
            print(f"  {comm_id}: no matching sheet found")
            continue

        print(f"  {comm_id}: using sheet '{sheet_name}'")
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))

        header_idx = find_header_row(rows)
        if header_idx is None:
            print(f"    No marketing year headers found")
            # Debug: print first rows
            for i, r in enumerate(rows[:5]):
                print(f"    Row {i}: {[str(c)[:20] if c else '' for c in (r or [])][:8]}")
            continue

        years, year_cols = extract_years(rows[header_idx])
        if not years:
            print(f"    No years extracted from header")
            continue

        sections = parse_sheet(rows, header_idx, years, year_cols)
        total_rows = sum(len(s["rows"]) for s in sections)

        if total_rows == 0:
            print(f"    No data rows parsed")
            continue

        results[comm_id] = {
            "id": comm_id,
            "label": comm_id.replace("_", " ").title(),
            "years": years,
            "sections": sections,
        }
        print(f"    OK: {len(years)} years ({years[0]}..{years[-1]}), {len(sections)} sections, {total_rows} rows")

    return results


def main():
    import openpyxl  # Verify it's installed
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    print("=" * 60)
    print("WASDE Data Fetch v4")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)

    result = {
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "us": {},
    }

    # ── CORN (Feed Grains Yearbook) ──
    print("\n-- CORN (Feed Grains Yearbook) --")
    data = fetch_url(CORN_URL)
    if data:
        wb = open_workbook(data)
        if wb:
            corn_sheets = {
                "corn": ["Corn", "Table 4", "FGYearbookTable04", "corn supply", "Corn Supply"],
            }
            parsed = process_workbook(wb, corn_sheets)
            # If no exact match, try every sheet
            if not parsed:
                print("  Trying all sheets...")
                for sn in wb.sheetnames:
                    ws = wb[sn]
                    rows = list(ws.iter_rows(values_only=True))
                    hi = find_header_row(rows)
                    if hi is not None:
                        years, yc = extract_years(rows[hi])
                        if len(years) > 10:
                            print(f"  Sheet '{sn}' has {len(years)} years - checking content...")
                            # Check if it has corn-related labels
                            for r in rows[hi+1:hi+10]:
                                if r:
                                    lbl = str(r[0]).strip().lower() if r[0] else ""
                                    if any(k in lbl for k in ["planted", "harvested", "production", "beginning", "supply", "feed"]):
                                        print(f"    Looks like S&D data, using this sheet")
                                        sections = parse_sheet(rows, hi, years, yc)
                                        if sections:
                                            total_rows = sum(len(s["rows"]) for s in sections)
                                            result["us"]["corn"] = {
                                                "id": "corn", "label": "Corn",
                                                "years": years, "sections": sections,
                                            }
                                            print(f"    OK: {len(years)} years, {total_rows} rows")
                                        break
                        if "corn" in result["us"]:
                            break
            else:
                result["us"].update(parsed)

    # ── SOYBEANS, MEAL, OIL (Oil Crops Yearbook - ZIP file) ──
    print("\n-- OIL CROPS (Soybeans, Meal, Oil) --")
    data = fetch_url(OILCROPS_URL)
    if data:
        try:
            zf = zipfile.ZipFile(BytesIO(data))
            print(f"  ZIP contents: {zf.namelist()[:15]}")

            soy_targets = {
                "soybeans": ["Soybeans", "Soybean", "soybean supply", "Table11", "soybeans supply"],
                "soybean_meal": ["Soybean Meal", "SBM", "Meal", "soybean meal", "Table21"],
                "soybean_oil": ["Soybean Oil", "SBO", "Oil", "soybean oil", "Table31"],
            }

            # Try each file in the zip
            for fname in zf.namelist():
                if not (fname.endswith(".xlsx") or fname.endswith(".xls")):
                    continue
                print(f"\n  Processing: {fname}")
                try:
                    file_data = zf.read(fname)
                    wb = open_workbook(file_data, fname)
                    if wb:
                        # Check which commodities this file might have
                        remaining = {k: v for k, v in soy_targets.items() if k not in result["us"]}
                        if remaining:
                            parsed = process_workbook(wb, remaining)
                            result["us"].update(parsed)
                except Exception as e:
                    print(f"    Error processing {fname}: {e}")

            # If we still didn't find things, try harder
            missing_soy = [k for k in soy_targets if k not in result["us"]]
            if missing_soy:
                print(f"\n  Still missing: {missing_soy}")
                print("  Trying every xlsx file, every sheet...")
                for fname in zf.namelist():
                    if not fname.endswith(".xlsx"):
                        continue
                    try:
                        file_data = zf.read(fname)
                        wb = open_workbook(file_data, fname)
                        if wb:
                            for sn in wb.sheetnames:
                                sn_lower = sn.lower()
                                ws = wb[sn]
                                rows = list(ws.iter_rows(values_only=True))
                                hi = find_header_row(rows)
                                if hi is None:
                                    continue
                                years, yc = extract_years(rows[hi])
                                if len(years) < 5:
                                    continue

                                comm_id = None
                                if "soybeans" not in result["us"] and ("soybean" in sn_lower and "meal" not in sn_lower and "oil" not in sn_lower):
                                    comm_id = "soybeans"
                                elif "soybean_meal" not in result["us"] and "meal" in sn_lower:
                                    comm_id = "soybean_meal"
                                elif "soybean_oil" not in result["us"] and "oil" in sn_lower:
                                    comm_id = "soybean_oil"

                                if comm_id:
                                    sections = parse_sheet(rows, hi, years, yc)
                                    if sections and sum(len(s["rows"]) for s in sections) > 3:
                                        result["us"][comm_id] = {
                                            "id": comm_id,
                                            "label": comm_id.replace("_", " ").title(),
                                            "years": years, "sections": sections,
                                        }
                                        total_rows = sum(len(s["rows"]) for s in sections)
                                        print(f"    Found {comm_id} in {fname}/{sn}: {len(years)} years, {total_rows} rows")
                    except Exception as e:
                        pass

        except zipfile.BadZipFile:
            print("  Not a valid ZIP file")
        except Exception as e:
            print(f"  ZIP error: {e}")

    # ── WHEAT ──
    print("\n-- WHEAT --")
    data = fetch_url(WHEAT_URL)
    if data:
        wb = open_workbook(data)
        if wb:
            wheat_sheets = {
                "wheat": ["Wheat", "All Wheat", "wheat supply", "Supply", "Table01"],
            }
            parsed = process_workbook(wb, wheat_sheets)
            if not parsed:
                # Try all sheets
                print("  Trying all sheets...")
                for sn in wb.sheetnames:
                    ws = wb[sn]
                    rows = list(ws.iter_rows(values_only=True))
                    hi = find_header_row(rows)
                    if hi is not None:
                        years, yc = extract_years(rows[hi])
                        if len(years) > 10:
                            sections = parse_sheet(rows, hi, years, yc)
                            if sections:
                                total_rows = sum(len(s["rows"]) for s in sections)
                                if total_rows > 3:
                                    result["us"]["wheat"] = {
                                        "id": "wheat", "label": "Wheat",
                                        "years": years, "sections": sections,
                                    }
                                    print(f"    Found in '{sn}': {len(years)} years, {total_rows} rows")
                                    break
            else:
                result["us"].update(parsed)

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print(f"RESULTS: {len(result['us'])} commodities")
    for comm_id, d in result["us"].items():
        total_rows = sum(len(s["rows"]) for s in d["sections"])
        print(f"  {comm_id}: {len(d['years'])} years, {len(d['sections'])} sections, {total_rows} rows")

    if not result["us"]:
        print("\nWARNING: No data parsed. Dashboard will use representative data.")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    print(f"  Wrote {os.path.getsize(output_file):,} bytes")
    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
