"""
make_epub_native.py
Compiles A Tale of Two Cities into an English EPUB3 eBook directly using Python's zipfile.
Includes embedded color illustrations.
"""

import os
import zipfile
import uuid
import re
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "two_cities.epub")

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

.illustration-container {
    text-align: center;
    margin: 1.5em 0;
}

.illustration {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
"""

def read_txt(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title, book_part=None):
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
    ]
    
    if book_part:
        html_parts.append(f"  <h2>{book_part}</h2>")
        
    html_parts.append(f"  <h1>{title}</h1>")
    
    first_p = True
    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue
        if line_s.startswith("Book the First") or line_s.startswith("Book the Second") or line_s.startswith("Book the Third"):
            continue
        if line_s.startswith("CHAPTER ") or line_s.startswith("Chapter ") or line_s.startswith("[Chapter ") or line_s.startswith("[Book "):
            continue
        if line_s.startswith("The Period") or line_s.startswith("The Mail") or line_s.startswith("The Night Shadows") or line_s.startswith("The Preparation") or line_s.startswith("The Wine-shop") or line_s.startswith("The Shoemaker"):
            continue

        # Convert illustration markdown to HTML tag
        # e.g. ![illustration](images/0403m_color.png)
        img_match = re.match(r'!\[illustration\]\(images/(.*?)\)', line_s)
        if img_match:
            img_filename = img_match.group(1)
            html_parts.append(f"  <div class=\"illustration-container\"><img src=\"../Images/{img_filename}\" alt=\"Illustration\" class=\"illustration\"/></div>")
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

    intro_text = read_txt(os.path.join(BASE_DIR, "introduction_en.txt"))
    copyright_text = read_txt(os.path.join(BASE_DIR, "copyright_en.txt"))

    # Chapters config: (Book Num, Ch Num, Ch Title)
    book_structure = []
    # Book 1: 6 chapters
    book1_titles = [
        "The Period", "The Mail", "The Night Shadows", "The Preparation", "The Wine-shop", "The Shoemaker"
    ]
    for idx, title in enumerate(book1_titles, 1):
        book_structure.append((1, idx, title))

    # Book 2: 24 chapters
    book2_titles = [
        "Five Years Later", "A Sight", "A Disappointment", "Congratulatory", "The Jackal", 
        "Hundreds of People", "Monseigneur in Town", "Monseigneur in the Country", "The Gorgon's Head", 
        "Two Promises", "A Companion Picture", "The Fellow of Delicacy", "The Fellow of No Delicacy", 
        "The Honest Tradesman", "Knitting", "Still Knitting", "One Night", "Nine Days", 
        "An Opinion", "A Plea", "Echoing Footsteps", "The Sea Still Rises", "Fire Rises", "Drawn to the Loadstone Rock"
    ]
    for idx, title in enumerate(book2_titles, 1):
        book_structure.append((2, idx, title))

    # Book 3: 15 chapters
    book3_titles = [
        "In Secret", "The Grindstone", "The Shadow", "Calm in Storm", "The Wood-sawyer", 
        "Triumph", "A Knock at the Door", "A Hand at Cards", "The Game Played", "The Substance of the Shadow", 
        "Dusk", "Darkness", "Fifty-two", "The Knitting Done", "The Footsteps Die Out For Ever"
    ]
    for idx, title in enumerate(book3_titles, 1):
        book_structure.append((3, idx, title))

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

        # Gather and bundle all images
        for f in os.listdir(IMAGES_DIR):
            if f.endswith("_color.png"):
                img_path = os.path.join(IMAGES_DIR, f)
                with open(img_path, "rb") as img_file:
                    z.writestr(f"OEBPS/Images/{f}", img_file.read())
                manifest_items.append(f'<item id="{f[:-4]}" href="Images/{f}" media-type="image/png"/>')

        if intro_text:
            z.writestr("OEBPS/Text/intro.xhtml", txt_to_html(intro_text, "A Note to the Reader"))
            manifest_items.append('<item id="intro" href="Text/intro.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="intro"/>')
            ncx_targets.append(("A Note to the Reader", "Text/intro.xhtml"))
            nav_targets.append(("A Note to the Reader", "Text/intro.xhtml"))

        for book_num, ch_num, ch_title in book_structure:
            filename = f"book{book_num}_ch_{ch_num:02d}.xhtml"
            item_id = f"book{book_num}_ch_{ch_num:02d}"
            
            raw_filename = f"book{book_num}_ch_{ch_num:02d}_en.txt"
            txt_file = os.path.join(CHAPTERS_DIR, raw_filename)
            text = read_txt(txt_file)
            
            book_part_label = f"Book {book_num}"
            full_title = f"Chapter {ch_num}: {ch_title}"
            
            z.writestr(f"OEBPS/Text/{filename}", txt_to_html(text, full_title, book_part_label))
            manifest_items.append(f'<item id="{item_id}" href="Text/{filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{item_id}"/>')
            ncx_targets.append((f"{book_part_label} - {full_title}", f"Text/{filename}"))
            nav_targets.append((f"{book_part_label} - {full_title}", f"Text/{filename}"))

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
    <dc:title>A Tale of Two Cities</dc:title>
    <dc:creator>Charles Dickens</dc:creator>
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
  <docTitle><text>A Tale of Two Cities</text></docTitle>
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
