import os
import zipfile
import uuid
from datetime import datetime, timezone

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters_en_v2")
IMAGES_DIR    = os.path.join(BASE_DIR, "images")
OUTPUT_FILE   = os.path.join(BASE_DIR, "beowulf_en_v2.epub")

# Mapping of chapter numbers to image filenames
CHAPTER_IMAGES = {
    11: ["illu_grendel.jpg"],
    26: ["illu_water_witch.jpg"],
    29: ["illu_grendel_head.jpg"],
    39: ["illu_dragon.jpg"],
    43: ["illu_death.png"]
}

# Alt text mapping for accessibility
IMAGE_ALTS = {
    "illu_grendel.jpg": "Illustration of the monstrous Grendel lurking in the dark outside the royal hall.",
    "illu_water_witch.jpg": "Illustration of Grendel's mother, the fierce water-witch, emerging from the lake.",
    "illu_grendel_head.jpg": "Illustration of Grendel's giant severed head being carried into the hall.",
    "illu_dragon.jpg": "Illustration of the fearsome fire dragon defending its hoard in the cave.",
    "illu_death.png": "Illustration of Beowulf's final moments and his tragic death."
}

# ── CSS Style ─────────────────────────────────────────────────────────────────
STYLE = """
body {
    font-family: 'Georgia', serif;
    font-size: 1em;
    line-height: 1.8;
    margin: 1.5em 2em;
    color: #1a1a1a;
    background-color: #fdfaf5;
}

h1 {
    font-size: 1.6em;
    font-weight: bold;
    text-align: center;
    margin-top: 2em;
    margin-bottom: 1em;
    letter-spacing: 0.05em;
    color: #2c1a0e;
}

h2 {
    font-size: 1.2em;
    font-weight: bold;
    text-align: center;
    margin-top: 1.5em;
    margin-bottom: 1em;
    color: #5a3e28;
}

p {
    margin: 0 0 1em 0;
    text-indent: 1.5em;
    word-break: normal;
}

blockquote {
    font-style: italic;
    font-weight: bold;
    margin: 1.5em 2em;
    padding: 0.5em 1em;
    border-left: 4px solid #8b6040;
    background-color: #f5eedf;
    color: #3b2a1a;
    text-indent: 0;
}

blockquote p {
    text-indent: 0;
    margin: 0;
}

img.illustration {
    display: block;
    max-width: 90%;
    margin: 2em auto;
    border: 1px solid #ccc;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.separator {
    text-align: center;
    margin: 2em 0;
    color: #8b6040;
    font-size: 1.2em;
}
"""

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title, images=None):
    lines = text.split("\n")
    html_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head>",
        f"  <title>{title}</title>",
        "  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        "</head>",
        "<body>",
        f"<h1>{title}</h1>"
    ]
    
    in_blockquote = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Skip the chapter title if it's already the first line
        if line == title or (line.startswith("Chapter") and ":" in line):
            if html_parts[-1] == f"<h1>{title}</h1>":
                continue

        if line.startswith(">"):
            if not in_blockquote:
                html_parts.append("<blockquote>")
                in_blockquote = True
            
            clean_line = line.lstrip("> *").rstrip("*").strip()
            if clean_line:
                html_parts.append(f"<p>{clean_line}</p>")
            continue
        else:
            if in_blockquote:
                html_parts.append("</blockquote>")
                in_blockquote = False
                
        html_parts.append(f"<p>{line}</p>")

    if in_blockquote:
        html_parts.append("</blockquote>")

    if images:
        for img_name in images:
            alt_text = IMAGE_ALTS.get(img_name, "Illustration of the scene")
            html_parts.append('<div class="separator">* * *</div>')
            html_parts.append(f'<img class="illustration" src="../Images/{img_name}" alt="{alt_text}"/>')

    html_parts.append("</body>")
    html_parts.append("</html>")
    return "\n".join(html_parts)

def main():
    print("Building EPUB natively with illustrations...")
    
    chapters = []
    images_to_add = []
    
    # 1. Introduction
    intro_txt_path = os.path.join(CHAPTERS_DIR, "introduction_en_v2.txt")
    if os.path.exists(intro_txt_path):
        intro_text = read_txt(intro_txt_path)
        intro_html = txt_to_html(intro_text, "Letter to the Reader")
        chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': 'Letter to the Reader', 'content': intro_html})

    # 2. Chapters 0-43
    for i in range(44):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        if not os.path.exists(txt_path):
            continue
        
        text = read_txt(txt_path)
        first_line = text.split("\n")[0].strip()
        title = first_line if first_line else f"Chapter {i}"
        
        img_names = []
        for img_name in CHAPTER_IMAGES.get(i, []):
            img_path = os.path.join(IMAGES_DIR, img_name)
            if os.path.exists(img_path):
                mime = "image/png" if img_name.endswith(".png") else "image/jpeg"
                images_to_add.append((img_path, img_name, mime))
                img_names.append(img_name)
                
        ch_html = txt_to_html(text, title, images=img_names)
        uid = f"ch{i:02d}"
        fname = f"Text/ch{i:02d}.xhtml"
        chapters.append({'id': uid, 'href': fname, 'title': title, 'content': ch_html})

    # 3. Copyright
    copy_txt_path = os.path.join(CHAPTERS_DIR, "copyright_en_v2.txt")
    if os.path.exists(copy_txt_path):
        copy_text = read_txt(copy_txt_path)
        copy_html = txt_to_html(copy_text, "Copyright and Editor's Note")
        chapters.append({'id': 'copyright', 'href': 'Text/copyright.xhtml', 'title': "Copyright and Editor's Note", 'content': copy_html})

    # Cover image
    has_cover = False
    cover_src = os.path.join(IMAGES_DIR, "cover.jpg")
    if os.path.exists(cover_src):
        images_to_add.append((cover_src, "cover.jpg", "image/jpeg"))
        has_cover = True

    book_uuid = f"urn:uuid:{uuid.uuid4()}"
    modified_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        f"    <dc:identifier id=\"pub-id\">{book_uuid}</dc:identifier>",
        "    <dc:title>Beowulf: Spectacular Modern English Edition</dc:title>",
        "    <dc:language>en</dc:language>",
        "    <dc:creator>Anonymous</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026-06-28</dc:date>",
        "    <dc:description>The oldest epic in English literature reborn into a spectacular modern fantasy blockbuster.</dc:description>",
        "    <dc:rights>Modern Adaptation Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>Fantasy</dc:subject>",
        "    <dc:subject>Action</dc:subject>",
        "    <dc:subject>Web Novel</dc:subject>",
        f"    <meta property=\"dcterms:modified\">{modified_date}</meta>"
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
        
    for img_path, img_name, mime in images_to_add:
        img_id = img_name.replace(".", "-").replace("_", "-")
        if img_name == "cover.jpg":
            opf_parts.append(f"    <item id=\"cover-image\" href=\"Images/{img_name}\" media-type=\"{mime}\" properties=\"cover-image\"/>")
        else:
            opf_parts.append(f"    <item id=\"{img_id}\" href=\"Images/{img_name}\" media-type=\"{mime}\"/>")

    opf_parts.append("  </manifest>")
    opf_parts.append("  <spine toc=\"ncx\">")
    for ch in chapters:
        opf_parts.append(f"    <itemref idref=\"{ch['id']}\"/>")
    opf_parts.append("  </spine>")
    opf_parts.append("</package>")
    opf_content = "\n".join(opf_parts)

    ncx_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">",
        "  <head>",
        "    <meta name=\"dtb:uid\" content=\"tkprof-beowulf-en-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle><text>Beowulf: Spectacular Modern English Edition</text></docTitle>",
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

    with zipfile.ZipFile(OUTPUT_FILE, 'w') as zf:
        zf.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        
        container_xml = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<container xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\" version=\"1.0\">\n"
            "  <rootfiles>\n"
            "    <rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\"/>\n"
            "  </rootfiles>\n"
            "</container>"
        )
        zf.writestr('META-INF/container.xml', container_xml, compress_type=zipfile.ZIP_DEFLATED)
        
        zf.writestr('OEBPS/content.opf', opf_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/toc.ncx', ncx_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/nav.xhtml', nav_content.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Styles/main.css', STYLE.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        
        for ch in chapters:
            zf.writestr(f"OEBPS/{ch['href']}", ch['content'].encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
            
        for img_path, img_name, mime in images_to_add:
            with open(img_path, 'rb') as f:
                img_data = f.read()
            zf.writestr(f"OEBPS/Images/{img_name}", img_data, compress_type=zipfile.ZIP_DEFLATED)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"Native EPUB with illustrations created: {OUTPUT_FILE}")
    print(f"Size: {size_kb:.0f} KB")

if __name__ == "__main__":
    main()
