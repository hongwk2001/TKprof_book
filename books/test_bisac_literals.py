"""
test_bisac_literals.py
Filters BISAC by query and lists data-literal attributes of matching category nodes.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_literals(query="Classics"):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        filter_input = page.locator("#filter-bisacs")
        filter_input.fill(query)
        page.wait_for_timeout(800)
        
        cats = page.locator("#bisac-list-wrapper .bisac-category")
        print(f"Filtered for '{query}' - Total category nodes: {cats.count()}")
        for i in range(min(15, cats.count())):
            c = cats.nth(i)
            lit = c.get_attribute("data-literal") or ""
            code = c.get_attribute("data-code") or ""
            txt = c.inner_text().strip().replace("\n", " ")
            print(f"  [{i+1}] code='{code}', literal='{lit}', text='{txt}'")

if __name__ == "__main__":
    inspect_literals("Classics")
