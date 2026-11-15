"""
inspect_editor_row.py
Inspects the elements on the active contributor input row on D2D Step 2.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_row():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        js = """
        () => {
            const wrapper = document.querySelector('#contributors-field-wrapper');
            const icons = Array.from(wrapper.querySelectorAll('i, svg, div[style*="cursor"], button'));
            return icons.map(el => ({
                tag: el.tagName.toLowerCase(),
                class: el.className || '',
                id: el.id || '',
                text: el.innerText ? el.innerText.trim() : '',
                outerHTML: el.outerHTML.substring(0, 150)
            }));
        }
        """
        results = page.evaluate(js)
        print("Icons/Buttons inside wrapper:")
        print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    inspect_row()
