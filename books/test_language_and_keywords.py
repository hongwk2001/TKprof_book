"""
test_language_and_keywords.py
Selects Language (Korean) and populates Search Terms with Enter keypresses on D2D Step 1.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

KEYWORDS = ["토노번게이", "Tono Bungay", "HG웰스", "고전소설", "영국문학", "풍자소설"]

def test_lang_keywords():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        # 1. Select Language (Korean)
        lang_wrapper = page.locator("#language-field-wrapper, #language")
        if lang_wrapper.count() > 0:
            print("Selecting Language: Korean...")
            page.locator("#language").click()
            page.wait_for_timeout(600)
            
            korean_opt = page.locator("text='Korean'")
            if korean_opt.count() > 0:
                korean_opt.first.click()
                print("  ✓ Selected Language: Korean")
            else:
                print("  ⚠️ Korean option not found in dropdown.")

        # 2. Populate Search Terms with Enter key
        search_input = page.locator("#searchTerms")
        if search_input.count() > 0:
            print("\nPopulating Search Terms with Enter keypresses...")
            for kw in KEYWORDS:
                search_input.fill("")
                search_input.type(kw, delay=50)
                search_input.press("Enter")
                page.wait_for_timeout(400)
                print(f"  ✓ Added Search Term (press Enter): {kw}")

        page.wait_for_timeout(800)

if __name__ == "__main__":
    test_lang_keywords()
