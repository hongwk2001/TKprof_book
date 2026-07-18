import os
import sys
import re

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\git_repo\TKprof_book\books\secret_garden"
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

def main():
    print("Scanning Korean chapters for any non-Korean, non-standard text (Hanja, foreign alphabets, weird symbols)...")
    
    # We want to allow:
    # 1. Hangul: \uac00-\ud7a3, \u1100-\u11ff, \u3130-\u318f
    # 2. Standard punctuation: spaces, newlines, periods, commas, quotes, exclamation, question, tilde, colon, semicolon, hyphens, brackets, parenthesis, middle dot (·), and standard quotes.
    # 3. Numbers: 0-9
    # Anything outside this range is flagged.
    
    # Allowed character pattern (negated set)
    # We'll match characters NOT in the allowed set.
    allowed_pattern = re.compile(
        r'[^\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f'  # Hangul
        r'0-9'                                        # Numbers
        r'\s'                                         # Whitespace (spaces, tabs, newlines)
        r'.,\'\"?!~:;·\-–—‘’“”()\[\]{}<>「」『』\\/&+=%*]' # Punctuation and symbols
    )
    
    found_any = False
    
    for i in range(1, 28):
        ko_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_ko.txt")
        if not os.path.exists(ko_path):
            continue
            
        with open(ko_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            # Find all non-allowed characters
            matches = allowed_pattern.findall(line)
            if matches:
                # Deduplicate matches to make it clean
                unique_matches = list(set(matches))
                found_any = True
                print(f"Chapter {i:02d}, Line {line_num}: Found unexpected characters: {unique_matches}")
                print(f"  Content: {line.strip()}")
                
    if not found_any:
        print("\nPerfect! No non-Korean or non-standard characters found in any of the chapters. The book is 100% clean.")

if __name__ == "__main__":
    main()
