import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGGED_DIR = os.path.join(BASE_DIR, "books", "secret_garden", "chapters", "tagged")

TAGS = "mary|colin|dickon|martha|craven|ben|others"

# Match patterns:
# 1. Straight quotes: "<tag>speech</tag>" -> <tag>"speech"</tag>
# 2. Curly quotes: “<tag>speech</tag>” -> <tag>“speech”</tag>
# 3. Mismatched: "<tag>speech</tag>” or “<tag>speech</tag>" -> <tag>"speech"</tag>
# 4. Handle quotes next to spaces or punctuation
PATTERNS = [
    (re.compile(r'"<(?P<tag>' + TAGS + r')>(.*?)</(?P=tag)>"'), r'<\g<tag>>"\2"</\g<tag>>'),
    (re.compile(r'“<(?P<tag>' + TAGS + r')>(.*?)</(?P=tag)>”'), r'<\g<tag>>“\2”</\g<tag>>'),
    (re.compile(r'“<(?P<tag>' + TAGS + r')>(.*?)</(?P=tag)>"'), r'<\g<tag>>“\2”</\g<tag>>'),
    (re.compile(r'"<(?P<tag>' + TAGS + r')>(.*?)</(?P=tag)>”'), r'<\g<tag>>“\2”</\g<tag>>'),
    (re.compile(r'“<(?P<tag>' + TAGS + r')>(.*?)</(?P=tag)>'), r'<\g<tag>>“\2</\g<tag>>'),
    (re.compile(r'<(?P<tag>' + TAGS + r')>(.*?)</(?P=tag)>”'), r'<\g<tag>>\2”</\g<tag>>'),
    (re.compile(r'"<(?P<tag>' + TAGS + r')>(.*?)</(?P=tag)>'), r'<\g<tag>>"\2</\g<tag>>'),
    (re.compile(r'<(?P<tag>' + TAGS + r')>(.*?)</(?P=tag)>"'), r'<\g<tag>>\2"</\g<tag>>'),
]

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = content
    for pattern, replacement in PATTERNS:
        # Run multiple times to catch overlapping/adjacent tags on same line
        for _ in range(3):
            new_content = pattern.sub(replacement, new_content)
            
    if new_content != content:
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    if not os.path.exists(TAGGED_DIR):
        print(f"Directory not found: {TAGGED_DIR}")
        return
        
    files = sorted([f for f in os.listdir(TAGGED_DIR) if f.startswith("tagged_") and f.endswith(".txt")])
    modified_files = []
    
    print("Scanning and cleaning quotation marks in tagged files...")
    for filename in files:
        filepath = os.path.join(TAGGED_DIR, filename)
        if clean_file(filepath):
            print(f"  [MODIFIED] {filename}")
            modified_files.append(filename)
            
    print("="*60)
    print(f"Complete. Modified {len(modified_files)} files.")
    
    # Save the list of modified files for subsequent steps
    modified_list_path = os.path.join(BASE_DIR, "scratch", "modified_tagged_chapters.txt")
    with open(modified_list_path, 'w', encoding='utf-8') as f:
        for filename in modified_files:
            f.write(filename + "\n")
            
if __name__ == "__main__":
    main()
