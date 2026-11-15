"""
test_add_contributors.py
Tests adding TKPROF LLC as Translator and Editor on Draft2Digital.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def add_contributor(name="TKPROF LLC", role="Translator"):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print(f"Adding Contributor: Name='{name}', Role='{role}'")
        
        # 1. Expand ADD NON-AUTHOR CONTRIBUTORS if needed
        btn = page.locator('#contributors-field-wrapper button:has-text("ADD NON-AUTHOR")')
        if btn.count() > 0:
            btn.first.click()
            page.wait_for_timeout(600)

        # 2. Set Name (#newContributorName)
        page.locator("#newContributorName").click()
        page.wait_for_timeout(600)
        
        existing_name = page.locator(f"text='{name}'")
        if existing_name.count() > 0:
            existing_name.first.click()
            print(f"  ✓ Selected existing contributor name: {name}")
        else:
            add_new_opt = page.locator("text='Add New Contributor'")
            if add_new_opt.count() > 0:
                add_new_opt.first.click()
                page.wait_for_timeout(500)
                name_input = page.locator('input[placeholder*="Contributor"], input[type="text"]').last
                name_input.fill(name)
                print(f"  ✓ Filled new contributor name: {name}")

        # 3. Set Role (#newContributorRole)
        page.locator("#newContributorRole").click()
        page.wait_for_timeout(600)
        
        role_opt = page.locator(f"text='{role}'")
        if role_opt.count() > 0:
            role_opt.first.click()
            print(f"  ✓ Selected contributor role: {role}")
        else:
            print(f"  ⚠️ Role option '{role}' not found.")

        # 4. Check if there is an Add / Save button
        add_btn = page.locator('#contributors-field-wrapper button:has-text("Add"), #contributors-field-wrapper .add-button')
        if add_btn.count() > 0:
            add_btn.first.click()
            print("  ✓ Clicked Add contributor button.")

        page.wait_for_timeout(800)
        print("\nContributor list HTML/Text:")
        print(page.locator("#contributors-field-wrapper").inner_text())

if __name__ == "__main__":
    add_contributor("TKPROF LLC", "Translator")
    add_contributor("TKPROF LLC", "Editor")
