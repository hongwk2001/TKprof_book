import sys
import re

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_12.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

paras = []
current_para = []

for line in lines:
    line = line.strip()
    if not line:
        if current_para:
            paras.append(' '.join(current_para))
            current_para = []
    else:
        current_para.append(line)
if current_para:
    paras.append(' '.join(current_para))

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch12_en.txt', 'w', encoding='utf-8') as f:
    for p in paras:
        p = p.replace('_', '')
        p = p.replace('“', '"').replace('”', '"').replace('’', "'")
        f.write(p + '\n\n')

print(f"Total paras: {len(paras)}")
