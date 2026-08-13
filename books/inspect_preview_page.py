"""
inspect_preview_page.py
Inspects buttons and approval checkboxes on the D2D Preview page (/preview).
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_prev():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        js = """
        () => {
            const els = Array.from(document.querySelectorAll('button, input, label, div[id*="save"], a[class*="button"]'));
            return els.map(el => ({
                tag: el.tagName.toLowerCase(),
                id: el.id || '',
                class: el.className || '',
                type: el.type || '',
                text: el.innerText ? el.innerText.trim() : '',
                outerHTML: el.outerHTML.substring(0, 150)
            })).filter(e => e.text || e.id || e.type === 'checkbox');
        }
        """
        results = page.evaluate(js)
        print(f"Found {len(results)} interactive elements on Preview page:")
        print(json.dumps(results[:20], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    inspect_prev()
