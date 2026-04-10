#!/usr/bin/env python3
"""Dig into report section structure for beef/pork + search wider range for poultry."""
import json, os, sys, urllib.request, urllib.error

API_KEY = os.environ.get("AMS_API_KEY", "")
BASE = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"

def fetch(slug, params=""):
    url = f"{BASE}/{slug}" + (f"?{params}" if params else "")
    headers = {"Authorization": API_KEY, "Accept": "application/json"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERR {slug}: {e}")
        return None

print("=" * 60)
print("Deep Dive: Report Sections + Poultry Search")
print("=" * 60)

# === Deep dive into key reports — explore reportSections ===
for rid, label in [("2453", "Beef Daily PM"), ("2465", "Beef Weekly Comp"), 
                    ("2498", "Pork Daily PM"), ("2680", "Pork Weekly Comp")]:
    print(f"\n\n{'='*60}")
    print(f"  REPORT {rid}: {label}")
    print(f"{'='*60}")
    
    data = fetch(rid)
    if not data: continue
    
    # Show reportSections
    sections = data.get("reportSections", [])
    print(f"  Sections: {sections}")
    
    results = data.get("results", [])
    print(f"  Results: {len(results)} records")
    
    if results:
        # Show ALL fields of the first record
        print(f"\n  First record (ALL fields):")
        for k, v in results[0].items():
            print(f"    {k:35s} = {str(v)[:100]}")
        
        # Show next 2 records compactly
        for i, rec in enumerate(results[1:4], 2):
            non_null = {k: v for k, v in rec.items() if v is not None and str(v).strip()}
            print(f"\n  Record {i}: {json.dumps(non_null, default=str)[:250]}")

    # Also try with section filter
    for section in sections[:3]:
        print(f"\n  --- Section: '{section}' ---")
        data2 = fetch(rid, f"sections={section.replace(' ', '%20')}")
        if data2:
            results2 = data2.get("results", [])
            print(f"  {len(results2)} records")
            if results2:
                # Show first record's non-null fields
                for k, v in results2[0].items():
                    if v is not None and str(v).strip():
                        print(f"    {k:35s} = {str(v)[:100]}")

# === Poultry search: wider range 2700-2900, 2900-3100, 3100-3300 ===
print(f"\n\n{'='*60}")
print("  POULTRY SEARCH (ranges 2700-3300)")
print(f"{'='*60}")
for rid in list(range(2705, 2750)) + list(range(2900, 2960)) + list(range(3000, 3060)) + list(range(3100, 3160)):
    data = fetch(str(rid))
    if not data or not isinstance(data, dict): continue
    results = data.get("results", [])
    if not results: continue
    title = results[0].get("report_title", "")
    text = title.lower()
    if any(k in text for k in ["poultry", "chicken", "broiler", "turkey", "egg"]):
        date = results[0].get("report_date", "")
        total = data.get("stats", {}).get("totalRows:", 0)
        print(f"  {rid:4d} | {total:>6} | {date:10s} | {title[:90]}")
