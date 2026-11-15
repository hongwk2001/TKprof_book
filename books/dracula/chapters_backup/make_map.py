import re

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_27.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paras = text.split('\n\n')
all_sents = []
for i, p in enumerate(paras):
    p = p.strip()
    if not p: continue
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z“_])', p.replace('\n', ' '))
    all_sents.append(sents)

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch27_ko.txt', 'r', encoding='utf-8') as f:
    ko_paras = [p.strip() for p in f.read().split('\n') if p.strip()]

with open('map_manual.txt', 'w', encoding='utf-8') as f:
    f.write('--- KOREAN PARAGRAPHS ---\n')
    for i, p in enumerate(ko_paras):
        f.write(f'KO {i}: {p[:40]}...\n')
    f.write('\n--- ENGLISH SPLITTABLE ---\n')
    for i, sents in enumerate(all_sents):
        if len(sents) > 1:
            f.write(f'\nPARA {i}\n')
            for j, s in enumerate(sents):
                if j > 0:
                    f.write(f'  [{i},{j}] {s[:40]}...\n')
