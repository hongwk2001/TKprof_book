"""
test_js_click.py
Dispatches click via page.evaluate to add FICTION / Classics to D2D chosen list.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_click():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        js = """
        () => {
            const el = document.querySelector('div[data-code="FIC004000"]') || document.querySelector('div[data-literal*="Classics"]');
            if (el) {
                el.click();
                return 'Clicked: ' + el.innerText.trim();
            }
            return 'Element not found';
        }
        """
        res = page.evaluate(js)
        print("JS Eval result:", res)
        page.wait_for_timeout(1000)
        
        print("\nChosen List after JS click:")
        print(page.locator("#chosen-bisac-list").inner_text())

if __name__ == "__main__":
    test_click()
