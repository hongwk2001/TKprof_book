"""
make_epub_native.py
Builds the The Heroes (그리스 영웅 이야기) EPUB 3 editions straight from json/ch_*.json with
zipfile. json/ is written by apply_quotes.py, which restores the dialogue quotation
marks that the app copy in json_app/ (from Book_apps/the_heroes/src/main/assets/books)
lost:
  bi  English-Korean bilingual (English line, Korean beneath)
  en  English only
  ko  Korean only

Row format: H = chapter title ("Perseus - Part I: How ..."), the one other is_header
row is the preface salutation, a row with "image" is an illustration (its en/ko is the
caption; the picture comes from the app's assets/images), P####_n = sentence n of
paragraph ####, THE_END = closing mark.

  python make_epub_native.py                 # all three
  python make_epub_native.py --edition bi --chapters 1
"""

import argparse
import glob
import io
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

IMAGE_DIR = r"C:\git_repo\Book_apps\the_heroes\src\main\assets"

EDITIONS = {
    "en": {
        "lang": "en",
        "title": "The Heroes",
        "subtitle": "Greek Fairy Tales · A Modern English Edition",
        "author": "Charles Kingsley",
        "file": "the_heroes_en.epub",
        "cover": "cover_en.jpg",
    },
    "ko": {
        "lang": "ko",
        "title": "그리스 영웅 이야기",
        "subtitle": "페르세우스, 아르고 원정대, 테세우스 · 현대어 새 번역",
        "author": "찰스 킹즐리",
        "file": "the_heroes_ko.epub",
        "cover": "cover_ko.jpg",
    },
    "bi": {
        "lang": "en",
        "title": "The Heroes · 그리스 영웅 이야기",
        "subtitle": "English–Korean Bilingual Edition · 영한 대역판",
        "author": "Charles Kingsley",
        "file": "the_heroes_bilingual.epub",
        "cover": "cover_bilingual.jpg",
    },
}

INTRO = {
    "en": [
        ("h1", "About This Book"),
        ("p", "<i>The Heroes</i> (1856) is Charles Kingsley’s retelling of three great Greek myths, written for "
              "his own children: Perseus, who slew the Gorgon and saved Andromeda; Jason and the Argonauts, who "
              "sailed to the end of the world for the Golden Fleece; and Theseus, who cleared the road to Athens "
              "of robbers and faced the Minotaur in the labyrinth."),
        ("p", "Kingsley tells the stories as a father speaking to his children, and for more than a century and a "
              "half they have been many young readers’ first meeting with the Greek heroes."),
        ("h2", "About This Edition"),
        ("p", "This edition retells the complete book, with Kingsley’s preface, in clear modern English, sentence "
              "by sentence, and arranges it in 16 chapters. Eight illustrations from the early editions appear "
              "here in colour."),
        ("p", "The Korean text is a new in-house translation made from the modern English, line by line. "
              "Kingsley’s original is in the public domain."),
    ],
    "ko": [
        ("h1", "이 책에 대하여"),
        ("p", "『영웅들』(1856)은 찰스 킹즐리가 자기 아이들을 위해 다시 들려준 세 편의 그리스 신화입니다. 고르곤을 "
              "물리치고 안드로메다를 구한 페르세우스, 황금 양털을 찾아 세상 끝까지 항해한 이아손과 아르고 원정대, "
              "그리고 아테네로 가는 길의 도적들을 없애고 미궁에서 미노타우로스와 맞선 테세우스의 이야기입니다."),
        ("p", "킹즐리는 아버지가 아이들에게 말하듯 이야기를 들려주며, 이 책은 150년이 넘도록 많은 어린 독자들이 "
              "그리스 영웅들을 처음 만나는 책이 되어 왔습니다."),
        ("h2", "이 판에 대하여"),
        ("p", "킹즐리의 머리말을 포함한 책 전체를 문장마다 쉬운 현대 영어로 다시 쓰고, 16개 장으로 나누었습니다. "
              "초기 판본의 삽화 여덟 점을 색을 입혀 함께 실었습니다."),
        ("p", "한국어 본문은 이 현대 영어를 한 줄씩 새로 옮긴 것입니다. 킹즐리의 원작은 공유 저작물입니다."),
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
p.salutation { text-indent: 0; font-style: italic; margin: 0 0 0.8em; }
p.salutation span.ko { display: block; font-style: normal; }
div.ill { text-align: center; margin: 1.5em 0; page-break-inside: avoid; }
div.ill img { max-width: 100%; max-height: 85vh; height: auto; }
div.ill p { text-indent: 0; text-align: center; font-size: 0.85em; font-style: italic; margin-top: 0.4em; }
div.ill p.ko { font-style: normal; margin-top: 0.1em; }
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
            if r.get("image"):
                blocks.append(("image", r["image"], r["en"].strip(), r["ko"].strip()))
                current_key = None
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


def split_title(title):
    """'Perseus - Part I: How Perseus ...' -> ('Perseus · Part I', 'How Perseus ...');
    'Preface: To My Children' -> ('Preface', 'To My Children')."""
    part, _, name = title.partition(": ")
    return part.replace(" - ", " · "), name


def illustration(path):
    """The app's colour illustrations, re-encoded (same size) to keep the EPUB small."""
    from PIL import Image
    buf = io.BytesIO()
    Image.open(os.path.join(IMAGE_DIR, path)).convert("RGB").save(buf, "JPEG", quality=82, optimize=True)
    return buf.getvalue()


def image_name(path):
    return "ill_" + os.path.basename(path).replace("_color", "")


def chapter_html(ch, edition):
    part_en, name_en = map(escape, split_title(ch["en_title"]))
    part_ko, name_ko = map(escape, split_title(ch["ko_title"]))
    parts = ['<section class="chapter" epub:type="chapter">']
    if edition == "ko":
        parts += [f'<p class="ch-num">{part_ko}</p>', f'<h1 class="ch-title">{name_ko}</h1>',
                  '<p class="ch-title-ko">&#160;</p>']
    elif edition == "en":
        parts += [f'<p class="ch-num">{part_en.upper()}</p>', f'<h1 class="ch-title">{name_en}</h1>',
                  '<p class="ch-title-ko">&#160;</p>']
    else:
        parts += [f'<p class="ch-num">{part_en.upper()} · <span{KO_ATTR}>{part_ko}</span></p>',
                  f'<h1 class="ch-title">{name_en}</h1>', f'<p class="ch-title-ko"{KO_ATTR}>{name_ko}</p>']

    first = True
    for block in ch["blocks"]:
        if block[0] == "end":
            _, en, ko = block
            text = {"en": escape(en), "ko": escape(ko), "bi": f"{escape(en)} · <span{KO_ATTR}>{escape(ko)}</span>"}[edition]
            parts.append(f'<p class="the-end">{text}</p>')
            continue
        if block[0] == "image":
            _, path, en, ko = block
            alt = escape(ko if edition == "ko" else en)
            caps = {"en": [f"<p>{escape(en)}</p>"], "ko": [f'<p class="ko"{KO_ATTR}>{escape(ko)}</p>'],
                    "bi": [f"<p>{escape(en)}</p>", f'<p class="ko"{KO_ATTR}>{escape(ko)}</p>']}[edition]
            parts.append(f'<div class="ill"><img src="../Images/{image_name(path)}" alt="{alt}"/>{"".join(caps)}</div>')
            continue
        if block[0] == "entry":
            _, en, ko = block
            text = {"en": escape(en), "ko": f'<span{KO_ATTR}>{escape(ko)}</span>',
                    "bi": f'{escape(en)}<span class="ko"{KO_ATTR}>{escape(ko)}</span>'}[edition]
            parts.append(f'<p class="salutation">{text}</p>')
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
    by = {"en": "Charles Kingsley",
          "ko": "찰스 킹즐리 지음",
          "bi": "Charles Kingsley"}[edition]
    lines = ['<section class="titlepage" epub:type="titlepage">',
             f'<p class="tp-title">{escape(ed["title"])}</p>',
             f'<p class="tp-sub"{lang_attr}>{escape(ed["subtitle"])}</p>',
             f'<p class="tp-small"{lang_attr}>{by}</p>']
    if edition == "bi":
        lines.append(f'<p class="tp-small"{KO_ATTR}>찰스 킹즐리 지음 · 현대어 새 번역</p>')
    lines += [f'<p class="tp-pub">{PUBLISHER}</p>', "</section>"]
    return "\n".join(lines)


def copyright_html(ed, edition):
    en = [f"<i>{escape(ed['title'] if edition == 'bi' else EDITIONS['en']['title'])}</i>",
          f"Modern English text and Korean translation © {YEAR} {PUBLISHER}. All rights reserved.",
          "Source text: <i>The Heroes; or, Greek Fairy Tales for My Children</i> by Charles Kingsley (1856). "
          "The original text and its illustrations are in the public domain. The illustrations in this "
          f"edition were coloured for {PUBLISHER}.",
          f"Published by {PUBLISHER}."]
    ko = [f"『{EDITIONS['ko']['title']}』",
          f"현대 영어 본문 및 한국어 번역 © {YEAR} {PUBLISHER}. 모든 권리 보유.",
          "저본: 찰스 킹즐리 『영웅들: 아이들을 위한 그리스 동화』(1856). 원작과 삽화는 공유 저작물이며, "
          f"이 판의 삽화는 {PUBLISHER}가 색을 입혔습니다.",
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
        return ": ".join(split_title(ch["en_title"]))
    if edition == "ko":
        return ": ".join(split_title(ch["ko_title"]))
    return f"{': '.join(split_title(ch['en_title']))} · {split_title(ch['ko_title'])[1]}"


def build(edition, chapters, out_dir, suffix=""):
    ed = EDITIONS[edition]
    lang = ed["lang"]
    book_id = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'tkprof.the_heroes.' + edition)}"
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
        images = sorted({b[1] for ch in chapters for b in ch["blocks"] if b[0] == "image"})
        for i, path in enumerate(images, 1):
            z.writestr(f"OEBPS/Images/{image_name(path)}", illustration(path))
            manifest.append(f'<item id="ill-{i}" href="Images/{image_name(path)}" media-type="image/jpeg"/>')
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
    <dc:subject>Juvenile Fiction / Legends, Myths, Fables / Greek &amp; Roman</dc:subject>
    <dc:subject>Fiction / Classics</dc:subject>
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
    print(f"{edition}: {out_path} ({os.path.getsize(out_path):,} bytes, {len(chapters)} chapters, "
          f"{len(images)} illustrations, cover={'yes' if has_cover else 'no'})")
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
