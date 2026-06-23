import os
import sys
import re
import zipfile
import argparse

# Force UTF-8 standard output for handling bilingual text logging
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\git_repo\TKprof_book\books"

CSS_CONTENT = """
body {
    font-family: "Georgia", "Times New Roman", serif;
    margin: 20px;
    line-height: 1.7;
    color: #111111;
}
h1 {
    text-align: center;
    color: #2c3e50;
    font-size: 1.8em;
    margin-top: 2em;
    margin-bottom: 1em;
    border-bottom: 1px solid #eeeeee;
    padding-bottom: 0.3em;
}
p {
    margin-bottom: 1.2em;
    text-indent: 1.5em;
    font-size: 1.05em;
}
p:first-of-type {
    text-indent: 0;
}
.cover-container {
    text-align: center;
    margin-top: 3em;
}
.cover-img {
    max-width: 100%;
    height: auto;
}
"""

CONTAINER_XML = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

def clean_xml_text(text):
    """Escapes XML special characters."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text

def parse_paragraphs(file_path):
    """Reads a text file and returns a list of paragraphs."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    
    # Split by double newlines or multiple empty lines
    raw_paras = re.split(r'\n\s*\n', content)
    paras = []
    for p in raw_paras:
        clean_p = p.replace('\n', ' ').strip()
        if clean_p:
            paras.append(clean_p)
    return paras

def compile_book(book_id):
    book_path = os.path.join(BASE_DIR, book_id)
    chapters_dir = os.path.join(book_path, "chapters")
    intro_file = os.path.join(book_path, "introduction_en.txt")
    copyright_file = os.path.join(book_path, "copyright_en.txt")
    
    if not os.path.exists(chapters_dir):
        print(f"Error: Chapters directory not found for {book_id}")
        return False
        
    # Get sorted list of English files
    en_files = sorted(glob_files(chapters_dir, "ch_*_en.txt") + glob_files(chapters_dir, "book*_ch_*_en.txt"))
    
    if not en_files:
        print(f"Error: No English chapter text files found in {chapters_dir}")
        return False
        
    print(f"Found {len(en_files)} chapters for {book_id}.")
    
    # Find cover image
    cover_image_path = None
    for file in os.listdir(book_path):
        if "cover" in file.lower() and file.endswith(('.png', '.jpg', '.jpeg')):
            cover_image_path = os.path.join(book_path, file)
            break
            
    # Manifest files list
    manifest_items = []
    spine_items = []
    
    # Create output directory
    output_dir = os.path.join(book_path, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # File name outputs
    epub_filename = f"{book_id}.epub"
    epub_path = os.path.join(output_dir, epub_filename)
    html_path = os.path.join(output_dir, f"{book_id}.html")
    
    # HTML compilation content
    html_chapters_body = []
    
    # We will write files inside memory/zip structure directly
    with zipfile.ZipFile(epub_path, 'w', zipfile.ZIP_DEFLATED) as epub:
        # 1. mimetype (MUST be first, uncompressed)
        epub.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        
        # 2. META-INF/container.xml
        epub.writestr('META-INF/container.xml', CONTAINER_XML)
        
        # 3. OEBPS/style.css
        epub.writestr('OEBPS/style.css', CSS_CONTENT)
        manifest_items.append('<item id="css" href="style.css" media-type="text/css"/>')
        
        # 4. Handle cover image if exists
        if cover_image_path:
            cover_ext = os.path.splitext(cover_image_path)[1].lower()
            cover_mime = "image/png" if cover_ext == ".png" else "image/jpeg"
            cover_in_epub = f"cover{cover_ext}"
            
            # Write image to zip
            with open(cover_image_path, 'rb') as img_f:
                epub.writestr(f'OEBPS/{cover_in_epub}', img_f.read())
                
            manifest_items.append(f'<item id="cover-image" href="{cover_in_epub}" media-type="{cover_mime}"/>')
            
            # Create cover page
            cover_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Cover</title>
  <link rel="stylesheet" href="style.css" type="text/css"/>
</head>
<body>
  <div class="cover-container">
    <img src="{cover_in_epub}" alt="Cover Image" class="cover-img"/>
  </div>
</body>
</html>
"""
            epub.writestr('OEBPS/cover.xhtml', cover_html)
            manifest_items.append('<item id="cover-page" href="cover.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="cover-page"/>')
            
            # HTML preview cover
            html_chapters_body.append(f'<div style="text-align: center; margin-bottom: 3em;"><img src="../{os.path.basename(cover_image_path)}" style="max-width: 400px; height: auto;" /></div>')

        # Read book Title from book_id
        display_title = book_id.replace('_', ' ').title()
        
        # 5. Compile Chapters
        toc_entries = []
        
        # Compile Introduction if it exists
        has_intro = os.path.exists(intro_file)
        if has_intro:
            intro_paras = parse_paragraphs(intro_file)
            intro_title = "Introduction"
            if intro_paras and not intro_paras[0].upper().startswith("CHAPTER") and len(intro_paras[0]) < 100:
                intro_title = intro_paras[0]
                intro_paras.pop(0)
                
            intro_html_content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{clean_xml_text(intro_title)}</title>
  <link rel="stylesheet" href="style.css" type="text/css"/>
</head>
<body>
  <h1>{clean_xml_text(intro_title)}</h1>
"""
            for p in intro_paras:
                p_clean = clean_xml_text(p)
                intro_html_content += f'  <p>{p_clean}</p>\n'
                
            intro_html_content += "</body>\n</html>"
            epub.writestr("OEBPS/introduction.xhtml", intro_html_content)
            manifest_items.append('<item id="introduction" href="introduction.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="introduction"/>')
            toc_entries.append(("introduction", "introduction.xhtml", intro_title))
            
            # Write to HTML preview
            html_chapters_body.append(f'<h1>{clean_xml_text(intro_title)}</h1>')
            for p in intro_paras:
                p_clean = clean_xml_text(p)
                html_chapters_body.append(f'<p style="margin-bottom: 1.2em; text-indent: 1.5em; font-size: 1.05em; line-height: 1.7;">{p_clean}</p>')
            html_chapters_body.append('<hr />')
        
        is_two_cities = (book_id == "two_cities")
        added_images = set()
        
        for idx, en_file_path in enumerate(en_files):
            chapter_num = idx + 1
            
            en_paras = parse_paragraphs(en_file_path)
            
            book_header = None
            chapter_header = None
            chapter_title = ""
            
            if is_two_cities:
                idx_para = 0
                if idx_para < len(en_paras) and "book the" in en_paras[idx_para].lower():
                    book_header = en_paras[idx_para]
                    idx_para += 1
                if idx_para < len(en_paras) and en_paras[idx_para].upper().startswith("CHAPTER"):
                    chapter_header = en_paras[idx_para]
                    idx_para += 1
                    
                    # Split combined chapter header and title (e.g. "CHAPTER I. Five Years Later")
                    match = re.match(r"^(CHAPTER\s+[IVXLCDM]+)\.?(?:\s+(.+))?$", chapter_header, re.IGNORECASE)
                    if match:
                        ch_num_part = match.group(1)
                        title_part = match.group(2)
                        if title_part:
                            chapter_header = ch_num_part
                            chapter_title = title_part.strip()
                            
                if not chapter_title and idx_para < len(en_paras) and len(en_paras[idx_para]) < 100:
                    chapter_title = en_paras[idx_para]
                    idx_para += 1
                
                for _ in range(idx_para):
                    en_paras.pop(0)
                    
                if chapter_header and chapter_title:
                    clean_ch_head = chapter_header.strip().rstrip('.')
                    display_ch_title = f"{clean_ch_head}: {chapter_title}"
                elif chapter_header:
                    display_ch_title = chapter_header.strip().rstrip('.')
                elif chapter_title:
                    display_ch_title = chapter_title
                else:
                    display_ch_title = f"Chapter {chapter_num}"
            else:
                chapter_title_en = f"Chapter {chapter_num}"
                if en_paras and en_paras[0].upper().startswith("CHAPTER"):
                    chapter_title_en = en_paras[0]
                    en_paras.pop(0)
                display_ch_title = chapter_title_en
                
            print(f"  Formatting {display_ch_title}...")
            
            # Create XHTML content
            ch_html_content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{clean_xml_text(display_ch_title)}</title>
  <link rel="stylesheet" href="style.css" type="text/css"/>
</head>
<body>
"""
            if is_two_cities and book_header:
                clean_book = book_header.replace("--", ": ")
                ch_html_content += f'  <h2 style="text-align: center; color: #7f8c8d; font-size: 1.3em; text-transform: uppercase; margin-top: 1.5em; margin-bottom: 0.5em;">{clean_xml_text(clean_book)}</h2>\n'
                html_chapters_body.append(f'<h2 style="text-align: center; color: #7f8c8d; font-size: 1.3em; text-transform: uppercase; margin-top: 2em; margin-bottom: 0.5em;">{clean_xml_text(clean_book)}</h2>')
            
            ch_html_content += f'  <h1>{clean_xml_text(display_ch_title)}</h1>\n'
            html_chapters_body.append(f'<h1>{clean_xml_text(display_ch_title)}</h1>')

            # Render paragraphs
            for p in en_paras:
                img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', p.strip())
                if img_match:
                    alt_text = img_match.group(1)
                    img_path_rel = img_match.group(2)
                    img_filename = os.path.basename(img_path_rel)
                    
                    if img_filename not in added_images:
                        added_images.add(img_filename)
                        full_img_path = os.path.join(book_path, img_path_rel)
                        if os.path.exists(full_img_path):
                            ext = os.path.splitext(img_filename)[1].lower()
                            mime = "image/png" if ext == ".png" else "image/jpeg"
                            with open(full_img_path, 'rb') as f_img:
                                epub.writestr(f'OEBPS/{img_filename}', f_img.read())
                            manifest_items.append(f'<item id="img_{img_filename.replace(".","_")}" href="{img_filename}" media-type="{mime}"/>')
                        else:
                            print(f"Warning: Image {full_img_path} not found.")
                            
                    img_html = f'<div style="text-align: center; margin-top: 1.5em; margin-bottom: 1.5em;"><img src="{img_filename}" alt="{clean_xml_text(alt_text)}" style="max-width: 100%; height: auto;" /></div>'
                    ch_html_content += f'  {img_html}\n'
                    html_chapters_body.append(f'<div style="text-align: center; margin-top: 1.5em; margin-bottom: 1.5em;"><img src="../{img_path_rel}" alt="{clean_xml_text(alt_text)}" style="max-width: 100%; height: auto;" /></div>')
                else:
                    en_p = clean_xml_text(p)
                    ch_html_content += f'  <p>{en_p}</p>\n'
                    html_chapters_body.append(f'<p style="margin-bottom: 1.2em; text-indent: 1.5em; font-size: 1.05em; line-height: 1.7;">{en_p}</p>')

            ch_html_content += "</body>\n</html>"
            
            # Write chapter to zip
            ch_filename = f"ch_{chapter_num:02d}.xhtml"
            epub.writestr(f"OEBPS/{ch_filename}", ch_html_content)
            
            manifest_items.append(f'<item id="ch_{chapter_num:02d}" href="{ch_filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="ch_{chapter_num:02d}"/>')
            toc_entries.append((f"ch_{chapter_num:02d}", ch_filename, display_ch_title))
            
        # Compile Copyright/Feedback if it exists
        has_copyright = os.path.exists(copyright_file)
        if has_copyright:
            copy_paras = parse_paragraphs(copyright_file)
            copy_title = "Copyright and Feedback"
            if copy_paras and not copy_paras[0].upper().startswith("CHAPTER") and len(copy_paras[0]) < 100:
                copy_title = copy_paras[0]
                copy_paras.pop(0)
                
            copy_html_content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>{clean_xml_text(copy_title)}</title>
  <link rel="stylesheet" href="style.css" type="text/css"/>
</head>
<body>
  <h1>{clean_xml_text(copy_title)}</h1>
"""
            for p in copy_paras:
                p_clean = clean_xml_text(p)
                copy_html_content += f'  <p>{p_clean}</p>\n'
                
            copy_html_content += "</body>\n</html>"
            epub.writestr("OEBPS/copyright.xhtml", copy_html_content)
            manifest_items.append('<item id="copyright" href="copyright.xhtml" media-type="application/xhtml+xml"/>')
            spine_items.append('<itemref idref="copyright"/>')
            toc_entries.append(("copyright", "copyright.xhtml", copy_title))
            
            # Write to HTML preview
            html_chapters_body.append('<hr />')
            html_chapters_body.append(f'<h1>{clean_xml_text(copy_title)}</h1>')
            for p in copy_paras:
                p_clean = clean_xml_text(p)
                html_chapters_body.append(f'<p style="margin-bottom: 1.2em; text-indent: 1.5em; font-size: 1.05em; line-height: 1.7;">{p_clean}</p>')
            
        # 6. Generate toc.ncx
        ncx_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:{book_id}-epub"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>{clean_xml_text(display_title)}</text>
  </docTitle>
  <navMap>
"""
        for i, entry in enumerate(toc_entries):
            id_ref, filename, title = entry
            ncx_content += f"""    <navPoint id="navPoint-{i+1}" playOrder="{i+1}">
      <navLabel>
        <text>{clean_xml_text(title)}</text>
      </navLabel>
      <content src="{filename}"/>
    </navPoint>
"""
        ncx_content += "  </navMap>\n</ncx>"
        epub.writestr('OEBPS/toc.ncx', ncx_content)
        manifest_items.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')
        
        # 7. Generate content.opf
        opf_content = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title>{clean_xml_text(display_title)}</dc:title>
    <dc:language>en</dc:language>
    <dc:identifier id="bookid">urn:uuid:{book_id}-epub</dc:identifier>
    <dc:publisher>TKPROF LLC</dc:publisher>
  </metadata>
  <manifest>
    {"    ".join(manifest_items)}
  </manifest>
  <spine toc="ncx">
    {"    ".join(spine_items)}
  </spine>
</package>
"""
        epub.writestr('OEBPS/content.opf', opf_content)
        
    # Write standalone HTML file
    standalone_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{clean_xml_text(display_title)}</title>
  <style>
    body {{
        max-width: 800px;
        margin: 40px auto;
        padding: 0 20px;
        font-family: "Georgia", serif;
        line-height: 1.7;
        color: #111;
        background-color: #fafafa;
    }}
    .book-container {{
        background: white;
        padding: 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-radius: 8px;
    }}
    h1 {{ text-align: center; color: #2c3e50; font-size: 2em; margin-top: 1.5em; }}
    h2 {{ text-align: center; color: #7f8c8d; font-size: 1.3em; margin-bottom: 2em; }}
    p {{
        margin-bottom: 1.2em;
        text-indent: 1.5em;
    }}
    hr {{ border: 0; border-top: 1px solid #eee; margin: 3em 0; }}
  </style>
</head>
<body>
  <div class="book-container">
    <h1 style="font-size: 2.5em; margin-bottom: 0.2em;">{clean_xml_text(display_title)}</h1>
    <h2 style="font-weight: normal; margin-bottom: 3em;">Modern English Edition</h2>
    {"".join(html_chapters_body)}
  </div>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as html_f:
        html_f.write(standalone_html)
        
    print(f"Successfully compiled eBook versions:")
    print(f"  - EPUB: {epub_path}")
    print(f"  - HTML: {html_path}")
    return True

def glob_files(directory, pattern):
    """Helper to find files matching a wildcard pattern in a directory."""
    import glob
    return glob.glob(os.path.join(directory, pattern))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile modernized eBooks into EPUB and HTML formats.")
    parser.add_argument("--book", required=True, help="Directory name of the target book (e.g. christmas_carol)")
    
    args = parser.parse_args()
    
    success = compile_book(args.book)
    sys.exit(0 if success else 1)
