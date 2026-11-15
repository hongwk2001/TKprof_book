"""
make_epub_native.py
Builds the 춘향전 EPUB 3 editions straight from json/ch_*.json with zipfile:
  bi  English-Korean bilingual (English line, Korean beneath)
  en  English only
  ko  Korean only

  python make_epub_native.py                 # all three
  python make_epub_native.py --edition bi --chapters 1
  python make_epub_native.py --edition bi --layout paragraph
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
SOURCE_IMAGE = "source_page_1a.jpg"  # leaf 1a, cropped from scans/90001.jpg
YEAR = "2026"

EDITIONS = {
    "en": {
        "lang": "en",
        "title": "The Tale of Chunhyang",
        "subtitle": "Korea's Great Love Story, Retold in Simple English",
        "author": "Anonymous",
        "file": "chunhyang_en.epub",
        "cover": "cover_en.jpg",
    },
    "ko": {
        "lang": "ko",
        "title": "춘향전",
        "subtitle": "완판 84장본 「열녀춘향수절가」 현대어 옮김",
        "author": "작자 미상",
        "file": "chunhyang_ko.epub",
        "cover": "cover_ko.jpg",
    },
    "bi": {
        "lang": "en",
        "title": "The Tale of Chunhyang · 춘향전",
        "subtitle": "English–Korean Bilingual Edition · 영한 대역판",
        "author": "Anonymous",
        "file": "chunhyang_bilingual.epub",
        "cover": "cover_bilingual.jpg",
    },
}

CREDIT_EN = ('Source images: "Yeollyeo Chunhyang Sujeolga" (<span lang="ko" xml:lang="ko">신수15187</span>), '
             'National Museum of Korea, used under KOGL Type 1 (<span lang="ko" xml:lang="ko">공공누리 제1유형</span>).')
CREDIT_KO = "원문 이미지: 국립중앙박물관 소장 「열녀춘향수절가」(신수15187), 공공누리 제1유형"

# Front and back matter. Each value is a list of (kind, html) where kind is h1/h2/p.
INTRO = {
    "en": [
        ("h1", "About This Tale"),
        ("p", "<i>Chunhyang-jeon</i>, the Tale of Chunhyang, is Korea's best-loved love story. "
              "It grew out of <i>pansori</i>, the sung storytelling of the Joseon era, and has been "
              "retold for centuries on stage, in print and on screen."),
        ("p", "In the town of Namwon, Chunhyang, the daughter of a retired gisaeng, meets Yi Mongryong, "
              "the young son of the local magistrate, on a spring day by a swing. They marry in secret, "
              "but he must leave for Seoul. When a cruel new magistrate demands that she serve him, "
              "she refuses, whatever it costs her."),
        ("h2", "About This Edition"),
        ("p", "This book follows the Wanpan woodblock edition of 1911, "
              "<span lang=\"ko\" xml:lang=\"ko\">「열녀춘향수절가」</span> "
              "(<i>Yeollyeo Chunhyang Sujeolga</i>), one of the fullest and best-loved versions of the tale. "
              "It has been newly translated, sentence by sentence, into modern Korean and into simple "
              "English (about CEFR level B1). The songs, puns and wordplay are explained inside the story "
              "instead of in notes."),
        ("p", "This is a modern retelling for readers aged 13 and up. The romance and the punishment scene "
              "are kept, and the most explicit lines of the original are softened."),
        ("p", "Two pages of the original (leaves 5b–6a) are missing from the source images. A short bridge "
              "passage, marked with 〔 〕, was written for this edition to keep the story whole."),
    ],
    "ko": [
        ("h1", "이 이야기에 대하여"),
        ("p", "『춘향전』은 한국인이 가장 사랑하는 사랑 이야기입니다. 조선 후기 판소리에서 자라난 이 이야기는 "
              "무대와 책과 화면에서 수백 년 동안 거듭 새로 태어났습니다."),
        ("p", "남원 땅, 퇴기 월매의 딸 춘향은 봄날 그네 아래에서 사또의 아들 이몽룡을 만납니다. 두 사람은 남몰래 "
              "백년가약을 맺지만 도련님은 한양으로 떠나야 하고, 새로 온 변 사또가 수청을 강요하자 춘향은 "
              "어떤 대가를 치르더라도 이를 거절합니다."),
        ("h2", "이 판에 대하여"),
        ("p", "이 책은 1911년 완판 84장본 「열녀춘향수절가」를 바탕으로 합니다. 춘향전의 여러 판본 가운데 "
              "가장 내용이 풍부하고 널리 사랑받는 판본입니다. 원문을 문장 단위로 새로 읽어 현대 한국어로 옮기고, "
              "쉬운 영어(CEFR B1 수준)로 번역했습니다. 노래와 말장난은 주석 대신 본문 안에서 풀어 썼습니다."),
        ("p", "이 책은 13세 이상 독자를 위한 현대어 재화(再話)입니다. 사랑 이야기와 매 맞는 장면은 살리되, "
              "원문에서 지나치게 노골적인 대목은 순화했습니다."),
        ("p", "원문 이미지 가운데 두 면(5장 뒷면–6장 앞면)이 전하지 않습니다. 이야기가 끊기지 않도록 "
              "이 판에서 짧게 이어 쓴 대목은 〔 〕로 표시했습니다."),
    ],
}

READING_NOTE = [
    ("h2", "How to Read This Book · 이 책을 읽는 법"),
    ("p", "Each sentence appears in English, with the Korean beneath it. "
          "Read one language and check the other, or read straight through in either."),
    ("p.ko", "문장마다 영어를 먼저 싣고 그 아래에 한국어를 실었습니다. 한쪽 언어로 읽다가 다른 쪽으로 확인해도 좋고, "
             "어느 한 언어로만 죽 읽어도 좋습니다."),
]

SOURCE = {
    "en": [
        ("h1", "About the Source"),
        ("p", "<i>Yeollyeo Chunhyang Sujeolga</i> "
              "(<span lang=\"ko\" xml:lang=\"ko\">열녀춘향수절가</span>, “The Faithful Wife Chunhyang Keeps Her Vow”) "
              "is the Wanpan woodblock edition of the Tale of Chunhyang in 84 leaves, printed in 1911. "
              "“Wanpan” means a book cut and printed in Jeonju, whose old name was Wansan. "
              "Its long, song-like text stays close to the pansori that the tale grew from."),
        ("p", "This edition was transcribed in-house from the images of the copy held by the National Museum "
              "of Korea (<span lang=\"ko\" xml:lang=\"ko\">신수15187</span>), published under the Korea Open "
              "Government License (KOGL) Type 1, and then translated into modern Korean and English."),
        ("p", CREDIT_EN),
    ],
    "ko": [
        ("h1", "원문에 대하여"),
        ("p", "「열녀춘향수절가」는 1911년에 간행된 완판 84장본 춘향전입니다. ‘완판’은 전주(옛 이름 완산)에서 "
              "판각하여 찍어낸 책을 말합니다. 길고 노래하는 듯한 문체에 판소리의 숨결이 그대로 남아 있습니다."),
        ("p", "이 판은 국립중앙박물관 소장본(신수15187)의 이미지를 직접 판독하여 입력한 뒤, 현대 한국어와 영어로 "
              "옮긴 것입니다. 원문 이미지는 공공누리 제1유형으로 개방되어 있습니다."),
        ("p", CREDIT_KO),
    ],
}

STYLE = """
body {
    margin: 0 3%;
    line-height: 1.6;
}
p {
    margin: 0;
    text-indent: 1.2em;
}
:lang(ko), .ko {
    word-break: keep-all;
    line-break: strict;
}
h1, h2 {
    font-weight: bold;
    text-align: center;
    line-height: 1.3;
}
h1 { font-size: 1.4em; margin: 2em 0 1em; }
h2 { font-size: 1.15em; margin: 1.6em 0 0.8em; }

/* chapter opening */
.chapter { page-break-before: always; }
p.ch-num {
    text-align: center;
    text-indent: 0;
    font-size: 0.85em;
    letter-spacing: 0.15em;
    margin-top: 3em;
}
h1.ch-title { margin: 0.4em 0 0.2em; }
p.ch-title-ko {
    text-align: center;
    text-indent: 0;
    font-size: 1.05em;
    margin-bottom: 2.2em;
}

/* single-language prose */
p.first { text-indent: 0; }
p.passage-gap { margin-top: 0.8em; }

/* bilingual pairs */
div.pair {
    margin: 0 0 0.9em;
    page-break-inside: avoid;
}
div.pair p { text-indent: 0; }
div.pair p.ko {
    font-size: 0.95em;
    margin-top: 0.2em;
    padding-left: 0.7em;
    border-left: 2px solid #999;
}
div.passage-start { margin-top: 1.8em; }
p.para-ko { text-indent: 0; margin: 0.4em 0 1.4em; padding-left: 0.7em; border-left: 2px solid #999; font-size: 0.95em; }
p.para-en { text-indent: 0; }

/* front and back matter */
.front p, .back p { text-indent: 0; margin: 0 0 0.8em; }
.front p.ko, .back p.ko { margin-bottom: 1.2em; }
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
figure.scan { margin: 2em 0 0; text-align: center; page-break-inside: avoid; }
figure.scan img { max-width: 100%; max-height: 85vh; height: auto; }
figure.scan figcaption { font-size: 0.8em; line-height: 1.4; margin-top: 0.6em; text-align: center; }
"""


def load_chapters(json_dir, only=None):
    chapters = []
    for path in sorted(glob.glob(os.path.join(json_dir, "ch_*.json"))):
        num = int(os.path.basename(path)[3:5])
        if only and num not in only:
            continue
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
        header = next(r for r in rows if r["type"] == "header")
        passages = []
        for r in rows:
            if r["type"] != "passage" or not r["sentences"]:
                continue
            sents = [(s["en"].strip(), s["ko"].strip()) for s in r["sentences"]]
            if r.get("editorial"):
                # the in-house bridge for the missing leaves 5b–6a
                sents[0] = ("〔" + sents[0][0], "〔" + sents[0][1])
                sents[-1] = (sents[-1][0] + "〕", sents[-1][1] + "〕")
            passages.append(sents)
        chapters.append({"num": num, "en_title": header["en_title"],
                         "ko_title": header["ko_title"], "passages": passages})
    return chapters


def page(lang, title, body):
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
            f'lang="{lang}" xml:lang="{lang}">\n<head>\n  <meta charset="utf-8"/>\n'
            f'  <title>{escape(title)}</title>\n'
            f'  <link rel="stylesheet" href="../Styles/main.css" type="text/css"/>\n</head>\n'
            f'<body>\n{body}\n</body>\n</html>\n')


KO_ATTR = ' lang="ko" xml:lang="ko"'


def blocks_html(blocks, ko=False):
    out = []
    for kind, html in blocks:
        attr = KO_ATTR if ko or kind.endswith(".ko") else ""
        tag = kind.split(".")[0]
        cls = ' class="ko"' if kind.endswith(".ko") or ko else ""
        out.append(f"<{tag}{cls}{attr}>{html}</{tag}>")
    return "\n".join(out)


def speech_paragraphs(sents):
    """Split a passage where it turns from narration to speech or back,
    so dialogue starts its own paragraph. Back-to-back quotes stay together."""
    groups = []
    for s in sents:
        quoted = s.lstrip("〔").startswith('"')
        if not groups or quoted != groups[-1][-1].rstrip("〕").endswith('"'):
            groups.append([s])
        else:
            groups[-1].append(s)
    return groups


def chapter_html(ch, edition, layout):
    n = ch["num"]
    en_t, ko_t = escape(ch["en_title"]), escape(ch["ko_title"])
    parts = ['<section class="chapter" epub:type="chapter">']
    if edition == "ko":
        parts.append(f'<p class="ch-num">제{n}장</p>')
        parts.append(f'<h1 class="ch-title">{ko_t}</h1>')
        parts.append('<p class="ch-title-ko">&#160;</p>')
    else:
        parts.append(f'<p class="ch-num">CHAPTER {n}{"" if edition == "en" else " · <span" + KO_ATTR + ">제" + str(n) + "장</span>"}</p>')
        parts.append(f'<h1 class="ch-title">{en_t}</h1>')
        parts.append(f'<p class="ch-title-ko"{KO_ATTR if edition == "bi" else ""}>{ko_t if edition == "bi" else "&#160;"}</p>')

    for pi, sents in enumerate(ch["passages"]):
        if edition in ("en", "ko"):
            idx = 0 if edition == "en" else 1
            for gi, group in enumerate(speech_paragraphs([s[idx] for s in sents])):
                text = " ".join(escape(s, quote=False) for s in group)
                cls = "first" if pi == 0 and gi == 0 else ""
                parts.append(f'<p class="{cls}">{text}</p>' if cls else f"<p>{text}</p>")
        elif layout == "paragraph":
            en = " ".join(escape(s[0], quote=False) for s in sents)
            ko = " ".join(escape(s[1], quote=False) for s in sents)
            parts.append(f'<p class="para-en">{en}</p>')
            parts.append(f'<p class="para-ko"{KO_ATTR}>{ko}</p>')
        else:
            for si, (en, ko) in enumerate(sents):
                cls = "pair passage-start" if si == 0 and pi > 0 else "pair"
                parts.append(f'<div class="{cls}"><p class="en">{escape(en, quote=False)}</p>'
                             f'<p class="ko"{KO_ATTR}>{escape(ko, quote=False)}</p></div>')
    parts.append("</section>")
    return "\n".join(parts)


def title_html(ed, edition):
    lang_attr = KO_ATTR if edition == "ko" else ""
    by = {"en": "Translated from the Wanpan woodblock edition of 1911",
          "ko": "1911년 간행 · 국립중앙박물관 소장본",
          "bi": "Translated from the Wanpan woodblock edition of 1911"}[edition]
    lines = [f'<section class="titlepage" epub:type="titlepage">',
             f'<p class="tp-title">{escape(ed["title"])}</p>',
             f'<p class="tp-sub"{lang_attr}>{escape(ed["subtitle"])}</p>',
             f'<p class="tp-small">{by}</p>']
    if edition == "bi":
        lines.append(f'<p class="tp-small"{KO_ATTR}>1911년 완판본 원문을 새로 옮김</p>')
    lines.append(f'<p class="tp-pub">{PUBLISHER}</p>')
    lines.append("</section>")
    return "\n".join(lines)


def copyright_html(ed, edition):
    en = [f"<i>{escape(EDITIONS['en']['title'] if edition != 'bi' else ed['title'])}</i>",
          f"Modern Korean text and English translation © {YEAR} {PUBLISHER}. All rights reserved.",
          "This is a modern retelling for readers aged 13 and up.",
          "Source text: <span lang=\"ko\" xml:lang=\"ko\">「열녀춘향수절가」</span>, Wanpan woodblock edition in 84 leaves, 1911. "
          "The original work is in the public domain.",
          CREDIT_EN,
          f"Published by {PUBLISHER}."]
    ko = [f"『{EDITIONS['ko']['title']}』",
          f"현대어 본문 및 영어 번역 © {YEAR} {PUBLISHER}. 모든 권리 보유.",
          "이 책은 13세 이상 독자를 위한 현대어 재화입니다.",
          "저본: 완판 84장본 「열녀춘향수절가」(1911). 원작은 공유 저작물입니다.",
          CREDIT_KO,
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


def source_figure(edition):
    cap_en = ('The opening page (leaf 1a) of <span lang="ko" xml:lang="ko">「열녀춘향수절가」</span>, '
              'with the title at the right. National Museum of Korea, '
              '<span lang="ko" xml:lang="ko">신수15187</span>, KOGL Type 1.')
    cap_ko = "「열녀춘향수절가」 첫 면(1장 앞면). 오른쪽 첫 줄이 제목이다. 국립중앙박물관 소장, 신수15187, 공공누리 제1유형."
    alt = ("Woodblock-printed page of Korean text in vertical columns, read from right to left"
           if edition != "ko" else "세로쓰기 한글이 오른쪽에서 왼쪽으로 새겨진 목판본 첫 면")
    caps = []
    if edition in ("en", "bi"):
        caps.append(cap_en)
    if edition in ("ko", "bi"):
        caps.append(f'<span lang="ko" xml:lang="ko">{cap_ko}</span>')
    return (f'<figure class="scan"><img src="../Images/{SOURCE_IMAGE}" alt="{alt}"/>'
            f'<figcaption>{"<br/>".join(caps)}</figcaption></figure>')


def source_html(edition):
    body = ['<section class="back" epub:type="appendix">']
    if edition in ("en", "bi"):
        body.append(blocks_html(SOURCE["en"]))
    if edition == "ko":
        body.append(blocks_html(SOURCE["ko"], ko=True))
    if edition == "bi":
        body.append(blocks_html([(k if k != "p" else "p.ko", v) for k, v in SOURCE["ko"]]))
    if os.path.exists(os.path.join(BASE_DIR, SOURCE_IMAGE)):
        body.append(source_figure(edition))
    body.append("</section>")
    return "\n".join(body)


def toc_label(ch, edition):
    if edition == "en":
        return f"{ch['num']}. {ch['en_title']}"
    if edition == "ko":
        return f"{ch['num']}. {ch['ko_title']}"
    return f"{ch['num']}. {ch['en_title']} · {ch['ko_title']}"


def build(edition, chapters, out_dir, layout, suffix=""):
    ed = EDITIONS[edition]
    lang = ed["lang"]
    # stable id per edition so rebuilds stay the same book
    book_id = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'tkprof.chunhyang.' + edition)}"
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cover_path = os.path.join(BASE_DIR, ed["cover"])
    has_cover = os.path.exists(cover_path)

    labels = {"en": ("Title Page", "Copyright", "About This Tale", "Contents", "About the Source"),
              "ko": ("표제지", "판권", "이 이야기에 대하여", "차례", "원문에 대하여"),
              "bi": ("Title Page", "Copyright · 판권", "About This Tale · 이 이야기에 대하여",
                     "Contents · 차례", "About the Source · 원문에 대하여")}[edition]

    docs = []  # (id, file, title, html, in_toc)
    if has_cover:
        docs.append(("cover", "cover.xhtml", "Cover",
                     '<section epub:type="cover"><img class="cover" src="../Images/cover.jpg" alt="Cover"/></section>', False))
    docs.append(("title", "title.xhtml", labels[0], title_html(ed, edition), False))
    docs.append(("copyright", "copyright.xhtml", labels[1], copyright_html(ed, edition), False))
    docs.append(("intro", "intro.xhtml", labels[2], intro_html(edition), True))
    for ch in chapters:
        docs.append((f"ch_{ch['num']:02d}", f"ch_{ch['num']:02d}.xhtml", toc_label(ch, edition),
                     chapter_html(ch, edition, layout), True))
    docs.append(("source", "source.xhtml", labels[4], source_html(edition), True))

    toc_items = [(d[1], d[2]) for d in docs if d[4]]
    first_ch = f"ch_{chapters[0]['num']:02d}.xhtml"

    nav_li = "\n".join(f'      <li><a href="{f}">{escape(t)}</a></li>' for f, t in toc_items)
    nav_body = (f'<nav epub:type="toc" id="toc">\n  <h1>{labels[3]}</h1>\n  <ol>\n{nav_li}\n  </ol>\n</nav>\n'
                f'<nav epub:type="landmarks" id="landmarks" hidden="hidden">\n  <ol>\n'
                + ('      <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>\n' if has_cover else "")
                + '      <li><a epub:type="toc" href="nav.xhtml">Contents</a></li>\n'
                f'      <li><a epub:type="bodymatter" href="{first_ch}">Start</a></li>\n  </ol>\n</nav>')

    out_path = os.path.join(out_dir, ed["file"].replace(".epub", f"{suffix}.epub"))
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                   '  <rootfiles>\n    <rootfile full-path="OEBPS/content.opf" '
                   'media-type="application/oebps-package+xml"/>\n  </rootfiles>\n</container>\n')
        z.writestr("OEBPS/Styles/main.css", STYLE)
        if has_cover:
            with open(cover_path, "rb") as f:
                z.writestr("OEBPS/Images/cover.jpg", f.read())

        manifest = ['<item id="css" href="Styles/main.css" media-type="text/css"/>',
                    '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
                    '<item id="nav" href="Text/nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>']
        if has_cover:
            manifest.append('<item id="cover-image" href="Images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>')
        source_image = os.path.join(BASE_DIR, SOURCE_IMAGE)
        if os.path.exists(source_image):
            with open(source_image, "rb") as f:
                z.writestr(f"OEBPS/Images/{SOURCE_IMAGE}", f.read())
            manifest.append(f'<item id="source-image" href="Images/{SOURCE_IMAGE}" media-type="image/jpeg"/>')
        spine = []
        for doc_id, fname, title, body, _ in docs:
            page_lang = "ko" if edition == "ko" else "en"
            z.writestr(f"OEBPS/Text/{fname}", page(page_lang, title, body))
            manifest.append(f'<item id="{doc_id}" href="Text/{fname}" media-type="application/xhtml+xml"/>')
            spine.append(f'<itemref idref="{doc_id}"/>')
            if doc_id == "copyright":  # visible contents page after the copyright page
                spine.append('<itemref idref="nav"/>')
        z.writestr("OEBPS/Text/nav.xhtml", page("ko" if edition == "ko" else "en", labels[3], nav_body))

        langs = '<dc:language>en</dc:language>\n    <dc:language>ko</dc:language>' if edition == "bi" \
            else f"<dc:language>{lang}</dc:language>"
        description = escape(" ".join(p for k, p in INTRO["ko" if edition == "ko" else "en"][1:3]
                                      if k == "p").replace("<i>", "").replace("</i>", ""))
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
    <dc:rights>Translation © {YEAR} {PUBLISHER}. Source images: National Museum of Korea (신수15187), KOGL Type 1.</dc:rights>
    <dc:subject>Fiction / Classics</dc:subject>
    <dc:subject>Korean literature</dc:subject>
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
    ap.add_argument("--layout", choices=["sentence", "paragraph"], default="sentence",
                    help="bilingual layout: sentence pairs or paragraph pairs")
    ap.add_argument("--chapters", type=int, nargs="*", help="chapter numbers (default: all)")
    ap.add_argument("--json-dir", default=os.path.join(BASE_DIR, "json"))
    ap.add_argument("--out-dir", default=BASE_DIR)
    ap.add_argument("--suffix", default="")
    args = ap.parse_args()

    chapters = load_chapters(args.json_dir, set(args.chapters) if args.chapters else None)
    for edition in (["bi", "en", "ko"] if args.edition == "all" else [args.edition]):
        build(edition, chapters, args.out_dir, args.layout, args.suffix)


if __name__ == "__main__":
    main()
