import zipfile
import os
import shutil

epub_path = r'D:\git_repo\TKprof_book\books\The_Muqaddimah\The_Muqaddimah_Retold1.epub'
temp_epub = epub_path + '.temp'

try:
    with zipfile.ZipFile(epub_path, 'r') as zin, zipfile.ZipFile(temp_epub, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)
            
            if item.filename == 'OEBPS/Text/cover.xhtml':
                # Replace &mdash; with the numeric entity &#8212;
                content_str = content.decode('utf-8')
                content_str = content_str.replace('&mdash;', '&#8212;')
                content = content_str.encode('utf-8')
            
            # mimetype must be stored uncompressed (ZIP_STORED) and as the first file in EPUB
            if item.filename == 'mimetype':
                zout.writestr(item, content, compress_type=zipfile.ZIP_STORED)
            else:
                zout.writestr(item, content)

    # Replace the original file with the fixed one
    os.remove(epub_path)
    os.rename(temp_epub, epub_path)
    print("EPUB fixed successfully.")
    
except Exception as e:
    print(f'Error fixing EPUB: {e}')
