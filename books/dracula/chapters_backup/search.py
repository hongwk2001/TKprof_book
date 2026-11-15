with open('sentences.txt', 'r', encoding='utf-8') as f:
    out = []
    for line in f:
        if any(w in line for w in ['종이', '인쇄', '심판']):
            out.append(line.strip())

with open('search_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
