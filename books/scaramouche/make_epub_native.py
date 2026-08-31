"""
make_epub_native.py
Compiles Scaramouche into an English EPUB3 eBook directly using Python's zipfile.
"""

import os
import zipfile
import uuid
import html
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
    escaped_title = html.escape(title)
    html_parts = [
        f"<?xml version='1.0' encoding='utf-8'?>",
        f"<!DOCTYPE html>",
        f"<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        f"<head>",
        f"  <title>{escaped_title}</title>",
        f"  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        f"</head>",
        f"<body>",
    ]
    
    if book_part:
        html_parts.append(f"<h2>{html.escape(book_part)}</h2>")
        
    html_parts.append(f"<h1>{escaped_title}</h1>")
    
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
            
        escaped_line = html.escape(line)
        if first_p:
            html_parts.append(f"<p class=\"no-indent\">{escaped_line}</p>")
            first_p = False
        else:
            html_parts.append(f"<p>{escaped_line}</p>")
            
    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

def compile_book(book_num):
    book_titles = {
        1: "Scaramouche, Book I: The Robe",
        2: "Scaramouche, Book II: The Buskin",
        3: "Scaramouche, Book III: The Sword"
    }
    output_filename = f"scaramouche_book{book_num}_en.epub"
    output_filepath = os.path.join(BASE_DIR, output_filename)
    
    print(f"Building {book_titles[book_num]} natively...")
    
    chapters = []
    
    # 0. Cover Page
    cover_filename = f"cover_book{book_num}_final.jpg"
    cover_filepath = os.path.join(BASE_DIR, cover_filename)
    has_cover = os.path.exists(cover_filepath)
    if has_cover:
        cover_html = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>Cover</title>
  <style type="text/css">
    body { margin: 0; padding: 0; text-align: center; background-color: #000000; }
    img { max-width: 100%; max-height: 100%; height: auto; }
  </style>
</head>
<body>
  <div style="text-align: center; padding: 0; margin: 0;">
    <img src="../Images/cover.jpg" alt="Cover"/>
  </div>
</body>
</html>"""
        chapters.append({'id': 'cover', 'href': 'Text/cover.xhtml', 'title': 'Cover', 'content': cover_html})

    # 1. Introduction (Only in Book I)
    if book_num == 1:
        intro_txt = os.path.join(CHAPTERS_DIR, "introduction_en.txt")
        if os.path.exists(intro_txt):
            text = read_txt(intro_txt)
            intro_html = txt_to_html(text, "About the Author & Book")
            chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': 'Introduction', 'content': intro_html})
            
    import json
    metadata_path = os.path.join(CHAPTERS_DIR, "metadata.json")
    metadata = {}
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    # 2. Chapters from book folder
    book_dir = os.path.join(CHAPTERS_DIR, f"book_{book_num}")
    if not os.path.exists(book_dir):
        print(f"Directory {book_dir} not found. Skipping Book {book_num}.")
        return

    inner_ch = 1
    while True:
        inner_ch_str = str(inner_ch).zfill(2)
        txt_path = os.path.join(book_dir, f"ch_{inner_ch_str}_en.txt")
        if not os.path.exists(txt_path):
            break
            
        title = f"Chapter {inner_ch}"
        text = read_txt(txt_path)
        
        # Read the actual chapter title from metadata
        book_key = f"book_{book_num}"
        ch_key = f"ch_{inner_ch_str}"
        title_text = metadata.get(book_key, {}).get(ch_key, {}).get("title_en", "")
        if title_text:
            title = f"Chapter {inner_ch}: {title_text}"
            
        # Add book part header to Chapter 1 of each volume
        book_part = None
        if inner_ch == 1:
            if book_num == 1:
                book_part = "Book I: The Robe"
            elif book_num == 2:
                book_part = "Book II: The Buskin"
            elif book_num == 3:
                book_part = "Book III: The Sword"

        ch_html = txt_to_html(text, title, book_part)
        uid = f"ch{inner_ch_str}"
        fname = f"Text/ch{inner_ch_str}.xhtml"
        chapters.append({'id': uid, 'href': fname, 'title': title, 'content': ch_html})
        
        inner_ch += 1
        
    # 3. Copyright (In all three books)
    copy_txt = os.path.join(CHAPTERS_DIR, "copyright_en.txt")
    if os.path.exists(copy_txt):
        text = read_txt(copy_txt)
        copy_html = txt_to_html(text, "Copyright & Editorial Notes")
        chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': 'Copyright & Editorial Notes', 'content': copy_html})
        
    book_uuid = f"urn:uuid:{uuid.uuid4()}"
    modified_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Pack Zip
    with zipfile.ZipFile(output_filepath, 'w', zipfile.ZIP_DEFLATED) as z:
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
            
        # Write Cover Image
        if has_cover:
            with open(cover_filepath, "rb") as cf:
                z.writestr("OEBPS/Images/cover.jpg", cf.read())
            
        # Write EPUB3 HTML Nav Document
        nav_items_xml = "\n        ".join([f'<li><a href="{ch["href"]}">{html.escape(ch["title"])}</a></li>' for ch in chapters])
        nav_html = f"""<?xml version="1.0" encoding="utf-8"?>
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
        {nav_items_xml}
    </ol>
  </nav>
</body>
</html>"""
        z.writestr("OEBPS/Text/nav.xhtml", nav_html)

        # OPF Metadata
        manifest_items = []
        spine_items = []
        
        manifest_items.append('<item id="css" href="Styles/main.css" media-type="text/css"/>')
        manifest_items.append('<item id="nav" href="Text/nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
        
        if has_cover:
            manifest_items.append('<item id="cover-image" href="Images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>')
        
        for ch in chapters:
            manifest_items.append(f'<item id="{ch["id"]}" href="{ch["href"]}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{ch["id"]}"/>')
            
        manifest_xml = "\n    ".join(manifest_items)
        spine_xml = "\n    ".join(spine_items)
        
        opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{book_uuid}</dc:identifier>
    <dc:title>{html.escape(book_titles[book_num])} - Modern English Edition</dc:title>
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
      <navLabel><text>{html.escape(ch['title'])}</text></navLabel>
      <content src="{ch['href']}"/>
    </navPoint>""")
            
        nav_points_xml = "\n".join(nav_points)
        ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book_uuid}"/>
    <meta name="dtb:depth" content="1"/>
  </head>
  <docTitle><text>{html.escape(book_titles[book_num])} - Modern English Edition</text></docTitle>
  <navMap>
    {nav_points_xml}
  </navMap>
</ncx>"""
        z.writestr("OEBPS/toc.ncx", ncx)
        
    print(f"{book_titles[book_num]} compiled successfully: {output_filepath}")

def main():
    print("Building English EPUBs natively for all 3 books...")
    for b in [1, 2, 3]:
        compile_book(b)

if __name__ == "__main__":
    main()
