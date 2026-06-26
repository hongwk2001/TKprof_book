"""
make_epub.py
Compiles The Collapse Code into a Google Books / KDP compatible EPUB3.
"""

import os
import re
import zipfile
import uuid
from datetime import datetime, timezone

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DRAFTS_DIR  = os.path.join(BASE_DIR, 'drafts')
OUTPUT_FILE = os.path.join(BASE_DIR, 'The_Muqaddimah_Retold.epub')

CHAPTERS = [
    ('00_introduction.md',  'Introduction'),
    ('chapter_1_draft.md',  'Chapter 1: Who Was This Guy?'),
    ('chapter_2_draft.md',  'Chapter 2: What Is Asabiyyah?'),
    ('chapter_3_draft.md',  'Chapter 3: How Empires Are Born'),
    ('chapter_4_draft.md',  'Chapter 4: The Luxury Trap'),
    ('chapter_5_draft.md',  'Chapter 5: Elite Overproduction'),
    ('chapter_6_draft.md',  'Chapter 6: The 3-Generation Rule'),
    ('chapter_7_draft.md',  "Chapter 7: Who's Next?"),
    ('08_readers_guide.md', "Appendix: Reader's Guide"),
    ('09_copyright.md',     'Copyright & Editorial Notes'),
]

CSS = """\
body {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 1em;
  line-height: 1.7;
  margin: 1.5em 2em;
  color: #222;
  background-color: #fdfaf5;
}
h1 {
  font-size: 1.8em;
  text-align: center;
  margin-top: 2em;
  margin-bottom: 0.5em;
  line-height: 1.3;
}
h2 {
  font-size: 1.3em;
  margin-top: 2em;
  border-bottom: 1px solid #ccc;
  padding-bottom: 4px;
}
h3 {
  font-size: 1.1em;
  margin-top: 1.5em;
}
p {
  margin: 0.8em 0;
  text-indent: 1.5em;
}
h1 + p, h2 + p, h3 + p, blockquote + p, ul + p {
  text-indent: 0;
}
blockquote {
  font-style: italic;
  background: #f9f9f9;
  border-left: 4px solid #aaa;
  margin: 1.5em 0;
  padding: 0.8em 1.2em;
}
blockquote p {
  text-indent: 0;
  margin: 0.5em 0;
}
ul {
  margin: 1em 0 1em 2em;
  padding: 0;
}
li {
  margin: 0.4em 0;
}
strong { font-weight: bold; }
em { font-style: italic; }"""


def inline_md(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', text)
    return text


def md_to_html(text):
    lines = text.split('\n')
    out = []
    in_blockquote = False
    in_list = False

    for line in lines:
        is_bq = line.startswith('>')
        is_li = bool(re.match(r'^[-*] ', line))

        if in_blockquote and not is_bq:
            out.append('</blockquote>')
            in_blockquote = False
        if in_list and not is_li:
            out.append('</ul>')
            in_list = False

        if line.startswith('### '):
            out.append(f'<h3>{inline_md(line[4:].strip())}</h3>')
        elif line.startswith('## '):
            out.append(f'<h2>{inline_md(line[3:].strip())}</h2>')
        elif line.startswith('# '):
            out.append(f'<h1>{inline_md(line[2:].strip())}</h1>')
        elif is_bq:
            if not in_blockquote:
                out.append('<blockquote>')
                in_blockquote = True
            content = line.lstrip('>').strip()
            if content:
                out.append(f'<p>{inline_md(content)}</p>')
        elif is_li:
            if not in_list:
                out.append('<ul>')
                in_list = True
            out.append(f'<li>{inline_md(line[2:].strip())}</li>')
        elif line.strip():
            out.append(f'<p>{inline_md(line.strip())}</p>')

    if in_blockquote:
        out.append('</blockquote>')
    if in_list:
        out.append('</ul>')

    return '\n'.join(out)


def make_xhtml(title, body_html):
    return f"""<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>{title}</title>
  <link rel="stylesheet" href="../Styles/main.css" type="text/css"/>
</head>
<body>
{body_html}
</body>
</html>"""


def main():
    book_uuid     = f"urn:uuid:{uuid.uuid4()}"
    modified_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Build chapter list
    chapters = []
    for md_filename, nav_title in CHAPTERS:
        uid       = md_filename.replace('.md', '').replace('_draft', '').replace('_', '-')
        href      = f"Text/{md_filename.replace('.md', '.xhtml')}"
        filepath  = os.path.join(DRAFTS_DIR, md_filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            md_text = f.read()
        first_line = md_text.split('\n')[0]
        page_title = first_line[2:].strip() if first_line.startswith('# ') else nav_title
        body_html  = md_to_html(md_text)
        xhtml      = make_xhtml(page_title, body_html)
        chapters.append({'id': uid, 'href': href, 'title': nav_title, 'content': xhtml})

    # content.opf
    manifest_items = [
        '    <item id="ncx"  href="toc.ncx"       media-type="application/x-dtbncx+xml"/>',
        '    <item id="nav"  href="nav.xhtml"      media-type="application/xhtml+xml" properties="nav"/>',
        '    <item id="css"  href="Styles/main.css" media-type="text/css"/>',
    ]
    for ch in chapters:
        manifest_items.append(f'    <item id="{ch["id"]}" href="{ch["href"]}" media-type="application/xhtml+xml"/>')

    spine_items = '\n'.join(f'    <itemref idref="{ch["id"]}"/>' for ch in chapters)

    content_opf = f"""<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="pub-id" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">{book_uuid}</dc:identifier>
    <dc:title>The Collapse Code: Ibn Khaldun's Formula for Why Civilizations Fall</dc:title>
    <dc:creator>Based on Ibn Khaldun's Muqaddimah</dc:creator>
    <dc:publisher>TKPROF LLC</dc:publisher>
    <dc:language>en</dc:language>
    <dc:date>2026</dc:date>
    <dc:subject>History</dc:subject>
    <dc:subject>Civilization</dc:subject>
    <dc:subject>Political Philosophy</dc:subject>
    <dc:subject>Social Theory</dc:subject>
    <dc:description>Ibn Khaldun cracked the code of civilizational collapse in 1377. This book applies his framework to Rome, the Mongols, Apple, Samsung, and the world order today.</dc:description>
    <meta property="dcterms:modified">{modified_date}</meta>
  </metadata>
  <manifest>
{chr(10).join(manifest_items)}
  </manifest>
  <spine toc="ncx">
{spine_items}
  </spine>
</package>"""

    # toc.ncx
    ncx_navpoints = []
    for idx, ch in enumerate(chapters, 1):
        ncx_navpoints.append(f"""    <navPoint id="navpoint-{idx}" playOrder="{idx}">
      <navLabel><text>{ch['title']}</text></navLabel>
      <content src="{ch['href']}"/>
    </navPoint>""")

    toc_ncx = f"""<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="{book_uuid}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>The Collapse Code</text></docTitle>
  <navMap>
{chr(10).join(ncx_navpoints)}
  </navMap>
</ncx>"""

    # nav.xhtml
    nav_items = '\n'.join(f'      <li><a href="{ch["href"]}">{ch["title"]}</a></li>' for ch in chapters)
    nav_xhtml = f"""<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Table of Contents</title>
  <link rel="stylesheet" href="Styles/main.css" type="text/css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Table of Contents</h1>
    <ol>
{nav_items}
    </ol>
  </nav>
</body>
</html>"""

    container_xml = """<?xml version='1.0' encoding='utf-8'?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""

    # Write EPUB
    with zipfile.ZipFile(OUTPUT_FILE, 'w') as zf:
        # mimetype must be first and uncompressed
        zf.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        zf.writestr('META-INF/container.xml',  container_xml.encode('utf-8'),  compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/content.opf',       content_opf.encode('utf-8'),   compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/toc.ncx',           toc_ncx.encode('utf-8'),       compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/nav.xhtml',         nav_xhtml.encode('utf-8'),     compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Styles/main.css',   CSS.encode('utf-8'),           compress_type=zipfile.ZIP_DEFLATED)
        for ch in chapters:
            zf.writestr(f"OEBPS/{ch['href']}", ch['content'].encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"EPUB created: {OUTPUT_FILE}")
    print(f"Size: {size_kb:.0f} KB  |  Chapters: {len(chapters)}")


if __name__ == '__main__':
    main()
