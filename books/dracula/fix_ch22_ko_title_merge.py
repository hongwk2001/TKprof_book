import re

def fix_ch22_ko():
    en_paras = [p.strip() for p in open('chapters/ch22_en.txt', encoding='utf-8').read().split('\n\n') if p.strip()]
    ko_paras = [p.strip() for p in open('chapters/ch22_ko.txt', encoding='utf-8').read().split('\n\n') if p.strip()]

    en_tags = [re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p).group(1) for p in en_paras if re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)]

    # Print where KO has an extra tag or mismatch
    print("EN tags:", len(en_tags))
    print("KO tags:", len(ko_paras))

    # If KO has P052a and P052b merged or split, let's inspect P052 in EN vs KO
    for i in range(min(len(en_tags), len(ko_paras))):
        m = re.match(r'^\[(P[a-zA-Z0-9_]+)\]', ko_paras[i])
        kt = m.group(1) if m else ''
        if en_tags[i] != kt:
            print(f"Mismatch at index {i}: EN [{en_tags[i]}] vs KO [{kt}]")
            break

if __name__ == '__main__':
    fix_ch22_ko()
