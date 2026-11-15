"""
make_epub_ko.py
Compiles the Korean version of The Epic of Gilgamesh into an EPUB file (gilgamesh_ko.epub).
"""

import os
import zipfile
import uuid
from datetime import datetime, timezone

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters")
IMAGES_DIR    = os.path.join(BASE_DIR, "images")
OUTPUT_FILE   = os.path.join(BASE_DIR, "gilgamesh_ko.epub")

# ── CSS Style ─────────────────────────────────────────────────────────────────
STYLE = """
body {
    font-family: 'Noto Serif KR', 'Malgun Gothic', 'Apple SD Gothic Neo', 'Nanum Myeongjo', serif;
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
    color: #3b2314;
}

h2 {
    font-size: 1.2em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 1em;
    color: #5a381e;
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
def escape_xml(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title):
    escaped_title = escape_xml(title)
    lines = text.split("\n")
    html_parts = [
        f"<?xml version='1.0' encoding='utf-8'?>",
        f"<!DOCTYPE html>",
        f"<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        f"<head>",
        f"  <title>{escaped_title}</title>",
        f"  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        f"</head>",
        f"<body>",
        f"<h1>{escaped_title}</h1>"
    ]
    
    is_first_p = True
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip header lines starting with #
        if line.startswith("# "):
            header_text = line[2:].strip()
            if header_text != title:
                html_parts.append(f"<h2>{escape_xml(header_text)}</h2>")
            continue

        if line.startswith("[") and line.endswith("]"):
            html_parts.append(f"<h2>{escape_xml(line[1:-1])}</h2>")
            is_first_p = True
        else:
            escaped_line = escape_xml(line)
            if is_first_p:
                html_parts.append(f"<p class=\"no-indent\">{escaped_line}</p>")
                is_first_p = False
            else:
                html_parts.append(f"<p>{escaped_line}</p>")

    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

# ── Build EPUB ────────────────────────────────────────────────────────────────
def main():
    print("Building Korean Gilgamesh EPUB...")
    
    chapters = []
    
    # 1. Introduction
    intro_txt_path = os.path.join(BASE_DIR, "introduction_ko.txt")
    if os.path.exists(intro_txt_path):
        intro_text = read_txt(intro_txt_path)
        intro_html = txt_to_html(intro_text, "독자에게 보내는 편지")
        chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': '독자에게 보내는 편지', 'content': intro_html})

    # 2. Chapters 1-6
    for i in range(1, 7):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_ko.txt")
        if not os.path.exists(txt_path):
            continue
        text = read_txt(txt_path)
        
        # Extract title from first line if available
        first_line = text.split("\n")[0].strip()
        if first_line.startswith("# "):
            title = first_line[2:].strip()
        else:
            title = f"제{i}장"
            
        ch_html = txt_to_html(text, title)
        uid = f"ch{i:02d}"
        fname = f"Text/ch{i:02d}.xhtml"
        chapters.append({'id': uid, 'href': fname, 'title': title, 'content': ch_html})

    # 3. Copyright
    copy_txt_path = os.path.join(BASE_DIR, "copyright_ko.txt")
    if os.path.exists(copy_txt_path):
        copy_text = read_txt(copy_txt_path)
        copy_html = txt_to_html(copy_text, "저작권 및 편집자 노트")
        chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': '저작권 및 편집자 노트', 'content': copy_html})

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
  <img src="../Images/cover_ko.png" alt="Cover" />
</body>
</html>"""

    # Build OPF Manifest
    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        f"    <dc:identifier id=\"pub-id\">{book_uuid}</dc:identifier>",
        "    <dc:title>길가메시 서사시 ( The Epic of Gilgamesh )</dc:title>",
        "    <dc:language>ko</dc:language>",
        "    <dc:creator>작자 미상 (고대 메소포타미아 서사시)</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026-08-12</dc:date>",
        "    <dc:description>인류 문학사상 가장 오래된 서사시. 잔혹한 폭군이었던 우루크의 왕 길가메시가 야생인 엔키두를 만나 진정한 우정을 맺고, 괴물 훔바바와 하늘의 황소를 물리친 후, 친구의 죽음으로 깨달은 삶과 죽음, 그리고 영생의 본질을 찾아 떠나는 위대한 영웅 이야기.</dc:description>",
        "    <dc:rights>한국어 번역판 Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>소설</dc:subject>",
        "    <dc:subject>고전</dc:subject>",
        "    <dc:subject>신화 및 서사시</dc:subject>",
        f"    <meta property=\"dcterms:modified\">{modified_date}</meta>",
        "    <meta name=\"cover\" content=\"cover-image\"/>",
        "  </metadata>",
        "  <manifest>",
        "    <item id=\"cover-image\" href=\"Images/cover_ko.png\" media-type=\"image/png\" properties=\"cover-image\"/>",
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
        "    <meta name=\"dtb:uid\" content=\"tkprof-gilgamesh-ko-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle>",
        "    <text>길가메시 서사시</text>",
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
        escaped_t = escape_xml(ch['title'])
        ncx_parts.append(f"    <navPoint id=\"navPoint-{play_order}\" playOrder=\"{play_order}\">")
        ncx_parts.append(f"      <navLabel><text>{escaped_t}</text></navLabel>")
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
        "    nav a { text-decoration: none; color: #3b2314; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <nav epub:type=\"toc\" id=\"toc\">",
        "    <h1>목차</h1>",
        "    <ol>",
        "      <li><a href=\"Text/cover.xhtml\">표지 (Cover)</a></li>"
    ]
    
    for ch in chapters:
        escaped_t = escape_xml(ch['title'])
        nav_parts.append(f"      <li><a href=\"{ch['href']}\">{escaped_t}</a></li>")
        
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
        
    cover_img_path = os.path.join(BASE_DIR, "cover_ko.png")

    with zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED) as epub:
        epub.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        epub.writestr("META-INF/container.xml", container_content)
        epub.write(cover_img_path, "OEBPS/Images/cover_ko.png")
        epub.writestr("OEBPS/Text/cover.xhtml", cover_html)
        epub.writestr("OEBPS/Styles/main.css", STYLE)
        epub.writestr("OEBPS/content.opf", opf_content)
        epub.writestr("OEBPS/toc.ncx", ncx_content)
        epub.writestr("OEBPS/nav.xhtml", nav_content)
        
        for ch in chapters:
            epub.writestr(f"OEBPS/{ch['href']}", ch['content'])
            
    print(f"Korean Gilgamesh EPUB created successfully at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
