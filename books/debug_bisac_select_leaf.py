"""
debug_bisac_select_leaf.py
Tests clicking FICTION -> FICTION / Classics leaf node and checking #chosen-bisac-list.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_leaf():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        filter_input = page.locator("#filter-bisacs")
        filter_input.fill("Classics")
        page.wait_for_timeout(800)
        
        # 1. Click FICTION parent
        fiction = page.locator('.bisac-category[data-literal="FICTION"]')
        fiction.first.click()
        page.wait_for_timeout(800)

        # 2. Click FICTION / Classics leaf
        classics = page.locator('.bisac-category[data-literal="FICTION / Classics"]')
        print("Classics leaf inner text:", classics.inner_text().strip())
        
        # Click span or div inside classics
        classics.first.click()
        page.wait_for_timeout(1000)
        
        print("Chosen list after clicking Classics:")
        print(page.locator("#chosen-bisac-list, #prioritized-bisacs-wrapper").first.inner_text())

if __name__ == "__main__":
    test_leaf()
