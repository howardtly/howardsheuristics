#!/usr/bin/env python3
"""
Fetch WASDE balance sheet data from USDA sources.

U.S. data: WASDE report Excel files from USDA OCE
World data: USDA FAS PSD Online API

Outputs: data/wasde.json
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# ──────────────────────────────────────────────────────────────
# USDA WASDE Excel workbook approach
# The WASDE report is published as Excel files at:
# https://www.usda.gov/oce/commodity/wasde/wasde-latest-report
#
# The full historical data tables are at:
# https://www.usda.gov/oce/commodity/wasde/wasde-data
# Direct link pattern: wasdeXXXX.xls where XXXX is the report number
# ──────────────────────────────────────────────────────────────

# Alternative: USDA ERS Feed Grains database has clean CSV downloads
# https://www.ers.usda.gov/data-products/feed-grains-database/feed-grains-yearbook-tables/
# And Oil Crops database:
# https://www.ers.usda.gov/data-products/oil-crops-yearbook/

# For simplicity and reliability, we'll use the WASDE bulk data download
# which is an Excel workbook with all commodities and all years.

WASDE_DATA_URL = "https://www.usda.gov/sites/default/files/documents/oce-wasde-data-tables.xlsx"

# Fallback: Cornell USDA library mirror
WASDE_CORNELL_URL = "https://usda.library.cornell.edu/apidatasets/WASDE"

# PSD API for world data (no API key required)
PSD_API_BASE = "https://apps.fas.usda.gov/PSDOnline/api"


def fetch_wasde_excel():
    """Download the WASDE data tables Excel workbook."""
    print(f"Fetching WASDE data from {WASDE_DATA_URL}")
    try:
        req = urllib.request.Request(WASDE_DATA_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        print(f"  Downloaded {len(data):,} bytes")
        return data
    except urllib.error.URLError as e:
        print(f"  Failed: {e}")
        return None


def parse_wasde_us(wb_data):
    """
    Parse U.S. balance sheets from WASDE Excel workbook.
    
    Expected sheet names: 'Corn', 'Soybeans', 'Wheat', 'Soybean Meal', 'Soybean Oil'
    Each sheet has marketing years as columns and line items as rows.
    
    Returns dict keyed by commodity with sections/rows matching our app format.
    """
    try:
        import openpyxl
        from io import BytesIO
        wb = openpyxl.load_workbook(BytesIO(wb_data), read_only=True, data_only=True)
    except ImportError:
        print("  openpyxl not installed, trying xlrd...")
        try:
            import xlrd
            # xlrd only handles .xls, not .xlsx — may need openpyxl
            print("  Note: xlrd may not handle .xlsx files. Install openpyxl: pip install openpyxl")
            return None
        except ImportError:
            print("  ERROR: Neither openpyxl nor xlrd available. Install with: pip install openpyxl")
            return None

    commodities = {}
    
    # Map sheet names to our commodity IDs
    sheet_map = {
        "Corn": "corn",
        "Soybeans": "soybeans", 
        "Wheat": "wheat",
        "Soybean Meal": "soybean_meal",
        "Soybean Oil": "soybean_oil",
    }
    
    for sheet_name, comm_id in sheet_map.items():
        if sheet_name not in wb.sheetnames:
            print(f"  Sheet '{sheet_name}' not found, skipping")
            continue
            
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))
        
        if len(rows) < 3:
            print(f"  Sheet '{sheet_name}' has too few rows, skipping")
            continue
        
        # Find the header row with marketing years (e.g., "1990/91", "2024/25")
        header_row = None
        header_idx = None
        for i, row in enumerate(rows):
            row_strs = [str(c) if c else "" for c in row]
            if any("/" in s and len(s) == 7 for s in row_strs):
                header_row = row
                header_idx = i
                break
        
        if header_row is None:
            print(f"  Could not find marketing year headers in '{sheet_name}'")
            continue
        
        # Extract marketing years from header
        years = []
        year_cols = []
        for j, cell in enumerate(header_row):
            s = str(cell) if cell else ""
            if "/" in s and len(s) == 7:
                years.append(s)
                year_cols.append(j)
        
        # Parse data rows
        sections = []
        current_section = None
        
        for i in range(header_idx + 1, len(rows)):
            row = rows[i]
            if not row or not row[0]:
                continue
            
            label = str(row[0]).strip()
            if not label:
                continue
            
            # Check if this is a section header (typically bold or all-caps in the source)
            # Heuristic: if most year columns are empty, it's likely a section header
            values = [row[j] if j < len(row) else None for j in year_cols]
            non_null = sum(1 for v in values if v is not None and str(v).strip() != "")
            
            if non_null < len(years) * 0.3 and non_null < 3:
                # Section header
                if current_section:
                    sections.append(current_section)
                current_section = {"header": label, "unit": "", "rows": []}
                continue
            
            if current_section is None:
                current_section = {"header": "Data", "unit": "", "rows": []}
            
            # Parse numeric values
            parsed_values = []
            for v in values:
                if v is None or str(v).strip() == "" or str(v).strip() == "--":
                    parsed_values.append(None)
                else:
                    try:
                        parsed_values.append(float(str(v).replace(",", "")))
                    except ValueError:
                        parsed_values.append(None)
            
            row_data = {"label": label, "values": parsed_values}
            
            # Detect bold/total rows
            lower = label.lower()
            if "total" in lower or "ending stocks" in lower:
                row_data["bold"] = True
            if "stocks/use" in lower or "percent" in lower:
                row_data["pct"] = True
            if "price" in lower or "$/bu" in lower or "$/ton" in lower:
                row_data["price"] = True
            if label.startswith("  ") or label.startswith("\t"):
                row_data["indent"] = True
                row_data["label"] = label.strip()
            
            current_section["rows"].append(row_data)
        
        if current_section:
            sections.append(current_section)
        
        commodities[comm_id] = {
            "id": comm_id,
            "label": sheet_name,
            "years": years,
            "sections": sections,
        }
        print(f"  Parsed {sheet_name}: {len(years)} years, {len(sections)} sections, {sum(len(s['rows']) for s in sections)} rows")
    
    return commodities


def fetch_psd_world(commodity_code, commodity_name, countries):
    """
    Fetch world balance sheet data from USDA PSD API.
    
    PSD API endpoint: GET /api/commodity/{commodityCode}
    No API key required.
    
    Parameters:
      commodity_code: PSD commodity code (e.g., "0440000" for corn)
      commodity_name: Display name
      countries: list of country codes to fetch
    
    Returns dict with world total and country-level S&D data.
    """
    url = f"{PSD_API_BASE}/commodity/{commodity_code}"
    print(f"  Fetching PSD data for {commodity_name} from {url}")
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        print(f"  Got {len(data)} records")
        return data
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"  Failed: {e}")
        return None


# PSD commodity codes
PSD_CODES = {
    "corn": "0440000",
    "soybeans": "2222000", 
    "wheat": "0410000",
    "soybean_meal": "0813100",
    "soybean_oil": "4232000",
}

# PSD country codes for major producers/consumers
PSD_COUNTRIES = {
    "corn": ["US", "CH", "BR", "AR", "UA"],
    "soybeans": ["US", "BR", "AR", "CH", "PY"],
    "wheat": ["US", "CH", "RS", "CA", "AU", "UA", "AR"],
    "soybean_meal": ["US", "BR", "AR", "CH"],
    "soybean_oil": ["US", "BR", "AR", "CH"],
}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")
    
    print("=" * 60)
    print("WASDE Data Fetch")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)
    
    result = {
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "us": None,
        "world": None,
    }
    
    # ── U.S. Balance Sheets ──
    print("\n── U.S. Balance Sheets (WASDE) ──")
    wb_data = fetch_wasde_excel()
    if wb_data:
        us_data = parse_wasde_us(wb_data)
        if us_data:
            result["us"] = us_data
            print(f"  ✓ Parsed {len(us_data)} commodities")
        else:
            print("  ✗ Failed to parse Excel workbook")
    else:
        print("  ✗ Failed to download WASDE data")
    
    # ── World Balance Sheets (PSD) ──
    print("\n── World Balance Sheets (PSD) ──")
    world_data = {}
    for comm_id, code in PSD_CODES.items():
        countries = PSD_COUNTRIES.get(comm_id, [])
        psd_data = fetch_psd_world(code, comm_id, countries)
        if psd_data:
            world_data[comm_id] = psd_data
    
    if world_data:
        result["world"] = world_data
        print(f"  ✓ Fetched {len(world_data)} commodities")
    
    # ── Write output ──
    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    
    file_size = os.path.getsize(output_file)
    print(f"  ✓ Wrote {file_size:,} bytes")
    print("\nDone!")
    
    return 0 if result["us"] else 1


if __name__ == "__main__":
    sys.exit(main())
