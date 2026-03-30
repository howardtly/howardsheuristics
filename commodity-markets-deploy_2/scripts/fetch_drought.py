#!/usr/bin/env python3
"""
Fetch USDA 'Commodities in Drought' data from agindrought.unl.edu
Downloads weekly drought percentages for 6 commodities and outputs drought.json.

Run locally first to test: python fetch_drought.py
Then add to GitHub Actions for weekly automation.
"""
import urllib.request, urllib.parse, re, json, os, sys
from datetime import datetime
from collections import defaultdict

# Commodities to fetch and their page/value mappings
# Page 1 = row crops, Page 2 = livestock/forage
# We need to discover the dropdown values by scraping the page
COMMODITIES = {
    "corn":         {"page": 1, "label": "Corn",         "search": "corn"},
    "soybeans":     {"page": 1, "label": "Soybeans",     "search": "soybean"},
    "winter_wheat": {"page": 1, "label": "Winter Wheat", "search": "winter wheat"},
    "spring_wheat": {"page": 1, "label": "Spring Wheat", "search": "spring wheat"},
    "cattle":       {"page": 2, "label": "Cattle",       "search": "cattle"},
    "hay":          {"page": 2, "label": "Hay",          "search": "hay"},
}

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(os.path.dirname(__file__), "..", "data"))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def get_page(url):
    """GET a page and return HTML."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=30)
    return resp.read().decode("utf-8", errors="replace")


def extract_form_fields(html):
    """Extract ASP.NET hidden form fields."""
    fields = {}
    for name in ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION", "__VIEWSTATEENCRYPTED"]:
        match = re.search(r'name="' + name + r'"[^>]*value="([^"]*)"', html)
        if match:
            fields[name] = match.group(1)
    return fields


def find_commodity_dropdown(html):
    """Find the commodity dropdown and its options."""
    # Look for select elements
    selects = re.findall(r'(<select[^>]*id="([^"]*)"[^>]*>.*?</select>)', html, re.DOTALL | re.IGNORECASE)
    
    for select_html, select_id in selects:
        options = re.findall(r'<option[^>]*value="([^"]*)"[^>]*>(.*?)</option>', select_html, re.IGNORECASE)
        if len(options) > 2:  # Likely the commodity dropdown
            print(f"  Found dropdown: {select_id} with {len(options)} options")
            for val, label in options[:5]:
                print(f"    {val}: {label}")
            if len(options) > 5:
                print(f"    ... and {len(options)-5} more")
            return select_id, options
    
    return None, []


def find_pagesize_dropdown(html):
    """Find the 'show all rows' dropdown."""
    selects = re.findall(r'(<select[^>]*id="([^"]*)"[^>]*>.*?</select>)', html, re.DOTALL | re.IGNORECASE)
    for select_html, select_id in selects:
        if "page" in select_id.lower() or "size" in select_id.lower() or "rows" in select_id.lower():
            options = re.findall(r'<option[^>]*value="([^"]*)"[^>]*>(.*?)</option>', select_html)
            print(f"  Page size dropdown: {select_id}")
            for val, label in options:
                print(f"    {val}: {label}")
            return select_id, options
    return None, []


def post_form(url, fields):
    """POST form data and return response HTML."""
    data = urllib.parse.urlencode(fields).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": UA,
        "Content-Type": "application/x-www-form-urlencoded",
    })
    resp = urllib.request.urlopen(req, timeout=30)
    return resp.read().decode("utf-8", errors="replace")


def parse_table(html):
    """Parse the data table from the page HTML."""
    # Find the main data table
    # Look for table with date-like content
    tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL | re.IGNORECASE)
    
    for table_html in tables:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL | re.IGNORECASE)
        if len(rows) < 5:
            continue
        
        # Check if this table has date-like content
        first_data = re.findall(r'<td[^>]*>(.*?)</td>', rows[1] if len(rows) > 1 else "", re.DOTALL | re.IGNORECASE)
        if not first_data or not re.match(r'\d{4}-\d{2}-\d{2}', first_data[0].strip() if first_data else ""):
            continue
        
        # Parse all rows
        data = []
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL | re.IGNORECASE)
            cells = [c.strip() for c in cells]
            if len(cells) >= 7 and re.match(r'\d{4}-\d{2}-\d{2}', cells[0]):
                try:
                    data.append({
                        "date": cells[0],
                        "none": int(cells[1]),
                        "d0_d4": int(cells[2]),
                        "d1_d4": int(cells[3]),
                        "d2_d4": int(cells[4]),
                        "d3_d4": int(cells[5]),
                        "d4": int(cells[6]),
                    })
                except (ValueError, IndexError):
                    continue
        
        if data:
            return data
    
    return []


def try_pandas_parse(html):
    """Fallback: use pandas to parse HTML tables."""
    try:
        import pandas as pd
        dfs = pd.read_html(html)
        for df in dfs:
            if len(df) > 10 and "Week" in df.columns or len(df.columns) >= 7:
                print(f"  Pandas found table: {df.shape}")
                data = []
                for _, row in df.iterrows():
                    date_str = str(row.iloc[0])
                    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                        try:
                            data.append({
                                "date": date_str,
                                "none": int(row.iloc[1]),
                                "d0_d4": int(row.iloc[2]),
                                "d1_d4": int(row.iloc[3]),
                                "d2_d4": int(row.iloc[4]),
                                "d3_d4": int(row.iloc[5]),
                                "d4": int(row.iloc[6]),
                            })
                        except:
                            continue
                if data:
                    return data
    except ImportError:
        pass
    return []


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "drought.json")
    
    print("=" * 60)
    print("USDA Commodities in Drought Fetch")
    print(f"Time: {datetime.utcnow().isoformat()}Z")
    print("=" * 60)
    
    # Step 1: Discover form structure from page 1
    print("\nStep 1: Discovering form structure...")
    for page_num in [1, 2]:
        url = f"https://agindrought.unl.edu/Table.aspx?{page_num}"
        print(f"\n  Page {page_num}: {url}")
        try:
            html = get_page(url)
            print(f"  HTML size: {len(html)} chars")
            
            # Find form fields
            form_fields = extract_form_fields(html)
            print(f"  Form fields: {list(form_fields.keys())}")
            
            # Find dropdowns
            dropdown_id, options = find_commodity_dropdown(html)
            pagesize_id, ps_options = find_pagesize_dropdown(html)
            
            # Show all select elements for debugging
            all_selects = re.findall(r'<select[^>]*id="([^"]*)"', html, re.IGNORECASE)
            print(f"  All select elements: {all_selects}")
            
            # Show form element
            form_match = re.search(r'<form[^>]*action="([^"]*)"[^>]*id="([^"]*)"', html, re.IGNORECASE)
            if form_match:
                print(f"  Form action: {form_match.group(1)}, id: {form_match.group(2)}")
            
            # Try to find the table even on initial load
            data = parse_table(html)
            if not data:
                data = try_pandas_parse(html)
            print(f"  Initial table rows: {len(data)}")
            if data:
                print(f"    First: {data[0]}")
                print(f"    Last:  {data[-1]}")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("Share this output so we can build the automated fetcher.")
    print("=" * 60)


if __name__ == "__main__":
    main()
