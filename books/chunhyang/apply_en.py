"""Apply reviewed English fixes to json/ch_NN.json (Stage 4 review).

Staging file: '## P0002' starts a passage; each following line is
'<n><TAB><english>' and replaces sentence n's English. The Korean is never
touched here, so a fix can't shift the ko/en pairing.

    python apply_en.py ch_02 path/to/ch_02_en_fix.txt
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
EN_MAX = 300


def main(chapter, staging):
    path = HERE / "json" / f"{chapter}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    by_tag = {r["tag"]: r for r in rows}
    tag, done = None, 0
    for line in pathlib.Path(staging).read_text(encoding="utf-8").splitlines():
        m = re.match(r"## (P\d{4})", line)
        if m:
            tag = m.group(1)
            continue
        if not line.strip():
            continue
        n, en = line.split("\t", 1)
        sents = by_tag[tag]["sentences"]
        s = next((s for s in sents if s["n"] == int(n)), None)
        if s is None or len(en) > EN_MAX:
            raise SystemExit(f"{tag}.{n}: no such sentence, or English over {EN_MAX}")
        s["en"] = en.strip()
        done += 1
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{chapter}: {done} English fixes applied")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
