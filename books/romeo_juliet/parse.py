"""
Stage 3: split raw/pg1513.txt into json/ch_NN.json, one chapter per scene.

    python parse.py            # write json/ (refuses to overwrite translated work)
    python parse.py --stats    # print per-chapter counts, write nothing

Each item is one unit of the play:
  header    - chapter title (act/scene/location)
  speech    - one speaker's uninterrupted lines; `raw` keeps verse line breaks
  direction - a stage direction, bracket/underscore markup removed

Layout rules (Gutenberg #1513):
  - a stage direction is indented exactly ONE space;
  - song lines inside a speech are indented two or more, so they stay speech;
  - `Aside` / `Within` / `To <name>` at the very start of a speech says how
    the line is delivered, not what happens: stored as the speech's
    `delivery`, and the narrator folds it into "says to himself" etc.

A direction inside a spoken line ("Here's to my love! [_Drinks._] O true
apothecary!") splits the speech into speech / direction / speech with the
same speaker, so the action gets its own card and never hides mid-sentence.

The two Chorus prologues are folded into the first scene of Acts 1 and 2.
`sentences` is empty until Stage 4 fills it; it is the only thing later
stages write, so re-running this parser is safe only while all are empty.
"""

import os
import re
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE_DIR, "raw", "pg1513.txt")
JSON_DIR = os.path.join(BASE_DIR, "json")

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}
SPEAKER_RE = re.compile(r"^([A-Z][A-Z’' ]+)\.$")
ACT_RE = re.compile(r"^ACT ([IVX]+)$")
SCENE_RE = re.compile(r"^SCENE ([IVX]+)\. (.+)$")
INLINE_DIR_RE = re.compile(r"\s*\[_(.+?)_?\]\s*")
DELIVERY_RE = re.compile(r"^(Aside|Within|To [A-Z][a-z]+)\.?$")


def body_lines():
    text = open(RAW, encoding="utf-8").read()
    start = text.index("THE PROLOGUE\n\n")          # skip contents + cast list
    end = text.index("*** END OF THE PROJECT GUTENBERG")
    return text[start:end].splitlines()


def clean_direction(s):
    s = s.strip()
    s = re.sub(r"^\[_?|_?\]$", "", s)
    return s.replace("_", "").strip()


def is_direction_line(line):
    return line.startswith(" ") and not line.startswith("  ") and bool(line.strip())


def parse():
    scenes = []          # list of dicts: act, scene, location, items
    prologue = []        # items waiting to be folded into the next scene
    act = 0
    cur = None           # current scene
    speaker = None
    buf = []             # lines of the speech being built
    delivery = None      # Aside / Within / To X for the speech being built
    started = False      # has the current speaker said anything yet

    def target():
        return cur["items"] if cur else prologue

    def flush():
        nonlocal buf, delivery
        text = "\n".join(buf).strip()
        if text:
            target().append({"type": "speech", "speaker": speaker,
                             "delivery": delivery, "raw": text})
            delivery = None
        buf = []

    def add_direction(s):
        flush()
        s = clean_direction(s)
        if s:
            target().append({"type": "direction", "speaker": None,
                             "delivery": None, "raw": s})

    lines = body_lines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if line.strip() in ("THE PROLOGUE",):
            continue
        m = ACT_RE.match(line)
        if m:
            flush()
            speaker = None
            act = ROMAN[m.group(1)]
            cur = None
            continue
        m = SCENE_RE.match(line)
        if m:
            flush()
            speaker = None
            cur = {"act": act or 1, "scene": ROMAN[m.group(1)],
                   "location": m.group(2).rstrip("."), "items": prologue}
            prologue = []
            scenes.append(cur)
            continue
        m = SPEAKER_RE.match(line)
        if m:
            flush()
            speaker = m.group(1).replace("’", "'")
            started = False
            continue
        if is_direction_line(line):
            # an indented direction may wrap onto further indented lines
            d = [line.strip()]
            while i < len(lines) and is_direction_line(lines[i]):
                d.append(lines[i].strip())
                i += 1
            add_direction(" ".join(d))
            continue
        if not line.strip():
            continue
        if speaker is None:
            raise ValueError(f"text with no speaker: {line!r}")
        # split on inline directions
        parts = INLINE_DIR_RE.split(line)
        for k, part in enumerate(parts):
            if k % 2 == 0:
                if part.strip():
                    buf.append(part.strip())
                    started = True
            elif not started and DELIVERY_RE.match(clean_direction(part)):
                delivery = clean_direction(part).rstrip(".")
            else:
                add_direction(part)
    flush()
    return scenes


def build(scenes):
    chapters = []
    pid = 0
    for n, sc in enumerate(scenes, 1):
        cid = f"ch_{n:02d}"
        items = [{
            "type": "header", "speaker": None, "delivery": None,
            "raw": f"Act {sc['act']}, Scene {sc['scene']} — {sc['location']}",
        }] + sc["items"]
        out = []
        for it in items:
            pid += 1
            out.append({
                "id": pid,
                "tag": f"P{pid:04d}",
                "chapter_id": cid,
                "act": sc["act"],
                "scene": sc["scene"],
                "type": it["type"],
                "speaker": it["speaker"],
                "delivery": it["delivery"],
                "raw": it["raw"],
                "sentences": [],
            })
        chapters.append(out)
    return chapters


def stats(chapters):
    tw = 0
    print(f"{'ch':6}{'act.sc':8}{'speech':>7}{'dir':>5}{'words':>7}{'max ch':>8}  location")
    for ch in chapters:
        sp = [x for x in ch if x["type"] == "speech"]
        dr = [x for x in ch if x["type"] == "direction"]
        w = sum(len(x["raw"].split()) for x in sp)
        mx = max(len(x["raw"]) for x in sp)
        tw += w
        h = ch[0]
        print(f"{h['chapter_id']:6}{h['act']}.{h['scene']:<6}{len(sp):>7}{len(dr):>5}{w:>7}{mx:>8}  "
              f"{h['raw'].split(' — ')[1]}")
    print(f"total words {tw}, items {sum(len(c) for c in chapters)}")


def main():
    chapters = build(parse())
    if "--stats" in sys.argv:
        stats(chapters)
        return
    os.makedirs(JSON_DIR, exist_ok=True)
    for ch in chapters:
        path = os.path.join(JSON_DIR, f"{ch[0]['chapter_id']}.json")
        if os.path.exists(path):
            old = json.load(open(path, encoding="utf-8"))
            if any(x["sentences"] or x.get("drafts") for x in old):
                sys.exit(f"refusing to overwrite {path}: it already has sentences or drafts")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(ch, f, ensure_ascii=False, indent=1)
    stats(chapters)


if __name__ == "__main__":
    main()
