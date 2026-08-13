"""
add_translators_editors.py
Selects TKPROF LLC as Translator and Editor under Non-Author Contributors on D2D Step 2.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def add_contributors():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        roles_to_add = ["Translator", "Editor"]
        
        for role_name in roles_to_add:
            print(f"\nAdding Contributor: TKPROF LLC as {role_name}...")
            
            # 1. Select Contributor Name (#newContributorName)
            page.locator("#newContributorName").click()
            page.wait_for_timeout(600)
            
            tkprof_opt = page.locator("text='TKPROF LLC'")
            if tkprof_opt.count() > 0:
                tkprof_opt.first.click()
                print("  ✓ Selected name: TKPROF LLC")
            else:
                add_new = page.locator("text='Add New Contributor'")
                if add_new.count() > 0:
                    add_new.first.click()
                    page.wait_for_timeout(500)
                    inp = page.locator('#contributors-field-wrapper input[type="text"]').last
                    inp.fill("TKPROF LLC")
                    print("  ✓ Filled new name: TKPROF LLC")

            # 2. Select Contributor Role (#newContributorRole)
            page.locator("#newContributorRole").click()
            page.wait_for_timeout(600)

            role_opt = page.locator(f"text='{role_name}'")
            if role_opt.count() > 0:
                role_opt.first.click()
                print(f"  ✓ Selected role: {role_name}")
            else:
                print(f"  ⚠️ Role {role_name} not found.")

            # 3. Click Add (+) button
            add_btn = page.locator('#contributors-field-wrapper button, #contributors-field-wrapper .add-button, #contributors-field-wrapper i.fa-plus')
            if add_btn.count() > 0:
                try:
                    add_btn.first.click()
                    print(f"  ✓ Clicked Add (+) for {role_name}")
                    page.wait_for_timeout(800)
                except Exception as e:
                    print(f"  ⚠️ Could not click add button: {e}")

        print("\nFinal Contributors Section Text:")
        print(page.locator("#contributors-field-wrapper").inner_text())

if __name__ == "__main__":
    add_contributors()
