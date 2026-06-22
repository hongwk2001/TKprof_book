import zipfile, re

with zipfile.ZipFile('scarlet_letter.epub', 'r') as z:
    print('--- Files in EPUB ---')
    for f in z.namelist():
        print(f)

    print()
    print('--- Nav href links ---')
    nav_files = [f for f in z.namelist() if 'nav' in f.lower() and f.endswith('.xhtml')]
    for n in nav_files:
        content = z.read(n).decode('utf-8')
        links = re.findall(r'href="([^"]+)"', content)
        for l in links[:15]:
            print(l)
