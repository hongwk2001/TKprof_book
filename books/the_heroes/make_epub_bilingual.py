# -*- coding: utf-8 -*-
"""
make_epub_bilingual.py
Compiles 'The Heroes: Greek Fairy Tales' into a publication-grade Bilingual EPUB3 eBook.
Renders strict 1:1 sentence-level matching pairs (en / kr) directly from the JSON dataset.
Adheres strictly to Google Play Books Partner Center ingestion & sanitization requirements.
"""

import os
import re
import json
import glob
import html
import uuid
import zipfile
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, 'json')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_EPUB = os.path.join(OUTPUT_DIR, 'the_heroes_bilingual.epub')

STYLE = """
@charset "utf-8";

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 1.05em;
    line-height: 1.65;
    margin: 1.5em 2em;
    color: #1a1a1a;
    background-color: #ffffff;
}

/* Cover Page */
.cover-page {
    margin: 0;
    padding: 0;
    text-align: center;
}
.cover-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
}
.cover-image {
    max-width: 100%;
    max-height: 100vh;
    height: auto;
    display: block;
    margin: 0 auto;
}

/* Title Page */
.title-page {
    text-align: center;
    margin-top: 3em;
    margin-bottom: 3em;
}
.main-title-en {
    font-size: 2em;
    font-weight: bold;
    color: #1a2c3d;
    margin-bottom: 0.2em;
}
.main-title-kr {
    font-size: 1.4em;
    font-weight: normal;
    color: #3b536b;
    margin-bottom: 1.5em;
}
.author-en {
    font-size: 1.2em;
    color: #333333;
    margin-bottom: 0.1em;
}
.author-kr {
    font-size: 1.05em;
    color: #666666;
    margin-bottom: 3em;
}
.publisher-info {
    font-size: 0.9em;
    color: #777777;
    margin-top: 4em;
}

/* Headings */
.chapter-header {
    text-align: center;
    margin-top: 2em;
    margin-bottom: 2.2em;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 1.5em;
}
h1.story-title {
    font-size: 1.6em;
    font-weight: bold;
    color: #1c2d42;
    margin-bottom: 0.3em;
}
.story-title-kr {
    font-size: 0.85em;
    font-weight: normal;
    color: #3b536b;
}
h2.part-title {
    font-size: 1.25em;
    font-weight: 600;
    color: #2c425e;
    margin-top: 0.5em;
    margin-bottom: 0.2em;
}
.part-title-kr {
    font-size: 0.85em;
    font-weight: normal;
    color: #475569;
}
h3.section-header {
    font-size: 1.1em;
    font-weight: bold;
    color: #1e293b;
    margin-top: 1.5em;
    margin-bottom: 0.8em;
}
.section-header-kr {
    font-size: 0.9em;
    font-weight: normal;
    color: #475569;
}

/* 1:1 Sentence Matching Layout */
.paragraph-block {
    margin-bottom: 1.6em;
    padding-bottom: 0.2em;
}
.sentence-pair {
    margin-bottom: 0.65em;
}
p.eng {
    margin: 0 0 0.18em 0;
    color: #1a1a1a;
    font-size: 1.05em;
    line-height: 1.6;
}
p.kor {
    margin: 0;
    color: #2b3e50;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif;
    font-size: 0.95em;
    line-height: 1.65;
    word-break: keep-all;
}

/* Illustrations */
.illustration-container {
    text-align: center;
    margin: 2.5em auto;
    max-width: 90%;
}
.illustration {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 0 auto 0.8em auto;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
.caption-eng {
    font-size: 0.9em;
    font-style: italic;
    color: #475569;
    margin: 0.3em 0 0.1em 0;
}
.caption-kor {
    font-size: 0.85em;
    color: #64748b;
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    margin: 0 0 1em 0;
}

/* Navigation Document */
nav#toc ol {
    list-style-type: none;
    padding-left: 0;
}
nav#toc ol ol {
    padding-left: 1.5em;
}
nav#toc li {
    margin-bottom: 0.6em;
}
nav#toc a {
    text-decoration: none;
    color: #1e3a8a;
}
nav#toc a:hover {
    text-decoration: underline;
}
"""

def clean_xml(text):
    if not text:
        return ""
    t = text.strip()
    return html.escape(t, quote=True)

def strip_outer_brackets(text):
    t = text.strip()
    if t.startswith('[') and t.endswith(']'):
        return t[1:-1].strip()
    return t

def main():
    print("=== Building Bilingual EPUB3 for 'The Heroes: Greek Fairy Tales' (1:1 Sentence Matching) ===")
    book_uuid = f"urn:uuid:{uuid.uuid4()}"
    modified_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1. Collect and parse JSON chapters
    json_paths = sorted(glob.glob(os.path.join(JSON_DIR, 'ch_*.json')))
    print(f"Found {len(json_paths)} chapter files.")

    chapters_data = []
    for jp in json_paths:
        with open(jp, 'r', encoding='utf-8') as f:
            data = json.load(f)
        chapters_data.append((os.path.basename(jp), data))

    # Stories grouping
    stories_map = {
        'Preface': {'title_en': 'Preface', 'title_kr': '머리말', 'chapters': []},
        'Story I: Perseus': {'title_en': 'Story I: Perseus', 'title_kr': '이야기 1: 페르세우스', 'chapters': []},
        'Story II: The Argonauts': {'title_en': 'Story II: The Argonauts', 'title_kr': '이야기 2: 아르고 호 원정대', 'chapters': []},
        'Story III: Theseus': {'title_en': 'Story III: Theseus', 'title_kr': '이야기 3: 테세우스', 'chapters': []}
    }

    # Process each chapter into XHTML
    html_chapters = []
    embedded_images = set()

    for fn, blocks in chapters_data:
        ch_stem = os.path.splitext(fn)[0] # e.g. ch_00
        ch_id = ch_stem
        xhtml_filename = f"{ch_stem}.xhtml"

        # Determine Story and Part title
        first_b = blocks[0]
        story_raw = first_b.get('story', 'Story')
        part_raw = first_b.get('part', 'Part')

        header_blocks = [b for b in blocks if b.get('is_header')]
        if header_blocks:
            h_trans = header_blocks[0]['translation'][0]
            header_en = strip_outer_brackets(h_trans['en'])
            header_kr = strip_outer_brackets(h_trans['kr'])
        else:
            header_en = part_raw
            header_kr = part_raw

        story_kr = '머리말' if 'Preface' in story_raw else ('이야기 1: 페르세우스' if 'Perseus' in story_raw else ('이야기 2: 아르고 호 원정대' if 'Argonauts' in story_raw else '이야기 3: 테세우스'))

        if 'Preface' in story_raw:
            s_key = 'Preface'
        elif 'Perseus' in story_raw:
            s_key = 'Story I: Perseus'
        elif 'Argonauts' in story_raw:
            s_key = 'Story II: The Argonauts'
        else:
            s_key = 'Story III: Theseus'

        stories_map[s_key]['chapters'].append((ch_id, xhtml_filename, header_en, header_kr))

        # Build XHTML body
        body_parts = []
        body_parts.append('<div class="chapter-header">')
        if s_key != 'Preface':
            body_parts.append(f'  <h1 class="story-title">{clean_xml(s_key)}<br /><span class="story-title-kr">{clean_xml(story_kr)}</span></h1>')
        body_parts.append(f'  <h2 class="part-title">{clean_xml(header_en)}<br /><span class="part-title-kr">{clean_xml(header_kr)}</span></h2>')
        body_parts.append('</div>')

        for b in blocks:
            if b.get('is_header'):
                continue

            # Check if this block is an illustration
            if 'image_color' in b or 'image' in b:
                img_rel = b.get('image_color') or b.get('image')
                img_name = os.path.basename(img_rel)
                full_img_path = os.path.join(IMAGES_DIR, img_name)

                if os.path.exists(full_img_path):
                    embedded_images.add(img_name)
                    trans = b.get('translation', [{}])[0]
                    cap_en = strip_outer_brackets(trans.get('en', 'Illustration'))
                    cap_kr = strip_outer_brackets(trans.get('kr', '삽화'))

                    body_parts.append('  <div class="illustration-container">')
                    body_parts.append(f'    <img src="../Images/{clean_xml(img_name)}" alt="{clean_xml(cap_en)}" class="illustration" />')
                    body_parts.append(f'    <p class="caption-eng">{clean_xml(cap_en)}</p>')
                    body_parts.append(f'    <p class="caption-kor">{clean_xml(cap_kr)}</p>')
                    body_parts.append('  </div>')
                continue

            # Regular paragraph block: render 1:1 sentence pairs!
            trans_list = b.get('translation', [])
            if not trans_list:
                continue

            # Group each paragraph block and iterate through matching 1:1 sentence pairs
            body_parts.append('  <div class="paragraph-block">')
            for t in trans_list:
                en_sent = t.get('en', '').strip()
                kr_sent = t.get('kr', '').strip()
                if not en_sent and not kr_sent:
                    continue
                body_parts.append('    <div class="sentence-pair">')
                if en_sent:
                    body_parts.append(f'      <p class="eng">{clean_xml(en_sent)}</p>')
                if kr_sent:
                    body_parts.append(f'      <p class="kor">{clean_xml(kr_sent)}</p>')
                body_parts.append('    </div>')
            body_parts.append('  </div>')

        # Assemble full XHTML
        doc_title = clean_xml(f"{s_key} - {header_en}")
        inner_body = "\n".join(body_parts)
        xhtml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <title>{doc_title}</title>
  <link rel="stylesheet" href="../Styles/main.css" type="text/css" />
</head>
<body>
{inner_body}
</body>
</html>"""
        html_chapters.append((ch_id, xhtml_filename, header_en, header_kr, s_key, xhtml_content.encode('utf-8')))

    print(f"Prepared {len(html_chapters)} XHTML chapter pages.")
    print(f"Identified {len(embedded_images)} embedded color illustrations.")

    # 2. Prepare Cover & Title Page
    cover_image_file = 'cover_color.jpg' if os.path.exists(os.path.join(IMAGES_DIR, 'cover_color.jpg')) else 'cover.jpg'
    embedded_images.add(cover_image_file)

    cover_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <title>Cover</title>
  <link rel="stylesheet" href="../Styles/main.css" type="text/css" />
</head>
<body class="cover-page">
  <div class="cover-container">
    <img src="../Images/{cover_image_file}" alt="Cover" class="cover-image" />
  </div>
</body>
</html>""".encode('utf-8')

    title_xhtml = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <title>Title Page</title>
  <link rel="stylesheet" href="../Styles/main.css" type="text/css" />
</head>
<body>
  <div class="title-page">
    <h1 class="main-title-en">The Heroes</h1>
    <h2 class="main-title-kr">그리스 영웅 이야기</h2>
    <p style="font-style: italic; color: #555; margin-bottom: 2em;">Greek Fairy Tales for My Children</p>
    <p class="author-en">Charles Kingsley</p>
    <p class="author-kr">찰스 킹슬리 지음 | TKPROF 현대어 1:1 대역판</p>
    <div class="publisher-info">
      <p>TKPROF LLC</p>
      <p>Modern English &amp; Korean Bilingual Illustrated Edition</p>
    </div>
  </div>
</body>
</html>""".encode('utf-8')

    # 3. Build EPUB 3 nav.xhtml
    nav_lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE html>',
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">',
        '<head>',
        '  <title>Table of Contents</title>',
        '  <link rel="stylesheet" href="../Styles/main.css" type="text/css" />',
        '</head>',
        '<body>',
        '  <nav epub:type="toc" id="toc">',
        '    <h1>목차 (Table of Contents)</h1>',
        '    <ol>',
        '      <li><a href="title.xhtml">Title Page</a></li>'
    ]

    for s_key in ['Preface', 'Story I: Perseus', 'Story II: The Argonauts', 'Story III: Theseus']:
        s_info = stories_map[s_key]
        if not s_info['chapters']:
            continue
        if s_key == 'Preface':
            ch_id, fn, h_en, h_kr = s_info['chapters'][0]
            nav_lines.append(f'      <li><a href="{fn}">{clean_xml(h_en)} ({clean_xml(h_kr)})</a></li>')
        else:
            nav_lines.append('      <li>')
            nav_lines.append(f'        <span><strong>{clean_xml(s_info["title_en"])} ({clean_xml(s_info["title_kr"])})</strong></span>')
            nav_lines.append('        <ol>')
            for ch_id, fn, h_en, h_kr in s_info['chapters']:
                nav_lines.append(f'          <li><a href="{fn}">{clean_xml(h_en)} ({clean_xml(h_kr)})</a></li>')
            nav_lines.append('        </ol>')
            nav_lines.append('      </li>')

    nav_lines.append('    </ol>')
    nav_lines.append('  </nav>')
    nav_lines.append('</body>')
    nav_lines.append('</html>')
    nav_xhtml = '\n'.join(nav_lines).encode('utf-8')

    # 4. Build EPUB 2 toc.ncx (for Google Play Books backward compatibility)
    ncx_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">',
        '  <head>',
        f'    <meta name="dtb:uid" content="{book_uuid}"/>',
        '    <meta name="dtb:depth" content="2"/>',
        '    <meta name="dtb:totalPageCount" content="0"/>',
        '    <meta name="dtb:maxPageNumber" content="0"/>',
        '  </head>',
        '  <docTitle><text>The Heroes: Greek Fairy Tales</text></docTitle>',
        '  <navMap>'
    ]

    play_order = 1
    ncx_lines.append(f'    <navPoint id="np-title" playOrder="{play_order}">')
    ncx_lines.append('      <navLabel><text>Title Page</text></navLabel>')
    ncx_lines.append('      <content src="Text/title.xhtml"/>')
    ncx_lines.append('    </navPoint>')
    play_order += 1

    for s_key in ['Preface', 'Story I: Perseus', 'Story II: The Argonauts', 'Story III: Theseus']:
        s_info = stories_map[s_key]
        if not s_info['chapters']:
            continue
        if s_key == 'Preface':
            ch_id, fn, h_en, h_kr = s_info['chapters'][0]
            ncx_lines.append(f'    <navPoint id="np-{ch_id}" playOrder="{play_order}">')
            ncx_lines.append(f'      <navLabel><text>{clean_xml(h_en)} ({clean_xml(h_kr)})</text></navLabel>')
            ncx_lines.append(f'      <content src="Text/{fn}"/>')
            ncx_lines.append('    </navPoint>')
            play_order += 1
        else:
            s_slug = s_key.split(':')[0].replace(' ', '').lower()
            ncx_lines.append(f'    <navPoint id="np-{s_slug}" playOrder="{play_order}">')
            ncx_lines.append(f'      <navLabel><text>{clean_xml(s_info["title_en"])} ({clean_xml(s_info["title_kr"])})</text></navLabel>')
            first_ch_fn = s_info['chapters'][0][1]
            ncx_lines.append(f'      <content src="Text/{first_ch_fn}"/>')
            play_order += 1
            for ch_id, fn, h_en, h_kr in s_info['chapters']:
                ncx_lines.append(f'      <navPoint id="np-{ch_id}" playOrder="{play_order}">')
                ncx_lines.append(f'        <navLabel><text>{clean_xml(h_en)} ({clean_xml(h_kr)})</text></navLabel>')
                ncx_lines.append(f'        <content src="Text/{fn}"/>')
                ncx_lines.append('      </navPoint>')
                play_order += 1
            ncx_lines.append('    </navPoint>')

    ncx_lines.append('  </navMap>')
    ncx_lines.append('</ncx>')
    toc_ncx = '\n'.join(ncx_lines).encode('utf-8')

    # 5. Build content.opf
    manifest_items = [
        '    <item id="style" href="Styles/main.css" media-type="text/css"/>',
        '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '    <item id="nav" href="Text/nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '    <item id="cover" href="Text/cover.xhtml" media-type="application/xhtml+xml"/>',
        '    <item id="title" href="Text/title.xhtml" media-type="application/xhtml+xml"/>'
    ]

    spine_items = [
        '    <itemref idref="cover"/>',
        '    <itemref idref="title"/>'
    ]

    for ch_id, xhtml_filename, _, _, _, _ in html_chapters:
        manifest_items.append(f'    <item id="{ch_id}" href="Text/{xhtml_filename}" media-type="application/xhtml+xml"/>')
        spine_items.append(f'    <itemref idref="{ch_id}"/>')

    for img_name in sorted(list(embedded_images)):
        img_id = re.sub(r'[^a-zA-Z0-9_-]', '_', os.path.splitext(img_name)[0])
        ext = os.path.splitext(img_name)[1].lower()
        mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
        if img_name == cover_image_file:
            manifest_items.append(f'    <item id="cover-image" href="Images/{img_name}" media-type="{mime}" properties="cover-image"/>')
        else:
            manifest_items.append(f'    <item id="img_{img_id}" href="Images/{img_name}" media-type="{mime}"/>')

    manifest_str = '\n'.join(manifest_items)
    spine_str = '\n'.join(spine_items)

    opf_lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="pub-id" version="3.0">',
        '  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">',
        f'    <dc:identifier id="pub-id">{book_uuid}</dc:identifier>',
        '    <dc:title>The Heroes: Greek Fairy Tales (그리스 영웅 이야기)</dc:title>',
        '    <dc:language>en</dc:language>',
        '    <dc:language>ko</dc:language>',
        '    <dc:creator id="author">Charles Kingsley (찰스 킹슬리)</dc:creator>',
        '    <meta refines="#author" property="role" scheme="marc:relators">aut</meta>',
        '    <dc:publisher>TKPROF LLC</dc:publisher>',
        f'    <dc:date>{datetime.now(timezone.utc).strftime("%Y-%m-%d")}</dc:date>',
        '    <dc:rights>Korean translation and modernized English edition Copyright 2026 TKPROF LLC. Original illustrations and stories public domain.</dc:rights>',
        '    <dc:description>찰스 킹슬리의 고전 명작 그리스 영웅 이야기 (페르세우스, 아르고 호 원정대와 이아손, 테세우스). 현대 영어와 정갈한 한국어 문장별 1:1 완벽 대역본 및 복원된 컬러 원작 삽화 수록.</dc:description>',
        '    <dc:subject>그리스 신화</dc:subject>',
        '    <dc:subject>영어 대역본</dc:subject>',
        '    <dc:subject>Bilingual Classic</dc:subject>',
        '    <dc:subject>Greek Mythology</dc:subject>',
        f'    <meta property="dcterms:modified">{modified_time}</meta>',
        '    <meta name="cover" content="cover-image"/>',
        '  </metadata>',
        '  <manifest>',
        manifest_str,
        '  </manifest>',
        '  <spine toc="ncx">',
        spine_str,
        '  </spine>',
        '</package>'
    ]
    content_opf = '\n'.join(opf_lines).encode('utf-8')

    # 6. Container XML
    container_xml = """<?xml version="1.0" encoding="utf-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>""".encode('utf-8')

    # 7. Write to Zip Archive
    print(f"Writing EPUB archive to: {OUTPUT_EPUB}")
    if os.path.exists(OUTPUT_EPUB):
        os.remove(OUTPUT_EPUB)

    with zipfile.ZipFile(OUTPUT_EPUB, 'w') as zf:
        # 1. mimetype: MUST be FIRST, MUST be UNCOMPRESSED
        zf.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        # 2. META-INF/container.xml
        zf.writestr('META-INF/container.xml', container_xml, compress_type=zipfile.ZIP_DEFLATED)

        # 3. OEBPS files
        zf.writestr('OEBPS/content.opf', content_opf, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/toc.ncx', toc_ncx, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Styles/main.css', STYLE.strip().encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Text/nav.xhtml', nav_xhtml, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Text/cover.xhtml', cover_xhtml, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/Text/title.xhtml', title_xhtml, compress_type=zipfile.ZIP_DEFLATED)

        # Chapter XHTML files
        for ch_id, xhtml_filename, _, _, _, xhtml_bytes in html_chapters:
            zf.writestr(f'OEBPS/Text/{xhtml_filename}', xhtml_bytes, compress_type=zipfile.ZIP_DEFLATED)

        # Images
        for img_name in sorted(list(embedded_images)):
            img_path = os.path.join(IMAGES_DIR, img_name)
            if os.path.exists(img_path):
                with open(img_path, 'rb') as img_f:
                    zf.writestr(f'OEBPS/Images/{img_name}', img_f.read(), compress_type=zipfile.ZIP_DEFLATED)
                print(f"  + Bundled Image: {img_name}")
            else:
                print(f"  ! WARNING: Image not found: {img_path}")

    size_mb = os.path.getsize(OUTPUT_EPUB) / (1024 * 1024)
    print(f"\nSUCCESS: 1:1 Sentence Matching EPUB successfully built!")
    print(f"File: {OUTPUT_EPUB}")
    print(f"Size: {size_mb:.2f} MB")

if __name__ == '__main__':
    main()
