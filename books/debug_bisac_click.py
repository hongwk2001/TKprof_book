"""
debug_bisac_click.py
Debugs selecting BISAC categories on D2D step-by-step.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def debug_bisac():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        filter_input = page.locator("#filter-bisacs")
        print("1. Typing 'Classics' into #filter-bisacs...")
        filter_input.fill("Classics")
        page.wait_for_timeout(1000)
        
        cats = page.locator("#bisac-list-wrapper .bisac-category")
        print(f"Total categories visible: {cats.count()}")
        for i in range(cats.count()):
            c = cats.nth(i)
            print(f"  [{i+1}] literal='{c.get_attribute('data-literal')}', text='{c.inner_text().strip()}'")

        # Click the first one (FICTION)
        if cats.count() > 0:
            print("\n2. Clicking first category (FICTION)...")
            cats.first.click()
            page.wait_for_timeout(1000)
            
            subcats = page.locator("#bisac-list-wrapper .bisac-category")
            print(f"Subcategories count after click: {subcats.count()}")
            for i in range(subcats.count()):
                sc = subcats.nth(i)
                print(f"  [{i+1}] literal='{sc.get_attribute('data-literal')}', text='{sc.inner_text().strip()}'")

if __name__ == "__main__":
    debug_bisac()
