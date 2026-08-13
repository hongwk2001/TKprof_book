import re

def fix_ch22_p051():
    ko_path = 'chapters/ch22_ko.txt'
    with open(ko_path, 'r', encoding='utf-8') as f:
        text = f.read()

    paras = [p.strip() for p in text.split('\n\n') if p.strip()]

    new_paras = []
    i = 0
    while i < len(paras):
        p = paras[i]
        if '우리는 아무런 문제 없이 카팍스에 들어갔고' in p:
            p1 = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p)
            i += 1
            if i < len(paras) and '반 헬싱 박사는 상자들 앞에 선 우리에게' in paras[i]:
                p2 = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', paras[i])
                i += 1
                new_paras.append(f"[P051a] {p1} {p2}")
                continue
            else:
                new_paras.append(p)
        else:
            new_paras.append(p)
            i += 1

    # Now update all tags in KO to match EN tags 1:1
    en_paras = [p.strip() for p in open('chapters/ch22_en.txt', encoding='utf-8').read().split('\n\n') if p.strip()]
    en_tags = [re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p).group(1) for p in en_paras if re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)]

    realigned_ko = []
    for idx, p in enumerate(new_paras):
        if idx < len(en_tags):
            target_tag = en_tags[idx]
            p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', f'[{target_tag}]', p)
        realigned_ko.append(p)

    with open(ko_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(realigned_ko) + '\n')

    print("Merged P051a/b in KO and realigned ch22_ko.txt 1:1 with EN (99 tags).")

if __name__ == '__main__':
    fix_ch22_p051()
