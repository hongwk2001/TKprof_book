"""
upload_tono_bungay_cover.py
Selects 'I have front cover art' radio option and uploads cover.jpg for Tono-Bungay on D2D.
"""

import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

COVER_PATH = r"C:\git_repo\TKprof_book\books\tono_bungay\cover.jpg"

def upload():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]
        
        print(f"Target Cover Path: {COVER_PATH} (Exists: {os.path.exists(COVER_PATH)})")
        
        # 1. Click radio option 'I have front cover art'
        have_cover_radio = page.locator('#front-cover-upload-1, label:has-text("I have front cover art")')
        if have_cover_radio.count() > 0:
            try:
                have_cover_radio.first.click()
                print("  ✓ Selected radio: 'I have front cover art.'")
                page.wait_for_timeout(600)
            except Exception as e:
                print(f"  ⚠️ Could not click radio: {e}")

        # 2. Upload file to #upload-front-cover or any file input
        cover_input = page.locator('#upload-front-cover, input[type="file"][accept*="image"]')
        if cover_input.count() > 0:
            try:
                cover_input.first.set_input_files(COVER_PATH)
                print(f"  ✓ Uploaded Cover Image to #upload-front-cover: {os.path.basename(COVER_PATH)}")
                page.wait_for_timeout(1000)
            except Exception as e:
                print(f"  ⚠️ Could not upload cover file: {e}")

if __name__ == "__main__":
    upload()
