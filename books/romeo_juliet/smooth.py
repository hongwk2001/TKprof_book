"""
Readability pass: join choppy runs of short sentences into natural ones.

    python smooth.py 7            # drafts.smooth for the flagged speeches in ch_07
    python smooth.py all          # every chapter
    python smooth.py 7 --show     # print current vs smoothed, write nothing
    python smooth.py all --list   # just list the flagged speeches

Works on the reviewed English in `sentences`, not on Shakespeare, so the
model edits plain modern English (far easier than Stage 4). Only speeches
that read like a list are sent:
  - 3+ sentences in a row of <= SHORT words, or
  - 3+ sentences opening with the same two words.

Guards, on top of simplify.check_item (length, archaic words, names, whole
sentences):
  - no new content word: every non-function word must already be in the
    current English or in the raw line (crude stemming), so no ideas are added;
  - nothing dropped: at least COVER of the current content words survive;
  - it must actually merge: fewer sentences than before.
Output goes to drafts.smooth, whole scene or nothing; promote.py --partial
then replaces only the smoothed items.
"""

import os
import re
import sys
import json
import time

import simplify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
NAME = "smooth"
SHORT = 6
COVER = 0.9
RETRIES = 5

FUNCTION = set("""
a an the and but or so because when if then than that this these those it its you your yours i me my mine
he him his she her hers we us our they them their there here what who whom whose which where why how
be am is are was were been being have has had do does did will would can could shall should may might must
not no nor to of in on at for with from by as too very just all also oh yes well now still yet even though
although while since until unless both either neither such own like let lets up down out over into onto off
again more most much many any some one ones every each other another only ever never always
""".split())


def stem(w):
    w = w.lower().replace("’", "'")
    w = re.sub(r"'(s|re|ll|ve|d|m|t)$", "", w)
    for suf in ("ing", "ed", "es", "ly", "s"):
        if len(w) > 4 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def content(text):
    return {stem(w) for w in re.findall(r"[A-Za-z’']+", text)
            if w.lower() not in FUNCTION and stem(w) not in FUNCTION}


def flagged(it):
    if it["type"] != "speech" or len(it["sentences"]) < 3:
        return False
    ss = [s["en"] for s in it["sentences"]]
    short = [len(s.split()) <= SHORT for s in ss]
    if any(all(short[i:i + 3]) for i in range(len(ss) - 2)):
        return True
    starts = [" ".join(s.split()[:2]) for s in ss]
    return any(starts.count(x) >= 3 for x in set(starts))


def check(it, old, new):
    errs = simplify.check_item(it, new)
    if errs:
        return errs
    if len(new) >= len(old):
        return [f"not merged: {len(new)} sentences for {len(old)}"]
    allowed = content(" ".join(old) + " " + it["raw"])
    added = sorted(content(" ".join(new)) - allowed)
    if added:
        errs.append(f"new words not in the text: {added[:6]}")
    before = content(" ".join(old))
    kept = len(before & content(" ".join(new))) / max(1, len(before))
    if kept < COVER:
        errs.append(f"dropped content: kept {kept:.0%} of the words")
    return errs


PROMPT = """You edit simple English for Korean learners of English (CEFR level B1). The text is Shakespeare's "Romeo and Juliet", already rewritten into plain modern English. It will be read aloud.

Each item is one character's speech: "now" is the current version as a list of sentences, "raw" is Shakespeare's original for reference only.

Make each speech read naturally aloud:
1. Join very short sentences that belong together into sentences of 8 to 15 words (never more than 20).
2. Use linking words like and, but, so, because, when, if, who, which.
3. Where many sentences start the same way, vary the openings.
4. Keep every idea and keep the meaning exactly. Do not add anything: no new facts, feelings, names, explanations or words that are not in "now" or "raw".
5. Keep the same plain modern words; never bring back old words like thou, thee, doth, 'tis.
6. Keep repetition the character uses on purpose, like "Romeo, Romeo" or "dead, dead, dead".
7. Keep the jokes and the tone.
8. Each list entry is one complete sentence that starts with a capital letter and ends with . ! ? or —
9. Return exactly the keys you were given.

Rewrite these items:
{items}"""


def run(ch):
    path = os.path.join(JSON_DIR, f"ch_{ch:02d}.json")
    items = json.load(open(path, encoding="utf-8"))
    ctx = {x["tag"]: x for x in simplify.model_items(json.loads(json.dumps(items)))}
    todo = [it for it in items if flagged(it)]
    if not todo:
        print(f"ch_{ch:02d}: nothing to smooth")
        return
    results, t0 = {}, time.time()
    for c in range(0, len(todo), 6):
        pending = todo[c:c + 6]
        label = f"{pending[0]['tag']}..{pending[-1]['tag']}"
        feedback = ""
        for attempt in range(1, RETRIES + 1):
            keys = [it["tag"] for it in pending]
            prompt = PROMPT.replace("{items}", json.dumps(
                {it["tag"]: {"speaker": simplify.narrate.SPEAKERS[it["speaker"]]["en"],
                             "now": [s["en"] for s in it["sentences"]], "raw": it["raw"]}
                 for it in pending}, ensure_ascii=False, indent=1))
            try:
                ans = simplify.call_ollama(prompt + feedback, keys)
            except (ValueError, OSError) as e:
                print(f"  {label} try {attempt}: call failed: {e}")
                continue
            errs, still = [], []
            for it in pending:
                old = [s["en"] for s in it["sentences"]]
                new = [simplify.clean(s) for s in simplify.fix_cutoff(it, ans.get(it["tag"], []))]
                e = check(ctx[it["tag"]], old, new)
                if e:
                    errs += [f"{it['tag']}: {x}" for x in e]
                    still.append(it)
                else:
                    results[it["tag"]] = new
            pending = still
            if not pending:
                print(f"  {label} ok (try {attempt}, {time.time() - t0:.0f}s)")
                break
            print(f"  {label} try {attempt}: " + "; ".join(errs[:3]))
            feedback = ("\n\nYour previous answer was rejected for these problems. Fix all of them:\n- "
                        + "\n- ".join(errs)
                        + "\nOnly join and reorder what is already there; use no new content words.")
        else:
            # a speech that cannot be smoothed safely simply stays as it is
            print(f"  {label}: left unchanged: {', '.join(it['tag'] for it in pending)}")
    for it in items:
        if it["tag"] in results:
            it.setdefault("drafts", {})[NAME] = [{"en": s} for s in results[it["tag"]]]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
    print(f"ch_{ch:02d}: {len(results)} of {len(todo)} flagged speeches smoothed, {time.time() - t0:.0f}s")


def show(ch):
    for it in json.load(open(os.path.join(JSON_DIR, f"ch_{ch:02d}.json"), encoding="utf-8")):
        d = it.get("drafts", {}).get(NAME)
        if d:
            print(f"── {it['tag']} {it['speaker']}")
            print("   NOW    " + " | ".join(s["en"] for s in it["sentences"]))
            print("   SMOOTH " + " | ".join(s["en"] for s in d))
            print()


def main():
    args = sys.argv[1:]
    target = next(a for a in args if not a.startswith("--"))
    chapters = range(1, 25) if target == "all" else [int(target)]
    for ch in chapters:
        if "--show" in args:
            show(ch)
        elif "--list" in args:
            items = json.load(open(os.path.join(JSON_DIR, f"ch_{ch:02d}.json"), encoding="utf-8"))
            print(f"ch_{ch:02d}: " + " ".join(it["tag"] for it in items if flagged(it)))
        else:
            run(ch)


if __name__ == "__main__":
    main()
