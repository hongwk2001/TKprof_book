"""
test_explicit_radio.py
Inspects and selects the non-explicit / general audience option on D2D.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_radio():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        # Search for label or input containing "does NOT contain content inappropriate for minors"
        label_locator = page.locator("label:has-text('does NOT contain content inappropriate for minors'), label:has-text('general audience')")
        if label_locator.count() > 0:
            print("Found general audience label:", label_locator.first.inner_text())
            label_locator.first.click()
            print("  ✓ Clicked general audience radio option.")
        else:
            # Check for input[type="radio"]
            radios = page.locator('input[type="radio"]')
            print("Found radio count:", radios.count())

if __name__ == "__main__":
    test_radio()
