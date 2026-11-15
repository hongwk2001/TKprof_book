"""
Stage 3: batches/batch_ch_NN.json -> batches/result_ch_NN.json, using a local Ollama model.

Two passes per item:
    1. 한문 (+glossary) -> 한국어
    2. 한문 + 한국어 (+glossary) -> English

Pass 2 is given the 한문 as well as the Korean, not the Korean alone. Korean has no
gendered pronoun and drops subjects almost as freely as 한문 does, so translating from
the Korean by itself reintroduces exactly the errors pass 1 just resolved -- in testing,
그 사람 referring to Charlotte came back as "the man" every time.

think=False is required. Left on, these models spend the whole budget deliberating and
return an empty response.

Usage:  python translate_local.py ch_01
        python translate_local.py ch_01 --model qwen3.5:27b
        python translate_local.py all
"""
import argparse
import glob
import json
import os
import re
import sys
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
BATCH = os.path.join(BASE, "batches")
API = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma4:12b"

GLOSSARY = json.load(open(os.path.join(BASE, "glossary.json"), encoding="utf-8"))

# Hand-written items that override generation entirely, so a rerun cannot regress them.
MANUAL = {k: v for k, v in json.load(
    open(os.path.join(BASE, "manual.json"), encoding="utf-8")).items()
    if not k.startswith("_")}


def _check_manual():
    """A manual key that names a tag which does not exist silently overwrites nothing --
    or worse, a tag that shifted, which overwrites real prose. 찬기파랑가 moved from
    P0013 to P0012 between segmenter runs and clobbered a 131-hanja passage before this
    check existed, so verify every key against the batches at import time."""
    known = {}
    for path in sorted(glob.glob(os.path.join(BATCH, "batch_ch_*.json"))):
        b = json.load(open(path, encoding="utf-8"))
        for i in b["items"]:
            if not i["is_header"]:
                known[f"{b['chapter_id']}/{i['tag']}"] = i
    bad = [k for k in MANUAL if k not in known]
    if bad:
        raise SystemExit(f"manual.json targets unknown items: {bad}")
    for k, v in MANUAL.items():
        if len(v["ko"]) != len(v["en"]):
            raise SystemExit(f"manual.json {k}: ko/en paragraph counts differ")


_check_manual()


def relevant_terms(hanmun):
    """Only the glossary entries this item actually contains -- keeps the prompt short."""
    return {k: v for k, v in GLOSSARY["terms"].items() if k in hanmun}


def context_block(item, chapter_id):
    lines = list(GLOSSARY["always"])
    terms = relevant_terms(item["hanmun"])
    if terms:
        lines.append("")
        lines.append("[이 대목에 나오는 말]")
        lines += [f"- {k} = {v}" for k, v in terms.items()]
    hints = GLOSSARY.get("hints", {}).get(f"{chapter_id}/{item['tag']}")
    if hints:
        lines.append("")
        lines.append("[이 대목의 배경 — 반드시 따를 것]")
        lines += [f"- {h}" for h in hints]
    return "\n".join(lines)


PROMPT_KO = """너는 한문(고전 중국어) 전문 번역가다. 아래는 고려 승려 일연이 쓴 《삼국유사》의 한 대목이다.
이것을 현대 한국어로 번역하라.

{context}

원문:
{hanmun}

번역문만 출력하라.
반드시 {units}개 문단으로 나누어라. 문단과 문단 사이는 빈 줄 하나로 구분하라.
한 문단은 100자 안팎으로 하고, 150자를 넘기지 마라. 한 덩어리로 붙여 쓰지 마라.
문단 안에서는 줄을 바꾸지 마라. 대사도 줄을 바꾸지 말고 이어서 써라."""

# Asking again, with the shortfall named. 73 of 271 items ignored the paragraph count on
# the first pass and returned one block -- one came back as a single 1,072-character
# English card, where the shipped books cap at 300.
PROMPT_KO_RESPLIT = """아래 한국어 번역문을 뜻을 바꾸지 말고 {units}개 문단으로 나누어라.
글자는 고치지 말고 문단 경계만 넣어라. 문단 사이는 빈 줄 하나로 구분하라.
나눈 결과만 출력하라.

{ko}"""

PROMPT_KO_VERSE = """아래는 《삼국유사》에 실린 향가다. 향찰로 적혀 있어 한문으로 읽을 수 없다.
아래 '내용' 설명에 근거하여, 이 노래가 무엇을 노래한 것인지 현대 한국어 산문 2~3문장으로 옮겨라.
한 줄씩 대응시키려 하지 마라. 원문 글자를 그대로 옮기지 마라.

노래 이름: {poem_ko}
내용: {gloss_ko}

향찰 원문(참고용):
{hanmun}

'-했다'체로 쓰라. '노래입니다', '표현하고 있습니다' 같은 해설 투를 쓰지 마라.
노래의 내용을 그대로 서술하라. 산문 번역만 출력하라."""

PROMPT_EN = """You are translating 《삼국유사》(Memorabilia of the Three Kingdoms), written by the
Korean monk Iryeon in 1281. You are given the Classical Chinese original and a Korean
translation of it. Produce natural literary English.

Rules:
- The Korean is a reliable guide to meaning; the Chinese is the authority on names and facts.
{en_rules}
- Keep parentheses （…） as parentheses; they are the author's own notes.
- Past tense, plain narrative register. No archaisms, no "thee"/"thou".
- Add nothing that is not in the original. No explanation, no commentary.
- Output {units} paragraph(s), matching the Korean paragraph breaks exactly.

Classical Chinese:
{hanmun}

Korean:
{ko}

Output only the English translation."""

# Last resort when the batch English pass will not match the Korean paragraph count.
# One paragraph at a time cannot miscount, and the full Chinese and Korean are still
# supplied as context so pronouns and subjects do not drift across the boundary.
PROMPT_EN_ONE = """You are translating 《삼국유사》, written by the Korean monk Iryeon in 1281.

Rules:
{en_rules}
- Past tense, plain narrative register. No archaisms.
- Add nothing that is not in the original. No explanation, no commentary.

For context, the Classical Chinese of the whole passage:
{hanmun}

For context, the whole passage in Korean:
{ko_all}

Now translate ONLY this one Korean paragraph into English. Output exactly one paragraph,
nothing else:

{ko_one}"""


def generate(model, prompt, retries=3):
    body = json.dumps({
        "model": model, "prompt": prompt, "stream": False, "think": False,
        "options": {"temperature": 0.2, "num_ctx": 8192},
    }).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(API, data=body,
                                         headers={"Content-Type": "application/json"})
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=1800) as r:
                d = json.load(r)
            text = (d.get("response") or "").strip()
            if text:
                return text, time.time() - t0
            print(f"      empty response (attempt {attempt + 1})")
        except Exception as exc:  # noqa: BLE001
            print(f"      {type(exc).__name__}: {exc} (attempt {attempt + 1})")
            time.sleep(5)
    return "", 0.0


EN_FIX = [(re.compile(k), v) for k, v in GLOSSARY.get("en_fix", {}).items()]


# Legitimate Sh- in English, or in Chinese names that keep a Chinese reading.
SH_OK = {"she", "shi", "shang", "shandong", "shu", "shall", "should", "short", "show",
         "shore", "ship", "shape", "share", "shed", "shot", "shut", "shine", "shield"}
SH_RE = re.compile(r"\bSh([aeiou])(\w*)")


def _desh(m):
    """Revised Romanization has no Sh-. Korean names keep coming back as McCune-Reischauer
    however firmly the prompt says otherwise, so it is corrected here instead."""
    word = m.group(0)
    return word if word.lower() in SH_OK else "S" + m.group(1) + m.group(2)


KO_FIX = [(re.compile(k), v) for k, v in GLOSSARY.get("ko_fix", {}).items()]


def normalize_ko(text):
    """Deterministic Korean corrections, for readings the model gets wrong even with the
    term in its context -- 唐堯 is 'Yao of Tao-Tang', a state name three thousand years
    older than the Tang dynasty, and it comes back as 당나라 요임금 regardless."""
    for pat, repl in KO_FIX:
        text = pat.sub(repl, text)
    return text


def normalize_en(text):
    """Romanization is enforced here, not in the prompt. The model reproduces
    McCune-Reischauer spellings even with an explicit rule against them in context."""
    for pat, repl in EN_FIX:
        text = pat.sub(repl, text)
    return SH_RE.sub(_desh, text)


# A whole paragraph in which the model reports on its own obedience, e.g.
# "(위의 내용은 원문의 구조에 따라 문단을 나누었으며, 요청하신 규칙을 모두 준수하였습니다.)"
# It always arrives as a trailing paragraph, so besides being wrong it also breaks
# ko/en alignment -- ch_19 P0007 was misaligned for exactly this reason.
META_PARA = re.compile(
    r"(요청하신|규칙을 (모두 )?(준수|따라)|위의 내용은|위 번역은|본 번역은|이상입니다|"
    r"도움이 되(었|시)|I have (followed|translated)|as requested|per your (rules|instructions))"
)

# The same thing in a different costume: a whole paragraph, wrapped in parentheses,
# talking about the translation rather than being it -- "(번역문은 원문의 문단 구분이나
# 흐름에 따라 네 부분으로 나눔)". Phrase-matching kept missing new variants, so this
# matches on shape: fully parenthesised, short, and about the act of translating.
META_SHAPE = re.compile(
    r"^[（(].{0,160}(번역|문단|원문|구분|나눔|나누었|translat|paragraph).{0,160}[）)]$", re.S
)


def _is_meta(p):
    return bool(META_PARA.search(p) or META_SHAPE.match(p.strip()))


# Measured on the finished text, one Korean character renders to 2.27 English characters
# -- 한문 expands into English harder than German does, which is why the first pass at
# 140 still left 144 cards over the 300-character cap the shipped books hold to.
# 300 / 2.27 = 132, so cap Korean at 125 for margin and aim splits at 92.
KO_PARA_MAX = 125
KO_PARA_TARGET = 92

# A paragraph shorter than this is a splitter artefact, not a paragraph. ch_17/P0002
# ended up with a Korean "paragraph" consisting of a single quotation mark, because the
# old pattern had an alternative that split BEFORE a closing quote. That one-character
# fragment then pushed every following English paragraph out of step.
KO_PARA_MIN = 20

# Split only on whitespace that follows sentence-ending punctuation, and allow a closing
# quote or bracket to come along with the punctuation it closes.
_SENT_END = re.compile(r'(?<=[.?!。])["”」』\')]?\s+')


def split_long_ko(paras):
    """Break over-long Korean paragraphs at sentence boundaries.

    Done here, BEFORE the English pass, not afterwards: the English is then generated to
    match the final Korean structure, so the two stay genuinely aligned. Splitting both
    sides after the fact would mean guessing where the Korean and English correspond.
    """
    out = []
    for p in paras:
        if len(p) <= KO_PARA_MAX:
            out.append(p)
            continue
        sentences = [s for s in _SENT_END.split(p) if s and s.strip()]
        if len(sentences) < 2:
            out.append(p)          # one unbreakable sentence; leave it rather than cut mid-clause
            continue
        n = max(2, round(len(p) / KO_PARA_TARGET))
        target = len(p) / n
        chunks, cur = [], ""
        for s in sentences:
            if cur and len(cur) + len(s) > target and len(chunks) < n - 1:
                chunks.append(cur.strip())
                cur = s
            else:
                cur = f"{cur} {s}".strip() if cur else s
        if cur.strip():
            chunks.append(cur.strip())
        out.extend(chunks)
    return merge_fragments(out)


def merge_fragments(paras):
    """Fold any sub-KO_PARA_MIN fragment back into a neighbour.

    A fragment is never a real card, and worse, it consumes an English slot -- which is
    how a stray quotation mark shifted every English paragraph after it in ch_17/P0002.
    """
    out = []
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if len(p) < KO_PARA_MIN and out:
            out[-1] = f"{out[-1]} {p}".strip()
        else:
            out.append(p)
    # a leading fragment has no previous neighbour, so it joins the one after it
    while len(out) > 1 and len(out[0]) < KO_PARA_MIN:
        out[0] = f"{out[0]} {out[1]}".strip()
        del out[1]
    return out


def clean(text):
    """Strip the preamble these models like to add despite being told not to."""
    text = re.sub(r"^\s*(번역[문:]*|Translation:|Here is.*?:|다음은.*?:)\s*\n", "", text)
    text = re.sub(r"```[a-z]*\n?", "", text)
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    paras = [p for p in paras if not _is_meta(p)]
    # The model sometimes translates the whole passage, then translates it again --
    # ch_08 P0004 came back as three paragraphs followed by the same three re-worded,
    # which is both a duplicate and a ko/en misalignment. Drop the repeats.
    seen, unique = set(), []
    for p in paras:
        key = re.sub(r"[^가-힣A-Za-z0-9]", "", p)[:60]
        if key and key in seen:
            continue
        seen.add(key)
        unique.append(p)
    return unique


def run_chapter(cid, model, en_only=False):
    path = os.path.join(BATCH, f"batch_{cid}.json")
    batch = json.load(open(path, encoding="utf-8"))
    body = [i for i in batch["items"] if not i["is_header"]]
    mode = " (English only, reusing existing Korean)" if en_only else ""
    print(f"\n=== {cid} {batch['chapter_ko']} — {len(body)} items, model={model}{mode}")

    # Re-splitting the Korean to a smaller card size does not require retranslating it.
    # The Korean has already been audited; only the English has to be regenerated, to
    # match the new paragraph structure.
    prior = {}
    if en_only:
        ppath = os.path.join(BATCH, f"result_{cid}.json")
        if not os.path.exists(ppath):
            raise SystemExit(f"{cid}: --en-only needs an existing result file")
        prior = json.load(open(ppath, encoding="utf-8"))["items"]

    out, t_start = {}, time.time()
    for n, item in enumerate(body, 1):
        manual = MANUAL.get(f"{cid}/{item['tag']}")
        if manual:
            out[str(item["id"])] = {"tag": item["tag"], "ko": manual["ko"], "en": manual["en"],
                                    "aligned": len(manual["ko"]) == len(manual["en"]),
                                    "manual": True}
            print(f"  [{n:>2}/{len(body)}] {item['tag']}  {item['hanja']:>3}h  "
                  f"hand-written, not generated")
            continue

        if en_only:
            got = prior.get(str(item["id"]))
            if not got:
                raise SystemExit(f"{cid}: {item['tag']} missing from existing result")
            ko_paras, t1 = got["ko"], 0.0
            if item.get("verse") != "hyangchal":
                ko_paras = split_long_ko(ko_paras)
        else:
            ko_paras, t1 = None, 0.0

        units = item.get("target_units", 2)
        if not en_only:
            if item.get("verse") == "hyangchal":
                p_ko = PROMPT_KO_VERSE.format(poem_ko=item["poem_ko"], gloss_ko=item["gloss_ko"],
                                              hanmun=item["hanmun"])
            else:
                p_ko = PROMPT_KO.format(context=context_block(item, cid),
                                        hanmun=item["hanmun"], units=units)
            ko_text, t1 = generate(model, p_ko)
            ko_paras = [normalize_ko(p) for p in clean(ko_text)]

        # The paragraph count in the prompt is advisory to this model -- a quarter of
        # items come back as one block regardless. Re-ask, splitting the text it already
        # produced rather than retranslating, so the wording cannot drift.
        if not en_only and item.get("verse") != "hyangchal" and units > 1 and len(ko_paras) < units:
            resplit, t_extra = generate(
                model, PROMPT_KO_RESPLIT.format(units=units, ko="\n\n".join(ko_paras)))
            candidate = [normalize_ko(p) for p in clean(resplit)]
            joined_before = re.sub(r"\s+", "", "".join(ko_paras))
            joined_after = re.sub(r"\s+", "", "".join(candidate))
            # only accept it if it really is the same text, just broken up
            if len(candidate) > len(ko_paras) and joined_after == joined_before:
                ko_paras, t1 = candidate, t1 + t_extra

        # Whatever the model did or did not do about paragraph count, enforce the card
        # ceiling deterministically before English is generated from it.
        if not en_only and item.get("verse") != "hyangchal":
            ko_paras = split_long_ko(ko_paras)

        en_rules = "\n".join(f"- {r}" for r in GLOSSARY.get("en_rules", []))
        t2, rescued = 0.0, ""

        # Werther cannot produce a shifted card because its English is the SOURCE: the
        # Korean is written into a pre-existing slot and apply_translation.py refuses any
        # count mismatch. Here both sides are generated, so there is no anchor -- and the
        # batch English pass exploits that, matching the paragraph COUNT while
        # re-segmenting the meaning freely. ch_01/P0007 came back with every English
        # paragraph from the fourth onward carrying the NEXT Korean paragraph's content.
        #
        # So the Korean is the anchor and English is generated one paragraph at a time
        # into fixed slots. Shift stops being unlikely and becomes impossible.
        if len(ko_paras) > 1:
            rebuilt = []
            for one in ko_paras:
                got, t_extra = generate(model, PROMPT_EN_ONE.format(
                    hanmun=item["hanmun"], ko_all="\n\n".join(ko_paras), ko_one=one,
                    en_rules=en_rules))
                t2 += t_extra
                parts = [normalize_en(p) for p in clean(got)]
                rebuilt.append(" ".join(parts) if parts else "")
            en_paras = rebuilt
            rescued = " (slot-wise)"
        else:
            p_en = PROMPT_EN.format(hanmun=item["hanmun"], ko="\n\n".join(ko_paras),
                                    units=1, en_rules=en_rules)
            en_text, t2 = generate(model, p_en)
            parts = [normalize_en(p) for p in clean(en_text)]
            en_paras = [" ".join(parts)] if parts else []

        out[str(item["id"])] = {
            "tag": item["tag"], "ko": ko_paras, "en": en_paras,
            "aligned": len(ko_paras) == len(en_paras) and len(ko_paras) > 0,
        }
        flag = "" if out[str(item["id"])]["aligned"] else f"  MISALIGNED ko={len(ko_paras)} en={len(en_paras)}"
        print(f"  [{n:>2}/{len(body)}] {item['tag']}  {item['hanja']:>3}h  "
              f"{t1:5.1f}s+{t2:5.1f}s  ko={len(ko_paras)} en={len(en_paras)}{rescued}{flag}")

    elapsed = time.time() - t_start
    aligned = sum(1 for v in out.values() if v["aligned"])
    res = {"chapter_id": cid, "model": model, "seconds": round(elapsed, 1),
           "aligned": aligned, "total": len(out), "items": out}
    with open(os.path.join(BATCH, f"result_{cid}.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    print(f"  -> result_{cid}.json  {aligned}/{len(out)} aligned, {elapsed / 60:.1f} min")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--en-only", action="store_true",
                    help="reuse the existing Korean, re-split it, regenerate only English")
    a = ap.parse_args()
    cids = ([f"ch_{n:02d}" for n in range(1, 25)] if a.chapter == "all" else [a.chapter])
    for cid in cids:
        run_chapter(cid, a.model, en_only=a.en_only)


if __name__ == "__main__":
    main()
