import os
import re
import zipfile
import uuid
import datetime

drafts_dir = 'drafts'
output_epub = 'The_Muqaddimah_Retold.epub'

CHAPTERS = [
    ('00_introduction.md',  'Introduction'),
    ('chapter_1_draft.md',  'Chapter 1: Who Was This Guy?'),
    ('chapter_2_draft.md',  'Chapter 2: What Is Asabiyyah?'),
    ('chapter_3_draft.md',  'Chapter 3: How Empires Are Born'),
    ('chapter_4_draft.md',  'Chapter 4: The Luxury Trap'),
    ('chapter_5_draft.md',  'Chapter 5: Elite Overproduction'),
    ('chapter_6_draft.md',  'Chapter 6: The 3-Generation Rule'),
    ('chapter_7_draft.md',  "Chapter 7: Who's Next?"),
    ('08_readers_guide.md', "Appendix A: Reader's Guide"),
    ('09_copyright.md',     'Copyright & Editorial Notes'),
]

CSS = '''body {
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.7;
  margin: 0 auto;
  max-width: 38em;
  padding: 2em 1em;
  color: #222;
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
em { font-style: italic; }'''


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
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>{title}</title>
  <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
{body_html}
</body>
</html>'''


epub_uuid = str(uuid.uuid4())
date_str = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

chapter_files = []
for md_filename, nav_title in CHAPTERS:
    xhtml_name = md_filename.replace('.md', '.xhtml')
    filepath = os.path.join(drafts_dir, md_filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        md_text = f.read()

    first_line = md_text.split('\n')[0]
    page_title = first_line[2:].strip() if first_line.startswith('# ') else nav_title

    body_html = md_to_html(md_text)
    xhtml_content = make_xhtml(page_title, body_html)
    chapter_files.append((xhtml_name, nav_title, xhtml_content))

manifest_items = (
    '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>\n'
    '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>\n'
    '    <item id="css" href="styles.css" media-type="text/css"/>\n'
)
for i, (xhtml_name, _, _) in enumerate(chapter_files):
    manifest_items += f'    <item id="ch{i:02d}" href="{xhtml_name}" media-type="application/xhtml+xml"/>\n'

spine_items = ''.join(
    f'    <itemref idref="ch{i:02d}"/>\n' for i in range(len(chapter_files))
)

content_opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="BookID">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">
    <dc:title>The Collapse Code: Ibn Khaldun\'s Formula for Why Civilizations Fall</dc:title>
    <dc:creator>Based on Ibn Khaldun\'s Muqaddimah</dc:creator>
    <dc:language>en</dc:language>
    <dc:identifier id="BookID">urn:uuid:{epub_uuid}</dc:identifier>
    <dc:subject>History; Civilization; Political Philosophy; Social Theory</dc:subject>
    <dc:description>Ibn Khaldun cracked the code of civilizational collapse in 1377. This book applies his framework to Rome, the Mongols, Apple, Samsung, and the world order today.</dc:description>
    <meta property="dcterms:modified">{date_str}</meta>
  </metadata>
  <manifest>
{manifest_items}  </manifest>
  <spine toc="ncx">
{spine_items}  </spine>
</package>'''

ncx_nav_points = ''.join(
    f'''    <navPoint id="np{i}" playOrder="{i+1}">
      <navLabel><text>{nav_title}</text></navLabel>
      <content src="{xhtml_name}"/>
    </navPoint>\n'''
    for i, (xhtml_name, nav_title, _) in enumerate(chapter_files)
)

toc_ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:{epub_uuid}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>The Collapse Code</text></docTitle>
  <navMap>
{ncx_nav_points}  </navMap>
</ncx>'''

nav_items = ''.join(
    f'      <li><a href="{xhtml_name}">{nav_title}</a></li>\n'
    for xhtml_name, nav_title, _ in chapter_files
)

nav_xhtml = f'''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Table of Contents</title>
  <link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
  <nav epub:type="toc" id="toc">
    <h1>Table of Contents</h1>
    <ol>
{nav_items}    </ol>
  </nav>
</body>
</html>'''

container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''

with zipfile.ZipFile(output_epub, 'w', zipfile.ZIP_DEFLATED) as epub:
    epub.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
    epub.writestr('META-INF/container.xml', container_xml)
    epub.writestr('OEBPS/content.opf', content_opf)
    epub.writestr('OEBPS/toc.ncx', toc_ncx)
    epub.writestr('OEBPS/nav.xhtml', nav_xhtml)
    epub.writestr('OEBPS/styles.css', CSS)
    for xhtml_name, _, xhtml_content in chapter_files:
        epub.writestr(f'OEBPS/{xhtml_name}', xhtml_content)

print(f"Successfully compiled {output_epub} with {len(chapter_files)} chapters!")
