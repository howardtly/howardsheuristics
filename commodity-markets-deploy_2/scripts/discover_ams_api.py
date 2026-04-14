#!/usr/bin/env python3
"""Check reports 2461, 2643, and 2465 for comprehensive cutout history."""
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

for rid, label in [("2643", "Unknown 2643"), ("2461", "Weekly Negotiated"), ("2465", "Weekly Comprehensive")]:
    print(f"\n{'='*60}")
    print(f"  Report {rid}: {label}")
    print(f"{'='*60}")

    # Get stats and date range (no date filter)
    data = fetch_json(f"{BASE}/{rid}")
    if isinstance(data, dict):
        results = data.get("results", [])
        stats = data.get("stats", {})
        sections = data.get("reportSections", [])
        title = results[0].get("report_title", "?") if results else "?"
        dates = sorted(set(r.get("report_date", "") for r in results if r.get("report_date")))
        print(f"  Title: {title[:100]}")
        print(f"  Stats: {stats}")
        print(f"  Sections: {sections}")
        if dates:
            print(f"  Date range: {dates[0]} to {dates[-1]} ({len(dates)} unique dates)")

    # Single recent date with allSections
    print(f"\n  --- allSections for most recent date ---")
    try:
        data2 = fetch_json(f"{BASE}/{rid}?q=report_date=04/06/2026&allSections=true")
        if not data2:
            data2 = fetch_json(f"{BASE}/{rid}?q=report_date=04/03/2026&allSections=true")
        blocks = data2 if isinstance(data2, list) else [data2]
        for block in blocks:
            if not isinstance(block, dict): continue
            section = block.get("reportSection", "?")
            results = block.get("results", [])
            if not results: continue
            print(f"\n  --- {section} ({len(results)} records) ---")
            for i, rec in enumerate(results[:5]):
                fields = {k: v for k, v in rec.items() if v is not None and str(v).strip() and k not in SKIP}
                print(f"    [{i}] {json.dumps(fields, default=str)[:220]}")
    except Exception as e:
        print(f"  Error: {e}")
