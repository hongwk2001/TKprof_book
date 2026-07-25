import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
TAGGED_DIR = os.path.join(CHAPTERS_DIR, "tagged")

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', '', text)
    text = re.sub(r'[^\w]', '', text)
    return text.lower()

def check_integrity():
    issues_found = False
    print("Checking Art of War chapters text integrity...")
    
    for ch in range(1, 14):
        ch_str = str(ch).zfill(2)
        source_file = os.path.join(CHAPTERS_DIR, f"ch_{ch_str}_en.txt")
        tagged_file = os.path.join(TAGGED_DIR, f"tagged_ch_{ch_str}_en.txt")
        
        if not os.path.exists(source_file):
            print(f"  [MISSING] Source file ch_{ch_str}_en.txt missing.")
            issues_found = True
            continue
            
        if not os.path.exists(tagged_file):
            # If no separate tagged folder exists, source chapter is master
            continue
            
        with open(source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()
        with open(tagged_file, 'r', encoding='utf-8') as f:
            tagged_content = f.read()
            
        clean_source = clean_text(source_content)
        clean_tagged = clean_text(tagged_content)
        
        if clean_source != clean_tagged:
            issues_found = True
            print(f"  [ERROR] Chapter {ch_str} has mismatch!")
            print(f"    Source Clean Length: {len(clean_source)}")
            print(f"    Tagged Clean Length: {len(clean_tagged)}")
            
    if not issues_found:
        print("[SUCCESS] All Art of War chapter text files passed integrity verification!")
    else:
        print("[FAIL] Integrity issues detected in chapter files.")

if __name__ == "__main__":
    check_integrity()
