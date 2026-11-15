import os
import json
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
MASTER_JSON = os.path.join(BASE_DIR, "the_heroes_raw.json")
MAX_CHARS = 200

def split_text_to_sentences(text, max_chars=MAX_CHARS):
    if not text or not text.strip():
        return []

    t = text.strip()

    if len(t) <= max_chars:
        return [{"id": 1, "text": t}]

    # Regex split: fixed-width lookbehinds for terminal punctuation with/without closing quotes
    pattern = r'(?:(?<=[.!?])|(?<=[.!?][\"\'”’]))\s+(?=[A-Z0-9\"\'“‘\[])'
    raw_sents = re.split(pattern, t)

    preliminary = []
    for s in raw_sents:
        s = s.strip()
        if not s:
            continue
        if len(s) > max_chars:
            # Try splitting on semicolons, colons, or em-dashes
            sub_parts = re.split(r'(?<=[;:—])\s+', s)
            for sp in sub_parts:
                sp = sp.strip()
                if not sp:
                    continue
                if len(sp) > max_chars:
                    # Further split on commas if still oversized
                    comma_parts = re.split(r'(?<=,)\s+', sp)
                    current_chunk = ""
                    for cp in comma_parts:
                        if len(current_chunk) + len(cp) + 1 <= max_chars:
                            current_chunk = f"{current_chunk} {cp}".strip()
                        else:
                            if current_chunk:
                                preliminary.append(current_chunk)
                            current_chunk = cp
                    if current_chunk:
                        preliminary.append(current_chunk)
                else:
                    preliminary.append(sp)
        else:
            preliminary.append(s)

    result = []
    for idx, sent in enumerate(preliminary, 1):
        clean_s = sent.strip().strip('"\'“”')
        # Remove any dangling or residual dialogue quotes that could confuse TTS prosody
        clean_s = clean_s.replace('"', '').replace('“', '').replace('”', '').strip()
        if clean_s:
            result.append({
                "id": len(result) + 1,
                "text": clean_s
            })
    return result

def process_all_json_files():
    # Reload from batches to get clean source strings
    batch_file = os.path.join(BASE_DIR, "batches", "batch_ch00_ch01.json")
    batch_dict = {}
    if os.path.exists(batch_file):
        with open(batch_file, "r", encoding="utf-8") as bf:
            b_items = json.load(bf)
            for it in b_items:
                if "id" in it and "en" in it:
                    batch_dict[it["id"]] = it["en"]

    ch_files = sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json")))
    total_sentences = 0
    oversized_sentences = 0

    for ch_path in ch_files:
        with open(ch_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        ch_updated = False
        ch_sents = 0

        for it in items:
            it_id = it["id"]
            if it_id in batch_dict:
                raw_en_string = batch_dict[it_id]
                sents = split_text_to_sentences(raw_en_string)
                it["en"] = sents
                ch_updated = True
                ch_sents += len(sents)
                for s in sents:
                    if len(s["text"]) > MAX_CHARS:
                        oversized_sentences += 1
                        print(f"Warning: Sentence exceeds {MAX_CHARS} chars ({len(s['text'])}): {s['text']}")
            else:
                if not isinstance(it.get("en"), list):
                    it["en"] = []
                    ch_updated = True

            if not isinstance(it.get("ko"), list):
                it["ko"] = []
                ch_updated = True

        if ch_updated:
            with open(ch_path, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            if ch_sents > 0:
                print(f"{os.path.basename(ch_path)}: {len(items)} paragraphs -> {ch_sents} sentences.")
            total_sentences += ch_sents

    # Update Master JSON
    if os.path.exists(MASTER_JSON):
        with open(MASTER_JSON, "r", encoding="utf-8") as mf:
            master = json.load(mf)

        for ch in master.get("chapters", []):
            ch_id = ch["chapter_id"]
            ch_json_file = os.path.join(JSON_DIR, f"{ch_id}.json")
            if os.path.exists(ch_json_file):
                with open(ch_json_file, "r", encoding="utf-8") as f:
                    updated_paras = json.load(f)
                ch["paragraphs"] = updated_paras

        with open(MASTER_JSON, "w", encoding="utf-8") as mf:
            json.dump(master, mf, ensure_ascii=False, indent=2)
        print(f"Master JSON updated: {MASTER_JSON}")

    print(f"\nCompleted sentence splitting.")
    print(f"Total structured sentences in modernized chapters: {total_sentences}")
    print(f"Oversized sentences (> {MAX_CHARS} chars): {oversized_sentences}")

if __name__ == "__main__":
    process_all_json_files()
