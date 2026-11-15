"""
select_adult_fiction_bisac.py
Clears Young Adult categories and selects Adult FICTION / Classics & FICTION / Romance / General on D2D.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def set_adult_fiction_bisacs():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print("1. Removing existing chosen categories...")
        # Remove chosen items by clicking their x buttons
        for _ in range(10):
            x_btns = page.locator('#chosen-bisac-list i, #chosen-bisac-list .fa-times, #prioritized-bisacs-wrapper i')
            if x_btns.count() > 0:
                try:
                    x_btns.first.click()
                    page.wait_for_timeout(250)
                except Exception:
                    break
            else:
                break

        # 2. Click Clear Filter
        clear_btn = page.locator("text='Clear Filter'")
        if clear_btn.count() > 0:
            try:
                clear_btn.first.click()
                page.wait_for_timeout(400)
            except Exception:
                pass

        # 3. Close top level category scope if open
        top_x = page.locator("#top-level-bisac-category i, #top-level-bisac-category .fa-times")
        if top_x.count() > 0:
            try:
                top_x.first.click()
                page.wait_for_timeout(400)
            except Exception:
                pass

        # 4. Filter for FICTION Classics
        print("2. Selecting FICTION / Classics...")
        filter_input = page.locator("#filter-bisacs")
        filter_input.fill("")
        filter_input.type("Classics", delay=80)
        page.wait_for_timeout(800)
        
        # Click parent category FICTION if listed
        fiction_cat = page.locator('#bisac-list-wrapper .bisac-category:has-text("FICTION"):not(:has-text("YOUNG ADULT"))')
        if fiction_cat.count() > 0:
            fiction_cat.first.click()
            page.wait_for_timeout(500)
            
        classics_opt = page.locator('#bisac-list-wrapper .bisac-category:has-text("Classics")')
        if classics_opt.count() > 0:
            classics_opt.first.click()
            print("  ✓ Selected Classics category.")

        # 5. Filter for FICTION Romance / General
        print("3. Selecting FICTION / Romance / General...")
        filter_input.fill("")
        filter_input.type("Romance", delay=80)
        page.wait_for_timeout(800)

        romance_opt = page.locator('#bisac-list-wrapper .bisac-category:has-text("General")')
        if romance_opt.count() > 0:
            romance_opt.first.click()
            print("  ✓ Selected Romance / General category.")

        print("\nCurrently Chosen BISAC List:")
        chosen = page.locator("#chosen-bisac-list")
        if chosen.count() > 0:
            print(chosen.inner_text())

if __name__ == "__main__":
    set_adult_fiction_bisacs()
