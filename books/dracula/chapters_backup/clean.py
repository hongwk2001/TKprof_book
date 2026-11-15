import re
import sys

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_02.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paras = re.split(r'\n\s*\n', text.strip())

cleaned_paras = []
for p in paras:
    p = p.strip()
    if not p: continue
    if re.match(r'^[\*\s]+$', p):
        continue
    p = re.sub(r'\n', ' ', p)
    p = re.sub(r'\s+', ' ', p)
    p = p.replace('“', '"').replace('”', '"')
    p = p.replace('_', '')
    cleaned_paras.append(p)

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch02_en.txt', 'w', encoding='utf-8') as f:
    for p in cleaned_paras:
        f.write(p + '\n')
