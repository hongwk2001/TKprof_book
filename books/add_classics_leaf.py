"""
add_classics_leaf.py
Adds FICTION / Classics to the current chosen BISAC list on D2D.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def add_classics():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        filter_input = page.locator("#filter-bisacs")
        filter_input.fill("Classics")
        page.wait_for_timeout(800)
        
        # Check if Classics is visible in list wrapper
        classics_items = page.locator('#bisac-list-wrapper span:has-text("Classics"), #bisac-list-wrapper div:has-text("Classics")')
        print(f"Classics elements count: {classics_items.count()}")
        
        for i in range(classics_items.count()):
            elem = classics_items.nth(i)
            txt = elem.inner_text().strip()
            print(f"  [{i+1}] text='{txt}'")
            if "Classics" in txt and "JUVENILE" not in txt and "YOUNG ADULT" not in txt:
                elem.click()
                print("  ✓ Clicked Classics item!")
                page.wait_for_timeout(600)
                break
                
        print("\nUpdated Chosen List:")
        print(page.locator("#chosen-bisac-list").inner_text())

if __name__ == "__main__":
    add_classics()
