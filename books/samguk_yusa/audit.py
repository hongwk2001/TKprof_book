"""
Stage 4: grade batches/result_ch_NN.json without reading every line by hand.

Every check here was written because the ch_01 pilot actually failed it. The point is
not to prove the translation is good -- only a reader can do that -- but to find the
failures that are *fluent*, which are the ones a skim will miss:

  삼칠일 left unexpanded, then read by the English pass as "thirty-seven days" (it is 21)
  唐高 read as 당나라 고조, moving a Gojoseon date 3,000 years into the Tang dynasty
  主穀主命主病 read as nouns 곡주·명주·병주 instead of "presides over grain, life, sickness"
  Shindan / Sindan, Woongnyeo / Ungnyeo -- the same name romanized two ways

Usage:  python audit.py ch_01
        python audit.py all
"""
import collections
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
BATCH = os.path.join(BASE, "batches")

HANJA = re.compile(r"[一-鿿]")
HANGUL = re.compile(r"[가-힣]")

KO_PARA_MIN = 20
_TERMS = json.load(open(os.path.join(BASE, "glossary.json"), encoding="utf-8"))["terms"]


def _as_name(value):
    """A glossary value is usable for a coverage check only if it names something.

    Many entries are explanations, not names -- 高麗 maps to '문맥에 따라 다르다…' and
    主穀主命… to '곡식·생명·질병…을 주관하게 했다'. Taking the first token of those
    produces nonsense like '문맥에' and reports it missing from every paragraph. A real
    name has no space before its dash or bracket.
    """
    head = re.split(r"\s*[—(]", value)[0].strip().rstrip(".·")
    if " " in head or not re.fullmatch(r"[가-힣]{2,8}", head.split("·")[0]):
        return None
    return head.split("·")[0]


GLOSS_NAMES = {k: n for k, v in _TERMS.items() if (n := _as_name(v))}

# (pattern, severity, message)
KO_CHECKS = [
    # Honorific verb endings are CORRECT inside quoted speech -- a subject addressing a
    # king says 하옵니다, and 78 of the first 92 hits were exactly that. Only narration
    # outside quotation marks is a register error, so this is checked separately below.
    (r"당(나라)?\s*고조|唐\s*高祖", "high", "唐高 를 당 고조로 읽음 — 여기서는 요(堯)임금"),
    (r"삼칠일(?!\s*[（(])", "med", "삼칠일을 풀지 않음 — '스무하루'로 (영문 pass가 37일로 읽는다)"),
    # 溟州 and 荊州 are real place names; only the bare forms signal the 主X misreading
    (r"곡주|병주|명주(?!\s*[（(]\s*溟)|형주(?!\s*[（(]\s*荊)", "high",
     "主穀主命主病主刑 을 명사로 읽음 — '곡식·생명·질병·형벌을 주관'"),
    (r"고구마|감자|칡", "high", "薯蕷 는 마다 — 고구마/감자는 조선 후기 작물"),
    (r"^\s*(다음은|아래는|번역)", "low", "머리말이 남음"),
]
SH_OK = {"she", "shi", "shang", "shandong", "shu", "shall", "should", "short", "show",
         "shore", "ship", "shape", "share", "shed", "shot", "shut", "shine", "shield"}

EN_CHECKS = [
    (r"\bthirty-seven days\b", "high", "삼칠일 = 21 days, not 37"),
    # Silla dealt with the real Tang constantly, so this is only an anachronism in the
    # Gojoseon/Buyeo chapters. Scoped to those in audit() below.
    (r"\bTang (Dynasty|dynasty|Gaozu)\b", "high", "Tang dynasty in a Gojoseon passage"),
    (r"\b(sweet potato|potato|arrowroot)\b", "high", "薯蕷 is yam"),
    (r"\b(?!She\b|Shi\b)Sh[aeiou]\w*\b", "med", "McCune-Reischauer 'Sh-' — RR uses 'S-'"),
    (r"\bthee\b|\bthou\b|\bhath\b", "low", "archaism"),
    (r"^(Here is|The following|Translation)", "low", "preamble left in"),
]


def norm_name(s):
    """Collapse a romanized name to a shape that survives spelling drift."""
    s = s.lower()
    s = s.replace("sh", "s").replace("oo", "u").replace("eo", "o").replace("ae", "e")
    s = re.sub(r"[^a-z]", "", s)
    return re.sub(r"(.)\1+", r"\1", s)


def audit(cid):
    rp = os.path.join(BATCH, f"result_{cid}.json")
    if not os.path.exists(rp):
        return None
    res = json.load(open(rp, encoding="utf-8"))
    batch = json.load(open(os.path.join(BATCH, f"batch_{cid}.json"), encoding="utf-8"))
    src = {str(i["id"]): i for i in batch["items"]}

    findings, names = [], collections.defaultdict(collections.Counter)
    for iid, v in res["items"].items():
        tag, item = v["tag"], src.get(iid, {})
        ko, en = "\n".join(v["ko"]), "\n".join(v["en"])

        # the model occasionally translates a passage twice; catch it even when the
        # duplicate happens not to break alignment
        keys = [re.sub(r"[^가-힣A-Za-z0-9]", "", p)[:60] for p in v["ko"]]
        if len(set(k for k in keys if k)) < len([k for k in keys if k]):
            findings.append(("high", tag, "같은 내용을 두 번 번역함"))

        if not v["aligned"]:
            findings.append(("high", tag, f"문단 수 불일치 ko={len(v['ko'])} en={len(v['en'])}"))
        for pat, sev, msg in KO_CHECKS:
            if not re.search(pat, ko, re.M):
                continue
            # 명주 is almost always 溟州 (modern Gangneung). Only call it the 主X
            # misreading when the source actually contains that construction.
            if "主穀" in msg and not re.search(r"主(穀|命|病|刑)", item.get("hanmun", "")):
                continue
            findings.append((sev, tag, f"KO: {msg}"))
        # --- pairing checks -------------------------------------------------------
        # Counting paragraphs proved worthless: a perfectly SHIFTED item, where every
        # English card carries the next Korean card's content, passes len(ko)==len(en)
        # every time. It was found by listening, not by auditing. These three catch it.
        kl = [len(p) for p in v["ko"]]
        el = [len(p) for p in v["en"]]

        for n, (a, b) in enumerate(zip(kl, el), 1):
            if a < KO_PARA_MIN:
                findings.append(("high", tag, f"KO 문단 {n}이 {a}자 — 조각 문단"))
            if b < 25:
                findings.append(("high", tag, f"EN 문단 {n}이 {b}자 — 조각 문단"))

        if len(kl) > 1 and not v.get("manual"):
            ratios = [b / max(1, a) for a, b in zip(kl, el)]
            spread = max(ratios) / max(0.01, min(ratios))
            if spread > 2.5:
                findings.append(("high", tag,
                                 f"ko/en 길이 비율이 {spread:.1f}배로 흔들림 — 문단이 밀렸을 수 있음 "
                                 f"{[round(r, 2) for r in ratios]}"))
            # the fingerprint of a shift: content displaced forward leaves the last
            # English paragraph starved
            elif ratios[-1] < 1.2:
                findings.append(("high", tag,
                                 f"마지막 EN 문단 비율 {ratios[-1]:.2f} — 뒤로 밀려 내용이 잘린 듯"))

        # Coverage: a glossary term that is in the 한문 should survive into the Korean.
        # This is Werther's check (English 'Werther' => Korean '베르테르'), which this
        # pipeline never had.
        for k, head in GLOSS_NAMES.items():
            if k in item.get("hanmun", "") and head not in ko and head[:-1] not in ko:
                findings.append(("med", tag, f"한문의 {k}({head})가 번역문에 없음"))

        # Register: honorifics are right in dialogue, wrong in narration. Strip quoted
        # spans first, then look at what is left.
        narration = re.sub(r"[\"“「][^\"”」]*[\"”」]", " ", ko)
        if re.search(r"습니다|합니다|입니다", narration):
            findings.append(("high", tag, "존댓말이 지문에 쓰임 — 지문은 '-했다'체"))

        hanmun = item.get("hanmun", "")
        for pat, sev, msg in EN_CHECKS:
            if not re.search(pat, en, re.M):
                continue
            # 唐裴矩傳 / 唐續高僧傳 are genuinely Tang-dynasty sources; 唐高 and 唐堯 are not
            if "Tang" in msg and re.search(r"唐(裴矩|續高僧|書|史)", hanmun):
                continue
            # Silla's dealings with the real Tang fill ch_09 onward; only the early
            # chapters are old enough for a Tang reference to be an anachronism.
            if "Tang" in msg and cid not in ("ch_01", "ch_02", "ch_03"):
                continue
            if "Sh-" in msg and all(w.lower() in SH_OK
                                    for w in re.findall(r"\bSh[aeiou]\w*", en)):
                continue
            findings.append((sev, tag, f"EN: {msg}"))

        # hanja outside （…） means a character leaked into running text
        bare = HANJA.findall(re.sub(r"（[^）]*）|\([^)]*\)", "", ko))
        if bare:
            findings.append(("med", tag, f"KO: 괄호 밖 한자 {''.join(bare[:8])}"))
        if HANGUL.search(en):
            findings.append(("high", tag, "EN: 한글이 섞임"))
        # A note explaining a variant graph -- "(the character rip [立] was also written
        # su [袖])" -- is clearer WITH the character, so only flag hanja in running text.
        en_bare = re.sub(r"[（(\[][^）)\]]*[）)\]]", " ", en)
        if HANJA.search(en_bare):
            findings.append(("high", tag, "EN: 한자가 본문에 섞임"))

        # 향가 are rendered as prose from the gloss, never transliterated. If the output
        # echoes the 향찰 or runs to the length of a line-by-line reading, the model
        # ignored the gloss and tried to read Old Korean as Classical Chinese.
        if item.get("verse") == "hyangchal":
            idu = sum(ko.count(c) for c in "隱肹叱尸賜")
            if idu:
                findings.append(("high", tag, f"향가: 향찰 글자가 번역문에 남음 ({idu}자)"))
            if item.get("poem_ko", "")[:3] not in ko and len(ko) > 260:
                findings.append(("med", tag, "향가: 산문 요약이 아니라 축자역으로 보임"))
            if not ko.strip():
                findings.append(("high", tag, "향가: 번역 없음"))

        # length sanity -- one hanja is roughly 2.7 Korean chars
        exp = 0 if item.get("verse") == "hyangchal" else item.get("hanja", 0) * 2.7
        if exp and not 0.45 * exp < len(ko) < 2.0 * exp:
            findings.append(("med", tag, f"KO 분량 이상: {len(ko)}자 (예상 {exp:.0f})"))

        for m in re.finditer(r"\b[A-Z][a-z]{2,}(?:[- ][A-Z]?[a-z]+)?\b", en):
            w = m.group(0)
            if w.split()[0] in ("The", "He", "She", "They", "In", "At", "And", "But", "This",
                                "That", "When", "Then", "There", "It", "His", "Her", "From"):
                continue
            names[norm_name(w)][w] += 1

    drift = {k: dict(c) for k, c in names.items() if len(c) > 1}
    return {"chapter": cid, "model": res.get("model"), "minutes": round(res["seconds"] / 60, 1),
            "aligned": f"{res['aligned']}/{res['total']}", "findings": findings, "drift": drift}


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    cids = [f"ch_{n:02d}" for n in range(1, 25)] if arg == "all" else [arg]
    order = {"high": 0, "med": 1, "low": 2}
    for cid in cids:
        r = audit(cid)
        if not r:
            continue
        print(f"\n=== {r['chapter']}  model={r['model']}  {r['minutes']} min  aligned {r['aligned']}")
        if not r["findings"]:
            print("  no findings")
        for sev, tag, msg in sorted(r["findings"], key=lambda x: (order[x[0]], x[1])):
            print(f"  [{sev:>4}] {tag}  {msg}")
        if r["drift"]:
            print("  -- romanization drift --")
            for k, forms in r["drift"].items():
                print(f"     {' / '.join(f'{w}({n})' for w, n in forms.items())}")


if __name__ == "__main__":
    main()
