"""
autofill_tono_bungay_step1.py
Fills Step 1 form fields for Tono-Bungay (KO) on Draft2Digital.
"""

import os
import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(os.path.dirname(BASE_DIR), "notes")
PAYLOAD_FILE = os.path.join(NOTES_DIR, "d2d_payload_tono_bungay_ko.json")

def autofill():
    with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
        payload = json.load(f)

    print(f"\n🚀 Running Step 1 Autofill for: {payload['title']}")
    print(f"  Author:           {payload['author']}")
    print(f"  Publisher:        {payload['publisher']}")
    print(f"  Content Rating:   General Audience (explicit_content={payload['explicit_content']})")
    print(f"  Categories:       {payload['categories']}")
    print(f"  Cover Image:      {payload['cover_path']}\n")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = [pg for pg in context.pages if "draft2digital.com" in pg.url][0]

        # 1. Book Title
        if page.locator("#title").count() > 0:
            page.locator("#title").fill(payload["title"])
            print(f"  ✓ Title: {payload['title']}")

        # 2. Publisher
        pub_wrapper = page.locator("#publisher-field-wrapper")
        if pub_wrapper.count() > 0:
            curr_pub = pub_wrapper.inner_text()
            if payload["publisher"] not in curr_pub:
                page.locator("#publisher").click()
                page.wait_for_timeout(600)
                pub_opt = page.locator(f"text='{payload['publisher']}'")
                if pub_opt.count() > 0:
                    pub_opt.first.click()
                    print(f"  ✓ Selected Publisher: {payload['publisher']}")
            else:
                print(f"  ✓ Publisher already set to: {payload['publisher']}")

        # 3. Author Name (H. G. 웰스)
        author_wrapper = page.locator("#authorName-field-wrapper")
        if author_wrapper.count() > 0:
            target_author = payload["author"]
            curr_author_text = author_wrapper.inner_text()
            if target_author not in curr_author_text:
                page.locator("#authorName").click()
                page.wait_for_timeout(800)
                existing_author = page.locator(f"text='{target_author}'")
                if existing_author.count() > 0:
                    existing_author.first.click()
                    print(f"  ✓ Selected Author: {target_author}")
                else:
                    add_new = page.locator("text='Add New Author'")
                    if add_new.count() > 0:
                        add_new.first.click()
                        page.wait_for_timeout(600)
                        author_input = page.locator('#new-contributor, input[placeholder*="Author"], input[type="text"]').last
                        author_input.fill(target_author)
                        modal_btn = page.locator(".modal-body button")
                        if modal_btn.count() > 0:
                            modal_btn.first.click()
                            page.wait_for_timeout(600)
                        print(f"  ✓ Added & Selected Author: {target_author}")
            else:
                print(f"  ✓ Author already set to: {target_author}")

        # 4. Content Rating (General Audience)
        general_label = page.locator("label:has-text('does NOT contain content inappropriate for minors'), label:has-text('general audience')")
        if general_label.count() > 0:
            general_label.first.click()
            print("  ✓ Selected Content Rating: General Audience")

        # 5. Search Terms
        if page.locator("#searchTerms").count() > 0 and payload.get("keywords"):
            keywords_str = ", ".join(payload["keywords"])
            page.locator("#searchTerms").fill(keywords_str)
            print(f"  ✓ Filled Search Terms: {keywords_str}")

        # 6. BISAC Categories Selection
        filter_input = page.locator("#filter-bisacs")
        if filter_input.count() > 0:
            chosen_container = page.locator("#chosen-bisac-list, #prioritized-bisacs-wrapper").first
            
            # Clear default Young Adult if present
            for _ in range(5):
                if "YOUNG ADULT" in chosen_container.inner_text():
                    del_btn = chosen_container.locator(".delete-item").first
                    if del_btn.count() > 0:
                        del_btn.click()
                        page.wait_for_timeout(300)
                else:
                    break

            for cat_path in payload["categories"]:
                parts = [p.strip() for p in cat_path.split("/")]
                leaf_name = parts[-1]

                if leaf_name in chosen_container.inner_text() and "FICTION" in chosen_container.inner_text():
                    print(f"  ✓ Category already in list: {cat_path}")
                    continue

                filter_input.fill("")
                filter_input.type(leaf_name, delay=80)
                page.wait_for_timeout(600)

                js_click = """
                (leafName) => {
                    const leaves = Array.from(document.querySelectorAll('#bisac-list-wrapper .bisac-category'));
                    let match = leaves.find(el => el.innerText.trim() === leafName || el.getAttribute('data-literal').endsWith('/ ' + leafName));
                    if (match) {
                        match.click();
                        return 'Clicked leaf: ' + leafName;
                    }
                    const parent = leaves.find(el => el.innerText.includes('FICTION'));
                    if (parent) {
                        const icon = parent.querySelector('i');
                        if (icon) icon.click();
                        else parent.click();
                        return 'Expanded parent for: ' + leafName;
                    }
                    return 'Not found';
                }
                """
                res = page.evaluate(js_click, leaf_name)
                page.wait_for_timeout(600)
                if "Expanded" in res:
                    page.evaluate(js_click, leaf_name)
                    page.wait_for_timeout(600)

                print(f"  ✓ Processed BISAC Category: {cat_path}")

        # 7. Upload Cover Image (#upload-front-cover)
        if payload["files_exist"]["cover"]:
            cover_input = page.locator('#upload-front-cover, input[type="file"][accept*="image"]')
            if cover_input.count() > 0:
                try:
                    cover_input.first.set_input_files(payload["cover_path"])
                    print(f"  ✓ Uploaded Cover Image: {os.path.basename(payload['cover_path'])}")
                except Exception as e:
                    print(f"  ⚠️ Could not set cover file directly: {e}")

        print("\n✨ Tono-Bungay Step 1 Autofill Completed Successfully!")

if __name__ == "__main__":
    autofill()
