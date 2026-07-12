"""
make_epub_ko.py
Compiles the Korean version of The Odyssey (오디세이아) into an EPUB file.
"""

import os
import zipfile
import uuid
import re
from datetime import datetime, timezone

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE   = os.path.join(BASE_DIR, "odyssey_ko.epub")

# ── CSS Style ─────────────────────────────────────────────────────────────────
STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');

body {
    font-family: 'Noto Serif KR', serif;
    font-size: 1em;
    line-height: 1.8;
    margin: 1.5em 2em;
    color: #2c2c2c;
    background-color: #fdfdfd;
}

h1 {
    font-size: 1.6em;
    font-weight: bold;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1em;
    color: #1a2a3a;
}

h2 {
    font-size: 1.2em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 1em;
    color: #2a3a4a;
}

p {
    margin: 0 0 1.2em 0;
    text-indent: 1em;
    word-break: keep-all;
}

p.no-indent {
    text-indent: 0;
}
"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title):
    lines = text.split("\n")
    html_parts = [
        f"<?xml version='1.0' encoding='utf-8'?>",
        f"<!DOCTYPE html>",
        f"<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        f"<head>",
        f"  <title>{title}</title>",
        f"  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        f"</head>",
        f"<body>",
        f"<h1>{title}</h1>"
    ]
    
    is_first_p = True
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip the chapter title if it's already the first line
        if line == title:
            continue
        
        # Check for headings or regular paragraphs
        if line.startswith("[") and line.endswith("]"):
            html_parts.append(f"<h2>{line[1:-1]}</h2>")
            is_first_p = True
        else:
            if is_first_p:
                html_parts.append(f"<p class=\"no-indent\">{line}</p>")
                is_first_p = False
            else:
                html_parts.append(f"<p>{line}</p>")

    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

# ── Build EPUB ────────────────────────────────────────────────────────────────
def main():
    print("Building Korean EPUB for Odyssey natively...")
    
    chapters = []
    
    # 1. Introduction
    intro_txt_path = os.path.join(BASE_DIR, "introduction_ko.txt")
    if os.path.exists(intro_txt_path):
        intro_text = read_txt(intro_txt_path)
        # Skip the title in text compilation
        lines = intro_text.split("\n")
        intro_body = "\n".join(lines[1:]) if lines[0].strip() == "오디세이아 소개" else intro_text
        intro_html = txt_to_html(intro_body, "오디세이아 소개")
        chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': '오디세이아 소개', 'content': intro_html})

    # 2. Chapters 1-24
    NUM_MAP = {
        1: '일', 2: '이', 3: '삼', 4: '사', 5: '오', 6: '육', 7: '칠', 8: '팔', 9: '구', 10: '십',
        11: '십일', 12: '십이', 13: '십삼', 14: '십사', 15: '십오', 16: '십육', 17: '십칠', 18: '십팔', 19: '십구', 20: '이십',
        21: '이십일', 22: '이십이', 23: '이십삼', 24: '이십사'
    }

    for i in range(1, 25):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_ko.txt")
        if not os.path.exists(txt_path):
            print(f"Warning: ch_{i:02d}_ko.txt missing, skipping.")
            continue
        sino_num = NUM_MAP[i]
        title = f"제 {sino_num}장"
        text = read_txt(txt_path)
        
        # We want to keep the subtitle (synopsis) inside the text as well
        ch_html = txt_to_html(text, title)
        uid = f"ch{i:02d}"
        fname = f"Text/ch{i:02d}.xhtml"
        chapters.append({'id': uid, 'href': fname, 'title': title, 'content': ch_html})

    # 3. Copyright
    copy_txt_path = os.path.join(BASE_DIR, "copyright_ko.txt")
    if os.path.exists(copy_txt_path):
        copy_text = read_txt(copy_txt_path)
        lines = copy_text.split("\n")
        copy_body = "\n".join(lines[1:]) if lines[0].strip() == "판권 및 본 에디션 소개" else copy_text
        copy_html = txt_to_html(copy_body, "판권 및 본 에디션 소개")
        chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': '판권 및 본 에디션 소개', 'content': copy_html})

    book_uuid = f"urn:uuid:{uuid.uuid4()}"
    modified_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    cover_html = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>Cover</title>
  <style type="text/css">
    body { margin: 0; padding: 0; text-align: center; background-color: #ffffff; }
    img { max-width: 100%; height: auto; }
  </style>
</head>
<body>
  <img src="../Images/cover.png" alt="Cover" />
</body>
</html>"""

    # Build OPF Manifest
    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        f"    <dc:identifier id=\"pub-id\">{book_uuid}</dc:identifier>",
        "    <dc:title>오디세이아 (Odysseia)</dc:title>",
        "    <dc:language>ko</dc:language>",
        "    <dc:creator>호메로스 (Homeros)</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026-07-11</dc:date>",
        "    <dc:description>고대 그리스의 영웅 오디세우스가 트로이 전쟁이 끝난 후 바다의 신 포세이돈의 분노를 극복하고 온갖 시련을 이겨내며 십 년 만에 고향 이타카로 돌아가는 대여정을 현대 청소년과 일반 독자들을 위해 흥미진진한 현대 구어체로 재해석한 소설.</dc:description>",
        "    <dc:rights>한국어 번역판 Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>소설</dc:subject>",
        "    <dc:subject>고전</dc:subject>",
        "    <dc:subject>그리스 신화</dc:subject>",
        f"    <meta property=\"dcterms:modified\">{modified_date}</meta>",
        "    <meta name=\"cover\" content=\"cover-image\"/>",
        "  </metadata>",
        "  <manifest>",
        "    <item id=\"cover-image\" href=\"Images/cover.png\" media-type=\"image/png\" properties=\"cover-image\"/>",
        "    <item id=\"cover\" href=\"Text/cover.xhtml\" media-type=\"application/xhtml+xml\"/>",
        "    <item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\"/>",
        "    <item id=\"nav\" href=\"nav.xhtml\" media-type=\"application/xhtml+xml\" properties=\"nav\"/>",
        "    <item id=\"css\" href=\"Styles/main.css\" media-type=\"text/css\"/>"
    ]
    
    for ch in chapters:
        opf_parts.append(f"    <item id=\"{ch['id']}\" href=\"{ch['href']}\" media-type=\"application/xhtml+xml\"/>")
        
    opf_parts.append("  </manifest>")
    opf_parts.append("  <spine toc=\"ncx\">")
    opf_parts.append("    <itemref idref=\"cover\"/>")
    for ch in chapters:
        opf_parts.append(f"    <itemref idref=\"{ch['id']}\"/>")
    opf_parts.append("  </spine>")
    opf_parts.append("</package>")
    opf_content = "\n".join(opf_parts)

    # Build NCX
    ncx_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">",
        "  <head>",
        "    <meta name=\"dtb:uid\" content=\"tkprof-odyssey-ko-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle>",
        "    <text>오디세이아</text>",
        "  </docTitle>",
        "  <navMap>"
    ]
    play_order = 1
    ncx_parts.append(f"    <navPoint id=\"navPoint-{play_order}\" playOrder=\"{play_order}\">")
    ncx_parts.append(f"      <navLabel><text>표지 (Cover)</text></navLabel>")
    ncx_parts.append(f"      <content src=\"Text/cover.xhtml\"/>")
    ncx_parts.append(f"    </navPoint>")
    
    for ch in chapters:
        play_order += 1
        ncx_parts.append(f"    <navPoint id=\"navPoint-{play_order}\" playOrder=\"{play_order}\">")
        ncx_parts.append(f"      <navLabel><text>{ch['title']}</text></navLabel>")
        ncx_parts.append(f"      <content src=\"{ch['href']}\"/>")
        ncx_parts.append(f"    </navPoint>")
        
    ncx_parts.append("  </navMap>")
    ncx_parts.append("</ncx>")
    ncx_content = "\n".join(ncx_parts)

    # Build HTML5 Navigation
    nav_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head>",
        "  <title>Table of Contents</title>",
        "  <style type=\"text/css\">",
        "    body { font-family: sans-serif; margin: 2em; }",
        "    nav ol { list-style-type: none; padding-left: 0; }",
        "    nav li { margin-bottom: 0.5em; }",
        "    nav a { text-decoration: none; color: #1a2a3a; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <nav epub:type=\"toc\" id=\"toc\">",
        "    <h1>목차</h1>",
        "    <ol>",
        "      <li><a href=\"Text/cover.xhtml\">표지 (Cover)</a></li>"
    ]
    
    for ch in chapters:
        nav_parts.append(f"      <li><a href=\"{ch['href']}\">{ch['title']}</a></li>")
        
    nav_parts.append("    </ol>")
    nav_parts.append("  </nav>")
    nav_parts.append("</body>")
    nav_parts.append("</html>")
    nav_content = "\n".join(nav_parts)

    # Write container.xml
    container_content = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""

    # Zip output
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        
    with zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED) as epub:
        epub.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        epub.writestr("META-INF/container.xml", container_content)
        epub.write(os.path.join(BASE_DIR, "cover.png"), "OEBPS/Images/cover.png")
        epub.writestr("OEBPS/Text/cover.xhtml", cover_html)
        epub.writestr("OEBPS/Styles/main.css", STYLE)
        epub.writestr("OEBPS/content.opf", opf_content)
        epub.writestr("OEBPS/toc.ncx", ncx_content)
        epub.writestr("OEBPS/nav.xhtml", nav_content)
        
        for ch in chapters:
            epub.writestr(f"OEBPS/{ch['href']}", ch['content'])
            
    print(f"Korean EPUB for Odyssey created successfully at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
