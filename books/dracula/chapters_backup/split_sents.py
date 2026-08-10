import re

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_27.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paras = text.split('\n\n')
all_sents = []
for p in paras:
    p = p.strip()
    if not p: continue
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z“_])', p.replace('\n', ' '))
    all_sents.append(sents)

with open('en_sents.txt', 'w', encoding='utf-8') as f:
    for i, p_sents in enumerate(all_sents):
        f.write(f'--- PARA {i} ---\n')
        for j, s in enumerate(p_sents):
            f.write(f'{j}: {s}\n')
