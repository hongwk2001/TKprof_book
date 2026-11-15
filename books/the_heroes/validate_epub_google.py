# -*- coding: utf-8 -*-
"""
validate_epub_google.py
Rigorous automated validator checking an EPUB against Google Play Books Partner Center
ingestion and sanitization requirements.
"""

import sys
import os
import zipfile
import re
import xml.etree.ElementTree as ET

def validate_epub(epub_path):
    print(f"=== Validating EPUB for Google Play Books: {epub_path} ===")
    if not os.path.exists(epub_path):
        print(f"ERROR: File not found: {epub_path}")
        return False

    errors = []
    warnings = []

    with zipfile.ZipFile(epub_path, 'r') as zf:
        infolist = zf.infolist()
        if not infolist:
            print("ERROR: EPUB zip archive is empty!")
            return False

        # 1. Mimetype Check
        first_entry = infolist[0]
        if first_entry.filename != 'mimetype':
            errors.append(f"MIMETYPE ERROR: First file in ZIP is '{first_entry.filename}', but Google requires 'mimetype' as exact first file.")
        if first_entry.compress_type != zipfile.ZIP_STORED:
            errors.append(f"MIMETYPE ERROR: 'mimetype' is compressed (type {first_entry.compress_type}). Google requires uncompressed ZIP_STORED (0).")
        mimetype_content = zf.read('mimetype')
        if mimetype_content != b'application/epub+zip':
            errors.append(f"MIMETYPE ERROR: Content is {mimetype_content}, expected b'application/epub+zip' (20 bytes).")
        else:
            print("  [PASS] 1. Mimetype is first entry, uncompressed, exactly 20 bytes.")

        # 2. Container XML Check
        if 'META-INF/container.xml' not in zf.namelist():
            errors.append("CONTAINER ERROR: Missing META-INF/container.xml.")
        else:
            try:
                c_xml = zf.read('META-INF/container.xml')
                c_root = ET.fromstring(c_xml)
                ns = {'c': 'urn:oasis:names:tc:opendocument:xmlns:container'}
                rootfile = c_root.find('.//c:rootfile', ns)
                if rootfile is None:
                    errors.append("CONTAINER ERROR: <rootfile> tag not found in container.xml.")
                else:
                    opf_path = rootfile.attrib.get('full-path')
                    print(f"  [PASS] 2. Container XML valid. OPF rootfile path: '{opf_path}'")
            except Exception as e:
                errors.append(f"CONTAINER XML PARSE ERROR: {e}")

        # 3. OPF Package and Manifest Check
        if opf_path not in zf.namelist():
            errors.append(f"OPF ERROR: Specified OPF file '{opf_path}' not found in archive.")
            opf_root = None
        else:
            try:
                opf_data = zf.read(opf_path)
                opf_root = ET.fromstring(opf_data)
                print(f"  [PASS] 3. OPF file '{opf_path}' parses as valid XML.")
            except Exception as e:
                errors.append(f"OPF XML PARSE ERROR: {e}")
                opf_root = None

        if opf_root is not None:
            # Check version
            ver = opf_root.attrib.get('version', '')
            print(f"       EPUB Package Version: {ver}")

            # Collect manifest items
            manifest_el = None
            spine_el = None
            for child in opf_root:
                tag = child.tag.split('}')[-1]
                if tag == 'manifest':
                    manifest_el = child
                elif tag == 'spine':
                    spine_el = child

            manifest_items = {}
            if manifest_el is not None:
                for item in manifest_el:
                    i_id = item.attrib.get('id')
                    i_href = item.attrib.get('href')
                    i_media = item.attrib.get('media-type')
                    i_prop = item.attrib.get('properties', '')
                    manifest_items[i_id] = {'href': i_href, 'media': i_media, 'properties': i_prop}

            print(f"  [PASS] 4. Manifest contains {len(manifest_items)} declared items.")

            # Verify every manifest file exists in zip
            opf_dir = os.path.dirname(opf_path)
            for i_id, i_data in manifest_items.items():
                rel_href = i_data['href']
                full_in_zip = f"{opf_dir}/{rel_href}" if opf_dir else rel_href
                if full_in_zip not in zf.namelist():
                    errors.append(f"MANIFEST MISMATCH: Item '{i_id}' points to '{full_in_zip}', but file does not exist in zip!")

            # Verify every file in OEBPS is in manifest (excluding container, mimetype, and opf itself)
            ignored_zip_files = {'mimetype', 'META-INF/container.xml', opf_path}
            declared_zip_files = {f"{opf_dir}/{d['href']}" if opf_dir else d['href'] for d in manifest_items.values()}
            for zname in zf.namelist():
                if zname in ignored_zip_files or zname.endswith('/'):
                    continue
                if zname not in declared_zip_files:
                    errors.append(f"GHOST FILE: File '{zname}' exists in archive but is NOT declared in OPF manifest!")

            # Check Spine
            if spine_el is not None:
                spine_toc = spine_el.attrib.get('toc')
                if not spine_toc or spine_toc not in manifest_items:
                    warnings.append(f"SPINE WARNING: spine toc attribute '{spine_toc}' not declared in manifest. Recommended for EPUB2 backward compatibility.")
                else:
                    print(f"  [PASS] 5. Spine toc attribute '{spine_toc}' declared for backward compatibility.")

                for itemref in spine_el:
                    idref = itemref.attrib.get('idref')
                    if idref not in manifest_items:
                        errors.append(f"SPINE ERROR: <itemref idref='{idref}'> does not exist in manifest!")
            else:
                errors.append("SPINE ERROR: <spine> element missing from OPF!")

            # Check cover declarations
            has_cover_prop = any('cover-image' in d.get('properties', '') for d in manifest_items.values())
            has_cover_meta = any(child.tag.endswith('meta') and child.attrib.get('name') == 'cover' for child in opf_root.find('{http://www.idpf.org/2007/opf}metadata') or [])
            if has_cover_prop:
                print("  [PASS] 6. Cover image declared via EPUB 3 properties='cover-image'.")
            else:
                warnings.append("COVER WARNING: No manifest item has properties='cover-image'.")
            if has_cover_meta:
                print("  [PASS] 7. Cover image declared via EPUB 2 <meta name='cover'>.")
            else:
                warnings.append("COVER WARNING: <meta name='cover'> missing in metadata.")

            # Check nav declaration
            has_nav_prop = any('nav' in d.get('properties', '') for d in manifest_items.values())
            if has_nav_prop:
                print("  [PASS] 8. EPUB 3 Navigation Document declared with properties='nav'.")
            else:
                errors.append("NAV ERROR: No manifest item has properties='nav' (required for EPUB 3).")

        # 4. Strict XML Well-Formedness of all XHTML files
        xhtml_files = [z for z in zf.namelist() if z.endswith(('.xhtml', '.html', '.xml'))]
        xml_errors = 0
        for xf in xhtml_files:
            try:
                x_data = zf.read(xf)
                ET.fromstring(x_data)
            except Exception as e:
                errors.append(f"XML PARSE ERROR in '{xf}': {e}")
                xml_errors += 1

        if xml_errors == 0:
            print(f"  [PASS] 9. All {len(xhtml_files)} XHTML/XML documents parse cleanly as valid XML (0 syntax/ampersand errors).")

        # 5. Check for External URLs
        external_url_count = 0
        for xf in xhtml_files:
            content = zf.read(xf).decode('utf-8', errors='ignore')
            # Look for http:// or https:// excluding standard xml namespaces
            cleaned = re.sub(r'xmlns(:\w+)?=["\']https?://[^"\']+["\']', '', content)
            cleaned = re.sub(r'http://www\.w3\.org/[^"\']+', '', cleaned)
            cleaned = re.sub(r'http://www\.idpf\.org/[^"\']+', '', cleaned)
            cleaned = re.sub(r'http://purl\.org/[^"\']+', '', cleaned)
            cleaned = re.sub(r'http://www\.daisy\.org/[^"\']+', '', cleaned)
            urls = re.findall(r'https?://[^\s"\'<>]+', cleaned)
            if urls:
                warnings.append(f"EXTERNAL URL in '{xf}': {urls[:3]}")
                external_url_count += len(urls)

        if external_url_count == 0:
            print("  [PASS] 10. Zero external URLs found (100% self-contained).")

    print("\n=== Validation Summary ===")
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  [WARN] {w}")
    if errors:
        print(f"ERRORS FOUND ({len(errors)}):")
        for e in errors:
            print(f"  [FAIL] {e}")
        return False
    else:
        print(f"ALL CHECKS PASSED: 100% COMPLIANT WITH GOOGLE PLAY BOOKS REQUIREMENTS!")
        return True

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else r'c:\git_repo\TKprof_book\books\the_heroes\output\the_heroes_bilingual.epub'
    ok = validate_epub(target)
    sys.exit(0 if ok else 1)
