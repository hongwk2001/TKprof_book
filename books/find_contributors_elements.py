"""
find_contributors_elements.py
Locates Non-Author Contributors buttons, selects, and inputs on D2D Step 2.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def find_elements():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        js = """
        () => {
            const list = [];
            const els = Array.from(document.querySelectorAll('button, div[id*="contribut"], div[class*="contribut"], label, div[id*="editor"], div[id*="translat"]'));
            els.forEach(el => {
                const txt = el.innerText ? el.innerText.trim() : '';
                if (txt.includes('Contributor') || txt.includes('Translator') || txt.includes('Editor') || txt.includes('Add')) {
                    list.push({
                        tag: el.tagName.toLowerCase(),
                        id: el.id || '',
                        class: el.className || '',
                        text: txt.substring(0, 80),
                        html: el.outerHTML.substring(0, 200)
                    });
                }
            });
            return list;
        }
        """
        results = page.evaluate(js)
        print(f"Found {len(results)} matching elements:")
        print(json.dumps(results[:20], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    find_elements()
