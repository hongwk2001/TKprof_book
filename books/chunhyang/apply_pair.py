"""Load hand-written Korean + English pairs into json/ch_NN.json in one step.

Staging file: '## P0002' starts a passage; each following line is
'<korean><TAB><english>', one sentence item per line. Used for chapters where
both texts are written in-session (no gemma draft), so the pairing can't drift.

    python apply_pair.py ch_11 path/to/ch_11.txt
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
KO_MAX, EN_MAX = 120, 300


def main(chapter, staging):
    path = HERE / "json" / f"{chapter}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    by_tag = {r["tag"]: r for r in rows}
    items, tag, bad = {}, None, []
    for line in pathlib.Path(staging).read_text(encoding="utf-8").splitlines():
        m = re.match(r"## (P\d{4})", line)
        if m:
            tag = m.group(1)
            items[tag] = []
        elif line.strip():
            ko, sep, en = line.partition("\t")
            if not sep or len(ko) > KO_MAX or len(en) > EN_MAX or not en.strip():
                bad.append(f"{tag}: {line[:40]}")
            items[tag].append((ko.strip(), en.strip()))
    unknown = [t for t in items if t not in by_tag or by_tag[t]["type"] != "passage"]
    if bad or unknown:
        raise SystemExit(f"bad lines {bad}; unknown tags {unknown}")
    for t, pairs in items.items():
        by_tag[t]["sentences"] = [{"n": i, "ko": k, "en": e} for i, (k, e) in enumerate(pairs, 1)]
        by_tag[t].pop("issues", None)
    missing = [r["tag"] for r in rows if r["type"] == "passage" and not r["sentences"]]
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{chapter}: {sum(map(len, items.values()))} pairs; still empty: {missing or 'none'}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
