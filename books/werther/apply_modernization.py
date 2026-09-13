"""
Stage 4 apply step: merge a modernization result into json/ch_NN.json.

Usage:  python apply_modernization.py ch_01

Reads batches/result_<ch>.json:

    {"chapter_id": "ch_01",
     "items": {"5": ["First modern sentence.", "Second."], ...}}

and writes each list into that item's `translation` as
[{"id": 1, "en": ..., "kr": ""}, ...], leaving `kr` for Stage 5.

Refuses to write if the result would drop content. Because modernization
rewrites wording, the text cannot be diffed against `raw`; instead every
number and every proper noun in `raw` must still appear in the modernized
English. That is what catches a silently dropped clause.
"""

import os
import re
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
BATCH_DIR = os.path.join(BASE_DIR, "batches")

# Proper nouns the modernizer is allowed to drop or rephrase: sentence-initial
# words that merely happen to be capitalised, plus archaic pronouns.
STOP = {
    "I", "A", "An", "The", "But", "And", "Or", "If", "When", "While", "Whilst",
    "For", "So", "Yet", "As", "At", "In", "On", "To", "Of", "It", "He", "She",
    "They", "We", "You", "Thou", "Thee", "Thy", "Thine", "My", "His", "Her",
    "This", "That", "These", "Those", "There", "Here", "Then", "Now", "How",
    "What", "Why", "Who", "Which", "Not", "No", "Oh", "Ah", "Alas", "Good",
    "Never", "Every", "Most", "Many", "Do", "Did", "Was", "Were", "Have", "Had",
    "Be", "Am", "Is", "Are", "Shall", "Should", "Will", "Would", "Can", "Could",
    "May", "Might", "Must", "Let", "Come", "Go", "Poor", "Dear", "Descending",
    "Persons", "Solitude", "Often", "Being", "Cease", "Rise", "Arise", "Star",
    "Narrow", "Sad", "Such", "Who", "Whose", "Though", "Since", "After",
    "Before", "Upon", "About", "Under", "Over", "Between", "Through",
    # Prepositions are never proper nouns, so they belong here regardless of
    # capitalisation. Needed because the source carries stray mid-sentence
    # capitals from typos ("exclaimed With eagerness", ch_11 id 312).
    "With", "Without", "Within", "Against", "Among", "Amongst", "Toward",
    "Towards", "Into", "Onto", "Across", "Beyond", "Beside", "Besides",
    # Archaic contractions. "'Tis" scans as a capitalised word after the
    # apostrophe, but modernizing it to "It is" is the correct treatment, so it
    # must not be demanded back.
    "Tis", "Twas", "Twere",
}


def required_tokens(text):
    """Numbers and proper nouns in `raw` that must survive modernization.

    Position-aware: only a capitalised word that is NOT sentence-initial counts
    as a genuine proper noun, so ordinary words that merely happen to open a
    sentence are not demanded back.
    """
    nums = set(re.findall(r"\b\d[\d,]*\b", text))
    props = set()
    for m in re.finditer(r"(?<![.!?\"]\s)(?<!^)\b([A-Z][a-zA-Z]{2,})\b", text, re.M):
        w = m.group(1)
        # An ALL-CAPS word in this source is a structural marker carried over
        # from the Gutenberg text ("THE SAME EVENING.", "THE END"), never a
        # proper noun. Modernization lowercases them, which is correct, so
        # demanding them back verbatim would reject a good pass.
        if w.isupper():
            continue
        if w not in STOP:
            props.add(w)
    return nums, props


def present_tokens(text):
    """Every number and capitalised word in the modernized English.

    Deliberately position-BLIND. Modernization reflows sentences, so a proper
    noun that sat mid-sentence in `raw` often ends up opening a sentence in the
    new text. Applying the position filter on this side too would report such a
    word as dropped when it is plainly present.
    """
    nums = set(re.findall(r"\b\d[\d,]*\b", text))
    props = set(re.findall(r"\b([A-Z][a-zA-Z]{2,})\b", text))
    return nums, props


def apply_result(ch_id):
    res_path = os.path.join(BATCH_DIR, f"result_{ch_id}.json")
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
    applied = 0
    entries = 0

    for sid, sentences in result["items"].items():
        iid = int(sid)
        if iid not in by_id:
            problems.append(f"id {iid} is not in {ch_id}")
            continue
        it = by_id[iid]
        if not sentences or not all(s.strip() for s in sentences):
            problems.append(f"id {iid}: empty sentence in result")
            continue

        joined = " ".join(sentences)
        raw_nums, raw_props = required_tokens(it["raw"])
        new_nums, new_props = present_tokens(joined)
        lost_nums = raw_nums - new_nums
        lost_props = raw_props - new_props
        if lost_nums:
            problems.append(f"id {iid}: numbers dropped {sorted(lost_nums)}")
        if lost_props:
            problems.append(f"id {iid}: proper nouns dropped {sorted(lost_props)}")

        it["translation"] = [
            {"id": n, "en": s.strip(), "kr": ""} for n, s in enumerate(sentences, 1)
        ]
        applied += 1
        entries += len(sentences)

    if problems:
        print(f"REFUSED — {len(problems)} problem(s), nothing written:")
        for p in problems:
            print("  -", p)
        return 1

    with open(ch_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    pending = sum(1 for it in items if not it["is_header"] and not it["translation"])
    seeded = sum(len(it["raw"].split()) for it in items if it["id"] in
                 {int(k) for k in result["items"]})
    print(f"{ch_id}: applied {applied} items, {entries} entries "
          f"({seeded} raw words in, {entries / max(applied,1):.1f} sentences/item)")
    print(f"{ch_id}: {pending} body items still pending modernization")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python apply_modernization.py ch_01")
        sys.exit(2)
    sys.exit(apply_result(sys.argv[1]))
