"""
clear_bisac_list.py
Clears chosen items from #chosen-bisac-list and resets the BISAC filter on D2D.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def clear_bisacs():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print("Clearing chosen BISAC list...")
        
        # 1. Click x buttons in #chosen-bisac-list or #prioritized-bisacs-wrapper
        items = page.locator('#chosen-bisac-list div, #prioritized-bisacs-wrapper div')
        for i in range(items.count()):
            x_btn = page.locator('#chosen-bisac-list .fa-times, #chosen-bisac-list i, #prioritized-bisacs-wrapper i')
            if x_btn.count() > 0:
                try:
                    x_btn.first.click()
                    page.wait_for_timeout(300)
                except Exception:
                    pass

        # 2. Click Clear Filter button
        clear_btn = page.locator("text='Clear Filter'")
        if clear_btn.count() > 0:
            clear_btn.first.click()
            page.wait_for_timeout(500)
            print("  ✓ Clicked 'Clear Filter'")

        # 3. If top level category has close x button
        top_x = page.locator("#top-level-bisac-category .fa-times, #top-level-bisac-category i")
        if top_x.count() > 0:
            top_x.first.click()
            page.wait_for_timeout(500)
            print("  ✓ Closed top-level category scope.")

        print("Current chosen BISAC list:")
        chosen = page.locator("#chosen-bisac-list")
        if chosen.count() > 0:
            print(chosen.inner_text())

if __name__ == "__main__":
    clear_bisacs()
