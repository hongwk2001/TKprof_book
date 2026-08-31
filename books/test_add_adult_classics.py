"""
test_add_adult_classics.py
Selects Adult FICTION / Classics and FICTION / Romance / General on D2D.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def add_adult_categories():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        filter_input = page.locator("#filter-bisacs")

        # --- 1. Select FICTION / Classics ---
        print("1. Filtering for 'Classics'...")
        filter_input.fill("Classics")
        page.wait_for_timeout(600)
        
        # Click parent category FICTION
        fiction_parent = page.locator('.bisac-category[data-literal="FICTION"]')
        if fiction_parent.count() > 0:
            fiction_parent.first.click()
            page.wait_for_timeout(600)
            print("  ✓ Expanded parent FICTION category.")
            
        classics_leaf = page.locator('.bisac-category[data-literal*="FICTION / Classics"]')
        if classics_leaf.count() > 0:
            classics_leaf.first.click()
            print("  ✓ Added FICTION / Classics to chosen list!")

        # --- 2. Select FICTION / Romance / General ---
        print("\n2. Filtering for 'Romance'...")
        filter_input.fill("Romance")
        page.wait_for_timeout(600)

        fiction_parent = page.locator('.bisac-category[data-literal="FICTION"]')
        if fiction_parent.count() > 0:
            fiction_parent.first.click()
            page.wait_for_timeout(600)
            print("  ✓ Expanded parent FICTION category.")

        romance_sub = page.locator('.bisac-category[data-literal="FICTION / Romance"]')
        if romance_sub.count() > 0:
            romance_sub.first.click()
            page.wait_for_timeout(600)
            print("  ✓ Expanded subcategory FICTION / Romance.")

        general_leaf = page.locator('.bisac-category[data-literal="FICTION / Romance / General"]')
        if general_leaf.count() > 0:
            general_leaf.first.click()
            print("  ✓ Added FICTION / Romance / General to chosen list!")

        print("\nFinal Chosen BISAC List:")
        chosen = page.locator("#chosen-bisac-list")
        if chosen.count() > 0:
            print(chosen.inner_text())

if __name__ == "__main__":
    add_adult_categories()
