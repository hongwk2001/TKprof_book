"""
make_epub_en.py
Compiles the English version of The Odyssey into an EPUB file.
"""

import os
import zipfile
import uuid
import re
import html
from datetime import datetime, timezone

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE   = os.path.join(BASE_DIR, "odyssey_en.epub")

# ── CSS Style ─────────────────────────────────────────────────────────────────
STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,700;1,400;1,700&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

body {
    font-family: 'Lora', Georgia, serif;
    font-size: 1em;
    line-height: 1.6;
    margin: 1.5em 2em;
    color: #2c2c2c;
    background-color: #fdfdfd;
}

h1, h2 {
    font-family: 'Playfair Display', serif;
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
    font-size: 1.25em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 1em;
    color: #2a3a4a;
    line-height: 1.4;
}

p {
    margin: 0 0 1.2em 0;
    text-indent: 1.5em;
}

p.no-indent {
    text-indent: 0;
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
        f"  <title>{html.escape(title)}</title>",
        f"  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        f"</head>",
        f"<body>",
        f"<h1>{html.escape(title)}</h1>"
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
            html_parts.append(f"<h2>{html.escape(line[1:-1])}</h2>")
            is_first_p = True
        else:
            escaped_line = html.escape(line)
            if is_first_p:
                html_parts.append(f"<p class=\"no-indent\">{escaped_line}</p>")
                is_first_p = False
            else:
                html_parts.append(f"<p>{escaped_line}</p>")

    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

# ── Build EPUB ────────────────────────────────────────────────────────────────
def main():
    print("Building English EPUB for The Odyssey natively...")
    
    chapters = []
    
    # 1. Introduction
    intro_txt_path = os.path.join(BASE_DIR, "introduction_en.txt")
    if os.path.exists(intro_txt_path):
        intro_text = read_txt(intro_txt_path)
        # Skip the title in text compilation
        lines = intro_text.split("\n")
        intro_body = "\n".join(lines[1:]) if lines[0].strip() == "About This Edition" else intro_text
        intro_html = txt_to_html(intro_body, "About This Edition")
        chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': 'About This Edition', 'content': intro_html})

    # 2. Chapters 1-24
    for i in range(1, 25):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        if not os.path.exists(txt_path):
            print(f"Warning: ch_{i:02d}_en.txt missing, skipping.")
            continue
        title = f"Book {i}"
        text = read_txt(txt_path)
        
        # Keep the subtitle (synopsis) inside the text as well
        ch_html = txt_to_html(text, title)
        uid = f"ch{i:02d}"
        fname = f"Text/ch{i:02d}.xhtml"
        chapters.append({'id': uid, 'href': fname, 'title': title, 'content': ch_html})

    # 3. Copyright
    copy_txt_path = os.path.join(BASE_DIR, "copyright_en.txt")
    if os.path.exists(copy_txt_path):
        copy_text = read_txt(copy_txt_path)
        lines = copy_text.split("\n")
        copy_body = "\n".join(lines[1:]) if lines[0].strip() == "Copyright & About This Edition" else copy_text
        copy_html = txt_to_html(copy_body, "Copyright & About This Edition")
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
        "    <dc:title>The Odyssey</dc:title>",
        "    <dc:language>en</dc:language>",
        "    <dc:creator>Homer</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026-07-12</dc:date>",
        "    <dc:description>A modernized adaptation of Homer's legendary epic poem, recounting Odysseus's ten-year journey home to Ithaca in clear, engaging, and accessible contemporary prose optimized for Text-to-Speech (TTS) listening.</dc:description>",
        "    <dc:rights>English translation and adaptation Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>Fiction</dc:subject>",
        "    <dc:subject>Classics</dc:subject>",
        "    <dc:subject>Greek Mythology</dc:subject>",
        "    <dc:subject>Adventure</dc:subject>",
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

    # Build NCX
    ncx_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">",
        "  <head>",
        "    <meta name=\"dtb:uid\" content=\"tkprof-odyssey-en-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle>",
        "    <text>The Odyssey</text>",
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
        ncx_parts.append(f"    <navPoint id=\"navPoint-{play_order}\" playOrder=\"{play_order}\">")
        ncx_parts.append(f"      <navLabel><text>{html.escape(ch['title'])}</text></navLabel>")
        ncx_parts.append(f"      <content src=\"{ch['href']}\"/>")
        ncx_parts.append(f"    </navPoint>")
        
    ncx_parts.append("  </navMap>")
    ncx_parts.append("</ncx>")
    ncx_content = "\n".join(ncx_parts)

    # Build HTML5 Navigation
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
        "    nav a { text-decoration: none; color: #1a2a3a; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <nav epub:type=\"toc\" id=\"toc\">",
        "    <h1>Contents</h1>",
        "    <ol>",
        "      <li><a href=\"Text/cover.xhtml\">Cover</a></li>"
    ]
    
    for ch in chapters:
        nav_parts.append(f"      <li><a href=\"{ch['href']}\">{html.escape(ch['title'])}</a></li>")
        
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

    # Zip output
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        
    with zipfile.ZipFile(OUTPUT_FILE, "w", zipfile.ZIP_DEFLATED) as epub:
        epub.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        epub.writestr("META-INF/container.xml", container_content)
        epub.write(os.path.join(BASE_DIR, "cover.png"), "OEBPS/Images/cover.png")
        epub.writestr("OEBPS/Text/cover.xhtml", cover_html)
        epub.writestr("OEBPS/Styles/main.css", STYLE)
        epub.writestr("OEBPS/content.opf", opf_content)
        epub.writestr("OEBPS/toc.ncx", ncx_content)
        epub.writestr("OEBPS/nav.xhtml", nav_content)
        
        for ch in chapters:
            epub.writestr(f"OEBPS/{ch['href']}", ch['content'])
            
    print(f"English EPUB for Odyssey created successfully at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
