"""
make_epub_native.py
Compiles Meditations into an EPUB file directly using python's zipfile.
"""

import os
import zipfile

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE   = os.path.join(BASE_DIR, "meditations_en.epub")

# ── CSS Style ─────────────────────────────────────────────────────────────────
STYLE = """
body {
    font-family: Georgia, 'Lora', serif;
    font-size: 1em;
    line-height: 1.7;
    margin: 1.5em 2em;
    color: #1a1a1a;
    background-color: #fdfaf5;
}

h1 {
    font-size: 1.6em;
    font-weight: bold;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 0.3em;
    letter-spacing: 0.05em;
    color: #2c1a0e;
}

h2 {
    font-size: 1.1em;
    font-weight: normal;
    text-align: center;
    font-style: italic;
    margin-top: 0;
    margin-bottom: 2em;
    color: #5a3e28;
}

p {
    margin: 0 0 0.9em 0;
    text-indent: 1.5em;
}

p.no-indent {
    text-indent: 0;
}

.separator {
    text-align: center;
    margin: 2em 0;
    color: #8b6040;
    font-size: 1.2em;
}

.copyright-page {
    font-size: 0.9em;
    color: #333;
}

.copyright-page h1 {
    font-size: 1.3em;
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
        f"  <title>{title}</title>",
        f"  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        f"</head>",
        f"<body>",
        f"<h1>{title}</h1>"
    ]
    
    # Skip the first line if it's the title itself (e.g. "Book 1")
    if lines and (lines[0].strip().lower().startswith("book ")):
        lines = lines[1:]

    for line in lines:
        line = line.strip()
        if not line:
            continue
        html_parts.append(f"<p>{line}</p>")

    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

# ── Build EPUB natively ───────────────────────────────────────────────────────
def main():
    print("Building EPUB natively...")
    
    chapters = [] # list of dicts: {'id': '', 'href': '', 'title': '', 'content': ''}
    
    # 1. Introduction
    intro_text = read_txt(os.path.join(BASE_DIR, "introduction_en.txt"))
    intro_html = txt_to_html(intro_text, "A Note to the Reader")
    chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': 'A Note to the Reader', 'content': intro_html})

    # 2. Chapters 1-12
    for i in range(1, 13):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        if not os.path.exists(txt_path):
            continue
        text = read_txt(txt_path)
        first_line = text.split("\n")[0].strip()
        title = first_line if first_line.lower().startswith("book") else f"Book {i}"
            
        ch_html = txt_to_html(text, title)
        uid = f"ch{i:02d}"
        fname = f"Text/ch{i:02d}.xhtml"
        chapters.append({'id': uid, 'href': fname, 'title': title, 'content': ch_html})

    # 3. Copyright
    copy_text = read_txt(os.path.join(BASE_DIR, "copyright_en.txt"))
    copy_html = txt_to_html(copy_text, "Copyright &amp; About This Edition")
    chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': 'Copyright &amp; About This Edition', 'content': copy_html})
        
    # Build OPF Manifest
    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        "    <dc:identifier id=\"pub-id\">tkprof-meditations-2026</dc:identifier>",
        "    <dc:title>Meditations</dc:title>",
        "    <dc:language>en</dc:language>",
        "    <dc:creator>Marcus Aurelius</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026</dc:date>",
        "    <dc:rights>Modernized edition Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>Philosophy</dc:subject>",
        "    <dc:subject>Stoicism</dc:subject>",
        "    <dc:subject>Classic Literature</dc:subject>",
        "    <dc:subject>Audiobook Friendly</dc:subject>",
        "    <meta property=\"dcterms:modified\">2026-07-04T12:00:00Z</meta>",
        "  </metadata>",
        "  <manifest>",
        "    <item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\"/>",
        "    <item id=\"nav\" href=\"nav.xhtml\" media-type=\"application/xhtml+xml\" properties=\"nav\"/>",
        "    <item id=\"css\" href=\"Styles/main.css\" media-type=\"text/css\"/>"
    ]
    
    for ch in chapters:
        opf_parts.append(f"    <item id=\"{ch['id']}\" href=\"{ch['href']}\" media-type=\"application/xhtml+xml\"/>")
        
    opf_parts.append("  </manifest>")
    opf_parts.append("  <spine toc=\"ncx\">")
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
        "    <meta name=\"dtb:uid\" content=\"tkprof-meditations-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle><text>Meditations</text></docTitle>",
        "  <navMap>"
    ]
    for idx, ch in enumerate(chapters, 1):
        ncx_parts.append(f"    <navPoint id=\"navpoint-{idx}\" playOrder=\"{idx}\">")
        ncx_parts.append(f"      <navLabel><text>{ch['title']}</text></navLabel>")
        ncx_parts.append(f"      <content src=\"{ch['href']}\"/>")
        ncx_parts.append(f"    </navPoint>")
    ncx_parts.append("  </navMap>")
    ncx_parts.append("</ncx>")
    ncx_content = "\n".join(ncx_parts)

    # Build Nav (EPUB 3 TOC)
    nav_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head><title>Table of Contents</title></head>",
        "<body>",
        "  <nav epub:type=\"toc\" id=\"toc\">",
        "    <h2>Table of Contents</h2>",
        "    <ol>"
    ]
    for ch in chapters:
        nav_parts.append(f"      <li><a href=\"{ch['href']}\">{ch['title']}</a></li>")
    nav_parts.append("    </ol>")
    nav_parts.append("  </nav>")
    nav_parts.append("</body>")
    nav_parts.append("</html>")
    nav_content = "\n".join(nav_parts)

    # Build the Zip Archive
    with zipfile.ZipFile(OUTPUT_FILE, 'w') as zf:
        # 1. mimetype (uncompressed)
        zf.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        
        # 2. META-INF
        container_xml = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<container xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\" version=\"1.0\">\n"
            "  <rootfiles>\n"
            "    <rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\"/>\n"
            "  </rootfiles>\n"
            "</container>"
        )
        zf.writestr('META-INF/container.xml', container_xml, compress_type=zipfile.ZIP_DEFLATED)
        
        # 3. OEBPS contents
        zf.writestr('OEBPS/content.opf', opf_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/toc.ncx', ncx_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/nav.xhtml', nav_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Styles/main.css', STYLE.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        
        for ch in chapters:
            zf.writestr(f"OEBPS/{ch['href']}", ch['content'].encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\nNative EPUB created: {OUTPUT_FILE}")
    print(f"Size: {size_kb:.0f} KB")

if __name__ == "__main__":
    main()
