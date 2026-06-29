import os
import zipfile
import uuid
from datetime import datetime, timezone
import re

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters_kr_v2")
IMAGES_DIR    = os.path.join(BASE_DIR, "images")
OUTPUT_FILE   = os.path.join(BASE_DIR, "beowulf_ko_v2.epub")

# ── Image Mapping ────────────────────────────────────────────────────────────
IMAGE_MAPPING = {
    'ch12': 'illu_grendel.jpg',
    'ch26': 'illu_water_witch.jpg',
    'ch29': 'illu_grendel_head.jpg',
    'ch39': 'illu_dragon.jpg',
    'ch43': 'illu_death.png'
}

# ── CSS Style ─────────────────────────────────────────────────────────────────
STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&display=swap');

body {
    font-family: 'Noto Serif KR', serif;
    font-size: 1em;
    line-height: 1.8;
    margin: 1.5em 2em;
    color: #1a1a1a;
    background-color: #fdfaf5;
}

h1 {
    font-size: 1.6em;
    font-weight: bold;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1em;
    letter-spacing: 0.05em;
    color: #2c1a0e;
}

h2 {
    font-size: 1.2em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 1em;
    color: #5a3e28;
}

p {
    margin: 0 0 1em 0;
    text-indent: 1em;
    word-break: keep-all;
}

blockquote {
    font-style: italic;
    font-weight: bold;
    margin: 1.5em 2em;
    padding: 0.5em 1em;
    border-left: 4px solid #8b6040;
    background-color: #f5eedf;
    color: #3b2a1a;
    text-indent: 0;
}

blockquote p {
    text-indent: 0;
    margin: 0;
}

.illustration {
    text-align: center;
    margin: 2em 0;
}

.illustration img {
    max-width: 100%;
    height: auto;
    border: 2px solid #8b6040;
    border-radius: 4px;
}
"""

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title, image_file=None):
    lines = text.split("\n")
    html_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head>",
        f"  <title>{title}</title>",
        "  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        "</head>",
        "<body>",
        f"<h1>{title}</h1>"
    ]
    
    if image_file:
        html_parts.append(f"<div class=\"illustration\"><img src=\"../Images/{image_file}\" alt=\"Illustration\"/></div>")
    
    in_blockquote = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip the chapter title if it's already the first line
        if line == title or (line.startswith("제") and "장" in line and ":" in line):
            if html_parts[-1] == f"<h1>{title}</h1>" or html_parts[-2] == f"<h1>{title}</h1>": # In case of image
                continue

        if line.startswith(">"):
            if not in_blockquote:
                html_parts.append("<blockquote>")
                in_blockquote = True
            
            clean_line = line.lstrip("> *").rstrip("*").strip()
            if clean_line:
                html_parts.append(f"<p>{clean_line}</p>")
            continue
        else:
            if in_blockquote:
                html_parts.append("</blockquote>")
                in_blockquote = False
                
        html_parts.append(f"<p>{line}</p>")

    if in_blockquote:
        html_parts.append("</blockquote>")

    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

def get_media_type(filename):
    ext = filename.lower().split('.')[-1]
    if ext in ['jpg', 'jpeg']:
        return 'image/jpeg'
    elif ext == 'png':
        return 'image/png'
    elif ext == 'gif':
        return 'image/gif'
    return 'application/octet-stream'

def main():
    print("Building EPUB natively with images...")
    
    chapters = []
    
    # 0. Cover Page
    cover_html = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head>",
        "  <title>Cover</title>",
        "  <style type=\"text/css\">",
        "    body { margin: 0; padding: 0; text-align: center; background-color: #000; }",
        "    img { max-width: 100%; height: 100vh; object-fit: contain; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <div><img src=\"../Images/cover.jpg\" alt=\"Cover\"/></div>",
        "</body>",
        "</html>"
    ]
    chapters.append({'id': 'cover', 'href': 'Text/cover.xhtml', 'title': '표지', 'content': "\n".join(cover_html)})

    # 1. Introduction
    intro_txt_path = os.path.join(CHAPTERS_DIR, "introduction_ko_v2.txt")
    if os.path.exists(intro_txt_path):
        intro_text = read_txt(intro_txt_path)
        intro_html = txt_to_html(intro_text, "독자에게 보내는 편지")
        chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': '독자에게 보내는 편지', 'content': intro_html})

    # 2. Chapters 0-43
    for i in range(44):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_ko.txt")
        if not os.path.exists(txt_path):
            continue
        
        text = read_txt(txt_path)
        first_line = text.split("\n")[0].strip()
        title = first_line if first_line else f"제{i}장"
        
        uid = f"ch{i:02d}"
        fname = f"Text/ch{i:02d}.xhtml"
        
        image_file = IMAGE_MAPPING.get(uid)
        ch_html = txt_to_html(text, title, image_file)
        
        chapters.append({'id': uid, 'href': fname, 'title': title, 'content': ch_html})

    # 3. Copyright
    copy_txt_path = os.path.join(CHAPTERS_DIR, "copyright_ko_v2.txt")
    if os.path.exists(copy_txt_path):
        copy_text = read_txt(copy_txt_path)
        copy_html = txt_to_html(copy_text, "저작권 및 편집자 노트")
        chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': '저작권 및 편집자 노트', 'content': copy_html})

    book_uuid = f"urn:uuid:{uuid.uuid4()}"
    modified_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        f"    <dc:identifier id=\"pub-id\">{book_uuid}</dc:identifier>",
        "    <dc:title>베오울프: 스펙터클 현대 한국어판 (Beowulf: Spectacular Modern Korean Edition)</dc:title>",
        "    <dc:language>ko</dc:language>",
        "    <dc:creator>작자 미상 (Anonymous)</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026-06-28</dc:date>",
        "    <dc:description>영문학 최고(最古)의 서사시 베오울프를 현대 판타지 소설의 문법에 맞춰 재탄생시킨 스펙터클 현대 한국어판. 영웅의 처절한 혈투와 웅장한 전설을 만난다.</dc:description>",
        "    <dc:rights>한국어 번역판 Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>판타지</dc:subject>",
        "    <dc:subject>액션</dc:subject>",
        "    <dc:subject>웹소설</dc:subject>",
        "    <meta name=\"cover\" content=\"cover-image\"/>",
        f"    <meta property=\"dcterms:modified\">{modified_date}</meta>",
        "  </metadata>",
        "  <manifest>",
        "    <item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\"/>",
        "    <item id=\"nav\" href=\"nav.xhtml\" media-type=\"application/xhtml+xml\" properties=\"nav\"/>",
        "    <item id=\"css\" href=\"Styles/main.css\" media-type=\"text/css\"/>"
    ]
    
    # Images in manifest
    image_files = ['cover.jpg', 'illu_death.png', 'illu_dragon.jpg', 'illu_grendel.jpg', 'illu_grendel_head.jpg', 'illu_water_witch.jpg']
    for img in image_files:
        img_id = "cover-image" if img == "cover.jpg" else f"img_{img.split('.')[0]}"
        mtype = get_media_type(img)
        props = " properties=\"cover-image\"" if img == "cover.jpg" else ""
        opf_parts.append(f"    <item id=\"{img_id}\" href=\"Images/{img}\" media-type=\"{mtype}\"{props}/>")
    
    # Chapters in manifest
    for ch in chapters:
        opf_parts.append(f"    <item id=\"{ch['id']}\" href=\"{ch['href']}\" media-type=\"application/xhtml+xml\"/>")
        
    opf_parts.append("  </manifest>")
    opf_parts.append("  <spine toc=\"ncx\">")
    for ch in chapters:
        opf_parts.append(f"    <itemref idref=\"{ch['id']}\"/>")
    opf_parts.append("  </spine>")
    opf_parts.append("</package>")
    opf_content = "\n".join(opf_parts)

    ncx_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">",
        "  <head>",
        "    <meta name=\"dtb:uid\" content=\"tkprof-beowulf-ko-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle><text>베오울프: 스펙터클 현대 한국어판</text></docTitle>",
        "  <navMap>"
    ]
    for idx, ch in enumerate(chapters, 1):
        ncx_parts.append(f"    <navPoint id=\"navpoint-{idx}\" playOrder=\"{idx}\">")
        ncx_parts.append(f"      <navLabel><text>{ch['title']}</text></navLabel>")
        ncx_parts.append(f"      <content src=\"{ch['href']}\"/>")
        ncx_parts.append(f"    </navPoint>")
    ncx_parts.append("  </navMap>")
    ncx_parts.append("</ncx>")
    ncx_content = "\n".join(ncx_parts)

    nav_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head><title>목차</title></head>",
        "<body>",
        "  <nav epub:type=\"toc\" id=\"toc\">",
        "    <h2>목차</h2>",
        "    <ol>"
    ]
    for ch in chapters:
        nav_parts.append(f"      <li><a href=\"{ch['href']}\">{ch['title']}</a></li>")
    nav_parts.append("    </ol>")
    nav_parts.append("  </nav>")
    nav_parts.append("</body>")
    nav_parts.append("</html>")
    nav_content = "\n".join(nav_parts)

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
        
        zf.writestr('OEBPS/content.opf', opf_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/toc.ncx', ncx_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/nav.xhtml', nav_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Styles/main.css', STYLE.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        
        for ch in chapters:
            zf.writestr(f"OEBPS/{ch['href']}", ch['content'].encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
            
        # Write images to zip
        for img in image_files:
            img_path = os.path.join(IMAGES_DIR, img)
            if os.path.exists(img_path):
                zf.write(img_path, f"OEBPS/Images/{img}", compress_type=zipfile.ZIP_STORED)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\\nNative EPUB created: {OUTPUT_FILE}")
    print(f"Size: {size_kb:.0f} KB")

if __name__ == "__main__":
    main()
