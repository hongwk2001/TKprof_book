import os
import sys
import json
import re
import glob

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")

def audit_parity(generate_corrections=False, chapters=None):
    ch_files = sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json")))
    if chapters:
        ch_files = [f for f in ch_files if os.path.basename(f).replace(".json", "") in chapters]

    total_blocks = 0
    completed_blocks = 0
    pending_blocks = 0
    total_sentences = 0
    overlength_sentences = 0
    missing_kr = 0
    missing_en = 0
    mismatched_ids = 0
    parenthetical_english = 0
    untranslated_headers = 0

    correction_queue = []

    print("=== Bilingual Parity & Cleanliness Audit ===\n")

    for ch_path in ch_files:
        fname = os.path.basename(ch_path)
        with open(ch_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        ch_sents = 0
        ch_missing_kr = 0
        ch_overlength = 0
        ch_issues = []

        for it in items:
            total_blocks += 1
            translations = it.get("translation", [])
            b_id = it.get("id")
            tag = it.get("tag", f"B{b_id}")

            if not translations:
                pending_blocks += 1
                continue

            completed_blocks += 1
            block_has_error = False
            block_errors = []

            for idx, s in enumerate(translations, 1):
                total_sentences += 1
                ch_sents += 1

                # Check ID sequential alignment
                s_id = s.get("id")
                if s_id != idx:
                    mismatched_ids += 1
                    block_has_error = True
                    block_errors.append(f"ID mismatch: got {s_id}, expected {idx}")

                # Check English completeness & length
                en_text = s.get("en", "").strip()
                if not en_text:
                    missing_en += 1
                    block_has_error = True
                    block_errors.append(f"Sentence {idx} missing English")
                elif len(en_text) > 200:
                    overlength_sentences += 1
                    ch_overlength += 1
                    block_has_error = True
                    block_errors.append(f"Sentence {idx} exceeds 200 chars ({len(en_text)} chars): '{en_text[:60]}...'")

                # Check Korean completeness
                kr_text = s.get("kr", "").strip()
                if not kr_text:
                    missing_kr += 1
                    ch_missing_kr += 1
                    block_has_error = True
                    block_errors.append(f"Sentence {idx} missing Korean")

                # Check for forbidden parenthetical English or Hanja (e.g. (Acrisius), (Medusa), etc.)
                if re.search(r'\([A-Za-z0-9\s]+\)', kr_text):
                    parenthetical_english += 1
                    block_has_error = True
                    block_errors.append(f"Sentence {idx} has parenthetical English: '{kr_text}'")

            # Check header translation cleanliness
            if it.get("is_header"):
                for s in translations:
                    kr_text = s.get("kr", "")
                    if re.search(r'^(PART|CHAPTER|STORY|\[Illustration)', kr_text, re.IGNORECASE):
                        untranslated_headers += 1
                        block_has_error = True
                        block_errors.append(f"Untranslated header in Korean: '{kr_text}'")

            if block_has_error:
                ch_issues.append({"block": it, "errors": block_errors})
                correction_queue.append({
                    "id": b_id,
                    "tag": tag,
                    "chapter_id": it.get("chapter_id"),
                    "raw": it.get("raw"),
                    "is_header": it.get("is_header", False),
                    "translation": translations,
                    "errors": block_errors
                })

        if ch_sents > 0:
            status_parts = []
            if ch_missing_kr == 0:
                status_parts.append("KR COMPLETE")
            else:
                status_parts.append(f"{ch_missing_kr} PENDING KR")
            if ch_overlength > 0:
                status_parts.append(f"{ch_overlength} OVERLENGTH (>200c)")
            if ch_issues:
                status_parts.append(f"{len(ch_issues)} ISSUES")
            else:
                status_parts.append("ALL PASSED")
            print(f"{fname:12s}: {len(items):3d} blocks, {ch_sents:3d} sentences -> {', '.join(status_parts)}")
        else:
            print(f"{fname:12s}: {len(items):3d} blocks -> PENDING ALL (0 sentences)")

    print("\n-------------------------------------------")
    print(f"Total Blocks Scanned: {total_blocks}")
    print(f"  Completed Blocks: {completed_blocks}")
    print(f"  Pending Blocks: {pending_blocks}")
    print(f"Total Sentences: {total_sentences}")
    print(f"  Sentences > 200 Chars: {overlength_sentences}")
    print(f"  Missing Korean Sentences: {missing_kr}")
    print(f"  Missing English Sentences: {missing_en}")
    print(f"  ID Mismatches: {mismatched_ids}")
    print(f"  Parenthetical English Violations: {parenthetical_english}")
    print(f"  Untranslated Headers: {untranslated_headers}")
    print("-------------------------------------------\n")

    if generate_corrections and correction_queue:
        corr_path = os.path.join(BASE_DIR, "batches", "correction_queue.json")
        with open(corr_path, "w", encoding="utf-8") as f:
            json.dump(correction_queue, f, ensure_ascii=False, indent=2)
        print(f"Exported {len(correction_queue)} problematic blocks to {corr_path}")

    has_errors = (overlength_sentences > 0 or missing_kr > 0 or missing_en > 0 or 
                  mismatched_ids > 0 or parenthetical_english > 0 or untranslated_headers > 0)
    
    return not has_errors, correction_queue

if __name__ == "__main__":
    gen_corr = "--generate-corrections" in sys.argv
    success, queue = audit_parity(generate_corrections=gen_corr)
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)
