import re

with open('c:/git_repo/TKprof_book/books/dracula/chapters/raw_ch_06.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paragraphs = text.split('\n\n')
cleaned = []
for p in paragraphs:
    if p.strip():
        # replace newlines with space, multiple spaces with single space
        p = p.replace('\n', ' ')
        p = re.sub(' +', ' ', p)
        # replace smart quotes with straight ones
        p = p.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        cleaned.append(p.strip())

with open('c:/git_repo/TKprof_book/books/dracula/chapters/ch06_en.txt', 'w', encoding='utf-8') as f:
    for p in cleaned:
        f.write(p + '\n')
