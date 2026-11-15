import re

def fix_ch08_complete():
    filepath = 'chapters/ch08_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    paras = [p.strip() for p in text.split('\n\n') if p.strip()]

    new_paras = []
    for p in paras:
        m = re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)
        if not m:
            new_paras.append(p)
            continue
        
        pid = m.group(1)

        # 1. Fix Index 63: P038 -> P037
        if pid == 'P038' and '10파운드' in p:
            p = re.sub(r'^\[P038\]', '[P037]', p)

        # 2. Fix Index 68-70: P044a/b/c -> P043a/b/c
        elif pid == 'P044a' and '그때 내 불쌍한' in p:
            p = re.sub(r'^\[P044a\]', '[P043a]', p)
        elif pid == 'P044b' and '그녀는 대답하기' in p:
            p = re.sub(r'^\[P044b\]', '[P043b]', p)
        elif pid == 'P044c' and '그가 왜 반했는지' in p:
            p = re.sub(r'^\[P044c\]', '[P043c]', p)

        # 3. Fix Index 71-72: P045a/b (Lucy dream) -> P044a/b
        elif pid == 'P045a' and '꿈이라기엔' in p:
            p = re.sub(r'^\[P045a\]', '[P044a]', p)
        elif pid == 'P045b' and '그러다 마치' in p:
            p = re.sub(r'^\[P045b\]', '[P044b]', p)

        # 4. Fix Index 73-74: P045a/b (Lucy laughter & mother) -> keep P045a/b
        # (already P045a and P045b)

        new_paras.append(p)

    # Now let's check where P045b (mother) is, and insert P046 (* * * * *) after it if missing
    final_paras = []
    has_p046 = any(re.match(r'^\[P046\]', p) for p in new_paras)
    
    for p in new_paras:
        final_paras.append(p)
        if not has_p046 and re.match(r'^\[P045b\]', p) and '어머니도' in p:
            final_paras.append('[P046] *       *       *       *       *')

    # Now for all paragraphs after P046, shift their tag to match English exact list!
    en_paras = [p.strip() for p in open('chapters/ch08_en.txt', encoding='utf-8').read().split('\n\n') if p.strip()]
    en_tags = [re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p).group(1) for p in en_paras if re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)]

    # From index 75 (which is P047 in EN), ensure KO tags match EN tags element by element
    realigned_paras = []
    for i, p in enumerate(final_paras):
        if i < len(en_tags):
            target_tag = en_tags[i]
            p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', f'[{target_tag}]', p)
        realigned_paras.append(p)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(realigned_paras) + '\n')

    print("Successfully realigned Chapter 08 tags 1:1 with English.")

if __name__ == '__main__':
    fix_ch08_complete()
