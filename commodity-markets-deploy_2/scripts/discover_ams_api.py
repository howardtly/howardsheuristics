#!/usr/bin/env python3
"""Explore MPR Datamart API structure for beef and pork cutout reports."""
import json, os, sys, urllib.request, urllib.error, urllib.parse

API_KEY = os.environ.get("AMS_API_KEY", "")
BASE = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"

def fetch(slug, params=None):
    url = f"{BASE}/{slug}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"Authorization": API_KEY, "Accept": "application/json"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  ERROR {slug}: {e}")
        return None

print("=" * 60)
print("MPR Datamart — Beef & Pork Cutout Structure")
print("=" * 60)

# === BEEF CUTOUT (2457) ===
print("\n\n=== REPORT 2457 (Beef Cutout) ===")
data = fetch("2457")
if data and isinstance(data, dict):
    print(f"Top-level keys: {list(data.keys())}")
    
    # Stats
    stats = data.get("stats", {})
    print(f"\nStats: {json.dumps(stats, default=str)[:300]}")
    
    # Report sections
    sections = data.get("reportSections", [])
    print(f"\nReport sections: {len(sections)}")
    for s in sections[:10]:
        print(f"  {json.dumps(s, default=str)[:150]}")
    
    # Results structure
    results = data.get("results", [])
    print(f"\nResults: {len(results)} records")
    if results:
        print(f"First record keys: {list(results[0].keys())}")
        # Show first 5 records
        for rec in results[:5]:
            print(f"  {json.dumps(rec, default=str)[:200]}")
        
        # Unique values for key fields
        report_dates = sorted(set(r.get("report_date", "") for r in results))
        item_descs = sorted(set(r.get("Item_Description", r.get("item_description", "")) for r in results))
        categories = sorted(set(r.get("category", r.get("Category", "")) for r in results))
        
        print(f"\nDate range: {report_dates[0]} to {report_dates[-1]} ({len(report_dates)} dates)")
        print(f"\nCategories ({len(categories)}):")
        for cat in categories[:20]:
            print(f"  {cat}")
        print(f"\nItem descriptions ({len(item_descs)}):")
        for item in item_descs[:30]:
            print(f"  {item}")

# === Try pork report IDs ===
print("\n\n=== SEARCHING FOR PORK REPORTS ===")
pork_candidates = [2498, 2499, 2500, 2501, 2502, 2503, 2510, 2511, 
                   2515, 2520, 2521, 2522, 2523, 2524, 2525, 2530]
for rid in pork_candidates:
    data = fetch(str(rid))
    if data and isinstance(data, dict):
        results = data.get("results", [])
        stats = data.get("stats", {})
        if results:
            sample = results[0]
            # Check if it's pork-related
            text = json.dumps(sample, default=str).lower()
            has_pork = any(k in text for k in ["pork", "loin", "belly", "ham", "butt", "rib", "picnic"])
            label = "PORK?" if has_pork else ""
            cats = sorted(set(r.get("category", r.get("Category", "")) for r in results[:50]))
            print(f"  {rid}: {len(results)} records, cats={cats[:5]} {label}")
            if has_pork:
                print(f"    Sample: {json.dumps(sample, default=str)[:200]}")
        else:
            sect = data.get("reportSections", [])
            if sect:
                print(f"  {rid}: 0 results but {len(sect)} sections: {sect[:3]}")

# === Try LM_PK602 variants ===
print("\n\n=== LM_PK SLUG VARIANTS ===")
for slug in ["LM_PK600", "LM_PK602", "LM_PK610", "LM_PK620"]:
    data = fetch(slug)
    if data and isinstance(data, dict):
        results = data.get("results", [])
        if results:
            print(f"  {slug}: {len(results)} records")
            print(f"    Sample: {json.dumps(results[0], default=str)[:200]}")
