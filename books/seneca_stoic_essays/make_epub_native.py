"""
make_epub_native.py
Compiles Seneca's Stoic Essays (On the Shortness of Life & On Happiness) into an English EPUB3 eBook directly using Python's zipfile.
"""

import os
import zipfile
import uuid
import re
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_FILE = os.path.join(BASE_DIR, "seneca_stoic_essays_en.epub")

STYLE = """
body {
    font-family: 'Times New Roman', Times, serif;
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

.part-title {
    text-align: center;
    margin-top: 5em;
}

.part-title h1 {
    font-size: 2em;
    color: #1c2d42;
}

.part-title h2 {
    font-size: 1.5em;
    color: #2c425e;
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
        f"  <h1>{title}</h1>",
    ]
    
    first_p = True
    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        if line_s.startswith("Chapter ") or line_s.startswith("# ") or (line_s.startswith("[") and line_s.endswith("]")):
            continue
            
        if first_p:
            html_parts.append(f"  <p class=\"no-indent\">{line_s}</p>")
            first_p = False
        else:
            html_parts.append(f"  <p>{line_s}</p>")
            
    html_parts.append("</body>\n</html>")
    return "\n".join(html_parts)

def build_epub():
    book_id = f"urn:uuid:{uuid.uuid4()}"
    pub_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    cover_path = os.path.join(IMAGES_DIR, "cover.jpg")
    has_cover = os.path.exists(cover_path)

    intro_text = read_txt(os.path.join(BASE_DIR, "introduction_en.txt"))
    overview_text = read_txt(os.path.join(BASE_DIR, "overview_en.txt"))
    copyright_text = read_txt(os.path.join(BASE_DIR, "copyright_en.txt"))

    part1_chapters = []
    shortness_dir = os.path.join(CHAPTERS_DIR, "shortness_of_life")
    for i in range(1, 21):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(shortness_dir, f"ch_{ch_str}_en.txt")
        text = read_txt(txt_file)
        
        first_line = text.split("\n")[0].strip() if text else ""
        if first_line.startswith("[") and first_line.endswith("]"):
            title = first_line[1:-1].strip()
        else:
            title = f"Chapter {i}"
        part1_chapters.append((f"shortness_ch_{ch_str}", f"shortness_ch_{ch_str}.xhtml", title, text))

    part2_chapters = []
    happiness_dir = os.path.join(CHAPTERS_DIR, "on_happiness")
    for i in range(1, 29):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(happiness_dir, f"ch_{ch_str}_en.txt")
        text = read_txt(txt_file)
        
        first_line = text.split("\n")[0].strip() if text else ""
        if first_line.startswith("[") and first_line.endswith("]"):
            title = first_line[1:-1].strip()
        else:
            title = f"Chapter {i}"
        part2_chapters.append((f"happiness_ch_{ch_str}", f"happiness_ch_{ch_str}.xhtml", title, text))

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
            z.writestr("OEBPS/Text/intro.xhtml", txt_to_html(intro_text, "Introduction"))
            manifest_items.append('<item id="intro" href="Text/intro.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="intro"/>')
            ncx_targets.append(("Introduction", "Text/intro.xhtml"))
            nav_targets.append(("Introduction", "Text/intro.xhtml"))

        if overview_text:
            z.writestr("OEBPS/Text/overview.xhtml", txt_to_html(overview_text, "Overview of Chapters"))
            manifest_items.append('<item id="overview" href="Text/overview.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="overview"/>')
            ncx_targets.append(("Overview of Chapters", "Text/overview.xhtml"))
            nav_targets.append(("Overview of Chapters", "Text/overview.xhtml"))

        # Part I Divider Page
        part1_divider = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Part I</title>
  <link rel="stylesheet" href="../Styles/main.css" type="text/css"/>
</head>
<body>
  <div class="part-title">
    <h1>PART I</h1>
    <h2>On the Shortness of Life</h2>
  </div>
</body>
</html>"""
        z.writestr("OEBPS/Text/part1_intro.xhtml", part1_divider)
        manifest_items.append('<item id="part1_intro" href="Text/part1_intro.xhtml" media-type="application/xhtml+xml"/>')
        spine_items.append('<itemref idref="part1_intro"/>')
        ncx_targets.append(("PART I: On the Shortness of Life", "Text/part1_intro.xhtml"))
        nav_targets.append(("PART I: On the Shortness of Life", "Text/part1_intro.xhtml"))

        # Part I Chapters
        for item_id, filename, title, text in part1_chapters:
            z.writestr(f"OEBPS/Text/{filename}", txt_to_html(text, title))
            manifest_items.append(f'<item id="{item_id}" href="Text/{filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{item_id}"/>')
            ncx_targets.append((f"  {title}", f"Text/{filename}"))
            nav_targets.append((f"  {title}", f"Text/{filename}"))

        # Part II Divider Page
        part2_divider = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Part II</title>
  <link rel="stylesheet" href="../Styles/main.css" type="text/css"/>
</head>
<body>
  <div class="part-title">
    <h1>PART II</h1>
    <h2>On Happiness</h2>
  </div>
</body>
</html>"""
        z.writestr("OEBPS/Text/part2_intro.xhtml", part2_divider)
        manifest_items.append('<item id="part2_intro" href="Text/part2_intro.xhtml" media-type="application/xhtml+xml"/>')
        spine_items.append('<itemref idref="part2_intro"/>')
        ncx_targets.append(("PART II: On Happiness", "Text/part2_intro.xhtml"))
        nav_targets.append(("PART II: On Happiness", "Text/part2_intro.xhtml"))

        # Part II Chapters
        for item_id, filename, title, text in part2_chapters:
            z.writestr(f"OEBPS/Text/{filename}", txt_to_html(text, title))
            manifest_items.append(f'<item id="{item_id}" href="Text/{filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{item_id}"/>')
            ncx_targets.append((f"  {title}", f"Text/{filename}"))
            nav_targets.append((f"  {title}", f"Text/{filename}"))

        if copyright_text:
            z.writestr("OEBPS/Text/copyright.xhtml", txt_to_html(copyright_text, "Copyright & Credits"))
            manifest_items.append('<item id="copyright" href="Text/copyright.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="copyright"/>')
            ncx_targets.append(("Copyright & Credits", "Text/copyright.xhtml"))
            nav_targets.append(("Copyright & Credits", "Text/copyright.xhtml"))

        manifest_str = "\n    ".join(manifest_items)
        spine_str = "\n    ".join(spine_items)

        content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">{book_id}</dc:identifier>
    <dc:title>Stoic Essays on Life and Happiness</dc:title>
    <dc:creator>Lucius Annaeus Seneca</dc:creator>
    <dc:language>en</dc:language>
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
      <navLabel><text>{label.strip()}</text></navLabel>
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
  <docTitle><text>Stoic Essays on Life and Happiness</text></docTitle>
  <navMap>
{nav_points_str}
  </navMap>
</ncx>"""
        z.writestr("OEBPS/toc.ncx", toc_ncx)

        nav_li = []
        for label, src in nav_targets:
            # Format indentations cleanly
            style_attr = ' style="padding-left: 20px;"' if label.startswith("  ") else ""
            nav_li.append(f'        <li{style_attr}><a href="{src}">{label.strip()}</a></li>')
        nav_li_str = "\n".join(nav_li)

        nav_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>Table of Contents</title>
  <link rel="stylesheet" href="Styles/main.css" type="text/css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Table of Contents</h1>
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
