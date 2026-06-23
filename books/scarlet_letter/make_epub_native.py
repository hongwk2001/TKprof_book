"""
make_epub_native.py
Compiles The Scarlet Letter into an EPUB file directly using python's zipfile.
This avoids the bugs present in ebooklib and generates a clean EPUB3 structure.
"""

import os
import zipfile
import uuid
from datetime import datetime, timezone
import uuid

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters")
IMAGES_DIR    = os.path.join(BASE_DIR, "images")
ARTIFACTS_DIR = r"C:\Users\hongw\.gemini\antigravity\brain\38029dd8-7a47-43bc-b3ce-22e975f3fe84"
OUTPUT_FILE   = os.path.join(BASE_DIR, "scarlet_letter.epub")

# ── Chapter metadata ─────────────────────────────────────────────────────────
CHAPTER_TITLES = {
    0:  "The Custom-House",
    1:  ("Chapter One", "The Prison-Door"),
    2:  ("Chapter Two", "The Market-Place"),
    3:  ("Chapter Three", "The Recognition"),
    4:  ("Chapter Four", "The Interview"),
    5:  ("Chapter Five", "Hester at Her Needle"),
    6:  ("Chapter Six", "Pearl"),
    7:  ("Chapter Seven", "The Governor's Hall"),
    8:  ("Chapter Eight", "The Elf-Child and the Minister"),
    9:  ("Chapter Nine", "The Leech"),
    10: ("Chapter Ten", "The Leech and His Patient"),
    11: ("Chapter Eleven", "The Interior of a Heart"),
    12: ("Chapter Twelve", "The Minister's Vigil"),
    13: ("Chapter Thirteen", "Another View of Hester"),
    14: ("Chapter Fourteen", "Hester and the Physician"),
    15: ("Chapter Fifteen", "Hester and Pearl"),
    16: ("Chapter Sixteen", "A Forest Walk"),
    17: ("Chapter Seventeen", "The Pastor and His Parishioner"),
    18: ("Chapter Eighteen", "A Flood of Sunshine"),
    19: ("Chapter Nineteen", "The Child at the Brook-Side"),
    20: ("Chapter Twenty", "The Minister in a Maze"),
    21: ("Chapter Twenty-One", "The New England Holiday"),
    22: ("Chapter Twenty-Two", "The Procession"),
    23: ("Chapter Twenty-Three", "The Revelation of the Scarlet Letter"),
    24: ("Chapter Twenty-Four", "Conclusion"),
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

CHAPTER_IMAGES = {
    0:  ["illu_001"],
    2:  ["illu_065"],
    4:  ["illu_087"],
    5:  ["illu_093"],
    6:  ["illu_099"],
    7:  ["illu_113"],
    8:  ["illu_125"],
    9:  ["illu_135"],
    10: ["illu_148"],
    11: ["illu_165"],
    12: ["illu_185"],
    13: ["illu_195"],
    14: ["illu_213"],
    15: ["illu_217"],
    16: ["illu_237"],
    17: ["illu_249"],
    18: ["illu_257"],
    20: ["illu_287"],
    22: ["illu_311"],
    24: ["illu_320"],
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title, subtitle=None, images=None):
    lines = text.split("\n")
    if isinstance(title, tuple):
        page_title = f"{title[0]}: {title[1]}"
        html_parts = [
            f"<?xml version='1.0' encoding='utf-8'?>",
            f"<!DOCTYPE html>",
            f"<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
            f"<head>",
            f"  <title>{title[0]}</title>",
            f"  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
            f"</head>",
            f"<body>",
            f"<h1>{title[0]}</h1>",
            f"<h2 class=\"chapter-subtitle\">{title[1].upper()}.</h2>"
        ]
    else:
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
        html_parts.append(f"<h2>{subtitle}</h2>")

    seen_paragraph = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("[Footnote"):
            html_parts.append(f'<p class="footnote">{line}</p>')
            seen_paragraph = True
        elif line.isupper() and len(line) < 80:
            if not seen_paragraph:
                continue  # Skip redundant chapter titles from the text file
            html_parts.append(f"<h2>{line}</h2>")
        elif line in ["A Note to the Reader", "About This Edition", "About \"The Custom-House\"", "Thank You for Reading", "A Note on This Modernized Edition", "Copyright"]:
            title_text = title[0] if isinstance(title, tuple) else title
            if not seen_paragraph and line == title_text:
                continue # Skip redundant top title
            html_parts.append(f"<h2>{line}</h2>")
            seen_paragraph = True
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

def find_colorized(stem):
    for f in os.listdir(ARTIFACTS_DIR):
        if f.startswith(stem + "_color") and f.endswith(".jpg"):
            return os.path.join(ARTIFACTS_DIR, f), ".jpg"
    for f in os.listdir(ARTIFACTS_DIR):
        if f.startswith(stem + "_color") and f.endswith(".png"):
            return os.path.join(ARTIFACTS_DIR, f), ".png"
    return None, None

def get_image_info(stem):
    color_path, ext = find_colorized(stem)
    if color_path:
        mime = "image/jpeg" if ext == ".jpg" else "image/png"
        return color_path, f"{stem}_color{ext}", mime
    
    bw_path = os.path.join(IMAGES_DIR, f"{stem}.jpg")
    if os.path.exists(bw_path):
        return bw_path, f"{stem}.jpg", "image/jpeg"
    return None, None, None

# ── Build EPUB natively ───────────────────────────────────────────────────────
def main():
    print("Building EPUB natively...")
    
    chapters = [] # list of dicts: {'id': '', 'href': '', 'title': '', 'content': ''}
    images_to_add = [] # list of tuples: (source_path, dest_filename, mimetype)
    
    # 1. Introduction
    intro_text = read_txt(os.path.join(BASE_DIR, "introduction_en.txt"))
    intro_html = txt_to_html(intro_text, "A Note to the Reader")
    chapters.append({'id': 'intro', 'href': 'Text/intro.xhtml', 'title': 'A Note to the Reader', 'content': intro_html})

    # 2. Chapters 1-24
    for i in range(1, 25):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        if not os.path.exists(txt_path):
            continue
        title = CHAPTER_TITLES[i]
        text = read_txt(txt_path)
        
        img_names = []
        for stem in CHAPTER_IMAGES.get(i, []):
            src, name, mime = get_image_info(stem)
            if src:
                images_to_add.append((src, name, mime))
                img_names.append(name)
                
        ch_html = txt_to_html(text, title, images=img_names)
        uid = f"ch{i:02d}"
        fname = f"Text/ch{i:02d}.xhtml"
        nav_title = f"{title[0]}: {title[1]}" if isinstance(title, tuple) else title
        chapters.append({'id': uid, 'href': fname, 'title': nav_title, 'content': ch_html})

    # 3. Custom-House & Preface
    ch00_full = read_txt(os.path.join(CHAPTERS_DIR, "ch_00_en.txt"))
    parts = ch00_full.split("THE CUSTOM-HOUSE")
    if len(parts) == 2:
        preface_text = parts[0].strip()
        custom_house_text = "THE CUSTOM-HOUSE" + parts[1]
    else:
        preface_text = ""
        custom_house_text = ch00_full

    if preface_text:
        pref_html = txt_to_html(preface_text, "Preface to the Second Edition")
        chapters.append({'id': 'preface', 'href': 'Text/preface.xhtml', 'title': 'Preface to the Second Edition', 'content': pref_html})

    img_names = []
    for stem in CHAPTER_IMAGES.get(0, []):
        src, name, mime = get_image_info(stem)
        if src:
            images_to_add.append((src, name, mime))
            img_names.append(name)
    ch00_html = txt_to_html(custom_house_text, CHAPTER_TITLES[0], subtitle="Introductory to The Scarlet Letter", images=img_names)
    chapters.append({'id': 'custom_house', 'href': 'Text/custom_house.xhtml', 'title': CHAPTER_TITLES[0], 'content': ch00_html})

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
        
    book_uuid = f"urn:uuid:{uuid.uuid4()}"
    modified_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build OPF Manifest
    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        f"    <dc:identifier id=\"pub-id\">{book_uuid}</dc:identifier>",
        "    <dc:title>The Scarlet Letter: Modern English Edition</dc:title>",
        "    <dc:language>en</dc:language>",
        "    <dc:creator>Nathaniel Hawthorne</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026-06-22</dc:date>",
        "    <dc:description>A modern English adaptation of Nathaniel Hawthorne's 1850 masterpiece. Set in Puritan Boston, The Scarlet Letter follows Hester Prynne, a woman condemned to wear a symbol of shame, as she finds courage, identity, and quiet redemption. This edition is adapted for language learners, students, and audiobook listeners, with digitally colorized historic illustrations from the 1878 edition.</dc:description>",
        "    <dc:rights>Modernized edition Copyright 2026 TKPROF LLC. Original text public domain.</dc:rights>",
        "    <dc:subject>Fiction</dc:subject>",
        "    <dc:subject>Classic Literature</dc:subject>",
        "    <dc:subject>Historical Fiction</dc:subject>",
        "    <dc:subject>American Literature</dc:subject>",
        "    <dc:subject>19th Century</dc:subject>",
        "    <dc:subject>ESL EFL Learning</dc:subject>",
        "    <dc:subject>Audiobook Friendly</dc:subject>",
        "    <dc:subject>Puritan New England</dc:subject>",
        "    <dc:subject>Nathaniel Hawthorne</dc:subject>",
        f"    <meta property=\"dcterms:modified\">{modified_date}</meta>",
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
        "    <meta name=\"dtb:uid\" content=\"tkprof-scarlet-letter-2026\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle><text>The Scarlet Letter: Modern English Edition</text></docTitle>",
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
