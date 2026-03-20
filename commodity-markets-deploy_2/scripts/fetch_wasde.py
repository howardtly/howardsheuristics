#!/usr/bin/env python3
"""
Fetch WASDE balance sheet data from USDA sources.
Tries multiple URLs with fallbacks.
Outputs: data/wasde.json (relative to repo root)
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

# Output to data/ at the repo root (go up from scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

# Multiple WASDE data URLs to try (in order)
WASDE_URLS = [
    # Cornell USDA library - reliable mirror
    "https://usda.library.cornell.edu/apidatasets/WASDE?format=xlsx",
    # USDA OCE direct download
    "https://www.usda.gov/sites/default/files/documents/oce-wasde-data-tables.xlsx",
    # ERS feed grains data (alternative)
    "https://www.ers.usda.gov/webdocs/DataFiles/50048/FeedGrainsYearbookTables2025.xlsx",
]


def download_with_retries(urls, timeout=45):
    """Try multiple URLs, return first successful response."""
    for url in urls:
        print(f"  Trying: {url}")
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
                content_type = resp.headers.get("Content-Type", "")
                print(f"  Success: {len(data):,} bytes, type: {content_type}")
                return data, url
        except urllib.error.HTTPError as e:
            print(f"  HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            print(f"  URL Error: {e.reason}")
        except TimeoutError:
            print(f"  Timeout after {timeout}s")
        except Exception as e:
            print(f"  Error: {e}")
    return None, None


def parse_wasde_us(wb_data):
    """Parse U.S. balance sheets from WASDE Excel workbook."""
    try:
        import openpyxl
        from io import BytesIO
        wb = openpyxl.load_workbook(BytesIO(wb_data), read_only=True, data_only=True)
    except Exception as e:
        print(f"  Failed to open workbook: {e}")
        return None

    print(f"  Sheets found: {wb.sheetnames}")

    commodities = {}

    # Try various possible sheet name patterns
    sheet_patterns = {
        "corn": ["Corn", "CORN", "U.S. Corn", "corn"],
        "soybeans": ["Soybeans", "SOYBEANS", "U.S. Soybeans", "soybeans"],
        "wheat": ["Wheat", "WHEAT", "U.S. Wheat", "wheat", "All Wheat"],
        "soybean_meal": ["Soybean Meal", "SOYBEAN MEAL", "Soy Meal", "SBM"],
        "soybean_oil": ["Soybean Oil", "SOYBEAN OIL", "Soy Oil", "SBO"],
    }

    for comm_id, patterns in sheet_patterns.items():
        sheet_name = None
        for p in patterns:
            if p in wb.sheetnames:
                sheet_name = p
                break
        # Also try case-insensitive partial match
        if sheet_name is None:
            for sn in wb.sheetnames:
                for p in patterns:
                    if p.lower() in sn.lower():
                        sheet_name = sn
                        break
                if sheet_name:
                    break

        if sheet_name is None:
            print(f"  No sheet found for {comm_id}")
            continue

        print(f"  Processing sheet: '{sheet_name}' -> {comm_id}")
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))

        if len(rows) < 3:
            print(f"    Too few rows ({len(rows)}), skipping")
            continue

        # Find header row with marketing years (pattern: YYYY/YY like "2024/25")
        header_row = None
        header_idx = None
        for i, row in enumerate(rows[:20]):  # Check first 20 rows
            if row is None:
                continue
            for cell in row:
                s = str(cell).strip() if cell else ""
                if "/" in s and len(s) == 7:
                    try:
                        yr = int(s[:4])
                        if 1980 <= yr <= 2030:
                            header_row = row
                            header_idx = i
                            break
                    except ValueError:
                        pass
            if header_row:
                break

        if header_row is None:
            print(f"    Could not find marketing year headers")
            # Print first few rows for debugging
            for i, row in enumerate(rows[:5]):
                print(f"    Row {i}: {[str(c)[:30] if c else '' for c in (row or [])][:8]}")
            continue

        # Extract marketing years
        years = []
        year_cols = []
        for j, cell in enumerate(header_row):
            s = str(cell).strip() if cell else ""
            if "/" in s and len(s) == 7:
                try:
                    yr = int(s[:4])
                    if 1980 <= yr <= 2030:
                        years.append(s)
                        year_cols.append(j)
                except ValueError:
                    pass

        print(f"    Found {len(years)} marketing years: {years[0]} to {years[-1]}")

        # Parse data rows into sections
        sections = []
        current_section = None

        for i in range(header_idx + 1, len(rows)):
            row = rows[i]
            if not row:
                continue

            # Get label from first non-empty cell
            label = None
            for cell in row[:3]:
                if cell and str(cell).strip():
                    label = str(cell).strip()
                    break
            if not label:
                continue

            # Get values for year columns
            values = []
            for j in year_cols:
                v = row[j] if j < len(row) else None
                values.append(v)

            non_null = sum(1 for v in values if v is not None and str(v).strip() not in ("", "--", "NA"))

            # Section header detection: row with few/no numeric values
            if non_null < max(3, len(years) * 0.2):
                if current_section and current_section["rows"]:
                    sections.append(current_section)
                current_section = {"header": label, "unit": "", "rows": []}
                continue

            if current_section is None:
                current_section = {"header": "Data", "unit": "", "rows": []}

            # Parse values to numbers
            parsed = []
            for v in values:
                if v is None or str(v).strip() in ("", "--", "NA", "N/A"):
                    parsed.append(None)
                else:
                    try:
                        parsed.append(float(str(v).replace(",", "")))
                    except ValueError:
                        parsed.append(None)

            row_data = {"label": label, "values": parsed}

            lower = label.lower()
            if "total" in lower or "ending stocks" in lower:
                row_data["bold"] = True
            if "stocks/use" in lower or "percent" in lower:
                row_data["pct"] = True
            if "price" in lower or "$/bu" in lower or "$/ton" in lower or "cents" in lower:
                row_data["price"] = True

            current_section["rows"].append(row_data)

        if current_section and current_section["rows"]:
            sections.append(current_section)

        commodities[comm_id] = {
            "id": comm_id,
            "label": sheet_name,
            "years": years,
            "sections": sections,
        }
        total_rows = sum(len(s["rows"]) for s in sections)
        print(f"    Result: {len(years)} years, {len(sections)} sections, {total_rows} data rows")

    return commodities if commodities else None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    print("=" * 60)
    print("WASDE Data Fetch")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print(f"Output: {output_file}")
    print("=" * 60)

    result = {
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "source": None,
        "us": None,
    }

    print("\n-- Downloading WASDE workbook --")
    wb_data, source_url = download_with_retries(WASDE_URLS)

    if wb_data:
        result["source"] = source_url
        print(f"\n-- Parsing U.S. Balance Sheets --")
        us_data = parse_wasde_us(wb_data)
        if us_data:
            result["us"] = us_data
            print(f"\n  SUCCESS: Parsed {len(us_data)} commodities")
        else:
            print(f"\n  FAILED: Could not parse any commodities from workbook")
            # Save the raw file for debugging
            debug_path = os.path.join(OUTPUT_DIR, "wasde_debug.xlsx")
            with open(debug_path, "wb") as f:
                f.write(wb_data)
            print(f"  Saved raw workbook to {debug_path} for debugging")
    else:
        print("\n  FAILED: Could not download from any URL")

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    file_size = os.path.getsize(output_file)
    print(f"  Wrote {file_size:,} bytes")

    if result["us"]:
        print("\nDone! Data fetched successfully.")
        return 0
    else:
        print("\nDone with errors. Check logs above.")
        return 0  # Don't fail the action so we can see the debug output


if __name__ == "__main__":
    sys.exit(main())
