import os
import zipfile
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_FILE = os.path.join(BASE_DIR, "dracula_bilingual.epub")

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

p.eng {
    color: #1a1a1a;
    margin-bottom: 0.2em;
}

p.kor {
    color: #2c3e50;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    margin-top: 0;
    margin-bottom: 1.5em;
}

.cover-img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
}
"""

def read_paragraphs(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        # Split by blank lines to get paragraphs
        raw = f.read().strip()
        if not raw:
            return []
        paras = [p.strip() for p in raw.split("\n\n") if p.strip()]
        return paras

def txt_to_bilingual_html(en_paras, ko_paras, title):
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
    
    # Check for headers in the first paragraph
    first_en = en_paras[0] if en_paras else title
    first_ko = ko_paras[0] if ko_paras else title
    
    import re
    # Strip ID from chapter title if present
    pid_match_en = re.match(r'^(\[P\d+\])\s*', first_en)
    if pid_match_en:
        first_en = first_en[len(pid_match_en.group(1)):].strip()
    pid_match_ko = re.match(r'^(\[P\d+\])\s*', first_ko)
    if pid_match_ko:
        first_ko = first_ko[len(pid_match_ko.group(1)):].strip()
    
    # Assume the first paragraph is the chapter title (e.g. CHAPTER I)
    html_parts.append(f"  <h2>{first_en}<br/><span style='font-size: 0.8em; color: #2c3e50;'>{first_ko}</span></h2>")
    
    for i in range(1, len(en_paras)):
        en_p = en_paras[i]
        ko_p = ko_paras[i]
        
        # Extract paragraph ID if present (e.g., [P001])
        pid_match = re.match(r'^(\[P\d+\])\s*', en_p)
        if pid_match:
            pid = pid_match.group(1)
            en_p = en_p[len(pid):].strip()
            # Also strip from Korean if present
            if ko_p.startswith(pid):
                ko_p = ko_p[len(pid):].strip()
            elif re.match(r'^(\[P\d+\])\s*', ko_p):
                # Fallback if ko_p starts with a different pid for some reason
                ko_p = re.sub(r'^\[P\d+\]\s*', '', ko_p)

        html_parts.append(f"  <p class=\"eng\">{en_p}</p>")
        html_parts.append(f"  <p class=\"kor\">{ko_p}</p>")

    html_parts.append("</body>\n</html>")
    return "\n".join(html_parts)

def build_epub():
    book_id = f"urn:uuid:{uuid.uuid4()}"
    pub_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    cover_path = os.path.join(BASE_DIR, "cover.jpg")
    has_cover = os.path.exists(cover_path)

    chapters_data = []
    
    # Process 27 chapters
    for i in range(1, 28):
        en_file = os.path.join(CHAPTERS_DIR, f"ch{i:02d}_en.txt")
        ko_file = os.path.join(CHAPTERS_DIR, f"ch{i:02d}_ko.txt")
        
        if not os.path.exists(en_file) or not os.path.exists(ko_file):
            print(f"Skipping Chapter {i} (missing files)")
            continue
            
        en_paras = read_paragraphs(en_file)
        ko_paras = read_paragraphs(ko_file)
        
        if len(en_paras) != len(ko_paras):
            print(f"ERROR: Paragraph count mismatch in Chapter {i}")
            print(f"  English paragraphs: {len(en_paras)}")
            print(f"  Korean paragraphs: {len(ko_paras)}")
            continue
            
        title = f"Chapter {i}"
        filename = f"ch{i:02d}.xhtml"
        item_id = f"ch{i:02d}"
        
        chapters_data.append((filename, item_id, title, en_paras, ko_paras))

    if not chapters_data:
        print("No valid chapters found. Aborting.")
        return

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

        for filename, item_id, title, en_paras, ko_paras in chapters_data:
            html_content = txt_to_bilingual_html(en_paras, ko_paras, title)
            z.writestr(f"OEBPS/Text/{filename}", html_content)
            manifest_items.append(f'<item id="{item_id}" href="Text/{filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{item_id}"/>')
            ncx_targets.append((title, f"Text/{filename}"))
            nav_targets.append((title, f"Text/{filename}"))

        manifest_str = "\n    ".join(manifest_items)
        spine_str = "\n    ".join(spine_items)

        content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">{book_id}</dc:identifier>
    <dc:title>Dracula (Bilingual Parallel Edition)</dc:title>
    <dc:creator>Bram Stoker</dc:creator>
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
  <docTitle><text>Dracula</text></docTitle>
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
