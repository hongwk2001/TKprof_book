import re

def fix_ch06():
    filepath = 'chapters/ch06_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    paras = text.split('\n\n')
    cleaned_paras = []

    for p in paras:
        # Strip hallucinated paragraph number prefixes like [P016] 16. or [P017a] 17.
        p = re.sub(r'^(\[P[a-zA-Z0-9_]+\])\s*\d+\.\s*', r'\1 ', p.strip())

        # Update P016 specifically
        if p.startswith('[P016]'):
            p = '[P016] "에드워드 스펜슬라, 선장, 1854년 4월 안드레스 연안에서 해적에게 살해됨, 향년 30세." 제가 돌아오자 스웨일스 할아버지가 계속해서 말했습니다.'

        cleaned_paras.append(p)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(cleaned_paras) + '\n')

    print("Fixed Ch 06 P016 and removed all embedded paragraph numbers from ch06_ko.txt!")

if __name__ == '__main__':
    fix_ch06()
