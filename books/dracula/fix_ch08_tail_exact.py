import re

def fix_ch08_tail_exact():
    filepath = 'chapters/ch08_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    paras = [p.strip() for p in text.split('\n\n') if p.strip()]

    # We need to map the last 5 paragraphs in KO to [P071a], [P071b], [P072], [P073], [P074]
    new_paras = []
    for p in paras:
        if '주인님, 당신의 명을 받들기 위해' in p:
            p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', '[P071a]', p)
        elif '어쨌거나 그는 속물적이고' in p:
            p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', '[P071b]', p)
        elif '그 정도의 힘과 집념이라면' in p:
            p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', '[P072]', p)
        elif '기다리겠습니다, 주인님' in p:
            p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', '[P073]', p)
        elif '그래서 나도 그 말에서 힌트를' in p:
            p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', '[P074]', p)
        new_paras.append(p)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_paras) + '\n')

    print("Fixed end of ch08_ko.txt to P074.")

if __name__ == '__main__':
    fix_ch08_tail_exact()
