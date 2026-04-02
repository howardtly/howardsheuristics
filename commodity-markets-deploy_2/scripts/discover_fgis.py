#!/usr/bin/env python3
"""Download and examine the FGIS export inspection CSV format."""
import csv
import io
from urllib.request import urlopen, Request

URL = "https://fgisonline.ams.usda.gov/ExportGrainReport/CY2026.csv"

print(f"Fetching {URL}...")
req = Request(URL)
req.add_header("User-Agent", "HowardsHeuristics/1.0")
resp = urlopen(req, timeout=30)
raw = resp.read().decode("utf-8", errors="replace")

print(f"\nTotal size: {len(raw):,} bytes")
print(f"Total lines: {raw.count(chr(10))}")

# Show first 30 lines raw
lines = raw.split("\n")
print("\n--- First 30 raw lines ---")
for i, line in enumerate(lines[:30]):
    print(f"  {i}: {line[:200]}")

# Try parsing as CSV
print("\n--- CSV parse attempt ---")
reader = csv.reader(io.StringIO(raw))
headers = None
for i, row in enumerate(reader):
    if i == 0:
        headers = row
        print(f"  Headers ({len(row)} columns): {row}")
    elif i <= 10:
        print(f"  Row {i}: {row[:10]}")
    else:
        break

# Show unique values in key columns
if headers:
    print("\n--- Unique values in first few columns (from first 500 rows) ---")
    reader2 = csv.reader(io.StringIO(raw))
    next(reader2)  # skip header
    col_vals = {i: set() for i in range(min(len(headers), 8))}
    for i, row in enumerate(reader2):
        if i > 500:
            break
        for j in range(min(len(row), 8)):
            col_vals[j].add(row[j][:50])
    for j in col_vals:
        vals = sorted(col_vals[j])
        print(f"  Col {j} ({headers[j] if j < len(headers) else '?'}): {vals[:20]}")
        if len(vals) > 20:
            print(f"    ... and {len(vals)-20} more")
