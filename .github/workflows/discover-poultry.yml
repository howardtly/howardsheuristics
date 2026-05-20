#!/usr/bin/env python3
"""
One-shot discovery script. Hits chicken (3646) and turkey (3647) reports for a few
recent dates and dumps raw JSON + a section/field summary.

USAGE:
    export AMS_API_KEY="your_key"   # optional; the LMPR API typically works without one
    python3 discover_poultry.py

Outputs:
    poultry_raw_3646.json
    poultry_raw_3647.json
    poultry_summary.txt
"""
import json, os, sys, urllib.request, urllib.error
from datetime import datetime, timedelta

API_KEY = os.environ.get("AMS_API_KEY", "")
BASE = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports"
HEADERS = {"Authorization": API_KEY, "Accept": "application/json", "User-Agent": "HowardsHeuristics-Discovery/1.0"}


def fetch(report_id, date_str=None):
    """Fetch a report. If date_str is None, fetch the most recent (no q filter)."""
    if date_str:
        url = f"{BASE}/{report_id}?q=report_date={date_str}&allSections=true"
    else:
        url = f"{BASE}/{report_id}?allSections=true"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8")), url
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}: {e.reason}", "_url": url}, url
    except Exception as e:
        return {"_error": str(e), "_url": url}, url


def find_recent_friday(weeks_back=0):
    """These are weekly reports, typically published Friday. Walk back to last Friday."""
    d = datetime.now()
    # Move back to Friday (weekday=4)
    while d.weekday() != 4:
        d -= timedelta(days=1)
    d -= timedelta(weeks=weeks_back)
    return d.strftime("%m/%d/%Y")


def summarize(data, report_id, out_lines):
    """Walk the response and print section + field names."""
    out_lines.append(f"\n{'='*70}")
    out_lines.append(f"REPORT {report_id}")
    out_lines.append(f"{'='*70}")

    if isinstance(data, dict) and "_error" in data:
        out_lines.append(f"ERROR: {data['_error']}")
        out_lines.append(f"URL: {data.get('_url', '')}")
        return

    blocks = data if isinstance(data, list) else [data]
    out_lines.append(f"Top-level: {type(data).__name__}, {len(blocks)} block(s)")

    for bi, block in enumerate(blocks):
        if not isinstance(block, dict):
            continue
        section = block.get("reportSection", "(no section)")
        results = block.get("results", []) or []
        out_lines.append(f"\n  [Block {bi}] reportSection = '{section}'   ({len(results)} rows)")
        # Other top-level keys on the block
        other_keys = [k for k in block.keys() if k not in ("reportSection", "results")]
        if other_keys:
            out_lines.append(f"    Block keys (non-results): {other_keys}")
        # Dump field names from first row
        if results:
            r0 = results[0]
            out_lines.append(f"    Row keys: {list(r0.keys())}")
            # Pull out commodity description fields if present
            for kk in ("commodity", "commodity_desc", "report_name", "item_description",
                       "Item_Description", "class", "class_description",
                       "trim_description", "primal_desc", "region", "destination"):
                if kk in r0:
                    out_lines.append(f"      '{kk}' (row 0): {r0.get(kk)!r}")
            # Sample first row in full
            out_lines.append(f"    Row 0 (full):")
            for k, v in r0.items():
                out_lines.append(f"      {k}: {v!r}")
            # If more than one row, list distinct item_description values (or similar)
            if len(results) > 1:
                for name_field in ("item_description", "Item_Description", "trim_description",
                                   "commodity", "class_description", "region"):
                    if name_field in r0:
                        names = sorted({str(r.get(name_field, "")) for r in results if r.get(name_field)})
                        out_lines.append(f"    Distinct '{name_field}' values ({len(names)}):")
                        for n in names:
                            out_lines.append(f"      - {n}")
                        break


def main():
    summary = []
    print(f"API_KEY {'set' if API_KEY else 'NOT set (trying without)'}")
    print(f"Today is {datetime.now().strftime('%m/%d/%Y')}")

    # Try the last few recent Fridays
    candidate_dates = [find_recent_friday(w) for w in range(0, 6)]
    print(f"Candidate dates to probe: {candidate_dates}")

    for report_id in ("3646", "3647"):
        print(f"\n===== Probing report {report_id} =====")
        # First, try the very latest (no date filter)
        data, url = fetch(report_id, None)
        print(f"  No-date fetch: {url}")
        # Save raw
        with open(f"poultry_raw_{report_id}_latest.json", "w") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"  -> wrote poultry_raw_{report_id}_latest.json ({len(json.dumps(data, default=str)):,} chars)")
        summarize(data, f"{report_id} (latest, no date filter)", summary)

        # Then try a few specific dates
        for ds in candidate_dates[:3]:
            data, url = fetch(report_id, ds)
            with open(f"poultry_raw_{report_id}_{ds.replace('/', '-')}.json", "w") as f:
                json.dump(data, f, indent=2, default=str)
            blocks = data if isinstance(data, list) else [data]
            n_rows = sum(len(b.get("results", []) or []) for b in blocks if isinstance(b, dict))
            print(f"  {ds}: {len(blocks)} blocks, {n_rows} total rows")
            if n_rows > 0:
                summarize(data, f"{report_id} (date={ds})", summary)
                break

    with open("poultry_summary.txt", "w") as f:
        f.write("\n".join(summary))
    print(f"\n\nWrote poultry_summary.txt — share that file with Claude.")
    print(f"Raw JSON dumps saved as poultry_raw_*.json (also handy to share).")


if __name__ == "__main__":
    main()
