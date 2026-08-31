"""
inspect_preview_details.py
Inspects approval checkboxes, form inputs, and buttons on the Preview page.
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
            const inputs = Array.from(document.querySelectorAll('input, label, form, .error, [class*="alert"]'));
            return inputs.map(el => ({
                tag: el.tagName.toLowerCase(),
                id: el.id || '',
                class: el.className || '',
                type: el.type || '',
                text: el.innerText ? el.innerText.trim() : '',
                checked: el.checked || false,
                outerHTML: el.outerHTML.substring(0, 180)
            })).filter(e => e.type === 'checkbox' || e.text.includes('approve') || e.text.includes('reviewed') || e.class.includes('error'));
        }
        """
        results = page.evaluate(js)
        print(f"Found {len(results)} checklist / input items:")
        print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    inspect_details()
