"""
Fetch the public-domain Classical Chinese (한문) original of 삼국유사 (三國遺事, Iryeon, 1281)
from zh.wikisource, which hosts a proofread transcription of the 1512 奎章閣本 woodblock edition.

Only the ORIGINAL is taken here. The original is public domain (author d. 1289); Wikisource's
own *translations* are CC BY-SA and are deliberately NOT used -- share-alike would contaminate
a paid app. Korean and English are produced in-house from this original.

Writes:
    raw/vol_N.html   verbatim rendered HTML (audit trail / re-parse without refetching)
    raw/vol_N.txt    cleaned plain text, one blank line between paragraphs
    raw/sections.json section headings per volume, where the wiki provides them
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "raw")
API = "https://zh.wikisource.org/w/api.php"
UA = {"User-Agent": "TKProf-booktool/1.0 (tkprof.h@gmail.com) one-off source acquisition"}
VOLUMES = ["一", "二", "三", "四", "五"]


def fetch_parse(title, tries=6):
    url = API + "?" + urllib.parse.urlencode(
        {
            "action": "parse",
            "page": title,
            "prop": "text|sections",
            "format": "json",
            "formatversion": "2",
        }
    )
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.load(resp)["parse"]
        except Exception as exc:  # noqa: BLE001 - retry on 429 / transient network
            wait = 8 * (attempt + 1)
            print(f"  retry {attempt + 1}/{tries} after {wait}s: {exc}")
            time.sleep(wait)
    raise SystemExit(f"gave up fetching {title}")


def clean(html):
    """Rendered wiki HTML -> plain 한문 text, preserving 세주 in its 〈 〉 brackets."""
    text = re.sub(r"(?is)<(script|style|table).*?</\1>", " ", html)
    # Proofread-Page scaffolding and wiki chrome that is not part of the text
    text = re.sub(r"(?is)<span[^>]*class=\"mw-editsection\".*?</span>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", "\n", text)
    text = text.replace("&#8203;", "\n").replace("​", "\n")
    text = re.sub(r"&[a-z]+;", " ", text)

    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line in ("编辑", "編輯", "[", "]"):
            continue
        if line.startswith("Page:") or line.startswith("Index:"):
            continue
        lines.append(line)

    # Re-join the 〈 세주 〉 brackets that the tag-stripper split onto their own lines
    out, buf = [], ""
    for line in lines:
        if line in ("〈", "（"):
            buf = line
            continue
        if buf:
            out.append(buf + line if line not in ("〉", "）") else buf + line)
            buf = ""
            continue
        out.append(line)
    return "\n\n".join(out)


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    sections = {}
    for vol_idx, vol in enumerate(VOLUMES, start=1):
        title = f"三國遺事/卷第{vol}"
        print(f"fetching {title} ...")
        parsed = fetch_parse(title)
        html = parsed["text"]
        body = clean(html)

        with open(os.path.join(RAW_DIR, f"vol_{vol_idx}.html"), "w", encoding="utf-8") as fh:
            fh.write(html)
        with open(os.path.join(RAW_DIR, f"vol_{vol_idx}.txt"), "w", encoding="utf-8") as fh:
            fh.write(body)

        sections[f"vol_{vol_idx}"] = [s["line"] for s in parsed.get("sections", [])]
        hanja = len(re.findall(r"[一-鿿]", body))
        print(f"  -> vol_{vol_idx}.txt  {hanja:,} hanja, {len(sections[f'vol_{vol_idx}'])} wiki sections")
        time.sleep(6)  # zh.wikisource rate-limits aggressively

    with open(os.path.join(RAW_DIR, "sections.json"), "w", encoding="utf-8") as fh:
        json.dump(sections, fh, ensure_ascii=False, indent=2)
    print(f"\nwrote {RAW_DIR}")


if __name__ == "__main__":
    main()
