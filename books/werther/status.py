"""
Print pipeline progress, and optionally rewrite the generated blocks in
roadmap.md so the numbers there can never drift from the actual files.

    python status.py            # print progress
    python status.py --next     # next chapter needing work, or DONE
    python status.py --write    # print, and update roadmap.md

Progress is derived entirely from json/ch_NN.json, which is the only
source of truth: `translation == []` means Stage 4 is outstanding for
that item, and an entry with `kr == ""` means Stage 5 is.
"""

import os
import re
import sys
import json
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
ROADMAP = os.path.join(BASE_DIR, "roadmap.md")

CARD_CAP = 300
CARD_MAX_ENTRIES = 3

BEGIN = "<!-- BEGIN GENERATED: chapters -->"
END = "<!-- END GENERATED: chapters -->"


def merge_cards(entries, cap=CARD_CAP, mx=CARD_MAX_ENTRIES):
    """Preview the migrate-time merge so card counts are real, not guessed."""
    out, cur = [], []
    for s in entries:
        if cur and (len(" ".join(cur)) + len(s) + 1 > cap or len(cur) >= mx):
            out.append(cur)
            cur = []
        cur.append(s)
    if cur:
        out.append(cur)
    return [" ".join(g) for g in out]


def chapter_stats():
    rows = []
    for path in sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json"))):
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
        body = [x for x in items if not x["is_header"]]
        entries = [e for x in items for e in x["translation"]]
        cards = []
        for x in items:
            if x["is_header"]:
                if x["translation"]:
                    cards.append(x["translation"][0]["en"])
                continue
            cards.extend(merge_cards([e["en"] for e in x["translation"]]))
        lens = [len(c) for c in cards] or [0]
        rows.append({
            "id": items[0]["chapter_id"],
            "items": len(items),
            "body": len(body),
            "modernized": sum(1 for x in body if x["translation"]),
            "entries": len(entries),
            "translated": sum(1 for e in entries if e["kr"].strip()),
            "cards": len(cards),
            "max": max(lens),
            "mean": sum(lens) // len(lens),
            "over": sum(1 for l in lens if l > CARD_CAP),
        })
    return rows


def render(rows):
    head = ("| Chapter | Items | Modernized | Entries | Korean | Cards | Mean | Max | Over cap |\n"
            "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    lines = [head]
    for r in rows:
        mod = "✅" if r["modernized"] == r["body"] else f"{r['modernized']}/{r['body']}"
        kr = "✅" if r["translated"] == r["entries"] else f"{r['translated']}/{r['entries']}"
        lines.append(f"| `{r['id']}` | {r['items']} | {mod} | {r['entries']} | {kr} | "
                     f"{r['cards']} | {r['mean']} | {r['max']} | {r['over']} |")
    t = {k: sum(r[k] for r in rows) for k in
         ("items", "body", "modernized", "entries", "translated", "cards", "over")}
    allmax = max(r["max"] for r in rows)
    lines.append(f"| **Total** | **{t['items']}** | **{t['modernized']}/{t['body']}** | "
                 f"**{t['entries']}** | **{t['translated']}/{t['entries']}** | "
                 f"**{t['cards']}** | | **{allmax}** | **{t['over']}** |")
    return "\n".join(lines), t


def bar(done, total, width=28):
    filled = 0 if not total else round(width * done / total)
    return "█" * filled + "░" * (width - filled)


def next_pending(rows):
    """First chapter with untranslated entries, or None when Stage 5 is done."""
    for r in rows:
        if r["modernized"] < r["body"]:
            return r["id"], "modernize"
        if r["translated"] < r["entries"]:
            return r["id"], "translate"
    return None, None


def main():
    rows = chapter_stats()

    # --next prints one token so a loop can branch on it and stop cleanly.
    if "--next" in sys.argv:
        ch, what = next_pending(rows)
        print("DONE" if ch is None else f"{ch} {what}")
        return 0

    table, t = render(rows)

    print(table.replace("| ", "  ").replace(" |", "").replace("**", ""))
    print()
    print(f"  Stage 4  modernization  {bar(t['modernized'], t['body'])}  "
          f"{t['modernized']}/{t['body']} items")
    print(f"  Stage 5  translation    {bar(t['translated'], t['entries'])}  "
          f"{t['translated']}/{t['entries']} entries")
    print()
    print(f"  Projected app cards: {t['cards']}  |  over {CARD_CAP} chars: {t['over']}")

    if "--write" in sys.argv:
        with open(ROADMAP, "r", encoding="utf-8") as f:
            doc = f.read()
        if BEGIN not in doc or END not in doc:
            print(f"\nroadmap.md has no generated block; add {BEGIN} / {END}")
            return 1
        block = f"{BEGIN}\n\n{table}\n\n{END}"
        doc = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), block, doc, flags=re.S)
        with open(ROADMAP, "w", encoding="utf-8") as f:
            f.write(doc)
        print("\nroadmap.md updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
