"""Write review/ch_NN.md: numbered side-by-side Korean / English for human review.

Each passage shows the old text it came from (shortened) and a table of its
sentences. Line ids like 'P0003.4' are what apply_en.py / apply_ko.py use, so
a review note can name the exact line.

    python make_review.py            # all chapters that have sentences
    python make_review.py ch_07
"""
import glob
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
FLAGS = json.loads((HERE / "review_flags.json").read_text(encoding="utf-8")) \
    if (HERE / "review_flags.json").exists() else {}


def cell(s):
    return s.replace("|", "\\|").replace("\n", " ")


def write(chapter):
    rows = json.loads((HERE / "json" / f"{chapter}.json").read_text(encoding="utf-8"))
    head = rows[0]
    sents = [s for r in rows for s in r["sentences"]]
    if not sents:
        return None
    words = sum(len(s["en"].split()) for s in sents)
    out = [f"# {chapter} · {head['ko_title']} / {head['en_title']}", "",
           f"Leaves {head['pages'][0]}–{head['pages'][1]} · {len(sents)} sentences · "
           f"{words} English words (~{words / 150:.0f} min)", ""]
    notes = FLAGS.get(chapter, [])
    if notes:
        out += ["## Please check", ""] + [f"- {n}" for n in notes] + [""]
    for r in rows[1:]:
        src = r["src"]
        short = src if len(src) <= 120 else src[:60] + " … " + src[-50:]
        tag = r["tag"] + (" · editorial bridge" if r.get("editorial") else "")
        out += [f"### {tag}", "", f"> {cell(short)}", "",
                "| # | 한국어 | English |", "|---|---|---|"]
        out += [f"| {r['tag']}.{s['n']} | {cell(s['ko'])} | {cell(s['en'])} |"
                for s in r["sentences"]]
        out.append("")
    path = HERE / "review" / f"{chapter}.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text("\n".join(out), encoding="utf-8")
    return words


def main():
    chapters = sys.argv[1:] or [pathlib.Path(p).stem for p in sorted(glob.glob(str(HERE / "json" / "ch_*.json")))]
    total = 0
    for ch in chapters:
        w = write(ch)
        if w:
            total += w
            print(f"{ch}: {w} words")
    print(f"total {total} English words (~{total / 150:.0f} min)")


if __name__ == "__main__":
    main()
