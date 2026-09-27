"""
Vocabulary check for Korean learners: list the uncommon words in the English.

    python vocab.py            # words below ZIPF, most frequent in the play first
    python vocab.py 3.0        # a different threshold

Frequency is wordfreq's Zipf scale (7 = "the", 5 = "friend", 4 = "dagger"
region, 3 = rare). Around 3.5 is where a B1 learner starts to stumble.
Names and glossary terms are skipped. Prints only; writes nothing.
"""

import os
import re
import sys
import json
import collections

from wordfreq import zipf_frequency

import narrate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
ZIPF = float(sys.argv[1]) if len(sys.argv) > 1 else 3.5

SKIP = {w.lower() for s in narrate.SPEAKERS.values() for w in re.findall(r"[A-Za-z]+", s["en"])}
SKIP |= {w.lower() for n in narrate.GLOSSARY["names"] for w in n.split()}


def main():
    seen = collections.defaultdict(list)
    for ch in range(1, 25):
        for it in json.load(open(os.path.join(JSON_DIR, f"ch_{ch:02d}.json"), encoding="utf-8")):
            for s in it["sentences"]:
                for m in re.finditer(r"[A-Za-z][A-Za-z'’-]*", s["en"]):
                    w = m.group(0).replace("’", "'")
                    if w[0].isupper() and m.start() > 0:      # a name mid-sentence
                        continue
                    lw = w.lower().split("'")[0]
                    if lw in SKIP or zipf_frequency(lw, "en") >= ZIPF:
                        continue
                    seen[lw].append((it["tag"], s["en"]))
    rows = sorted(seen.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    print(f"{len(rows)} words below Zipf {ZIPF}")
    for w, uses in rows:
        tag, ex = uses[0]
        print(f"{w:<16} {zipfs(w):>4}  x{len(uses):<3} {tag}  {ex[:90]}")


def zipfs(w):
    return f"{zipf_frequency(w, 'en'):.1f}"


if __name__ == "__main__":
    main()
