#!/usr/bin/env python3
"""Check report 2461 (weekly negotiated cutout) for historical cutout values."""
import json, os, urllib.request

API_KEY = os.environ.get("AMS_API_KEY", "")
BASE = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"

def fetch_json(url):
    headers = {"Authorization": API_KEY, "Accept": "application/json"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))

SKIP = {"report_title","slug_name","slug_id","office_name","office_code",
        "office_city","office_state","market_location_name","market_location_city",
        "market_location_state","market_type","market_type_category","is_correction",
        "narrative","trend","published_date"}

print("=" * 60)
print("Report 2461 (LM_XB459) — Weekly Negotiated Cutout")
print("=" * 60)

# Single date with allSections
data = fetch_json(f"{BASE}/2461?q=report_date=04/03/2026&allSections=true")
if isinstance(data, list):
    for block in data:
        section = block.get("reportSection", "?")
        results = block.get("results", [])
        if not results: continue
        print(f"\n  --- {section} ({len(results)} records) ---")
        for i, rec in enumerate(results[:6]):
            fields = {k: v for k, v in rec.items() if v is not None and str(v).strip() and k not in SKIP}
            print(f"    [{i}] {json.dumps(fields, default=str)[:200]}")

# Date range check
print(f"\n\n{'='*60}")
print("Date range for 2461 vs 2465")
print(f"{'='*60}")

for rid, label in [("2461", "Weekly Negotiated"), ("2465", "Weekly Comprehensive")]:
    data = fetch_json(f"{BASE}/{rid}")
    if isinstance(data, dict):
        results = data.get("results", [])
        stats = data.get("stats", {})
        dates = sorted(set(r.get("report_date", "") for r in results))
        print(f"\n  {rid} ({label}): {stats}")
        if dates:
            print(f"    Date range: {dates[0]} to {dates[-1]} ({len(dates)} dates)")
