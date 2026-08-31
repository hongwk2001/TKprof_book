"""
debug_second_contributor.py
Inspects elements inside #contributors-field-wrapper and clicks the Add button to commit Editor.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def debug_contrib():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        # 1. Select TKPROF LLC for the 2nd name input (#newContributorName)
        page.locator("#newContributorName").click()
        page.wait_for_timeout(600)
        
        tkprof_opt = page.locator("text='TKPROF LLC'")
        if tkprof_opt.count() > 0:
            tkprof_opt.first.click()
            print("  ✓ Selected name: TKPROF LLC")
            page.wait_for_timeout(400)

        # 2. Select Editor for the role input (#newContributorRole)
        page.locator("#newContributorRole").click()
        page.wait_for_timeout(600)
        
        editor_opt = page.locator("text='Editor'")
        if editor_opt.count() > 0:
            editor_opt.first.click()
            print("  ✓ Selected role: Editor")
            page.wait_for_timeout(400)

        # 3. Find and click the Add button inside #contributors-field-wrapper
        js = """
        () => {
            const btns = Array.from(document.querySelectorAll('#contributors-field-wrapper button, #contributors-field-wrapper i, #contributors-field-wrapper div[class*="add"]'));
            return btns.map(b => ({ tag: b.tagName.toLowerCase(), class: b.className, text: b.innerText, outerHTML: b.outerHTML.substring(0, 150) }));
        }
        """
        btns_info = page.evaluate(js)
        print("\nFound buttons inside contributors wrapper:")
        print(json.dumps(btns_info, indent=2, ensure_ascii=False))

        # Attempt to click the add button/plus icon
        add_icon = page.locator('#contributors-field-wrapper i.fa-plus, #contributors-field-wrapper button:has-text("+"), #contributors-field-wrapper .add-button, #contributors-field-wrapper button')
        if add_icon.count() > 0:
            add_icon.first.click()
            print("  ✓ Clicked Add (+) button!")
            page.wait_for_timeout(800)

        print("\nUpdated Contributor Section Text:")
        print(page.locator("#contributors-field-wrapper").inner_text())

if __name__ == "__main__":
    debug_contrib()
