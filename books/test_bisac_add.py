"""
test_bisac_add.py
Tests filtering and selecting a BISAC category on Draft2Digital.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def add_bisac(search_term="Romance"):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print(f"Filtering BISAC by: '{search_term}'")
        filter_input = page.locator("#filter-bisacs")
        filter_input.fill("")
        filter_input.type(search_term, delay=80)
        page.wait_for_timeout(800)
        
        # Locate matching category items inside #bisac-list-wrapper
        categories = page.locator("#bisac-list-wrapper .bisac-category")
        print(f"Found {categories.count()} category options in list wrapper:")
        for i in range(min(10, categories.count())):
            cat = categories.nth(i)
            print(f"  [{i+1}] {cat.inner_text().strip()}")

        if categories.count() > 0:
            categories.first.click()
            print(f"  ✓ Clicked BISAC category: {categories.first.inner_text().strip()}")
            page.wait_for_timeout(500)
            
            # Print current chosen BISAC list
            chosen_list = page.locator("#chosen-bisac-list")
            if chosen_list.count() > 0:
                print("\nCurrently Chosen BISAC List:")
                print(chosen_list.inner_text())

if __name__ == "__main__":
    add_bisac()
