"""
Stage 4b: semantic audit of batches/result_ch_NN.json with the local model.

audit.py checks what a regex can check. It cannot tell you whether English paragraph 3
actually says what Korean paragraph 3 says -- and that is the defect that reached the
user's ears, because a perfectly shifted item passes every structural check.

Judging "do these two paragraphs say the same thing" is a much easier task than
producing them, which is why a 12B model is worth trusting here and was not worth
trusting alone for the translation.

The model is asked for JSON. It is not reliable about that, so the parser is lenient and
anything unparseable is recorded as an error rather than silently dropped -- a skipped
item must never look like a clean one.

Writes:
    audit/problems.json   machine-readable, for the review pass
    audit/problems.md     readable, worst first

Usage:  python llm_audit.py            # all chapters
        python llm_audit.py ch_01
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

PROMPT = """너는 번역 검수자다. 아래는 《삼국유사》의 한문 원문과, 그것을 옮긴 한국어·영어 문단 쌍이다.

같은 번호의 한국어와 영어가 서로 같은 내용을 말하는지 확인하라.

각 번호마다 다음 중 하나로 판정하라:
- OK        : 한국어와 영어가 같은 내용이다
- SHIFTED   : 영어가 다른 번호의 한국어 내용을 담고 있다
- MISSING   : 한국어에 있는 내용이 영어에 빠졌다
- EXTRA     : 영어에 원문에 없는 내용이 덧붙었다

그리고 한문 원문에 있으나 한국어 번역 전체에서 빠진 내용이 있으면 적어라.

반드시 아래 JSON 형식으로만 답하라. 설명을 덧붙이지 마라.
{{"pairs":[{{"n":1,"verdict":"OK","note":""}}],"omitted":[]}}

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

    problems = []
    body = [i for i in batch["items"] if not i["is_header"]]
    for n, item in enumerate(body, 1):
        v = result.get(str(item["id"]))
        if not v:
            continue
        if v.get("manual"):
            continue                      # hand-written; not the model's to judge
        pairs = "\n".join(
            f"[{i}]\nKO: {k}\nEN: {e}\n"
            for i, (k, e) in enumerate(zip(v["ko"], v["en"]), 1))
        raw = generate(PROMPT.format(hanmun=item["hanmun"], pairs=pairs))
        parsed = parse(raw)
        if parsed is None:
            problems.append({"chapter": cid, "tag": v["tag"], "n": None,
                             "verdict": "UNPARSEABLE", "note": raw[:200]})
            print(f"  [{n:>2}/{len(body)}] {v['tag']}  unparseable")
            continue

        flagged = [p for p in parsed.get("pairs", [])
                   if str(p.get("verdict", "OK")).upper() != "OK"]
        for p in flagged:
            problems.append({"chapter": cid, "tag": v["tag"], "n": p.get("n"),
                             "verdict": str(p.get("verdict", "")).upper(),
                             "note": str(p.get("note", ""))[:300],
                             "ko": (v["ko"][p["n"] - 1][:200]
                                    if isinstance(p.get("n"), int) and 0 < p["n"] <= len(v["ko"]) else ""),
                             "en": (v["en"][p["n"] - 1][:200]
                                    if isinstance(p.get("n"), int) and 0 < p["n"] <= len(v["en"]) else "")})
        for o in parsed.get("omitted", []) or []:
            problems.append({"chapter": cid, "tag": v["tag"], "n": None,
                             "verdict": "OMITTED", "note": str(o)[:300], "ko": "", "en": ""})
        mark = f"  {len(flagged)} flagged" if flagged else ""
        print(f"  [{n:>2}/{len(body)}] {v['tag']}{mark}")
    return problems


def main():
    os.makedirs(OUT, exist_ok=True)
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    cids = [f"ch_{n:02d}" for n in range(1, 25)] if arg == "all" else [arg]

    all_problems = []
    for cid in cids:
        print(f"\n=== {cid}  (model={MODEL})")
        all_problems += audit_chapter(cid)

    with open(os.path.join(OUT, "problems.json"), "w", encoding="utf-8") as fh:
        json.dump({"model": MODEL, "count": len(all_problems),
                   "problems": all_problems}, fh, ensure_ascii=False, indent=1)

    order = {"SHIFTED": 0, "MISSING": 1, "OMITTED": 2, "EXTRA": 3, "UNPARSEABLE": 4}
    all_problems.sort(key=lambda p: (order.get(p["verdict"], 9), p["chapter"], p["tag"]))
    with open(os.path.join(OUT, "problems.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# LLM audit — {len(all_problems)} problems ({MODEL})\n\n")
        by_verdict = {}
        for p in all_problems:
            by_verdict.setdefault(p["verdict"], []).append(p)
        for verdict, items in sorted(by_verdict.items(), key=lambda x: order.get(x[0], 9)):
            fh.write(f"\n## {verdict} — {len(items)}\n\n")
            for p in items:
                loc = f"{p['chapter']}/{p['tag']}" + (f" para {p['n']}" if p["n"] else "")
                fh.write(f"### {loc}\n\n")
                if p.get("note"):
                    fh.write(f"{p['note']}\n\n")
                if p.get("ko"):
                    fh.write(f"- KO: {p['ko']}\n- EN: {p['en']}\n\n")

    counts = {k: len(v) for k, v in sorted(by_verdict.items())} if all_problems else {}
    print(f"\n{len(all_problems)} problems -> {OUT}/problems.md")
    print(f"  {counts}")


if __name__ == "__main__":
    main()
