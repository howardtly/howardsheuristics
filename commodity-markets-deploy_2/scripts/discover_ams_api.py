#!/usr/bin/env python3
"""Map all section fields using allSections=true."""
import json, os, sys, urllib.request, urllib.error

API_KEY = os.environ.get("AMS_API_KEY", "")
BASE = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"

def fetch_json(url):
    headers = {"Authorization": API_KEY, "Accept": "application/json"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERR: {e}")
        return None

SKIP_FIELDS = {"report_title","slug_name","slug_id","office_name","office_code",
               "office_city","office_state","market_location_name","market_location_city",
               "market_location_state","market_type","market_type_category","is_correction",
               "narrative","trend","published_date","report_date"}

def show_sections(data, label):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    if not isinstance(data, list):
        data = [data]
    for block in data:
        section = block.get("reportSection", "?")
        results = block.get("results", [])
        if not results: continue
        rec = results[0]
        fields = {k: v for k, v in rec.items() if v is not None and str(v).strip() and k not in SKIP_FIELDS}
        print(f"\n  --- {section} ({len(results)} records) ---")
        for k, v in fields.items():
            print(f"    {k:40s} = {str(v)[:80]}")
        # If many records (cuts), show first 5
        if len(results) > 1:
            print(f"    ... ({len(results)} total records)")
            for rec2 in results[1:min(6, len(results))]:
                f2 = {k: v for k, v in rec2.items() if v is not None and str(v).strip() and k not in SKIP_FIELDS}
                compact = ", ".join(f"{k}={v}" for k, v in list(f2.items())[:8])
                print(f"    [{compact[:150]}]")

print("=" * 60)
print("Full Section Field Map")
print("=" * 60)

# BEEF DAILY PM (2453) — single date
print("\n\nFetching Beef Daily PM 2453...")
data = fetch_json(f"{BASE}/2453?q=report_date=04/09/2026&allSections=true")
if data: show_sections(data, "BEEF DAILY PM (2453) — 04/09/2026")

# PORK DAILY PM (2498) — single date
print("\n\nFetching Pork Daily PM 2498...")
data = fetch_json(f"{BASE}/2498?q=report_date=04/09/2026&allSections=true")
if data: show_sections(data, "PORK DAILY PM (2498) — 04/09/2026")

# BEEF WEEKLY COMP (2465) — single date
print("\n\nFetching Beef Weekly Comp 2465...")
data = fetch_json(f"{BASE}/2465?q=report_date=04/06/2026&allSections=true")
if data: show_sections(data, "BEEF WEEKLY COMP (2465) — 04/06/2026")

# PORK WEEKLY COMP (2680) — single date
print("\n\nFetching Pork Weekly Comp 2680...")
data = fetch_json(f"{BASE}/2680?q=report_date=04/06/2026&allSections=true")
if data: show_sections(data, "PORK WEEKLY COMP (2680) — 04/06/2026")
