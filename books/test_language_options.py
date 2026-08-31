"""
test_language_options.py
Inspects and selects Korean in the Language dropdown (#language) on D2D.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_lang():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print("Clicking #language dropdown...")
        page.locator("#language").click()
        page.wait_for_timeout(800)
        
        # Locate Korean option in listbox
        korean_item = page.locator('#language-listbox div:has-text("Korean"), #language-listbox span:has-text("Korean"), div[data-value*="Korean"]')
        print(f"Korean items count: {korean_item.count()}")
        
        if korean_item.count() > 0:
            korean_item.first.click()
            print("  ✓ Clicked Korean option!")
        else:
            # Fallback: search all option elements
            all_opts = page.locator('.select-component-option, [role="option"]')
            print(f"Total options in dropdown: {all_opts.count()}")
            for i in range(all_opts.count()):
                opt = all_opts.nth(i)
                txt = opt.inner_text().strip()
                if "Korean" in txt:
                    opt.click()
                    print(f"  ✓ Clicked option: {txt}")
                    break

        page.wait_for_timeout(800)
        print("\nLanguage field text now:")
        print(page.locator("#language-field-wrapper").inner_text())

if __name__ == "__main__":
    inspect_lang()
