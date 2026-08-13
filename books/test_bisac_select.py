"""
test_bisac_select.py
Types a BISAC search query into #filter-bisacs and inspects available BISAC subject items.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_bisac(search_term="Classics"):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        filter_input = page.locator("#filter-bisacs")
        print(f"Filtering BISAC by: '{search_term}'")
        filter_input.fill("")
        filter_input.type(search_term, delay=100)
        page.wait_for_timeout(1000)
        
        js = """
        () => {
            const items = Array.from(document.querySelectorAll('div[id*="bisac"], div[class*="bisac"], li, label, input[type="checkbox"]'));
            return items.map(el => ({
                tag: el.tagName.toLowerCase(),
                id: el.id,
                class: el.className,
                text: el.innerText ? el.innerText.trim() : '',
                checked: el.checked || el.getAttribute('aria-checked') || false
            })).filter(e => e.text && (e.text.includes('Fiction') || e.text.includes('Classics') || e.text.includes('Romance') || e.text.includes('General')));
        }
        """
        results = page.evaluate(js)
        print("Matching BISAC elements found:")
        for r in results[:15]:
            print(f"  [{r['tag']}] id='{r['id']}', class='{r['class']}', text='{r['text'][:60]}'")

if __name__ == "__main__":
    test_bisac()
