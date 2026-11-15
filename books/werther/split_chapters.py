"""
Split werther_raw.txt into 15 chapter files under chapters/.

The novel is epistolary: 84 dated letters plus a closing third-person
narration. Letters are far too uneven to be chapters on their own
(18 to 3,042 words), so chapters are defined as spans of letters,
anchored on their date headers. The Editor's narration carries no date
headers and is anchored on scene-opening sentences instead.

Source note: the Gutenberg text is double-spaced -- wrapped lines are
separated by one blank line and paragraphs by two. normalize() collapses
that so paragraphs are ordinary blank-line-separated blocks.
"""

import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_FILE = os.path.join(BASE_DIR, "werther_raw.txt")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

# Anchors are matched against the start of a normalized line.
# (index, filename, section, title_en, title_ko, start_anchor)
# Each chapter runs from its own anchor up to the next chapter's anchor.
CHAPTER_DEFS = [
    (1,  "raw_ch_01.txt", "Book I",  "Arrival",
     "도착", "PREFACE"),
    (2,  "raw_ch_02.txt", "Book I",  "Wahlheim",
     "발하임", "MAY 22."),
    (3,  "raw_ch_03.txt", "Book I",  "The Ball",
     "무도회", "JUNE 16."),
    (4,  "raw_ch_04.txt", "Book I",  "In Love",
     "사랑에 빠지다", "JUNE 19."),
    (5,  "raw_ch_05.txt", "Book I",  "Albert",
     "알베르트", "JULY 6."),
    (6,  "raw_ch_06.txt", "Book I",  "The Pistols",
     "권총", "AUGUST 8."),
    (7,  "raw_ch_07.txt", "Book I",  "Departure",
     "이별", "AUGUST 15."),
    (8,  "raw_ch_08.txt", "Book II", "In the Ambassador's Service",
     "공사관에서", "BOOK II."),
    (9,  "raw_ch_09.txt", "Book II", "Disgrace and Departure",
     "모욕과 사직", "MARCH 15."),
    (10, "raw_ch_10.txt", "Book II", "Return to Wahlheim",
     "발하임으로 돌아오다", "AUGUST 4."),
    (11, "raw_ch_11.txt", "Book II", "Descent",
     "무너져 가는 마음", "NOVEMBER 3."),
    (12, "raw_ch_12.txt", "Editor",  "The Editor to the Reader",
     "엮은이가 독자에게", "THE EDITOR TO THE READER."),
    (13, "raw_ch_13.txt", "Editor",  "The Last Visit",
     "마지막 방문", "We find it difficult to express the emotions"),
    (14, "raw_ch_14.txt", "Editor",  "Ossian",
     "오시안", '"Star of descending night! fair is thy light'),
    (15, "raw_ch_15.txt", "Editor",  "The Final Night",
     "마지막 밤", "Werther ran to the gate of the town."),
]

# Matches a letter date header and nothing else. Must stay case-SENSITIVE:
# a case-insensitive version also matches wrapped lines starting "may ...".
LETTER_RE = re.compile(
    r"^(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER"
    r"|OCTOBER|NOVEMBER|DECEMBER) \d+[.,]?(\s*\d{4})?\.?$"
)


def normalize(text):
    """Collapse the source's double-spacing into ordinary paragraphs."""
    return text.replace("\n\n", "\n")


def find_anchor(lines, anchor, search_from):
    """Line index of the first line at or after search_from starting with anchor."""
    for i in range(search_from, len(lines)):
        if lines[i].strip().startswith(anchor):
            return i
    return -1


def split_werther():
    if not os.path.exists(RAW_FILE):
        print(f"Error: {RAW_FILE} not found. Run download_book.py first.")
        return

    with open(RAW_FILE, "r", encoding="utf-8") as f:
        lines = normalize(f.read()).split("\n")

    start_marker = find_anchor(lines, "*** START", 0)
    end_marker = find_anchor(lines, "*** END", 0)
    if end_marker == -1:
        end_marker = len(lines)

    os.makedirs(CHAPTERS_DIR, exist_ok=True)

    # Resolve every anchor to a line index, scanning forward so that
    # repeated dates (SEPTEMBER 3 appears in both books) resolve in order.
    positions = []
    cursor = start_marker + 1
    for defn in CHAPTER_DEFS:
        idx, filename, section, t_en, t_ko, anchor = defn
        pos = find_anchor(lines, anchor, cursor)
        if pos == -1:
            print(f"Warning: could not locate anchor for {filename}: {anchor!r}")
            continue
        positions.append((defn, pos))
        cursor = pos + 1

    if len(positions) != len(CHAPTER_DEFS):
        print("Aborting: not every chapter anchor was found.")
        return

    total_words = 0
    for i, (defn, start_p) in enumerate(positions):
        idx, filename, section, t_en, t_ko, _ = defn
        end_p = positions[i + 1][1] if i + 1 < len(positions) else end_marker

        body = "\n".join(lines[start_p:end_p]).strip()
        # Drop the standalone "BOOK I" / "BOOK II." section banners; the
        # chapter title carries that information already.
        body = re.sub(r"^BOOK I{1,2}\.?\s*$", "", body, flags=re.M).strip()

        out_path = os.path.join(CHAPTERS_DIR, filename)
        with open(out_path, "w", encoding="utf-8") as out_f:
            out_f.write(body + "\n")

        words = len(body.split())
        letters = sum(1 for l in body.split("\n") if LETTER_RE.match(l.strip()))
        total_words += words
        print(f"Saved {filename:14s} ({words:5d} words, {letters:2d} letters) "
              f"- {section} | {t_en} / {t_ko}")

    print(f"\nSplit complete: {len(positions)} chapters, {total_words} words.")


if __name__ == "__main__":
    split_werther()
