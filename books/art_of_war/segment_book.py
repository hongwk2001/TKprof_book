import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_FILE = os.path.join(SCRIPT_DIR, "art_of_war_raw.txt")
CHAPTERS_DIR = os.path.join(SCRIPT_DIR, "chapters")
os.makedirs(CHAPTERS_DIR, exist_ok=True)

CHAPTER_TITLES = [
    "I. LAYING PLANS",
    "II. WAGING WAR",
    "III. ATTACK BY STRATAGEM",
    "IV. TACTICAL DISPOSITIONS",
    "V. ENERGY",
    "VI. WEAK POINTS AND STRONG",
    "VII. MANEUVERING",
    "VIII. VARIATION OF TACTICS",
    "IX. THE ARMY ON THE MARCH",
    "X. TERRAIN",
    "XI. THE NINE SITUATIONS",
    "XII. THE ATTACK BY FIRE",
    "XIII. THE USE OF SPIES"
]

def segment_art_of_war():
    with open(RAW_FILE, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Find the main body starting around Chapter I. LAYING PLANS
    start_pos = content.find("Chapter I. LAYING PLANS")
    if start_pos == -1:
        start_pos = content.find("Chapter I.")
    
    # End of main text (Project Gutenberg footer)
    end_pos = content.find("END OF THE PROJECT GUTENBERG EBOOK")
    if end_pos != -1:
        content = content[start_pos:end_pos]
    else:
        content = content[start_pos:]

    # Split by Chapter headers
    pattern = r'(Chapter\s+(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|XIII)\.\s+.*)'
    parts = re.split(pattern, content)

    chapters = []
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i+1].strip() if i+1 < len(parts) else ""
        chapters.append((header, body))

    print(f"Found {len(chapters)} chapter blocks.")

    for idx, (header, body) in enumerate(chapters, 1):
        ch_str = str(idx).zfill(2)
        out_filename = f"ch_{ch_str}_en.txt"
        out_path = os.path.join(CHAPTERS_DIR, out_filename)

        # Fix encoding artifacts like MANUVERING
        clean_header = re.sub(r'MAN.*UVERING', 'MANEUVERING', header, flags=re.IGNORECASE)
        clean_body = body.replace('MANUVERING', 'MANEUVERING')

        full_text = f"{clean_header}\n\n{clean_body}\n"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"Saved Chapter {ch_str}: {out_filename} ({len(full_text)} chars)")

if __name__ == "__main__":
    segment_art_of_war()
