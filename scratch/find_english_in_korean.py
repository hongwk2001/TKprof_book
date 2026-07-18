import os
import sys
import re

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\git_repo\TKprof_book\books\secret_garden"
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

def main():
    print("Scanning Korean chapters for any remaining English words/letters...")
    
    # Regex to find English words (A-Za-z)
    eng_word_pattern = re.compile(r'[A-Za-z]+')
    
    found_any = False
    
    for i in range(1, 28):
        ko_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_ko.txt")
        if not os.path.exists(ko_path):
            continue
            
        with open(ko_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            matches = eng_word_pattern.findall(line)
            if matches:
                # We skip chapter headers if they are English titles like "Chapter 3: Across the Moor"
                # but we print them to check if they should be translated.
                found_any = True
                print(f"Chapter {i:02d}, Line {line_num}: Found English: {matches}")
                print(f"  Content: {line.strip()}")
                
    if not found_any:
        print("No English letters found in any of the Korean chapters! The files are clean.")

if __name__ == "__main__":
    main()
