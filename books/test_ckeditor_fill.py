"""
test_ckeditor_fill.py
Fills the CKEditor 5 Ebook Description box using Playwright locator and keyboard insertion.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OVERVIEW_PATH = os.path.join(BASE_DIR, "tono_bungay", "overview_ko.txt")

def fill_ckeditor():
    with open(OVERVIEW_PATH, "r", encoding="utf-8") as f:
        overview_ko = f.read().strip()

    print(f"Target Korean Description length: {len(overview_ko)} chars")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]

        editor = page.locator(".ck-editor__editable")
        if editor.count() > 0:
            print("Found .ck-editor__editable element.")
            
            # Method 1: Click & focus
            editor.first.click()
            page.wait_for_timeout(300)

            # Method 2: Use JS to set data on CKEditor instance if available, or execCommand
            js_fill = """
            (text) => {
                const el = document.querySelector('.ck-editor__editable');
                if (!el) return 'No el';
                
                // Check for CKEditor instance
                if (el.ckeditorInstance) {
                    el.ckeditorInstance.setData(text);
                    return 'Used ckeditorInstance.setData';
                }
                
                // Fallback: set innerText & dispatch input/change/blur
                el.innerText = text;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                el.dispatchEvent(new Event('blur', { bubbles: true }));
                return 'Used innerText + events';
            }
            """
            res = page.evaluate(js_fill, overview_ko)
            print(f"  ✓ JS Fill Result: {res}")
            page.wait_for_timeout(500)

            # Check if text is now present in editor
            curr_text = editor.first.inner_text().strip()
            print(f"Current editor text length: {len(curr_text)} chars")
            
            # If still empty, use Playwright keyboard insert_text
            if len(curr_text) < 10:
                print("Falling back to Playwright keyboard.insert_text...")
                editor.first.click()
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.insert_text(overview_ko)
                page.wait_for_timeout(500)
                curr_text = editor.first.inner_text().strip()
                print(f"After keyboard insert length: {len(curr_text)} chars")
        else:
            print("  ⚠️ .ck-editor__editable element not found.")

if __name__ == "__main__":
    fill_ckeditor()
