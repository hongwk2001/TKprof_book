"""
inspect_d2d_detail.py
Inspects inputs, textareas, dropdowns, and file upload containers on the active D2D page.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_details():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        js = """
        () => {
            const results = [];
            const elements = Array.from(document.querySelectorAll('input, select, textarea, [contenteditable="true"], button'));
            elements.forEach(el => {
                const tag = el.tagName.toLowerCase();
                const type = el.getAttribute('type') || '';
                const id = el.id || '';
                const name = el.getAttribute('name') || '';
                const placeholder = el.placeholder || el.getAttribute('placeholder') || '';
                const parentText = el.parentElement ? el.parentElement.innerText.replace(/\\s+/g, ' ').substring(0, 80) : '';
                const outerHTML = el.outerHTML.substring(0, 150);
                
                results.push({
                    tag, type, id, name, placeholder, parentText, outerHTML
                });
            });
            return { url: window.location.href, elements: results };
        }
        """
        data = page.evaluate(js)
        print(f"Active Page: {data['url']}")
        print(json.dumps(data["elements"], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    inspect_details()
