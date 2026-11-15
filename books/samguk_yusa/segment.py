"""
Stage 2: raw/vol_N.txt -> chapters/ch_NN.txt (readable) + batches/batch_ch_NN.json (for translation).

Does four things the raw fetch left undone:

  1. Rejoins the 〈 세주 〉 interlinear notes, which the HTML tag-stripper split across
     blocks ("〈一作勿吉" / "〉").
  2. Applies the 세주 policy: short notes survive inline as parentheses, bibliographic
     ones (師古曰 / 按 / 見上 …) are dropped. This is a reader's edition, not an apparatus.
  3. Cuts the 王曆 king-list tables and MediaWiki footnote debris off the tail of vol 1.
  4. Packs each 조 into translation items of ~135 hanja, split only at 。 boundaries.

Item size is calibrated against the shipped apps: werther averages 101 Korean chars and
197 English chars per paragraph, with a hard 300-char English ceiling. One hanja renders
to roughly 2.7 Korean chars, so a ~135-hanja item yields the 3-4 paragraphs a translator
can hold in view at once without the unit growing large enough to drift out of alignment.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chapters import CHAPTERS, part_label  # noqa: E402
from entries import VOL1, VOL2, VOL1_END_MARKER  # noqa: E402
from poems import HANMUN_VERSE, HANMUN_VERSE_MARKERS, HYANGGA  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
RAW, CH_DIR, BATCH_DIR = (os.path.join(BASE, d) for d in ("raw", "chapters", "batches"))

TARGET_HANJA = 135      # per translation item
MAX_HANJA = 200         # never let an item exceed this
SEJU_MAX = 25           # 세주 longer than this are dropped rather than inlined

# 세주 that are source-criticism rather than story: Yan Shigu's Han-shu glosses,
# cross-references, "see above" pointers, and notes that open by citing another book
# in order to dispute a date or a place name. A reader's edition keeps none of these.
SEJU_DROP = re.compile(
    r"^(師古曰|臣讚曰|李曰|按|見上|詳見|已見|出[^。]{0,8}傳|國史|鄉記云|古本云|"
    r"[一-鿿]{1,4}(書|典|記|傳|志|鑑|覽)(則|云|曰|注云)|未詳孰是)"
)

HANJA = re.compile(r"[一-鿿㐀-䶿\U00020000-\U0002ffff]")


def count(text):
    return len(HANJA.findall(text))


def rejoin_seju(blocks):
    """'〈一作勿吉' + '〉' -> '〈一作勿吉〉', and glue a note onto the text it annotates."""
    out, buf = [], None
    for b in blocks:
        if buf is not None:
            buf += b
            if "〉" in b:
                out.append(buf)
                buf = None
            continue
        if b.startswith("〈") and "〉" not in b:
            buf = b
            continue
        out.append(b)
    if buf is not None:
        out.append(buf + "〉")
    return out


def apply_seju_policy(text):
    """Inline short 세주 as （…）, drop the bibliographic and the overlong.

    The transcription is inconsistent about which bracket marks a 세주 -- most use
    〈…〉 but a good number were already （…） in the source -- so both are judged
    by the same rule.
    """
    def repl(m):
        note = m.group(1).strip("。， ")
        if not note or SEJU_DROP.match(note) or count(note) > SEJU_MAX:
            return ""
        return f"（{note}）"
    text = re.sub(r"〈([^〈〉]*)〉", repl, text)
    return re.sub(r"（([^（）]*)）", repl, text)


def load_volume(vol, table):
    path = os.path.join(RAW, f"vol_{vol}.txt")
    blocks = [b.strip() for b in open(path, encoding="utf-8").read().split("\n\n") if b.strip()]
    blocks = rejoin_seju(blocks)

    end = len(blocks)
    if vol == 1:
        for i, b in enumerate(blocks):
            if b.startswith(VOL1_END_MARKER):
                end = i
                break

    pos, cursor = [], 0
    for key, ko, en in table:
        for i in range(cursor, end):
            if len(blocks[i]) < 45 and blocks[i].startswith(key):
                pos.append((i, key, ko, en))
                cursor = i + 1
                break
        else:
            raise SystemExit(f"entry not found in vol_{vol}: {key}")

    entries = []
    for n, (i, key, ko, en) in enumerate(pos):
        stop = pos[n + 1][0] if n + 1 < len(pos) else end
        body = apply_seju_policy("".join(blocks[i + 1:stop]))
        body = re.sub(r"（\s*）", "", body)
        entries.append({"key": key, "ko": ko, "en": en, "body": body})
    return entries


SENTINEL = "\x00"


def split_sentences(body):
    """Sentences end at 。 -- but never at a 。 inside a （세주）, which would orphan
    the closing bracket onto the next item."""
    masked = re.sub(r"（[^（）]*）", lambda m: m.group(0).replace("。", SENTINEL), body)
    return [s.replace(SENTINEL, "。") for s in re.split(r"(?<=。)", masked) if s.strip()]


def carve_poems(body):
    """Pull each 향가 out as its own unit so a translator never meets 향찰 mid-paragraph.

    Returns [(text, poem_or_None), ...] in document order.
    """
    cuts = []
    for kind, table in (("hyangchal", HYANGGA), ("hanmun", HANMUN_VERSE)):
        for p in table:
            i = body.find(p["start"])
            if i < 0:
                continue
            j = body.find(p["end"], i)
            if j < 0:
                raise SystemExit(f"{p['ko']}: start found but end marker missing")
            cuts.append((i, j + len(p["end"]), {**p, "kind": kind}))
    cuts.sort()

    out, pos = [], 0
    for a, b, p in cuts:
        before = body[pos:a]
        # "…讚耆婆郎歌曰：" belongs to the song it announces, not to the prose before it.
        # Left in the prose it strands a six-character card of its own.
        m = re.search(r"(?:^|(?<=[。）\s]))[^。）\s]{0,8}?(?:歌曰|謠曰|唱之云|詞曰)[：。]?\s*$", before)
        intro = ""
        if m:
            intro = m.group(0).strip()
            before = before[:m.start()]
        if before.strip():
            out.append((before, None))
        out.append((body[a:b], {**p, "intro": intro}))
        pos = b
    if body[pos:].strip():
        out.append((body[pos:], None))
    return out


def pack_prose(body):
    """Split prose into ~TARGET_HANJA items, cutting only at a sentence end."""
    items, cur = [], ""
    for s in split_sentences(body):
        if not cur:
            cur = s
        elif count(cur) + count(s) > MAX_HANJA:
            items.append(cur)
            cur = s
        elif count(cur) + count(s) > TARGET_HANJA and count(cur) >= TARGET_HANJA * 0.5:
            items.append(cur)
            cur = s
        else:
            cur += s
    if cur.strip():
        # a short tail rejoins the previous item, but never past the hard cap
        if items and count(cur) < TARGET_HANJA * 0.25 and count(items[-1]) + count(cur) <= MAX_HANJA:
            items[-1] += cur
        else:
            items.append(cur)
    return items


def pack(body):
    """[(text, poem_or_None), ...] -- prose packed to size, each 향가 left whole."""
    out = []
    for seg, poem in carve_poems(body):
        if poem:
            out.append((seg.strip(), poem))
        else:
            out.extend((chunk, None) for chunk in pack_prose(seg))
    return out


def main():
    for d in (CH_DIR, BATCH_DIR):
        os.makedirs(d, exist_ok=True)

    entries = load_volume(1, VOL1) + load_volume(2, VOL2)

    chapters = []
    for ko, en, idxs, split in CHAPTERS:
        group = [entries[i - 1] for i in idxs]
        if split == 1:
            chapters.append((ko, en, group))
            continue
        # one oversized 조 cut into N chapters at item boundaries
        only = group[0]
        packed = pack(only["body"])
        per = -(-len(packed) // split)
        for p in range(split):
            chunk = packed[p * per:(p + 1) * per]
            if not chunk:
                continue
            lbl = part_label(p, split)
            chapters.append((
                f"{ko} ({lbl})",
                f"{en} ({lbl})",
                [{**only, "ko": f"{only['ko']} ({lbl})", "en": f"{only['en']} ({lbl})",
                  "_packed": chunk}],
            ))

    total_items = total_hanja = 0
    for n, (cko, cen, group) in enumerate(chapters, start=1):
        cid = f"ch_{n:02d}"
        items, pid = [], 0

        def add(**kw):
            nonlocal pid
            pid += 1
            items.append({"id": pid, **kw})

        add(tag="H01", is_header=True, ko=cko, en=cen)
        for e in group:
            # a 조 header is redundant when it just restates the chapter title
            if not (len(group) == 1 and e["ko"].startswith(cko.split(" (")[0])):
                add(tag=f"S{pid:02d}", is_header=True, ko=e["ko"], en=e["en"])
            for chunk, poem in e.get("_packed") or pack(e["body"]):
                text = chunk.strip()
                extra = {}
                if poem and poem["kind"] == "hanmun":
                    extra = {"verse": "hanmun", "poem_ko": poem["ko"], "poem_en": poem["en"],
                             "intro": poem.get("intro", ""),
                             "gloss_ko": poem["gloss_ko"], "gloss_en": poem["gloss_en"]}
                elif poem:
                    # 향찰, not 한문 -- rendered from the surrounding narrative, and never
                    # repacked with prose, so the translator always sees the whole song.
                    extra = {"verse": "hyangchal", "poem_ko": poem["ko"], "poem_en": poem["en"],
                             "intro": poem.get("intro", ""),
                             "gloss_ko": poem["gloss_ko"], "gloss_en": poem["gloss_en"],
                             "target_units": 1}
                elif any(m in text for m in HANMUN_VERSE_MARKERS):
                    extra = {"verse": "hanmun"}
                fields = {"target_units": max(1, round(count(text) * 2.7 / 100)), **extra}
                add(tag=f"P{pid:04d}", is_header=False, hanmun=text, hanja=count(text), **fields)

        body_items = [i for i in items if not i["is_header"]]
        hanja = sum(i["hanja"] for i in body_items)
        total_items += len(body_items)
        total_hanja += hanja

        with open(os.path.join(BATCH_DIR, f"batch_{cid}.json"), "w", encoding="utf-8") as fh:
            json.dump({"batch_id": cid, "chapter_id": cid, "chapter_ko": cko, "chapter_en": cen,
                       "item_count": len(body_items), "hanja": hanja, "items": items},
                      fh, ensure_ascii=False, indent=1)

        with open(os.path.join(CH_DIR, f"{cid}.txt"), "w", encoding="utf-8") as fh:
            fh.write(f"# {cko}\n# {cen}\n\n")
            for i in items:
                fh.write(f"[{i['tag']}] {i['ko']} / {i['en']}\n\n" if i["is_header"]
                         else f"{i['hanmun']}\n\n")

        print(f"{cid}  {cko:<28} {hanja:>5} hanja  {len(body_items):>3} items")

    print(f"\n{len(chapters)} chapters · {total_items} items · {total_hanja:,} hanja")
    print(f"projected ~{round(total_hanja * 2.7 / 100)} paragraph pairs")


if __name__ == "__main__":
    main()
