import glob
import os
import re

def clean_file_formatting(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split paragraphs by 2 or more newlines (or lines with only whitespace)
    # First, split lines and strip trailing whitespace from each line
    lines = [line.rstrip() for line in text.splitlines()]
    
    # Rejoin with single newlines
    cleaned_text = '\n'.join(lines)
    
    # Replace 3 or more newlines with exactly 2 newlines (\n\n)
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text).strip() + '\n'

    if cleaned_text != text:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        return True
    return False

def main():
    chapters = glob.glob('chapters/*.txt')
    cleaned_files = []

    for fpath in chapters:
        if clean_file_formatting(fpath):
            cleaned_files.append(fpath)

    print(f"=== PARAGRAPH BLANK LINE CLEANUP ===")
    print(f"Cleaned {len(cleaned_files)} files by enforcing exactly 1 blank line between paragraphs:")
    for f in sorted(cleaned_files):
        print(f"  - {f}")

if __name__ == '__main__':
    main()
