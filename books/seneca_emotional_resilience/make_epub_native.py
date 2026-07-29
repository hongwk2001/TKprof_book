"""
make_epub_native.py
Compiles Seneca's Stoic Treatises on Emotional Resilience into an English EPUB3 eBook directly using Python's zipfile.
"""

import os
import zipfile
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE = os.path.join(BASE_DIR, "seneca_emotional_resilience_en.epub")

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
        # Skip the chapter bracket title if it is the first line
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

    intro_text = read_txt(os.path.join(BASE_DIR, "introduction_en.txt"))

    # Gather Chapters
    chapters = []
    
    # 1. On Anger
    # Book I (21 chapters)
    for i in range(1, 22):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(CHAPTERS_DIR, "1.on_anger", f"on_anger_book1_ch{ch_str}_en.txt")
        text = read_txt(txt_file)
        chapters.append(("anger_b1_ch" + ch_str, f"on_anger_b1_ch{ch_str}.xhtml", f"On Anger Book 1 - Chapter {i}", text, "On Anger (Book 1)"))
        
    # Book II (36 chapters)
    for i in range(1, 37):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(CHAPTERS_DIR, "1.on_anger", f"on_anger_book2_ch{ch_str}_en.txt")
        text = read_txt(txt_file)
        chapters.append(("anger_b2_ch" + ch_str, f"on_anger_b2_ch{ch_str}.xhtml", f"On Anger Book 2 - Chapter {i}", text, "On Anger (Book 2)"))
        
    # Book III (43 chapters)
    for i in range(1, 44):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(CHAPTERS_DIR, "1.on_anger", f"on_anger_book3_ch{ch_str}_en.txt")
        text = read_txt(txt_file)
        chapters.append(("anger_b3_ch" + ch_str, f"on_anger_b3_ch{ch_str}.xhtml", f"On Anger Book 3 - Chapter {i}", text, "On Anger (Book 3)"))

    # 2. Tranquillity of Mind (17 chapters)
    for i in range(1, 18):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(CHAPTERS_DIR, "2.tranquillity_of_mind", f"tranquillity_ch{ch_str}_en.txt")
        text = read_txt(txt_file)
        chapters.append(("tranquillity_ch" + ch_str, f"tranquillity_ch{ch_str}.xhtml", f"On Tranquillity of Mind - Chapter {i}", text, "On Tranquillity of Mind"))

    # 3. Constancy (19 chapters)
    for i in range(1, 20):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(CHAPTERS_DIR, "3.constancy", f"constancy_ch{ch_str}_en.txt")
        text = read_txt(txt_file)
        chapters.append(("constancy_ch" + ch_str, f"constancy_ch{ch_str}.xhtml", f"On Constancy - Chapter {i}", text, "On Constancy"))

    # 4. Providence (6 chapters)
    for i in range(1, 7):
        ch_str = str(i).zfill(2)
        txt_file = os.path.join(CHAPTERS_DIR, "4.providence", f"providence_ch{ch_str}_en.txt")
        text = read_txt(txt_file)
        chapters.append(("providence_ch" + ch_str, f"providence_ch{ch_str}.xhtml", f"On Providence - Chapter {i}", text, "On Providence"))

    with zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED) as z:
        # Write mimetype first with no compression
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

        # Write Introduction
        if intro_text:
            z.writestr("OEBPS/Text/intro.xhtml", txt_to_html(intro_text, "Introduction"))
            manifest_items.append('<item id="intro" href="Text/intro.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="intro"/>')
            ncx_targets.append(("Introduction", "Text/intro.xhtml"))
            nav_targets.append(("Introduction", "Text/intro.xhtml"))

        # Write Chapters and Parts
        current_part = None
        part_index = 0
        for item_id, filename, title, text, part_name in chapters:
            if part_name != current_part:
                current_part = part_name
                part_index += 1
                part_id = f"part{part_index}_intro"
                part_filename = f"part{part_index}_intro.xhtml"
                
                part_divider = f"""<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{part_name}</title>
  <link rel="stylesheet" href="../Styles/main.css" type="text/css"/>
</head>
<body>
  <div class="part-title">
    <h1>PART {part_index}</h1>
    <h2>{part_name}</h2>
  </div>
</body>
</html>"""
                z.writestr(f"OEBPS/Text/{part_filename}", part_divider)
                manifest_items.append(f'<item id="{part_id}" href="Text/{part_filename}" media-type="application/xhtml+xml"/>')
                spine_items.append(f'<itemref idref="{part_id}"/>')
                ncx_targets.append((f"PART {part_index}: {part_name}", f"Text/{part_filename}"))
                nav_targets.append((f"PART {part_index}: {part_name}", f"Text/{part_filename}"))

            # Write chapter content
            z.writestr(f"OEBPS/Text/{filename}", txt_to_html(text, title))
            manifest_items.append(f'<item id="{item_id}" href="Text/{filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{item_id}"/>')
            ncx_targets.append((f"  {title}", f"Text/{filename}"))
            nav_targets.append((f"  {title}", f"Text/{filename}"))

        # Write Nav/TOC files
        nav_html = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<!DOCTYPE html>',
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">',
            '<head>',
            '  <title>Navigation</title>',
            '  <link rel="stylesheet" href="Styles/main.css" type="text/css"/>',
            '</head>',
            '<body>',
            '  <nav epub:type="toc" id="toc">',
            '    <h1>Table of Contents</h1>',
            '    <ol>'
        ]
        for name, target in nav_targets:
            # Shift path for nav.xhtml in root of OEBPS
            clean_target = target.replace("Text/", "Text/")
            if name.startswith("PART") or name == "Introduction":
                nav_html.append(f'      <li><a href="{clean_target}">{name}</a></li>')
            else:
                nav_html.append(f'      <li style="margin-left: 20px;"><a href="{clean_target}">{name.strip()}</a></li>')
        nav_html.extend([
            '    </ol>',
            '  </nav>',
            '</body>',
            '</html>'
        ])
        z.writestr("OEBPS/nav.xhtml", "\n".join(nav_html))

        # NCX TOC
        ncx_xml = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">',
            '  <head>',
            f'    <meta name="dtb:uid" content="{book_id}"/>',
            '    <meta name="dtb:depth" content="2"/>',
            '    <meta name="dtb:totalPageCount" content="0"/>',
            '    <meta name="dtb:maxPageNumber" content="0"/>',
            '  </head>',
            '  <docTitle>',
            '    <text>Stoic Treatises on Emotional Resilience: Modernized Edition</text>',
            '  </docTitle>',
            '  <navMap>'
        ]
        for idx, (name, target) in enumerate(ncx_targets, 1):
            ncx_xml.extend([
                f'    <navPoint id="navpoint-{idx}" playOrder="{idx}">',
                f'      <navLabel><text>{name}</text></navLabel>',
                f'      <content src="{target}"/>',
                '    </navPoint>'
            ])
        ncx_xml.extend([
            '  </navMap>',
            '</ncx>'
        ])
        z.writestr("OEBPS/toc.ncx", "\n".join(ncx_xml))

        # content.opf
        manifest_str = "\n    ".join(manifest_items)
        spine_str = "\n    ".join(spine_items)
        
        content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">{book_id}</dc:identifier>
    <dc:title>Stoic Treatises on Emotional Resilience: Modernized Edition</dc:title>
    <dc:creator id="creator">Lucius Annaeus Seneca</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>TKPROF LLC</dc:publisher>
    <dc:date>{pub_date}</dc:date>
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

    print(f"EPUB created successfully at: {OUTPUT_FILE}")

if __name__ == "__main__":
    build_epub()
