"""
test_romance_tree.py
Inspects Romance category nodes under FICTION.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_romance():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        filter_input = page.locator("#filter-bisacs")
        filter_input.fill("Romance")
        page.wait_for_timeout(600)
        
        fiction = page.locator('.bisac-category[data-literal="FICTION"]')
        if fiction.count() > 0:
            fiction.first.click()
            page.wait_for_timeout(600)
            
        cats = page.locator("#bisac-list-wrapper .bisac-category")
        print(f"Total nodes under Romance search: {cats.count()}")
        for i in range(min(20, cats.count())):
            c = cats.nth(i)
            lit = c.get_attribute("data-literal") or ""
            code = c.get_attribute("data-code") or ""
            txt = c.inner_text().strip().replace("\n", " ")
            print(f"  [{i+1}] code='{code}', literal='{lit}', text='{txt}'")

if __name__ == "__main__":
    inspect_romance()
