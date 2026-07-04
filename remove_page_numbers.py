import os
import re

def main():
    books_dir = r"d:\git_repo\TKprof_book\books"
    pattern = re.compile(r'^\s*\d+\s*$')
    count_files_modified = 0
    count_lines_removed = 0

    for root, dirs, files in os.walk(books_dir):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                modified = False
                for line in lines:
                    if pattern.match(line):
                        modified = True
                        count_lines_removed += 1
                    else:
                        new_lines.append(line)
                
                if modified:
                    count_files_modified += 1
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"Modified: {filepath}")

    print(f"\nDone. Removed {count_lines_removed} page numbers across {count_files_modified} files.")

if __name__ == "__main__":
    main()
