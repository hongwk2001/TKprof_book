import re
import json

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_27.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paras = text.split('\n\n')
en_sents = []
for i, p in enumerate(paras):
    p = p.strip()
    if not p: continue
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z“_])', p.replace('\n', ' '))
    for j, s in enumerate(sents):
        en_sents.append({'p': i, 's': j, 'text': s})

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch27_ko.txt', 'r', encoding='utf-8') as f:
    ko_paras = [p.strip() for p in f.read().split('\n') if p.strip()]

def get_entities(text):
    ents = set()
    if re.search(r'Mina|미나', text, re.I): ents.add('Mina')
    if re.search(r'Helsing|헬싱', text, re.I): ents.add('Helsing')
    if re.search(r'Jonathan|조나단', text, re.I): ents.add('Jonathan')
    if re.search(r'Morris|모리스', text, re.I): ents.add('Morris')
    if re.search(r'Seward|수어드', text, re.I): ents.add('Seward')
    if re.search(r'Godalming|고달밍', text, re.I): ents.add('Godalming')
    if re.search(r'Quincey|퀸시', text, re.I): ents.add('Quincey')
    if re.search(r'Dracula|드라큘라', text, re.I): ents.add('Dracula')
    return ents

splits = []
for kp in ko_paras:
    k_ents = get_entities(kp)
    best_match = None
    best_score = -1
    for es in en_sents:
        if es['s'] == 0: continue # Already a paragraph start
        e_ents = get_entities(es['text'])
        score = len(k_ents.intersection(e_ents))
        if score > best_score and score > 0:
            best_score = score
            best_match = es
    if best_match and best_match not in splits:
        splits.append(best_match)

print(f'Found {len(splits)} splits using entities.')
