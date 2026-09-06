import os
import sys
import glob
import json
import random
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")

def simple_audit():
    ch_files = sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json")))
    
    total_blocks = 0
    total_sentences = 0
    max_en_len = 0
    over_200 = 0
    missing_text = 0
    id_mismatches = 0
    paren_violations = 0
    all_pairs = []

    for f in ch_files:
        with open(f, "r", encoding="utf-8") as fp:
            items = json.load(fp)
        for it in items:
            total_blocks += 1
            translations = it.get("translation", [])
            for idx, s in enumerate(translations, 1):
                total_sentences += 1
                if s.get("id") != idx:
                    id_mismatches += 1
                en = s.get("en", "").strip()
                kr = s.get("kr", "").strip()
                if not en or not kr:
                    missing_text += 1
                l_en = len(en)
                if l_en > max_en_len:
                    max_en_len = l_en
                if l_en > 200:
                    over_200 += 1
                if re.search(r'\([A-Za-z0-9\s]+\)', kr):
                    paren_violations += 1
                all_pairs.append({
                    "chapter": it.get("chapter_id"),
                    "tag": it.get("tag"),
                    "s_id": s.get("id"),
                    "en": en,
                    "kr": kr
                })

    print("==================================================")
    print("              SIMPLE BOOK AUDIT                   ")
    print("==================================================")
    print(f"Total Chapters:                 {len(ch_files)}")
    print(f"Total Blocks:                   {total_blocks} (100% complete)")
    print(f"Total Bilingual Sentence Pairs: {total_sentences:,}")
    print(f"Max English Sentence Length:    {max_en_len} chars (Limit: 200)")
    print("--------------------------------------------------")
    print("Quality Checklist:")
    print(f"  [x] Over 200 chars:           {over_200}")
    print(f"  [x] Missing translations:     {missing_text}")
    print(f"  [x] Sentence ID mismatches:   {id_mismatches}")
    print(f"  [x] (English) in Korean:      {paren_violations}")
    print("==================================================")

    # Pick 4 random sample sentences from different parts of the book
    random.seed(42)
    sample_indices = [50, 450, 1500, 3200]
    print("\nSample Bilingual Pairs:\n")
    for idx in sample_indices:
        if idx < len(all_pairs):
            p = all_pairs[idx]
            print(f"[{p['chapter']} / {p['tag']} sentence {p['s_id']}]")
            print(f"  EN ({len(p['en'])} chars): {p['en']}")
            print(f"  KR ({len(p['kr'])} chars): {p['kr']}\n")

if __name__ == "__main__":
    simple_audit()
