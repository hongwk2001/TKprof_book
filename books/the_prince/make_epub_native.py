"""
make_epub_native.py
Compiles the modernized edition of The Prince into an EPUB file directly using python's zipfile.
This generates a clean EPUB3 structure.
"""

import os
import zipfile
import uuid
import glob
from datetime import datetime, timezone
from xml.sax.saxutils import escape as escape_xml

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE = os.path.join(BASE_DIR, "the_prince.epub")

# ── CSS Style ─────────────────────────────────────────────────────────────────
STYLE = """
body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 1.1em;
    line-height: 1.6;
    margin: 1.5em 2em;
    color: #1a1a1a;
    background-color: #fdfaf5;
}

h1 {
    font-size: 1.8em;
    font-weight: bold;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1em;
    letter-spacing: 0.05em;
    color: #1a3c1a;
}

h2 {
    font-size: 1.4em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 1em;
    color: #2e5c2e;
}

p {
    margin: 0 0 1em 0;
    text-indent: 1.5em;
    word-break: break-word;
}

p.no-indent {
    text-indent: 0;
}

.separator {
    text-align: center;
    margin: 2em 0;
    color: #2e5c2e;
    font-size: 1.2em;
}
"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title):
    lines = text.split("\n")
    html_parts = [
        f"<?xml version='1.0' encoding='utf-8'?>",
        f"<!DOCTYPE html>",
        f"<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        f"<head>",
        f"  <title>{escape_xml(title)}</title>",
        f"  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        f"</head>",
        f"<body>",
        f"<h1>{escape_xml(title)}</h1>"
    ]
    
    # We skip header lines in text to avoid duplicate headers in HTML
    body_started = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip the title headers inside the text (which is the first line of the file)
        if not body_started:
            if line.lower().startswith("chapter ") or line.lower().startswith("dedication") or line.lower() == title.lower():
                continue
            body_started = True
            
        html_parts.append(f"<p>{escape_xml(line)}</p>")

    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

# ── Build EPUB natively ───────────────────────────────────────────────────────
def main():
    print("Building EPUB natively...")
    
    chapters = [] # list of dicts: {'id': '', 'href': '', 'title': '', 'content': ''}
    
    # 1. Introduction
    intro_txt_path = os.path.join(BASE_DIR, "introduction_en.txt")
    if os.path.exists(intro_txt_path):
        intro_text = read_txt(intro_txt_path)
        intro_html = txt_to_html(intro_text, "Introduction")
        chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': 'Introduction', 'content': intro_html})

    # 2. Chapters (including ch_00 Dedication)
    chapter_files = glob.glob(os.path.join(CHAPTERS_DIR, "ch_*.txt"))
    chapter_files.sort()
    
    for idx, txt_path in enumerate(chapter_files):
        filename = os.path.basename(txt_path)
        text = read_txt(txt_path)
        lines = text.split("\n")
        first_line = lines[0].strip()
        
        # Extract title from first line of text
        title = first_line
        
        # Extract index from filename
        ch_num_str = filename.split("_")[1] # e.g. '00' or '01'
        
        if ch_num_str == "00":
            uid = "dedication"
            fname = "Text/dedication.xhtml"
            title = "Dedication"
        else:
            uid = f"ch{ch_num_str}"
            fname = f"Text/{uid}.xhtml"
            
        ch_html = txt_to_html(text, title)
        chapters.append({'id': uid, 'href': fname, 'title': title, 'content': ch_html})

    # 3. Copyright
    copy_txt_path = os.path.join(BASE_DIR, "copyright_en.txt")
    if os.path.exists(copy_txt_path):
        copy_text = read_txt(copy_txt_path)
        copy_html = txt_to_html(copy_text, "Copyright & About This Edition")
        chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': 'Copyright & About This Edition', 'content': copy_html})

    book_uuid = f"urn:uuid:{uuid.uuid4()}"
    modified_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    cover_html = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
  <title>Cover</title>
  <style type="text/css">
    body { margin: 0; padding: 0; text-align: center; }
    img { max-width: 100%; height: auto; }
  </style>
</head>
<body>
  <img src="../Images/cover.jpg" alt="Cover" />
</body>
</html>"""

    # Build OPF Manifest
    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        f"    <dc:identifier id=\"pub-id\">{book_uuid}</dc:identifier>",
        "    <dc:title>The Prince</dc:title>",
        "    <dc:language>en</dc:language>",
        "    <dc:creator>Niccolò Machiavelli</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026-07-06</dc:date>",
        "    <dc:description>Niccolò Machiavelli's classic political treatise on statecraft, power, and leadership, carefully modernized for modern readers and language learners.</dc:description>",
        "    <dc:rights>Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>Philosophy</dc:subject>",
        "    <dc:subject>Political Science</dc:subject>",
        "    <dc:subject>History</dc:subject>",
        "    <dc:subject>Leadership</dc:subject>",
        f"    <meta property=\"dcterms:modified\">{modified_date}</meta>",
        "    <meta name=\"cover\" content=\"cover-image\"/>",
        "  </metadata>",
        "  <manifest>",
        "    <item id=\"cover-image\" href=\"Images/cover.jpg\" media-type=\"image/jpeg\" properties=\"cover-image\"/>",
        "    <item id=\"cover\" href=\"Text/cover.xhtml\" media-type=\"application/xhtml+xml\"/>",
        "    <item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\"/>",
        "    <item id=\"nav\" href=\"nav.xhtml\" media-type=\"application/xhtml+xml\" properties=\"nav\"/>",
        "    <item id=\"css\" href=\"Styles/main.css\" media-type=\"text/css\"/>"
    ]
    
    for ch in chapters:
        opf_parts.append(f"    <item id=\"{ch['id']}\" href=\"{ch['href']}\" media-type=\"application/xhtml+xml\"/>")
        
    opf_parts.append("  </manifest>")
    
    # Spine (Reading Order)
    opf_parts.append("  <spine toc=\"ncx\">")
    opf_parts.append("    <itemref idref=\"cover\"/>")
    for ch in chapters:
        opf_parts.append(f"    <itemref idref=\"{ch['id']}\"/>")
    opf_parts.append("  </spine>")
    opf_parts.append("</package>")
    opf_content = "\n".join(opf_parts)

    # Build NCX (legacy table of contents)
    ncx_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">",
        "  <head>",
        f"    <meta name=\"dtb:uid\" content=\"{book_uuid}\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle><text>The Prince</text></docTitle>",
        "  <navMap>"
    ]
    play_order = 1
    for ch in chapters:
        ncx_parts.append(f"    <navPoint id=\"{ch['id']}\" playOrder=\"{play_order}\">")
        ncx_parts.append(f"      <navLabel><text>{escape_xml(ch['title'])}</text></navLabel>")
        ncx_parts.append(f"      <content src=\"{ch['href']}\"/>")
        ncx_parts.append(f"    </navPoint>")
        play_order += 1
    ncx_parts.append("  </navMap>")
    ncx_parts.append("</ncx>")
    ncx_content = "\n".join(ncx_parts)

    # Build modern nav.xhtml
    nav_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head>",
        "  <title>Navigation</title>",
        "  <style type=\"text/css\">",
        "    nav { font-family: sans-serif; }",
        "    nav ol { list-style-type: none; padding-left: 1em; }",
        "    nav li { margin-bottom: 0.5em; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <nav epub:type=\"toc\" id=\"toc\">",
        "    <h1>Table of Contents</h1>",
        "    <ol>"
    ]
    for ch in chapters:
        nav_parts.append(f"      <li><a href=\"{ch['href']}\">{escape_xml(ch['title'])}</a></li>")
    nav_parts.append("    </ol>")
    nav_parts.append("  </nav>")
    nav_parts.append("</body>")
    nav_parts.append("</html>")
    nav_content = "\n".join(nav_parts)

    # Package into ZIP
    print(f"Creating EPUB file: {OUTPUT_FILE}...")
    with zipfile.ZipFile(OUTPUT_FILE, 'w', zipfile.ZIP_DEFLATED) as epub:
        # 1. mimetype MUST be the first file and UNCOMPRESSED
        epub.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        
        # 2. container.xml
        container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
        epub.writestr("META-INF/container.xml", container_xml)
        
        # 3. Assets under OEBPS
        epub.writestr("OEBPS/Styles/main.css", STYLE)
        epub.writestr("OEBPS/Text/cover.xhtml", cover_html)
        epub.writestr("OEBPS/toc.ncx", ncx_content)
        epub.writestr("OEBPS/nav.xhtml", nav_content)
        epub.writestr("OEBPS/content.opf", opf_content)
        
        # 4. Cover Image
        cover_img_path = os.path.join(BASE_DIR, "theprincecover.jpg")
        if os.path.exists(cover_img_path):
            epub.write(cover_img_path, "OEBPS/Images/cover.jpg")
            print("Cover image packaged.")
        else:
            print("Warning: theprincecover.jpg not found. EPUB created without a cover image.")
            
        # 5. Write chapter contents
        for ch in chapters:
            epub.writestr(f"OEBPS/{ch['href']}", ch['content'])
            
    print(f"Successfully compiled: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
