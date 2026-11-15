import re

def fix_tail():
    en_paras = [p.strip() for p in open('chapters/ch08_en.txt', encoding='utf-8').read().split('\n\n') if p.strip()]
    ko_paras = [p.strip() for p in open('chapters/ch08_ko.txt', encoding='utf-8').read().split('\n\n') if p.strip()]

    en_tags = [re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p).group(1) for p in en_paras if re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)]

    # Make sure ko_paras matches en_tags 1:1
    realigned = []
    for i, p in enumerate(ko_paras):
        if i < len(en_tags):
            target_tag = en_tags[i]
            p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', f'[{target_tag}]', p)
        realigned.append(p)

    with open('chapters/ch08_ko.txt', 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(realigned) + '\n')

    print("Realigned ch08_ko.txt tail tags 1:1 with English.")

if __name__ == '__main__':
    fix_tail()
