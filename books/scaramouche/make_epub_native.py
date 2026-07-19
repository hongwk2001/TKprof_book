"""
make_epub_native.py
Compiles Scaramouche into an English EPUB3 eBook directly using Python's zipfile.
"""

import os
import zipfile
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE = os.path.join(BASE_DIR, "scaramouche_en.epub")

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
    color: #2c1a0e;
}

h2 {
    font-size: 1.3em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.8em;
    margin-bottom: 1em;
    color: #5a3e28;
    text-transform: uppercase;
}

h3 {
    font-size: 1.1em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.2em;
    margin-bottom: 0.8em;
    color: #6a4e38;
}

p {
    margin: 0 0 1em 0;
    text-indent: 1.2em;
}

p.no-indent {
    text-indent: 0;
}
"""

def read_txt(path):
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
        html_parts.append(f"<h2>{book_part}</h2>")
        
    html_parts.append(f"<h1>{title}</h1>")
    
    first_p = True
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip header if duplicate
        if line.startswith("[") and line.endswith("]"):
            continue
        if line.startswith("Chapter ") or line.startswith("Book "):
            continue
            
        if first_p:
            html_parts.append(f"<p class=\"no-indent\">{line}</p>")
            first_p = False
        else:
            html_parts.append(f"<p>{line}</p>")
            
    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

def main():
    print("Building English EPUB natively...")
    
    chapters = []
    
    # 1. Introduction
    intro_txt = os.path.join(CHAPTERS_DIR, "introduction_en.txt")
    if os.path.exists(intro_txt):
        text = read_txt(intro_txt)
        html = txt_to_html(text, "About the Author & Book")
        chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': 'Introduction', 'content': html})
        
    # 2. Chapters 1-36 with Book divisions
    for i in range(1, 37):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        if not os.path.exists(txt_path):
            continue
            
        # Book Divisions
        book_part = None
        if i == 1:
            book_part = "Book I: The Robe"
        elif i == 10:
            book_part = "Book II: The Buskin"
        elif i == 21:
            book_part = "Book III: The Sword"
            
        title = f"Chapter {i}"
        text = read_txt(txt_path)
        
        # Read the actual chapter title if present in bracketed header
        first_line = text.split("\n")[0].strip()
        if first_line.startswith("[") and first_line.endswith("]"):
            title_text = first_line[1:-1]
            if " - " in title_text:
                title_text = title_text.split(" - ", 1)[1]
            if ":" in title_text:
                title_text = title_text.split(":", 1)[1].strip()
            title = f"Chapter {i}: {title_text}"
            
        ch_html = txt_to_html(text, title, book_part)
        uid = f"ch{i:02d}"
        fname = f"Text/ch{i:02d}.xhtml"
        chapters.append({'id': uid, 'href': fname, 'title': title, 'content': ch_html})
        
    # 3. Copyright
    copy_txt = os.path.join(CHAPTERS_DIR, "copyright_en.txt")
    if os.path.exists(copy_txt):
        text = read_txt(copy_txt)
        html = txt_to_html(text, "Copyright & Editorial Notes")
        chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': 'Copyright & Editorial Notes', 'content': html})
        
    book_uuid = f"urn:uuid:{uuid.uuid4()}"
    modified_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Pack Zip
    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as z:
        # mimetype MUST be first and uncompressed
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        
        # Container
        container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
        z.writestr("META-INF/container.xml", container_xml)
        
        # Styles
        z.writestr("OEBPS/Styles/main.css", STYLE)
        
        # Write Chapters
        for ch in chapters:
            z.writestr(f"OEBPS/{ch['href']}", ch['content'])
            
        # OPF Metadata
        manifest_items = []
        spine_items = []
        
        manifest_items.append('<item id="css" href="Styles/main.css" media-type="text/css"/>')
        
        for ch in chapters:
            manifest_items.append(f'<item id="{ch["id"]}" href="{ch["href"]}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{ch["id"]}"/>')
            
        manifest_xml = "\n    ".join(manifest_items)
        spine_xml = "\n    ".join(spine_items)
        
        opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{book_uuid}</dc:identifier>
    <dc:title>Scaramouche: Modern English Edition</dc:title>
    <dc:creator>Rafael Sabatini</dc:creator>
    <dc:language>en</dc:language>
    <dc:publisher>TKPROF LLC</dc:publisher>
    <meta property="dcterms:modified">{modified_date}</meta>
  </metadata>
  <manifest>
    {manifest_xml}
  </manifest>
  <spine>
    {spine_xml}
  </spine>
</package>"""
        z.writestr("OEBPS/content.opf", opf)
        
        # TOC NCX (for compatibility)
        nav_points = []
        for idx, ch in enumerate(chapters):
            nav_points.append(f"""    <navPoint id="{ch['id']}" playOrder="{idx+1}">
      <navLabel><text>{ch['title']}</text></navLabel>
      <content src="{ch['href']}"/>
    </navPoint>""")
            
        nav_points_xml = "\n".join(nav_points)
        ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book_uuid}"/>
    <meta name="dtb:depth" content="1"/>
  </head>
  <docTitle><text>Scaramouche: Modern English Edition</text></docTitle>
  <navMap>
    {nav_points_xml}
  </navMap>
</ncx>"""
        z.writestr("OEBPS/toc.ncx", ncx)
        
    print(f"English EPUB compiled successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
