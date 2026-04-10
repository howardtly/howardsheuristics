#!/usr/bin/env python3
"""Discover USDA AMS MARS API — try multiple auth methods."""
import json, os, sys, urllib.request, urllib.error, urllib.parse

API_KEY = os.environ.get("AMS_API_KEY", "")
BASE = "https://marsapi.ams.usda.gov/services/v1.2/reports"

def try_request(label, url, headers):
    print(f"\n  [{label}] GET {url[:100]}...")
    print(f"    Headers: { {k: v[:30]+'...' if len(v)>30 else v for k,v in headers.items()} }")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read().decode("utf-8")
            print(f"    ✓ OK: {len(data):,} bytes")
            j = json.loads(data)
            if isinstance(j, list):
                print(f"    {len(j)} records")
                if j: print(f"    Sample: {json.dumps(j[0], default=str)[:200]}")
            elif isinstance(j, dict):
                print(f"    Keys: {list(j.keys())[:10]}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:200]
        print(f"    ✗ HTTP {e.code}: {body}")
    except Exception as e:
        print(f"    ✗ {e}")
    return False

print("=" * 60)
print("USDA AMS MARS API — Auth Method Discovery")
print(f"API key length: {len(API_KEY)}, starts with: {API_KEY[:8]}...")
print("=" * 60)

# Test a known report slug
test_url = f"{BASE}/LM_XB459"

# Method 1: Authorization header (raw key)
try_request("Auth: raw key", test_url, {"Authorization": API_KEY, "Accept": "application/json"})

# Method 2: Authorization: Bearer
try_request("Auth: Bearer", test_url, {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"})

# Method 3: Authorization: Basic
import base64
b64key = base64.b64encode(API_KEY.encode()).decode()
try_request("Auth: Basic", test_url, {"Authorization": f"Basic {b64key}", "Accept": "application/json"})

# Method 4: API key in query parameter
test_url_param = f"{BASE}/LM_XB459?api_key={urllib.parse.quote(API_KEY)}"
try_request("Query: api_key", test_url_param, {"Accept": "application/json"})

# Method 5: Custom header names
try_request("Header: X-Api-Key", test_url, {"X-Api-Key": API_KEY, "Accept": "application/json"})
try_request("Header: ApiKey", test_url, {"ApiKey": API_KEY, "Accept": "application/json"})
try_request("Header: api_key", test_url, {"api_key": API_KEY, "Accept": "application/json"})

# Method 6: No auth (maybe public?)
try_request("No auth", test_url, {"Accept": "application/json"})

# Method 7: Try different API base URLs
alt_bases = [
    "https://marsapi.ams.usda.gov/services/v1.1/reports/LM_XB459",
    "https://marsapi.ams.usda.gov/services/v1/reports/LM_XB459",
    "https://marketnews.usda.gov/mnp/ls-landing",
    "https://mpr.datamart.ams.usda.gov/services/v1.1/reports/LM_XB459",
]
for alt_url in alt_bases:
    try_request(f"Alt URL", alt_url, {"Authorization": API_KEY, "Accept": "application/json"})

# Method 8: Try the datamart API specifically
print("\n\n=== MPR Datamart API ===")
dm_base = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"
for slug in ["LM_XB459", "2457"]:
    for auth_style in [
        {"Authorization": API_KEY},
        {"Authorization": f"Bearer {API_KEY}"},
        {},  # no auth
    ]:
        headers = {**auth_style, "Accept": "application/json"}
        if try_request(f"Datamart {slug}", f"{dm_base}/{slug}", headers):
            # If successful, get some data
            break
