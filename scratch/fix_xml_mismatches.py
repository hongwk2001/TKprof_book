import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGGED_DIR = os.path.join(BASE_DIR, "books", "secret_garden", "chapters", "tagged")

def fix_file(filename):
    filepath = os.path.join(TAGGED_DIR, filename)
    if not os.path.exists(filepath):
        print(f"{filename} not found.")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace `<mary>...</colin>` with `<mary>...</mary>`
    # We use a regex that matches `<mary>` followed by non-tag chars, then `</colin>`
    new_content = re.sub(r'<mary>([^<]*?)</colin>', r'<mary>\1</mary>', content)
    
    # Also handle nested case: `<mary>...</mary> ... <mary>...</colin>`
    # The regex `(<mary>[^<]*?)</colin>` will match the latter part.
    # Let's run it multiple times just in case.
    for _ in range(5):
        new_content = re.sub(r'<mary>([^<]*?)</colin>', r'<mary>\1</mary>', new_content)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed mismatches in {filename}")
    else:
        print(f"No changes made in {filename}")

def main():
    fix_file("tagged_ch_13_ko.txt")
    fix_file("tagged_ch_14_ko.txt")
    fix_file("tagged_ch_18_ko.txt")

if __name__ == "__main__":
    main()
