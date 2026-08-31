"""
inspect_contributors_safe.py
Safely expands #contributors-field-wrapper and inspects all elements inside it without triggering any form submission.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_safe():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        wrapper = page.locator("#contributors-field-wrapper")
        if wrapper.count() == 0:
            print("Wrapper not found.")
            return

        # 1. Expand contributor section if needed
        open_btn = wrapper.locator('button:has-text("ADD NON-AUTHOR CONTRIBUTORS")')
        if open_btn.count() > 0 and open_btn.is_visible():
            open_btn.click()
            print("  ✓ Expanded Non-Author Contributors section")
            page.wait_for_timeout(800)

        # 2. Select Name: TKPROF LLC
        page.locator("#newContributorName").click()
        page.wait_for_timeout(600)
        tkprof_name = page.locator("text='TKPROF LLC'")
        if tkprof_name.count() > 0:
            tkprof_name.first.click()
            print("  ✓ Selected name: TKPROF LLC")
            page.wait_for_timeout(400)

        # 3. Select Role: Translator
        page.locator("#newContributorRole").click()
        page.wait_for_timeout(600)
        trans_opt = page.locator("text='Translator'")
        if trans_opt.count() > 0:
            trans_opt.first.click()
            print("  ✓ Selected role: Translator")
            page.wait_for_timeout(400)

        # 4. Inspect HTML of #contributors-field-wrapper
        js = """
        () => {
            const wrapper = document.querySelector('#contributors-field-wrapper');
            return {
                text: wrapper.innerText,
                html: wrapper.outerHTML
            };
        }
        """
        data = page.evaluate(js)
        print("\nWrapper Text:")
        print(data['text'])
        print("\nWrapper HTML Snippet:")
        print(data['html'][:1500])

if __name__ == "__main__":
    inspect_safe()
