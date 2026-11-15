"""Load hand-written modern Korean into json/ch_NN.json (Stage 2, written in-session).

Input is a staging text file: '## P0002' starts a passage, and each following
non-empty line is one Korean sentence item. Existing English is cleared for any
passage whose Korean changes, so modernize.py --en-only regenerates it.

    python apply_ko.py ch_02 path/to/ch_02_ko.txt
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
KO_MAX = 120


def main(chapter, staging):
    path = HERE / "json" / f"{chapter}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    by_tag = {r["tag"]: r for r in rows}
    items, tag = {}, None
    for line in pathlib.Path(staging).read_text(encoding="utf-8").splitlines():
        m = re.match(r"## (P\d{4})", line)
        if m:
            tag = m.group(1)
            items[tag] = []
        elif line.strip() and tag:
            items[tag].append(line.strip())
    bad = [t for t in items if t not in by_tag or by_tag[t]["type"] != "passage"]
    long_ = [(t, s) for t, ss in items.items() for s in ss if len(s) > KO_MAX]
    if bad or long_:
        raise SystemExit(f"unknown tags {bad}; over {KO_MAX}: {long_}")
    for t, ss in items.items():
        old = [s["ko"] for s in by_tag[t]["sentences"]]
        if old != ss:
            by_tag[t]["sentences"] = [{"n": i, "ko": s, "en": ""} for i, s in enumerate(ss, 1)]
            by_tag[t].pop("issues", None)
    missing = [r["tag"] for r in rows if r["type"] == "passage" and not r["sentences"]]
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{chapter}: {sum(map(len, items.values()))} sentences in {len(items)} passages; "
          f"still empty: {missing or 'none'}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
