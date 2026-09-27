"""
Stage 4: Shakespeare -> short, simple modern English, written into json/ as drafts.

    python simplify.py 7                 # gemma4 drafts for ch_07
    python simplify.py 7 --engine gemma4
    python simplify.py 7 --name gemma4_gloss   # save under another drafts key
    python simplify.py 7 --no-gloss      # baseline without glossary.json → gloss
    python simplify.py 7 --show          # print raw vs every draft, write nothing

Nothing is written outside json/ch_NN.json, and nothing is written at all
unless the WHOLE scene passes:

  1. Items are sent keyed by tag, and the answer schema makes exactly those
     tags required keys (Ollama structured output), so the model cannot
     skip, add or reorder an item.
  2. check_item() re-verifies every item: exact key set, no empty answer,
     sentence length, no archaic words, no speaker labels, and no character
     name that isn't in the raw line (or, for a direction, the people around it).
  3. A failing chunk is retried; if it still fails, the scene is abandoned
     and the file is left untouched.

Accepted output goes into each item's own `drafts[engine]`; promote.py later
copies the chosen engine into `sentences`.

Items the narrator writes itself (headers, bare Enter/Exit/Exeunt with known
names — see narrate.script_direction) are never sent.
"""

import os
import re
import sys
import json
import time
import urllib.request

import narrate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
OLLAMA = "http://localhost:11434/api/generate"

CHUNK = 8              # items per request
CONTEXT = 4            # preceding items shown for continuity, not answered
MAX_WORDS = 25         # hard limit per sentence (the target in the prompt is 20)
RETRIES = 5

ARCHAIC = re.compile(
    r"\b(thou|thee|thy|thine|doth|dost|hath|hast|shalt|wilt|'tis|’tis|'twas|’twas|"
    r"wherefore|ere|nay|anon|prithee|methinks|forsooth|o'er|o’er|whither|hither|"
    r"thither|hence|whence|mayst|canst|art thou|thou art)\b", re.I)
LABEL = re.compile(r"^[A-Z][A-Z' ]{2,}[:.]\s")
# a whole sentence: starts with a capital (or quote / digit), ends with . ! ? —
# (a trailing — is allowed because Shakespeare's speakers get cut off mid-line)
SENTENCE = re.compile(r"^['‘\"“(]?[A-Z0-9].*[.!?—…]['’\"”)]?$", re.S)

# every character / place name the checker polices
NAMES = sorted({re.sub(r"^(the|a) ", "", s["en"], flags=re.I).split("'")[0]
                for s in narrate.SPEAKERS.values()
                if s["en"][0].isupper()} | set(narrate.GLOSSARY["names"]) |
               {"Capulet", "Montague", "Rosaline", "Petrucio", "Valentine", "Cupid",
                "Dian", "Venus", "Phoebus", "Phaeton", "Mab"}, key=len, reverse=True)

PROMPT = """You rewrite Shakespeare's "Romeo and Juliet" into simple modern English for Korean learners of English (CEFR level B1).

You get a JSON object. Each key is an item id. Each value has:
- "type": "speech" (words a character says) or "direction" (a stage direction)
- "speaker": who says the speech; for a direction, "around" lists who spoke just before and after
- "raw": Shakespeare's text

For EVERY key, return a list of short sentences in plain modern English.

Rules:
1. Keep the full meaning of every line. Do not skip anything. Do not add ideas, jokes, feelings or explanations that are not in the text.
2. One idea per sentence. At most 20 words per sentence. Use common, everyday words. Every list entry must be a complete sentence that starts with a capital letter and ends with . ! or ? — never split one sentence across two entries.
3. Never use old words: thou, thee, thy, thine, art, doth, hath, 'tis, wherefore, ere, nay, anon, hence, prithee, o'er, marry.
4. Never add a person's name that is not in the raw text. Do not write who is speaking; the speaker is added later.
5. For wordplay that cannot be kept in modern English, keep the plain meaning and drop the pun.
6. Keep famous lines recognizable, e.g. "O Romeo, Romeo, wherefore art thou Romeo?" becomes "Oh Romeo, Romeo, why are you Romeo?"
7. A "direction" becomes one or two short present-tense narrator sentences, e.g. "Juliet appears at a window above." Say who acts, using only names from "raw" or "around".
8. Speech is in the first person, as the character talks. Use single quotes ' ' for any quotation inside a speech, never double quotes.
9. Shakespeare often uses 'and' or 'an' to mean 'if' at the start of a condition: 'And I were so apt to quarrel as thou art' means 'If I were as quick to fight as you are'.
10. Keep famous lines close to the original words, e.g. 'A plague o' both your houses' becomes 'A plague on both your houses'.
11. Return exactly the keys you were given, no more and no fewer.

{gloss}{context}Rewrite these items:
{items}"""


# ---------- which items the model handles ----------

def model_items(items):
    """Speech, and directions the narrator can't script, with context for each."""
    out = []
    last = None
    for i, it in enumerate(items):
        if it["type"] == "speech":
            out.append(it)
            last = it["speaker"]
        elif it["type"] == "direction" and not narrate.script_direction(it["raw"], last):
            nxt = next((x["speaker"] for x in items[i + 1:] if x["type"] == "speech"), None)
            it["_around"] = [p for p in dict.fromkeys([last, nxt]) if p]
            out.append(it)
    return out


GLOSS = narrate.GLOSSARY.get("gloss", {})


def gloss_hits(chunk):
    text = " ".join(it["raw"] for it in chunk).replace("’", "'").lower()
    return [(k, v) for k, v in GLOSS.items()
            if re.search(rf"(?<![\w']){re.escape(k.lower())}(?![\w'])", text)]


def gloss_block(chunk):
    """Meanings for the Shakespeare words that actually occur in this chunk."""
    hits = gloss_hits(chunk)
    if not hits:
        return ""
    return ("Meanings of old words in these lines. They are correct. Write the plain modern meaning in your sentence; never copy the old word itself:\n"
            + "\n".join(f"- {k}: {v}" for k, v in hits) + "\n\n")


def payload(it):
    if it["type"] == "speech":
        v = {"type": "speech", "speaker": narrate.SPEAKERS[it["speaker"]]["en"], "raw": it["raw"]}
    else:
        v = {"type": "direction",
             "around": [narrate.SPEAKERS[s]["en"] for s in it["_around"]], "raw": it["raw"]}
    return v


# ---------- checks ----------

def names_in(text):
    found, t = set(), text
    for n in NAMES:
        if re.search(rf"\b{re.escape(n)}\b", t):
            found.add(n)
            t = re.sub(rf"\b{re.escape(n)}\b", " ", t)
    return found


def check_item(it, sents):
    errs = []
    if not isinstance(sents, list) or not sents or not all(isinstance(s, str) and s.strip() for s in sents):
        return ["empty or malformed answer"]
    # a name the gloss supplies for this line is not an addition ("the County" = Paris)
    allowed_src = it["raw"] + " " + " ".join(v for _, v in gloss_hits([it]))
    if it["type"] == "direction":
        allowed_src += " " + " ".join(narrate.SPEAKERS[s]["en"] for s in it["_around"])
    allowed = names_in(allowed_src)
    for s in sents:
        w = len(s.split())
        if w > MAX_WORDS:
            errs.append(f"{w} words: {s[:60]}")
        m = ARCHAIC.search(s)
        if m:
            errs.append(f"archaic '{m.group(0)}': {s[:60]}")
        if LABEL.match(s):
            errs.append(f"speaker label: {s[:60]}")
        if not SENTENCE.match(s.strip()):
            errs.append(f"not a whole sentence: {s[:60]}")
        extra = names_in(s) - allowed
        if extra:
            errs.append(f"added name {sorted(extra)}: {s[:60]}")
    raw_w, out_w = len(it["raw"].split()), sum(len(s.split()) for s in sents)
    if raw_w >= 8 and not 0.5 <= out_w / raw_w <= 2.5:
        errs.append(f"length {out_w} words for {raw_w} raw words")
    return errs


def fix_cutoff(it, sents):
    """Mechanical repair of split sentences, before checking:
    an entry ending in a comma (or with no end punctuation) is joined to the next
    one, and a speaker cut off mid-line ('I do beseech thee,—') ends on a dash.
    The joined sentence still has to pass check_item (length etc.)."""
    if not (isinstance(sents, list) and all(isinstance(s, str) for s in sents)):
        return sents
    out = []
    for s in (x.strip() for x in sents if x.strip()):
        if out and not re.search(r"[.!?—…]['’\"”)]?$", out[-1]):
            # mid-sentence now: lowercase unless it's "I", a name or God
            word = re.sub(r"[^\w'’]", "", s.split(" ")[0])
            if not (word == "I" or re.match(r"I['’]", word) or word in NAMES
                    or word in {"God", "Jove", "Heaven"}):
                s = s[0].lower() + s[1:]
            out[-1] = out[-1] + " " + s
        else:
            out.append(s)
    if out and it["raw"].rstrip().endswith("—") and out[-1].endswith(","):
        out[-1] = out[-1][:-1] + "—"
    return out


def clean(s):
    s = s.strip().replace("“", "'").replace("”", "'").replace('"', "'")
    return re.sub(r"\s+", " ", s)


# ---------- engines ----------

def call_ollama(prompt, keys, model="gemma4:12b"):
    schema = {"type": "object",
              "properties": {k: {"type": "array", "items": {"type": "string"}} for k in keys},
              "required": keys, "additionalProperties": False}
    body = json.dumps({"model": model, "prompt": prompt, "stream": False, "think": False,
                       "format": schema,
                       "options": {"temperature": 0.2, "num_ctx": 8192}}).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        return json.loads(json.loads(r.read())["response"])


ENGINES = {"gemma4": call_ollama}


# ---------- run ----------

def run(ch, engine, name, use_gloss=True):
    path = os.path.join(JSON_DIR, f"ch_{ch:02d}.json")
    items = json.load(open(path, encoding="utf-8"))
    todo = model_items(items)
    call = ENGINES[engine]
    results = {}
    t0 = time.time()
    for c in range(0, len(todo), CHUNK):
        chunk = todo[c:c + CHUNK]
        keys = [it["tag"] for it in chunk]
        prev = todo[max(0, c - CONTEXT):c]
        context = ""
        if prev:
            context = ("For context only, the lines just before (do not rewrite these):\n"
                       + json.dumps({it["tag"]: payload(it) for it in prev},
                                    ensure_ascii=False, indent=1) + "\n\n")
        label = f"{keys[0]}..{keys[-1]}"
        pending = list(chunk)          # items still without an accepted answer
        feedback = ""
        for attempt in range(1, RETRIES + 1):
            pkeys = [it["tag"] for it in pending]
            prompt = (PROMPT.replace("{gloss}", gloss_block(pending) if use_gloss else "")
                      .replace("{context}", context)
                      .replace("{items}", json.dumps({it["tag"]: payload(it) for it in pending},
                                                     ensure_ascii=False, indent=1)))
            try:
                ans = call(prompt + feedback, pkeys)
            except (ValueError, OSError) as e:
                print(f"  {label} try {attempt}: call failed: {e}")
                continue
            if set(ans) != set(pkeys):
                errs = [f"keys differ: missing {sorted(set(pkeys) - set(ans))}, "
                        f"extra {sorted(set(ans) - set(pkeys))}"]
            else:
                # keep every item that passes; re-ask only the ones that don't
                errs, still = [], []
                for it in pending:
                    ans[it["tag"]] = fix_cutoff(it, ans[it["tag"]])
                    e = check_item(it, ans[it["tag"]])
                    if e:
                        errs += [f"{it['tag']}: {x}" for x in e]
                        still.append(it)
                    else:
                        results[it["tag"]] = [clean(s) for s in ans[it["tag"]]]
                pending = still
            if not pending:
                print(f"  {label} ok (try {attempt}, {time.time() - t0:.0f}s)")
                break
            print(f"  {label} try {attempt}: " + "; ".join(errs[:4]))
            # the same prompt at low temperature returns the same answer, so say what to fix
            feedback = ("\n\nYour previous answer was rejected for these problems. Fix all of them:\n- "
                        + "\n- ".join(errs)
                        + "\nEach list entry is one complete sentence of at most 20 words. "
                          "A clause like 'If you love me,' belongs in the same entry as the rest "
                          "of its sentence; a sentence that gets too long must be rewritten as "
                          "two or more complete sentences. For a long 'If you were ..., then you "
                          "could ...' sentence, first write short sentences like 'Imagine you were "
                          "young like me.' 'Imagine Juliet was your love.', then the result as its "
                          "own sentence: 'Then you could speak.'")
        else:
            sys.exit(f"ch_{ch:02d}: {len(pending)} item(s) in {label} failed {RETRIES} times "
                     f"({', '.join(it['tag'] for it in pending)}); nothing written")

    # whole scene passed: write drafts into the items themselves
    for it in items:
        it.pop("_around", None)
        if it["tag"] in results:
            it.setdefault("drafts", {})[name] = [{"en": s} for s in results[it["tag"]]]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)
    n = sum(len(v) for v in results.values())
    print(f"ch_{ch:02d}: {len(results)} items -> {n} sentences (drafts.{name}), "
          f"{time.time() - t0:.0f}s")


def show(ch):
    items = json.load(open(os.path.join(JSON_DIR, f"ch_{ch:02d}.json"), encoding="utf-8"))
    for it in items:
        if not it.get("drafts"):
            continue
        who = it["speaker"] or "(direction)"
        print(f"── {it['tag']} {who}")
        print("   RAW  " + it["raw"].replace("\n", " / "))
        for eng, sents in it["drafts"].items():
            print(f"   {eng:<6} " + " | ".join(s["en"] for s in sents))
        print()


def main():
    args = sys.argv[1:]
    ch = int(next(a for a in args if not a.startswith("--")))
    if "--show" in args:
        show(ch)
        return
    engine = args[args.index("--engine") + 1] if "--engine" in args else "gemma4"
    name = args[args.index("--name") + 1] if "--name" in args else engine
    run(ch, engine, name, use_gloss="--no-gloss" not in args)


if __name__ == "__main__":
    main()
