import os
import re

BASE_DIR = r"d:\git_repo\TKprof_book\books\the_enchanted_april"
RAW_FILE = os.path.join(BASE_DIR, "the_enchanted_april_raw.txt")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

if not os.path.exists(CHAPTERS_DIR):
    os.makedirs(CHAPTERS_DIR)

# Matches "Chapter 1", "Chapter 22", etc.
CHAPTER_PATTERN = re.compile(r"^Chapter \d+$", re.IGNORECASE)
END_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK"

current_chapter = 0
current_content = []

print("Starting segmentation...")

with open(RAW_FILE, "r", encoding="utf-8") as f:
    for line in f:
        # Check for Project Gutenberg end marker
        if END_MARKER in line:
            break
            
        # Check if line is a chapter header (must be exactly at start of line)
        cleaned_line = line.rstrip("\r\n")
        if CHAPTER_PATTERN.match(cleaned_line):
            # Save preceding content (e.g. Gutenberg metadata if current_chapter is 0)
            out_file = os.path.join(CHAPTERS_DIR, f"raw_ch_{current_chapter:02d}.txt")
            with open(out_file, "w", encoding="utf-8") as out:
                out.write("".join(current_content))
            print(f"Saved track {current_chapter} -> {os.path.basename(out_file)}")
            
            # Start new chapter
            current_chapter += 1
            current_content = [line]
        else:
            current_content.append(line)

# Save the final chapter
if current_content:
    out_file = os.path.join(CHAPTERS_DIR, f"raw_ch_{current_chapter:02d}.txt")
    with open(out_file, "w", encoding="utf-8") as out:
        out.write("".join(current_content))
    print(f"Saved track {current_chapter} -> {os.path.basename(out_file)}")

print("Segmentation complete.")
