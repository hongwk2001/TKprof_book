import zipfile
import xml.etree.ElementTree as ET

epub_path = r'books/dracula/dracula_bilingual.epub'
with zipfile.ZipFile(epub_path, 'r') as z:
    for name in z.namelist():
        if name.endswith(('.xhtml', '.xml', '.opf', '.ncx')):
            content = z.read(name)
            try:
                ET.fromstring(content)
            except ET.ParseError as e:
                print(f"Error in {name}: {e}")
