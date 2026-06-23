import os
import re

source_path = "D:/git_repo/TKprof_book/books/blue_castle/the_blue_castle.txt"
output_dir = "D:/git_repo/TKprof_book/books/blue_castle/chapters"

os.makedirs(output_dir, exist_ok=True)

with open(source_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_chapter = 0
current_content = []

chapter_pattern = re.compile(r'^CHAPTER\s+[IVXLCDM]+\.?\s*$')

for line in lines:
    if chapter_pattern.match(line):
        # Save previous chapter if there is content
        if current_content:
            output_file = os.path.join(output_dir, f"raw_ch_{current_chapter:02d}.txt")
            with open(output_file, 'w', encoding='utf-8') as out:
                out.writelines(current_content)
        
        # Start new chapter
        current_chapter += 1
        current_content = [line]
    else:
        current_content.append(line)

# Save the last chapter
if current_content:
    output_file = os.path.join(output_dir, f"raw_ch_{current_chapter:02d}.txt")
    with open(output_file, 'w', encoding='utf-8') as out:
        out.writelines(current_content)

print(f"Successfully segmented {current_chapter} chapters into {output_dir}")
