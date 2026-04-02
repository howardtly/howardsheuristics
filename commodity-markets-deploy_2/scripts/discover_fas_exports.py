#!/usr/bin/env python3
"""
Explore the USDA FAS API for export sales data.
"""
import json
import os
from urllib.request import urlopen, Request
from urllib.error import HTTPError

API_KEY = os.environ.get("FAS_API_KEY", "9B50B342-EA13-4269-BFC8-77E9E9903161")
BASE = "https://apps.fas.usda.gov"

def try_url(url, label=""):
    print(f"\n{'='*60}")
    print(f"  {label or url}")
    print(f"  {url}")
    print(f"{'='*60}")
    try:
        req = Request(url)
        req.add_header("API_KEY", API_KEY)
        req.add_header("User-Agent", "HowardsHeuristics/1.0")
        req.add_header("Accept", "application/json")
        resp = urlopen(req, timeout=30)
        data = resp.read().decode("utf-8", errors="replace")
        print(f"  Status: {resp.status}")
        print(f"  Size: {len(data):,} bytes")
        try:
            j = json.loads(data)
            if isinstance(j, list):
                print(f"  Array with {len(j)} items")
                if len(j) > 0:
                    print(f"  First item keys: {list(j[0].keys()) if isinstance(j[0], dict) else type(j[0])}")
                    for item in j[:5]:
                        if isinstance(item, dict):
                            print(f"    {json.dumps(item, default=str)[:250]}")
                        else:
                            print(f"    {str(item)[:250]}")
            elif isinstance(j, dict):
                print(f"  Dict keys: {list(j.keys())}")
                for k, v in list(j.items())[:10]:
                    print(f"    {k}: {str(v)[:200]}")
            else:
                print(f"  {str(j)[:500]}")
        except json.JSONDecodeError:
            print(f"  Not JSON: {data[:500]}")
    except HTTPError as e:
        print(f"  HTTP {e.code}: {e.reason}")
        try:
            print(f"  Body: {e.read().decode()[:300]}")
        except: pass
    except Exception as e:
        print(f"  ERROR: {e}")

# 1. Get the full swagger spec to find all available endpoints
print("\n\n=== SWAGGER SPEC: ALL API PATHS ===")
try:
    req = Request(f"{BASE}/PSDOnlineDataServices/swagger/v1/swagger.json")
    req.add_header("User-Agent", "HowardsHeuristics/1.0")
    resp = urlopen(req, timeout=30)
    swagger = json.loads(resp.read().decode("utf-8"))
    paths = swagger.get("paths", {})
    print(f"Found {len(paths)} API paths:")
    for path in sorted(paths.keys()):
        print(f"\n  {path}")
        for method, details in paths[path].items():
            summary = details.get("summary", "")
            op_id = details.get("operationId", "")
            params = details.get("parameters", [])
            param_names = [p.get("name", "") for p in params]
            print(f"    {method.upper()}: {summary or op_id}")
            if param_names:
                print(f"    Params: {param_names}")
except Exception as e:
    print(f"  ERROR: {e}")

# 2. Try export-sales-related paths
print("\n\n=== TRYING EXPORT SALES ENDPOINTS ===")
endpoints = [
    "/PSDOnlineDataServices/api/ExportSales",
    "/PSDOnlineDataServices/api/exportsales",
    "/PSDOnlineDataServices/api/ExportSales/commodities",
    "/PSDOnlineDataServices/api/ExportSalesData",
    "/PSDOnlineDataServices/api/ESRD",
    "/PSDOnlineDataServices/api/WeeklyExportSales",
]
for ep in endpoints:
    try_url(f"{BASE}{ep}", ep)
