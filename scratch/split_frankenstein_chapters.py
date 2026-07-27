import os
import re
import sys
import subprocess

# Reconfigure stdout to prevent encoding errors on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\git_repo\TKprof_book\books\frankenstein\chapters"

parts = [
    (0, 1),
    (1, 5),
    (2, 9),
    (3, 13),
    (4, 17),
    (5, 21),
    (6, 25),
]

def split_file(lang):
    print(f"Splitting {lang} files...")
    
    header_patterns = {
        "en": re.compile(r"^(Letter \d+|Chapter \d+|Chapter [IVXLCDM]+)$", re.IGNORECASE),
        "ko": re.compile(r"^(편지 \d+|제\d+장)$")
    }
    
    pattern = header_patterns[lang]
    
    for part_num, start_ch in parts:
        src_filename = f"ch_{part_num:02d}_{lang}.txt"
        git_path = f"books/frankenstein/chapters/{src_filename}"
        
        try:
            content = subprocess.check_output(["git", "show", f"HEAD:{git_path}"], stderr=subprocess.DEVNULL).decode("utf-8")
        except subprocess.CalledProcessError:
            print(f"Could not read {git_path} from git. Trying local file...")
            src_path = os.path.join(BASE_DIR, src_filename)
            if not os.path.exists(src_path):
                print(f"Source file not found: {src_path}")
                continue
            with open(src_path, "r", encoding="utf-8") as f:
                content = f.read()
                
        lines = content.splitlines()
        
        # If it's the TOC part (ch_00), skip the TOC and title lines (first 35 lines)
        if part_num == 0:
            lines = lines[35:]
            
        chapters_data = []
        current_chapter_lines = []
        
        for line in lines:
            clean_line = line.replace("\ufeff", "").strip()
            
            if pattern.match(clean_line):
                if current_chapter_lines:
                    chapters_data.append(current_chapter_lines)
                    current_chapter_lines = []
                current_chapter_lines.append(line)
            else:
                if current_chapter_lines or pattern.match(clean_line):
                    current_chapter_lines.append(line)
                    
        if current_chapter_lines:
            chapters_data.append(current_chapter_lines)
            
        print(f"File {src_filename} -> Found {len(chapters_data)} chapters")
        found_headers = [lines[0].strip() for lines in chapters_data if lines]
        print(f"  Headers: {found_headers}")
        
        if len(chapters_data) != 4:
            print(f"Warning: Expected 4 chapters in {src_filename}, but found {len(chapters_data)}")
            
        # Write out to new files
        for i, ch_lines in enumerate(chapters_data):
            dest_ch_num = start_ch + i
            dest_filename = f"ch_{dest_ch_num:02d}_{lang}.txt"
            dest_path = os.path.join(BASE_DIR, dest_filename)
            
            with open(dest_path, "w", encoding="utf-8") as out:
                out.write("\n".join(ch_lines).strip() + "\n")
            print(f"  Saved {dest_filename} ({len(ch_lines)} lines)")

if __name__ == "__main__":
    split_file("en")
    split_file("ko")
