import re

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_18.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paragraphs = re.split(r'\n\s*\n', text)
cleaned_paragraphs = []
for p in paragraphs:
    p = p.strip()
    if p:
        # replace single newlines with space
        p = re.sub(r'(?<!\n)\n(?!\n)', ' ', p)
        # standardizing quotes
        p = p.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        # replace multiple spaces with single space
        p = re.sub(r' +', ' ', p)
        cleaned_paragraphs.append(p)

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch18_en.txt', 'w', encoding='utf-8') as f:
    for i, p in enumerate(cleaned_paragraphs):
        f.write(p)
        if i < len(cleaned_paragraphs) - 1:
            f.write('\n\n')
