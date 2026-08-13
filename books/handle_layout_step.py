"""
handle_layout_step.py
Handles Draft2Digital Ebook Layout page (/layout) and clicks Save & Continue.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def handle_layout():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print(f"Current Page: {page.url} ({page.title()})")
        
        save_btn = page.locator("#save-and-continue, button:has-text('Save'), button:has-text('SAVE'), input[type='submit']")
        if save_btn.count() > 0:
            save_btn.first.click()
            print("  ✓ Clicked Save & Continue on Layout page!")
            page.wait_for_timeout(3000)
            
            page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
            print(f"New Page URL: {page.url}")
            print(f"New Page Title: {page.title()}")

if __name__ == "__main__":
    handle_layout()
