#!/usr/bin/env python3
"""Broad scan of MPR Datamart — beef (AM/PM/weekly), pork (AM/PM), poultry, turkey."""
import json, os, sys, urllib.request, urllib.error

API_KEY = os.environ.get("AMS_API_KEY", "")
BASE = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"

def fetch(slug):
    url = f"{BASE}/{slug}"
    headers = {"Authorization": API_KEY, "Accept": "application/json"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except:
        return None

print("=" * 60)
print("MPR Datamart — Full Meat & Poultry Report Scan")
print("=" * 60)

# Scan broad range: beef 2440-2490, pork 2495-2540, lamb/veal 2540-2580, poultry 2640-2740
RANGES = (list(range(2440, 2495)) + list(range(2495, 2545)) + 
          list(range(2545, 2585)) + list(range(2640, 2745)))

hits = []
for rid in RANGES:
    data = fetch(str(rid))
    if not data or not isinstance(data, dict):
        continue
    results = data.get("results", [])
    if not results:
        continue
    
    sample = results[0]
    title = sample.get("report_title", "")
    date = sample.get("report_date", "")
    total = data.get("stats", {}).get("totalRows:", 0)
    
    text = title.lower()
    tag = ""
    if "beef" in text or "boxed" in text or "cutout" in text and "pork" not in text: tag = "BEEF"
    if "pork" in text: tag = "PORK"
    if "chicken" in text or "broiler" in text or "poultry" in text: tag = "POULTRY"
    if "turkey" in text: tag = "TURKEY"
    if "lamb" in text: tag = "LAMB"
    if "egg" in text: tag = "EGG"
    if "veal" in text: tag = "VEAL"
    
    timing = ""
    if "morning" in text or "- am" in text or "a.m." in text: timing = "AM"
    elif "afternoon" in text or "- pm" in text or "p.m." in text: timing = "PM"
    elif "weekly" in text: timing = "WEEKLY"
    elif "daily" in text: timing = "DAILY"
    
    freq = "daily" if "daily" in text else "weekly" if "weekly" in text else "?"
    
    hits.append((rid, total, date, tag, timing, freq, title))
    print(f"  {rid:4d} | {total:>6} | {date:10s} | {tag:7s} | {timing:6s} | {freq:6s} | {title[:85]}")

# Slug-based access
print("\n\n=== SLUG-BASED ACCESS ===")
slugs = [
    # Beef cutout
    "LM_XB459",   # Daily boxed beef cutout & cuts
    "LM_XB403",   # Boxed beef cuts
    "LM_CT100",   # Weekly comprehensive cutout
    "LM_CT150",   # Comprehensive cutout
    "LM_CT153",   # Comprehensive cutout
    "LM_CT170",   # Comprehensive cutout
    "LM_BF100",   # Carcass
    # Pork
    "LM_PK600",   # Pork cutout morning
    "LM_PK602",   # Pork FOB afternoon
    "LM_PK610",   # Pork weekly
    # Poultry
    "PY_WB001",   # Broiler weekly
    "PY_WB003",   # Broiler
    "PY_PY003",   # Poultry market
    "PY_PY006",   # Poultry
    "AJ_PY004",   # Poultry
    "AJ_PY017",   # Poultry
    "NW_PY013",   # Broilers
    "NW_PY007",   # National poultry
    # Turkey
    "PY_TK003",   # Turkey
    "PY_TK001",   # Turkey
    "NW_TK603",   # Turkey
]
for slug in slugs:
    data = fetch(slug)
    if data and isinstance(data, dict):
        results = data.get("results", [])
        total = data.get("stats", {}).get("totalRows:", 0)
        if results:
            title = results[0].get("report_title", "?")
            date = results[0].get("report_date", "?")
            # Show a few field values from first record to understand data shape
            sample = results[0]
            price_fields = {k: v for k, v in sample.items() 
                          if v and any(p in k.lower() for p in ["price", "value", "weight", "load", "cutout", "total"])}
            print(f"  {slug:12s} | {total:>6} | {date:10s} | {title[:75]}")
            if price_fields:
                print(f"    Price fields: {json.dumps(price_fields, default=str)[:200]}")
        else:
            print(f"  {slug:12s} | empty")
    else:
        print(f"  {slug:12s} | not found")

# Deep dive on confirmed hits — show record structure
print("\n\n=== RECORD STRUCTURE FOR KEY REPORTS ===")
for rid, label in [(2457, "Beef 2457"), (2498, "Pork PM 2498")]:
    data = fetch(str(rid))
    if not data: continue
    results = data.get("results", [])
    if not results: continue
    
    # Get most recent record
    latest = results[0]
    print(f"\n--- {label} (report_date={latest.get('report_date')}) ---")
    print(f"All fields:")
    for k, v in latest.items():
        if v is not None and str(v).strip():
            print(f"  {k:30s} = {str(v)[:80]}")
    
    # Show a few more records to see variation
    print(f"\nFirst 8 records (key fields):")
    for rec in results[:8]:
        item = rec.get("Item_Description", rec.get("item_description", rec.get("label", "")))
        cat = rec.get("category", rec.get("Category", ""))
        price = rec.get("current_avg_price", rec.get("price_range_low", rec.get("avg_price", "")))
        wt = rec.get("total_pounds", rec.get("total_loads", ""))
        dt = rec.get("report_date", "")
        print(f"  {dt:10s} | {cat:20s} | {str(item):40s} | price={price} | wt={wt}")
