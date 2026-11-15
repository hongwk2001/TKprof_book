"""Stage 1b: split the normalized text into chapters and passages -> json/ch_NN.json.

Each chapter starts at an anchor string in the normalized text (see CHAPTERS).
Inside a chapter the text is cut into passages of roughly PASSAGE_MAX
characters, preferring the printed ○ marks, the boxed 이때 marks, and
old sentence endings (…더라, …이라, …로다). Stage 2 turns each passage into
modern sentences.

    python chapters.py           # write json/, print chapter sizes
    python chapters.py --dry     # print sizes only

json/ch_NN.json is the single source of truth from here on. This script
refuses to overwrite a chapter that already has sentences.
"""
import json
import pathlib
import re
import sys

import normalize as nz

HERE = pathlib.Path(__file__).parent
PASSAGE_MAX = 450

# (anchor in normalized text, Korean title, English title)
CHAPTERS = [
    ("숙종대왕직위초", "남원 땅의 춘향", "A Girl Born in Namwon"),
    ("잇때월매딸춘향", "그네 타는 춘향", "Chunhyang on the Swing"),
    ("춘향이가그제야못이기", "광한루에서 만나다", "The Meeting at Gwanghallu"),
    ("잇때도련임이춘향을", "글이 눈에 들어오지 않는 밤", "A Night Too Long for Study"),
    ("방자야예퇴령노와", "춘향의 집을 찾아가다", "The Visit to Chunhyang's House"),
    ("춘향어모엿자오되말삼은황송", "백년가약", "The Promise for a Lifetime"),
    ("춘향어모상단이불너", "첫날밤과 사랑가", "The First Night and the Love Song"),
    ("정자로노라보자", "사랑 놀이", "Lovers' Games"),
    ("이때 뜻박긔방자나와", "떠나야 하는 도련님", "Orders to Leave"),
    ("허허이것별일낫다", "이별", "The Farewell"),
    ("춘향이할길업서여보도련임내손의", "떠나는 임, 남는 춘향", "The One Who Leaves, the One Who Stays"),
    ("잇때수삭만의신관", "새 사또 변학도", "The New Magistrate"),
    ("춘향을부르란청영", "수청을 거절하다", "Chunhyang Refuses"),
    ("사또대로하야이열", "매를 맞는 춘향", "The Beating"),
    ("옥으로도러갈제", "옥중의 꿈", "Dreams in Prison"),
    ("봉사한나지나가되", "점쟁이의 해몽", "The Fortune-Teller"),
    ("이때 한양성도련임", "암행어사가 되다", "The Secret Royal Inspector"),
    ("아해하나오난대", "거지 차림의 사위", "The Beggar Son-in-Law"),
    ("이때 상단이옥", "옥중 상봉", "Meeting in Prison"),
    ("잇튼날조사끗티", "변 사또의 생일잔치", "The Magistrate's Birthday Feast"),
    ("암행어사출도야", "어사출두", "The Inspector Arrives"),
]

ENDINGS = re.compile(r"(더라|이라|로다|구나|하니라|엇다|하더라|이로다|하노라|소서|시요)")


def book():
    """Normalized text plus, for each character, the leaf side it came from."""
    flags, pages = [], nz.load_raw()
    bridge = (HERE / "raw" / "bridge_005b_006a.txt").read_text(encoding="utf-8")
    text, owner = "", []
    for side, raw in pages.items():
        part = nz.normalize(raw, flags).replace("\n", "")
        if side == "006b":  # 녹음방초's first syllable was on the missing page 6a
            part = "녹" + part
        text += part
        owner += [side] * len(part)
        if side == "005a":
            body = "".join(l for l in bridge.splitlines(True) if not l.startswith("#"))
            part = "〔" + body.strip() + "〕"
            text += part
            owner += ["bridge"] * len(part)
    return text, owner


def passages(chunk):
    """Cut at ○ / 이때 marks first, then at sentence endings once long enough."""
    units = [u.strip() for u in re.split(r"\s*○\s*|(?=이때 )|(?=〔)|(?<=〕)", chunk) if u.strip()]
    out = []
    for u in units:
        while len(u) > PASSAGE_MAX and "〔" not in u:  # never cut the editorial bridge
            cut = None
            for m in ENDINGS.finditer(u, 0, PASSAGE_MAX):
                if m.end() >= PASSAGE_MAX // 2:
                    cut = m.end()
            if cut is None:  # no ending found: fall back to the cap
                cut = PASSAGE_MAX
            out.append(u[:cut])
            u = u[cut:]
        out.append(u)
    # glue list items (○) shorter than 40 chars onto their neighbour
    merged = []
    for p in out:
        if merged and "〔" not in p + merged[-1] and (len(p) < 40 or len(merged[-1]) < 40) and len(merged[-1]) + len(p) <= PASSAGE_MAX:
            merged[-1] += " ○ " + p
        else:
            merged.append(p)
    return merged


def main():
    text, owner = book()
    starts = []
    for anchor, *_ in CHAPTERS:
        i = text.find(anchor)
        if i < 0 or text.find(anchor, i + 1) >= 0:
            raise SystemExit(f"anchor not found or not unique: {anchor}")
        starts.append(i)
    if starts != sorted(starts):
        raise SystemExit("anchors out of order")
    starts.append(len(text))
    (HERE / "json").mkdir(exist_ok=True)
    total = 0
    for n, (anchor, ko, en) in enumerate(CHAPTERS, 1):
        a, b = starts[n - 1], starts[n]
        chunk = text[a:b]
        sides = sorted(set(owner[a:b]) - {"bridge"})
        ps = passages(chunk)
        syl = len(re.findall("[가-힣]", chunk))
        total += syl
        print(f"ch_{n:02d} {syl:5d} syl {len(ps):3d} passages  {sides[0]}-{sides[-1]}  {ko}")
        if "--dry" in sys.argv:
            continue
        path = HERE / "json" / f"ch_{n:02d}.json"
        if path.exists() and any(r.get("sentences") for r in json.loads(path.read_text(encoding="utf-8"))):
            print(f"  {path.name} has sentences; not overwritten")
            continue
        rows = [{"id": 1, "tag": "P0001", "chapter_id": f"ch_{n:02d}", "type": "header",
                 "pages": [sides[0], sides[-1]], "src": "", "ko_title": ko, "en_title": en,
                 "sentences": []}]
        for k, p in enumerate(ps, 2):
            rows.append({"id": k, "tag": f"P{k:04d}", "chapter_id": f"ch_{n:02d}",
                         "type": "passage", "editorial": "〔" in p, "src": p, "sentences": []})
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"total {total} syllables in {len(CHAPTERS)} chapters")


if __name__ == "__main__":
    main()
