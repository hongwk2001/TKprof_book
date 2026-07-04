import os
import re

BASE_DIR = r"d:\git_repo\TKprof_book\books\think_and_grow_rich"
RAW_FILE = os.path.join(BASE_DIR, "think_and_grow_rich_raw.txt")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

if not os.path.exists(CHAPTERS_DIR):
    os.makedirs(CHAPTERS_DIR)

# The chapters are exactly formatted as "1. Introduction", "2. Desire", etc.
# without leading whitespace in the body of the text.
CHAPTER_PATTERN = re.compile(r"^([1-9]|1[0-5])\.\s+[A-Z]")

current_chapter = 0
current_content = []

with open(RAW_FILE, "r", encoding="utf-8") as f:
    for line in f:
        # Check if line matches exactly "1. Introduction", etc. (no leading tabs/spaces)
        if CHAPTER_PATTERN.match(line):
            # Save the current accumulated content to the previous chapter file
            out_file = os.path.join(CHAPTERS_DIR, f"raw_ch_{current_chapter:02d}.txt")
            with open(out_file, "w", encoding="utf-8") as out:
                out.write("".join(current_content))
            print(f"Saved chapter {current_chapter} -> {os.path.basename(out_file)}")
            
            # Start the new chapter
            current_chapter += 1
            current_content = [line]
        else:
            current_content.append(line)

# Save the final chapter
out_file = os.path.join(CHAPTERS_DIR, f"raw_ch_{current_chapter:02d}.txt")
with open(out_file, "w", encoding="utf-8") as out:
    out.write("".join(current_content))
print(f"Saved chapter {current_chapter} -> {os.path.basename(out_file)}")
