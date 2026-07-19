import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
TAGGED_DIR = os.path.join(CHAPTERS_DIR, "tagged")

def clean_text(text):
    # Remove XML/HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove all whitespace, punctuation, and casing
    text = re.sub(r'\s+', '', text)
    text = re.sub(r'[^\w]', '', text)
    return text.lower()

def check_integrity():
    issues_found = False
    
    # Check both English and Korean chapters
    for lang in ["en", "ko"]:
        print(f"Checking {lang.upper()} chapters...")
        for ch in range(1, 28):  # Secret Garden has 27 chapters
            ch_str = str(ch).zfill(2)
            source_file = os.path.join(CHAPTERS_DIR, f"ch_{ch_str}_{lang}.txt")
            tagged_file = os.path.join(TAGGED_DIR, f"tagged_ch_{ch_str}_{lang}.txt")
            
            if not os.path.exists(source_file) or not os.path.exists(tagged_file):
                continue
                
            with open(source_file, 'r', encoding='utf-8') as f:
                source_content = f.read()
            with open(tagged_file, 'r', encoding='utf-8') as f:
                tagged_content = f.read()
                
            clean_source = clean_text(source_content)
            clean_tagged = clean_text(tagged_content)
            
            # 1. Length/Equality Check
            if clean_source != clean_tagged:
                issues_found = True
                print(f"  [ERROR] Chapter {ch_str} ({lang}) has mismatch!")
                print(f"    Source Clean Length: {len(clean_source)}")
                print(f"    Tagged Clean Length: {len(clean_tagged)}")
                
                # Check if tagged contains duplicates or insertions
                if len(clean_tagged) > len(clean_source):
                    print("    -> Tagged text has extra/duplicated content.")
                else:
                    print("    -> Tagged text is missing content.")
            
    if not issues_found:
        print("\n[SUCCESS] All chapters passed integrity check! No text duplication or deletion found.")
        return True
    else:
        print("\n[FAIL] Integrity issues found. Please fix the tagged files.")
        return False

if __name__ == "__main__":
    if not check_integrity():
        sys.exit(1)
