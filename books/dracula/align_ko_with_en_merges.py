import glob
import re

def align_ko_chapter(ch_num):
    en_path = f"chapters/ch{ch_num:02d}_en.txt"
    ko_path = f"chapters/ch{ch_num:02d}_ko.txt"
    
    with open(en_path, 'r', encoding='utf-8') as f:
        en_text = f.read().strip()
    with open(ko_path, 'r', encoding='utf-8') as f:
        ko_text = f.read().strip()

    en_paras = [p.strip() for p in en_text.split('\n\n') if p.strip()]
    ko_paras = [p.strip() for p in ko_text.split('\n\n') if p.strip()]

    en_tags = [re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p).group(1) for p in en_paras if re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)]

    if len(en_paras) == len(ko_paras):
        # Simply update tags in KO to match EN 1:1
        realigned_ko = []
        for i, p in enumerate(ko_paras):
            target_tag = en_tags[i]
            p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', f'[{target_tag}]', p)
            realigned_ko.append(p)
        with open(ko_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(realigned_ko) + '\n')
        print(f"Ch {ch_num:02d}: Re-aligned KO tags 1:1 with EN ({len(en_paras)} tags).")
    else:
        print(f"Ch {ch_num:02d}: EN={len(en_paras)} vs KO={len(ko_paras)} (Count mismatch, requires block alignment)")

def main():
    for i in range(1, 28):
        align_ko_chapter(i)

if __name__ == '__main__':
    main()
