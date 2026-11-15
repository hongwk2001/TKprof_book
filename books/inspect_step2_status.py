"""
inspect_step2_status.py
Inspects description fields and manuscript upload input on D2D Step 2.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_status():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print(f"Page URL: {page.url} ({page.title()})\n")
        
        # 1. Short Description
        short_val = page.locator("#short-description-editor").input_value() if page.locator("#short-description-editor").count() > 0 else "N/A"
        print("--- Short Description ---")
        print(short_val)

        # 2. Main Description
        main_editor = page.locator('.cq-editor, [contenteditable="true"]')
        main_text = main_editor.first.inner_text() if main_editor.count() > 0 else "N/A"
        print("\n--- Main Description ---")
        print(main_text[:300])

        # 3. Manuscript Upload Input Status
        file_input = page.locator('#ebook-upload-content, input[type="file"][accept*="epub"]')
        print(f"\nManuscript Input count: {file_input.count()}")
        
        # Check text in manuscript section
        ms_section = page.locator('div:has-text("Upload Final Manuscript"), section:has-text("Manuscript")')
        if ms_section.count() > 0:
            print("\n--- Manuscript Section Text ---")
            print(ms_section.first.inner_text()[:300])

if __name__ == "__main__":
    inspect_status()
