import zipfile
import xml.etree.ElementTree as ET

epub_path = r'D:\git_repo\TKprof_book\books\The_Muqaddimah\The_Muqaddimah_Retold1.epub'

try:
    with zipfile.ZipFile(epub_path, 'r') as z:
        container = z.read('META-INF/container.xml')
        root = ET.fromstring(container)
        ns = {'n': 'urn:oasis:names:tc:opendocument:xmlns:container'}
        opf_path = root.find('.//n:rootfile', ns).attrib.get('full-path')
        
        it = ET.iterparse(z.open(opf_path))
        for _, el in it:
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]
        opf_root = it.root
        
        print('EPUB version:', opf_root.attrib.get('version', 'unknown'))
        
        manifest = opf_root.find('manifest')
        print('\n--- Manifest Items ---')
        if manifest is not None:
            for item in manifest.findall('item'):
                print(f"ID: {item.attrib.get('id')}, Href: {item.attrib.get('href')}, Media: {item.attrib.get('media-type')}, Properties: {item.attrib.get('properties', '')}")
        
        spine = opf_root.find('spine')
        print('\n--- Spine ---')
        if spine is not None:
            print('TOC id:', spine.attrib.get('toc', 'none'))
            for itemref in spine.findall('itemref'):
                print(f"IDref: {itemref.attrib.get('idref')}")
                
except Exception as e:
    print(f'Error: {e}')
