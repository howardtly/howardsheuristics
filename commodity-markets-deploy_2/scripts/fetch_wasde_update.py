#!/usr/bin/env python3
"""
Fetch and parse the monthly WASDE Excel file to update U.S. balance sheets.
Downloads from: https://esmis.nal.usda.gov/sites/default/release-files/wasde{MM}{YY}.xls
Overlays current/next marketing year data onto existing wasde.json.

The WASDE XLS has these pages of interest:
  Page 11 (Sheet 4): U.S. Wheat — cols c4, c6, c9, c11 (prior yr, current yr est, next yr Feb, next yr Mar)
  Page 12 (Sheet 5): U.S. Corn — cols c1-c4 (prior yr, current yr est, next yr Feb, next yr Mar)
  Page 15 (Sheet 8): U.S. Soybeans/Oil/Meal — cols c1-c4 same structure
"""

import json, os, sys, urllib.request, urllib.error, tempfile
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

WASDE_URL_TEMPLATE = "https://www.usda.gov/oce/commodity/wasde/wasde{mm}{yy}.xls"


def download_wasde(month, year):
    """Download WASDE XLS for given month/year. Returns path to temp file or None."""
    mm = f"{month:02d}"
    yy = f"{year % 100:02d}"
    url = WASDE_URL_TEMPLATE.format(mm=mm, yy=yy)
    print(f"Downloading: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            tmp = os.path.join(tempfile.gettempdir(), f"wasde{mm}{yy}.xls")
            with open(tmp, "wb") as f:
                f.write(data)
            print(f"  Downloaded: {len(data):,} bytes")
            return tmp
    except Exception as e:
        print(f"  Download failed: {e}")
        return None


def to_float(v):
    """Convert cell value to float, return None if not numeric."""
    if v is None or v == "" or v == "Filler" or v == "filler":
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def ri(v):
    """Round to integer."""
    if v is None: return None
    return round(v)

def r1(v):
    """Round to 1 decimal."""
    if v is None: return None
    return round(v, 1)

def pct(es, tu):
    if es is not None and tu is not None and tu != 0:
        return round(es / tu * 100, 1)
    return None


def parse_corn(wb):
    """Parse Page 12 for U.S. corn data. Returns dict with marketing years as keys."""
    import xlrd
    ws = wb.sheet_by_name("Page 12")

    # Find CORN section (starts after FEED GRAINS)
    corn_start = None
    for r in range(ws.nrows):
        v = str(ws.cell_value(r, 0)).strip()
        if v == "CORN":
            corn_start = r
            break
    if corn_start is None:
        print("  ERROR: CORN section not found in Page 12")
        return None

    # Header row has year labels
    # c1=2023/24, c2=2024/25 Est., c3=2025/26 Proj., c4=2025/26 Proj.
    # The rightmost column (c4) is the latest month's projection
    header = [str(ws.cell_value(corn_start, c)).strip() for c in range(ws.ncols)]
    print(f"  Corn header: {header}")

    # Extract year labels from header
    year_cols = {}  # {marketing_year_label: col_index}
    for c in range(1, ws.ncols):
        h = header[c]
        if "/" in h and len(h) >= 6:
            # e.g. "2023/24" or "2024/25 Est." or "2025/26 Proj."
            my = h[:7]  # "2023/24" or "2024/2"
            if not my.endswith("/"):
                year_cols[my] = c

    # For projected year, use the rightmost column (latest month)
    # The two projection columns share the same year label — we want the last one
    for c in range(ws.ncols - 1, 0, -1):
        h = header[c]
        if "Proj." in h or "proj" in h.lower():
            my = h.split(" ")[0][:7]
            year_cols[my] = c  # overwrite with rightmost
            break

    print(f"  Year columns: {year_cols}")

    # Parse data rows
    data = {}
    for r in range(corn_start + 1, ws.nrows):
        label = str(ws.cell_value(r, 0)).strip()
        if not label or label.startswith("Note") or label == "Total":
            continue
        # Skip unit/filler rows
        if label in ("Filler", "filler") or "Million" in label or "Bushels" in label:
            continue

        for my_label, col in year_cols.items():
            if my_label not in data:
                data[my_label] = {}
            v = to_float(ws.cell_value(r, col))
            if v is not None:
                data[my_label][label] = v

    print(f"  Corn: {len(data)} marketing years")
    for my, vals in data.items():
        print(f"    {my}: {list(vals.keys())[:5]}...")
    return data


def build_corn_rows(wasde_data, my_label):
    """Build corn balance sheet rows from WASDE data for a single marketing year."""
    d = wasde_data.get(my_label, {})
    if not d:
        return None

    area_planted = r1(d.get("Area Planted"))
    area_harvested = r1(d.get("Area Harvested"))
    yield_val = r1(d.get("Yield per Harvested Acre"))
    beg_stocks = ri(d.get("Beginning Stocks"))
    production = ri(d.get("Production"))
    imports_val = ri(d.get("Imports"))
    supply = ri(d.get("    Supply, Total", d.get("Supply, Total")))
    feed_residual = ri(d.get("Feed and Residual"))
    fsi = ri(d.get("Food, Seed & Industrial 2/", d.get("Food, Seed & Industrial")))
    ethanol = ri(d.get("   Ethanol & by-products 3/", d.get("Ethanol & by-products 3/")))
    # Seed: FSI includes seed in WASDE, but we need to back out seed separately
    # WASDE doesn't break out seed from FSI — we'll keep our ERS seed value
    domestic = ri(d.get("    Domestic, Total", d.get("Domestic, Total")))
    exports = ri(d.get("Exports"))
    use_total = ri(d.get("    Use, Total", d.get("Use, Total")))
    ending_stocks = ri(d.get("Ending Stocks"))
    price = d.get("Avg. Farm Price ($/bu)  4/", d.get("Avg. Farm Price ($/bu)"))

    return {
        "Area planted": area_planted,
        "Area harvested": area_harvested,
        "Yield per harvested acre": yield_val,
        "Beginning stocks": beg_stocks,
        "Production": production,
        "Imports": imports_val,
        "Total supply": supply,
        "Feed and residual": feed_residual,
        "Food, seed & industrial": fsi,
        "Ethanol": ethanol,
        "Total domestic use": domestic,
        "Exports": exports,
        "Total usage": use_total,
        "Ending stocks": ending_stocks,
        "Avg. farm price ($/bu)": price,
    }


def parse_wheat(wb):
    """Parse Page 11 for U.S. wheat data. Different column layout: c4, c6, c9, c11."""
    import xlrd
    ws = wb.sheet_by_name("Page 11")

    # Header at R8: c4=2023/24, c6=2024/25 Est., c9=2025/26 Proj., c11=2025/26 Proj.
    # R9: c9=Feb, c11=Mar
    # Data cols: prior year=c4, current year=c6, projected=c11 (latest month)
    header_row = 8
    year_cols = {}

    for c in [4, 6, 9, 11]:
        h = str(ws.cell_value(header_row, c)).strip()
        if "/" in h and len(h) >= 6:
            my = h[:7]
            year_cols[my] = c  # rightmost wins for projected year

    print(f"  Wheat year columns: {year_cols}")

    # Parse data rows (R11 to ~R27)
    data = {}
    for r in range(11, 28):
        label = str(ws.cell_value(r, 0)).strip()
        if not label or label.startswith("Note") or "Million" in label or "Bushels" in label:
            continue

        for my_label, col in year_cols.items():
            if my_label not in data:
                data[my_label] = {}
            v = to_float(ws.cell_value(r, col))
            if v is not None:
                data[my_label][label] = v

    print(f"  Wheat: {len(data)} marketing years")
    for my, vals in data.items():
        print(f"    {my}: {list(vals.keys())[:5]}...")
    return data


def build_wheat_rows(wasde_data, my_label):
    d = wasde_data.get(my_label, {})
    if not d: return None

    return {
        "Area planted": r1(d.get("Area Planted")),
        "Area harvested": r1(d.get("Area Harvested")),
        "Yield per harvested acre": r1(d.get("Yield per Harvested Acre")),
        "Beginning stocks": ri(d.get("Beginning Stocks")),
        "Production": ri(d.get("Production")),
        "Imports": ri(d.get("Imports")),
        "Total supply": ri(d.get("  Supply, Total", d.get("Supply, Total"))),
        "Food": ri(d.get("Food")),
        "Seed": ri(d.get("Seed")),
        "Feed and residual": ri(d.get("Feed and Residual")),
        "Total domestic use": ri(d.get("  Domestic, Total", d.get("Domestic, Total"))),
        "Exports": ri(d.get("Exports")),
        "Total usage": ri(d.get("  Use, Total", d.get("Use, Total"))),
        "Ending stocks": ri(d.get("Ending Stocks")),
        "Avg. farm price ($/bu)": d.get("Avg. Farm Price ($/bu)  2/", d.get("Avg. Farm Price ($/bu)")),
    }


def parse_soybeans(wb):
    """Parse Page 15 SOYBEANS section."""
    import xlrd
    ws = wb.sheet_by_name("Page 15")

    # Header at R8: c1=2023/24, c2=2024/25 Est., c3=2025/26 Proj., c4=2025/26 Proj.
    header = [str(ws.cell_value(8, c)).strip() for c in range(ws.ncols)]
    year_cols = {}
    for c in range(1, ws.ncols):
        h = header[c]
        if "/" in h and len(h) >= 6:
            my = h[:7]
            year_cols[my] = c

    # For projected year, use rightmost
    for c in range(ws.ncols - 1, 0, -1):
        h = header[c]
        if "Proj." in h:
            my = h.split(" ")[0][:7]
            year_cols[my] = c
            break

    print(f"  Soybean year columns: {year_cols}")

    # Parse rows R12-R27
    data = {}
    for r in range(12, 28):
        label = str(ws.cell_value(r, 0)).strip()
        if not label or label in ("Filler", "Total") or "Million" in label or "Bushels" in label:
            continue
        for my_label, col in year_cols.items():
            if my_label not in data:
                data[my_label] = {}
            v = to_float(ws.cell_value(r, col))
            if v is not None:
                data[my_label][label] = v

    print(f"  Soybeans: {len(data)} marketing years")
    return data


def build_soybean_rows(wasde_data, my_label):
    d = wasde_data.get(my_label, {})
    if not d: return None

    crush = ri(d.get("Crushings"))
    seed = ri(d.get("Seed"))
    residual = ri(d.get("Residual"))
    exports = ri(d.get("Exports"))

    return {
        "Area planted": r1(d.get("Area Planted")),
        "Area harvested": r1(d.get("Area Harvested")),
        "Yield per harvested acre": r1(d.get("Yield per Harvested Acre")),
        "Beginning stocks": ri(d.get("Beginning Stocks")),
        "Production": ri(d.get("Production")),
        "Imports": ri(d.get("Imports")),
        "Total supply": ri(d.get("    Supply, Total", d.get("Supply, Total"))),
        "Crush": crush,
        "Seed": seed,
        "Feed and residual": residual,
        "Total domestic use": ri((crush or 0) + (seed or 0) + (residual or 0)) if crush else None,
        "Exports": exports,
        "Total usage": ri(d.get("    Use, Total", d.get("Use, Total"))),
        "Ending stocks": ri(d.get("Ending Stocks")),
        "Avg. farm price ($/bu)": d.get("Avg. Farm Price ($/bu)  2/"),
    }


def parse_soyoil(wb):
    """Parse Page 15 SOYBEAN OIL section."""
    import xlrd
    ws = wb.sheet_by_name("Page 15")

    # Find SOYBEAN OIL header row
    oil_start = None
    for r in range(ws.nrows):
        if str(ws.cell_value(r, 0)).strip() == "SOYBEAN OIL":
            oil_start = r
            break
    if oil_start is None:
        print("  ERROR: SOYBEAN OIL not found")
        return None

    header = [str(ws.cell_value(oil_start, c)).strip() for c in range(ws.ncols)]
    year_cols = {}
    for c in range(1, ws.ncols):
        h = header[c]
        if "/" in h and len(h) >= 6:
            my = h[:7]
            year_cols[my] = c
    for c in range(ws.ncols - 1, 0, -1):
        h = header[c]
        if "Proj." in h:
            my = h.split(" ")[0][:7]
            year_cols[my] = c
            break

    print(f"  Soy oil year columns: {year_cols}")

    data = {}
    for r in range(oil_start + 1, oil_start + 16):
        label = str(ws.cell_value(r, 0)).strip()
        if not label or label in ("Filler", "Total") or "Million" in label:
            continue
        for my_label, col in year_cols.items():
            if my_label not in data:
                data[my_label] = {}
            v = to_float(ws.cell_value(r, col))
            if v is not None:
                data[my_label][label] = v

    print(f"  Soy oil: {len(data)} marketing years")
    return data


def build_soyoil_rows(wasde_data, my_label):
    d = wasde_data.get(my_label, {})
    if not d: return None

    return {
        "Beginning stocks": ri(d.get("Beginning Stocks")),
        "Production": ri(d.get("Production 4/", d.get("Production"))),
        "Imports": ri(d.get("Imports")),
        "Total supply": ri(d.get("    Supply, Total", d.get("Supply, Total"))),
        "Domestic total": ri(d.get("Domestic Disappearance")),
        "Biofuel": ri(d.get("     Biofuel 3/", d.get("Biofuel 3/"))),
        "Food, feed, and other industrial": ri(d.get("     Food, Feed & other Industrial", d.get("Food, Feed & other Industrial"))),
        "Exports": ri(d.get("Exports")),
        "Total usage": ri(d.get("     Use, Total", d.get("Use, Total"))),
        "Ending stocks": ri(d.get("Ending stocks", d.get("Ending Stocks"))),
    }


def parse_soymeal(wb):
    """Parse Page 15 SOYBEAN MEAL section."""
    import xlrd
    ws = wb.sheet_by_name("Page 15")

    meal_start = None
    for r in range(ws.nrows):
        if str(ws.cell_value(r, 0)).strip() == "SOYBEAN MEAL":
            meal_start = r
            break
    if meal_start is None:
        print("  ERROR: SOYBEAN MEAL not found")
        return None

    header = [str(ws.cell_value(meal_start, c)).strip() for c in range(ws.ncols)]
    year_cols = {}
    for c in range(1, ws.ncols):
        h = header[c]
        if "/" in h and len(h) >= 6:
            my = h[:7]
            year_cols[my] = c
    for c in range(ws.ncols - 1, 0, -1):
        h = header[c]
        if "Proj." in h:
            my = h.split(" ")[0][:7]
            year_cols[my] = c
            break

    print(f"  Soy meal year columns: {year_cols}")

    data = {}
    for r in range(meal_start + 1, meal_start + 14):
        label = str(ws.cell_value(r, 0)).strip()
        if not label or label in ("Filler", "Total") or "Thousand" in label or "Tons" in label:
            continue
        for my_label, col in year_cols.items():
            if my_label not in data:
                data[my_label] = {}
            v = to_float(ws.cell_value(r, col))
            if v is not None:
                data[my_label][label] = v

    print(f"  Soy meal: {len(data)} marketing years")
    return data


def build_soymeal_rows(wasde_data, my_label):
    d = wasde_data.get(my_label, {})
    if not d: return None

    return {
        "Beginning stocks": ri(d.get("Beginning Stocks")),
        "Production": ri(d.get("Production 4/", d.get("Production"))),
        "Imports": ri(d.get("Imports")),
        "Total supply": ri(d.get("    Supply, Total", d.get("Supply, Total"))),
        "Domestic use": ri(d.get("Domestic Disappearance")),
        "Exports": ri(d.get("Exports")),
        "Total usage": ri(d.get("    Use, Total", d.get("Use, Total"))),
        "Ending stocks": ri(d.get("Ending Stocks")),
    }


def overlay_wasde_on_us(existing_us, commodity_id, wasde_rows_by_year):
    """Overlay WASDE data onto existing US balance sheet for a commodity.
    wasde_rows_by_year: {marketing_year_label: {row_label: value}}
    """
    if commodity_id not in existing_us:
        print(f"  {commodity_id} not in existing US data — skipping")
        return

    commodity = existing_us[commodity_id]
    years = commodity.get("years", [])
    sections = commodity.get("sections", [])

    updated_count = 0
    for my_label, wasde_vals in wasde_rows_by_year.items():
        if not wasde_vals:
            continue

        # Find the column index for this marketing year
        # WASDE uses "2023/24" format, existing uses "2023/24" format
        if my_label in years:
            col_idx = years.index(my_label)
        else:
            # New year — append
            years.append(my_label)
            col_idx = len(years) - 1
            # Extend all existing rows with None
            for section in sections:
                for row in section.get("rows", []):
                    while len(row.get("values", [])) < len(years):
                        row["values"].append(None)
            print(f"  Added new year column: {my_label}")

        # Match WASDE values to existing rows by label (case-insensitive)
        for section in sections:
            for row in section.get("rows", []):
                row_label = row.get("label", "")
                # Try to match
                for wasde_label, wasde_val in wasde_vals.items():
                    if wasde_val is None:
                        continue
                    if row_label.lower().strip() == wasde_label.lower().strip():
                        # Ensure values array is long enough
                        while len(row["values"]) <= col_idx:
                            row["values"].append(None)
                        old_val = row["values"][col_idx]
                        row["values"][col_idx] = wasde_val
                        if old_val != wasde_val:
                            updated_count += 1
                        break

        # Recalculate stocks/use if present
        for section in sections:
            es_row = next((r for r in section["rows"] if "stocks/use" in r["label"].lower()), None)
            ending_row = next((r for r in section["rows"] if r["label"].lower().strip() == "ending stocks"), None)
            usage_row = next((r for r in section["rows"] if r["label"].lower().strip() == "total usage"), None)
            if es_row and ending_row and usage_row:
                while len(es_row["values"]) <= col_idx:
                    es_row["values"].append(None)
                es = ending_row["values"][col_idx] if col_idx < len(ending_row["values"]) else None
                tu = usage_row["values"][col_idx] if col_idx < len(usage_row["values"]) else None
                es_row["values"][col_idx] = pct(es, tu)

    commodity["years"] = years
    print(f"  {commodity_id}: {updated_count} values updated across {len(wasde_rows_by_year)} years")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "wasde.json")

    # Load existing data
    existing = {}
    if os.path.exists(output_file):
        try:
            with open(output_file) as f:
                existing = json.load(f)
            print(f"Loaded existing: us={list(existing.get('us', {}).keys())}")
        except:
            pass

    if "us" not in existing:
        print("ERROR: No existing US data in wasde.json. Run fetch_wasde.py first.")
        return 1

    # Determine which WASDE to fetch
    now = datetime.utcnow()
    month = now.month
    year = now.year
    # Allow override via env vars
    month = int(os.environ.get("WASDE_MONTH", month))
    year = int(os.environ.get("WASDE_YEAR", year))

    print("=" * 60)
    print(f"WASDE Update: {month:02d}/{year}")
    print(f"Time: {now.isoformat()}Z")
    print("=" * 60)

    # Download
    xls_path = download_wasde(month, year)
    if not xls_path:
        # Try previous month
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        print(f"  Trying previous month: {prev_month:02d}/{prev_year}")
        xls_path = download_wasde(prev_month, prev_year)
        if not xls_path:
            print("ERROR: Could not download WASDE")
            return 1

    import xlrd
    wb = xlrd.open_workbook(xls_path)
    print(f"  Opened: {wb.nsheets} sheets")

    # Parse all commodities
    print("\n-- Parsing CORN (Page 12) --")
    corn_data = parse_corn(wb)

    print("\n-- Parsing WHEAT (Page 11) --")
    wheat_data = parse_wheat(wb)

    print("\n-- Parsing SOYBEANS (Page 15) --")
    soy_data = parse_soybeans(wb)

    print("\n-- Parsing SOYBEAN OIL (Page 15) --")
    soyoil_data = parse_soyoil(wb)

    print("\n-- Parsing SOYBEAN MEAL (Page 15) --")
    soymeal_data = parse_soymeal(wb)

    # Build WASDE rows for each commodity and year
    print("\n-- Building WASDE overlay --")

    corn_overlay = {}
    if corn_data:
        for my in corn_data:
            rows = build_corn_rows(corn_data, my)
            if rows:
                corn_overlay[my] = rows
                print(f"  Corn {my}: {len([v for v in rows.values() if v is not None])} values")

    wheat_overlay = {}
    if wheat_data:
        for my in wheat_data:
            rows = build_wheat_rows(wheat_data, my)
            if rows:
                wheat_overlay[my] = rows
                print(f"  Wheat {my}: {len([v for v in rows.values() if v is not None])} values")

    soy_overlay = {}
    if soy_data:
        for my in soy_data:
            rows = build_soybean_rows(soy_data, my)
            if rows:
                soy_overlay[my] = rows
                print(f"  Soybeans {my}: {len([v for v in rows.values() if v is not None])} values")

    soyoil_overlay = {}
    if soyoil_data:
        for my in soyoil_data:
            rows = build_soyoil_rows(soyoil_data, my)
            if rows:
                soyoil_overlay[my] = rows
                print(f"  Soy oil {my}: {len([v for v in rows.values() if v is not None])} values")

    soymeal_overlay = {}
    if soymeal_data:
        for my in soymeal_data:
            rows = build_soymeal_rows(soymeal_data, my)
            if rows:
                soymeal_overlay[my] = rows
                print(f"  Soy meal {my}: {len([v for v in rows.values() if v is not None])} values")

    # Apply overlays
    print("\n-- Applying overlays to wasde.json --")
    us = existing["us"]
    overlay_wasde_on_us(us, "corn", corn_overlay)
    overlay_wasde_on_us(us, "wheat", wheat_overlay)
    overlay_wasde_on_us(us, "soybeans", soy_overlay)
    overlay_wasde_on_us(us, "soybean_oil", soyoil_overlay)
    overlay_wasde_on_us(us, "soybean_meal", soymeal_overlay)

    # Save
    existing["wasde_updated_at"] = now.isoformat() + "Z"
    existing["wasde_month"] = f"{month:02d}/{year}"

    print(f"\nWriting {output_file}")
    with open(output_file, "w") as f:
        json.dump(existing, f)
    print(f"  {os.path.getsize(output_file):,} bytes")

    # Cleanup
    try:
        os.remove(xls_path)
    except:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
