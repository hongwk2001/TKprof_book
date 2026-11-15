"""
inspect_tono_bungay_descriptions.py
Inspects current description fields on D2D Step 2 for Tono-Bungay.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_desc():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print(f"Active Page: {page.url} ({page.title()})\n")
        
        short_val = page.locator("#short-description-editor").input_value() if page.locator("#short-description-editor").count() > 0 else "N/A"
        print("--- Short Description ---")
        print(short_val)
        
        main_editor = page.locator('.cq-editor, [contenteditable="true"], textarea[name*="description"]')
        main_text = main_editor.first.inner_text() if main_editor.count() > 0 else "N/A"
        print("\n--- Main Ebook Description ---")
        print(main_text[:400])

if __name__ == "__main__":
    inspect_desc()
