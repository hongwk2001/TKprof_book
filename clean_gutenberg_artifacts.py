import glob
import re
import os

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Gutenberg often uses __word__ for italics, we can just replace __ with empty string
    new_content = content.replace('__', '')
    
    # Replace -- with em dash
    new_content = new_content.replace('--', '—')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    en_files = glob.glob('books/dracula/chapters/ch*_en.txt')
    ko_files = glob.glob('books/dracula/chapters/ch*_ko.txt')
    
    all_files = en_files + ko_files
    
    changed = 0
    for f in all_files:
        if clean_file(f):
            changed += 1
            print(f"Cleaned {f}")
            
    print(f"Cleaned {changed} files.")

if __name__ == '__main__':
    main()
