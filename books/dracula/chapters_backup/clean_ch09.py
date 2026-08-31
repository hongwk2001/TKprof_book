import re

with open('c:/git_repo/TKprof_book/books/dracula/chapters/raw_ch_09.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
paragraphs = text.split('\n\n')

cleaned_paragraphs = []
for p in paragraphs:
    p = p.strip()
    if not p:
        continue
    if re.match(r'^(\s*\*\s*)+$', p):
        p = '***'
    else:
        p = re.sub(r'\s+', ' ', p)
    cleaned_paragraphs.append(p)

with open('c:/git_repo/TKprof_book/books/dracula/chapters/ch09_en.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(cleaned_paragraphs))
