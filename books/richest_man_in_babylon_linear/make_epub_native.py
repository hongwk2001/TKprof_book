"""
make_epub_native.py
Compiles the Recreated Linear Edition of The Richest Man in Babylon into an EPUB file directly using python's zipfile.
This generates a clean EPUB3 structure.
"""

import os
import zipfile
import uuid
import glob
from datetime import datetime, timezone

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE   = os.path.join(BASE_DIR, "the_richest_man_in_babylon_linear.epub")

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
    color: #2c1a0e;
}

h2 {
    font-size: 1.4em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 1em;
    color: #5a3e28;
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
    color: #8b6040;
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
        f"  <title>{title}</title>",
        f"  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        f"</head>",
        f"<body>",
        f"<h1>{title}</h1>"
    ]
    
    # We skip header lines in text to avoid duplicate headers in HTML
    body_started = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip the title headers inside the text
        if not body_started:
            if line.lower() == title.lower() or line.lower().startswith("chapter ") or line.lower().startswith("epilogue"):
                continue
            body_started = True
            
        if line.startswith("[") and line.endswith("]"):
            html_parts.append(f"<h2>{line[1:-1]}</h2>")
        else:
            html_parts.append(f"<p>{line}</p>")

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

    # 2. Chapters 1-10 (including Epilogue)
    chapter_files = glob.glob(os.path.join(CHAPTERS_DIR, "ch_*.txt"))
    chapter_files.sort()
    
    for idx, txt_path in enumerate(chapter_files, 1):
        filename = os.path.basename(txt_path)
        text = read_txt(txt_path)
        
        # Determine title
        if "epilogue" in filename.lower():
            title = "Epilogue: The Nottingham Letters"
            uid = "epilogue"
            fname = "Text/epilogue.xhtml"
        else:
            title = f"Chapter {idx}"
            # Attempt to extract actual title from the second line of text if available
            lines = text.split("\n")
            if len(lines) > 1 and lines[1].strip() and not lines[1].startswith("Chapter"):
                title = f"Chapter {idx}: {lines[1].strip()}"
                
            uid = f"ch{idx:02d}"
            fname = f"Text/ch{idx:02d}.xhtml"
            
        ch_html = txt_to_html(text, title)
        chapters.append({'id': uid, 'href': fname, 'title': title, 'content': ch_html})

    # 3. Copyright
    copy_txt_path = os.path.join(BASE_DIR, "copyright_en.txt")
    if os.path.exists(copy_txt_path):
        copy_text = read_txt(copy_txt_path)
        copy_html = txt_to_html(copy_text, "Copyright")
        chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': 'Copyright', 'content': copy_html})

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
  <img src="../Images/cover.png" alt="Cover" />
</body>
</html>"""

    # Build OPF Manifest
    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        f"    <dc:identifier id=\"pub-id\">{book_uuid}</dc:identifier>",
        "    <dc:title>The Richest Man in Babylon (Recreated Linear Edition)</dc:title>",
        "    <dc:language>en</dc:language>",
        "    <dc:creator>George S. Clason</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026-07-02</dc:date>",
        "    <dc:description>A complete chronological novelization of the Babylonian wealth parables. Follow Tarkad from bankruptcy to wealth under the mentorship of Arkad and Mathon.</dc:description>",
        "    <dc:rights>Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>Personal Finance</dc:subject>",
        "    <dc:subject>Wealth Management</dc:subject>",
        "    <dc:subject>Parables</dc:subject>",
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
        "    <meta name=\"dtb:uid\" content=\"tkprof-richest-man-in-babylon-linear-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle><text>The Richest Man in Babylon (Linear Edition)</text></docTitle>",
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
        cover_path = os.path.join(BASE_DIR, 'cover_with_text.png')
        if os.path.exists(cover_path):
            zf.write(cover_path, 'OEBPS/Images/cover.png')
        else:
            print(f"Warning: Cover image not found at {cover_path}")
            
        zf.writestr('OEBPS/Text/cover.xhtml', cover_html.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
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
