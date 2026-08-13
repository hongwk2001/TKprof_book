"""
run_d2d_browser.py
Launches Playwright's Chromium browser in interactive mode (headless=False)
with a persistent user profile to log into Draft2Digital and manage book entries.
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(BASE_DIR, "d2d_browser_profile")
os.makedirs(PROFILE_DIR, exist_ok=True)

def launch_d2d_chromium():
    print(f"🚀 Launching Playwright Chromium Browser...")
    print(f"  Profile Storage: {PROFILE_DIR}")
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--remote-debugging-port=9222", "--start-maximized"]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://www.draft2digital.com")
        
        print("\n✅ Chromium window launched successfully at https://www.draft2digital.com!")
        print("Please log in to Draft2Digital in the opened window, navigate to your book form, and then keep the window open.")
        print("Press Ctrl+C in this terminal when finished.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing Chromium browser session.")
            context.close()

if __name__ == "__main__":
    launch_d2d_chromium()
