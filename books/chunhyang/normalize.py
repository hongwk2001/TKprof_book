"""Stage 1: old-orthography transcription -> modern spelling, no LLM.

Reads raw/leaf_NNN.txt (one printed column per line) and returns the book as
one string in modern Hangul spelling. This is spelling only: words, endings and
grammar are left as printed (마리 for 말이, 남원부의 for 남원부에), because
choosing a modern word is Stage 2's job and needs context.

    python normalize.py            # print stats and the marks needing review
    python normalize.py --dump     # also write the text to stdout
"""
import glob
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent

# Old initial clusters -> modern initial (index into the 19 modern choseong).
CHO = {chr(0x1100 + i): i for i in range(19)}
CHO.update({
    "ᄭ": 1,   # ᄭ sk -> ㄲ
    "ᄯ": 4,   # ᄯ st -> ㄸ
    "ᄹ": 4,   # ᄹ sth -> ㄸ (ᄹᆞ아 = 땋아)
    "ᄲ": 8,   # ᄲ sp -> ㅃ
    "ᄡ": 10,  # ᄡ ps -> ㅆ (ᄡᅳ다 = 쓰다)
    "ᄶ": 13,  # ᄶ sc -> ㅉ
})
JUNG = {chr(0x1161 + i): i for i in range(21)}
JUNG.update({"ᆞ": 0, "ᆡ": 1})  # ᆞ -> ㅏ, ᆡ -> ㅐ
JONG = {chr(0x11a8 + i): i + 1 for i in range(27)}

# Y-glide after ㅅ ㅈ ㅊ (and their tense forms) is dropped in modern spelling:
# 셩 -> 성, 쳥 -> 청, 졔 -> 제, 슈 -> 수.
PALATAL = {9, 10, 12, 13, 14}           # ㅅ ㅆ ㅈ ㅉ ㅊ
DEGLIDE = {2: 0, 6: 4, 12: 8, 17: 13, 7: 5, 3: 1}  # ㅑㅕㅛㅠㅖㅒ -> ㅏㅓㅗㅜㅔㅐ

DROP = ["春香傳上終", "完西溪書鋪", "[印]", "열여춘향슈졀가라", "춘향젼하권이라"]


def compose(text):
    """Turn L V [T] old-jamo runs into modern syllables."""
    out, i = [], 0
    while i < len(text):
        c = text[i]
        if c in CHO and i + 1 < len(text) and text[i + 1] in JUNG:
            l, v = CHO[c], JUNG[text[i + 1]]
            t, step = 0, 2
            if i + 2 < len(text) and text[i + 2] in JONG:
                t, step = JONG[text[i + 2]], 3
            out.append(chr(0xAC00 + (l * 21 + v) * 28 + t))
            i += step
        else:
            out.append(c)
            i += 1
    return "".join(out)


def deglide(text):
    def fix(ch):
        o = ord(ch) - 0xAC00
        if not 0 <= o < 11172:
            return ch
        l, v, t = o // 588, (o % 588) // 28, o % 28
        if l in PALATAL and v in DEGLIDE:
            return chr(0xAC00 + (l * 21 + DEGLIDE[v]) * 28 + t)
        return ch
    return "".join(fix(c) for c in text)


def expand_repeats(text, flags):
    """〻 repeats the syllables before it: 계〻승〻 = 계계승승, 흔들〻〻 = 흔들흔들.
    A run of k marks repeats the previous k syllables. Runs of 3+ are often
    looser than that (보고지거〻〻〻), so they are flagged for review."""
    def rep(m):
        k = len(m.group(2))
        base = m.group(1)
        if k >= 3:
            flags.append(f"repeat x{k} after …{base[-6:]}")
        return base + base[-k:]
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r"([가-힣]+)(〻+)", rep, text, count=1)
    return text


def load_raw():
    """Columns joined in reading order, one string per leaf side, keyed '005a'."""
    pages = {}
    for f in sorted(glob.glob(str(HERE / "raw" / "leaf_*.txt"))):
        side = None
        for line in open(f, encoding="utf-8"):
            m = re.match(r"## (\d+)([ab])", line)
            if m:
                side = f"{int(m.group(1)):03d}{m.group(2)}"
                pages[side] = ""
            elif not line.startswith("#") and side:
                pages[side] += line.strip()
    return pages


def normalize(raw, flags):
    t = raw
    for d in DROP:
        t = t.replace(d, "")
    t = re.sub(r"\[\?([^\]]*)\]", r"\1", t)              # keep the best reading
    t = re.sub(r"\[(이|잇)ᄯᆡ\]", "\n\n이때 ", t)          # boxed section mark
    t = t.replace("■", "□")                              # unreadable stays visible
    t = compose(t)
    t = deglide(t)
    t = expand_repeats(t, flags)
    t = t.replace("○", " ○ ").replace("●", " ○ ")        # list / verse separator
    return re.sub(r"[ \t]+", " ", t).strip()


def main():
    flags = []
    pages = load_raw()
    bridge = (HERE / "raw" / "bridge_005b_006a.txt").read_text(encoding="utf-8")
    parts = []
    for side, raw in pages.items():
        parts.append(normalize(raw, flags))
        if side == "005a":
            body = "".join(l for l in bridge.splitlines(True) if not l.startswith("#"))
            parts.append("〔" + body.strip() + "〕")  # editorial bridge, marked
    text = "".join(parts)
    leftovers = sorted({c for c in text if "ᄀ" <= c <= "ᇿ"})
    print(f"pages {len(pages)}, syllables {len(re.findall('[가-힣]', text))}, "
          f"leftover old jamo {leftovers}, flags {len(flags)}", file=sys.stderr)
    for f in flags:
        print("  ", f, file=sys.stderr)
    if "--dump" in sys.argv:
        print(text)
    return text


if __name__ == "__main__":
    main()
