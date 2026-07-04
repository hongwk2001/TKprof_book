import os
import re

BASE_DIR = r"d:\git_repo\TKprof_book\books\meditations"
RAW_FILE = os.path.join(BASE_DIR, "meditations_chrystal_raw.txt")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

os.makedirs(CHAPTERS_DIR, exist_ok=True)

def segment_book():
    with open(RAW_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    chapters = {}
    current_chapter = 0
    buffer = []
    
    # Regex for catching "BOOK I.", "BOOK II.", etc.
    header_pattern = re.compile(r'^\s*BOOK [IVX]+\.\s*$')
    end_pattern = re.compile(r'\*\*\* END OF THE PROJECT GUTENBERG EBOOK')

    recording = False

    for line in lines:
        if end_pattern.search(line):
            if current_chapter > 0:
                chapters[current_chapter] = buffer
            break
            
        if header_pattern.match(line):
            if current_chapter > 0:
                chapters[current_chapter] = buffer
            current_chapter += 1
            recording = True
            buffer = []
            
        if recording:
            buffer.append(line)

    print(f"Found {len(chapters)} chapters.")

    for ch_num, ch_lines in chapters.items():
        ch_text = "".join(ch_lines).strip()
        out_file = os.path.join(CHAPTERS_DIR, f"raw_ch_{ch_num:02d}.txt")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(ch_text)
        print(f"Saved {out_file} (length: {len(ch_text)} chars)")

if __name__ == "__main__":
    segment_book()
