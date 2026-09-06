import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_FILE = os.path.join(BASE_DIR, "the_heroes_raw.txt")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

# Definitions of each chapter / part
# (chapter_index, filename, story_title, part_title, search_header)
CHAPTER_DEFS = [
    (0, "raw_ch_00.txt", "Preface", "Preface: To My Children", "PREFACE"),
    (1, "raw_ch_01.txt", "Story I: Perseus", "Part I: How Perseus and His Mother Came to Seriphos", "PART I\nHOW PERSEUS AND HIS MOTHER CAME TO SERIPHOS"),
    (2, "raw_ch_02.txt", "Story I: Perseus", "Part II: How Perseus Vowed a Rash Vow", "PART II\nHOW PERSEUS VOWED A RASH VOW"),
    (3, "raw_ch_03.txt", "Story I: Perseus", "Part III: How Perseus Slew the Gorgon", "PART III\nHOW PERSEUS SLEW THE GORGON"),
    (4, "raw_ch_04.txt", "Story I: Perseus", "Part IV: How Perseus Came to the Æthiops", "PART IV\nHOW PERSEUS CAME TO THE"),
    (5, "raw_ch_05.txt", "Story I: Perseus", "Part V: How Perseus Came Home Again", "PART V\nHOW PERSEUS CAME HOME AGAIN"),
    (6, "raw_ch_06.txt", "Story II: The Argonauts", "Part I: How the Centaur Trained the Heroes on Pelion", "PART I\nHOW THE CENTAUR TRAINED THE HEROES ON PELION"),
    (7, "raw_ch_07.txt", "Story II: The Argonauts", "Part II: How Jason Lost His Sandal in Anauros", "PART II\nHOW JASON LOST HIS SANDAL IN ANAUROS"),
    (8, "raw_ch_08.txt", "Story II: The Argonauts", "Part III: How They Built the Ship 'Argo' in Iolcos", "PART III\nHOW THEY BUILT THE SHIP"),
    (9, "raw_ch_09.txt", "Story II: The Argonauts", "Part IV: How the Argonauts Sailed to Colchis", "PART IV\nHOW THE ARGONAUTS SAILED TO COLCHIS"),
    (10, "raw_ch_10.txt", "Story II: The Argonauts", "Part V: How the Argonauts Were Driven into the Unknown Sea", "PART V\nHOW THE ARGONAUTS WERE DRIVEN INTO THE UNKNOWN SEA"),
    (11, "raw_ch_11.txt", "Story II: The Argonauts", "Part VI: What Was the End of the Heroes", "PART VI\nWHAT WAS THE END OF THE HEROES"),
    (12, "raw_ch_12.txt", "Story III: Theseus", "Part I: How Theseus Lifted the Stone", "PART I\nHOW THESEUS LIFTED THE STONE"),
    (13, "raw_ch_13.txt", "Story III: Theseus", "Part II: How Theseus Slew the Devourers of Men", "PART II\nHOW THESEUS SLEW THE DEVOURERS OF MEN"),
    (14, "raw_ch_14.txt", "Story III: Theseus", "Part III: How Theseus Slew the Minotaur", "PART III\nHOW THESEUS SLEW THE MINOTAUR"),
    (15, "raw_ch_15.txt", "Story III: Theseus", "Part IV: How Theseus Fell by His Pride", "PART IV\nHOW THESEUS FELL BY HIS PRIDE"),
]

def split_the_heroes():
    if not os.path.exists(RAW_FILE):
        print(f"Error: {RAW_FILE} not found. Run download_book.py first.")
        return

    with open(RAW_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    os.makedirs(CHAPTERS_DIR, exist_ok=True)

    # Locate preface
    pref_start = text.find("\nPREFACE\n")
    pref_end = text.find("\nCONTENTS\n")
    if pref_start == -1:
        pref_start = text.find("PREFACE")
    if pref_end == -1:
        pref_end = text.find("CONTENTS")

    # Positions for chapters 1 to 15
    # Search starts after line of CONTENTS
    body_search_start = pref_end + 500
    positions = []

    for idx, filename, s_title, p_title, header_pat in CHAPTER_DEFS:
        if idx == 0:
            positions.append((idx, filename, s_title, p_title, pref_start, pref_end))
            continue

        lines = header_pat.split("\n")
        first_line = lines[0].strip()
        second_line = lines[1].strip() if len(lines) > 1 else ""

        pos = -1
        # Search for pattern in body
        search_region = text[body_search_start:]
        if second_line:
            pattern = re.escape(first_line) + r"\s*\n\s*" + re.escape(second_line)
            m = re.search(pattern, search_region)
            if m:
                pos = body_search_start + m.start()
        else:
            m = re.search(r"\b" + re.escape(first_line) + r"\b", search_region)
            if m:
                pos = body_search_start + m.start()

        if pos == -1:
            print(f"Warning: Could not locate position for {filename}: {header_pat}")
        else:
            positions.append((idx, filename, s_title, p_title, pos, -1))

    end_marker = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if end_marker == -1:
        end_marker = len(text)

    # Calculate end positions for body chapters
    for i in range(1, len(positions)):
        idx, filename, s_title, p_title, start_p, _ = positions[i]
        if i + 1 < len(positions):
            next_start = positions[i+1][4]
            slice_text = text[start_p:next_start]
            # If there is a STORY title header right before next part, trim before it
            story_match = re.search(r"\n\s*STORY\s+[IVX]+[^\n]*\n", slice_text)
            if story_match:
                end_p = start_p + story_match.start()
            else:
                end_p = next_start
        else:
            end_p = end_marker

        chapter_content = text[start_p:end_p].strip()
        # Clean trailing asterisks / section separators if present at end
        chapter_content = re.sub(r"(\n\s*\*\s*\*\s*\*\s*\*\s*\*)+\s*$", "", chapter_content).strip()

        out_path = os.path.join(CHAPTERS_DIR, filename)
        with open(out_path, "w", encoding="utf-8") as out_f:
            out_f.write(chapter_content + "\n")

        words = len(chapter_content.split())
        print(f"Saved {filename:14s} ({len(chapter_content):6d} chars, {words:5d} words) - {s_title} | {p_title}")

    # Save Preface (idx 0)
    pref_text = text[positions[0][4]:positions[0][5]].strip()
    pref_out = os.path.join(CHAPTERS_DIR, CHAPTER_DEFS[0][1])
    with open(pref_out, "w", encoding="utf-8") as out_f:
        out_f.write(pref_text + "\n")
    print(f"Saved {CHAPTER_DEFS[0][1]:14s} ({len(pref_text):6d} chars, {len(pref_text.split()):5d} words) - Preface")

if __name__ == "__main__":
    split_the_heroes()
