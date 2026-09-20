import os
import sys
import re
import json

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def load_tagged_paragraphs(filepath):
    """
    Reads a tagged chapter text file and returns an ordered list of (tag, text) tuples.
    """
    paragraphs = []
    if not os.path.exists(filepath):
        return paragraphs
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by double newline or search for tag blocks
    raw_blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    for block in raw_blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        full_block_text = " ".join(lines)
        match = re.match(r"^\[(P[a-zA-Z0-9_]+)\]\s*(.*)$", full_block_text)
        if match:
            tag = match.group(1)
            text = match.group(2).strip()
            paragraphs.append((tag, text))
    return paragraphs

def prepare_chapter_script(ch_num, chapters_dir, scripts_out_dir):
    ch_str = f"{ch_num:02d}"
    en_file = os.path.join(chapters_dir, f"ch{ch_str}_en.txt")
    ko_file = os.path.join(chapters_dir, f"ch{ch_str}_ko.txt")

    if not os.path.exists(en_file) or not os.path.exists(ko_file):
        print(f"[ERROR] Chapter {ch_num} source files missing.")
        return False

    en_paras = load_tagged_paragraphs(en_file)
    ko_paras = load_tagged_paragraphs(ko_file)

    en_dict = dict(en_paras)
    ko_dict = dict(ko_paras)

    # Get ordered unique tags preserving EN order
    en_tags = [t for t, _ in en_paras]
    ko_tags = [t for t, _ in ko_paras]

    if en_tags != ko_tags:
        print(f"[WARNING] Chapter {ch_num} tag sequence mismatch! EN len={len(en_tags)}, KO len={len(ko_tags)}")

    script_items = []
    item_id = 1

    for tag in en_tags:
        en_text = en_dict.get(tag, "")
        ko_text = ko_dict.get(tag, "")

        if not en_text or not ko_text:
            print(f"  [WARNING] Missing text for tag [{tag}] in Ch {ch_num}")
            continue

        clean_en = en_text.strip('"\'“”').strip()
        clean_ko = ko_text.strip('"\'“”').strip()

        # EN segment
        script_items.append({
            "id": item_id,
            "tag": tag,
            "lang": "en",
            "text": clean_en
        })
        item_id += 1

        # KO segment
        script_items.append({
            "id": item_id,
            "tag": tag,
            "lang": "ko",
            "text": clean_ko
        })
        item_id += 1

    out_file = os.path.join(scripts_out_dir, f"bilingual_ch_{ch_str}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(script_items, f, indent=2, ensure_ascii=False)

    print(f"  -> Generated Chapter {ch_str}: {out_file} ({len(script_items)} segments / {len(en_tags)} pairs)")
    return True

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    chapters_dir = os.path.join(script_dir, "chapters")
    scripts_out_dir = os.path.join(script_dir, "scripts")
    os.makedirs(scripts_out_dir, exist_ok=True)

    print("==================================================")
    print("Preparing Dracula Bilingual Scripts (Chapters 1..27)")
    print("==================================================")

    success_count = 0
    for ch in range(1, 28):
        if prepare_chapter_script(ch, chapters_dir, scripts_out_dir):
            success_count += 1

    print(f"\n[SUMMARY] Successfully generated scripts for {success_count}/27 chapters.")

if __name__ == "__main__":
    main()
