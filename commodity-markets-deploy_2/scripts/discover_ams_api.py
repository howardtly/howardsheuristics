#!/usr/bin/env python3
"""Try different API approaches to extract actual price data."""
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
print("Extract Actual Price Data")
print("=" * 60)

# Try 1: Filter to single date to limit response, dump FULL raw JSON
print("\n=== BEEF 2453 — single date, full JSON ===")
for param in [
    "filter={\"filters\":[{\"fieldName\":\"report_date\",\"operatorType\":\"EQUAL\",\"values\":[\"04/09/2026\"]}]}",
    "q=report_date=04/09/2026",
    "allSections=true&filter={\"filters\":[{\"fieldName\":\"report_date\",\"operatorType\":\"EQUAL\",\"values\":[\"04/09/2026\"]}]}",
]:
    url = f"{BASE}/2453?{param}"
    print(f"\n  URL: {url[:120]}...")
    raw = fetch_raw(url)
    if raw:
        print(f"  Size: {len(raw)} bytes")
        # Pretty print first 3000 chars
        try:
            j = json.loads(raw)
            pretty = json.dumps(j, indent=2, default=str)
            print(pretty[:3000])
            if len(pretty) > 3000:
                print(f"  ... ({len(pretty)} total chars)")
        except:
            print(raw[:3000])
        break

# Try 2: Pork 2498 same approach
print("\n\n=== PORK 2498 — single date ===")
for param in [
    "filter={\"filters\":[{\"fieldName\":\"report_date\",\"operatorType\":\"EQUAL\",\"values\":[\"04/09/2026\"]}]}",
    "q=report_date=04/09/2026",
]:
    url = f"{BASE}/2498?{param}"
    raw = fetch_raw(url)
    if raw:
        print(f"  Size: {len(raw)} bytes")
        try:
            j = json.loads(raw)
            pretty = json.dumps(j, indent=2, default=str)
            print(pretty[:3000])
        except:
            print(raw[:3000])
        break

# Try 3: Beef Weekly Comp 2465 — this one had loads data, maybe sections have prices
print("\n\n=== BEEF WEEKLY 2465 — Cuts section, single date ===")
url = f"{BASE}/2465?sections=Cuts&filter={{\"filters\":[{{\"fieldName\":\"report_date\",\"operatorType\":\"EQUAL\",\"values\":[\"04/06/2026\"]}}]}}"
raw = fetch_raw(url)
if raw:
    print(f"  Size: {len(raw)} bytes")
    try:
        j = json.loads(raw)
        pretty = json.dumps(j, indent=2, default=str)
        print(pretty[:4000])
    except:
        print(raw[:4000])

# Try 4: Different API version v1.2
print("\n\n=== v1.2 API ===")
for slug in ["2453", "2498"]:
    url = f"https://mpr.datamart.ams.usda.gov/services/v1.2/reports/{slug}"
    raw = fetch_raw(url)
    if raw:
        print(f"  v1.2 {slug}: {len(raw)} bytes")
        try:
            j = json.loads(raw)
            if isinstance(j, dict):
                print(f"  Keys: {list(j.keys())}")
                results = j.get("results", [])
                if results:
                    print(f"  First record keys: {list(results[0].keys())[:20]}")
                    # Print any key that looks price-related
                    for k, v in results[0].items():
                        if v and any(p in k.lower() for p in ["price", "cutout", "value", "total", "load", "weight", "avg"]):
                            print(f"    {k} = {v}")
        except:
            print(raw[:500])
