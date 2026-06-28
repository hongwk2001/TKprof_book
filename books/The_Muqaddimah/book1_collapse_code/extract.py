import zipfile
import xml.etree.ElementTree as ET
import os
import re

epub_path = r'D:\git_repo\TKprof_book\books\The_Muqaddimah\_archive\collapse_code\The_Muqaddimah_Retold.epub'
out_path = r'D:\git_repo\TKprof_book\books\The_Muqaddimah\_archive\collapse_code\extracted_text.txt'

try:
    with zipfile.ZipFile(epub_path, 'r') as z:
        container = z.read('META-INF/container.xml')
        root = ET.fromstring(container)
        ns = {'n': 'urn:oasis:names:tc:opendocument:xmlns:container'}
        opf_path = root.find('.//n:rootfile', ns).attrib.get('full-path')
        
        opf_dir = ''
        if '/' in opf_path:
            opf_dir = opf_path.rsplit('/', 1)[0] + '/'
            
        it = ET.iterparse(z.open(opf_path))
        for _, el in it:
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]
        opf_root = it.root
        
        manifest = opf_root.find('manifest')
        spine = opf_root.find('spine')
        
        items = {}
        for item in manifest.findall('item'):
            items[item.attrib.get('id')] = item.attrib.get('href')
            
        full_text = []
        for itemref in spine.findall('itemref'):
            idref = itemref.attrib.get('idref')
            if idref in items:
                href = items[idref]
                full_href = opf_dir + href
                if full_href in z.namelist():
                    content = z.read(full_href).decode('utf-8', errors='ignore')
                    full_text.append(f'--- Chapter: {href} ---')
                    # Strip html tags roughly
                    text = re.sub('<[^<]+>', '', content)
                    # Unescape basic entities
                    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'").replace('&#8212;', '-')
                    # condense whitespace
                    text = re.sub('\s+', ' ', text).strip()
                    full_text.append(text)
                    full_text.append('\n')
                    
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(full_text))
        print(f'Successfully extracted text to {out_path}')
except FileNotFoundError:
    print('EPUB file not found!')
except Exception as e:
    print(f'Error: {e}')
