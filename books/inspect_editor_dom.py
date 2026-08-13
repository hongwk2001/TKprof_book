"""
inspect_editor_dom.py
Inspects the rich text editor elements and iframe structure on D2D Step 2.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def inspect_editor():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        js = """
        () => {
            const iframes = Array.from(document.querySelectorAll('iframe'));
            const textareas = Array.from(document.querySelectorAll('textarea'));
            const editables = Array.from(document.querySelectorAll('[contenteditable="true"], .cq-editor, [id*="description"]'));
            
            return {
                iframes: iframes.map(f => ({ id: f.id, class: f.className, src: f.src, title: f.title })),
                textareas: textareas.map(t => ({ id: t.id, name: t.name, class: t.className, val: t.value.substring(0, 100) })),
                editables: editables.map(e => ({ tag: e.tagName.toLowerCase(), id: e.id, class: e.className, text: e.innerText.substring(0, 100) }))
            };
        }
        """
        data = page.evaluate(js)
        print("Rich Text Editor DOM Structure:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    inspect_editor()
