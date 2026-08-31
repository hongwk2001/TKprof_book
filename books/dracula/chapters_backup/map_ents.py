import re

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_27.txt', 'r', encoding='utf-8') as f:
    en_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch27_ko.txt', 'r', encoding='utf-8') as f:
    ko_paras = [p.strip() for p in f.read().split('\n') if p.strip()]

def get_entities(text):
    ents = []
    if re.search(r'Mina|미나', text, re.I): ents.append('Mina')
    if re.search(r'Helsing|헬싱', text, re.I): ents.append('Helsing')
    if re.search(r'Jonathan|조나단', text, re.I): ents.append('Jonathan')
    if re.search(r'Morris|모리스', text, re.I): ents.append('Morris')
    if re.search(r'Seward|수어드', text, re.I): ents.append('Seward')
    if re.search(r'Godalming|고달밍', text, re.I): ents.append('Godalming')
    if re.search(r'Quincey|퀸시', text, re.I): ents.append('Quincey')
    if re.search(r'Dracula|드라큘라', text, re.I): ents.append('Dracula')
    return ents

with open('align_ents.txt', 'w', encoding='utf-8') as f:
    for i, p in enumerate(en_paras):
        f.write(f'EN {i}: {get_entities(p)} | {p[:50]}...\n')
    f.write('='*50 + '\n')
    for i, p in enumerate(ko_paras):
        f.write(f'KO {i}: {get_entities(p)} | {p[:50]}...\n')
