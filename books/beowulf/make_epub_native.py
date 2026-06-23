"""
make_epub_native.py
Compiles Beowulf into an EPUB file directly using python's zipfile.
"""

import os
import zipfile

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters")
IMAGES_DIR    = os.path.join(BASE_DIR, "images")
OUTPUT_FILE   = os.path.join(BASE_DIR, "beowulf.epub")

CHAPTER_IMAGES = {
    11: ["illu_grendel.jpg"],
    26: ["illu_water_witch.jpg"],
    29: ["illu_grendel_head.jpg"],
    39: ["illu_dragon.jpg"],
    43: ["illu_death.png"]
}

# ── CSS Style ─────────────────────────────────────────────────────────────────
STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,700;1,400&display=swap');

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

h2.chapter-subtitle {
    font-size: 1.2em;
    font-style: normal;
    font-weight: bold;
    letter-spacing: 0.1em;
    margin-top: -1em;
    margin-bottom: 2.5em;
    color: #2c1a0e;
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

img.illustration {
    display: block;
    max-width: 85%;
    margin: 1.5em auto;
}

.footnote {
    font-size: 0.85em;
    color: #555;
    margin-top: 2em;
    border-top: 1px solid #ccc;
    padding-top: 0.5em;
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
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except UnicodeDecodeError:
        with open(path, "r", encoding="cp1252") as f:
            return f.read().strip()

def txt_to_html(text, title, subtitle=None, images=None):
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
    
    if subtitle:
        html_parts.append(f"<h2 class=\"chapter-subtitle\">{subtitle}</h2>")

    # skip the first line if it's the title
    if lines and (lines[0].startswith("Chapter") or lines[0].startswith("Prologue")):
        lines = lines[1:]

    seen_paragraph = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("[Footnote"):
            html_parts.append(f'<p class="footnote">{line}</p>')
            seen_paragraph = True
        elif line.isupper() and len(line) < 80:
            html_parts.append(f"<h2>{line}</h2>")
        else:
            html_parts.append(f"<p>{line}</p>")
            seen_paragraph = True

    if images:
        for img_name in images:
            html_parts.append(f'<div class="separator">* * *</div>')
            html_parts.append(f'<img class="illustration" src="../Images/{img_name}" alt="Illustration"/>')

    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

# ── Build EPUB natively ───────────────────────────────────────────────────────
def main():
    print("Building EPUB natively...")
    
    chapters = [] # list of dicts: {'id': '', 'href': '', 'title': '', 'content': ''}
    images_to_add = [] # list of tuples: (source_path, dest_filename, mimetype)
    
    # 1. Introduction
    intro_text = read_txt(os.path.join(BASE_DIR, "introduction_en.txt"))
    intro_html = txt_to_html(intro_text, "A Note to the Reader")
    chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': 'A Note to the Reader', 'content': intro_html})

    # 2. Prologue (Chapter 0)
    ch00_txt_path = os.path.join(CHAPTERS_DIR, "ch_00_en.txt")
    if os.path.exists(ch00_txt_path):
        text = read_txt(ch00_txt_path)
        first_line = text.split("\n")[0]
        if ":" in first_line:
            title, subtitle = first_line.split(":", 1)
            title = title.strip()
            subtitle = subtitle.strip()
        else:
            title = first_line
            subtitle = None
        ch_html = txt_to_html(text, title, subtitle=subtitle)
        chapters.append({'id': 'ch00', 'href': 'Text/ch00.xhtml', 'title': first_line, 'content': ch_html})

    # 3. Chapters 1-43
    for i in range(1, 44):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        if not os.path.exists(txt_path):
            continue
        text = read_txt(txt_path)
        first_line = text.split("\n")[0]
        if ":" in first_line:
            title, subtitle = first_line.split(":", 1)
            title = title.strip()
            subtitle = subtitle.strip()
        else:
            title = first_line
            subtitle = None
            
        img_names = []
        for img_name in CHAPTER_IMAGES.get(i, []):
            img_path = os.path.join(IMAGES_DIR, img_name)
            if os.path.exists(img_path):
                mime = "image/png" if img_name.endswith(".png") else "image/jpeg"
                images_to_add.append((img_path, img_name, mime))
                img_names.append(img_name)
                
        ch_html = txt_to_html(text, title, subtitle=subtitle, images=img_names)
        uid = f"ch{i:02d}"
        fname = f"Text/ch{i:02d}.xhtml"
        nav_title = first_line
        chapters.append({'id': uid, 'href': fname, 'title': nav_title, 'content': ch_html})

    # 4. Copyright
    copy_text = read_txt(os.path.join(BASE_DIR, "copyright_en.txt"))
    copy_html = txt_to_html(copy_text, "Copyright &amp; About This Edition")
    chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': 'Copyright &amp; About This Edition', 'content': copy_html})
        
    # Cover image
    has_cover = False
    cover_src = os.path.join(IMAGES_DIR, "cover.jpg")
    if os.path.exists(cover_src):
        images_to_add.append((cover_src, "cover.jpg", "image/jpeg"))
        has_cover = True
        
    # Build OPF Manifest
    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        "    <dc:identifier id=\"pub-id\">tkprof-beowulf-2026</dc:identifier>",
        "    <dc:title>Beowulf: Modern English Edition</dc:title>",
        "    <dc:language>en</dc:language>",
        "    <dc:creator>Anonymous</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026</dc:date>",
        "    <dc:rights>Modernized edition Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>Epic Poetry</dc:subject>",
        "    <dc:subject>Classic Literature</dc:subject>",
        "    <dc:subject>Fantasy</dc:subject>",
        "    <dc:subject>Old English</dc:subject>",
        "    <dc:subject>ESL EFL Learning</dc:subject>",
        "    <dc:subject>Audiobook Friendly</dc:subject>",
        "    <meta property=\"dcterms:modified\">2026-06-21T12:00:00Z</meta>"
    ]
    if has_cover:
        opf_parts.append("    <meta name=\"cover\" content=\"cover-image\"/>")
    opf_parts.append("  </metadata>")
    opf_parts.append("  <manifest>")
    opf_parts.append("    <item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\"/>")
    opf_parts.append("    <item id=\"nav\" href=\"nav.xhtml\" media-type=\"application/xhtml+xml\" properties=\"nav\"/>")
    opf_parts.append("    <item id=\"css\" href=\"Styles/main.css\" media-type=\"text/css\"/>")
    
    for ch in chapters:
        opf_parts.append(f"    <item id=\"{ch['id']}\" href=\"{ch['href']}\" media-type=\"application/xhtml+xml\"/>")
        
    for idx, (src, name, mime) in enumerate(images_to_add):
        item_id = "cover-image" if name == "cover.jpg" else f"img{idx}"
        props = ' properties="cover-image"' if name == "cover.jpg" else ""
        opf_parts.append(f"    <item id=\"{item_id}\" href=\"Images/{name}\" media-type=\"{mime}\"{props}/>")

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
        "    <meta name=\"dtb:uid\" content=\"tkprof-beowulf-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle><text>Beowulf: Modern English Edition</text></docTitle>",
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
            
        for src, name, mime in images_to_add:
            zf.write(src, arcname=f"OEBPS/Images/{name}", compress_type=zipfile.ZIP_DEFLATED)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\nNative EPUB created: {OUTPUT_FILE}")
    print(f"Size: {size_kb:.0f} KB")

if __name__ == "__main__":
    main()
