import os
import glob

# Path to the chapters directory
chapters_dir = r"d:\git_repo\TKprof_book\books\science_of_getting_rich\chapters"

# Find all modernized chapter files
chapter_files = glob.glob(os.path.join(chapters_dir, "ch_*_en.txt"))

files_modified = 0

for file_path in chapter_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "*" in content:
        # Remove all asterisks
        new_content = content.replace("*", "")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        files_modified += 1
        print(f"Removed asterisks from: {os.path.basename(file_path)}")

print(f"Total files modified: {files_modified}")
