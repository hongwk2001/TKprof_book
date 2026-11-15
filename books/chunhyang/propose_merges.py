"""Find cards that are too short or cut mid-sentence, and ask gemma how to merge them.

Step 1 (rules, no LLM): a card is a candidate when its English is under SHORT
characters, ends without sentence punctuation, or is a bare speaker tag
("Chunhyang answers."). Consecutive candidates form a run.
Step 2 (gemma4:12b): for each run, gemma sees the card before, the run, and the
card after, and returns merged cards. It may only join neighbours and fix the
punctuation at the seam; every word must survive (checked here, not trusted).

Writes review/merge_proposals.json for human review; touches no chapter JSON.

    python propose_merges.py            # all chapters
    python propose_merges.py ch_02      # one chapter
"""
import json
import pathlib
import re
import sys
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = pathlib.Path(__file__).parent
API = "http://localhost:11434/api/generate"
MODEL = "gemma4:12b"
SHORT = 40
EN_CAP, KO_CAP = 300, 120
END = re.compile(r"""[.!?]["')]?$|[.!?]"$|\?"$""")
TAG = re.compile(r"""^[^"]{0,60}\b(says|answers|asks|replies|shouts|mutters|laughs|speaks|cries|calls|whispers|sighs)\b[^"]*[.,:]$""", re.I)

PROMPT = """You are fixing a bilingual (Korean/English) e-book where some cards are too short
or cut in the middle of a sentence. Each card is one line on the reader's screen.

Cards, in order (id, English, Korean):
{cards}

Cards marked >>> are the problem cards. Merge each problem card with a neighbour so
that no card is a lonely fragment. Rules:
- Only JOIN neighbouring cards, in order. Never drop, reorder, or rewrite words.
- You may change punctuation and capital letters at the join, and join a speaker tag to
  its speech: 'Chunhyang answers.' + '"Yes."' -> 'Chunhyang answers, "Yes."'.
- A quick back-and-forth of very short lines may become one card.
- Korean is joined the same way as the English (same cards, same order), with a space.
- Each merged card: English at most {en_cap} characters, Korean at most {ko_cap}.
- Cards you do not need to touch may be left out of your answer.

Return JSON: {{"merges": [{{"ids": ["P0004.1", "P0004.2"], "en": "...", "ko": "...", "why": "..."}}]}}
"""


def load(ch):
    rows = json.loads((HERE / "json" / f"{ch}.json").read_text(encoding="utf-8"))
    cards = []
    for p in rows[1:]:
        for s in p["sentences"]:
            cards.append({"id": f"{p['tag']}.{s['n']}", "en": s["en"], "ko": s["ko"]})
    return cards


def is_candidate(c):
    en = c["en"].strip()
    return len(en) < SHORT or not END.search(en) or bool(TAG.match(en))


def runs(cards):
    out, cur = [], []
    for i, c in enumerate(cards):
        if is_candidate(c):
            cur.append(i)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def words(text):
    return re.findall(r"[\w']+", text.lower())


def ollama(prompt):
    body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False, "think": False, "format": "json",
                       "options": {"temperature": 0.1, "num_ctx": 8192}}).encode()
    req = urllib.request.Request(API, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())["response"]


def check(merge, by_id, order):
    """Problems with a proposed merge; an empty list means it passes."""
    ids = merge.get("ids") or []
    if len(ids) < 2 or any(i not in by_id for i in ids):
        return ["unknown or single id"]
    pos = [order[i] for i in ids]
    issues = []
    if pos != list(range(pos[0], pos[0] + len(pos))):
        issues.append("ids not consecutive")
    en, ko = merge.get("en", ""), merge.get("ko", "")
    if words(en) != [w for i in ids for w in words(by_id[i]["en"])]:
        issues.append("English words changed")
    if ko.replace(" ", "") != "".join(by_id[i]["ko"] for i in ids).replace(" ", ""):
        issues.append("Korean changed")
    if len(en) > EN_CAP:
        issues.append(f"English over {EN_CAP}")
    if len(ko) > KO_CAP:
        issues.append(f"Korean over {KO_CAP}")
    return issues


def main():
    chapters = sys.argv[1:] or [p.stem for p in sorted((HERE / "json").glob("ch_*.json"))]
    out_path = HERE / "review" / "merge_proposals.json"
    result = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    for ch in chapters:
        if ch in result and not sys.argv[1:]:
            continue  # already done in an earlier run; name the chapter to redo it
        cards = load(ch)
        by_id = {c["id"]: c for c in cards}
        order = {c["id"]: i for i, c in enumerate(cards)}
        props, t0 = [], time.time()
        for run in runs(cards):
            lo, hi = max(0, run[0] - 1), min(len(cards) - 1, run[-1] + 1)
            listing = "\n".join(f"{'>>>' if i in run else '   '} {cards[i]['id']} | {cards[i]['en']} | {cards[i]['ko']}"
                                for i in range(lo, hi + 1))
            try:
                merges = json.loads(ollama(PROMPT.format(cards=listing, en_cap=EN_CAP, ko_cap=KO_CAP)))["merges"]
            except (ValueError, KeyError, TypeError):
                merges = []
            for m in merges:
                m["issues"] = check(m, by_id, order)
                m["before"] = [{"id": i, "en": by_id[i]["en"], "ko": by_id[i]["ko"]} for i in m.get("ids", []) if i in by_id]
            props.append({"run": [cards[i]["id"] for i in run], "merges": merges})
        result[ch] = props
        bad = sum(1 for p in props for m in p["merges"] if m["issues"])
        n = sum(len(p["merges"]) for p in props)
        print(f"{ch}: {len(props)} runs, {n} merges proposed, {bad} failing checks, {int(time.time() - t0)}s", flush=True)
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
