"""
make_epub_native_en.py
Compiles H. G. Wells' Tono-Bungay (Modernized English Edition) into an EPUB3 eBook.
"""

import os
import zipfile
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE = os.path.join(BASE_DIR, "tono_bungay_en.epub")

BOOK_TITLES = {
    1: "Book 1: The Days Before Tono-Bungay Was Invented",
    2: "Book 2: The Rise of Tono-Bungay",
    3: "Book 3: The Great Days of Tono-Bungay",
    4: "Book 4: The Aftermath of Tono-Bungay"
}

STYLE = """
body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 1.05em;
    line-height: 1.6;
    margin: 1.5em 2em;
    color: #111111;
}

h1 {
    font-size: 1.8em;
    font-weight: bold;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1em;
    color: #1a2a3a;
}

h2 {
    font-size: 1.3em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 1em;
    color: #2c3e50;
}

p {
    margin: 0 0 1em 0;
    text-indent: 1.2em;
}

p.no-indent {
    text-indent: 0;
}

.book-title {
    text-align: center;
    margin-top: 4em;
    margin-bottom: 4em;
}

.book-title h1 {
    font-size: 2.2em;
    color: #1a2a3a;
}

blockquote {
    margin: 1em 0 1em 1.5em;
    padding: 0.6em 1em;
    border-left: 4px solid #2c3e50;
    background-color: #f8f9fa;
    font-style: italic;
    color: #333333;
}
"""

import html

def read_txt(path):
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    escaped_title = html.escape(title)
    h1_title = escaped_title.replace(" - ", "<br/>")
    
    html_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head>",
        f"  <title>{escaped_title}</title>",
        "  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        "</head>",
        "<body>",
        f"  <h1>{h1_title}</h1>"
    ]
    
    first = True
    for para in lines:
        if para.startswith("#"):
            html_parts.append(f"  <h2>{html.escape(para.lstrip('#').strip())}</h2>")
        else:
            cls = " class=\"no-indent\"" if first else ""
            html_parts.append(f"  <p{cls}>{html.escape(para)}</p>")
            first = False
            
    html_parts.extend(["</body>", "</html>"])
    return "\n".join(html_parts)

def build_epub():
    book_id = f"urn:uuid:{uuid.uuid4()}"
    pub_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    manifest_items = []
    spine_items = []
    toc_ncx_items = []
    nav_html_items = []
    
    # Cover image support
    cover_path = os.path.join(BASE_DIR, "cover_en.jpg")
    if not os.path.exists(cover_path):
        cover_path = os.path.join(BASE_DIR, "cover.jpg")
    has_cover = os.path.exists(cover_path)

    if has_cover:
        manifest_items.append('<item id="cover-image" href="Images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>')
        manifest_items.append('<item id="cover" href="Text/cover.xhtml" media-type="application/xhtml+xml"/>')
        spine_items.append('<itemref idref="cover"/>')

    # CSS
    manifest_items.append('<item id="css" href="Styles/main.css" media-type="text/css"/>')
    
    chapter_index = 1
    
    chapters_structure = [
        (1, [1, 2, 3]),
        (2, [1, 2, 3, 4]),
        (3, [1, 2, 3, 4]),
        (4, [1, 2, 3])
    ]

    html_files = {}

    if has_cover:
        cover_xhtml = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>Cover</title>
  <style type="text/css">
    body { margin: 0; padding: 0; text-align: center; background-color: #000; }
    img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
  </style>
</head>
<body>
  <div>
    <img src="../Images/cover.jpg" alt="Cover"/>
  </div>
</body>
</html>"""
        html_files["OEBPS/Text/cover.xhtml"] = cover_xhtml

    for b_num, ch_list in chapters_structure:
        book_heading = BOOK_TITLES[b_num]
        
        for c_num in ch_list:
            filepath = os.path.join(CHAPTERS_DIR, f"book{b_num}", f"book{b_num}_ch{c_num:02d}_en.txt")
            text = read_txt(filepath)
            
            if not text:
                continue
                
            lines = text.split('\n')
            if lines and lines[0].startswith('#'):
                chapter_specific_title = lines[0].lstrip('#').strip()
                ch_title = f"{book_heading} - {chapter_specific_title}"
                text = '\n'.join(lines[1:]).strip()
            else:
                ch_title = f"{book_heading} - Chapter {c_num}"

            item_id = f"ch_{b_num}_{c_num}"
            filename = f"ch_{b_num}_{c_num}.xhtml"
            
            html_content = txt_to_html(text, ch_title)
            html_files[f"OEBPS/Text/{filename}"] = html_content
            
            manifest_items.append(f'<item id="{item_id}" href="Text/{filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{item_id}"/>')
            
            toc_ncx_items.append(f'''  <navPoint id="{item_id}" playOrder="{chapter_index}">
    <navLabel><text>{html.escape(ch_title)}</text></navLabel>
    <content src="Text/{filename}"/>
  </navPoint>''')
            
            nav_html_items.append(f'    <li><a href="{filename}">{html.escape(ch_title)}</a></li>')
            chapter_index += 1

    manifest_str = "\n    ".join(manifest_items)
    spine_str = "\n    ".join(spine_items)
    toc_ncx_str = "\n".join(toc_ncx_items)
    nav_html_str = "\n".join(nav_html_items)

    # OPF
    opf_content = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">{book_id}</dc:identifier>
    <dc:title>Tono-Bungay (Modernized Edition)</dc:title>
    <dc:language>en</dc:language>
    <dc:creator>H. G. Wells</dc:creator>
    <dc:publisher>TKprof Publishing</dc:publisher>
    <dc:date>{pub_date}</dc:date>
    <meta property="dcterms:modified">{pub_date}</meta>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="nav" href="Text/nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    {manifest_str}
  </manifest>
  <spine toc="ncx">
    {spine_str}
  </spine>
</package>'''

    # NCX
    ncx_content = f'''<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book_id}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>Tono-Bungay (Modernized Edition)</text></docTitle>
  <navMap>
{toc_ncx_str}
  </navMap>
</ncx>'''

    # Nav HTML
    nav_html_content = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>Table of Contents</title>
  <link rel="stylesheet" href="../Styles/main.css" type="text/css"/>
</head>
<body>
  <h1>Table of Contents</h1>
  <nav epub:type="toc" id="toc">
    <ol>
{nav_html_str}
    </ol>
  </nav>
</body>
</html>'''

    with zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED) as zf:
        # mimetype (must be uncompressed)
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        
        # META-INF/container.xml
        container_xml = '''<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''
        zf.writestr("META-INF/container.xml", container_xml)
        
        zf.writestr("OEBPS/content.opf", opf_content)
        zf.writestr("OEBPS/toc.ncx", ncx_content)
        zf.writestr("OEBPS/Styles/main.css", STYLE)
        zf.writestr("OEBPS/Text/nav.xhtml", nav_html_content)
        
        if has_cover:
            with open(cover_path, "rb") as img_f:
                zf.writestr("OEBPS/Images/cover.jpg", img_f.read())

        for path, content in html_files.items():
            zf.writestr(path, content)
            
    print(f"Successfully generated EPUB: {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE)} bytes)")

if __name__ == "__main__":
    build_epub()
