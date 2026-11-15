"""
Build json/ch_01.json .. ch_15.json (and the master werther_raw.json)
from the chapter files written by split_chapters.py.

Each paragraph becomes one item with an empty `en` (modernized English)
and `ko` (Korean) awaiting Stages 4 and 5. Chapter definitions are
imported from split_chapters so the two scripts cannot drift apart.

Werther-specific: every item carries the `letter` it belongs to (the
date header above it, e.g. "MAY 4."), so a translator always knows whose
voice is speaking and when. Paragraphs in the Editor's narration carry
`letter: null`.

Items carry only `chapter_id` and `section`, not the chapter titles --
titles live once per chapter in the master JSON and are joined on
`chapter_id` when a translation batch needs them.
"""

import os
import re
import json

from split_chapters import CHAPTER_DEFS, LETTER_RE, CHAPTERS_DIR

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
MASTER_JSON = os.path.join(BASE_DIR, "werther_raw.json")

# Structural headings that are not letter dates.
STATIC_HEADERS = {"PREFACE", "THE EDITOR TO THE READER."}

# Inside the Editor's section a dated letter is followed by narration with no
# header of its own, so `current_letter` would keep attributing the editor's
# prose to Werther. These opening phrases mark narration resuming; matching
# paragraphs (and those after them) revert to letter: null until the next date.
EDITOR_RESUME = (
    "Under the circumstances narrated above",
)


def clean_paragraph_text(chunk_text):
    """Join line wraps within a paragraph and normalize whitespace."""
    lines = [l.strip() for l in chunk_text.splitlines() if l.strip()]
    return " ".join(lines)


def is_header_paragraph(text):
    """A letter date header or a section heading."""
    t = text.strip()
    return bool(LETTER_RE.match(t)) or t in STATIC_HEADERS


def make_json():
    os.makedirs(JSON_DIR, exist_ok=True)

    master = {
        "title": "The Sorrows of Young Werther",
        "author": "Johann Wolfgang von Goethe",
        "original_title": "Die Leiden des jungen Werthers",
        "translator": "R. Dillon Boylan",
        "source": "Project Gutenberg eBook #2527",
        "total_chapters": len(CHAPTER_DEFS),
        "chapters": [],
    }

    global_id = 1
    total_words_all = 0
    total_letters = 0

    for idx, filename, section, title_en, title_ko, _anchor in CHAPTER_DEFS:
        ch_id = f"ch_{idx:02d}"
        raw_path = os.path.join(CHAPTERS_DIR, filename)
        if not os.path.exists(raw_path):
            print(f"Warning: {raw_path} does not exist. Run split_chapters.py first.")
            continue

        with open(raw_path, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = [c for c in re.split(r"\n{2,}", content) if c.strip()]

        items = []
        current_letter = None
        for chunk in chunks:
            p_clean = clean_paragraph_text(chunk)
            if not p_clean:
                continue

            header = is_header_paragraph(p_clean)
            if header and LETTER_RE.match(p_clean):
                current_letter = p_clean
                total_letters += 1
            elif p_clean.startswith(EDITOR_RESUME):
                current_letter = None

            words = len(p_clean.split())
            total_words_all += words

            items.append({
                "id": global_id,
                "tag": f"P{global_id:04d}",
                "chapter_id": ch_id,
                "section": section,
                "letter": current_letter,
                "raw": p_clean,
                "en": "",
                "ko": "",
                "is_header": header,
                "word_count": words,
            })
            global_id += 1

        ch_path = os.path.join(JSON_DIR, f"{ch_id}.json")
        with open(ch_path, "w", encoding="utf-8") as out_f:
            json.dump(items, out_f, ensure_ascii=False, indent=2)

        ch_words = sum(it["word_count"] for it in items)
        ch_letters = sum(1 for it in items if it["is_header"] and LETTER_RE.match(it["raw"]))
        master["chapters"].append({
            "chapter_id": ch_id,
            "section": section,
            "title_en": title_en,
            "title_ko": title_ko,
            "paragraph_count": len(items),
            "letter_count": ch_letters,
            "word_count": ch_words,
            "paragraphs": items,
        })

        print(f"Processed {ch_id}: {len(items):3d} items "
              f"({ch_letters:2d} letters, {ch_words:5d} words) -> json/{ch_id}.json")

    master["total_items"] = global_id - 1
    master["total_words"] = total_words_all
    master["total_letters"] = total_letters

    with open(MASTER_JSON, "w", encoding="utf-8") as mf:
        json.dump(master, mf, ensure_ascii=False, indent=2)

    print(f"\nMaster JSON: {MASTER_JSON}")
    print(f"Chapters: {len(master['chapters'])}, Items: {global_id - 1}, "
          f"Letters: {total_letters}, Words: {total_words_all}")


if __name__ == "__main__":
    make_json()
