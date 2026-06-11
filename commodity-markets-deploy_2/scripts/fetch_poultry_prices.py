#!/usr/bin/env python3
"""
Fetch weekly chicken (3646) and turkey (3647) prices from USDA MARS / MyMarketNews API.

Endpoint:  https://marsapi.ams.usda.gov/services/v1.2/reports/{slug_id}/Report Detail
Auth:      HTTP Basic, API key as username + empty password (env var MMN_API_KEY)

This version captures the FULL item universe (not a curated whitelist):
  - region = National only
  - trade_status in {Domestic, Export}  (Import dropped)
  - >= 20 distinct weeks of observations to be included
  - size dimension collapsed: composite (All Sizes / N/A) row preferred,
    else the highest-volume size row for that week
  - chicken whole bird: ALL Items (headline, dashboard) + WOG + RTC (charts only)

Output: data/poultry_prices.json
{
  "fetched_at": "...",
  "meta": {
    "chicken": { "series": [ {name, group, item, class, trade, condition,
                              weeks, legacy, headline_whole, dashboard}, ... ] },
    "turkey":  { "series": [ ... ] }
  },
  "weekly": [
    { "date": "MM/DD/YYYY",
      "chicken": { "series": { "<display name>": {avg, low, high, change, volume}, ... } },
      "turkey":  { "series": { ... } } },
    ...
  ],
  "seasonal": {
    "chicken": { "years": [ {year, dates:[...], series:{name:[vals...]}}, ...,
                            {year:"5yr_avg", dates:[...], series:{...}} ] },
    "turkey":  { "years": [ ... ] }
  },
  "latest": { "date": "...", "chicken": {"series":{...}}, "turkey": {"series":{...}} }
}
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "data")

API_KEY = os.environ.get("MMN_API_KEY", "")
BASE = "https://marsapi.ams.usda.gov/services/v1.2/reports"

_auth = base64.b64encode((API_KEY + ":").encode()).decode() if API_KEY else ""
HEADERS = {
    "Authorization": "Basic " + _auth,
    "Accept": "application/json",
    "User-Agent": "HowardsHeuristics/2.0",
}

MIN_WEEKS = 20  # series must have >= this many distinct weeks to be kept
ALLOWED_TRADE = ("domestic", "export")

# Chicken whole-bird series that are charts-only (alternative methodologies)
CHICKEN_LEGACY_WHOLE = {"wog", "rtc broiler/fryer"}
CHICKEN_HEADLINE_WHOLE = "all items"  # -> National Composite Whole Bird


# ── value parsing ────────────────────────────────────────────────────────────
def _f(v):
    if v is None:
        return None
    try:
        s = str(v).replace(",", "").strip()
        if not s:
            return None
        f = float(s)
        return round(f, 2)
    except Exception:
        return None


def _i(v):
    if v is None:
        return None
    try:
        s = str(v).replace(",", "").strip()
        if not s:
            return None
        return int(float(s))
    except Exception:
        return None


def _norm(s):
    return (s or "").strip().lower()


def prettify_item(item):
    """Clean up a raw USDA item name into a display-friendly string."""
    s = item or ""
    s = s.replace("Boneless/Skinless", "B/S").replace("Boneless Skinless", "B/S")
    s = s.replace(",", " ")
    s = " ".join(s.split())  # collapse whitespace
    return s.strip()


# ── API ──────────────────────────────────────────────────────────────────────
def fetch_report_detail(slug_id, report_date=None):
    section = urllib.parse.quote("Report Detail")
    url = BASE + "/" + slug_id + "/" + section
    if report_date:
        url += "?q=report_date=" + report_date
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if isinstance(data, dict):
            return data.get("results") or []
        if isinstance(data, list):
            out = []
            for b in data:
                if isinstance(b, dict) and b.get("reportSection") == "Report Detail":
                    out.extend(b.get("results") or [])
            return out
        return []
    except Exception as e:
        print("  ERROR fetching " + slug_id + " date=" + str(report_date) + ": " + str(e), flush=True)
        return []


# ── series identity & collapsing ──────────────────────────────────────────────
def series_key(row):
    """Identity tuple for a price series (size collapsed away)."""
    primal = (row.get("primal") or "").strip()
    group = "Whole" if primal.lower() == "whole" else "Parts"
    return (
        group,
        (row.get("class") or "").strip(),
        (row.get("item") or "").strip(),
        (row.get("trade_status") or "").strip(),
        (row.get("condition") or "").strip(),
    )


def is_composite_size(sz):
    s = _norm(sz)
    return s in ("all sizes", "n/a", "")


def collapse_rows_by_date(rows):
    """Return {series_key: {date: chosen_row}} collapsing the size dimension.
    Composite (All Sizes / N/A) preferred; else highest-volume size."""
    # group by (series_key, date)
    grouped = defaultdict(list)
    for r in rows:
        if _norm(r.get("region")) != "national":
            continue
        if _norm(r.get("trade_status")) not in ALLOWED_TRADE:
            continue
        d = r.get("report_date")
        if not d:
            continue
        grouped[(series_key(r), d)].append(r)

    chosen = defaultdict(dict)  # series_key -> {date: row}
    for (skey, d), rs in grouped.items():
        composite = [r for r in rs if is_composite_size(r.get("size"))]
        pool = composite if composite else rs
        # pick highest volume (None treated as -1)
        best = max(pool, key=lambda r: (_i(r.get("volume")) if _i(r.get("volume")) is not None else -1))
        chosen[skey][d] = best
    return chosen


def display_names_for(series_keys):
    """Build {series_key: display_name} with disambiguation.
    series_keys: iterable of (group, class, item, trade, condition)."""
    # Group by (group, class, item); within each, disambiguate by trade/condition
    by_item = defaultdict(list)
    for sk in series_keys:
        group, klass, item, trade, cond = sk
        by_item[(group, klass, item)].append(sk)

    names = {}
    used = set()

    def core_name(group, klass, item):
        if _norm(item) == CHICKEN_HEADLINE_WHOLE and group == "Whole" and klass == "":
            return "National Composite Whole Bird"
        base = prettify_item(item)
        if klass and _norm(klass) != "n/a":
            base = base + " " + klass
        return base

    for (group, klass, item), variants in by_item.items():
        core = core_name(group, klass, item)
        if len(variants) == 1:
            cand = core
            sk = variants[0]
            if cand in used:
                g, k, it, tr, co = sk
                cand = core + " (" + tr + ", " + co + ")"
            names[sk] = cand
            used.add(cand)
            continue

        # multiple variants: find which dims vary
        trades = set(v[3] for v in variants)
        conds = set(v[4] for v in variants)
        vary_trade = len(trades) > 1
        vary_cond = len(conds) > 1

        # pick primary: Domestic > Export, Fresh > Frozen, then stable
        def rank(v):
            g, k, it, tr, co = v
            t_rank = 0 if _norm(tr) == "domestic" else 1
            c_rank = 0 if _norm(co) == "fresh" else 1
            return (t_rank, c_rank, tr, co)
        variants_sorted = sorted(variants, key=rank)
        primary = variants_sorted[0]

        for sk in variants_sorted:
            g, k, it, tr, co = sk
            if sk == primary:
                cand = core
            else:
                quals = []
                if vary_trade:
                    quals.append(tr)
                if vary_cond:
                    quals.append(co)
                if not quals:  # shouldn't happen, but guard
                    quals = [tr, co]
                cand = core + " (" + ", ".join(quals) + ")"
            # collision guard
            if cand in used:
                cand = core + " (" + tr + ", " + co + ")"
            n = 2
            base_cand = cand
            while cand in used:
                cand = base_cand + " #" + str(n)
                n += 1
            names[sk] = cand
            used.add(cand)
    return names


# ── build weekly records + meta for one commodity ─────────────────────────────
def build_commodity(rows, commodity):
    """Returns (meta_series_list, weekly_by_date, all_dates_sorted)."""
    chosen = collapse_rows_by_date(rows)  # series_key -> {date: row}

    # filter by min weeks
    kept = {sk: dr for sk, dr in chosen.items()
            if len([d for d, r in dr.items() if _f(r.get("wtd_avg_price")) is not None]) >= MIN_WEEKS}

    names = display_names_for(kept.keys())

    # meta
    meta_series = []
    for sk, dr in kept.items():
        group, klass, item, trade, cond = sk
        weeks = len([d for d, r in dr.items() if _f(r.get("wtd_avg_price")) is not None])
        legacy = (commodity == "chicken" and group == "Whole"
                  and _norm(item) in CHICKEN_LEGACY_WHOLE)
        headline = (commodity == "chicken" and group == "Whole"
                    and _norm(item) == CHICKEN_HEADLINE_WHOLE)
        meta_series.append({
            "name": names[sk],
            "group": group,
            "item": item,
            "class": klass,
            "trade": trade,
            "condition": cond,
            "weeks": weeks,
            "legacy": legacy,
            "headline_whole": headline,
            "dashboard": (not legacy),
        })
    # sort meta: Whole first (headline first), then Parts; alpha within
    def meta_sort(m):
        grp_rank = 0 if m["group"] == "Whole" else 1
        head_rank = 0 if m["headline_whole"] else 1
        return (grp_rank, head_rank, m["name"])
    meta_series.sort(key=meta_sort)

    # weekly records: date -> {name: prices}
    all_dates = set()
    for sk, dr in kept.items():
        all_dates.update(dr.keys())
    all_dates_sorted = sorted(all_dates, key=lambda ds: datetime.strptime(ds, "%m/%d/%Y"))

    weekly_by_date = {}
    for d in all_dates_sorted:
        series_obj = {}
        for sk, dr in kept.items():
            r = dr.get(d)
            if not r:
                continue
            avg = _f(r.get("wtd_avg_price"))
            if avg is None:
                continue
            series_obj[names[sk]] = {
                "avg": avg,
                "low": _f(r.get("low_price")),
                "high": _f(r.get("high_price")),
                "change": _f(r.get("price_change")),
                "volume": _i(r.get("volume")),
            }
        weekly_by_date[d] = {"series": series_obj}

    return meta_series, weekly_by_date, all_dates_sorted


# ── seasonal arrays for one commodity ─────────────────────────────────────────
def _md(ds):
    p = ds.split("/")
    return str(int(p[0])) + "/" + str(int(p[1]))


def build_seasonal_commodity(weekly_list):
    """weekly_list: [{date, series:{name:{avg,...}}}] sorted ascending.
    Returns {years:[...]}."""
    by_year = defaultdict(list)
    for rec in weekly_list:
        try:
            yr = int(rec["date"].split("/")[2])
        except Exception:
            continue
        by_year[yr].append(rec)

    years_sorted = sorted(by_year.keys())
    current_year = years_sorted[-1] if years_sorted else datetime.now().year

    # all series names seen
    all_names = set()
    for rec in weekly_list:
        all_names.update((rec.get("series") or {}).keys())

    year_objs = []
    for yr in years_sorted:
        recs = by_year[yr]
        labels = [_md(r["date"]) for r in recs]
        series_arrays = {}
        for name in all_names:
            arr = []
            has_any = False
            for r in recs:
                v = (r.get("series") or {}).get(name)
                val = v.get("avg") if v else None
                if val is not None:
                    has_any = True
                arr.append(val)
            if has_any:
                series_arrays[name] = arr
        year_objs.append({"year": yr, "dates": labels, "series": series_arrays})

    # 5-year average (per series), index-aligned
    prior_years = [y for y in years_sorted if y < current_year][-5:]
    if prior_years:
        # template = year with most weeks among prior years
        longest = max(prior_years, key=lambda y: len(by_year[y]))
        longest_obj = next(yo for yo in year_objs if yo["year"] == longest)
        labels = longest_obj["dates"]
        L = len(labels)
        avg_series = {}
        for name in all_names:
            out = []
            for i in range(L):
                vals = []
                for y in prior_years:
                    yo = next((z for z in year_objs if z["year"] == y), None)
                    if not yo:
                        continue
                    arr = (yo.get("series") or {}).get(name)
                    if arr and i < len(arr) and arr[i] is not None:
                        vals.append(arr[i])
                out.append(round(sum(vals) / len(vals), 2) if vals else None)
            if any(v is not None for v in out):
                avg_series[name] = out
        year_objs.append({"year": "5yr_avg", "dates": labels, "series": avg_series})

    return {"years": year_objs}


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Poultry Price Fetch (full item universe)")
    print("Time: " + datetime.now().isoformat())
    print("=" * 60)

    if not API_KEY:
        print("ERROR: MMN_API_KEY env var not set.")
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "poultry_prices.json")

    existing = {}
    if os.path.exists(output_file):
        try:
            with open(output_file) as f:
                existing = json.load(f)
            print("Loaded existing: " + str(len(existing.get("weekly", []))) + " weekly records")
        except Exception:
            pass

    print("\n--- Fetching chicken (3646) ---")
    chicken_rows = fetch_report_detail("3646", None)
    print("  Bulk pull: " + str(len(chicken_rows)) + " rows")
    time.sleep(0.5)

    print("\n--- Fetching turkey (3647) ---")
    turkey_rows = fetch_report_detail("3647", None)
    print("  Bulk pull: " + str(len(turkey_rows)) + " rows")

    ch_meta, ch_weekly, ch_dates = build_commodity(chicken_rows, "chicken")
    tk_meta, tk_weekly, tk_dates = build_commodity(turkey_rows, "turkey")
    print("\nChicken series kept: " + str(len(ch_meta)) + " (dashboard: "
          + str(len([m for m in ch_meta if m["dashboard"]])) + ", legacy: "
          + str(len([m for m in ch_meta if m["legacy"]])) + ")")
    print("Turkey series kept:  " + str(len(tk_meta)))

    # ── merge weekly with existing (new data authoritative) ──
    new_dates = set(ch_dates) | set(tk_dates)
    existing_weekly = existing.get("weekly", []) or []
    merged = []
    for old in existing_weekly:
        if old.get("date") and old["date"] not in new_dates:
            merged.append(old)
    # build new combined weekly records
    all_new_dates = sorted(new_dates, key=lambda ds: datetime.strptime(ds, "%m/%d/%Y"))
    for d in all_new_dates:
        rec = {"date": d}
        if d in ch_weekly:
            rec["chicken"] = ch_weekly[d]
        if d in tk_weekly:
            rec["turkey"] = tk_weekly[d]
        merged.append(rec)
    merged.sort(key=lambda r: datetime.strptime(r["date"], "%m/%d/%Y"))

    # ── seasonal (built from the fresh pulls; full window each run) ──
    ch_weekly_list = [{"date": d, "series": ch_weekly[d]["series"]} for d in ch_dates]
    tk_weekly_list = [{"date": d, "series": tk_weekly[d]["series"]} for d in tk_dates]
    seasonal = {
        "chicken": build_seasonal_commodity(ch_weekly_list),
        "turkey": build_seasonal_commodity(tk_weekly_list),
    }

    # ── latest (most recent date with any data) ──
    latest = None
    for rec in reversed(merged):
        has = ((rec.get("chicken", {}).get("series"))
               or (rec.get("turkey", {}).get("series")))
        if has:
            latest = rec
            break

    result = {
        "fetched_at": datetime.now().isoformat(),
        "meta": {"chicken": {"series": ch_meta}, "turkey": {"series": tk_meta}},
        "weekly": merged,
        "seasonal": seasonal,
        "latest": latest,
    }

    print("\nTotal weeks after merge: " + str(len(merged)))
    if merged:
        print("  Range: " + merged[0]["date"] + " to " + merged[-1]["date"])
    if latest:
        print("  Latest: " + latest["date"])
        ch_n = len((latest.get("chicken", {}).get("series")) or {})
        tk_n = len((latest.get("turkey", {}).get("series")) or {})
        print("    chicken series this week: " + str(ch_n))
        print("    turkey series this week:  " + str(tk_n))

    with open(output_file, "w") as f:
        json.dump(result, f)
    print("\nWrote " + output_file + " (" + format(os.path.getsize(output_file), ",") + " bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
