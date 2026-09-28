"""
Stage 5: reviewed English -> Korean, one Korean sentence per English sentence.

    python translate.py 7          # fill sentences[].ko for ch_07
    python translate.py 7 --show   # print en / ko pairs, write nothing
    python translate.py 7 --force  # redo items that already have Korean

Writes straight into sentences[n].ko of json/ch_NN.json, whole scene or
nothing (git keeps the history). Headers, summaries and the narrator's own
lines are not sent: they are written by hand or by narrate.py.

Each item is sent keyed by tag with its numbered English sentences, the
speaker, the person spoken to (guessed from the scene), the required speech
level from glossary.json -> register, and the two lines before it.
Checks, all per item (a failing item is re-asked with the reasons):
  - exactly one Korean sentence per English sentence (schema + check);
  - no Chinese characters or Latin letters;
  - every glossary name in the English appears in its Korean form;
  - sentence endings match the speech level (요/습니다 vs 다/어/라);
  - Korean no longer than the English (catches added explanations).
"""

import os
import re
import sys
import json
import time
import urllib.request

import narrate
import simplify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
G = narrate.GLOSSARY
SPEAKERS = G["speakers"]
REG = G["register"]
RETRIES = 5
CHUNK = 6

LEVEL_TEXT = {
    "haeyo": "해요체 — polite, every sentence ends in …요 (e.g. '어디 가요?', '사랑해요.')",
    "hasipsio": "하십시오체 — formal, sentences end in …습니다 / …ㅂ니다 / …십시오 (e.g. '알겠습니다.')",
    "banmal": "반말 — casual/plain, sentences end in …다 / …어 / …야 / …라, never …요 or …니다",
    "plain": "해라체 narration or talking to oneself — sentences end in …다 (e.g. '그녀가 창가에 나타난다.')",
}

# name -> Korean, for the name check: speakers (without "the"), plus other names
NAME_KO = {re.sub(r"^(the|a) ", "", s["en"], flags=re.I): s["ko"] for s in SPEAKERS.values()
           if s["en"][0].isupper() or s["en"].startswith("the ") and s["en"][4].isupper()}
NAME_KO.update(G["names"])
NAME_KO.update({"Lawrence": "로런스", "Capulets": "캐퓰릿", "Montagues": "몬태규", "Cupid": "큐피드",
                "Queen Mab": "맵", "Mab": "맵"})

HANZI = re.compile(r"[㐀-鿿]")
LATIN = re.compile(r"[A-Za-z]")
END = r"[\s.!?…—'\"’”)]*$"
_POLITE = re.compile(r"(요|십시오|소서)" + END)
_NIDA = re.compile(r"(.)(니다|니까)" + END)


class _Polite:
    """…요 / …십시오, or 니다/니까 after a syllable ending in ㅂ (습니다, 합니다),
    so that plain 아니다 is not mistaken for polite …ㅂ니다."""
    def search(self, k):
        if _POLITE.search(k):
            return True
        m = _NIDA.search(k)
        return bool(m and "가" <= m.group(1) <= "힣" and (ord(m.group(1)) - 0xAC00) % 28 == 17)


POLITE = _Polite()
PLAIN = re.compile(r"(다|어|아|야|지|니|냐|자|라|해|게|군|네|래|걸|까|마|렴|구나|거라|너라|봐|줘|워)" + END)


# ---------- speech level ----------

def members(x):
    if x == "*":
        return None
    if x.startswith("@"):
        return set(REG["groups"][x[1:]])
    return {x}


def in_set(label, names):
    for n in names:
        m = members(n)
        if m is None or label in m:
            return True
    return False


def level(speaker, to):
    if to is None:
        return "plain"
    for frm, tos, lvl in REG["rules"]:
        if in_set(speaker, frm) and in_set(to, tos):
            return lvl
    return "haeyo"


def addressees(items):
    """Guess who each speech is spoken to. Only someone on stage can be spoken
    to: presence is tracked from the Enter/Exit/Exeunt directions and from who
    has spoken. 'To X' wins; Aside or nobody else present means a soliloquy
    (None -> plain style). Otherwise: the other person in the exchange, i.e.
    the previous speaker if still present, else the next one if present."""
    out, present, last = {}, set(), None
    speeches = [it for it in items if it["type"] == "speech"]
    for it in items:
        if it["type"] == "direction":
            sd = narrate.script_direction(it["raw"], last)
            if sd:
                kind, keys = sd
                if kind in ("enter", "reenter"):
                    present |= set(keys)
                elif kind == "exeunt_all":
                    present = set()
                else:
                    present -= set(keys)
            continue
        if it["type"] != "speech":
            continue
        sp = it["speaker"]
        present.add(sp)
        last = sp
        if "to" in it:              # set by hand in review: who is really addressed (null = self)
            out[it["tag"]] = it["to"]
            continue
        d = it["delivery"] or ""
        if d == "Aside":
            out[it["tag"]] = None
            continue
        if d.startswith("To "):
            out[it["tag"]] = narrate.lookup(d[3:])
            continue
        k = speeches.index(it)
        prev = next((s["speaker"] for s in reversed(speeches[:k]) if s["speaker"] != sp), None)
        nxt = next((s["speaker"] for s in speeches[k + 1:] if s["speaker"] != sp), None)
        if prev in present:
            out[it["tag"]] = prev
        elif nxt in present:
            out[it["tag"]] = nxt
        else:
            # someone silent may still be on stage (the Nurse in 4.3)
            others = sorted(present - {sp})
            out[it["tag"]] = others[0] if len(others) == 1 else None
    return out


# ---------- checks ----------

def item_level(it, to):
    """Speech level for an item: a hand-set 'level' wins (review), then plain
    for directions, else the register table for speaker -> addressee."""
    if it.get("level"):
        return it["level"]
    if it["type"] == "direction":
        return "plain"
    return level(it["speaker"], to.get(it["tag"]))


def check(it, en, ko, lvl):
    errs = []
    if len(ko) != len(en):
        return [f"{len(ko)} Korean sentences for {len(en)} English ones"]
    for e, k in zip(en, ko):
        if not k.strip():
            errs.append(f"empty Korean for: {e[:50]}")
        if HANZI.search(k):
            errs.append(f"Chinese characters in: {k[:40]}")
        if LATIN.search(k):
            errs.append(f"English letters in: {k[:40]}")
        if len(k) > max(20, 1.3 * len(e)):
            errs.append(f"Korean longer than the English: {k[:40]}")
    all_en, all_ko = " ".join(en), " ".join(ko)
    for name, kname in NAME_KO.items():
        if re.search(rf"\b{re.escape(name)}\b", all_en) and kname.split()[0] not in all_ko:
            errs.append(f"name {name} must be written {kname}")
    if it["type"] == "speech" and lvl in ("haeyo", "hasipsio"):
        bad = [k for k in ko if PLAIN.search(k) and not POLITE.search(k)]
        if bad:
            errs.append(f"speech level must be {lvl} (…요/…니다), but: {bad[0][:40]}")
    elif lvl in ("banmal", "plain"):
        bad = [k for k in ko if POLITE.search(k)]
        if bad:
            errs.append(f"speech level must be {lvl} (no …요/…니다), but: {bad[0][:40]}")
    return errs


def clean(k):
    k = k.strip().replace("“", "'").replace("”", "'").replace('"', "'")
    return re.sub(r"\s+", " ", k)


# ---------- model ----------

def call(prompt, spec):
    """spec: {tag: n}. Each tag must come back as a list of exactly n strings."""
    schema = {"type": "object",
              "properties": {t: {"type": "array", "items": {"type": "string"},
                                 "minItems": n, "maxItems": n} for t, n in spec.items()},
              "required": list(spec), "additionalProperties": False}
    body = json.dumps({"model": "gemma4:12b", "prompt": prompt, "stream": False, "think": False,
                       "format": schema, "options": {"temperature": 0.2, "num_ctx": 8192}}).encode()
    req = urllib.request.Request(simplify.OLLAMA, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        return json.loads(json.loads(r.read())["response"])


PROMPT = """You translate simple English into natural, simple modern Korean for a bilingual app for Korean readers. The text is Shakespeare's "Romeo and Juliet", already rewritten into plain English. It will be read aloud.

Each item has numbered English sentences. Return a list with EXACTLY one Korean sentence for each English sentence, in the same order. Never merge or split sentences.

Rules:
1. Natural spoken Korean, not word-for-word. Short and clear. Do not add explanations.
2. Use exactly the speech level given for each item ("level"). Every sentence of that item must use it.
3. Names are fixed: {names}
4. Useful words: {terms}
5. "direction" items are the narrator describing the stage: present tense, 해라체 (…한다).
6. Quotations inside a sentence use single quotes ' '.
7. Write only Korean (Hangul). No Chinese characters, no English words.

{context}Translate these items:
{items}"""


def names_block():
    return ", ".join(f"{k} = {v}" for k, v in NAME_KO.items())


def terms_block():
    return ", ".join(f"{k} = {v}" for k, v in G["terms_ko"].items())


def run(ch, force=False):
    path = os.path.join(JSON_DIR, f"ch_{ch:02d}.json")
    items = json.load(open(path, encoding="utf-8"))
    need = {x["tag"] for x in simplify.model_items(json.loads(json.dumps(items)))}
    to = addressees(items)
    todo = [it for it in items if it["tag"] in need and it["sentences"]
            and (force or any(not s.get("ko") for s in it["sentences"]))]
    lvl = {it["tag"]: item_level(it, to) for it in todo}
    results, t0 = {}, time.time()
    order = [it["tag"] for it in items]
    for c in range(0, len(todo), CHUNK):
        pending = todo[c:c + CHUNK]
        label = f"{pending[0]['tag']}..{pending[-1]['tag']}"
        first = order.index(pending[0]["tag"])
        before = [x for x in items[max(0, first - 3):first] if x["sentences"] and x["type"] != "header"][-2:]
        context = ""
        if before:
            context = "The lines just before (for context only):\n" + "\n".join(
                f"- {x['speaker'] or 'narrator'}: " + " ".join(s["en"] for s in x["sentences"]) for x in before) + "\n\n"
        feedback = ""
        for attempt in range(1, RETRIES + 1):
            payload = {}
            for it in pending:
                t = it["tag"]
                entry = {"type": it["type"],
                         "level": LEVEL_TEXT[lvl[t]],
                         "sentences": {str(i + 1): s["en"] for i, s in enumerate(it["sentences"])}}
                if it["type"] == "speech":
                    entry["speaker"] = SPEAKERS[it["speaker"]]["en"]
                    if to.get(t):
                        entry["speaking to"] = SPEAKERS[to[t]]["en"]
                payload[t] = entry
            prompt = (PROMPT.replace("{names}", names_block()).replace("{terms}", terms_block())
                      .replace("{context}", context)
                      .replace("{items}", json.dumps(payload, ensure_ascii=False, indent=1)))
            try:
                ans = call(prompt + feedback, {it["tag"]: len(it["sentences"]) for it in pending})
            except (ValueError, OSError) as e:
                print(f"  {label} try {attempt}: call failed: {e}")
                continue
            errs, still = [], []
            for it in pending:
                en = [s["en"] for s in it["sentences"]]
                ko = [clean(k) for k in ans.get(it["tag"], [])]
                e = check(it, en, ko, lvl[it["tag"]])
                if e:
                    errs += [f"{it['tag']}: {x}" for x in e]
                    still.append(it)
                else:
                    results[it["tag"]] = ko
            pending = still
            if not pending:
                print(f"  {label} ok (try {attempt}, {time.time() - t0:.0f}s)")
                break
            print(f"  {label} try {attempt}: " + "; ".join(errs[:3]))
            feedback = ("\n\nYour previous answer was rejected for these problems. Fix all of them:\n- "
                        + "\n- ".join(errs))
        else:
            sys.exit(f"ch_{ch:02d}: {', '.join(it['tag'] for it in pending)} failed {RETRIES} times; nothing written")
    for it in items:
        if it["tag"] in results:
            for s, k in zip(it["sentences"], results[it["tag"]]):
                s["ko"] = k
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
    print(f"ch_{ch:02d}: {len(results)} items translated, {time.time() - t0:.0f}s")


def show(ch):
    items = json.load(open(os.path.join(JSON_DIR, f"ch_{ch:02d}.json"), encoding="utf-8"))
    to = addressees(items)
    for it in items:
        if it["type"] == "header" or not it["sentences"]:
            continue
        lv = item_level(it, to)
        print(f"── {it['tag']} {it['speaker'] or '(direction)'} → {to.get(it['tag'])} [{lv}]")
        for s in it["sentences"]:
            print(f"   {s['en']}\n   {s.get('ko') or '⚙'}")
        print()


def main():
    args = sys.argv[1:]
    target = next(a for a in args if not a.startswith("--"))
    chapters = range(1, 25) if target == "all" else [int(target)]
    for ch in chapters:
        if "--show" in args:
            show(ch)
        else:
            run(ch, "--force" in args)


if __name__ == "__main__":
    main()
