"""
Choose one draft per item as the English text of record.

    python promote.py 7 gemma4_gloss           # ch_07: drafts.gemma4_gloss -> sentences
    python promote.py all gemma4_gloss         # every chapter
    python promote.py 7 gemma4_gloss --check   # report only, write nothing
    python promote.py all smooth --partial     # replace only the items that have that draft

For each item with drafts, `sentences` becomes [{"n": 1, "en": ..., "ko": ""}, ...]
from the named draft, and `drafts` is deleted, so a finished chapter holds one
version only (git keeps the history).

With --partial (for passes that touch only some items, like smooth.py),
items without that draft keep their sentences unchanged.

Refuses, and writes nothing for that chapter, when:
  - an item that needs model text has no draft under that name (not with --partial), or
  - an item already has sentences with Korean in them (Stage 5 work would be lost).
"""

import os
import sys
import json

import simplify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")


def promote(ch, name, check_only, partial=False):
    path = os.path.join(JSON_DIR, f"ch_{ch:02d}.json")
    items = json.load(open(path, encoding="utf-8"))
    needed = {it["tag"] for it in simplify.model_items(json.loads(json.dumps(items)))}
    missing = [] if partial else [
        t for t in sorted(needed)
        if name not in next(x for x in items if x["tag"] == t).get("drafts", {})]
    has_ko = [it["tag"] for it in items if any(s.get("ko") for s in it["sentences"])]
    if missing or has_ko:
        print(f"ch_{ch:02d}: NOT promoted — "
              + (f"{len(missing)} item(s) lack drafts.{name} ({', '.join(missing[:5])}) " if missing else "")
              + (f"{len(has_ko)} item(s) already have Korean ({', '.join(has_ko[:5])})" if has_ko else ""))
        return False
    n = changed = 0
    for it in items:
        d = it.get("drafts")
        if not d:
            continue
        if partial and name not in d:
            continue
        if it["tag"] in needed:
            changed += 1
            it["sentences"] = [{"n": i, "en": s["en"], "ko": ""} for i, s in enumerate(d[name], 1)]
            n += len(it["sentences"])
        del it["drafts"]
    if check_only:
        print(f"ch_{ch:02d}: ok to promote ({len(needed)} items, {n} sentences)")
        return True
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
    print(f"ch_{ch:02d}: promoted drafts.{name} -> {changed} items, {n} sentences; drafts removed")
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    target, name = args[0], args[1]
    chapters = range(1, 25) if target == "all" else [int(target)]
    for ch in chapters:
        promote(ch, name, "--check" in sys.argv, "--partial" in sys.argv)


if __name__ == "__main__":
    main()
