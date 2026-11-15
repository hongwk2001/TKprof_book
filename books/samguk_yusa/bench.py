"""
Benchmark local Ollama models on the actual 한문 -> 한국어 pass.

한문 is not a normal translation pair. A model can be fluent in both modern Chinese and
Korean and still fail here, because Classical Chinese leaves out the subject, the tense,
the number and usually the object, and the reader is expected to supply them from context.
So the test is not "does it produce Korean" -- all of them will -- but whether it supplies
the *right* implied subjects and resists turning a proper noun into a common noun.

The three probes are chosen to fail in different ways, and all three are passages whose
correct reading is independently known, so the output can actually be graded:

  ch_01 P0002  단군 신화      -- famous, high prior; tests basic narrative competence
  ch_02 P0007  낙랑/대방      -- dense in Han-dynasty toponyms; tests proper-noun handling
  ch_20 P0011  서동 설화      -- plain narrative with dialogue; tests register

Usage:  python bench.py                    # all installed models
        python bench.py qwen3.5:9b ...     # named models
"""
import json
import os
import sys
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "bench")
API = "http://localhost:11434/api"

PROBES = [("ch_01", "P0002"), ("ch_02", "P0007"), ("ch_20", "P0011")]

PROMPT = """너는 한문(고전 중국어) 전문 번역가다. 아래는 고려시대 일연이 쓴 《삼국유사》의 한 대목이다.

이것을 현대 한국어로 번역하라. 규칙:
1. 한문은 주어와 목적어를 자주 생략한다. 문맥에서 판단해 자연스러운 한국어 문장으로 복원하라.
2. 인명·지명·관직명은 한글로 옮기고, 처음 나올 때만 괄호 안에 한자를 병기하라. 예: 환웅(桓雄)
3. 괄호 （）안의 글은 지은이의 주석이다. 본문 흐름에 맞게 괄호로 유지하라.
4. 원문에 없는 내용을 지어내지 마라. 모르면 모르는 대로 직역하라.
5. 설명이나 해설을 덧붙이지 마라. 번역문만 출력하라.
6. 읽기 좋게 2~4개 문단으로 나누어라.

원문:
{hanmun}

번역:"""


def load_probes():
    out = []
    for cid, tag in PROBES:
        d = json.load(open(os.path.join(BASE, "batches", f"batch_{cid}.json"), encoding="utf-8"))
        item = next(i for i in d["items"] if i.get("tag") == tag)
        out.append((cid, tag, item))
    return out


def installed():
    with urllib.request.urlopen(f"{API}/tags", timeout=30) as r:
        return [m["name"] for m in json.load(r)["models"]]


def generate(model, prompt):
    # think=False is not a nicety. Left on, qwen3.5 and gemma4 spend the entire token
    # budget deliberating and return an EMPTY response -- 6,600 characters of reasoning
    # for a three-clause sentence, and no translation at all.
    body = json.dumps({
        "model": model, "prompt": prompt, "stream": False, "think": False,
        "options": {"temperature": 0.2, "num_ctx": 8192},
    }).encode()
    req = urllib.request.Request(f"{API}/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        d = json.load(r)
    return (d.get("response") or "").strip(), time.time() - t0, d


def main():
    os.makedirs(OUT, exist_ok=True)
    models = sys.argv[1:] or installed()
    probes = load_probes()
    print(f"models: {', '.join(models)}\nprobes: {len(probes)}\n")

    report = {}
    for model in models:
        report[model] = []
        for cid, tag, item in probes:
            try:
                text, secs, meta = generate(model, PROMPT.format(hanmun=item["hanmun"]))
            except Exception as exc:  # noqa: BLE001
                print(f"  {model:<18} {cid}/{tag}  FAILED: {exc}")
                report[model].append({"probe": f"{cid}/{tag}", "error": str(exc)})
                continue
            n = meta.get("eval_count", 0)
            tps = n / max(1e-9, meta.get("eval_duration", 1) / 1e9)
            print(f"  {model:<18} {cid}/{tag}  {secs:6.1f}s  {tps:5.1f} tok/s  {len(text):4d} chars")
            report[model].append({
                "probe": f"{cid}/{tag}", "hanja": item["hanja"], "seconds": round(secs, 1),
                "tok_per_s": round(tps, 1), "chars": len(text), "output": text,
            })
        print()

    with open(os.path.join(OUT, "results.json"), "w", encoding="utf-8") as fh:
        json.dump({"probes": [{"id": f"{c}/{t}", "hanmun": i["hanmun"]} for c, t, i in probes],
                   "results": report}, fh, ensure_ascii=False, indent=1)

    with open(os.path.join(OUT, "results.md"), "w", encoding="utf-8") as fh:
        for cid, tag, item in probes:
            fh.write(f"# {cid}/{tag}  ({item['hanja']} hanja)\n\n```\n{item['hanmun']}\n```\n\n")
            for model in models:
                r = next((x for x in report[model] if x["probe"] == f"{cid}/{tag}"), None)
                if not r:
                    continue
                fh.write(f"## {model}\n\n")
                fh.write(f"`{r.get('seconds')}s · {r.get('tok_per_s')} tok/s`\n\n"
                         if "output" in r else f"FAILED: {r['error']}\n\n")
                fh.write(r.get("output", "") + "\n\n")
            fh.write("---\n\n")
    print(f"wrote {OUT}/results.md")


if __name__ == "__main__":
    main()
