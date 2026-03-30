#!/usr/bin/env python3
"""
Diagnostic: find where crude oil and natural gas positions went in 2024 CFTC files.
Searches both disaggregated-combined and legacy-combined reports.
Run this as a one-off GitHub Action or locally.
"""
import urllib.request, zipfile, io, csv, sys

def download(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.read()
    except Exception as e:
        print(f"  Failed: {e}")
        return None

def search_file(data, label):
    """Search a CFTC zip for rows with large energy positions."""
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        csv_name = zf.namelist()[0]
        csv_data = zf.read(csv_name).decode("utf-8", errors="replace")
        lines = csv_data.strip().split("\n")
        lines[0] = ",".join(h.strip() for h in lines[0].split(","))

    reader = csv.DictReader(lines)
    cols = reader.fieldnames
    print(f"\n=== {label} ({len(lines)-1} rows) ===")
    
    # Try various column names for market and positions
    results = {}
    for row in reader:
        market = (row.get("Market_and_Exchange_Names") or row.get("Market and Exchange Names") or "").strip()
        name_up = market.upper()
        
        # Only look at energy
        if not any(kw in name_up for kw in ["OIL", "GAS", "CRUDE", "HENRY", "NYMEX", "WTI"]):
            continue
        
        commodity = market.split(" - ")[0].strip()
        
        # Try to get managed money / noncommercial long
        mm_long = 0
        for col in ["M_Money_Positions_Long_All", "NonComm_Positions_Long_All"]:
            try: mm_long = max(mm_long, int(row.get(col, 0) or 0))
            except: pass
        
        oi = 0
        for col in ["Open_Interest_All", "Open_Interest_All "]:
            try: oi = max(oi, int(row.get(col, 0) or 0))
            except: pass
        
        if commodity not in results or oi > results[commodity]["max_oi"]:
            results[commodity] = {"max_oi": oi, "max_mm_long": mm_long, "count": 0}
        results[commodity]["count"] += 1
        results[commodity]["max_mm_long"] = max(results[commodity]["max_mm_long"], mm_long)
        results[commodity]["max_oi"] = max(results[commodity]["max_oi"], oi)

    # Sort by OI descending and show top entries
    sorted_results = sorted(results.items(), key=lambda x: -x[1]["max_oi"])
    print(f"  Energy commodities found ({len(sorted_results)}):")
    print(f"  {'Commodity':<50} {'Rows':>5} {'Max OI':>12} {'Max MM Long':>12}")
    print(f"  {'-'*50} {'-'*5} {'-'*12} {'-'*12}")
    for name, info in sorted_results[:30]:
        print(f"  {name:<50} {info['count']:>5} {info['max_oi']:>12,} {info['max_mm_long']:>12,}")

# URLs to try
year = 2024
urls = [
    (f"https://www.cftc.gov/files/dea/history/com_disagg_txt_{year}.zip", "Disaggregated Combined"),
    (f"https://www.cftc.gov/files/dea/history/fut_disagg_txt_{year}.zip", "Disaggregated Futures-Only"),
    (f"https://www.cftc.gov/files/dea/history/fin_com_{year}.zip", "Financial Combined"),
    (f"https://www.cftc.gov/files/dea/history/fin_fut_txt_{year}.zip", "Financial Futures-Only"),
    (f"https://www.cftc.gov/files/dea/history/deacom{year}.zip", "Legacy Combined"),
    (f"https://www.cftc.gov/files/dea/history/deafut{year}.zip", "Legacy Futures-Only"),
]

for url, label in urls:
    print(f"\nDownloading {label}...")
    print(f"  URL: {url}")
    data = download(url)
    if data:
        print(f"  Size: {len(data):,} bytes")
        search_file(data, label)
    else:
        print(f"  Skipped")
