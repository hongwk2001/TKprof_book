"""
inspect_bisac_tree.py
Inspects the BISAC subject category selection tree and filter input on Draft2Digital.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_bisac():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        filter_input = page.locator("#filter-bisacs")
        if filter_input.count() > 0:
            print("Filter input found! Parent HTML:")
            parent_html = filter_input.locator("xpath=../..").evaluate("el => el.innerHTML")
            print(parent_html[:1500])
        else:
            print("Filter input #filter-bisacs not found.")

if __name__ == "__main__":
    inspect_bisac()
