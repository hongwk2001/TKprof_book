"""
Stage 8: build the app assets from the finished pipeline JSON.

    python migrate_werther.py

Reads  json/ch_01..15.json
Writes Book_apps/werther/src/main/assets/books/ch_01..15.json

The app asset format is the one every TKProf book app already uses (see
the_heroes): a flat array of cards carrying only

    {"id", "tag", "en", "ko", "is_header"}

`raw`, `chapter_id`, `section`, `letter`, `word_count` and the sentence
level structure all stop here -- they are pipeline concerns. Card ids are
renumbered 1..N per file, because BookRepository reads each chapter on its
own; the pipeline's global 1..438 numbering does not survive.

Three things this script has to repair on the way through, all recorded in
roadmap.md. None can be fixed upstream: re-running make_json.py would
discard 2,519 finished translation entries.

  1. Chapters 13-15 open mid-narration at a scene cut and have no leading
     header item. Without a prepended chapter header, BookRepository's
     `takeWhile { is_header }` finds nothing and the drawer falls back to
     "Chapter 13/14/15" for the last three chapters of the book.
  2. Two real letter dates sit in body items -- ch_08 id 187 ("November 26.")
     and ch_09 id 220 ("March 16."). The Gutenberg source prints those two in
     title case while the other 84 are uppercase, and LETTER_RE is
     deliberately case-sensitive (a case-insensitive version matches wrapped
     lines beginning "may..."). They are promoted to header cards here.
  3. The 84 letter dates are headers and most chapters open on one, so the
     drawer title becomes "Arrival - May 4" / "도착 - 5월 4일". That is
     accepted rather than fixed: the alternative is changing `takeWhile` in
     :shared, which would alter the chapter titles of five shipped apps.
"""

import os
import re
import json
import glob

from split_chapters import CHAPTER_DEFS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
DEST_DIR = os.path.abspath(os.path.join(
    BASE_DIR, "..", "..", "..", "Book_apps", "werther",
    "src", "main", "assets", "books"))

CARD_CAP = 300
CARD_MAX_ENTRIES = 3

# Chapters whose first item is not a header, so one must be prepended.
# Derived at runtime rather than hard-coded, but listed here for the reader.
# (ch_13, ch_14, ch_15 as of the current split.)

MONTHS_KO = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11,
    "December": 12,
}

# A body item that is nothing but a date -- see repair 2 above.
DATE_ONLY = re.compile(
    r"^(January|February|March|April|May|June|July|August|September"
    r"|October|November|December)\s+(\d+)[.,]?(?:\s*(\d{4}))?\.?$")


def date_to_korean(text):
    m = DATE_ONLY.match(text.strip())
    if not m:
        return None
    month, day, year = m.group(1), int(m.group(2)), m.group(3)
    if year:
        return "%s년 %d월 %d일" % (year, MONTHS_KO[month], day)
    return "%d월 %d일" % (MONTHS_KO[month], day)


def merge_groups(entries, cap=CARD_CAP, mx=CARD_MAX_ENTRIES):
    """Group entries into cards. Grouping is decided on the English, and the
    Korean follows the same grouping -- both languages sit on one card, so
    they must never be grouped independently."""
    out, cur = [], []
    for e in entries:
        if cur and (len(" ".join(x["en"] for x in cur)) + len(e["en"]) + 1 > cap
                    or len(cur) >= mx):
            out.append(cur)
            cur = []
        cur.append(e)
    if cur:
        out.append(cur)
    return out


def migrate():
    os.makedirs(DEST_DIR, exist_ok=True)
    titles = {"ch_%02d" % d[0]: (d[3], d[4]) for d in CHAPTER_DEFS}

    total_cards = 0
    prepended = []
    promoted = []

    for path in sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json"))):
        ch_id = os.path.basename(path).replace(".json", "")
        ch_num = int(ch_id.split("_")[1])
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)

        cards = []
        title_en, title_ko = titles[ch_id]

        # Repair 1: every chapter gets the canonical title as its first card.
        #
        # BookRepository builds the drawer title from the leading run of
        # is_header cards joined by " - ". Most chapters open on a letter date,
        # so without this the drawer would read a bare "May 22" / "June 16"
        # with no chapter name at all -- and chapters 13-15, which open
        # mid-narration with no header, would fall back to "Chapter 13".
        # Prepending unconditionally gives "Wahlheim - May 22", which names
        # the chapter and dates it.
        cards.append({
            "id": 0,
            "tag": "H%02d" % ch_num,
            "en": title_en,
            "ko": title_ko,
            "is_header": True,
        })
        prepended.append(ch_id)

        # ...but if the chapter's own first header already says the same thing
        # (ch_12 opens on "The Editor to the Reader", which is also its title),
        # drop it so the drawer does not read the title twice.
        skip_first = (items[0]["is_header"]
                      and items[0]["translation"]
                      and items[0]["translation"][0]["en"].strip().rstrip(".").lower()
                      == title_en.strip().lower())

        for idx, it in enumerate(items):
            if idx == 0 and skip_first:
                continue
            entries = it["translation"]
            if not entries:
                continue

            is_header = it["is_header"]

            # Repair 2: a body item that is only a date is really a letter
            # header the splitter missed.
            if not is_header:
                ko_date = date_to_korean(entries[0]["en"]) if len(entries) == 1 else None
                if ko_date:
                    is_header = True
                    entries = [{"id": 1, "en": entries[0]["en"].rstrip(". "),
                                "kr": ko_date}]
                    promoted.append("%s id %d (%s)" % (ch_id, it["id"], entries[0]["en"]))

            if is_header:
                cards.append({
                    "id": 0,
                    "tag": it["tag"],
                    "en": entries[0]["en"],
                    "ko": entries[0]["kr"],
                    "is_header": True,
                })
                continue

            groups = merge_groups(entries)
            for n, g in enumerate(groups, 1):
                cards.append({
                    "id": 0,
                    "tag": it["tag"] if len(groups) == 1 else "%s_%d" % (it["tag"], n),
                    "en": " ".join(x["en"] for x in g),
                    "ko": " ".join(x["kr"] for x in g),
                    "is_header": False,
                })

        # Closing marker, matching the_heroes.
        if ch_num == len(CHAPTER_DEFS):
            cards.append({"id": 0, "tag": "THE_END", "en": "THE END",
                          "ko": "끝", "is_header": False})

        for n, c in enumerate(cards, 1):
            c["id"] = n

        out_path = os.path.join(DEST_DIR, "%s.json" % ch_id)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False, indent=2)

        total_cards += len(cards)
        headers = sum(1 for c in cards if c["is_header"])
        print("  %s  %4d cards (%2d headers)  ->  %s.json"
              % (ch_id, len(cards), headers, ch_id))

    print("\nWrote %d chapter files, %d cards total" % (len(CHAPTER_DEFS), total_cards))
    print("Destination: %s" % DEST_DIR)
    if prepended:
        print("Repair 1 -- chapter header prepended: %s" % ", ".join(prepended))
    if promoted:
        print("Repair 2 -- date promoted to header: %s" % "; ".join(promoted))


if __name__ == "__main__":
    migrate()
