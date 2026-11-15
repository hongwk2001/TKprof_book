"""Restore dialogue quotation marks in The Heroes.

The app text (json_app/, copied from Book_apps/the_heroes/src/main/assets/books)
has every quotation mark stripped. quotes/ch_XX.json says, per paragraph, where
the speech is, and this writes json/ch_XX.json with curly quotes in en and ko:

  "S"   whole paragraph is speech: open at start, close at end
  "So"  speech that runs on into the next paragraph: open only
  {"en": [...], "ko": [...], "c": true}
        each snippet is the text with quotes inserted; the same text without
        “ ” must occur exactly once in the paragraph. "@”" stands for a comma
        in the source that becomes ".”" (Korean: “…니다.” 하고 그가 말했습니다).
        A [old, new] pair replaces literally. "c" closes the quote at the end of the paragraph.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def strip(s):
    return s.replace("@”", ",").replace("“", "").replace("”", "")


def apply_paragraph(rows, spec, lang, where):
    if spec in ("S", "So"):
        rows[0][lang] = "“" + rows[0][lang]
        if spec == "S":
            rows[-1][lang] += "”"
        return
    if lang not in spec:  # e.g. the Korean is indirect speech: leave it alone
        return
    for snip in spec[lang]:
        old, new = snip if isinstance(snip, list) else (strip(snip), snip.replace("@”", ".”"))
        hits = [r for r in rows if old in r[lang]]
        n = sum(r[lang].count(old) for r in hits)
        if n != 1:
            sys.exit(f"{where} {lang}: {old!r} found {n} times")
        hits[0][lang] = hits[0][lang].replace(old, new)
    if spec.get("c"):
        rows[-1][lang] += "”"


def main():
    os.makedirs(os.path.join(HERE, "json"), exist_ok=True)
    for src in sorted(glob.glob(os.path.join(HERE, "json_app", "ch_*.json"))):
        name = os.path.basename(src)
        rows = json.load(open(src, encoding="utf-8"))
        qpath = os.path.join(HERE, "quotes", name)
        specs = json.load(open(qpath, encoding="utf-8")) if os.path.exists(qpath) else {}
        paras = {}
        for r in rows:
            if r["is_header"] or r.get("image"):
                continue
            paras.setdefault(r["tag"].split("_")[0][1:], []).append(r)
        for pid, spec in specs.items():
            if pid not in paras:
                sys.exit(f"{name} {pid}: no such paragraph")
            for lang in ("en", "ko"):
                apply_paragraph(paras[pid], spec, lang, f"{name} {pid}")
        with open(os.path.join(HERE, "json", name), "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        print(name, len(specs), "paragraphs quoted")


if __name__ == "__main__":
    main()
