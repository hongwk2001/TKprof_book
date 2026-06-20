import os
import re

BASE_DIR = r"d:\git_repo\TKprof_book\books\two_cities"
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
os.makedirs(CHAPTERS_DIR, exist_ok=True)

def split_english():
    draft_path = os.path.join(BASE_DIR, "modern_draft_en.txt")
    with open(draft_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split by chapter headers
    # Chapter 1: Recalled to Life
    pattern = r"(Chapter \d+:[^\n]+)"
    parts = re.split(pattern, content)
    
    # parts will be [header_preamble, chapter_header_1, chapter_content_1, chapter_header_2, chapter_content_2, ...]
    # We find chapter headers and combine them with content
    chapters = {}
    current_header = None
    for part in parts:
        part = part.strip()
        if not part:
            continue
        match = re.match(r"Chapter (\d+):", part)
        if match:
            current_header = part
        elif current_header:
            ch_num = int(re.match(r"Chapter (\d+):", current_header).group(1))
            chapters[ch_num] = current_header + "\n\n" + part
            current_header = None
            
    for ch_num, ch_content in chapters.items():
        dest_path = os.path.join(CHAPTERS_DIR, f"ch_{ch_num:02d}_en.txt")
        with open(dest_path, "w", encoding="utf-8") as out:
            out.write(ch_content)
        print(f"Saved {dest_path} ({len(ch_content)} chars)")

def split_korean():
    draft_path = os.path.join(BASE_DIR, "modern_draft_ko.txt")
    with open(draft_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    pattern = r"(제\d+장:[^\n]+)"
    parts = re.split(pattern, content)
    
    chapters = {}
    current_header = None
    for part in parts:
        part = part.strip()
        if not part:
            continue
        match = re.match(r"제(\d+)장:", part)
        if match:
            current_header = part
        elif current_header:
            ch_num = int(re.match(r"제(\d+)장:", current_header).group(1))
            chapters[ch_num] = current_header + "\n\n" + part
            current_header = None
            
    for ch_num, ch_content in chapters.items():
        dest_path = os.path.join(CHAPTERS_DIR, f"ch_{ch_num:02d}_ko.txt")
        with open(dest_path, "w", encoding="utf-8") as out:
            out.write(ch_content)
        print(f"Saved {dest_path} ({len(ch_content)} chars)")

if __name__ == "__main__":
    print("Splitting English draft...")
    split_english()
    print("Splitting Korean draft...")
    split_korean()
    print("Draft splitting complete!")
