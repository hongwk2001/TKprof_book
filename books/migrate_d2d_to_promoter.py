"""
migrate_d2d_to_promoter.py
Copies all Draft2Digital automation scripts from TKprof_book to C:\\git_repo\\AppPromoter_AI\\draft2digital
"""

import os
import sys
import shutil

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
DEST_DIR = r"C:\git_repo\AppPromoter_AI\draft2digital"

D2D_SCRIPTS = [
    "start_d2d_browser.py",
    "inspect_d2d_form.py",
    "prepare_d2d_metadata.py",
    "automate_d2d_upload.py",
    "automate_d2d_step2.py",
    "automate_d2d_step3.py",
    "click_save_and_continue.py",
    "save_store_preferences.py",
    "capture_d2d_screenshot.py",
    "add_tkprof_contributors.py",
    "add_clean_contributors.py",
    "select_all_channels_js.py",
    "update_ckeditor_korean.py",
    "fix_step2_korean_and_epub.py"
]

def migrate():
    os.makedirs(DEST_DIR, exist_ok=True)
    print(f"🚀 Migrating Draft2Digital Automation Scripts")
    print(f"  Source: {SOURCE_DIR}")
    print(f"  Target: {DEST_DIR}\n")

    copied_count = 0
    for filename in D2D_SCRIPTS:
        src_path = os.path.join(SOURCE_DIR, filename)
        dest_path = os.path.join(DEST_DIR, filename)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"  ✓ Copied: {filename}")
            copied_count += 1
        else:
            print(f"  ⚠️ File not found in source: {filename}")

    # Create README in AppPromoter_AI/draft2digital
    readme_path = os.path.join(DEST_DIR, "README.md")
    readme_content = """# Draft2Digital (D2D) Publishing Automation Suite

Automated Playwright CDP publishing pipeline for Draft2Digital ebooks.

## Scripts Overview

1. **`start_d2d_browser.py`**: Launches Playwright Chromium on CDP port `9222` with a persistent profile.
2. **`inspect_d2d_form.py`**: Connects via CDP and extracts form field schemas (`d2d_form_schema_<step>.json`).
3. **`prepare_d2d_metadata.py`**: Prepares JSON metadata payloads (`d2d_payload_<book>_<lang>.json`) with title, author, publisher, content rating, categories, and file paths.
4. **`automate_d2d_upload.py`**: Automates **Step 1 (Metadata)**: Title, Author, Publisher, Language, Content Rating, Search Terms (with Enter keypresses), 3+ BISACs, and Cover Upload.
5. **`automate_d2d_step2.py`**: Automates **Step 2 (Ebook Details)**: Manuscript EPUB Upload, Short Description, CKEditor 5 Description (`setData`), Non-Author Contributors (`TKPROF LLC` as Translator & Editor), and Free D2D ISBN.
6. **`automate_d2d_step3.py`**: Automates **Step 3 (Pricing & Distribution)**: Digital Price, Library Price, 38+ Supported Distribution Channels/Stores.
7. **`click_save_and_continue.py`**: Navigates between publishing steps.
8. **`save_store_preferences.py`**: Checks "Remember my store preferences".
9. **`capture_d2d_screenshot.py`**: Captures CDP screenshots for visual verification.

## Usage Example

```bash
# 1. Start Browser
python draft2digital/start_d2d_browser.py

# 2. Run Step 1 (Shared Metadata & Cover Upload)
python draft2digital/automate_d2d_upload.py --book tono_bungay --lang ko

# 3. Run Step 2 (Ebook Details & EPUB Upload)
python draft2digital/automate_d2d_step2.py --book tono_bungay --lang ko

# 4. Run Step 3 (Pricing & Rights)
python draft2digital/automate_d2d_step3.py --price 3.99 --library-price 9.99
```
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"  ✓ Created README.md in {DEST_DIR}")

    # Also migrate JSON payloads and schemas from notes/
    notes_src = os.path.join(os.path.dirname(SOURCE_DIR), "notes")
    notes_dest1 = os.path.join(DEST_DIR, "notes")
    notes_dest2 = os.path.join(os.path.dirname(DEST_DIR), "notes")
    os.makedirs(notes_dest1, exist_ok=True)
    os.makedirs(notes_dest2, exist_ok=True)

    if os.path.exists(notes_src):
        for fname in os.listdir(notes_src):
            if fname.startswith("d2d_"):
                f_src = os.path.join(notes_src, fname)
                shutil.copy2(f_src, os.path.join(notes_dest1, fname))
                shutil.copy2(f_src, os.path.join(notes_dest2, fname))
                print(f"  ✓ Copied payload/schema: {fname}")

    print(f"\n✨ Successfully migrated D2D automation scripts and JSON payloads to AppPromoter_AI!")

if __name__ == "__main__":
    migrate()
