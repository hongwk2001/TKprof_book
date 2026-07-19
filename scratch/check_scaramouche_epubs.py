import zipfile
import os
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPUB_EN = os.path.join(BASE_DIR, "books", "scaramouche", "scaramouche_en.epub")
EPUB_KO = os.path.join(BASE_DIR, "books", "scaramouche", "scaramouche_ko.epub")

def check_epub(epub_path):
    print(f"\nVerifying EPUB: {os.path.basename(epub_path)}...")
    if not os.path.exists(epub_path):
        print(f"Error: file does not exist!")
        return False
        
    try:
        with zipfile.ZipFile(epub_path, 'r') as z:
            # 1. Check mimetype
            mimetype = z.read('mimetype').decode('utf-8').strip()
            if mimetype != "application/epub+zip":
                print("  [FAIL] mimetype is incorrect!")
                return False
            print("  [PASS] mimetype verified.")
            
            # 2. Check container
            container = z.read('META-INF/container.xml')
            root = ET.fromstring(container)
            ns = {'n': 'urn:oasis:names:tc:opendocument:xmlns:container'}
            opf_path = root.find('.//n:rootfile', ns).attrib.get('full-path')
            print(f"  [PASS] container.xml matches OPF path: {opf_path}")
            
            # 3. Read OPF
            opf_data = z.read(opf_path)
            opf_root = ET.fromstring(opf_data)
            # Simple tag cleanup
            for el in opf_root.iter():
                if '}' in el.tag:
                    el.tag = el.tag.split('}', 1)[1]
            
            version = opf_root.attrib.get('version', 'unknown')
            print(f"  [PASS] EPUB version: {version}")
            
            manifest = opf_root.find('manifest')
            spine = opf_root.find('spine')
            
            manifest_items = manifest.findall('item') if manifest is not None else []
            spine_items = spine.findall('itemref') if spine is not None else []
            
            print(f"  [PASS] Manifest has {len(manifest_items)} items.")
            print(f"  [PASS] Spine has {len(spine_items)} items.")
            
            # Confirm files in manifest exist in zip
            missing = 0
            opf_dir = os.path.dirname(opf_path)
            for item in manifest_items:
                href = item.attrib.get('href')
                full_href = os.path.join(opf_dir, href).replace('\\', '/') if opf_dir else href
                try:
                    z.getinfo(full_href)
                except KeyError:
                    print(f"  [FAIL] Missing manifest file in zip: {full_href}")
                    missing += 1
                    
            if missing == 0:
                print("  [PASS] All manifest files exist in zip package.")
                return True
            else:
                return False
                
    except Exception as e:
        print(f"  [ERROR] Failed to parse EPUB: {e}")
        return False

def main():
    ok_en = check_epub(EPUB_EN)
    ok_ko = check_epub(EPUB_KO)
    print("\n" + "="*60)
    if ok_en and ok_ko:
        print("SUCCESS: Both EPUBs are verified as spec-compliant and correct!")
    else:
        print("FAIL: One or both EPUBs failed validation check.")
    print("="*60)

if __name__ == "__main__":
    main()
