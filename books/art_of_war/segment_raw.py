import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_FILE = os.path.join(SCRIPT_DIR, "art_of_war_raw.txt")
RAW_CHAPTERS_DIR = os.path.join(SCRIPT_DIR, "raw_chapters")
os.makedirs(RAW_CHAPTERS_DIR, exist_ok=True)

def segment_raw():
    with open(RAW_FILE, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    start_pos = content.find("Chapter I. LAYING PLANS")
    end_pos = content.find("END OF THE PROJECT GUTENBERG EBOOK")
    if end_pos != -1:
        content = content[start_pos:end_pos]
    else:
        content = content[start_pos:]

    pattern = r'(Chapter\s+(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII)\.\s+.*)'
    parts = re.split(pattern, content)

    chapters = []
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i+1].strip() if i+1 < len(parts) else ""
        chapters.append((header, body))

    print(f"Segmented {len(chapters)} raw chapter blocks.")

    for idx, (header, body) in enumerate(chapters, 1):
        ch_str = str(idx).zfill(2)
        out_filename = f"raw_ch_{ch_str}.txt"
        out_path = os.path.join(RAW_CHAPTERS_DIR, out_filename)

        clean_header = re.sub(r'MAN.*UVERING', 'MANEUVERING', header, flags=re.IGNORECASE)
        full_text = f"{clean_header}\n\n{body}\n"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"Saved {out_filename} ({len(full_text)} chars)")

if __name__ == "__main__":
    segment_raw()
