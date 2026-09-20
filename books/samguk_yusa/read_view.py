"""
Render batches/result_ch_NN.json as something a human can actually read.

The translation output is JSON keyed by item id, which is fine for migrate and
unreadable for a person. This writes one markdown file per chapter with the Korean
and English paragraphs paired, plus the hanmun the pair came from.

Each file is stamped with the register it was produced in, detected by counting
hanja in the Korean: voice D removes them entirely, the earlier formal register
glosses names inline. That stamp is the thing that was missing when a half-converted
book looked identical to a finished one.

Usage:  python read_view.py            # all chapters that have results
        python read_view.py ch_01
"""
import glob
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
BATCH = os.path.join(BASE, "batches")
OUT = os.path.join(BASE, "review")
HANJA = re.compile(r"[一-鿿]")


def voice_of(ko_text):
    """Voice D carries no hanja at all; the formal register glosses names inline."""
    n = len(HANJA.findall(ko_text))
    if n == 0:
        return "D (casual)", 0
    return "formal", n


def render(cid):
    rpath = os.path.join(BATCH, "result_%s.json" % cid)
    bpath = os.path.join(BATCH, "batch_%s.json" % cid)
    if not os.path.exists(rpath):
        return None
    result = json.load(open(rpath, encoding="utf-8"))
    items = result["items"]
    batch = json.load(open(bpath, encoding="utf-8"))
    title = batch.get("title") or cid
    src = {str(i["id"]): i for i in batch["items"]}

    all_ko = " ".join(p for v in items.values() for p in v["ko"])
    voice, hanja = voice_of(all_ko)

    lines = ["# %s — %s" % (cid, title), "",
             "**voice: %s**  ·  hanja in Korean: %d  ·  %d/%d items aligned"
             % (voice, hanja, result["aligned"], result["total"]), ""]

    for key, v in sorted(items.items(), key=lambda kv: int(kv[0])):
        item = src.get(key, {})
        mark = "  *(hand-written)*" if v.get("manual") else ""
        lines += ["---", "", "### %s%s" % (v["tag"], mark), ""]
        if item.get("hanmun"):
            lines += ["<sub>%s</sub>" % item["hanmun"], ""]
        for n, (k, e) in enumerate(zip(v["ko"], v["en"]), 1):
            lines += ["**%d.** %s" % (n, k), "", "> %s" % e, ""]
    return {"voice": voice, "hanja": hanja, "title": title,
            "text": "\n".join(lines),
            "aligned": result["aligned"], "total": result["total"]}


def main():
    os.makedirs(OUT, exist_ok=True)
    if len(sys.argv) > 1:
        cids = sys.argv[1:]
    else:
        cids = sorted(os.path.basename(f)[7:-5]
                      for f in glob.glob(os.path.join(BATCH, "result_ch_*.json")))

    index = ["# 삼국유사 — reading view", "",
             "One file per chapter, Korean and English paired under the hanmun they",
             "came from. `voice` says which register produced it.", "",
             "| chapter | title | voice | hanja | aligned |",
             "|---|---|---|---:|---|"]
    for cid in cids:
        got = render(cid)
        if not got:
            print("  %s: no result yet" % cid)
            continue
        with open(os.path.join(OUT, "%s.md" % cid), "w", encoding="utf-8") as fh:
            fh.write(got["text"])
        index.append("| [%s](%s.md) | %s | %s | %d | %d/%d |"
                     % (cid, cid, got["title"], got["voice"], got["hanja"],
                        got["aligned"], got["total"]))
        print("  %s  %-12s hanja %4d  %s" % (cid, got["voice"], got["hanja"], got["title"]))

    with open(os.path.join(OUT, "INDEX.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(index) + "\n")
    print("\nwrote %s" % OUT)


if __name__ == "__main__":
    main()
