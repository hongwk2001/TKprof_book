import re

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_27.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paras = text.split('\n\n')
new_paras = []

splits = {
    2: [1, 2, 11, 21],
    4: [1, 2, 3],
    6: [2, 4, 6, 8, 10, 12, 14],
    8: [2, 4, 9, 11],
    10: [1, 2, 3],
    15: [3, 6, 8, 9, 10],
    16: [6]
}

split_count = 0

for i, p in enumerate(paras):
    p = p.strip()
    if not p:
        new_paras.append('')
        continue
    
    if i in splits:
        sents = re.split(r'(?<=[.!?])\s+(?=[A-Z“_])', p.replace('\n', ' '))
        current_para = []
        for j, s in enumerate(sents):
            if j in splits[i]:
                new_paras.append(' '.join(current_para))
                current_para = [s]
                split_count += 1
            else:
                current_para.append(s)
        if current_para:
            new_paras.append(' '.join(current_para))
    else:
        new_paras.append(p)

# Filter out empty paras if any, but wait, the prompt says "only insert paragraph breaks".
# This means we shouldn't replace '\n' with ' ' inside paragraphs if we can avoid it.
# Wait, replacing \n with ' ' changes words (replaces newline with space).
# The prompt says: "Do NOT change or add any English words — only insert paragraph breaks (\n\n) into the English text."
