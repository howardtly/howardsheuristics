#!/usr/bin/env python3
"""
Fetch WASDE / S&D balance sheet data from USDA ERS data products.

Uses the ERS Feed Grains, Oil Crops, and Wheat databases which provide
clean CSV/Excel downloads of the same underlying WASDE data.

These URLs are more stable than the WASDE report files themselves.

Outputs: data/wasde.json
"""

import json
import os
import sys
import urllib.request
import urllib.error
import csv
from io import StringIO, BytesIO
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
}

# ──────────────────────────────────────────────────────────────
# ERS Data Product URLs
# Feed Grains: https://www.ers.usda.gov/data-products/feed-grains-database/
# Oil Crops:   https://www.ers.usda.gov/data-products/oil-crops-yearbook/
# Wheat:       https://www.ers.usda.gov/data-products/wheat-data/
# ──────────────────────────────────────────────────────────────

# Try multiple URL patterns for each data source
CORN_URLS = [
    "https://www.ers.usda.gov/webdocs/DataFiles/50048/FeedGrainsYearbookTables2024.xlsx",
    "https://www.ers.usda.gov/webdocs/DataFiles/50048/FGYearbookTable04.csv",
    "https://www.ers.usda.gov/data-products/feed-grains-database/feed-grains-yearbook-tables/?reportType=csv",
]

SOY_URLS = [
    "https://www.ers.usda.gov/webdocs/DataFiles/52218/OilCropsYearbook2024.xlsx",
    "https://www.ers.usda.gov/webdocs/DataFiles/52218/Soybeans.csv",
]

WHEAT_URLS = [
    "https://www.ers.usda.gov/webdocs/DataFiles/54392/WheatYearbook2024.xlsx", 
    "https://www.ers.usda.gov/webdocs/DataFiles/54392/WheatSupply-Disappearance.csv",
]

# WASDE direct - try the latest report number pattern
# Reports are numbered sequentially, ~660+ as of 2026
WASDE_DIRECT_URLS = [
    "https://downloads.usda.library.cornell.edu/usda-esmis/files/3t945q76s/latest/wasde.xlsx",
    "https://usda.library.cornell.edu/concern/publications/3t945q76s?format=xlsx",
]


def fetch_url(url, timeout=45):
    """Fetch a single URL, return bytes or None."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            ct = resp.headers.get("Content-Type", "")
            print(f"    OK: {len(data):,} bytes ({ct[:40]})")
            return data
    except urllib.error.HTTPError as e:
        print(f"    HTTP {e.code}")
        return None
    except Exception as e:
        print(f"    Error: {str(e)[:80]}")
        return None


def try_urls(urls):
    """Try multiple URLs, return first success."""
    for url in urls:
        print(f"  Trying: {url[:80]}...")
        data = fetch_url(url)
        if data and len(data) > 100:
            return data, url
    return None, None


def parse_excel_generic(wb_data):
    """Try to parse an Excel file and extract S&D data."""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(BytesIO(wb_data), read_only=True, data_only=True)
        print(f"    Sheets: {wb.sheetnames[:10]}")
        
        results = {}
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            rows = list(ws.iter_rows(values_only=True))
            if len(rows) > 3:
                # Check if this looks like S&D data
                for i, row in enumerate(rows[:15]):
                    has_years = False
                    for cell in (row or []):
                        s = str(cell).strip() if cell else ""
                        if "/" in s and len(s) == 7:
                            try:
                                yr = int(s[:4])
                                if 1980 <= yr <= 2030:
                                    has_years = True
                                    break
                            except ValueError:
                                pass
                    if has_years:
                        results[sheet_name] = {"header_row": i, "total_rows": len(rows)}
                        break
        
        if results:
            print(f"    Found S&D data in sheets: {list(results.keys())}")
        else:
            print(f"    No S&D-style data found in any sheet")
            # Print first sheet's first rows for debugging
            if wb.sheetnames:
                ws = wb[wb.sheetnames[0]]
                for i, row in enumerate(list(ws.iter_rows(values_only=True))[:5]):
                    print(f"    Row {i}: {[str(c)[:25] if c else '' for c in (row or [])][:6]}")
        
        return wb, results
    except Exception as e:
        print(f"    Parse error: {e}")
        return None, None


def extract_commodity(wb, sheet_name, header_row_idx, comm_id, label):
    """Extract a single commodity's S&D data from a workbook sheet."""
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    
    header_row = rows[header_row_idx]
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
    
    if not years:
        return None
    
    sections = []
    current_section = None
    
    for i in range(header_row_idx + 1, len(rows)):
        row = rows[i]
        if not row:
            continue
        
        lbl = None
        for cell in row[:3]:
            if cell and str(cell).strip():
                lbl = str(cell).strip()
                break
        if not lbl:
            continue
        
        values = [row[j] if j < len(row) else None for j in year_cols]
        non_null = sum(1 for v in values if v is not None and str(v).strip() not in ("", "--", "NA"))
        
        if non_null < max(3, len(years) * 0.2):
            if current_section and current_section["rows"]:
                sections.append(current_section)
            current_section = {"header": lbl, "unit": "", "rows": []}
            continue
        
        if current_section is None:
            current_section = {"header": "Data", "unit": "", "rows": []}
        
        parsed = []
        for v in values:
            if v is None or str(v).strip() in ("", "--", "NA", "N/A"):
                parsed.append(None)
            else:
                try:
                    parsed.append(float(str(v).replace(",", "")))
                except ValueError:
                    parsed.append(None)
        
        row_data = {"label": lbl, "values": parsed}
        lower = lbl.lower()
        if "total" in lower or "ending stocks" in lower:
            row_data["bold"] = True
        if "stocks/use" in lower or "percent" in lower:
            row_data["pct"] = True
        if "price" in lower or "$/bu" in lower or "$/ton" in lower:
            row_data["price"] = True
        
        current_section["rows"].append(row_data)
    
    if current_section and current_section["rows"]:
        sections.append(current_section)
    
    if not sections:
        return None
    
    total_rows = sum(len(s["rows"]) for s in sections)
    print(f"    {label}: {len(years)} years ({years[0]}..{years[-1]}), {len(sections)} sections, {total_rows} rows")
    
    return {
        "id": comm_id,
        "label": label,
        "years": years,
        "sections": sections,
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")
    
    print("=" * 60)
    print("WASDE Data Fetch v3")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)
    
    result = {
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "sources": [],
        "us": {},
    }
    
    # Strategy: try to get a single WASDE workbook first (has all commodities)
    # If that fails, try individual ERS data products
    
    print("\n-- Attempt 1: WASDE direct download --")
    wb_data, url = try_urls(WASDE_DIRECT_URLS)
    if wb_data:
        wb, sheet_info = parse_excel_generic(wb_data)
        if wb and sheet_info:
            result["sources"].append(url)
            for sheet_name, info in sheet_info.items():
                sn_lower = sheet_name.lower()
                if "corn" in sn_lower:
                    d = extract_commodity(wb, sheet_name, info["header_row"], "corn", "Corn")
                    if d: result["us"]["corn"] = d
                elif "soybean" in sn_lower and "meal" in sn_lower:
                    d = extract_commodity(wb, sheet_name, info["header_row"], "soybean_meal", "Soybean Meal")
                    if d: result["us"]["soybean_meal"] = d
                elif "soybean" in sn_lower and "oil" in sn_lower:
                    d = extract_commodity(wb, sheet_name, info["header_row"], "soybean_oil", "Soybean Oil")
                    if d: result["us"]["soybean_oil"] = d
                elif "soybean" in sn_lower:
                    d = extract_commodity(wb, sheet_name, info["header_row"], "soybeans", "Soybeans")
                    if d: result["us"]["soybeans"] = d
                elif "wheat" in sn_lower:
                    d = extract_commodity(wb, sheet_name, info["header_row"], "wheat", "Wheat")
                    if d: result["us"]["wheat"] = d
    
    # If we didn't get all commodities, try individual sources
    missing = [c for c in ["corn", "soybeans", "wheat", "soybean_meal", "soybean_oil"] if c not in result["us"]]
    
    if missing:
        print(f"\n-- Attempt 2: ERS individual data products (missing: {missing}) --")
        
        url_map = {
            "corn": CORN_URLS,
            "soybeans": SOY_URLS,
            "soybean_meal": SOY_URLS,
            "soybean_oil": SOY_URLS,
            "wheat": WHEAT_URLS,
        }
        
        for comm_id in missing:
            urls = url_map.get(comm_id, [])
            if not urls:
                continue
            print(f"\n  Fetching {comm_id}:")
            data, url = try_urls(urls)
            if data:
                wb, sheet_info = parse_excel_generic(data)
                if wb and sheet_info:
                    result["sources"].append(url)
                    for sheet_name, info in sheet_info.items():
                        d = extract_commodity(wb, sheet_name, info["header_row"], comm_id, comm_id.replace("_", " ").title())
                        if d:
                            result["us"][comm_id] = d
                            break
    
    # Summary
    print(f"\n{'=' * 60}")
    print(f"Results: {len(result['us'])} commodities parsed")
    for comm_id, data in result["us"].items():
        print(f"  {comm_id}: {len(data['years'])} years, {sum(len(s['rows']) for s in data['sections'])} rows")
    
    if not result["us"]:
        print("\nWARNING: No data was parsed. The dashboard will use representative data.")
        print("This likely means USDA has changed their download URLs.")
        print("Check https://www.ers.usda.gov/data-products/ for current links.")
    
    # Write output
    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(result, f)
    
    print(f"  Wrote {os.path.getsize(output_file):,} bytes")
    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
