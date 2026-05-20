#!/usr/bin/env python3
"""
One-shot discovery script for chicken (3646) and turkey (3647) reports.

These reports live on the **MyMarketNews / MARS API**, NOT the MPR Datamart.
- Endpoint:  https://marsapi.ams.usda.gov/services/v1.2/reports/{slug_id}
- Auth:      HTTP Basic, API key as username, empty password

Run via GitHub Actions (.github/workflows/discover-poultry.yml).
Reads MMN_API_KEY from environment (configure as a GitHub repo secret).

Outputs:
    poultry_raw_<reportId>_<date>.json
    poultry_summary.txt
"""
import base64
import json
import os
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# MyMarketNews / MARS API key — separate from AMS_API_KEY which is for MPR Datamart
API_KEY = os.environ.get("MMN_API_KEY", "")
BASE = "https://marsapi.ams.usda.gov/services/v1.2/reports"

# Basic auth: API key as username, empty password -> base64("key:")
_auth = base64.b64encode(f"{API_KEY}:".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {_auth}",
    "Accept": "application/json",
    "User-Agent": "HowardsHeuristics-Discovery/1.0",
}


def fetch(report_id, date_str=None):
    """Fetch a report. If date_str is None, fetch most recent (no filter)."""
    if date_str:
        # MARS API uses report_begin_date filter via the q= parameter, similar to LMR.
        # Try a few common patterns; the first that returns data wins.
        url = f"{BASE}/{report_id}?q=report_begin_date={date_str}"
    else:
        url = f"{BASE}/{report_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8")), url
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        return {"_error": f"HTTP {e.code}: {e.reason}", "_url": url, "_body": body}, url
    except Exception as e:
        return {"_error": str(e), "_url": url}, url


def find_recent_friday(weeks_back=0):
    """Walk back to last Friday (weekly reports typically publish Fridays)."""
    d = datetime.now()
    while d.weekday() != 4:  # Friday
        d -= timedelta(days=1)
    d -= timedelta(weeks=weeks_back)
    return d.strftime("%m/%d/%Y")


def summarize(data, label, out_lines):
    """Walk the response and print section + field names."""
    out_lines.append(f"\n{'='*70}")
    out_lines.append(f"REPORT {label}")
    out_lines.append(f"{'='*70}")

    if isinstance(data, dict) and "_error" in data:
        out_lines.append(f"ERROR: {data['_error']}")
        out_lines.append(f"URL: {data.get('_url', '')}")
        if data.get("_body"):
            out_lines.append(f"Body: {data['_body']}")
        return

    if isinstance(data, str):
        out_lines.append(f"Got string response (likely error): {data[:500]}")
        return

    blocks = data if isinstance(data, list) else [data]
    out_lines.append(f"Top-level: {type(data).__name__}, {len(blocks)} block(s)")

    for bi, block in enumerate(blocks):
        if not isinstance(block, dict):
            out_lines.append(f"  [Block {bi}] type={type(block).__name__}, value={block!r}")
            continue
        section = block.get("report_section") or block.get("reportSection") or "(no section field)"
        results = block.get("results") or []
        out_lines.append(f"\n  [Block {bi}] section = '{section}'   ({len(results)} rows)")
        other_keys = [k for k in block.keys() if k not in
                      ("report_section", "reportSection", "results")]
        if other_keys:
            out_lines.append(f"    Block top-level keys (non-results): {other_keys}")
        if results:
            r0 = results[0]
            if isinstance(r0, dict):
                out_lines.append(f"    Row 0 keys: {list(r0.keys())}")
                out_lines.append(f"    Row 0 full content:")
                for k, v in r0.items():
                    out_lines.append(f"      {k}: {v!r}")
                if len(results) > 1:
                    for name_field in ("commodity", "class", "class_description",
                                       "item_description", "Item_Description",
                                       "report_name", "primal_desc", "trim_description",
                                       "region"):
                        if name_field in r0:
                            names = sorted({str(r.get(name_field, ""))
                                            for r in results if r.get(name_field)})
                            out_lines.append(
                                f"    Distinct '{name_field}' values ({len(names)}):")
                            for n in names:
                                out_lines.append(f"      - {n}")
                            break
            else:
                out_lines.append(f"    Row 0 (non-dict): {r0!r}")


def main():
    summary = []
    print(f"MMN_API_KEY {'set (len ' + str(len(API_KEY)) + ')' if API_KEY else 'NOT set'}")
    print(f"Today: {datetime.now().strftime('%m/%d/%Y')}")

    if not API_KEY:
        msg = ("ERROR: MMN_API_KEY env var is not set. "
               "Register at https://mymarketnews.ams.usda.gov/, get your API key, "
               "and add it as a GitHub repo secret named MMN_API_KEY.")
        print(msg)
        summary.append(msg)
        with open("poultry_summary.txt", "w") as f:
            f.write("\n".join(summary))
        return

    candidate_dates = [find_recent_friday(w) for w in range(0, 8)]
    print(f"Candidate dates: {candidate_dates}")

    for report_id in ("3646", "3647"):
        print(f"\n===== Probing report {report_id} =====")
        # Latest with no filter
        data, url = fetch(report_id, None)
        print(f"  Latest fetch URL: {url}")
        with open(f"poultry_raw_{report_id}_latest.json", "w") as f:
            json.dump(data, f, indent=2, default=str)
        size = len(json.dumps(data, default=str))
        print(f"  -> wrote poultry_raw_{report_id}_latest.json ({size:,} chars)")
        summarize(data, f"{report_id} (latest, no filter)", summary)

        # Now try specific dates
        first_with_data = None
        for ds in candidate_dates:
            data, url = fetch(report_id, ds)
            fname = f"poultry_raw_{report_id}_{ds.replace('/', '-')}.json"
            with open(fname, "w") as f:
                json.dump(data, f, indent=2, default=str)
            if isinstance(data, dict) and "_error" in data:
                print(f"  {ds}: ERROR {data['_error']}")
                continue
            if isinstance(data, str):
                print(f"  {ds}: string response: {data[:80]}")
                continue
            blocks = data if isinstance(data, list) else [data]
            n_rows = sum(len(b.get("results", []) or [])
                         for b in blocks if isinstance(b, dict))
            print(f"  {ds}: {len(blocks)} blocks, {n_rows} rows")
            if n_rows > 0 and not first_with_data:
                first_with_data = ds
                summarize(data, f"{report_id} (date={ds})", summary)

        if not first_with_data:
            summary.append(f"\n[Report {report_id}] No dates produced any rows. "
                           f"Check raw files for details.")

    with open("poultry_summary.txt", "w") as f:
        f.write("\n".join(summary))
    print(f"\nWrote poultry_summary.txt")
