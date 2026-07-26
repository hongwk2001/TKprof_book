"""
make_epub_native_ko.py
Compiles Mary Shelley's Frankenstein into a Korean EPUB3 eBook directly using Python's zipfile.
"""

import os
import zipfile
import uuid
import re
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_FILE = os.path.join(BASE_DIR, "frankenstein_ko.epub")

STYLE = """
body {
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    font-size: 1em;
    line-height: 1.6;
    margin: 1.5em 2em;
    color: #1a1a1a;
}

h1 {
    font-size: 1.6em;
    font-weight: bold;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1em;
    color: #1c2d42;
}

h2 {
    font-size: 1.3em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.8em;
    margin-bottom: 1em;
    color: #2c425e;
    text-transform: uppercase;
}

p {
    margin: 0 0 1em 0;
    text-indent: 1.2em;
}

p.no-indent {
    text-indent: 0;
}

blockquote {
    margin: 1em 0 1em 1.5em;
    padding: 0.6em 1em;
    border-left: 4px solid #1c2d42;
    background-color: #f4f7fa;
    font-style: italic;
    color: #2c3e50;
}

.cover-img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
}
"""

def read_txt(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title, ch_id=""):
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
        f"  <h1>{title}</h1>",
    ]
    
    first_p = True
    in_bq = False
    heading_count = 0
    in_contents = False

    for line in lines:
        line_s = line.strip()
        if not line_s:
            if in_bq:
                html_parts.append("  </blockquote>")
                in_bq = False
            continue

        if line_s in ["Contents", "목차"]:
            in_contents = True

        # Match Chapter/Letter headings like "제1장", "편지 1"
        is_heading = False
        if re.match(r'^(제\s*\d+\s*장|편지\s*\d+)$', line_s):
            is_heading = True

        if is_heading:
            heading_count += 1
            if ch_id == "00" and in_contents:
                if heading_count > 28:
                    in_contents = False
                else:
                    # It's a TOC list item in the intro content of Chapter 0
                    if in_bq:
                        html_parts.append("  </blockquote>")
                        in_bq = False
                    html_parts.append(f"  <p class=\"no-indent\" style=\"text-align: center;\"><strong>{line_s}</strong></p>")
                    first_p = True
                    continue
            
            if in_bq:
                html_parts.append("  </blockquote>")
                in_bq = False
            html_parts.append(f"  <h2>{line_s}</h2>")
            first_p = True
            continue

        if line_s.startswith("# ") or line_s.startswith("Part "):
            continue
            
        if line_s.startswith(">"):
            bq_content = line_s[1:].strip()
            bq_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', bq_content)
            if not in_bq:
                html_parts.append("  </blockquote>")
                in_bq = True
            html_parts.append(f"    <p class=\"no-indent\">{bq_content}</p>")
        else:
            if in_bq:
                html_parts.append("  </blockquote>")
                in_bq = False

            if first_p:
                html_parts.append(f"  <p class=\"no-indent\">{line_s}</p>")
                first_p = False
            else:
                html_parts.append(f"  <p>{line_s}</p>")

    if in_bq:
        html_parts.append("  </blockquote>")
            
    html_parts.append("</body>\n</html>")
    return "\n".join(html_parts)

def build_epub():
    book_id = f"urn:uuid:{uuid.uuid4()}"
    pub_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    cover_path = os.path.join(IMAGES_DIR, "cover_ko.jpg")
    has_cover = os.path.exists(cover_path)

    intro_text = read_txt(os.path.join(BASE_DIR, "introduction_ko.txt"))
    overview_text = read_txt(os.path.join(BASE_DIR, "overview_ko.txt"))
    copyright_text = read_txt(os.path.join(BASE_DIR, "copyright_ko.txt"))

    chapters_data = []
    
    chapter_titles = [
        "제1부: 편지 I–IV",
        "제2부: 제1장–4장",
        "제3부: 제5장–8장",
        "제4부: 제9장–12장",
        "제5부: 제13장–16장",
        "제6부: 제17장–20장",
        "제7부: 제21장–24장"
    ]

    for i in range(7):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(CHAPTERS_DIR, f"ch_{ch_str}_ko.txt")
        text = read_txt(txt_file)
        title = chapter_titles[i]
        chapters_data.append((ch_str, title, text))

    with zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)

        container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
        z.writestr("META-INF/container.xml", container_xml)
        z.writestr("OEBPS/Styles/main.css", STYLE)

        manifest_items = [
            '<item id="style" href="Styles/main.css" media-type="text/css"/>',
            '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
            '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
        ]
        spine_items = []
        ncx_targets = []
        nav_targets = []

        if has_cover:
            with open(cover_path, "rb") as img:
                z.writestr("OEBPS/Images/cover.jpg", img.read())
            manifest_items.append('<item id="cover-image" href="Images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>')

            cover_xhtml = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Cover</title>
  <link rel="stylesheet" href="../Styles/main.css" type="text/css"/>
</head>
<body style="margin:0; padding:0; text-align:center;">
  <img src="../Images/cover.jpg" alt="Cover" class="cover-img"/>
</body>
</html>"""
            z.writestr("OEBPS/Text/cover.xhtml", cover_xhtml)
            manifest_items.append('<item id="cover" href="Text/cover.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="cover"/>')

        if intro_text:
            z.writestr("OEBPS/Text/intro.xhtml", txt_to_html(intro_text, "서문"))
            manifest_items.append('<item id="intro" href="Text/intro.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="intro"/>')
            ncx_targets.append(("서문", "Text/intro.xhtml"))
            nav_targets.append(("서문", "Text/intro.xhtml"))

        if overview_text:
            z.writestr("OEBPS/Text/overview.xhtml", txt_to_html(overview_text, "도서 개요"))
            manifest_items.append('<item id="overview" href="Text/overview.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="overview"/>')
            ncx_targets.append(("도서 개요", "Text/overview.xhtml"))
            nav_targets.append(("도서 개요", "Text/overview.xhtml"))

        for ch_str, title, text in chapters_data:
            filename = f"ch_{ch_str}.xhtml"
            item_id = f"ch_{ch_str}"
            z.writestr(f"OEBPS/Text/{filename}", txt_to_html(text, title, ch_id=ch_str))
            manifest_items.append(f'<item id="{item_id}" href="Text/{filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{item_id}"/>')
            ncx_targets.append((title, f"Text/{filename}"))
            nav_targets.append((title, f"Text/{filename}"))

        if copyright_text:
            z.writestr("OEBPS/Text/copyright.xhtml", txt_to_html(copyright_text, "판권 및 저작권 정보"))
            manifest_items.append('<item id="copyright" href="Text/copyright.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="copyright"/>')
            ncx_targets.append(("판권 및 저작권 정보", "Text/copyright.xhtml"))
            nav_targets.append(("판권 및 저작권 정보", "Text/copyright.xhtml"))

        manifest_str = "\n    ".join(manifest_items)
        spine_str = "\n    ".join(spine_items)

        content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">{book_id}</dc:identifier>
    <dc:title>프랑켄슈타인 (현대어 한국어판)</dc:title>
    <dc:creator>메리 울스턴크래프트 셸리</dc:creator>
    <dc:language>ko</dc:language>
    <dc:publisher>TKPROF LLC</dc:publisher>
    <meta property="dcterms:modified">{pub_date}</meta>
  </metadata>
  <manifest>
    {manifest_str}
  </manifest>
  <spine toc="ncx">
    {spine_str}
  </spine>
</package>"""
        z.writestr("OEBPS/content.opf", content_opf)

        nav_points = []
        for idx, (label, src) in enumerate(ncx_targets, 1):
            nav_points.append(f"""    <navPoint id="navPoint-{idx}" playOrder="{idx}">
      <navLabel><text>{label}</text></navLabel>
      <content src="{src}"/>
    </navPoint>""")
        nav_points_str = "\n".join(nav_points)

        toc_ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book_id}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>프랑켄슈타인</text></docTitle>
  <navMap>
{nav_points_str}
  </navMap>
</ncx>"""
        z.writestr("OEBPS/toc.ncx", toc_ncx)

        nav_li = []
        for label, src in nav_targets:
            nav_li.append(f'        <li><a href="{src}">{label}</a></li>')
        nav_li_str = "\n".join(nav_li)

        nav_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>목차</title>
  <link rel="stylesheet" href="Styles/main.css" type="text/css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>목차</h1>
    <ol>
{nav_li_str}
    </ol>
  </nav>
</body>
</html>"""
        z.writestr("OEBPS/nav.xhtml", nav_xhtml)

    print(f"Successfully compiled native EPUB: {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE)} bytes)")

if __name__ == "__main__":
    build_epub()
