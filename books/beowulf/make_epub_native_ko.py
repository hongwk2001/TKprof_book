"""
make_epub_native_ko.py
Compiles the Korean edition of Beowulf into an EPUB file using Python's zipfile.
Input:  books/beowulf/chapters_kr/ch_XX_ko.txt  (44 files)
        books/beowulf/introduction_ko.txt
        books/beowulf/copyright_ko.txt
Output: books/beowulf/beowulf_ko.epub
"""

import os
import re
import zipfile

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters_kr")
IMAGES_DIR   = os.path.join(BASE_DIR, "images")
OUTPUT_FILE  = os.path.join(BASE_DIR, "beowulf_ko.epub")

CHAPTER_IMAGES = {
    11: ["illu_grendel.jpg"],
    26: ["illu_water_witch.jpg"],
    29: ["illu_grendel_head.jpg"],
    39: ["illu_dragon.jpg"],
    43: ["illu_death.png"]
}

# ── CSS Style (Korean-optimised) ──────────────────────────────────────────────
STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@400;700&family=Noto+Serif+KR:wght@400;700&display=swap');

body {
    font-family: 'Nanum Myeongjo', 'Noto Serif KR', 'Malgun Gothic', 'Apple SD Gothic Neo', serif;
    font-size: 1em;
    line-height: 1.9;
    margin: 1.5em 2em;
    color: #1a1a1a;
    background-color: #fdfaf5;
    word-break: keep-all;
    overflow-wrap: break-word;
}

h1 {
    font-size: 1.5em;
    font-weight: bold;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 0.3em;
    letter-spacing: 0.02em;
    color: #2c1a0e;
}

h2 {
    font-size: 1.05em;
    font-weight: normal;
    text-align: center;
    font-style: normal;
    margin-top: 0;
    margin-bottom: 2em;
    color: #5a3e28;
}

h2.chapter-subtitle {
    font-size: 1.15em;
    font-weight: bold;
    letter-spacing: 0.03em;
    margin-top: -1em;
    margin-bottom: 2.5em;
    color: #2c1a0e;
}

p {
    margin: 0 0 0.9em 0;
    text-indent: 1.5em;
}

p.no-indent {
    text-indent: 0;
}

.separator {
    text-align: center;
    margin: 2em 0;
    color: #8b6040;
    font-size: 1.2em;
}

img.illustration {
    display: block;
    max-width: 85%;
    margin: 1.5em auto;
}

.footnote {
    font-size: 0.85em;
    color: #555;
    margin-top: 2em;
    border-top: 1px solid #ccc;
    padding-top: 0.5em;
}

.copyright-page {
    font-size: 0.9em;
    color: #333;
}

.copyright-page h1 {
    font-size: 1.3em;
}
"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

# Korean chapter first-line patterns: "프롤로그: …", "1장: …", "43장: …"
_KO_CHAPTER_RE = re.compile(r'^(프롤로그|\d+장)\s*:')

def txt_to_html(text, title, subtitle=None, images=None):
    lines = text.split("\n")

    html_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\" xml:lang=\"ko\" lang=\"ko\">",
        "<head>",
        f"  <title>{title}</title>",
        "  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        "</head>",
        "<body>",
        f"<h1>{title}</h1>"
    ]

    if subtitle:
        html_parts.append(f"<h2 class=\"chapter-subtitle\">{subtitle}</h2>")

    # Skip first line when it is the chapter heading (already rendered as h1/h2)
    if lines and _KO_CHAPTER_RE.match(lines[0].strip()):
        lines = lines[1:]

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("[Footnote"):
            html_parts.append(f'<p class="footnote">{line}</p>')
        elif line.isupper() and len(line) < 80:
            html_parts.append(f"<h2>{line}</h2>")
        else:
            html_parts.append(f"<p>{line}</p>")

    if images:
        for img_name in images:
            html_parts.append('<div class="separator">* * *</div>')
            html_parts.append(f'<img class="illustration" src="../Images/{img_name}" alt="삽화"/>')

    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

def parse_chapter_title(text):
    """Return (h1_title, h2_subtitle) from a Korean chapter file's first line."""
    first_line = text.split("\n")[0].strip()
    if ":" in first_line:
        h1, h2 = first_line.split(":", 1)
        return h1.strip(), h2.strip()
    return first_line, None

# ── Build EPUB ────────────────────────────────────────────────────────────────
def main():
    print("한국어판 EPUB 빌드 중...")

    chapters = []
    images_to_add = []

    # 1. Introduction (Korean)
    intro_text = read_txt(os.path.join(BASE_DIR, "introduction_ko.txt"))
    intro_html = txt_to_html(intro_text, "베오울프 소개")
    chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': '베오울프 소개', 'content': intro_html})

    # 2. Prologue (ch_00_ko.txt)
    ch00_path = os.path.join(CHAPTERS_DIR, "ch_00_ko.txt")
    if os.path.exists(ch00_path):
        text = read_txt(ch00_path)
        title, subtitle = parse_chapter_title(text)
        ch_html = txt_to_html(text, title, subtitle=subtitle)
        nav_label = f"{title}: {subtitle}" if subtitle else title
        chapters.append({'id': 'ch00', 'href': 'Text/ch00.xhtml', 'title': nav_label, 'content': ch_html})

    # 3. Chapters 1–43
    for i in range(1, 44):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_ko.txt")
        if not os.path.exists(txt_path):
            print(f"  경고: {txt_path} 없음 — 건너뜀")
            continue
        text = read_txt(txt_path)
        title, subtitle = parse_chapter_title(text)

        img_names = []
        for img_name in CHAPTER_IMAGES.get(i, []):
            img_path = os.path.join(IMAGES_DIR, img_name)
            if os.path.exists(img_path):
                mime = "image/png" if img_name.endswith(".png") else "image/jpeg"
                images_to_add.append((img_path, img_name, mime))
                img_names.append(img_name)

        ch_html = txt_to_html(text, title, subtitle=subtitle, images=img_names if img_names else None)
        nav_label = f"{title}: {subtitle}" if subtitle else title
        chapters.append({'id': f"ch{i:02d}", 'href': f"Text/ch{i:02d}.xhtml", 'title': nav_label, 'content': ch_html})

    # 4. Copyright (Korean)
    copy_text = read_txt(os.path.join(BASE_DIR, "copyright_ko.txt"))
    copy_html = txt_to_html(copy_text, "저작권 및 편집 노트")
    chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': '저작권 및 편집 노트', 'content': copy_html})

    # Cover image
    has_cover = False
    cover_src = os.path.join(IMAGES_DIR, "cover.jpg")
    if os.path.exists(cover_src):
        images_to_add.append((cover_src, "cover.jpg", "image/jpeg"))
        has_cover = True

    # Deduplicate images (same illustration can appear only once in manifest)
    seen_images = {}
    unique_images = []
    for src, name, mime in images_to_add:
        if name not in seen_images:
            seen_images[name] = True
            unique_images.append((src, name, mime))
    images_to_add = unique_images

    # ── OPF ──────────────────────────────────────────────────────────────────
    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\" xml:lang=\"ko\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        "    <dc:identifier id=\"pub-id\">tkprof-beowulf-ko-2026</dc:identifier>",
        "    <dc:title>베오울프: 현대 한국어판</dc:title>",
        "    <dc:language>ko</dc:language>",
        "    <dc:creator>작자 미상</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026</dc:date>",
        "    <dc:rights>현대화 편집본 Copyright 2026 TKPROF LLC. 원문 퍼블릭 도메인.</dc:rights>",
        "    <dc:subject>서사시</dc:subject>",
        "    <dc:subject>고전 문학</dc:subject>",
        "    <dc:subject>앵글로색슨 문학</dc:subject>",
        "    <dc:subject>신화</dc:subject>",
        "    <dc:subject>한국어판</dc:subject>",
        "    <dc:subject>오디오북</dc:subject>",
        "    <meta property=\"dcterms:modified\">2026-06-27T12:00:00Z</meta>",
    ]
    if has_cover:
        opf_parts.append("    <meta name=\"cover\" content=\"cover-image\"/>")
    opf_parts.append("  </metadata>")
    opf_parts.append("  <manifest>")
    opf_parts.append("    <item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\"/>")
    opf_parts.append("    <item id=\"nav\" href=\"nav.xhtml\" media-type=\"application/xhtml+xml\" properties=\"nav\"/>")
    opf_parts.append("    <item id=\"css\" href=\"Styles/main.css\" media-type=\"text/css\"/>")

    for ch in chapters:
        opf_parts.append(f"    <item id=\"{ch['id']}\" href=\"{ch['href']}\" media-type=\"application/xhtml+xml\"/>")

    for idx, (src, name, mime) in enumerate(images_to_add):
        item_id = "cover-image" if name == "cover.jpg" else f"img{idx}"
        props = ' properties="cover-image"' if name == "cover.jpg" else ""
        opf_parts.append(f"    <item id=\"{item_id}\" href=\"Images/{name}\" media-type=\"{mime}\"{props}/>")

    opf_parts.append("  </manifest>")
    opf_parts.append("  <spine toc=\"ncx\">")
    for ch in chapters:
        opf_parts.append(f"    <itemref idref=\"{ch['id']}\"/>")
    opf_parts.append("  </spine>")
    opf_parts.append("</package>")
    opf_content = "\n".join(opf_parts)

    # ── NCX (EPUB 2 TOC) ──────────────────────────────────────────────────────
    ncx_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">",
        "  <head>",
        "    <meta name=\"dtb:uid\" content=\"tkprof-beowulf-ko-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle><text>베오울프: 현대 한국어판</text></docTitle>",
        "  <navMap>",
    ]
    for idx, ch in enumerate(chapters, 1):
        ncx_parts.append(f"    <navPoint id=\"navpoint-{idx}\" playOrder=\"{idx}\">")
        ncx_parts.append(f"      <navLabel><text>{ch['title']}</text></navLabel>")
        ncx_parts.append(f"      <content src=\"{ch['href']}\"/>")
        ncx_parts.append(f"    </navPoint>")
    ncx_parts.append("  </navMap>")
    ncx_parts.append("</ncx>")
    ncx_content = "\n".join(ncx_parts)

    # ── Nav (EPUB 3 TOC) ──────────────────────────────────────────────────────
    nav_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\" xml:lang=\"ko\" lang=\"ko\">",
        "<head><title>목차</title></head>",
        "<body>",
        "  <nav epub:type=\"toc\" id=\"toc\">",
        "    <h2>목차</h2>",
        "    <ol>",
    ]
    for ch in chapters:
        nav_parts.append(f"      <li><a href=\"{ch['href']}\">{ch['title']}</a></li>")
    nav_parts.append("    </ol>")
    nav_parts.append("  </nav>")
    nav_parts.append("</body>")
    nav_parts.append("</html>")
    nav_content = "\n".join(nav_parts)

    # ── Write ZIP / EPUB ──────────────────────────────────────────────────────
    with zipfile.ZipFile(OUTPUT_FILE, 'w') as zf:
        zf.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        container_xml = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<container xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\" version=\"1.0\">\n"
            "  <rootfiles>\n"
            "    <rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\"/>\n"
            "  </rootfiles>\n"
            "</container>"
        )
        zf.writestr('META-INF/container.xml', container_xml, compress_type=zipfile.ZIP_DEFLATED)

        zf.writestr('OEBPS/content.opf',   opf_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/toc.ncx',       ncx_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/nav.xhtml',     nav_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Styles/main.css', STYLE.encode('utf-8'),     compress_type=zipfile.ZIP_DEFLATED)

        for ch in chapters:
            zf.writestr(f"OEBPS/{ch['href']}", ch['content'].encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)

        for src, name, mime in images_to_add:
            zf.write(src, arcname=f"OEBPS/Images/{name}", compress_type=zipfile.ZIP_DEFLATED)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\n✓ 한국어판 EPUB 생성 완료: {OUTPUT_FILE}")
    print(f"  파일 크기: {size_kb:.0f} KB")
    print(f"  총 장 수: {len(chapters)} (서론 + 프롤로그 + 1~43장 + 저작권)")

if __name__ == "__main__":
    main()
