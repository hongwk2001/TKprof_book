"""
make_epub_native.py
Builds the 젊은 베르테르의 슬픔 EPUB 3 editions straight from json/ch_*.json (copied from
Book_apps/werther/src/main/assets/books) with zipfile:
  bi  English-Korean bilingual (English line, Korean beneath)
  en  English only
  ko  Korean only

Row format: H = chapter title, any other is_header row = letter date (or "Preface"),
P####_n = sentence n of paragraph ####, THE_END = closing mark.

  python make_epub_native.py                 # all three
  python make_epub_native.py --edition bi --chapters 1
"""

import argparse
import glob
import json
import os
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from html import escape

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLISHER = "TKPROF LLC"
YEAR = "2026"

EDITIONS = {
    "en": {
        "lang": "en",
        "title": "The Sorrows of Young Werther",
        "subtitle": "A Modern English Edition",
        "author": "Johann Wolfgang von Goethe",
        "file": "werther_en.epub",
        "cover": "cover_en.jpg",
    },
    "ko": {
        "lang": "ko",
        "title": "젊은 베르테르의 슬픔",
        "subtitle": "현대어 새 번역",
        "author": "요한 볼프강 폰 괴테",
        "file": "werther_ko.epub",
        "cover": "cover_ko.jpg",
    },
    "bi": {
        "lang": "en",
        "title": "The Sorrows of Young Werther · 젊은 베르테르의 슬픔",
        "subtitle": "English–Korean Bilingual Edition · 영한 대역판",
        "author": "Johann Wolfgang von Goethe",
        "file": "werther_bilingual.epub",
        "cover": "cover_bilingual.jpg",
    },
}

INTRO = {
    "en": [
        ("h1", "About This Book"),
        ("p", "<i>The Sorrows of Young Werther</i> (1774) made Johann Wolfgang von Goethe famous across Europe "
              "at the age of twenty-four. Told almost entirely through Werther’s letters to his friend Wilhelm, "
              "it follows a young artist who falls in love with Charlotte, a woman already promised to another man."),
        ("p", "Its intensity shocked and moved its first readers. Young men dressed in Werther’s blue coat and yellow "
              "waistcoat, and the novel became a founding work of the Sturm und Drang movement and of Romantic "
              "literature."),
        ("h2", "About This Edition"),
        ("p", "This edition retells the complete novel in clear modern English, sentence by sentence, based on "
              "R. D. Boylan’s nineteenth-century translation, and arranges it in 15 chapters. Werther’s letters "
              "keep their original dates."),
        ("p", "The Korean text is a new in-house translation made from the modern English, line by line. "
              "Goethe’s original and Boylan’s translation are in the public domain."),
    ],
    "ko": [
        ("h1", "이 책에 대하여"),
        ("p", "『젊은 베르테르의 슬픔』(1774)은 스물네 살의 요한 볼프강 폰 괴테를 단숨에 유럽 전역에 알린 소설입니다. "
              "거의 모든 이야기가 베르테르가 친구 빌헬름에게 보낸 편지로 이루어져 있으며, 이미 다른 남자와 약혼한 "
              "샤를로테를 사랑하게 된 젊은 화가의 이야기를 따라갑니다."),
        ("p", "이 소설의 격렬한 감정은 첫 독자들을 놀라게 하고 깊이 흔들었습니다. 젊은이들은 베르테르처럼 푸른 연미복에 "
              "노란 조끼를 입었고, 이 작품은 질풍노도 운동과 낭만주의 문학의 출발점이 되었습니다."),
        ("h2", "이 판에 대하여"),
        ("p", "R. D. 보일런의 19세기 영어 번역을 바탕으로 소설 전체를 문장마다 쉬운 현대 영어로 다시 쓰고, "
              "15개 장으로 나누었습니다. 베르테르의 편지는 원래 날짜를 그대로 두었습니다."),
        ("p", "한국어 본문은 이 현대 영어를 한 줄씩 새로 옮긴 것입니다. 괴테의 원작과 보일런의 번역은 공유 저작물입니다."),
    ],
}

READING_NOTE = [
    ("h2", "How to Read This Book · 이 책을 읽는 법"),
    ("p", "Each sentence appears in English, with the Korean beneath it. "
          "Read one language and check the other, or read straight through in either."),
    ("p.ko", "문장마다 영어를 먼저 싣고 그 아래에 한국어를 실었습니다. 한쪽 언어로 읽다가 다른 쪽으로 확인해도 좋고, "
             "어느 한 언어로만 죽 읽어도 좋습니다."),
]

STYLE = """
body { margin: 0 3%; line-height: 1.6; }
p { margin: 0; text-indent: 1.2em; }
:lang(ko), .ko { word-break: keep-all; line-break: strict; }
h1, h2 { font-weight: bold; text-align: center; line-height: 1.3; }
h1 { font-size: 1.4em; margin: 2em 0 1em; }
h2 { font-size: 1.15em; margin: 1.6em 0 0.8em; }
h2.entry { font-size: 1.05em; margin: 2em 0 1em; page-break-after: avoid; }
p.the-end { text-align: center; text-indent: 0; letter-spacing: 0.2em; margin: 3em 0; }
h2.entry span.ko { display: block; font-size: 0.9em; font-weight: normal; margin-top: 0.2em; }
.chapter { page-break-before: always; }
p.ch-num { text-align: center; text-indent: 0; font-size: 0.85em; letter-spacing: 0.15em; margin-top: 3em; }
h1.ch-title { margin: 0.4em 0 0.2em; }
p.ch-title-ko { text-align: center; text-indent: 0; font-size: 1.05em; margin-bottom: 2.2em; }
p.first { text-indent: 0; }
div.pair { margin: 0 0 0.9em; page-break-inside: avoid; }
div.pair p { text-indent: 0; }
div.pair p.ko { font-size: 0.95em; margin-top: 0.2em; padding-left: 0.7em; border-left: 2px solid #999; }
div.passage-start { margin-top: 1.8em; }
.front p { text-indent: 0; margin: 0 0 0.8em; }
.front p.ko { margin-bottom: 1.2em; }
.titlepage { text-align: center; page-break-before: always; }
.titlepage p { text-indent: 0; text-align: center; }
p.tp-title { font-size: 2em; font-weight: bold; line-height: 1.25; margin: 4em 0 0.5em; }
p.tp-sub { font-size: 1.05em; margin-bottom: 3em; }
p.tp-small { font-size: 0.9em; margin: 0.3em 0; }
p.tp-pub { margin-top: 5em; letter-spacing: 0.1em; }
.copyright p { font-size: 0.85em; text-indent: 0; margin: 0 0 0.8em; }
.copyright { margin-top: 3em; }
nav ol { list-style-type: none; padding-left: 0; }
nav li { margin: 0.35em 0; }
nav a { text-decoration: none; }
img.cover { max-width: 100%; height: auto; }
"""

KO_ATTR = ' lang="ko" xml:lang="ko"'


def load_chapters(json_dir, only=None):
    """Each chapter: title pair plus a list of blocks, ("entry", en, ko), ("end", en, ko) or ("para", [(en, ko), ...])."""
    chapters = []
    for path in sorted(glob.glob(os.path.join(json_dir, "ch_*.json"))):
        num = int(os.path.basename(path)[3:5])
        if only and num not in only:
            continue
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
        header = next(r for r in rows if r["tag"].startswith("H"))
        blocks, current, current_key = [], None, None
        for r in rows:
            tag = r["tag"]
            if tag.startswith("H"):
                continue
            if r.get("is_header") or tag == "THE_END":
                blocks.append(("end" if tag == "THE_END" else "entry", r["en"].strip(), r["ko"].strip()))
                current_key = None
                continue
            key = tag.split("_")[0]
            if key != current_key:
                current = []
                blocks.append(("para", current))
                current_key = key
            current.append((r["en"].strip(), r["ko"].strip()))
        chapters.append({"num": num, "en_title": header["en"].strip(),
                         "ko_title": header["ko"].strip(), "blocks": blocks})
    return chapters


def page(lang, title, body):
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
            f'lang="{lang}" xml:lang="{lang}">\n<head>\n  <meta charset="utf-8"/>\n'
            f'  <title>{escape(title)}</title>\n'
            f'  <link rel="stylesheet" href="../Styles/main.css" type="text/css"/>\n</head>\n'
            f'<body>\n{body}\n</body>\n</html>\n')


def blocks_html(blocks, ko=False):
    out = []
    for kind, html in blocks:
        attr = KO_ATTR if ko or kind.endswith(".ko") else ""
        tag = kind.split(".")[0]
        cls = ' class="ko"' if kind.endswith(".ko") or ko else ""
        out.append(f"<{tag}{cls}{attr}>{html}</{tag}>")
    return "\n".join(out)


def chapter_html(ch, edition):
    n = ch["num"]
    en_t, ko_t = escape(ch["en_title"]), escape(ch["ko_title"])
    parts = ['<section class="chapter" epub:type="chapter">']
    if edition == "ko":
        parts += [f'<p class="ch-num">제{n}장</p>', f'<h1 class="ch-title">{ko_t}</h1>',
                  '<p class="ch-title-ko">&#160;</p>']
    else:
        num = f"CHAPTER {n}" + ("" if edition == "en" else f" · <span{KO_ATTR}>제{n}장</span>")
        parts += [f'<p class="ch-num">{num}</p>', f'<h1 class="ch-title">{en_t}</h1>',
                  f'<p class="ch-title-ko"{KO_ATTR if edition == "bi" else ""}>{ko_t if edition == "bi" else "&#160;"}</p>']

    first = True
    for block in ch["blocks"]:
        if block[0] == "end":
            _, en, ko = block
            text = {"en": escape(en), "ko": escape(ko), "bi": f"{escape(en)} · <span{KO_ATTR}>{escape(ko)}</span>"}[edition]
            parts.append(f'<p class="the-end">{text}</p>')
            continue
        if block[0] == "entry":
            _, en, ko = block
            if edition == "ko":
                parts.append(f'<h2 class="entry">{escape(ko)}</h2>')
            elif edition == "en":
                parts.append(f'<h2 class="entry">{escape(en)}</h2>')
            else:
                parts.append(f'<h2 class="entry">{escape(en)}<span class="ko"{KO_ATTR}>{escape(ko)}</span></h2>')
            first = True
            continue
        sents = block[1]
        if edition in ("en", "ko"):
            idx = 0 if edition == "en" else 1
            text = " ".join(escape(s[idx], quote=False) for s in sents)
            parts.append(f'<p class="first">{text}</p>' if first else f"<p>{text}</p>")
        else:
            for si, (en, ko) in enumerate(sents):
                cls = "pair passage-start" if si == 0 and not first else "pair"
                parts.append(f'<div class="{cls}"><p class="en">{escape(en, quote=False)}</p>'
                             f'<p class="ko"{KO_ATTR}>{escape(ko, quote=False)}</p></div>')
        first = False
    parts.append("</section>")
    return "\n".join(parts)


def title_html(ed, edition):
    lang_attr = KO_ATTR if edition == "ko" else ""
    by = {"en": "Johann Wolfgang von Goethe",
          "ko": "요한 볼프강 폰 괴테 지음",
          "bi": "Johann Wolfgang von Goethe"}[edition]
    lines = ['<section class="titlepage" epub:type="titlepage">',
             f'<p class="tp-title">{escape(ed["title"])}</p>',
             f'<p class="tp-sub"{lang_attr}>{escape(ed["subtitle"])}</p>',
             f'<p class="tp-small"{lang_attr}>{by}</p>']
    if edition == "bi":
        lines.append(f'<p class="tp-small"{KO_ATTR}>요한 볼프강 폰 괴테 지음 · 현대어 새 번역</p>')
    lines += [f'<p class="tp-pub">{PUBLISHER}</p>', "</section>"]
    return "\n".join(lines)


def copyright_html(ed, edition):
    en = [f"<i>{escape(ed['title'] if edition == 'bi' else EDITIONS['en']['title'])}</i>",
          f"Modern English text and Korean translation © {YEAR} {PUBLISHER}. All rights reserved.",
          "Source text: <i>The Sorrows of Young Werther</i> by Johann Wolfgang von Goethe (1774), in the "
          "English translation by R. D. Boylan (Project Gutenberg #2527). Both are in the public domain.",
          f"Published by {PUBLISHER}."]
    ko = [f"『{EDITIONS['ko']['title']}』",
          f"현대 영어 본문 및 한국어 번역 © {YEAR} {PUBLISHER}. 모든 권리 보유.",
          "저본: 괴테 『젊은 베르테르의 슬픔』(1774)의 R. D. 보일런 영어 번역(프로젝트 구텐베르크 #2527). 둘 다 공유 저작물입니다.",
          f"펴낸 곳: {PUBLISHER}"]
    body = ['<section class="copyright" epub:type="copyright-page">']
    if edition in ("en", "bi"):
        body += [f"<p>{line}</p>" for line in en]
    if edition == "bi":
        body.append("<p>&#160;</p>")
    if edition in ("ko", "bi"):
        body += [f'<p class="ko"{KO_ATTR}>{line}</p>' for line in ko]
    body.append("</section>")
    return "\n".join(body)


def intro_html(edition):
    body = ['<section class="front" epub:type="introduction">']
    if edition in ("en", "bi"):
        body.append(blocks_html(INTRO["en"]))
    if edition == "ko":
        body.append(blocks_html(INTRO["ko"], ko=True))
    if edition == "bi":
        body.append(blocks_html([(k if k != "p" else "p.ko", v) for k, v in INTRO["ko"]]))
        body.append(blocks_html(READING_NOTE))
    body.append("</section>")
    return "\n".join(body)


def toc_label(ch, edition):
    if edition == "en":
        return f"{ch['num']}. {ch['en_title']}"
    if edition == "ko":
        return f"{ch['num']}. {ch['ko_title']}"
    return f"{ch['num']}. {ch['en_title']} · {ch['ko_title']}"


def build(edition, chapters, out_dir, suffix=""):
    ed = EDITIONS[edition]
    lang = ed["lang"]
    book_id = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'tkprof.werther.' + edition)}"
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cover_path = os.path.join(BASE_DIR, ed["cover"])
    has_cover = os.path.exists(cover_path)

    labels = {"en": ("Title Page", "Copyright", "About This Book", "Contents"),
              "ko": ("표제지", "판권", "이 책에 대하여", "차례"),
              "bi": ("Title Page", "Copyright · 판권", "About This Book · 이 책에 대하여", "Contents · 차례")}[edition]

    docs = []  # (id, file, title, html, in_toc)
    if has_cover:
        docs.append(("cover", "cover.xhtml", "Cover",
                     '<section epub:type="cover"><img class="cover" src="../Images/cover.jpg" alt="Cover"/></section>', False))
    docs.append(("title", "title.xhtml", labels[0], title_html(ed, edition), False))
    docs.append(("copyright", "copyright.xhtml", labels[1], copyright_html(ed, edition), False))
    docs.append(("intro", "intro.xhtml", labels[2], intro_html(edition), True))
    for ch in chapters:
        docs.append((f"ch_{ch['num']:02d}", f"ch_{ch['num']:02d}.xhtml", toc_label(ch, edition),
                     chapter_html(ch, edition), True))

    toc_items = [(d[1], d[2]) for d in docs if d[4]]
    first_ch = f"ch_{chapters[0]['num']:02d}.xhtml"
    nav_li = "\n".join(f'      <li><a href="{f}">{escape(t)}</a></li>' for f, t in toc_items)
    nav_body = (f'<nav epub:type="toc" id="toc">\n  <h1>{labels[3]}</h1>\n  <ol>\n{nav_li}\n  </ol>\n</nav>\n'
                f'<nav epub:type="landmarks" id="landmarks" hidden="hidden">\n  <ol>\n'
                + ('      <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>\n' if has_cover else "")
                + '      <li><a epub:type="toc" href="nav.xhtml">Contents</a></li>\n'
                f'      <li><a epub:type="bodymatter" href="{first_ch}">Start</a></li>\n  </ol>\n</nav>')

    out_path = os.path.join(out_dir, ed["file"].replace(".epub", f"{suffix}.epub"))
    page_lang = "ko" if edition == "ko" else "en"
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                   '  <rootfiles>\n    <rootfile full-path="OEBPS/content.opf" '
                   'media-type="application/oebps-package+xml"/>\n  </rootfiles>\n</container>\n')
        z.writestr("OEBPS/Styles/main.css", STYLE)
        manifest = ['<item id="css" href="Styles/main.css" media-type="text/css"/>',
                    '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
                    '<item id="nav" href="Text/nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>']
        if has_cover:
            with open(cover_path, "rb") as f:
                z.writestr("OEBPS/Images/cover.jpg", f.read())
            manifest.append('<item id="cover-image" href="Images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>')
        spine = []
        for doc_id, fname, title, body, _ in docs:
            z.writestr(f"OEBPS/Text/{fname}", page(page_lang, title, body))
            manifest.append(f'<item id="{doc_id}" href="Text/{fname}" media-type="application/xhtml+xml"/>')
            spine.append(f'<itemref idref="{doc_id}"/>')
            if doc_id == "copyright":
                spine.append('<itemref idref="nav"/>')
        z.writestr("OEBPS/Text/nav.xhtml", page(page_lang, labels[3], nav_body))

        langs = '<dc:language>en</dc:language>\n    <dc:language>ko</dc:language>' if edition == "bi" \
            else f"<dc:language>{lang}</dc:language>"
        intro = INTRO["ko" if edition == "ko" else "en"]
        description = escape(" ".join(p for k, p in intro[1:3] if k == "p")
                             .replace("<i>", "").replace("</i>", ""))
        opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0" xml:lang="{lang}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">{book_id}</dc:identifier>
    <dc:title>{escape(ed["title"])}</dc:title>
    {langs}
    <dc:creator id="author">{escape(ed["author"])}</dc:creator>
    <meta refines="#author" property="role" scheme="marc:relators">aut</meta>
    <dc:contributor id="translator">{PUBLISHER}</dc:contributor>
    <meta refines="#translator" property="role" scheme="marc:relators">trl</meta>
    <dc:publisher>{PUBLISHER}</dc:publisher>
    <dc:date>{YEAR}</dc:date>
    <dc:rights>Modern English text and Korean translation © {YEAR} {PUBLISHER}. Original text in the public domain.</dc:rights>
    <dc:subject>Fiction / Classics</dc:subject>
    <dc:subject>German literature</dc:subject>
    <dc:description>{description}</dc:description>
    <meta property="dcterms:modified">{modified}</meta>{chr(10) + '    <meta name="cover" content="cover-image"/>' if has_cover else ""}
  </metadata>
  <manifest>
    {chr(10).join("    " + m for m in manifest).lstrip()}
  </manifest>
  <spine toc="ncx">
    {chr(10).join("    " + s for s in spine).lstrip()}
  </spine>
</package>
"""
        z.writestr("OEBPS/content.opf", opf)
        points = "\n".join(
            f'    <navPoint id="np-{i}" playOrder="{i}">\n      <navLabel><text>{escape(t)}</text></navLabel>\n'
            f'      <content src="Text/{f}"/>\n    </navPoint>' for i, (f, t) in enumerate(toc_items, 1))
        z.writestr("OEBPS/toc.ncx", f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="{lang}">
  <head>
    <meta name="dtb:uid" content="{book_id}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>{escape(ed["title"])}</text></docTitle>
  <navMap>
{points}
  </navMap>
</ncx>
""")
    print(f"{edition}: {out_path} ({os.path.getsize(out_path):,} bytes, {len(chapters)} chapters, cover={'yes' if has_cover else 'no'})")
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition", choices=["bi", "en", "ko", "all"], default="all")
    ap.add_argument("--chapters", type=int, nargs="*", help="chapter numbers (default: all)")
    ap.add_argument("--json-dir", default=os.path.join(BASE_DIR, "json"))
    ap.add_argument("--out-dir", default=BASE_DIR)
    ap.add_argument("--suffix", default="")
    args = ap.parse_args()

    chapters = load_chapters(args.json_dir, set(args.chapters) if args.chapters else None)
    for edition in (["bi", "en", "ko"] if args.edition == "all" else [args.edition]):
        build(edition, chapters, args.out_dir, args.suffix)


if __name__ == "__main__":
    main()
