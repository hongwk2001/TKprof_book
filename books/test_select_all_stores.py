"""
test_select_all_stores.py
Selects all supported digital stores and library channels on Draft2Digital Step 3.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def select_all_stores():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        # Locate all checkboxes where aria-disabled is false and aria-checked is false
        unchecked = page.locator('div.toggle[aria-disabled="false"][aria-checked="false"], div[role="checkbox"][aria-disabled="false"][aria-checked="false"]')
        count = unchecked.count()
        print(f"Found {count} unchecked, supported store/channel checkboxes.")
        
        selected_names = []
        for i in range(count):
            cb = unchecked.nth(i)
            # Get parent row title
            row = cb.locator("xpath=ancestor::tr")
            row_title = row.get_attribute("title") if row.count() > 0 else f"Store #{i+1}"
            
            try:
                cb.click()
                selected_names.append(row_title)
                print(f"  ✓ Checked store: {row_title}")
                page.wait_for_timeout(200)
            except Exception as e:
                print(f"  ⚠️ Could not check store {row_title}: {e}")

        print(f"\nSuccessfully selected {len(selected_names)} digital stores & library channels!")

if __name__ == "__main__":
    select_all_stores()
