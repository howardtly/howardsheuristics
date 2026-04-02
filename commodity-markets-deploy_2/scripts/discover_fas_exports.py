#!/usr/bin/env python3
"""
Targeted FAS Export Sales API discovery.
Base: https://api.fas.usda.gov
Auth: API key (try multiple header styles)
"""
import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError

API_KEY = "bo4ZgCpTfU16EqJbEORDHU7rqlf90oM3buzhIcgb"
BASE = "https://api.fas.usda.gov"

AUTH_STYLES = [
    {"x-api-key": API_KEY},
    {"API_KEY": API_KEY},
    {"api_key": API_KEY},
    {"Authorization": f"Bearer {API_KEY}"},
]

def fetch(url, label=""):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  {url}")
    for headers in AUTH_STYLES:
        hdr_name = list(headers.keys())[0]
        try:
            req = Request(url)
            for k, v in headers.items():
                req.add_header(k, v)
            req.add_header("User-Agent", "HowardsHeuristics/1.0")
            req.add_header("Accept", "application/json")
            resp = urlopen(req, timeout=30)
            data = resp.read().decode("utf-8", errors="replace")
            print(f"  SUCCESS with [{hdr_name}] | {len(data):,} bytes")
            try:
                j = json.loads(data)
                if isinstance(j, list):
                    print(f"  Array: {len(j)} items")
                    for item in j[:10]:
                        if isinstance(item, dict):
                            print(f"    {json.dumps(item, default=str)[:300]}")
                        else:
                            print(f"    {str(item)[:300]}")
                    if len(j) > 10:
                        print(f"    ... ({len(j) - 10} more)")
                elif isinstance(j, dict):
                    print(f"  Keys: {list(j.keys())}")
                    for k, v in list(j.items())[:8]:
                        vstr = json.dumps(v, default=str) if isinstance(v, (dict, list)) else str(v)
                        print(f"    {k}: {vstr[:250]}")
                return j
            except:
                print(f"  Raw: {data[:500]}")
                return data
        except HTTPError as e:
            if e.code in (401, 403):
                continue
            print(f"  HTTP {e.code} with [{hdr_name}]")
            try:
                print(f"  Body: {e.read().decode()[:200]}")
            except: pass
            return None
        except Exception as e:
            print(f"  ERR: {e}")
            return None
    print(f"  AUTH FAILED (all styles tried)")
    # Try as query param
    sep = "&" if "?" in url else "?"
    qurl = f"{url}{sep}api_key={API_KEY}"
    print(f"  Trying query param: {qurl}")
    try:
        req = Request(qurl)
        req.add_header("User-Agent", "HowardsHeuristics/1.0")
        req.add_header("Accept", "application/json")
        resp = urlopen(req, timeout=30)
        data = resp.read().decode("utf-8", errors="replace")
        print(f"  SUCCESS with query param | {len(data):,} bytes")
        try:
            j = json.loads(data)
            if isinstance(j, list):
                print(f"  Array: {len(j)} items")
                for item in j[:10]:
                    print(f"    {json.dumps(item, default=str)[:300]}")
            elif isinstance(j, dict):
                for k, v in list(j.items())[:8]:
                    print(f"    {k}: {str(v)[:200]}")
            return j
        except:
            print(f"  Raw: {data[:500]}")
    except HTTPError as e:
        print(f"  HTTP {e.code} with query param")
    except Exception as e:
        print(f"  ERR: {e}")
    return None

print("=" * 60)
print("FAS EXPORT SALES API - TARGETED DISCOVERY")
print("=" * 60)

# 1. Commodities list
commodities = fetch(f"{BASE}/api/esr/commodities", "ESR Commodities")

# 2. Countries list (first 10)
fetch(f"{BASE}/api/esr/countries", "ESR Countries")

# 3. Data release dates
fetch(f"{BASE}/api/esr/datareleasedates", "ESR Data Release Dates")

# 4. Try actual export data for corn (code 401)
fetch(f"{BASE}/api/esr/exports/commodityCode/401/allCountries/marketYear/2025", "Corn exports MY2025")

# 5. Try soybeans (code 801)
fetch(f"{BASE}/api/esr/exports/commodityCode/801/allCountries/marketYear/2025", "Soybeans exports MY2025")

# 6. Try wheat (code 101 = HRW)
fetch(f"{BASE}/api/esr/exports/commodityCode/101/allCountries/marketYear/2025", "Wheat HRW exports MY2025")

# 7. Search for sorghum in commodities
if commodities and isinstance(commodities, list):
    print("\n\n=== LOOKING FOR SORGHUM AND ALL GRAIN CODES ===")
    for c in commodities:
        if isinstance(c, dict):
            name = str(c.get("commodityName", c.get("commodity_name", c.get("name", "")))).upper()
            if any(k in name for k in ["SORGHUM", "CORN", "SOY", "WHEAT", "GRAIN"]):
                print(f"  {json.dumps(c)}")
