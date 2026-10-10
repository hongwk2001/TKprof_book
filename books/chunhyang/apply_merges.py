"""Apply reviewed card merges (review/merge_decisions.json) to json/ch_NN.json.

Text is joined by fixed rules, so no word is lost and quotes stay balanced:
  - a quote cut in two ('...Muju,"' + '"and the...') becomes one quote;
  - a speaker tag ending '.' or ',' before a quote ('Chunhyang answers.' + '"Yes."')
    becomes 'Chunhyang answers, "Yes."' in English (Korean keeps its period);
  - consecutive quotes become one quote (one speaker going on), except in groups
    listed under 'exchanges' (two speakers, or a book read aloud then a remark);
  - anything else is joined with a single space.
A group that spans passages is moved into its first passage. Sentence numbers
are renumbered inside each changed passage; a passage left empty is removed.

    python apply_merges.py --dry-run   # write review/merges_for_approval.md, change nothing
    python apply_merges.py             # apply
"""
import json
import pathlib
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = pathlib.Path(__file__).parent
EN_CAP, KO_CAP = 300, 170
SPEECH_TAG = re.compile(r"\b(says|said|answers(?: him)?|asks|replies|shouts|mutters to himself|speaks(?: up| politely)?|"
                        r"whispers|calls|cries|laughs(?: loudly)?|is surprised|gets angry|sighs|is startled)[.,:]$")


def join(a, b, lang, exchange=False):
    a, b = a.rstrip(), b.lstrip()
    # A quote cut in two: '..."' / '..., ' + '"and ...'  ->  one quote
    if b.startswith('"') and (a.endswith(',"') or (a.count('"') % 2 == 1)):
        a = a[:-1] if a.endswith('"') else a
        return a + " " + b[1:]
    # One speaker going on: '..."' + '"...' -> one quote (not for real back-and-forths)
    if not exchange and b.startswith('"') and re.search(r"""[.!?]'?"$""", a):
        return a[:-1] + " " + b[1:]
    if lang == "en" and b.startswith('"') and '"' not in a and SPEECH_TAG.search(a):
        return a[:-1] + ", " + b
    return a + " " + b


def load(ch):
    return json.loads((HERE / "json" / f"{ch}.json").read_text(encoding="utf-8"))


def main():
    dry = "--dry-run" in sys.argv
    dec = json.loads((HERE / "review" / "merge_decisions.json").read_text(encoding="utf-8"))
    report, problems, total_before, total_after = [], [], 0, 0
    chapters = sorted({k.split("/")[0] for k in dec["edits"]} | set(dec["groups"]))
    for ch in chapters:
        rows = load(ch)
        passages = {r["tag"]: r for r in rows if r["type"] == "passage"}
        sent = {f"{t}.{s['n']}": (t, s) for t, p in passages.items() for s in p["sentences"]}
        total_before += len(sent)
        section = [f"## {ch}", ""]
        for key, e in dec["edits"].items():
            c, cid = key.split("/")
            if c != ch:
                continue
            _, s = sent[cid]
            section += [f"**{cid}** (edit) — {e['why']}", f"- before: {s['en']}", f"- after:  {e['en']}",
                        f"- 전: {s['ko']}", f"- 후: {e['ko']}", ""]
            s["en"], s["ko"] = e["en"], e["ko"]
        for ids in dec["groups"].get(ch, []):
            missing = [i for i in ids if i not in sent]
            if missing:
                problems.append(f"{ch} {ids}: unknown {missing}")
                continue
            parts = [sent[i][1] for i in ids]
            en, ko = parts[0]["en"], parts[0]["ko"]
            ex = "+".join(ids) in dec.get("exchanges", {}).get(ch, [])
            for p in parts[1:]:
                en, ko = join(en, p["en"], "en", ex), join(ko, p["ko"], "ko", ex)
            if len(en) > EN_CAP or len(ko) > KO_CAP:
                problems.append(f"{ch} {'+'.join(ids)}: en {len(en)} / ko {len(ko)} over cap, skipped")
                continue
            if en.count('"') % 2 or ko.count('"') % 2:
                problems.append(f"{ch} {'+'.join(ids)}: unbalanced quotes, check")
            section += [f"**{' + '.join(ids)}**"] + [f"- {p['en']}" for p in parts] + [f"- → {en}", f"- 한: {ko}", ""]
            first_tag, first = sent[ids[0]]
            first["en"], first["ko"] = en, ko
            for i in ids[1:]:
                tag, s = sent[i]
                passages[tag]["sentences"] = [x for x in passages[tag]["sentences"] if x is not s]
        rows = [r for r in rows if r["type"] != "passage" or r["sentences"]]
        for r in rows:
            for n, s in enumerate(r["sentences"], 1):
                s["n"] = n
        total_after += sum(len(r["sentences"]) for r in rows if r["type"] == "passage")
        report += section
        if not dry:
            (HERE / "json" / f"{ch}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    head = [f"# Card merges for approval", "",
            f"{sum(len(v) for v in dec['groups'].values())} merges and {len(dec['edits'])} edits in "
            f"{len(chapters)} chapters. Cards in these chapters: {total_before} → {total_after}.", "",
            "Each block shows the cards before, then the merged English (→) and Korean (한).", ""]
    if problems:
        head += ["## Problems", ""] + [f"- {p}" for p in problems] + [""]
    if dry:
        (HERE / "review" / "merges_for_approval.md").write_text("\n".join(head + report), encoding="utf-8")
    print(f"{'dry run: ' if dry else ''}{total_before} -> {total_after} cards; {len(problems)} problem(s)")
    for p in problems:
        print("  ", p)


if __name__ == "__main__":
    main()
