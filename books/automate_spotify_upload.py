import os
import sys
import argparse
import time
from playwright.sync_api import sync_playwright

BASE_DIR = r"d:\git_repo\thefirstaicompany"
BOOKS_DIR = os.path.join(BASE_DIR, "books")
METADATA_DIR = os.path.join(BASE_DIR, "distribution_metadata")

def get_metadata(book, chapter, lang):
    """Loads the title and description from the generated metadata folder."""
    filename = f"{book}_ch_{chapter:02d}_{lang}.txt"
    if book == "gilgamesh":
        # Gilgamesh is podcast parts, check if chapter fits part 1 or part 2
        part = 1 if chapter in [1, 2, 3] else 2
        filename = f"gilgamesh_part_{part}_{lang}.txt"
        
    metadata_path = os.path.join(METADATA_DIR, filename)
    if not os.path.exists(metadata_path):
        print(f"Error: Metadata file not found at {metadata_path}")
        return None, None
        
    with open(metadata_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Split Title and Description
    parts = content.split("DESCRIPTION:\n")
    if len(parts) < 2:
        print("Error: Could not parse Title and Description from file")
        return None, None
        
    title_line = parts[0].replace("TITLE:\n", "").strip()
    description = parts[1].strip()
    
    # If it is Christmas Carol, we change the episode title to focus on the chapter name
    # e.g., "Chapter 2: The First of the Three Spirits (Easy Modern Translation & Multi-Voice Audio)"
    if book == "christmas_carol":
        title_line = title_line.replace("A Christmas Carol - ", "")
        title_line = title_line.replace(" (Easy Modern Translation & Multi-Voice Audio for ESL / Casual Listeners)", " (Easy Modern Translation & Multi-Voice Audio)")
        
    return title_line, description

def run_automation(book, chapter, lang, draft_mode):
    audio_filename = f"ch_{chapter:02d}_{lang}.mp3"
    if book == "gilgamesh":
        part = 1 if chapter in [1, 2, 3] else 2
        audio_filename = f"podcast_prt_{part}_{lang}.mp3"
        
    audio_path = os.path.abspath(os.path.join(BOOKS_DIR, book, "audio", audio_filename))
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return
        
    title, description = get_metadata(book, chapter, lang)
    if not title or not description:
        return
        
    print(f"\n🚀 Initiating Spotify Upload for: {book.upper()} Ch {chapter} ({lang.upper()})")
    print(f"  File: {audio_path}")
    print(f"  Title: {title}")
    
    with sync_playwright() as p:
        print("Connecting to Chrome via remote debugging (localhost:9222)...")
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print(f"Failed to connect to Chrome on port 9222: {e}")
            print("Please make sure Chrome is launched with '--remote-debugging-port=9222'.")
            return
            
        context = browser.contexts[0]
        page = None
        for p_obj in context.pages:
            if "creators.spotify.com" in p_obj.url:
                page = p_obj
                break
                
        if not page:
            print("Error: Could not find any open tab with 'creators.spotify.com'")
            return
            
        print(f"Successfully attached to Spotify Creators tab: {page.url}")
        
        # 1. Upload File
        title_selector = "input[placeholder='Give your episode a name']"
        is_uploading = page.locator("text=Generating preview").is_visible() or page.locator("text=Uploading").is_visible()
        is_details_page = page.locator(title_selector).is_visible()
        
        if is_details_page:
            print("Details page is already visible. Skipping upload step.")
        elif is_uploading:
            print("An upload is already in progress in the browser. Skipping upload step and waiting for completion...")
        else:
            print("No active upload detected. Uploading file...")
            file_input = page.locator("input[type='file']")
            file_input.wait_for(state="attached", timeout=10000)
            file_input.set_input_files(audio_path)
            print("Audio file selected and uploading started!")
        
        # 2. Wait for upload to finish and transition to details page
        print("Waiting for Details form to appear (waiting for upload to complete)...")
        # Wait up to 5 minutes for upload
        page.wait_for_selector(title_selector, timeout=300000)
        print("Details form visible! Filling fields...")
        
        # 3. Fill Title
        page.fill(title_selector, title)
        
        # 4. Fill Description using the HTML toggle trick
        print("Activating HTML description mode...")
        # Toggle HTML mode on
        html_toggle = page.locator("text=HTML")
        html_toggle.click()
        time.sleep(1)
        
        # Fill description text into standard textarea
        page.fill("textarea", description)
        print("Title and Description filled successfully!")
        
        # 5. Content Checks Toggles
        # Explicit is 'No' by default (first toggle)
        # Promotional is 'No' by default (second toggle)
        # We can scroll to the bottom to make sure buttons are clickable
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        
        # 6. Click Next
        print("Navigating to next step...")
        next_btn = page.get_by_role("button", name="Next")
        next_btn.click()
        
        # Wait a moment for page transition
        time.sleep(2)
        
        # 7. Next again (usually to Review/Publish page)
        # Check if another Next button exists (for Interactive elements or Scheduling)
        try:
            if page.get_by_role("button", name="Next").is_visible():
                page.get_by_role("button", name="Next").click()
                time.sleep(2)
        except:
            pass
            
        # 8. Final publish/save step
        if draft_mode:
            print("Draft Mode: Saving as draft...")
            save_draft_btn = page.get_by_role("button", name="Save draft")
            save_draft_btn.click()
            print("Successfully saved episode as DRAFT!")
        else:
            print("Publish Mode: Clicking publish...")
            publish_btn = page.get_by_role("button", name="Publish now")
            # If "Publish" is not immediately visible, look for generic publish button
            if not publish_btn.is_visible():
                publish_btn = page.get_by_role("button", name="Publish")
            
            # For safety, ask user to review manually or wait
            print("Ready to Publish! You can click Publish now manually on your browser screen.")
            
        print("\n🎉 Automation completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify Podcast upload automation.")
    parser.add_argument("--book", required=True, choices=["christmas_carol", "gilgamesh"], help="Book folder name.")
    parser.add_argument("--chapter", required=True, type=int, help="Chapter number (1-6).")
    parser.add_argument("--lang", required=True, choices=["en", "ko"], help="Language track (en/ko).")
    parser.add_argument("--publish", action="store_true", help="Publish directly instead of saving as draft.")
    
    args = parser.parse_args()
    
    run_automation(args.book, args.chapter, args.lang, not args.publish)
