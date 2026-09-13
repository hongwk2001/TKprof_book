"""
Stage 5 apply step: merge a Korean translation result into json/ch_NN.json.

Usage:  python apply_translation.py ch_01

Reads batches/result_kr_<ch>.json:

    {"chapter_id": "ch_01",
     "items": {"5": ["첫 문장.", "둘째 문장."], ...}}

Each list must align 1:1 with that item's existing English entries --
Stage 5 never re-segments. Re-segmenting here would silently break the
alignment that migrate relies on to build cards.

Refuses the whole chapter if anything is wrong, so a bad pass cannot
land in the data.
"""

import os
import re
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
BATCH_DIR = os.path.join(BASE_DIR, "batches")

# Fixed renderings from metadata.md. If the English mentions the name, the
# Korean must use the agreed form -- this is what keeps 2,519 entries
# translated across many passes from drifting into three spellings of Lotte.
GLOSSARY = {
    "Werther": "베르테르",
    "Wilhelm": "빌헬름",
    "Albert": "알베르트",
    "Charlotte": "샤를로테",
    "Wahlheim": "발하임",
    "Walheim": "발하임",
    "Ossian": "오시안",
}

# A Korean line should not carry a run of untranslated English. Proper nouns
# and initials legitimately survive (S—, N. N., "Emilia Galotti"), so only a
# run of three or more Latin words counts as a leak.
LATIN_RUN = re.compile(r"[A-Za-z]{2,}(?:[ ,]+[A-Za-z]{2,}){2,}")


def apply_result(ch_id):
    res_path = os.path.join(BATCH_DIR, f"result_kr_{ch_id}.json")
    ch_path = os.path.join(JSON_DIR, f"{ch_id}.json")
    for p in (res_path, ch_path):
        if not os.path.exists(p):
            print(f"Error: {p} not found.")
            return 1

    with open(res_path, "r", encoding="utf-8") as f:
        result = json.load(f)
    with open(ch_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    by_id = {it["id"]: it for it in items}
    problems = []
    applied = entries = 0

    for sid, ko_list in result["items"].items():
        iid = int(sid)
        it = by_id.get(iid)
        if it is None:
            problems.append(f"id {iid} is not in {ch_id}")
            continue
        if not it["translation"]:
            problems.append(f"id {iid}: has no English yet (Stage 4 outstanding)")
            continue
        if len(ko_list) != len(it["translation"]):
            problems.append(f"id {iid}: {len(ko_list)} Korean vs "
                            f"{len(it['translation'])} English entries — must be 1:1")
            continue

        for n, (ko, entry) in enumerate(zip(ko_list, it["translation"]), 1):
            ko = ko.strip()
            if not ko:
                problems.append(f"id {iid} entry {n}: empty Korean")
                continue
            if LATIN_RUN.search(ko):
                problems.append(f"id {iid} entry {n}: untranslated English left in "
                                f"Korean — {LATIN_RUN.search(ko).group(0)!r}")
            for en_name, ko_name in GLOSSARY.items():
                if re.search(rf"\b{en_name}\b", entry["en"]) and ko_name not in ko:
                    problems.append(f"id {iid} entry {n}: English has {en_name!r} but "
                                    f"Korean is missing {ko_name!r}")
            entry["kr"] = ko
            entries += 1
        applied += 1

    if problems:
        print(f"REFUSED — {len(problems)} problem(s), nothing written:")
        for p in problems[:25]:
            print("  -", p)
        if len(problems) > 25:
            print(f"  ... and {len(problems) - 25} more")
        return 1

    with open(ch_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    pending = sum(1 for it in items for e in it["translation"] if not e["kr"].strip())
    print(f"{ch_id}: applied {applied} items, {entries} Korean entries")
    print(f"{ch_id}: {pending} entries still pending translation")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python apply_translation.py ch_01")
        sys.exit(2)
    sys.exit(apply_result(sys.argv[1]))
