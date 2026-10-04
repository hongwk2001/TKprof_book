"""Stage 2 + 4 on local Ollama: old Korean -> modern Korean sentences -> simple English.

For each passage in json/ch_NN.json:
    pass KO: src (old words, modern spelling, no spacing) -> list of modern Korean
             sentences, each at most KO_MAX characters (1:N split happens here,
             once, so the English never has to guess where to cut).
    pass EN: src + numbered Korean sentences -> the same number of plain English
             sentences (ESL, B1), one per Korean sentence.

think=False is mandatory: left on, gemma4 spends the whole budget deliberating
and returns an empty response.

Usage:  python modernize.py ch_02            # both passes, skips passages already done
        python modernize.py ch_02 --force    # redo every passage
        python modernize.py ch_02 --en-only  # keep Korean, regenerate English
"""
import argparse
import json
import pathlib
import re
import sys
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = pathlib.Path(__file__).parent
API = "http://localhost:11434/api/generate"
MODEL = "gemma4:12b"
KO_MAX = 120   # the shipped books cap an English card at 300 characters
EN_MAX = 300
GLOSSARY = json.loads((HERE / "glossary.json").read_text(encoding="utf-8"))

PROMPT_KO = """너는 한국 고전소설을 현대 한국어로 옮기는 전문가다.

{context}

[앞 대목의 현대어 — 이어지는 흐름 참고용]
{prev}

[이번 대목 원문]
{src}

할 일:
- 이번 대목 원문을 빠짐없이 자연스러운 현대 한국어로 옮겨라. 요약하지 말고, 내용을 더하지 마라.
- 옛 어휘는 요즘 독자가 아는 말로 바꿔라. 꼭 남겨야 할 한자어는 쉬운 말로 풀어 써라.
- 대사는 큰따옴표로 묶고, 누가 말하는지 분명하게 하라(원문에 없는 사람을 지어내지 마라).
- 판소리 사설의 나열(○로 구분된 항목, 음식·경치 목록)은 항목을 살려서 옮겨라.
- 서술은 '-다'체 현재형으로 써라(원문의 생생한 말투를 살린다).
- 문장 단위로 나누어 JSON으로 출력하라: {{"sentences": ["...", "..."]}}
- 한 항목은 {ko_max}자를 넘기지 마라. 길면 두 문장으로 나눠라."""

PROMPT_EN = """You are turning a classic Korean novel, the Tale of Chunhyang (1800s), into
simple modern English for Korean learners of English (CEFR B1).

{context}

Old Korean original (for meaning):
{src}

Modern Korean, numbered:
{ko}

Rules:
- Write exactly {n} English items, one for each numbered Korean sentence, same order.
- Plain, clear, modern English. Short sentences, common words, active voice.
- Readability comes first. If an old allusion or pun would confuse a learner, give its
  plain meaning or a modern equivalent the reader can follow; never a vague stand-in.
- Keep crude or sexy jokes as jokes, but say them clearly rather than graphically.
- Keep quotes in double quotation marks. Present tense for narration.
- No archaic English (thee, thou, 'tis, hath).
- Each item at most {en_max} characters.

Output JSON: {{"en": ["...", "..."]}}"""


def ollama(prompt, temperature=0.2):
    body = json.dumps({
        "model": MODEL, "prompt": prompt, "stream": False, "think": False,
        "format": "json",
        "options": {"temperature": temperature, "num_ctx": 8192, "num_predict": 4096},
    }).encode()
    req = urllib.request.Request(API, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())["response"]


def context_ko(src):
    lines = list(GLOSSARY["always"])
    terms = [v for k, v in GLOSSARY["terms"].items() if k in src]
    if terms:
        lines += ["", "[이 대목에 나오는 말]"] + [f"- {t}" for t in terms]
    return "\n".join(lines)


def en_fix(text):
    for pat, rep in GLOSSARY["en_fix"]:
        text = re.sub(pat, rep, text)
    return text


def split_editorial(src):
    """The in-house bridge is already modern Korean: split it, don't rewrite it."""
    body = src.strip("〔〕")
    return [s.strip() for s in re.split(r"(?<=[.다,])\s+(?=\S)", body) if s.strip()]


def pass_ko(row, prev):
    if row.get("editorial"):
        return split_editorial(row["src"]), []
    issues = []
    for attempt in range(3):
        out = ollama(PROMPT_KO.format(context=context_ko(row["src"]), prev=prev or "(없음)",
                                      src=row["src"], ko_max=KO_MAX), 0.2 + 0.2 * attempt)
        try:
            sents = [s.strip() for s in json.loads(out)["sentences"] if s.strip()]
        except (ValueError, KeyError, TypeError):
            issues = ["bad json"]
            continue
        issues = []
        long_ = [s for s in sents if len(s) > KO_MAX]
        if long_:
            issues.append(f"{len(long_)} sentence(s) over {KO_MAX}")
        ratio = sum(map(len, sents)) / max(1, len(row["src"]))
        if not 0.8 <= ratio <= 2.2:
            issues.append(f"length ratio {ratio:.2f}")
        if re.search(r"[一-鿿]", "".join(sents)):
            issues.append("hanja in output")
        if not issues:
            return sents, []
    return sents if "bad json" not in issues else [], issues


def pass_en(row, ko):
    n = len(ko)
    numbered = "\n".join(f"{i}. {s}" for i, s in enumerate(ko, 1))
    ctx = "\n".join(GLOSSARY["en_always"])
    issues = []
    for attempt in range(3):
        out = ollama(PROMPT_EN.format(context=ctx, src=row["src"], ko=numbered, n=n,
                                      en_max=EN_MAX), 0.2 + 0.2 * attempt)
        try:
            en = [en_fix(s.strip()) for s in json.loads(out)["en"]]
        except (ValueError, KeyError, TypeError):
            issues = ["bad json"]
            continue
        issues = []
        if len(en) != n:
            issues.append(f"{len(en)} English items for {n} Korean")
            continue
        if any(len(s) > EN_MAX for s in en):
            issues.append(f"English over {EN_MAX}")
        if re.search(r"[가-힣]", "".join(en)):
            issues.append("Korean in English")
        if not issues:
            return en, []
    return (en if len(en) == n else [""] * n), issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--en-only", action="store_true")
    a = ap.parse_args()
    path = HERE / "json" / f"{a.chapter}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    prev, t0 = "", time.time()
    for row in rows:
        if row["type"] != "passage":
            continue
        done = row["sentences"] and all(s["en"] for s in row["sentences"])
        if done and not (a.force or a.en_only):
            prev = " ".join(s["ko"] for s in row["sentences"][-3:])
            continue
        if a.en_only and row["sentences"]:
            ko, ko_issues = [s["ko"] for s in row["sentences"]], []
        else:
            ko, ko_issues = pass_ko(row, prev)
        en, en_issues = pass_en(row, ko) if ko else ([], ["no Korean"])
        row["sentences"] = [{"n": i, "ko": k, "en": e} for i, (k, e) in enumerate(zip(ko, en), 1)]
        row["issues"] = ko_issues + en_issues
        prev = " ".join(ko[-3:])
        path.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{row['tag']} {len(ko):2d} sents  {int(time.time() - t0):4d}s  {row['issues'] or ''}", flush=True)
    ko_c = sum(len(s["ko"]) for r in rows for s in r["sentences"])
    en_c = sum(len(s["en"]) for r in rows for s in r["sentences"])
    en_w = sum(len(s["en"].split()) for r in rows for s in r["sentences"])
    print(f"{a.chapter}: ko {ko_c} chars, en {en_c} chars / {en_w} words "
          f"(~{en_w / 150:.1f} min), en/ko {en_c / max(1, ko_c):.2f}, {int(time.time() - t0)}s")


if __name__ == "__main__":
    main()
