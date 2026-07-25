"""
make_epub.py
Compiles The Enchanted April into an EPUB file directly using python's zipfile.
This generates a clean EPUB3 structure.
"""

import os
import zipfile
import uuid
from datetime import datetime, timezone

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE   = os.path.join(BASE_DIR, "the_enchanted_april.epub")

# ── CSS Style ─────────────────────────────────────────────────────────────────
STYLE = """
body {
    font-family: 'Lora', Georgia, serif;
    font-size: 1em;
    line-height: 1.6;
    margin: 1.5em 2em;
    color: #2c2c2c;
    background-color: #fdfdfd;
}

h1 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.8em;
    font-weight: bold;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1em;
    color: #4a2f13;
}

h2 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.3em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 1em;
    color: #5d4022;
}

p {
    margin: 0 0 1em 0;
    text-indent: 1.5em;
}

p.no-indent {
    text-indent: 0;
}
"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def escape_xml(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title):
    escaped_title = escape_xml(title)
    lines = text.split("\n")
    html_parts = [
        f"<?xml version='1.0' encoding='utf-8'?>",
        f"<!DOCTYPE html>",
        f"<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        f"<head>",
        f"  <title>{escaped_title}</title>",
        f"  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        f"</head>",
        f"<body>",
        f"<h1>{escaped_title}</h1>"
    ]
    
    is_first_p = True
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Skip the chapter title if it's already the first line
        if line == title:
            continue
        
        # Check for headings or regular paragraphs
        if line.startswith("[") and line.endswith("]"):
            html_parts.append(f"<h2>{escape_xml(line[1:-1])}</h2>")
            is_first_p = True
        else:
            # First paragraph after a heading usually has no text-indent
            escaped_line = escape_xml(line)
            if is_first_p:
                html_parts.append(f"<p class=\"no-indent\">{escaped_line}</p>")
                is_first_p = False
            else:
                html_parts.append(f"<p>{escaped_line}</p>")

    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

# ── Build EPUB natively ───────────────────────────────────────────────────────
def main():
    print("Building EPUB natively...")
    
    chapters = [] # list of dicts: {'id': '', 'href': '', 'title': '', 'content': ''}
    
    # 1. Introduction
    intro_txt_path = os.path.join(BASE_DIR, "overview_en.txt")
    if os.path.exists(intro_txt_path):
        intro_text = read_txt(intro_txt_path)
        intro_html = txt_to_html(intro_text, "A Note to the Reader")
        chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': 'A Note to the Reader', 'content': intro_html})

    # 2. Chapters 1-22
    for i in range(1, 23):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        if not os.path.exists(txt_path):
            continue
        title = f"Chapter {i}"
        text = read_txt(txt_path)
        
        ch_html = txt_to_html(text, title)
        uid = f"ch{i:02d}"
        fname = f"Text/ch{i:02d}.xhtml"
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
    body { margin: 0; padding: 0; text-align: center; background-color: #ffffff; }
    img { max-width: 100%; height: auto; }
  </style>
</head>
<body>
  <img src="../Images/cover.png" alt="Cover" />
</body>
</html>"""

    # Build OPF Manifest
    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        f"    <dc:identifier id=\"pub-id\">{book_uuid}</dc:identifier>",
        "    <dc:title>The Enchanted April</dc:title>",
        "    <dc:language>en</dc:language>",
        "    <dc:creator>Elizabeth von Arnim</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026-07-07</dc:date>",
        "    <dc:description>Four very different Englishwomen rent a medieval Italian castle on the Mediterranean for a month to escape their dreary lives and husbands, and find themselves transformed by the beauty, flowers, and sunshine of Italy.</dc:description>",
        "    <dc:rights>Adapted and Modernized Edition Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>Fiction</dc:subject>",
        "    <dc:subject>Classics</dc:subject>",
        "    <dc:subject>Modernized</dc:subject>",
        f"    <meta property=\"dcterms:modified\">{modified_date}</meta>",
        "    <meta name=\"cover\" content=\"cover-image\"/>",
        "  </metadata>",
        "  <manifest>",
        "    <item id=\"cover-image\" href=\"Images/cover.png\" media-type=\"image/png\" properties=\"cover-image\"/>",
        "    <item id=\"cover\" href=\"Text/cover.xhtml\" media-type=\"application/xhtml+xml\"/>",
        "    <item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\"/>",
        "    <item id=\"nav\" href=\"nav.xhtml\" media-type=\"application/xhtml+xml\" properties=\"nav\"/>",
        "    <item id=\"css\" href=\"Styles/main.css\" media-type=\"text/css\"/>"
    ]
    
    for ch in chapters:
        opf_parts.append(f"    <item id=\"{ch['id']}\" href=\"{ch['href']}\" media-type=\"application/xhtml+xml\"/>")
        
    opf_parts.append("  </manifest>")
    opf_parts.append("  <spine toc=\"ncx\">")
    opf_parts.append("    <itemref idref=\"cover\"/>")
    for ch in chapters:
        opf_parts.append(f"    <itemref idref=\"{ch['id']}\"/>")
    opf_parts.append("  </spine>")
    opf_parts.append("</package>")
    opf_content = "\n".join(opf_parts)

    # Build NCX (EPUB 2 TOC)
    ncx_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">",
        "  <head>",
        "    <meta name=\"dtb:uid\" content=\"tkprof-enchanted-april-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle>",
        "    <text>The Enchanted April</text>",
        "  </docTitle>",
        "  <navMap>"
    ]
    play_order = 1
    ncx_parts.append(f"    <navPoint id=\"navPoint-{play_order}\" playOrder=\"{play_order}\">")
    ncx_parts.append(f"      <navLabel><text>Cover</text></navLabel>")
    ncx_parts.append(f"      <content src=\"Text/cover.xhtml\"/>")
    ncx_parts.append(f"    </navPoint>")
    
    for ch in chapters:
        play_order += 1
        escaped_t = escape_xml(ch['title'])
        ncx_parts.append(f"    <navPoint id=\"navPoint-{play_order}\" playOrder=\"{play_order}\">")
        ncx_parts.append(f"      <navLabel><text>{escaped_t}</text></navLabel>")
        ncx_parts.append(f"      <content src=\"{ch['href']}\"/>")
        ncx_parts.append(f"    </navPoint>")
        
    ncx_parts.append("  </navMap>")
    ncx_parts.append("</ncx>")
    ncx_content = "\n".join(ncx_parts)

    # Build HTML5 Navigation (EPUB 3 TOC)
    nav_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head>",
        "  <title>Table of Contents</title>",
        "  <style type=\"text/css\">",
        "    body { font-family: sans-serif; margin: 2em; }",
        "    nav ol { list-style-type: none; padding-left: 0; }",
        "    nav li { margin-bottom: 0.5em; }",
        "    nav a { text-decoration: none; color: #4a2f13; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <nav epub:type=\"toc\" id=\"toc\">",
        "    <h1>Table of Contents</h1>",
        "    <ol>",
        "      <li><a href=\"Text/cover.xhtml\">Cover</a></li>"
    ]
    
    for ch in chapters:
        escaped_t = escape_xml(ch['title'])
        nav_parts.append(f"      <li><a href=\"{ch['href']}\">{escaped_t}</a></li>")
        
    nav_parts.append("    </ol>")
    nav_parts.append("  </nav>")
    nav_parts.append("</body>")
    nav_parts.append("</html>")
    nav_content = "\n".join(nav_parts)

    # Write container.xml
    container_content = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""

    # 4. Zip all components directly to output file
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        
    with zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED) as epub:
        # Write mimetype first, uncompressed
        epub.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        
        # Meta-inf
        epub.writestr("META-INF/container.xml", container_content)
        
        # OEBPS Assets
        epub.write(os.path.join(BASE_DIR, "cover.png"), "OEBPS/Images/cover.png")
        epub.writestr("OEBPS/Text/cover.xhtml", cover_html)
        epub.writestr("OEBPS/Styles/main.css", STYLE)
        epub.writestr("OEBPS/content.opf", opf_content)
        epub.writestr("OEBPS/toc.ncx", ncx_content)
        epub.writestr("OEBPS/nav.xhtml", nav_content)
        
        # Chapter Content
        for ch in chapters:
            epub.writestr(f"OEBPS/{ch['href']}", ch['content'])
            
    print(f"EPUB created successfully at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
