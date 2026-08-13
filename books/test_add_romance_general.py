"""
test_add_romance_general.py
Tests expanding FICTION -> FICTION / Romance -> FICTION / Romance / General.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def add_romance():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        filter_input = page.locator("#filter-bisacs")
        filter_input.fill("Romance")
        page.wait_for_timeout(600)
        
        # 1. Expand FICTION
        fiction = page.locator('.bisac-category[data-literal="FICTION"]')
        if fiction.count() > 0:
            fiction.first.click()
            page.wait_for_timeout(600)
            
        # 2. Expand FICTION / Romance
        romance = page.locator('.bisac-category[data-literal="FICTION / Romance"]')
        if romance.count() > 0:
            romance.first.click()
            page.wait_for_timeout(600)
            print("  ✓ Expanded FICTION / Romance subcategory.")
            
        # 3. Click General leaf
        general = page.locator('.bisac-category[data-literal="FICTION / Romance / General"], .bisac-category[data-code="FIC027000"]')
        if general.count() > 0:
            general.first.click()
            print("  ✓ Selected FICTION / Romance / General!")

        print("\nFinal Chosen BISAC List:")
        print(page.locator("#chosen-bisac-list").inner_text())

if __name__ == "__main__":
    add_romance()
