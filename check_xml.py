import zipfile
import xml.etree.ElementTree as ET

epub_path = r'D:\git_repo\TKprof_book\books\The_Muqaddimah\The_Muqaddimah_Retold1.epub'

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
        
        for item in manifest.findall('item'):
            href = item.attrib.get('href')
            media = item.attrib.get('media-type')
            
            if media in ['application/xhtml+xml', 'application/x-dtbncx+xml', 'text/xml']:
                full_href = opf_dir + href
                try:
                    content = z.read(full_href)
                    ET.fromstring(content)
                except ET.ParseError as e:
                    print(f"XML Parse Error in {full_href}: {e}")
                except KeyError:
                    print(f"File missing from zip: {full_href}")

        print("Finished XML validation.")
                
except Exception as e:
    print(f'Error: {e}')
