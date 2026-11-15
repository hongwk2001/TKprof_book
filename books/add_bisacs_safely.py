"""
add_bisacs_safely.py
Safely populates Adult FICTION / Classics & FICTION / Romance / General into Draft2Digital chosen BISAC list.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def add_bisacs():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        filter_input = page.locator("#filter-bisacs")

        # 1. Reset filter and scope
        filter_input.fill("")
        top_x = page.locator("#top-level-bisac-category i, #top-level-bisac-category .fa-times")
        if top_x.count() > 0:
            try:
                top_x.first.click()
                page.wait_for_timeout(400)
            except Exception:
                pass

        # 2. Add FICTION / Classics if not present
        curr_text = page.locator("#chosen-bisac-list, #prioritized-bisacs-wrapper").first.inner_text()
        if "Classics" not in curr_text or "YOUNG ADULT" in curr_text:
            print("Adding FICTION / Classics...")
            filter_input.fill("Classics")
            page.wait_for_timeout(600)
            
            fiction_parent = page.locator('.bisac-category[data-literal="FICTION"]')
            if fiction_parent.count() > 0:
                fiction_parent.first.click()
                page.wait_for_timeout(600)
                
            classics_leaf = page.locator('.bisac-category[data-literal="FICTION / Classics"]')
            if classics_leaf.count() == 0:
                classics_leaf = page.locator('.bisac-category:has-text("Classics")')
            if classics_leaf.count() > 0:
                classics_leaf.first.click()
                print("  ✓ Added FICTION / Classics")
                page.wait_for_timeout(500)

        # 3. Add FICTION / Romance / General if not present
        curr_text = page.locator("#chosen-bisac-list, #prioritized-bisacs-wrapper").first.inner_text()
        if "Romance" not in curr_text:
            print("Adding FICTION / Romance / General...")
            filter_input.fill("Romance")
            page.wait_for_timeout(600)

            fiction_parent = page.locator('.bisac-category[data-literal="FICTION"]')
            if fiction_parent.count() > 0:
                fiction_parent.first.click()
                page.wait_for_timeout(600)

            romance_sub = page.locator('.bisac-category[data-literal="FICTION / Romance"]')
            if romance_sub.count() > 0:
                romance_sub.first.click()
                page.wait_for_timeout(600)

            general_leaf = page.locator('.bisac-category[data-literal="FICTION / Romance / General"]')
            if general_leaf.count() == 0:
                general_leaf = page.locator('.bisac-category:has-text("General")')
            if general_leaf.count() > 0:
                general_leaf.first.click()
                print("  ✓ Added FICTION / Romance / General")
                page.wait_for_timeout(500)

        print("\nFinal Chosen BISAC List:")
        print(page.locator("#chosen-bisac-list, #prioritized-bisacs-wrapper").first.inner_text())

if __name__ == "__main__":
    add_bisacs()
