"""
make_epub_greatest_hits.py
Compiles The Muqaddimah: Greatest Hits Edition into an EPUB.
Mirrors books/blue_castle/make_epub_native.py structure (Google Books compatible).
"""

import os
import re
import zipfile
import uuid
from datetime import datetime, timezone

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DRAFTS_DIR  = os.path.join(BASE_DIR, "book2_greatest_hits")
OUTPUT_FILE = os.path.join(BASE_DIR, "The_Muqaddimah_Greatest_Hits.epub")

BOOK_TITLE    = "The Muqaddimah: Essential Passages in Plain English"
BOOK_SUBTITLE = "The Ideas That Made It the Most Important Book You’ve Never Read"
BOOK_CREATOR  = "Ibn Khaldun (rendered by TKPROF)"
BOOK_NCX_UID  = "tkprof-muqaddimah-greatest-hits-en-2026"

# ── Chapter list ──────────────────────────────────────────────────────────────
# (md_filename, uid, nav_title)
CHAPTERS = [
    ("00_editors_note.md",              "p00", "Editor's Note"),
    ("01_why_i_wrote_this.md",          "p01", "Why I Wrote This Book"),
    ("02_what_is_asabiyyah.md",         "p02", "What Is Asabiyyah?"),
    ("03_desert_people_braver.md",      "p03", "Why Desert People Are Braver"),
    ("04_asabiyyah_creates_leadership.md","p04","How Asabiyyah Creates Leadership"),
    ("05_desert_conquers_city.md",      "p05", "The Desert Man Conquers the City"),
    ("06_religion_supercharges.md",     "p06", "Why Religion Supercharges Asabiyyah"),
    ("07_dynasties_born.md",            "p07", "How Dynasties Are Born"),
    ("08_ruler_hoards_glory.md",        "p08", "The Ruler Who Hoards All the Glory"),
    ("09_city_life_destroys.md",        "p09", "Why City Life Destroys Fighting Spirit"),
    ("10_three_generations.md",         "p10", "The Three Generations"),
    ("11_taxation_kills.md",            "p11", "How Taxation Kills the Dynasty"),
    ("12_hired_soldiers.md",            "p12", "The Hired Soldiers Problem"),
    ("13_senility_of_dynasties.md",     "p13", "The Senility of Dynasties"),
    ("14_cycle_begins_again.md",        "p14", "The Cycle Begins Again"),
    ("15_about_the_source.md",          "p15", "About the Source"),
    ("16_copyright.md",                 "p16", "Copyright"),
]

# ── CSS Style ─────────────────────────────────────────────────────────────────
STYLE = """
body {
    font-family: Georgia, 'Times New Roman', serif;
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
    margin-bottom: 0.4em;
    color: #2c1a0e;
}

h2 {
    font-size: 1.25em;
    font-weight: bold;
    margin-top: 2em;
    margin-bottom: 0.5em;
    color: #3a2a1a;
    border-bottom: 1px solid #ccc;
    padding-bottom: 4px;
}

h3 {
    font-size: 1.1em;
    font-weight: bold;
    margin-top: 1.5em;
    margin-bottom: 0.4em;
    color: #4a3a2a;
}

p {
    margin: 0 0 1em 0;
    text-indent: 1.5em;
}

h1 + p, h2 + p, h3 + p, hr + p {
    text-indent: 0;
}

em {
    font-style: italic;
}

p.subtitle {
    text-align: center;
    text-indent: 0;
    color: #5a4a3a;
    margin-bottom: 1.5em;
}

blockquote {
    font-style: italic;
    background: #f4f1eb;
    border-left: 4px solid #8b6040;
    margin: 1.5em 0;
    padding: 0.8em 1.2em;
}

blockquote p {
    text-indent: 0;
    margin: 0.5em 0;
}

ul {
    margin: 0.8em 0 0.8em 2em;
    padding: 0;
}

li {
    margin: 0.3em 0;
}

hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 2em 0;
}
"""

# ── Helpers ───────────────────────────────────────────────────────────────────
def esc(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text

def inline_md(text):
    text = esc(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+?)\*',  r'<em>\1</em>', text)
    return text

def read_md(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def md_to_html(text, nav_title):
    lines = text.split("\n")
    parts = []
    in_blockquote = False
    in_list = False
    first_content = True  # track whether we've passed the h1 skip

    parts.append(f"<h1>{esc(nav_title)}</h1>")

    for line in lines:
        raw = line.rstrip()

        is_bq = raw.startswith(">")
        is_li = bool(re.match(r"^[-*\+] ", raw))

        if in_blockquote and not is_bq:
            parts.append("</blockquote>")
            in_blockquote = False
        if in_list and not is_li:
            parts.append("</ul>")
            in_list = False

        if raw.startswith("### "):
            parts.append(f"<h3>{inline_md(raw[4:].strip())}</h3>")
        elif raw.startswith("## "):
            parts.append(f"<h2>{inline_md(raw[3:].strip())}</h2>")
        elif raw.startswith("# "):
            # Skip markdown h1 — already emitted nav_title
            pass
        elif re.match(r"^---+$", raw.strip()):
            parts.append("<hr/>")
        elif is_bq:
            if not in_blockquote:
                parts.append("<blockquote>")
                in_blockquote = True
            content = raw.lstrip(">").strip()
            if content:
                parts.append(f"<p>{inline_md(content)}</p>")
        elif is_li:
            if not in_list:
                parts.append("<ul>")
                in_list = True
            item_text = re.sub(r"^[-*\+] ", "", raw).strip()
            parts.append(f"<li>{inline_md(item_text)}</li>")
        elif raw.strip():
            # Detect italic-only lines (passage subtitles) — render centered
            stripped = raw.strip()
            if re.match(r"^\*.+\*$", stripped) and not stripped.startswith("**"):
                inner = stripped[1:-1]
                parts.append(f"<p class=\"subtitle\"><em>{esc(inner)}</em></p>")
            else:
                parts.append(f"<p>{inline_md(stripped)}</p>")

    if in_blockquote:
        parts.append("</blockquote>")
    if in_list:
        parts.append("</ul>")

    return "\n".join(parts)

def make_xhtml(title, body_content):
    return "\n".join([
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head>",
        f"  <title>{esc(title)}</title>",
        "  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        "</head>",
        "<body>",
        body_content,
        "</body>",
        "</html>",
    ])

# ── Build EPUB ─────────────────────────────────────────────────────────────────
def main():
    print("Building Greatest Hits EPUB...")

    chapters = []

    for md_file, uid, nav_title in CHAPTERS:
        path = os.path.join(DRAFTS_DIR, md_file)
        if not os.path.exists(path):
            print(f"  WARNING: {md_file} not found, skipping.")
            continue
        md_text = read_md(path)
        body    = md_to_html(md_text, nav_title)
        xhtml   = make_xhtml(nav_title, body)
        chapters.append({'id': uid, 'href': f"Text/{uid}.xhtml", 'title': nav_title, 'content': xhtml})

    book_uuid     = f"urn:uuid:{uuid.uuid4()}"
    modified_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Cover / title page
    cover_html = "\n".join([
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head>",
        "  <title>The Muqaddimah: Essential Passages in Plain English</title>",
        "  <link rel=\"stylesheet\" href=\"../Styles/main.css\" type=\"text/css\"/>",
        "</head>",
        "<body>",
        "  <h1>The Muqaddimah</h1>",
        "  <h2 style=\"text-align:center; border:none;\">Essential Passages in Plain English</h2>",
        "  <p style=\"text-align:center; text-indent:0; font-style:italic;\">The Ideas That Made It the Most Important Book You’ve Never Read</p>",
        "  <p style=\"text-align:center; text-indent:0;\">Ibn Khaldun</p>",
        "  <p style=\"text-align:center; text-indent:0;\">Rendered by TKPROF &mdash; 2026</p>",
        "</body>",
        "</html>",
    ])

    # ── OPF ───────────────────────────────────────────────────────────────────
    opf_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<package xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"pub-id\" version=\"3.0\">",
        "  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\">",
        f"    <dc:identifier id=\"pub-id\">{book_uuid}</dc:identifier>",
        f"    <dc:title>{esc(BOOK_TITLE)}</dc:title>",
        "    <dc:language>en</dc:language>",
        f"    <dc:creator>{esc(BOOK_CREATOR)}</dc:creator>",
        "    <dc:publisher>TKPROF LLC</dc:publisher>",
        "    <dc:date>2026</dc:date>",
        "    <dc:rights>Copyright 2026 TKPROF LLC. All rights reserved.</dc:rights>",
        "    <dc:subject>History</dc:subject>",
        "    <dc:subject>Political Philosophy</dc:subject>",
        "    <dc:subject>Islamic Civilization</dc:subject>",
        "    <dc:description>Fourteen essential passages from Ibn Khaldun's Muqaddimah — the 14th-century masterwork on why civilizations rise and fall — rendered in plain modern English.</dc:description>",
        f"    <meta property=\"dcterms:modified\">{modified_date}</meta>",
        "  </metadata>",
        "  <manifest>",
        "    <item id=\"cover\" href=\"Text/cover.xhtml\"  media-type=\"application/xhtml+xml\"/>",
        "    <item id=\"ncx\"   href=\"toc.ncx\"           media-type=\"application/x-dtbncx+xml\"/>",
        "    <item id=\"nav\"   href=\"nav.xhtml\"          media-type=\"application/xhtml+xml\" properties=\"nav\"/>",
        "    <item id=\"css\"   href=\"Styles/main.css\"   media-type=\"text/css\"/>",
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

    # ── NCX ───────────────────────────────────────────────────────────────────
    ncx_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">",
        "  <head>",
        f"    <meta name=\"dtb:uid\" content=\"{BOOK_NCX_UID}\"/>",
        "    <meta name=\"dtb:depth\" content=\"1\"/>",
        "    <meta name=\"dtb:totalPageCount\" content=\"0\"/>",
        "    <meta name=\"dtb:maxPageNumber\" content=\"0\"/>",
        "  </head>",
        "  <docTitle><text>The Muqaddimah: Essential Passages in Plain English</text></docTitle>",
        "  <navMap>",
    ]
    for idx, ch in enumerate(chapters, 1):
        ncx_parts.append(f"    <navPoint id=\"navpoint-{idx}\" playOrder=\"{idx}\">")
        ncx_parts.append(f"      <navLabel><text>{esc(ch['title'])}</text></navLabel>")
        ncx_parts.append(f"      <content src=\"{ch['href']}\"/>")
        ncx_parts.append(f"    </navPoint>")
    ncx_parts.append("  </navMap>")
    ncx_parts.append("</ncx>")
    ncx_content = "\n".join(ncx_parts)

    # ── Nav ───────────────────────────────────────────────────────────────────
    nav_parts = [
        "<?xml version='1.0' encoding='utf-8'?>",
        "<!DOCTYPE html>",
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\">",
        "<head><title>Table of Contents</title></head>",
        "<body>",
        "  <nav epub:type=\"toc\" id=\"toc\">",
        "    <h2>Table of Contents</h2>",
        "    <ol>",
    ]
    for ch in chapters:
        nav_parts.append(f"      <li><a href=\"{ch['href']}\">{esc(ch['title'])}</a></li>")
    nav_parts.append("    </ol>")
    nav_parts.append("  </nav>")
    nav_parts.append("</body>")
    nav_parts.append("</html>")
    nav_content = "\n".join(nav_parts)

    # ── container.xml ─────────────────────────────────────────────────────────
    container_xml = (
        "<?xml version='1.0' encoding='utf-8'?>\n"
        "<container xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\" version=\"1.0\">\n"
        "  <rootfiles>\n"
        "    <rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\"/>\n"
        "  </rootfiles>\n"
        "</container>"
    )

    # ── Write zip (same order as blue_castle) ─────────────────────────────────
    with zipfile.ZipFile(OUTPUT_FILE, 'w') as zf:
        zf.writestr('mimetype',                  b'application/epub+zip',         compress_type=zipfile.ZIP_STORED)
        zf.writestr('META-INF/container.xml',    container_xml.encode('utf-8'),   compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Text/cover.xhtml',    cover_html.encode('utf-8'),      compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/content.opf',         opf_content.encode('utf-8'),     compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/toc.ncx',             ncx_content.encode('utf-8'),     compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/nav.xhtml',           nav_content.encode('utf-8'),     compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Styles/main.css',     STYLE.encode('utf-8'),           compress_type=zipfile.ZIP_DEFLATED)
        for ch in chapters:
            zf.writestr(f"OEBPS/{ch['href']}",  ch['content'].encode('utf-8'),   compress_type=zipfile.ZIP_DEFLATED)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\nEPUB created: {OUTPUT_FILE}")
    print(f"Size: {size_kb:.0f} KB  |  Chapters: {len(chapters)}")

if __name__ == "__main__":
    main()
