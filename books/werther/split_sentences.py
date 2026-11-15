"""
Stage 3c: give every item its sentence-level `translation` scaffold and
build the modernization work queue.

Transforms each item in json/ch_NN.json from the make_json.py shape
(item-level `en` / `ko`, both empty) into the unified shape used by
the_heroes:

    "translation": [ {"id": 1, "en": "...", "kr": "..."}, ... ]

`translation == []` means the item still needs Stage 4 (modernization).
An entry with `kr == ""` still needs Stage 5 (translation). Those two
conditions are the only progress state, and both live in the files, so
an interrupted run resumes by simply re-running the queue builder.

The mechanical sentence split is written to batches/ as a *suggestion*
for the modernizer, not into the chapter files. Modernization is free to
re-segment -- in the_heroes it did so for 83% of items, breaking the
long semicolon-chained Victorian periods into separate modern sentences.
Keeping the suggestion out of the chapter files avoids storing a second
copy of the book that would go stale the moment it is re-segmented.

The 86 header items (84 letter dates plus PREFACE and THE EDITOR TO THE
READER.) are filled in here rather than queued: date conversion is
deterministic, so spending a model pass on it would only add a chance of
inconsistency.
"""

import os
import re
import json
import glob

from split_chapters import LETTER_RE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
BATCH_DIR = os.path.join(BASE_DIR, "batches")
QUEUE_FILE = os.path.join(BASE_DIR, "work_queue.json")

# Raw words per batch. Every Werther chapter is 2,251-3,397 words, so each
# becomes exactly one batch; the guard only exists to stop a future edit
# from silently producing a batch too large to process in one pass. The
# largest batch the_heroes completed was ~15,000 words.
MAX_BATCH_WORDS = 6000

MONTHS_KO = {
    "JANUARY": 1, "FEBRUARY": 2, "MARCH": 3, "APRIL": 4,
    "MAY": 5, "JUNE": 6, "JULY": 7, "AUGUST": 8,
    "SEPTEMBER": 9, "OCTOBER": 10, "NOVEMBER": 11, "DECEMBER": 12,
}

STATIC_HEADERS = {
    "PREFACE": ("Preface", "머리말"),
    "THE EDITOR TO THE READER.": ("The Editor to the Reader", "엮은이가 독자에게"),
}

# "etc." is the only abbreviation in the text that ends in a period and can
# be followed by a capital. Truncated names (V—, S—, C—) use an em dash,
# not a period, so they never trigger a split.
PROTECT = [("etc.", "\x00ETC\x00")]

# A closing quote must stay with the sentence it closes. Writing the quote
# as an optional member of the separator ( ["”]?\s+ ) instead makes the regex
# CONSUME it, silently deleting one character from items ending in dialogue.
# Two fixed-length lookbehinds avoid that; re rejects a variable-length one.
SENT_SPLIT = re.compile(
    r'(?<=[.!?]["”])\s+(?=["“—]?[A-Z])'
    r'|(?<=[.!?])\s+(?=["“—]?[A-Z])'
)


def date_header(text):
    """('MAY 4.', 'JANUARY 8, 1772.') -> (english, korean) or None."""
    m = re.match(r"^([A-Z]+) (\d+)[.,]?(?:\s*(\d{4}))?\.?$", text.strip())
    if not m or m.group(1) not in MONTHS_KO:
        return None
    month, day, year = m.group(1), int(m.group(2)), m.group(3)
    month_n = MONTHS_KO[month]
    en_month = month.capitalize()
    if year:
        return f"{en_month} {day}, {year}", f"{year}년 {month_n}월 {day}일"
    return f"{en_month} {day}", f"{month_n}월 {day}일"


def split_into_sentences(text):
    t = text
    for real, token in PROTECT:
        t = t.replace(real, token)
    parts = [p.strip() for p in SENT_SPLIT.split(t) if p.strip()]
    out = []
    for p in parts:
        for real, token in PROTECT:
            p = p.replace(token, real)
        out.append(p)
    out = out or [text.strip()]

    # The split must be lossless: sentences rejoined, ignoring whitespace,
    # have to equal the raw paragraph. Silent character loss here would
    # propagate into the modernized English and the translation.
    if re.sub(r"\s+", "", " ".join(out)) != re.sub(r"\s+", "", text):
        raise ValueError(f"lossy sentence split: {text[:80]!r}")
    return out


def header_translation(raw):
    """Deterministic en/kr for a header item, or None if it is not one."""
    if raw in STATIC_HEADERS:
        en, kr = STATIC_HEADERS[raw]
        return [{"id": 1, "en": en, "kr": kr}]
    if LETTER_RE.match(raw):
        conv = date_header(raw)
        if conv:
            return [{"id": 1, "en": conv[0], "kr": conv[1]}]
    return None


def split_sentences():
    os.makedirs(BATCH_DIR, exist_ok=True)

    batches = []
    pending_items = 0
    filled_headers = 0
    kept = 0
    total_sentences = 0

    for path in sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json"))):
        ch_id = os.path.basename(path).replace(".json", "")
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)

        batch_items = []
        for it in items:
            # Drop the pre-split item-level fields; translation supersedes them.
            it.pop("en", None)
            it.pop("ko", None)

            sentences = split_into_sentences(it["raw"])
            it["sentence_count"] = len(sentences)
            total_sentences += len(sentences)

            if it.get("translation"):
                kept += 1          # already processed; never clobber
                continue

            if it["is_header"]:
                tr = header_translation(it["raw"])
                if tr:
                    it["translation"] = tr
                    filled_headers += 1
                    continue

            it["translation"] = []
            pending_items += 1
            batch_items.append({
                "id": it["id"],
                "tag": it["tag"],
                "letter": it["letter"],
                "is_header": it["is_header"],
                "raw": it["raw"],
                "sentences": sentences,
            })

        # Reorder keys so translation reads last.
        ordered = []
        for it in items:
            tr = it.pop("translation", [])
            it["translation"] = tr
            ordered.append(it)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(ordered, f, ensure_ascii=False, indent=2)

        if not batch_items:
            print(f"{ch_id}: nothing pending")
            continue

        words = sum(len(b["raw"].split()) for b in batch_items)
        if words > MAX_BATCH_WORDS:
            print(f"  WARNING {ch_id}: {words} raw words exceeds "
                  f"MAX_BATCH_WORDS={MAX_BATCH_WORDS}; split this batch by hand.")
        batch_name = f"batch_{ch_id}.json"
        with open(os.path.join(BATCH_DIR, batch_name), "w", encoding="utf-8") as bf:
            json.dump({
                "batch_id": ch_id,
                "chapter_id": ch_id,
                "item_count": len(batch_items),
                "raw_words": words,
                "sentence_count": sum(len(b["sentences"]) for b in batch_items),
                "items": batch_items,
            }, bf, ensure_ascii=False, indent=2)

        batches.append({
            "batch_id": ch_id,
            "file": f"batches/{batch_name}",
            "item_count": len(batch_items),
            "raw_words": words,
            "sentence_count": sum(len(b["sentences"]) for b in batch_items),
        })
        print(f"{ch_id}: {len(batch_items):3d} items pending "
              f"({words:5d} raw words, {sum(len(b['sentences']) for b in batch_items):4d} sentences) "
              f"-> {batch_name}")

    with open(QUEUE_FILE, "w", encoding="utf-8") as qf:
        json.dump({
            "pending_items": pending_items,
            "batch_count": len(batches),
            "batches": batches,
        }, qf, ensure_ascii=False, indent=2)

    print(f"\nHeaders filled deterministically: {filled_headers}")
    if kept:
        print(f"Items already processed, left untouched: {kept}")
    print(f"Pending items: {pending_items} across {len(batches)} batches")
    print(f"Mechanical sentence split: {total_sentences} sentences (a suggestion; "
          f"Stage 4 may re-segment)")
    print(f"Queue: {QUEUE_FILE}")


if __name__ == "__main__":
    split_sentences()
