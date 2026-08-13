"""
find_save_button.py
Locates Save and Continue button on D2D Step 2 page.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def find_save():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        js = """
        () => {
            const buttons = Array.from(document.querySelectorAll('button, input[type="submit"], div[id*="save"]'));
            return buttons.map(el => ({
                tag: el.tagName.toLowerCase(),
                id: el.id || '',
                class: el.className || '',
                text: el.innerText ? el.innerText.trim() : '',
                outerHTML: el.outerHTML.substring(0, 180)
            }));
        }
        """
        results = page.evaluate(js)
        print(f"Found {len(results)} buttons/submits:")
        print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    find_save()
