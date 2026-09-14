"""
TRIAL ONLY -- reads batches/, writes style_trial/, never touches the product.

The shipped Korean reads like a 논문: long sentences with embedded clauses, 한자 glosses
mid-sentence, and classical endings (-바였다, -게 마련이다). That is fine on a page and
bad in the ear -- TTS stumbles over 부명(符命), and a listener has lost the subject by the
time the verb arrives.

This is a Korean-to-Korean rewrite, which a 12B model does far better than it translates:
the meaning is already fixed and correct, so the only job is register.

Three candidate voices are generated side by side so a human can pick one. Nothing here
is wired into translate_local.py; adopting a voice is a separate, deliberate step.

Usage:  python style_trial.py                 # the default sample
        python style_trial.py ch_01/P0002 ch_20/P0011
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
OUT = os.path.join(BASE, "style_trial")
API = "http://localhost:11434/api/generate"
MODEL = os.environ.get("STYLE_MODEL", "gemma4:12b")

# Chosen to stress different registers: the abstract preface the user complained about,
# a plain narrative, a passage thick with titles and offices, and one with dialogue.
SAMPLE = ["ch_01/P0002", "ch_01/P0006", "ch_20/P0011", "ch_17/P0002", "ch_07/P0009"]

COMMON = """규칙:
- 뜻을 바꾸지 마라. 없는 내용을 지어내지 마라.
- 한자 병기를 모두 없애라. '부명(符命)'은 그냥 '부명'으로, 괄호와 한자를 빼라.
- 한 문장을 짧게 끊어라. 한 문장에 한 가지만 말하라.
- 주어를 분명히 하라. 누가 무엇을 했는지 먼저 말하라.
- 어려운 한자어는 쉬운 우리말로 바꿔라. 다만 인명·지명·벼슬 이름은 그대로 두라.
- 결과만 출력하라. 설명을 덧붙이지 마라."""

VOICES = {
    "A_이야기체": f"""아래 글을 옛이야기를 들려주듯이 다시 써라.
할머니가 아이에게 옛날이야기를 해 주는 말투로, 귀로 듣기 좋게 고쳐라.
'-했다', '-였다'로 끝내되 문장을 짧고 리듬 있게 하라.

{COMMON}

원래 글:
{{ko}}

고친 글:""",

    "B_쉬운설명체": f"""아래 글을 요즘 사람이 쓰는 쉬운 우리말로 다시 써라.
교과서 말투나 논문 말투를 버리고, 신문 기사처럼 담백하고 분명하게 고쳐라.
'-했다', '-이다'로 끝내라.

{COMMON}

원래 글:
{{ko}}

고친 글:""",

    "C_들려주는말투": f"""아래 글을 소리 내어 읽어 줄 원고로 다시 써라.
라디오에서 옛이야기를 들려주는 사람의 말투로, 듣는 사람이 한 번에 알아듣게 고쳐라.
'-했습니다'체를 써도 좋다. 문장을 아주 짧게 끊어라.

{COMMON}

원래 글:
{{ko}}

고친 글:""",

    # A blend of what worked: C's habit of unpacking 한자어 into plain Korean
    # ('괴력난신' -> '괴이한 힘이나 귀신 이야기'), but in 했다체 and without addressing
    # the listener, so it stays a text rather than becoming a broadcast script.
    "D_옛이야기_담백": f"""아래 글을 옛이야기를 들려주는 담백한 우리말로 다시 써라.

{COMMON}
- 어려운 한자어는 뜻으로 풀어라. '괴력난신'은 '괴이한 힘이나 귀신 이야기'처럼 풀어 쓰라.
- '-했다', '-였다'로 끝내라. '-합니다'체를 쓰지 마라.
- 듣는 사람에게 말을 걸지 마라. '봅시다', '보세요' 같은 표현을 쓰지 마라.
- 한 문장은 스물다섯 자 안팎으로 하라. 지나치게 토막 내지는 마라.

원래 글:
{{ko}}

고친 글:""",
}


def generate(prompt, retries=3):
    body = json.dumps({
        "model": MODEL, "prompt": prompt, "stream": False, "think": False,
        "options": {"temperature": 0.3, "num_ctx": 8192},
    }).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(API, data=body,
                                         headers={"Content-Type": "application/json"})
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=900) as r:
                d = json.load(r)
            text = (d.get("response") or "").strip()
            if text:
                return text, time.time() - t0
        except Exception as exc:  # noqa: BLE001
            print(f"      {type(exc).__name__}: {exc}")
            time.sleep(5)
    return "", 0.0


def clean(text):
    text = re.sub(r"^\s*(고친 글|결과)\s*:?\s*\n", "", text)
    text = re.sub(r"```[a-z]*\n?|```", "", text)
    return text.strip()


def listenability(s):
    """Crude but honest proxies for how this lands in the ear."""
    sentences = [x for x in re.split(r"(?<=[.!?])\s+", s) if x.strip()]
    return {
        "chars": len(s),
        "sentences": len(sentences),
        "avg_sentence": round(len(s) / max(1, len(sentences))),
        "hanja": len(re.findall(r"[一-鿿]", s)),
        "glosses": len(re.findall(r"[（(][^）)]*[一-鿿][^）)]*[）)]", s)),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    keys = sys.argv[1:] or SAMPLE

    report = {}
    md = ["# 문체 시험 — 원문 대비 세 가지 목소리", "",
          f"모델 `{MODEL}`. **시험용이며 제품에는 반영하지 않았다.**", ""]

    for key in keys:
        cid, tag = key.split("/")
        r = json.load(open(os.path.join(BATCH, f"result_{cid}.json"), encoding="utf-8"))
        v = next((x for x in r["items"].values() if x["tag"] == tag), None)
        if not v:
            print(f"  {key}: not found")
            continue
        original = "\n\n".join(v["ko"])

        md += [f"\n---\n\n## {key}", "", "### 지금 (원래)", "",
               f"`{listenability(original)}`", ""]
        md += [f"> {p}" for p in v["ko"]] + [""]

        report[key] = {"original": v["ko"], "stats": listenability(original), "voices": {}}
        print(f"\n=== {key}")
        for name, tmpl in VOICES.items():
            text, secs = generate(tmpl.format(ko=original))
            text = clean(text)
            paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
            st = listenability(text)
            report[key]["voices"][name] = {"paras": paras, "stats": st,
                                           "seconds": round(secs, 1)}
            print(f"  {name:<16} {secs:5.1f}s  {st['sentences']:>2} sentences, "
                  f"avg {st['avg_sentence']:>3}자, hanja {st['hanja']}")
            md += [f"### {name}", "", f"`{st}`", ""]
            md += [f"> {p}" for p in paras] + [""]

    with open(os.path.join(OUT, "trial.json"), "w", encoding="utf-8") as fh:
        json.dump({"model": MODEL, "results": report}, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "trial.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
    print(f"\nwrote {OUT}\\trial.md   (product untouched)")


if __name__ == "__main__":
    main()
