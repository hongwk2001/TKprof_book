import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
JSON_DIR = os.path.join(BASE_DIR, "json")
MASTER_JSON = os.path.join(BASE_DIR, "the_heroes_raw.json")

CHAPTER_INFO = [
    {"index": 0, "id": "ch_00", "file": "raw_ch_00.txt", "story": "Preface", "part": "Preface: To My Children"},
    {"index": 1, "id": "ch_01", "file": "raw_ch_01.txt", "story": "Story I: Perseus", "part": "Part I: How Perseus and His Mother Came to Seriphos"},
    {"index": 2, "id": "ch_02", "file": "raw_ch_02.txt", "story": "Story I: Perseus", "part": "Part II: How Perseus Vowed a Rash Vow"},
    {"index": 3, "id": "ch_03", "file": "raw_ch_03.txt", "story": "Story I: Perseus", "part": "Part III: How Perseus Slew the Gorgon"},
    {"index": 4, "id": "ch_04", "file": "raw_ch_04.txt", "story": "Story I: Perseus", "part": "Part IV: How Perseus Came to the Æthiops"},
    {"index": 5, "id": "ch_05", "file": "raw_ch_05.txt", "story": "Story I: Perseus", "part": "Part V: How Perseus Came Home Again"},
    {"index": 6, "id": "ch_06", "file": "raw_ch_06.txt", "story": "Story II: The Argonauts", "part": "Part I: How the Centaur Trained the Heroes on Pelion"},
    {"index": 7, "id": "ch_07", "file": "raw_ch_07.txt", "story": "Story II: The Argonauts", "part": "Part II: How Jason Lost His Sandal in Anauros"},
    {"index": 8, "id": "ch_08", "file": "raw_ch_08.txt", "story": "Story II: The Argonauts", "part": "Part III: How They Built the Ship 'Argo' in Iolcos"},
    {"index": 9, "id": "ch_09", "file": "raw_ch_09.txt", "story": "Story II: The Argonauts", "part": "Part IV: How the Argonauts Sailed to Colchis"},
    {"index": 10, "id": "ch_10", "file": "raw_ch_10.txt", "story": "Story II: The Argonauts", "part": "Part V: How the Argonauts Were Driven into the Unknown Sea"},
    {"index": 11, "id": "ch_11", "file": "raw_ch_11.txt", "story": "Story II: The Argonauts", "part": "Part VI: What Was the End of the Heroes"},
    {"index": 12, "id": "ch_12", "file": "raw_ch_12.txt", "story": "Story III: Theseus", "part": "Part I: How Theseus Lifted the Stone"},
    {"index": 13, "id": "ch_13", "file": "raw_ch_13.txt", "story": "Story III: Theseus", "part": "Part II: How Theseus Slew the Devourers of Men"},
    {"index": 14, "id": "ch_14", "file": "raw_ch_14.txt", "story": "Story III: Theseus", "part": "Part III: How Theseus Slew the Minotaur"},
    {"index": 15, "id": "ch_15", "file": "raw_ch_15.txt", "story": "Story III: Theseus", "part": "Part IV: How Theseus Fell by His Pride"},
]

def clean_paragraph_text(chunk_text):
    """Joins line wraps within a paragraph and normalizes whitespace."""
    lines = [l.strip() for l in chunk_text.splitlines() if l.strip()]
    return " ".join(lines)

def is_header_paragraph(text):
    """Determines whether a paragraph is a structural heading."""
    t = text.strip()
    if t in ["PREFACE", "MY DEAR CHILDREN,", "THE END"]:
        return True
    if t.startswith("PART ") and len(t) < 120:
        return True
    if t.startswith("STORY ") and len(t) < 80:
        return True
    return False

def make_json():
    os.makedirs(JSON_DIR, exist_ok=True)

    master_data = {
        "title": "The Heroes: Greek Fairy Tales",
        "author": "Charles Kingsley",
        "original_title": "The Heroes; Or, Greek Fairy Tales for My Children",
        "source": "Project Gutenberg eBook #677",
        "total_chapters": len(CHAPTER_INFO),
        "chapters": []
    }

    global_id = 1
    total_words_all = 0

    for ch in CHAPTER_INFO:
        raw_file_path = os.path.join(CHAPTERS_DIR, ch["file"])
        if not os.path.exists(raw_file_path):
            print(f"Warning: {raw_file_path} does not exist.")
            continue

        with open(raw_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split into paragraph blocks (3 or more newlines)
        chunks = [c.strip() for c in re.split(r"\n{3,}", content) if c.strip()]

        chapter_items = []
        normalized_paragraphs = []

        for p_idx, chunk in enumerate(chunks, 1):
            p_clean = clean_paragraph_text(chunk)
            if not p_clean:
                continue

            is_header = is_header_paragraph(p_clean)
            words = len(p_clean.split())
            total_words_all += words

            item = {
                "id": global_id,
                "tag": f"P{global_id:04d}",
                "chapter_id": ch["id"],
                "story": ch["story"],
                "part": ch["part"],
                "raw": p_clean,
                "en": "",
                "ko": "",
                "is_header": is_header,
                "word_count": words
            }
            chapter_items.append(item)
            normalized_paragraphs.append(p_clean)
            global_id += 1

        # Save individual chapter JSON
        ch_json_filename = f"{ch['id']}.json"
        ch_json_path = os.path.join(JSON_DIR, ch_json_filename)
        with open(ch_json_path, "w", encoding="utf-8") as out_f:
            json.dump(chapter_items, out_f, ensure_ascii=False, indent=2)

        # Update raw chapter txt file with cleanly normalized paragraphs (\n\n separated)
        with open(raw_file_path, "w", encoding="utf-8") as out_txt:
            out_txt.write("\n\n".join(normalized_paragraphs) + "\n")

        ch_data = {
            "chapter_id": ch["id"],
            "story": ch["story"],
            "part": ch["part"],
            "paragraph_count": len(chapter_items),
            "word_count": sum(it["word_count"] for it in chapter_items),
            "paragraphs": chapter_items
        }
        master_data["chapters"].append(ch_data)

        print(f"Processed {ch['id']}: {len(chapter_items):3d} items ({ch_data['word_count']:5d} words) -> {ch_json_filename}")

    master_data["total_items"] = global_id - 1
    master_data["total_words"] = total_words_all

    # Save Master JSON
    with open(MASTER_JSON, "w", encoding="utf-8") as mf:
        json.dump(master_data, mf, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully generated Master JSON: {MASTER_JSON}")
    print(f"Total Chapters: {len(CHAPTER_INFO)}, Total Paragraph Blocks: {global_id - 1}, Total Words: {total_words_all}")

if __name__ == "__main__":
    make_json()
