#!/usr/bin/env python3
"""
Discover USDA AMS MyMarketNews (MARS) API endpoints for boxed beef and pork cutout data.
API docs: https://marsapi.ams.usda.gov
"""
import json, os, sys, urllib.request, urllib.error, urllib.parse

API_KEY = os.environ.get("AMS_API_KEY", "N/KUHW09nFBAU2t+zT+LF049q6BNTxIl")
BASE = "https://marsapi.ams.usda.gov/services/v1.2/reports"

def fetch_api(path, params=None):
    """Fetch from MARS API with auth."""
    url = f"{BASE}/{path}" if path else BASE
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {
        "Authorization": API_KEY,
        "Accept": "application/json",
    }
    print(f"\n  GET {url[:120]}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8")
            print(f"  OK: {len(data):,} bytes")
            return json.loads(data)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:300]
        print(f"  HTTP {e.code}: {body}")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


print("=" * 60)
print("USDA AMS MARS API Discovery")
print("=" * 60)

# 1. List available reports
print("\n\n=== ALL AVAILABLE REPORTS ===")
reports = fetch_api("")
if reports:
    if isinstance(reports, list):
        print(f"  {len(reports)} reports")
        # Filter for beef/pork related
        for r in reports:
            name = str(r) if isinstance(r, str) else json.dumps(r)[:120]
            name_lower = name.lower()
            if any(k in name_lower for k in ["beef", "pork", "cutout", "boxed", "lm_xb", "lm_pk", "lm_bf"]):
                print(f"    {name}")
    elif isinstance(reports, dict):
        print(f"  Keys: {list(reports.keys())[:20]}")
        for k, v in list(reports.items())[:5]:
            print(f"    {k}: {str(v)[:200]}")

# 2. Try specific known report slugs
REPORT_SLUGS = [
    "2457",      # LM_XB459 - National Daily Boxed Beef Cutout
    "2461",      # LM_BF100 - maybe?
    "2498",      # LM_PK602 - Pork cutout
    "LM_XB459",  # Try slug-based access
    "LM_BF100",
    "LM_PK602",
]

print("\n\n=== TRYING KNOWN REPORT SLUGS ===")
for slug in REPORT_SLUGS:
    data = fetch_api(slug)
    if data:
        if isinstance(data, list) and len(data) > 0:
            print(f"  {slug}: {len(data)} records")
            sample = data[0]
            if isinstance(sample, dict):
                print(f"  Keys: {list(sample.keys())[:15]}")
                for k, v in list(sample.items())[:8]:
                    print(f"    {k} = {str(v)[:80]}")
        elif isinstance(data, dict):
            print(f"  {slug}: dict keys = {list(data.keys())[:15]}")

# 3. Try with filters
print("\n\n=== BEEF CUTOUT WITH DATE FILTER ===")
for slug in ["2457", "LM_XB459"]:
    data = fetch_api(slug, {"filter": '{"report_date":"04/08/2026"}'})
    if not data:
        data = fetch_api(slug, {"q": "report_date=04/08/2026"})
    if data and isinstance(data, list) and len(data) > 0:
        print(f"\n  {slug}: {len(data)} records for date filter")
        for rec in data[:3]:
            print(f"    {json.dumps(rec, default=str)[:200]}")
        break

# 4. Try pork
print("\n\n=== PORK CUTOUT ===")
for slug in ["2498", "LM_PK602"]:
    data = fetch_api(slug)
    if data and isinstance(data, list) and len(data) > 0:
        print(f"\n  {slug}: {len(data)} records")
        sample = data[0]
        if isinstance(sample, dict):
            print(f"  Keys: {list(sample.keys())[:15]}")
            for k, v in list(sample.items())[:10]:
                print(f"    {k} = {str(v)[:80]}")
        break
