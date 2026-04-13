#!/usr/bin/env python3
"""Check LM_XB401 (report 2451) structure for 90% trim data."""
import json, os, sys, urllib.request, urllib.error

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
print("Report 2451 (LM_XB401) — Boneless Processing Beef/Trimmings PM")
print("=" * 60)

# Get single date with all sections
url = f"{BASE}/2451?q=report_date=04/09/2026&allSections=true"
print(f"\n  {url[:100]}...")
raw = fetch_raw(url)
if raw:
    print(f"  {len(raw)} bytes")
    data = json.loads(raw)
    
    SKIP = {"report_title","slug_name","slug_id","office_name","office_code",
            "office_city","office_state","market_location_name","market_location_city",
            "market_location_state","market_type","market_type_category","is_correction",
            "narrative","trend","published_date","report_date"}
    
    if isinstance(data, list):
        for block in data:
            section = block.get("reportSection", "?")
            results = block.get("results", [])
            if not results: continue
            print(f"\n  --- {section} ({len(results)} records) ---")
            for i, rec in enumerate(results[:20]):
                fields = {k: v for k, v in rec.items() if v is not None and str(v).strip() and k not in SKIP}
                print(f"    [{i}] {json.dumps(fields, default=str)[:200]}")
    elif isinstance(data, dict):
        section = data.get("reportSection", "?")
        results = data.get("results", [])
        print(f"\n  --- {section} ({len(results)} records) ---")
        for i, rec in enumerate(results[:10]):
            fields = {k: v for k, v in rec.items() if v is not None and str(v).strip() and k not in SKIP}
            print(f"    [{i}] {json.dumps(fields, default=str)[:200]}")
