"""
inspect_contributor_modal.py
Inspects the modal dialog that pops up for Add New Contributor on D2D.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_modal():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        js = """
        () => {
            const modals = Array.from(document.querySelectorAll('.modal, .modal-backdrop, div[role="dialog"], [class*="modal"]'));
            return modals.map(el => ({
                class: el.className,
                html: el.outerHTML.substring(0, 1000)
            }));
        }
        """
        results = page.evaluate(js)
        print(f"Found {len(results)} modal elements:")
        print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    inspect_modal()
