import os
import sys
import glob
import json
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")

def forensic_check():
    latin_in_kr = []
    glitches = []
    pic_blocks = []
    short_sentences = []
    very_long_kr = []
    whitespace_issues = []

    for f in sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json"))):
        fname = os.path.basename(f)
        with open(f, "r", encoding="utf-8") as fp:
            items = json.load(fp)

        for it in items:
            b_id = it["id"]
            tag = it["tag"]
            raw = it.get("raw", "")
            
            # Picture/Illustration markers
            if "Picture" in raw or "Illustration" in raw:
                pic_blocks.append((fname, b_id, tag, it.get("translation", [])))

            translations = it.get("translation", [])
            for s in translations:
                s_id = s.get("id")
                en = s.get("en", "")
                kr = s.get("kr", "")

                # 1. Any Latin / English characters in Korean?
                latin = re.findall(r'[A-Za-z]+', kr)
                if latin:
                    latin_in_kr.append((fname, b_id, tag, s_id, latin, kr))

                # 2. Encoding glitches
                for t in [en, kr]:
                    if any(x in t for x in ['\ufffd', '&amp;', '&quot;', 'â€', 'Ã']):
                        glitches.append((fname, b_id, tag, s_id, t))

                # 3. Leading/trailing whitespace
                if en != en.strip() or kr != kr.strip():
                    whitespace_issues.append((fname, b_id, tag, s_id))

                # 4. Korean sentence length anomalies (>200 chars)
                if len(kr) > 200:
                    very_long_kr.append((fname, b_id, tag, s_id, len(kr), kr))

    print("=== FORENSIC HEALTH CHECK RESULTS ===")
    print(f"1. Picture/Illustration Blocks:     {len(pic_blocks)}")
    print(f"2. Latin Characters in Korean:      {len(latin_in_kr)}")
    print(f"3. Encoding Glitches:               {len(glitches)}")
    print(f"4. Whitespace Trimming Issues:      {len(whitespace_issues)}")
    print(f"5. Korean Sentences > 200 chars:    {len(very_long_kr)}")
    print("======================================\n")

    if latin_in_kr:
        print("--- Latin Characters Found in Korean ---")
        for x in latin_in_kr:
            print(f"[{x[0]}] Block {x[1]} ({x[2]}_{x[3]}): {x[4]} -> {x[5]}")
        print()

    if pic_blocks:
        print("--- Picture Blocks in Dataset ---")
        for x in pic_blocks:
            print(f"[{x[0]}] Block {x[1]} ({x[2]}):")
            for s in x[3]:
                print(f"     EN: {s.get('en')}")
                print(f"     KR: {s.get('kr')}")
        print()

    if very_long_kr:
        print("--- Very Long Korean Sentences (>200c) ---")
        for x in very_long_kr:
            print(f"[{x[0]}] Block {x[1]} ({x[2]}_{x[3]}): {x[4]} chars -> {x[5]}")
        print()

if __name__ == "__main__":
    forensic_check()
