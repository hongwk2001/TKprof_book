import os
import glob
import re

chapters_dir = r"d:\git_repo\TKprof_book\books\science_of_getting_rich\chapters"
chapter_files = glob.glob(os.path.join(chapters_dir, "ch_*_en.txt"))

for file_path in chapter_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # We are looking for something like [Chapter 14: The Impression of Increase]
    # or [Preface]
    
    def replace_header(match):
        header_text = match.group(1)
        if ":" in header_text:
            parts = header_text.split(":", 1)
            return f"{parts[0].strip()}\n{parts[1].strip()}"
        else:
            return header_text.strip()
            
    new_content = re.sub(r"^\[(.*?)\]", replace_header, content, flags=re.MULTILINE)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Fixed headers in {os.path.basename(file_path)}")
