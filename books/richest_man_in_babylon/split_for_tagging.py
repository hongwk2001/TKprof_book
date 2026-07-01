import os
import glob

CHAPTERS_DIR = "chapters"

# Get all modernized chapters (excluding frontmatter, intro, etc if they don't have dialogue, but let's just do all ch_*_en.txt)
chapter_files = sorted(glob.glob(os.path.join(CHAPTERS_DIR, "ch_*_en.txt")))

MAX_LINES = 150

for file_path in chapter_files:
    filename = os.path.basename(file_path)
    if "frontmatter" in filename or "about_the_author" in filename or "foreword" in filename:
        continue
    
    chapter_prefix = filename.split('_en.txt')[0] # e.g. ch_04_the_man_who_desired_gold
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    part_num = 1
    current_chunk = []
    
    for line in lines:
        current_chunk.append(line)
        if len(current_chunk) >= MAX_LINES and line.strip() == "":
            out_name = f"{chapter_prefix}_part{part_num}.txt"
            with open(os.path.join(CHAPTERS_DIR, out_name), 'w', encoding='utf-8') as out:
                out.writelines(current_chunk)
            print(f"Created {out_name}")
            part_num += 1
            current_chunk = []
            
    if current_chunk:
        out_name = f"{chapter_prefix}_part{part_num}.txt"
        with open(os.path.join(CHAPTERS_DIR, out_name), 'w', encoding='utf-8') as out:
            out.writelines(current_chunk)
        print(f"Created {out_name}")
