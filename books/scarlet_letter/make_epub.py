"""
make_epub.py
Compiles The Scarlet Letter (Modern English Edition) into an EPUB file.

Layout order:
  1. Introduction
  2. Chapters 1-24
  3. The Custom-House essay (ch_00)
  4. Copyright / Ending

Illustrations: uses colorized versions from the artifacts dir if available,
otherwise falls back to the original B&W images from books/scarlet_letter/images/.
"""

import os
import re
from ebooklib import epub

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR  = os.path.join(BASE_DIR, "chapters")
IMAGES_DIR    = os.path.join(BASE_DIR, "images")
ARTIFACTS_DIR = r"C:\Users\hongw\.gemini\antigravity\brain\38029dd8-7a47-43bc-b3ce-22e975f3fe84"
OUTPUT_FILE   = os.path.join(BASE_DIR, "scarlet_letter.epub")

# ── Chapter metadata ─────────────────────────────────────────────────────────
CHAPTER_TITLES = {
    0:  "The Custom-House",
    1:  "Chapter I: The Prison-Door",
    2:  "Chapter II: The Market-Place",
    3:  "Chapter III: The Recognition",
    4:  "Chapter IV: The Interview",
    5:  "Chapter V: Hester at Her Needle",
    6:  "Chapter VI: Pearl",
    7:  "Chapter VII: The Governor's Hall",
    8:  "Chapter VIII: The Elf-Child and the Minister",
    9:  "Chapter IX: The Leech",
    10: "Chapter X: The Leech and His Patient",
    11: "Chapter XI: The Interior of a Heart",
    12: "Chapter XII: The Minister's Vigil",
    13: "Chapter XIII: Another View of Hester",
    14: "Chapter XIV: Hester and the Physician",
    15: "Chapter XV: Hester and Pearl",
    16: "Chapter XVI: A Forest Walk",
    17: "Chapter XVII: The Pastor and His Parishioner",
    18: "Chapter XVIII: A Flood of Sunshine",
    19: "Chapter XIX: The Child at the Brook-Side",
    20: "Chapter XX: The Minister in a Maze",
    21: "Chapter XXI: The New England Holiday",
    22: "Chapter XXII: The Procession",
    23: "Chapter XXIII: The Revelation of the Scarlet Letter",
    24: "Chapter XXIV: Conclusion",
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
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

def txt_to_html(text, title, subtitle=None):
    """Convert plain text paragraphs to HTML content for an EPUB chapter."""
    lines = text.split("\n")
    html_parts = [f"<h1>{title}</h1>"]
    if subtitle:
        html_parts.append(f"<h2>{subtitle}</h2>")

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Footnotes
        if line.startswith("[Footnote"):
            html_parts.append(f'<p class="footnote">{line}</p>')
        # Section headings (ALL CAPS short lines)
        elif line.isupper() and len(line) < 80:
            html_parts.append(f"<h2>{line}</h2>")
        else:
            html_parts.append(f"<p>{line}</p>")

    return "\n".join(html_parts)

def find_colorized(stem):
    """Return path to colorized PNG in artifacts dir, or None."""
    for f in os.listdir(ARTIFACTS_DIR):
        if f.startswith(stem + "_color") and f.endswith(".png"):
            return os.path.join(ARTIFACTS_DIR, f)
    return None

def add_image_to_book(book, stem):
    """Add a colorized or B&W image to the epub, return the epub image item."""
    color_path = find_colorized(stem)
    if color_path:
        img_path = color_path
        media_type = "image/png"
        epub_name = f"images/{stem}_color.png"
    else:
        bw_path = os.path.join(IMAGES_DIR, f"{stem}.jpg")
        if not os.path.exists(bw_path):
            return None
        img_path = bw_path
        media_type = "image/jpeg"
        epub_name = f"images/{stem}.jpg"

    with open(img_path, "rb") as f:
        img_data = f.read()

    img_item = epub.EpubImage()
    img_item.file_name = epub_name
    img_item.media_type = media_type
    img_item.content = img_data
    book.add_item(img_item)
    return epub_name

# ── Illustration mapping: chapter number -> list of image stems ───────────────
CHAPTER_IMAGES = {
    0:  ["illu_001"],                        # Custom House building
    2:  ["illu_065"],                        # Hester on scaffold
    4:  ["illu_087"],                        # Prison cell / Chillingworth
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

# ── Build EPUB ────────────────────────────────────────────────────────────────
def main():
    book = epub.EpubBook()
    book.set_identifier("tkprof-scarlet-letter-2026")
    book.set_title("The Scarlet Letter: Modern English Edition")
    book.set_language("en")
    book.add_author("Nathaniel Hawthorne")
    book.add_metadata("DC", "publisher",    "TKPROF LLC")
    book.add_metadata("DC", "date",         "2026")
    book.add_metadata("DC", "rights",       "Modernized edition Copyright 2026 TKPROF LLC. Original text public domain.")
    book.add_metadata("DC", "description",
        "A modern English adaptation of Nathaniel Hawthorne's The Scarlet Letter, "
        "optimized for audiobook listening and ESL/EFL readers. Features clear, "
        "subject-first sentences, clean punctuation, and all 58 original 1878 "
        "illustrations digitally colorized in period-accurate watercolor style.")

    # Subject tags — improve discoverability on Google Play Books & Amazon KDP
    for tag in [
        "Fiction",
        "Classic Literature",
        "Historical Fiction",
        "American Literature",
        "19th Century",
        "ESL EFL Learning",
        "Audiobook Friendly",
        "Puritan New England",
        "Nathaniel Hawthorne",
    ]:
        book.add_metadata("DC", "subject", tag)

    # Add CSS
    style_item = epub.EpubItem(
        uid="style",
        file_name="style/main.css",
        media_type="text/css",
        content=STYLE
    )
    book.add_item(style_item)

    spine = ["nav"]
    toc   = []

    # ── Cover image ───────────────────────────────────────────────────────────
    cover_path = os.path.join(IMAGES_DIR, "cover.jpg")
    if os.path.exists(cover_path):
        with open(cover_path, "rb") as f:
            book.set_cover("images/cover.jpg", f.read())
        print("Added cover image")

    # ── Helper: make epub chapter ─────────────────────────────────────────────
    def make_chapter(uid, file_name, title, html_body, images=None):
        full_html = f"""<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{title}</title>
  <link rel="stylesheet" href="style/main.css" type="text/css"/>
</head>
<body>
{html_body}
"""
        # Append illustration(s) at end of chapter if provided
        if images:
            for img_epub_name in images:
                full_html += f'<div class="separator">* * *</div>\n'
                # images/ and content files are both at EPUB root level
                full_html += f'<img class="illustration" src="{img_epub_name}" alt="Illustration"/>\n'

        full_html += "</body>\n</html>"

        ch = epub.EpubHtml(title=title, file_name=file_name, lang="en")
        ch.content = full_html
        ch.add_item(style_item)
        book.add_item(ch)
        return ch

    # ── 1. Introduction ───────────────────────────────────────────────────────
    intro_text = read_txt(os.path.join(BASE_DIR, "introduction_en.txt"))
    intro_html = txt_to_html(intro_text, "A Note to the Reader")
    intro_ch   = make_chapter("intro", "intro.xhtml", "A Note to the Reader", intro_html)
    spine.append(intro_ch)
    toc.append(intro_ch)
    print("Added: Introduction")

    # ── 2. Chapters 1-24 ─────────────────────────────────────────────────────
    for i in range(1, 25):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_en.txt")
        if not os.path.exists(txt_path):
            print(f"WARNING: Missing ch_{i:02d}_en.txt")
            continue

        title = CHAPTER_TITLES[i]
        text  = read_txt(txt_path)

        # Add images for this chapter
        img_names = []
        for stem in CHAPTER_IMAGES.get(i, []):
            name = add_image_to_book(book, stem)
            if name:
                img_names.append(name)

        ch_html = txt_to_html(text, title)
        uid      = f"ch{i:02d}"
        fname    = f"ch{i:02d}.xhtml"
        ch_item  = make_chapter(uid, fname, title, ch_html, img_names)
        spine.append(ch_item)
        toc.append(ch_item)
        print(f"Added: {title}")

    # ── 3. The Custom-House (back of book) ────────────────────────────────────
    ch00_text = read_txt(os.path.join(CHAPTERS_DIR, "ch_00_en.txt"))
    ch00_title = "The Custom-House"

    img_names = []
    for stem in CHAPTER_IMAGES.get(0, []):
        name = add_image_to_book(book, stem)
        if name:
            img_names.append(name)

    ch00_html  = txt_to_html(ch00_text, ch00_title,
                             subtitle="Introductory to The Scarlet Letter")
    ch00_item  = make_chapter("ch00", "ch00.xhtml", ch00_title, ch00_html, img_names)
    spine.append(ch00_item)
    toc.append(ch00_item)
    print("Added: The Custom-House")

    # ── 4. Copyright / Ending ─────────────────────────────────────────────────
    copy_text = read_txt(os.path.join(BASE_DIR, "copyright_en.txt"))
    copy_html = txt_to_html(copy_text, "Copyright &amp; About This Edition")
    copy_item = make_chapter("copyright", "copyright.xhtml",
                             "Copyright & About This Edition", copy_html)
    spine.append(copy_item)
    toc.append(copy_item)
    print("Added: Copyright")

    # ── Finalize ──────────────────────────────────────────────────────────────
    book.toc = toc

    # Only use EPUB3 Nav — skip the legacy NCX which generates broken EPUB/ prefixes
    nav = epub.EpubNav()
    book.add_item(nav)
    book.spine = [nav] + spine[1:]

    epub.write_epub(OUTPUT_FILE, book, {"epub3_landmark": False, "epub3_pages": False})

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\nEPUB created: {OUTPUT_FILE}")
    print(f"Size: {size_kb:.0f} KB")

if __name__ == "__main__":
    main()
