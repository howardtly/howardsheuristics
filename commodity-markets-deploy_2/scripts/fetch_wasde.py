#!/usr/bin/env python3
"""
Debug script: dump first rows of each sheet from USDA ERS workbooks.
This helps us see the exact labels and format so we can build the right parser.
"""

import os
import sys
import urllib.request
import zipfile
from io import BytesIO

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

CORN_URL = "https://www.ers.usda.gov/media/5764/feed-grains-yearbook-tables-all-years.xlsx?v=77939"
OILCROPS_URL = "https://www.ers.usda.gov/media/5219/all-tables-oil-crops-yearbook-complete-data-set-in-compressed-zip-file.zip?v=11593"
WHEAT_URL = "https://www.ers.usda.gov/media/5706/wheat-data-all-years.xlsx?v=53976"


def fetch(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except Exception as e:
        print(f"  FAILED: {e}")
        return None


def dump_workbook(data, label):
    import openpyxl
    try:
        wb = openpyxl.load_workbook(BytesIO(data), read_only=True, data_only=True)
    except Exception as e:
        print(f"  openpyxl failed: {e}")
        return

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  Sheets: {wb.sheetnames}")
    print(f"{'='*60}")

    for sn in wb.sheetnames:
        if sn.lower() == "contents":
            continue
        ws = wb[sn]
        rows = list(ws.iter_rows(values_only=True))
        print(f"\n--- Sheet: '{sn}' ({len(rows)} rows) ---")
        for i, row in enumerate(rows[:8]):
            if row:
                cells = [str(c)[:35] if c is not None else "" for c in row[:10]]
                print(f"  Row {i}: {cells}")


def main():
    import openpyxl

    # CORN
    print("\n** CORN **")
    data = fetch(CORN_URL)
    if data:
        dump_workbook(data, "Feed Grains Yearbook")

    # SOY (just Soy.xlsx from zip)
    print("\n\n** OIL CROPS **")
    data = fetch(OILCROPS_URL)
    if data:
        zf = zipfile.ZipFile(BytesIO(data))
        for fname in ["Soy.xlsx", "OilCropsAllTables.xlsx"]:
            if fname in zf.namelist():
                print(f"\n  --- From ZIP: {fname} ---")
                dump_workbook(zf.read(fname), fname)

    # WHEAT - skip since openpyxl can't open it
    print("\n\n** WHEAT **")
    print("  (openpyxl can't open this file - needs pandas+calamine)")
    data = fetch(WHEAT_URL)
    if data:
        try:
            import pandas as pd
            xls = pd.ExcelFile(BytesIO(data), engine="calamine")
            print(f"  Sheets: {xls.sheet_names}")
            for sn in xls.sheet_names[:10]:
                if sn.lower() == "contents":
                    continue
                df = pd.read_excel(xls, sheet_name=sn, header=None)
                print(f"\n--- Sheet: '{sn}' ({len(df)} rows) ---")
                for i in range(min(8, len(df))):
                    cells = [str(c)[:35] if pd.notna(c) else "" for c in df.iloc[i, :10]]
                    print(f"  Row {i}: {cells}")
        except ImportError:
            print("  pandas not installed")
        except Exception as e:
            print(f"  Error: {e}")


if __name__ == "__main__":
    main()
