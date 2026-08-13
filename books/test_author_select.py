"""
test_author_select.py
Tests selecting or adding an author name on Draft2Digital.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_author(author_name="엘리자베스 폰 아르님"):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print(f"Testing setting author to: {author_name}")
        
        # 1. Click #authorName to expand dropdown
        page.locator("#authorName").click()
        page.wait_for_timeout(800)
        
        # 2. Check if author_name is already in list
        author_item = page.locator(f"text='{author_name}'")
        if author_item.count() > 0:
            author_item.first.click()
            print(f"  ✓ Selected existing author from dropdown: {author_name}")
        else:
            # Click "Add New Author" option
            add_new_opt = page.locator("text='Add New Author'")
            if add_new_opt.count() > 0:
                add_new_opt.first.click()
                page.wait_for_timeout(800)
                
                # Check for new author text input
                new_author_input = page.locator('input[placeholder*="Author"], input[id*="author"], input[type="text"]').last
                if new_author_input.count() > 0:
                    new_author_input.fill(author_name)
                    print(f"  ✓ Filled new author name: {author_name}")
            else:
                print("  ⚠️ Could not find 'Add New Author' option.")

        # 3. Check Publisher (#publisher)
        pub_locator = page.locator("#publisher")
        if pub_locator.count() > 0:
            # Click #publisher if not already TKPROF LLC
            curr_pub = page.locator("#publisher-field-wrapper").inner_text()
            if "TKPROF LLC" not in curr_pub:
                pub_locator.click()
                page.wait_for_timeout(500)
                tkprof_opt = page.locator("text='TKPROF LLC'")
                if tkprof_opt.count() > 0:
                    tkprof_opt.first.click()
                    print("  ✓ Selected publisher: TKPROF LLC")
                else:
                    print("  ⚠️ TKPROF LLC option not found in dropdown.")
            else:
                print("  ✓ Publisher is already set to TKPROF LLC.")

if __name__ == "__main__":
    test_author()
