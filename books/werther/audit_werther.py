"""
Stage 6: integrity audit over json/ch_NN.json before migration.

    python audit_werther.py           # report
    python audit_werther.py -v        # report and list every finding

Exit code is non-zero if any ERROR-level check fails, so this can gate the
migrate step. WARN-level findings are judgement calls: they are listed but
do not fail the run.

Checks, in the order they can bite:

  1. STRUCTURE   ids sequential per file, all chapters present, every item
                 has a non-empty translation, en and kr both filled.
  2. COVERAGE    every number and proper noun in `raw` survives into the
                 modernized English. This is the only check that can catch
                 a whole clause going missing, since modernization rewrites
                 wording and so cannot be diffed against the source.
  3. CARDS       the migrate-time merge is replayed here, so card lengths
                 are measured rather than estimated. Cards must be <= CARD_CAP
                 on BOTH sides -- the app shows en and ko on the same card.
  4. ENDINGS     a card should not end mid-sentence, which is what a silent
                 upstream truncation looks like.
  5. KOREAN      no run of untranslated English left in kr, the metadata.md
                 glossary is honoured, and kr is not suspiciously short.
"""

import os
import re
import sys
import json
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")

CARD_CAP = 300
CARD_MAX_ENTRIES = 3
EXPECTED_CHAPTERS = 15

# Mirrors apply_modernization.py. Kept as its own copy so the audit stays
# runnable even if that script is refactored or moved.
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
    "Narrow", "Sad", "Such", "Whose", "Though", "Since", "After",
    "Before", "Upon", "About", "Under", "Over", "Between", "Through",
    "Tis", "Twas", "Twere",
    "With", "Without", "Within", "Against", "Among", "Amongst", "Toward",
    "Towards", "Into", "Onto", "Across", "Beyond", "Beside", "Besides",
}

GLOSSARY = {
    "Werther": "베르테르",
    "Wilhelm": "빌헬름",
    "Albert": "알베르트",
    "Charlotte": "샤를로테",
    "Wahlheim": "발하임",
    "Walheim": "발하임",
    "Ossian": "오시안",
}

LATIN_RUN = re.compile(r"[A-Za-z]{2,}(?:[ ,]+[A-Za-z]{2,}){2,}")

# A finished card ends in terminal punctuation, optionally followed by a
# closing quote. An em dash also counts: Werther breaks off mid-thought
# constantly, and that is authorial, not truncation.
#
# Semicolon and colon are deliberately NOT terminators. They mark a clause
# continuing into the next card, which is exactly what a Korean trailing
# comma marks -- treating one as finished and the other as unfinished made
# an ordinary split period look like a one-sided defect.
CLOSERS = "\"’”')]"
GOOD_END = re.compile("[.!?…—][" + re.escape(CLOSERS) + "]*$")


def required_tokens(text):
    """Numbers and proper nouns in `raw` that must survive modernization."""
    nums = set(re.findall(r"\b\d[\d,]*\b", text))
    props = set()
    for m in re.finditer(r"(?<![.!?\"]\s)(?<!^)\b([A-Z][a-zA-Z]{2,})\b", text, re.M):
        w = m.group(1)
        if w.isupper() or w in STOP:
            continue
        props.add(w)
    return nums, props


def present_tokens(text):
    """Position-blind: modernization reflows sentences, so a proper noun may
    legitimately move to the start of one."""
    return (set(re.findall(r"\b\d[\d,]*\b", text)),
            set(re.findall(r"\b([A-Z][a-zA-Z]{2,})\b", text)))


def merge_groups(entries, cap=CARD_CAP, mx=CARD_MAX_ENTRIES):
    """Replay the migrate-time merge. Groups are chosen on the English, and
    the Korean follows the same grouping -- both go on one card."""
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


def main():
    verbose = "-v" in sys.argv
    errors, warns = [], []
    files = sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json")))

    if len(files) != EXPECTED_CHAPTERS:
        errors.append(("STRUCTURE", "-",
                       "expected %d chapter files, found %d" % (EXPECTED_CHAPTERS, len(files))))

    items_n = entries_n = cards_n = 0
    card_en, card_ko = [], []
    prev_id = 0

    for path in files:
        ch = os.path.basename(path).replace(".json", "")
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)

        # ids run 1..438 across the whole book, not 1..N per file -- that is
        # what make_json.py produces, and migrate_werther.py renumbers per
        # file on the way into the app assets. So the invariant to check is
        # that the global sequence has no gap and no restart.
        ids = [it["id"] for it in items]
        if ids != list(range(prev_id + 1, prev_id + 1 + len(items))):
            errors.append(("STRUCTURE", ch,
                           "ids break the global sequence (expected %d.., got %d..%d)"
                           % (prev_id + 1, ids[0], ids[-1])))
        prev_id = ids[-1]

        for it in items:
            items_n += 1
            tr = it["translation"]
            if not tr:
                errors.append(("STRUCTURE", ch, "id %d: empty translation" % it["id"]))
                continue

            for n, e in enumerate(tr, 1):
                entries_n += 1
                if not e["en"].strip():
                    errors.append(("STRUCTURE", ch, "id %d entry %d: empty en" % (it["id"], n)))
                if not e["kr"].strip():
                    errors.append(("STRUCTURE", ch, "id %d entry %d: empty kr" % (it["id"], n)))

            joined = " ".join(e["en"] for e in tr)
            rn, rp = required_tokens(it["raw"])
            pn, pp = present_tokens(joined)
            for lost in sorted(rn - pn):
                errors.append(("COVERAGE", ch, "id %d: number %r lost" % (it["id"], lost)))
            for lost in sorted(rp - pp):
                errors.append(("COVERAGE", ch, "id %d: proper noun %r lost" % (it["id"], lost)))

            for n, e in enumerate(tr, 1):
                leak = LATIN_RUN.search(e["kr"])
                if leak:
                    errors.append(("KOREAN", ch, "id %d entry %d: English left in kr -- %r"
                                   % (it["id"], n, leak.group(0))))
                for en_name, ko_name in GLOSSARY.items():
                    if re.search(r"\b%s\b" % en_name, e["en"]) and ko_name not in e["kr"]:
                        errors.append(("KOREAN", ch, "id %d entry %d: %r but no %r"
                                       % (it["id"], n, en_name, ko_name)))
                if len(e["en"]) > 60 and len(e["kr"]) < len(e["en"]) * 0.25:
                    warns.append(("KOREAN", ch, "id %d entry %d: kr unusually short (%d vs en %d)"
                                  % (it["id"], n, len(e["kr"]), len(e["en"]))))

            groups = [tr[:1]] if it["is_header"] else merge_groups(tr)
            for g in groups:
                cards_n += 1
                en = " ".join(x["en"] for x in g)
                ko = " ".join(x["kr"] for x in g)
                card_en.append(len(en))
                card_ko.append(len(ko))
                if len(en) > CARD_CAP:
                    errors.append(("CARDS", ch, "id %d: en card %d chars > %d"
                                   % (it["id"], len(en), CARD_CAP)))
                if len(ko) > CARD_CAP:
                    errors.append(("CARDS", ch, "id %d: ko card %d chars > %d"
                                   % (it["id"], len(ko), CARD_CAP)))
                if not it["is_header"]:
                    # A card may legitimately end mid-sentence: a long period
                    # split across entries lands on consecutive cards, and the
                    # reader simply continues. What distinguishes that from a
                    # truncation is PARITY -- a real split leaves both languages
                    # unterminated, while a truncation hits only one side. So
                    # only a mismatch is worth reporting.
                    en_done = bool(GOOD_END.search(en.rstrip()))
                    ko_done = bool(GOOD_END.search(ko.rstrip()))
                    if en_done != ko_done:
                        warns.append(("ENDINGS", ch,
                                      "id %d: en %s but ko %s -- en ...%r / ko ...%r"
                                      % (it["id"],
                                         "ends" if en_done else "runs on",
                                         "ends" if ko_done else "runs on",
                                         en[-30:], ko[-20:])))

    def show(label, rows):
        by_kind = {}
        for kind, ch, msg in rows:
            by_kind.setdefault(kind, []).append((ch, msg))
        print("\n%s: %d" % (label, len(rows)))
        for kind in sorted(by_kind):
            rs = by_kind[kind]
            print("  %-10s %d" % (kind, len(rs)))
            for ch, msg in (rs if verbose else rs[:5]):
                print("      %s  %s" % (ch, msg))
            if not verbose and len(rs) > 5:
                print("      ... and %d more (-v for all)" % (len(rs) - 5))

    print("Chapters %d | items %d | entries %d | cards %d"
          % (len(files), items_n, entries_n, cards_n))
    print("en cards: max %d mean %d" % (max(card_en), sum(card_en) // len(card_en)))
    print("ko cards: max %d mean %d" % (max(card_ko), sum(card_ko) // len(card_ko)))

    show("ERRORS", errors) if errors else print("\nERRORS: 0")
    show("WARNINGS", warns) if warns else print("WARNINGS: 0")

    print("\nAUDIT " + ("FAILED" if errors else "PASSED"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
