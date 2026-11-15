import os
import sys
import json
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
MASTER_PATH = os.path.join(BASE_DIR, "the_heroes_raw.json")

def run_audit():
    print("================================================================")
    print("   THE HEROES (CHARLES KINGSLEY) - COMPLETE BOOK AUDIT")
    print("================================================================\n")

    ch_files = sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json")))
    if len(ch_files) != 16:
        print(f"ERROR: Expected 16 chapter files, found {len(ch_files)}")
        return False

    total_blocks = 0
    total_sentences = 0
    en_lengths = []
    kr_lengths = []
    
    over_200 = 0
    missing_en = 0
    missing_kr = 0
    id_mismatches = 0
    parenthetical_violations = 0
    untranslated_headers = 0
    quote_violations = 0

    chapter_stats = []

    asterisk_dividers = 0
    footnote_artifacts = 0
    expected_block_id = 1

    for ch_file in ch_files:
        fname = os.path.basename(ch_file)
        with open(ch_file, "r", encoding="utf-8") as f:
            items = json.load(f)

        ch_sents = 0
        ch_over = 0
        ch_max_en = 0

        for it in items:
            total_blocks += 1
            b_id = it.get("id")
            tag = it.get("tag", "")
            raw = it.get("raw", "").strip()

            # Check for non-narrative artifacts
            if raw == "* * * * *" or re.fullmatch(r'[\*\s]+', raw):
                asterisk_dividers += 1
                print(f"[{fname}] Lingering divider found in {tag}: {raw}")
            if raw == "Footnotes" or re.match(r'^\{\d+[a-z]?\}', raw) or "Printed by" in raw:
                footnote_artifacts += 1
                print(f"[{fname}] Lingering metadata artifact in {tag}: {raw}")

            # Continuity check
            if b_id != expected_block_id:
                print(f"[{fname}] Block ID gap: expected {expected_block_id}, got {b_id}")
            expected_block_id += 1

            translations = it.get("translation", [])
            if not translations:
                print(f"[{fname}] Block {b_id} ({tag}) has empty translation array!")

            for idx, s in enumerate(translations, 1):
                total_sentences += 1
                ch_sents += 1

                # ID sequence check
                s_id = s.get("id")
                if s_id != idx:
                    id_mismatches += 1

                # English check
                en = s.get("en", "").strip()
                if not en:
                    missing_en += 1
                else:
                    l_en = len(en)
                    en_lengths.append(l_en)
                    if l_en > ch_max_en:
                        ch_max_en = l_en
                    if l_en > 200:
                        over_200 += 1
                        ch_over += 1
                        print(f"[{fname}] {tag}_{s_id} EN > 200c ({l_en}): {en[:60]}...")

                # Korean check
                kr = s.get("kr", "").strip()
                if not kr:
                    missing_kr += 1
                else:
                    kr_lengths.append(len(kr))

                # Cleanliness check (zero English/Hanja in parens)
                if re.search(r'\([A-Za-z0-9\s]+\)', kr):
                    parenthetical_violations += 1
                    print(f"[{fname}] {tag}_{s_id} Parenthetical English: {kr}")

                # Quote cleanliness (no outer quotes)
                if en.startswith(('"', "'", "“", "”")) or en.endswith(('"', "'", "“", "”")):
                    quote_violations += 1
                if kr.startswith(('"', "'", "“", "”")) or kr.endswith(('"', "'", "“", "”")):
                    quote_violations += 1

            # Header check
            if it.get("is_header"):
                for s in translations:
                    kr_text = s.get("kr", "")
                    if re.search(r'^(PART|CHAPTER|STORY|\[Illustration)', kr_text, re.IGNORECASE):
                        untranslated_headers += 1
                        print(f"[{fname}] Untranslated header: {kr_text}")

        chapter_stats.append({
            "chapter": fname,
            "blocks": len(items),
            "sentences": ch_sents,
            "max_en_len": ch_max_en,
            "over_200": ch_over
        })

    # Verify Master JSON
    master_synced = False
    if os.path.exists(MASTER_PATH):
        with open(MASTER_PATH, "r", encoding="utf-8") as f:
            master = json.load(f)
        master_blocks = sum(len(c["paragraphs"]) for c in master.get("chapters", []))
        master_sents = sum(sum(len(p.get("translation", [])) for p in c["paragraphs"]) for c in master.get("chapters", []))
        master_synced = (master_blocks == total_blocks and master_sents == total_sentences)

    # Print Chapter Table
    print(f"{'Chapter':<15} | {'Blocks':<8} | {'Sentences':<10} | {'Max EN Len':<11} | {'Status'}")
    print("-" * 65)
    for cs in chapter_stats:
        status = "PASSED (100%)" if cs["over_200"] == 0 else f"FAILED ({cs['over_200']} >200c)"
        print(f"{cs['chapter']:<15} | {cs['blocks']:<8} | {cs['sentences']:<10} | {cs['max_en_len']:<11} | {status}")
    print("-" * 65)

    print("\n=== OVERALL BOOK METRICS ===")
    print(f"Total Chapters Processed:        16 / 16 (100%)")
    print(f"Total Paragraph Blocks:          {total_blocks} / 853 (100%)")
    print(f"Total Bilingual Sentences:       {total_sentences:,}")
    print(f"Average EN Sentence Length:      {sum(en_lengths)/len(en_lengths):.1f} chars")
    print(f"Maximum EN Sentence Length:      {max(en_lengths)} chars (Limit: 200)")
    print(f"Average KR Sentence Length:      {sum(kr_lengths)/len(kr_lengths):.1f} chars")
    print(f"Master JSON Synchronized:        {master_synced}")

    print("\n=== ZERO-TOLERANCE QUALITY AUDIT ===")
    print(f"Sentences Exceeding 200 Chars:   {over_200}")
    print(f"Missing English Sentences:       {missing_en}")
    print(f"Missing Korean Sentences:        {missing_kr}")
    print(f"Sentence ID Mismatches:          {id_mismatches}")
    print(f"Parenthetical English in KR:     {parenthetical_violations}")
    print(f"Untranslated Headers in KR:      {untranslated_headers}")
    print(f"Outer Dialogue Quote Artifacts:  {quote_violations}")
    print(f"Asterisk Dividers (* * * * *):   {asterisk_dividers}")
    print(f"Colophon / Footnote Artifacts:   {footnote_artifacts}")
    print("================================================================\n")

    passed = (over_200 == 0 and missing_en == 0 and missing_kr == 0 and 
              id_mismatches == 0 and parenthetical_violations == 0 and 
              untranslated_headers == 0 and quote_violations == 0 and 
              asterisk_dividers == 0 and footnote_artifacts == 0 and
              total_blocks == 853 and master_synced)

    if passed:
        print(">>> ALL AUDIT CHECKS PASSED PERFECTLY WITH ZERO DEFECTS! <<<\n")
        return True
    else:
        print(">>> AUDIT DETECTED DEFECTS! <<<\n")
        return False

if __name__ == "__main__":
    success = run_audit()
    sys.exit(0 if success else 1)
