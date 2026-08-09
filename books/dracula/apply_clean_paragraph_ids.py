import os
import re

chapters_dir = r"C:\git_repo\TKprof_book\books\dracula\chapters"

def main():
    for i in range(1, 28):
        ch = f"ch{i:02d}"
        en_file = os.path.join(chapters_dir, f"{ch}_en.txt")
        ko_file = os.path.join(chapters_dir, f"{ch}_ko.txt")
        
        if not os.path.exists(en_file) or not os.path.exists(ko_file):
            print(f"Skipping {ch} (files do not exist)")
            continue
            
        with open(en_file, 'r', encoding='utf-8') as f:
            en_content = f.read().replace('\r\n', '\n').strip()
        with open(ko_file, 'r', encoding='utf-8') as f:
            ko_content = f.read().replace('\r\n', '\n').strip()
            
        if '\n\n' not in en_content:
            en_paras = [p.strip() for p in en_content.split('\n') if p.strip()]
        else:
            en_paras = [p.strip() for p in en_content.split('\n\n') if p.strip()]
            
        if '\n\n' not in ko_content:
            ko_paras = [p.strip() for p in ko_content.split('\n') if p.strip()]
        else:
            ko_paras = [p.strip() for p in ko_content.split('\n\n') if p.strip()]
        
        if len(en_paras) != len(ko_paras):
            print(f"ERROR: {ch} count mismatch! EN: {len(en_paras)}, KO: {len(ko_paras)}")
            continue
            
        tagged_en = []
        tagged_ko = []
        for idx in range(len(en_paras)):
            clean_en = re.sub(r'^\[P\d+\]\s*', '', en_paras[idx])
            clean_ko = re.sub(r'^\[P\d+\]\s*', '', ko_paras[idx])
            
            tagged_en.append(f"[P{idx+1:03d}] {clean_en}")
            tagged_ko.append(f"[P{idx+1:03d}] {clean_ko}")
            
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(tagged_en))
        with open(ko_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(tagged_ko))
            
        print(f"Successfully applied clean IDs to {ch} ({len(en_paras)} paragraphs)")

if __name__ == '__main__':
    main()
