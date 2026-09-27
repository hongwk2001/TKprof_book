"""
Turn json/ch_NN.json into narrated app cards.

    python narrate.py 1            # print ch_01 as it will read (uses sentences if filled)
    python narrate.py 1 --raw      # same, with Shakespeare's raw text as stand-in
    python narrate.py 1 --json     # print the exact card JSON the app will get
    python narrate.py all --raw    # one summary line per chapter

Prints only; it never writes a file. json/ch_NN.json is the single source,
and the migrate script writes the app assets from this same code.

The model never writes narration. Everything here is deterministic:

  speech     -> Sampson says, "..."          / 샘슨이 말한다. "..."
                asks / 묻는다 when the card's text ends in "?"
  delivery   -> Aside: says to himself       / 혼잣말로 말한다
                Within: calls from inside    / 안에서 부른다
                To X: says to X              / X에게 말한다
  continued  -> Romeo goes on, "..."         / 로미오가 말을 잇는다. "..."
                (same speaker again after a direction in between)
  Enter X.   -> X enters.                    / X가 들어온다.
                merged into "X enters and says, ..." when X speaks next
  Re-enter X -> X comes back.                / X가 다시 들어온다.
  Exit.      -> <last speaker> leaves.       / <last speaker>가 나간다.
  Exit X.    -> X leaves.                    / X가 나간다.
  Exeunt.    -> They all leave.              / 모두 나간다.

Any direction these rules can't place (unknown name, extra detail) needs
Stage 4 sentences from the model; in a preview it shows marked with ⚙.

Long speeches split across cards of at most CARD_CAP chars; only the first
card carries "X says,", and every card is its own quote so a card reads
correctly on its own.
"""

import os
import re
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
GLOSSARY = json.load(open(os.path.join(BASE_DIR, "glossary.json"), encoding="utf-8"))
SPEAKERS = GLOSSARY["speakers"]

CARD_CAP = 300
PENDING = "⚙"
REFLEXIVE = {"m": "himself", "f": "herself", "n": "itself"}


# ---------- names and Korean particles ----------

def has_batchim(word):
    ch = word.strip()[-1]
    if not "가" <= ch <= "힣":
        return False
    return (ord(ch) - 0xAC00) % 28 != 0


def ko_subj(word):
    return word + ("이" if has_batchim(word) else "가")


def cap(s):
    return s[:1].upper() + s[1:]


def en_list(names):
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def ko_list(names):
    if len(names) == 1:
        return names[0]
    head = ", ".join(names[:-1])
    return head + ("과 " if has_batchim(names[-2]) else "와 ") + names[-1]


def lookup(name):
    """'Lady Capulet' / 'the Nurse' / 'first Servant' -> speaker key, or None."""
    key = re.sub(r"^(the|a|an)\s+", "", name.strip(), flags=re.I).upper().replace("’", "'")
    return key if key in SPEAKERS else None


def resolve(names_text):
    parts = [p for p in re.split(r",\s*|\s+and\s+", names_text) if p.strip()]
    keys = [lookup(p) for p in parts]
    return keys if keys and all(keys) else None


# ---------- directions the script can narrate ----------

def script_direction(raw, last_speaker):
    """Return (kind, [speaker keys]) or None if the model must handle it."""
    s = raw.strip().rstrip(".")
    if s == "Exit":
        return ("exit", [last_speaker]) if last_speaker else None
    if s == "Exeunt":
        return ("exeunt_all", [])
    m = re.match(r"^(Exit|Exeunt|Enter|Re-enter)\s+(.+)$", s)
    if not m:
        return None
    keys = resolve(m.group(2))
    if not keys:
        return None
    kind = {"Exit": "exit", "Exeunt": "exit", "Enter": "enter", "Re-enter": "reenter"}[m.group(1)]
    return (kind, keys)


def render_direction(kind, keys):
    if kind == "exeunt_all":
        return "They all leave.", "모두 나간다."
    en = cap(en_list([SPEAKERS[k]["en"] for k in keys]))
    ko = ko_subj(ko_list([SPEAKERS[k]["ko"] for k in keys]))
    one = len(keys) == 1
    if kind == "enter":
        return f"{en} {'enters' if one else 'enter'}.", f"{ko} 들어온다."
    if kind == "reenter":
        return f"{en} {'comes' if one else 'come'} back.", f"{ko} 다시 들어온다."
    return f"{en} {'leaves' if one else 'leave'}.", f"{ko} 나간다."


# ---------- speech ----------

def raw_sentences(raw):
    text = " ".join(line.strip() for line in raw.splitlines())
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z‘“’'])", text)
    return [(p, "…") for p in parts if p.strip()]


def item_sentences(item, use_raw):
    if item["sentences"]:
        return [(s["en"], s.get("ko") or PENDING) for s in item["sentences"]]
    if use_raw:
        return raw_sentences(item["raw"])
    return [(PENDING + " " + item["raw"], PENDING)]


def attribution(item, mode, question):
    """(en prefix, ko prefix) for the first card of a speech."""
    sp = SPEAKERS[item["speaker"]]
    who_en, who_ko = cap(sp["en"]), ko_subj(sp["ko"])
    d = item["delivery"] or ""
    if mode == "enter":
        return (f"{who_en} enters and {'asks' if question else 'says'},",
                f"{who_ko} 들어와 {'묻는다' if question else '말한다'}.")
    if mode == "continue":
        return f"{who_en} goes on,", f"{who_ko} 말을 잇는다."
    if d == "Aside":
        ref = REFLEXIVE[sp["g"]]
        return (f"{who_en} {'asks' if question else 'says to'} {ref},",
                f"{who_ko} 혼잣말로 {'묻는다' if question else '말한다'}.")
    if d == "Within":
        return f"{who_en} calls from inside,", f"{who_ko} 안에서 부른다."
    if d.startswith("To "):
        to = lookup(d[3:])
        to_en = SPEAKERS[to]["en"] if to else d[3:]
        to_ko = SPEAKERS[to]["ko"] if to else d[3:]
        return (f"{who_en} {'asks' if question else 'says to'} {to_en},",
                f"{who_ko} {to_ko}에게 {'묻는다' if question else '말한다'}.")
    return (f"{who_en} {'asks' if question else 'says'},",
            f"{who_ko} {'묻는다' if question else '말한다'}.")


def group_cards(pairs, first_prefix_len):
    groups, cur, size = [], [], first_prefix_len
    for en, ko in pairs:
        add = len(en) + (1 if cur else 0)
        if cur and size + add + 2 > CARD_CAP:
            groups.append(cur)
            cur, size = [], 0
            add = len(en)
        cur.append((en, ko))
        size += add
    if cur:
        groups.append(cur)
    return groups


def speech_cards(item, mode, use_raw):
    pairs = item_sentences(item, use_raw)
    groups = group_cards(pairs, 30)          # ~ room for "Friar Lawrence goes on, "
    cards = []
    for n, g in enumerate(groups):
        en = " ".join(e for e, _ in g)
        ko = " ".join(k for _, k in g)
        if n == 0:
            question = en.rstrip("’'\"”").endswith("?")
            pen, pko = attribution(item, mode, question)
            en, ko = f'{pen} "{en}"', f'{pko} "{ko}"'
        else:
            en, ko = f'"{en}"', f'"{ko}"'
        cards.append({"tag": f"{item['tag']}_{n + 1}", "en": en, "ko": ko,
                      "is_header": False, "src": "speech"})
    return cards


# ---------- chapter ----------

def build_cards(items, use_raw=False):
    cards = []
    last_speaker = None       # speaker of the most recent speech
    since_speech = []         # directions seen since that speech
    merged_enter = False      # the previous direction was folded into this speech
    for i, it in enumerate(items):
        if it["type"] == "header":
            ko_loc = it["sentences"][0]["ko"] if it["sentences"] else PENDING
            cards.append({"tag": it["tag"], "en": it["raw"],
                          "ko": f"{it['act']}막 {it['scene']}장 — {ko_loc}",
                          "is_header": True, "src": "header"})
            continue

        if it["type"] == "direction":
            sd = script_direction(it["raw"], last_speaker)
            nxt = items[i + 1] if i + 1 < len(items) else None
            if (sd and sd[0] == "enter" and len(sd[1]) == 1 and nxt
                    and nxt["type"] == "speech" and nxt["speaker"] == sd[1][0]
                    and not nxt["delivery"]):
                merged_enter = True
                continue
            since_speech.append(it)
            if sd:
                en, ko = render_direction(*sd)
                src = "script"
            elif it["sentences"]:
                en = " ".join(s["en"] for s in it["sentences"])
                ko = " ".join(s.get("ko") or PENDING for s in it["sentences"])
                src = "model"
            else:
                en, ko, src = f"{PENDING} [{it['raw']}]", PENDING, "model"
            cards.append({"tag": it["tag"], "en": en, "ko": ko,
                          "is_header": False, "src": src})
            continue

        # speech
        if merged_enter:
            mode = "enter"
        elif it["speaker"] == last_speaker and since_speech and not it["delivery"]:
            mode = "continue"
        else:
            mode = "say"
        cards.extend(speech_cards(it, mode, use_raw))
        merged_enter = False
        last_speaker = it["speaker"]
        since_speech = []
    return cards


def load(ch):
    return json.load(open(os.path.join(JSON_DIR, f"ch_{ch:02d}.json"), encoding="utf-8"))


def render_text(cards):
    out = []
    for c in cards:
        mark = "#" if c["is_header"] else " "
        out.append(f"{mark} {c['tag']:<9} {c['en']}")
        out.append(f"  {'':<9} {c['ko']}")
        out.append("")
    return "\n".join(out)


def summary(cards):
    body = [c for c in cards if not c["is_header"]]
    by = {}
    for c in body:
        by[c["src"]] = by.get(c["src"], 0) + 1
    over = [c for c in body if len(c["en"]) > CARD_CAP]
    return (f"{len(body)} cards: {by.get('speech', 0)} speech, "
            f"{by.get('script', 0)} script directions, {by.get('model', 0)} model directions; "
            f"{len(over)} over {CARD_CAP} chars")


def main():
    args = sys.argv[1:]
    use_raw = "--raw" in args
    target = next((a for a in args if not a.startswith("--")), "1")
    chapters = range(1, 25) if target == "all" else [int(target)]
    for ch in chapters:
        cards = build_cards(load(ch), use_raw)
        if len(chapters) == 1:
            if "--json" in args:
                print(json.dumps(cards, ensure_ascii=False, indent=1))
                continue
            print(render_text(cards))
        print(f"ch_{ch:02d}: {summary(cards)}")


if __name__ == "__main__":
    main()
