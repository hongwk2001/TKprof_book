"""
Stage 4c: term-accuracy and fluency audit of batches/result_ch_NN.json with the local model.

llm_audit.py (stage 4b) already checks whether English says what Korean says. That leaves
two failure modes untouched, because they can be internally consistent between KO and EN
while still being wrong or just unpleasant to read:

    TERM_ERROR  a name/title/place is misread against the hanmun ITSELF, not against the
                Korean gloss -- e.g. 公子 (a nobleman's son) read as 孔子 (Confucius). If
                the Korean also just wrote the ambiguous "공자" with nothing to disambiguate,
                the English can match the Korean perfectly and still be wrong.
    AWKWARD     content is correct but the prose is stiff, unnatural, or hard to follow.

Both need the hanmun, not just the KO/EN pair, so the finding record carries it -- unlike
llm_audit.py's problems.json, which drops it.

Runs over ALL non-manual tags (not just ones already flagged by llm_audit.py), since
roughness and term errors are orthogonal to content-equivalence and can hide behind a
clean SHIFTED/MISSING/EXTRA verdict.

Writes:
    audit/quality.json   machine-readable, for the review pass
    audit/quality.md     readable, worst first

Usage:  python quality_audit.py            # all chapters
        python quality_audit.py ch_01
"""
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
OUT = os.path.join(BASE, "audit")
API = "http://localhost:11434/api/generate"
MODEL = os.environ.get("AUDIT_MODEL", "gemma4:12b")

sys.path.insert(0, BASE)
from translate_local import relevant_terms  # noqa: E402  (reuse the glossary lookup, not a copy)

PROMPT = """너는 《삼국유사》 번역의 품질 검수자다. 아래는 한문 원문과, 그것을 옮긴 한국어·영어 문단 쌍이다.

내용이 서로 같은지는 이미 다른 단계에서 확인했다. 이번에는 두 가지만 확인하라.

1. 용어 정확성 (TERM_ERROR): 사람 이름·벼슬·지명 등이 한문 원문의 글자와 실제로 맞는지 확인하라.
   한국어와 영어가 서로 일치하더라도, 원문 한자를 잘못 읽었으면 TERM_ERROR다.
   예: 원문이 公子(귀공자, 왕의 아들)인데 孔子(유학자 공자)로 옮겼다면 TERM_ERROR다.
   한국어 자체가 모호해서 생긴 오류(예: 한자 없이 "공자"라고만 쓴 경우)도 TERM_ERROR로 잡아라.
2. 자연스러움 (AWKWARD): 내용은 맞지만 문장이 딱딱하거나 어색하거나 읽기 어려우면 AWKWARD다.

{glossary_hint}

각 번호마다 다음 중 하나로 판정하라:
- OK          : 문제 없음
- TERM_ERROR  : 이름·벼슬·지명 등이 원문 한자와 다르게 옮겨졌다
- AWKWARD     : 내용은 맞으나 문장이 어색하거나 딱딱하다

TERM_ERROR나 AWKWARD라면 고친 영어를 "fix_en"에 써라. 한국어 자체가 모호해서 생긴 오류일 때만
"fix_ko"도 채워라. 그렇지 않으면 "fix_ko"는 빈 문자열로 두라. note에는 무엇이 왜 문제인지
한 문장으로 적어라.

반드시 아래 JSON 형식으로만 답하라. 설명을 덧붙이지 마라.
{{"pairs":[{{"n":1,"verdict":"OK","note":"","fix_ko":"","fix_en":""}}]}}

한문 원문:
{hanmun}

문단 쌍:
{pairs}
"""


def generate(prompt, retries=3):
    body = json.dumps({
        "model": MODEL, "prompt": prompt, "stream": False, "think": False,
        "options": {"temperature": 0.0, "num_ctx": 8192},
    }).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(API, data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=1800) as r:
                d = json.load(r)
            text = (d.get("response") or "").strip()
            if text:
                return text
        except Exception as exc:  # noqa: BLE001
            print(f"      {type(exc).__name__}: {exc} (attempt {attempt + 1})")
            time.sleep(5)
    return ""


def parse(text):
    """Pull the JSON object out of whatever the model wrapped it in."""
    text = re.sub(r"```[a-z]*|```", "", text)
    start = text.find("{")
    if start < 0:
        return None
    depth = 0
    for i, ch in enumerate(text[start:], start):
        depth += (ch == "{") - (ch == "}")
        if depth == 0:
            try:
                return json.loads(text[start:i + 1])
            except json.JSONDecodeError:
                return None
    return None


def audit_chapter(cid):
    bpath = os.path.join(BATCH, f"batch_{cid}.json")
    rpath = os.path.join(BATCH, f"result_{cid}.json")
    if not os.path.exists(rpath):
        return []
    batch = json.load(open(bpath, encoding="utf-8"))
    result = json.load(open(rpath, encoding="utf-8"))["items"]
    src = {str(i["id"]): i for i in batch["items"]}

    findings = []
    body = [i for i in batch["items"] if not i["is_header"]]
    for n, item in enumerate(body, 1):
        v = result.get(str(item["id"]))
        if not v:
            continue
        if v.get("manual"):
            continue                      # hand-written (향가 etc.); not the model's to judge

        terms = relevant_terms(item["hanmun"])
        glossary_hint = ""
        if terms:
            glossary_hint = "[참고 - 이 대목에 나오는 용어]\n" + "\n".join(
                f"- {k} = {val}" for k, val in terms.items())

        pairs = "\n".join(
            f"[{i}]\nKO: {k}\nEN: {e}\n"
            for i, (k, e) in enumerate(zip(v["ko"], v["en"]), 1))
        raw = generate(PROMPT.format(hanmun=item["hanmun"], pairs=pairs,
                                     glossary_hint=glossary_hint))
        parsed = parse(raw)
        if parsed is None:
            findings.append({"chapter": cid, "tag": v["tag"], "n": None, "item_id": item["id"],
                             "hanmun": item["hanmun"], "verdict": "UNPARSEABLE",
                             "note": raw[:200], "ko": "", "en": "", "fix_ko": "", "fix_en": ""})
            print(f"  [{n:>2}/{len(body)}] {v['tag']}  unparseable")
            continue

        flagged = [p for p in parsed.get("pairs", [])
                   if str(p.get("verdict", "OK")).upper() != "OK"]
        for p in flagged:
            idx = p.get("n")
            ok_idx = isinstance(idx, int) and 0 < idx <= len(v["ko"])
            findings.append({
                "chapter": cid, "tag": v["tag"], "n": idx, "item_id": item["id"],
                "hanmun": item["hanmun"],
                "verdict": str(p.get("verdict", "")).upper(),
                "note": str(p.get("note", ""))[:300],
                "ko": v["ko"][idx - 1] if ok_idx else "",
                "en": v["en"][idx - 1] if ok_idx else "",
                "fix_ko": str(p.get("fix_ko", "") or ""),
                "fix_en": str(p.get("fix_en", "") or ""),
            })
        mark = f"  {len(flagged)} flagged" if flagged else ""
        print(f"  [{n:>2}/{len(body)}] {v['tag']}{mark}")
    return findings


def main():
    os.makedirs(OUT, exist_ok=True)
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    cids = [f"ch_{n:02d}" for n in range(1, 25)] if arg == "all" else [arg]

    all_findings = []
    for cid in cids:
        print(f"\n=== {cid}  (model={MODEL})")
        all_findings += audit_chapter(cid)

    with open(os.path.join(OUT, "quality.json"), "w", encoding="utf-8") as fh:
        json.dump({"model": MODEL, "count": len(all_findings),
                   "findings": all_findings}, fh, ensure_ascii=False, indent=1)

    order = {"TERM_ERROR": 0, "AWKWARD": 1, "UNPARSEABLE": 2}
    all_findings.sort(key=lambda p: (order.get(p["verdict"], 9), p["chapter"], p["tag"]))
    with open(os.path.join(OUT, "quality.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# Quality audit (term accuracy + fluency) — {len(all_findings)} findings ({MODEL})\n\n")
        by_verdict = {}
        for p in all_findings:
            by_verdict.setdefault(p["verdict"], []).append(p)
        for verdict, items in sorted(by_verdict.items(), key=lambda x: order.get(x[0], 9)):
            fh.write(f"\n## {verdict} — {len(items)}\n\n")
            for p in items:
                loc = f"{p['chapter']}/{p['tag']}" + (f" para {p['n']}" if p["n"] else "")
                fh.write(f"### {loc}\n\n")
                if p.get("note"):
                    fh.write(f"{p['note']}\n\n")
                if p.get("hanmun"):
                    fh.write(f"- 漢文: {p['hanmun']}\n")
                if p.get("ko"):
                    fh.write(f"- KO: {p['ko']}\n- EN: {p['en']}\n")
                if p.get("fix_en"):
                    fh.write(f"- fix EN: {p['fix_en']}\n")
                if p.get("fix_ko"):
                    fh.write(f"- fix KO: {p['fix_ko']}\n")
                fh.write("\n")

    counts = {k: len(v) for k, v in sorted(by_verdict.items())} if all_findings else {}
    print(f"\n{len(all_findings)} findings -> {OUT}/quality.md")
    print(f"  {counts}")


if __name__ == "__main__":
    main()
