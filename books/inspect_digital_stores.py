"""
inspect_digital_stores.py
Inspects digital stores and library service checkboxes on Draft2Digital Step 3.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_stores():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        js = """
        () => {
            const rows = Array.from(document.querySelectorAll('tr, div[class*="store"], div[class*="channel"], div[class*="row"]'));
            const list = [];
            rows.forEach(r => {
                const txt = r.innerText ? r.innerText.replace(/\\s+/g, ' ').trim() : '';
                const cb = r.querySelector('input[type="checkbox"], div[role="checkbox"], div[class*="checkbox"]');
                if (txt && (txt.includes('Apple') || txt.includes('Kobo') || txt.includes('Tolino') || txt.includes('Smashwords') || txt.includes('Vivlio') || txt.includes('Barnes') || txt.includes('OverDrive') || txt.includes('Scribd'))) {
                    list.push({
                        text: txt,
                        hasCheckbox: !!cb,
                        isChecked: cb ? (cb.checked || cb.getAttribute('aria-checked') === 'true' || cb.className.includes('checked')) : false,
                        isDisabled: cb ? (cb.disabled || txt.includes('not supported')) : txt.includes('not supported'),
                        outerHTML: r.outerHTML.substring(0, 200)
                    });
                }
            });
            return list;
        }
        """
        results = page.evaluate(js)
        print(f"Found {len(results)} digital store rows:")
        print(json.dumps(results[:25], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    inspect_stores()
