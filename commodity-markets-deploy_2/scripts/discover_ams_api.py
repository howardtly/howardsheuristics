#!/usr/bin/env python3
"""Request specific sections with date filter to get actual price data."""
import json, os, sys, urllib.request, urllib.error, urllib.parse

API_KEY = os.environ.get("AMS_API_KEY", "")
BASE = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"

def fetch_raw(url):
    headers = {"Authorization": API_KEY, "Accept": "application/json"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(f"  ERR: {e}")
        return None

print("=" * 60)
print("Section + Date Filter Combos")
print("=" * 60)

# BEEF 2453: try each section with date filter
BEEF_SECTIONS = [
    "Current Cutout Values",
    "Composite Primal Values", 
    "Choice Cuts",
    "Current Volume",
    "Beef Trimmings",
]

for section in BEEF_SECTIONS:
    enc_section = urllib.parse.quote(section)
    url = f"{BASE}/2453?q=report_date=04/09/2026&sections={enc_section}"
    print(f"\n--- Beef: {section} ---")
    print(f"  {url[:120]}")
    raw = fetch_raw(url)
    if raw:
        print(f"  {len(raw)} bytes")
        try:
            j = json.loads(raw)
            results = j.get("results", [])
            if results:
                rec = results[0]
                # Print ALL non-null keys
                for k, v in rec.items():
                    if v is not None and str(v).strip():
                        print(f"    {k:35s} = {str(v)[:80]}")
        except:
            print(f"  {raw[:500]}")

# PORK 2498: try key sections
PORK_SECTIONS = [
    "Cutout and Primal Values",
    "Loin Cuts",
    "Belly Cuts",
    "Current Volume",
]

for section in PORK_SECTIONS:
    enc_section = urllib.parse.quote(section)
    url = f"{BASE}/2498?q=report_date=04/09/2026&sections={enc_section}"
    print(f"\n--- Pork: {section} ---")
    raw = fetch_raw(url)
    if raw:
        print(f"  {len(raw)} bytes")
        try:
            j = json.loads(raw)
            results = j.get("results", [])
            if results:
                rec = results[0]
                for k, v in rec.items():
                    if v is not None and str(v).strip():
                        print(f"    {k:35s} = {str(v)[:80]}")
        except:
            print(f"  {raw[:500]}")

# BEEF WEEKLY 2465: try Cuts section with date (this report had loads data)
print(f"\n--- Beef Weekly 2465: Cuts section ---")
url = f"{BASE}/2465?q=report_date=04/06/2026&sections={urllib.parse.quote('Cuts')}"
raw = fetch_raw(url)
if raw:
    print(f"  {len(raw)} bytes")
    try:
        j = json.loads(raw)
        results = j.get("results", [])
        print(f"  {len(results)} records")
        if results:
            for k, v in results[0].items():
                if v is not None and str(v).strip():
                    print(f"    {k:35s} = {str(v)[:80]}")
            if len(results) > 1:
                print(f"\n  Record 2:")
                for k, v in results[1].items():
                    if v is not None and str(v).strip():
                        print(f"    {k:35s} = {str(v)[:80]}")
    except:
        print(raw[:1000])

# Also try: maybe we need allSections=true
print(f"\n\n--- Beef 2453: allSections=true ---")
url = f"{BASE}/2453?q=report_date=04/09/2026&allSections=true"
raw = fetch_raw(url)
if raw:
    print(f"  {len(raw)} bytes")
    try:
        j = json.loads(raw)
        results = j.get("results", [])
        print(f"  {len(results)} records")
        if results:
            # Print all records since different sections may have different fields
            for i, rec in enumerate(results[:15]):
                non_meta = {k: v for k, v in rec.items() 
                           if v is not None and str(v).strip() 
                           and k not in ("report_title","slug_name","slug_id","office_name","office_code",
                                        "office_city","office_state","market_location_name","market_location_city",
                                        "market_location_state","market_type","market_type_category","is_correction","narrative")}
                print(f"  [{i}] {json.dumps(non_meta, default=str)[:250]}")
    except:
        print(raw[:2000])
