"""
test_upload_cover.py
Uploads cover_ko.jpg directly to #upload-front-cover on Draft2Digital.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def upload_cover(cover_path=r"C:\git_repo\TKprof_book\books\the_enchanted_april\cover_ko.jpg"):
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print(f"Uploading cover image: {cover_path}")
        
        # 1. Inspect all file inputs
        inputs = page.locator('input[type="file"]')
        print(f"Total file inputs found: {inputs.count()}")
        for i in range(inputs.count()):
            inp = inputs.nth(i)
            inp_id = inp.get_attribute("id")
            inp_accept = inp.get_attribute("accept")
            print(f"  Input #{i+1}: id='{inp_id}', accept='{inp_accept}'")

        # 2. Target #upload-front-cover
        cover_input = page.locator("#upload-front-cover")
        if cover_input.count() > 0:
            cover_input.set_input_files(cover_path)
            print("  ✓ Successfully attached cover image to #upload-front-cover!")
        else:
            print("  ⚠️ Selector #upload-front-cover not found.")

if __name__ == "__main__":
    upload_cover()
