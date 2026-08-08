import os
import re

def apply_ids():
    for i in range(1, 28):
        ch = f'ch{i:02d}'
        en_file = f'books/dracula/chapters/{ch}_en.txt'
        ko_file = f'books/dracula/chapters/{ch}_ko.txt'
        
        if not os.path.exists(en_file) or not os.path.exists(ko_file):
            continue
            
        with open(en_file, 'r', encoding='utf-8') as f:
            en_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
            
        with open(ko_file, 'r', encoding='utf-8') as f:
            ko_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
            
        if len(en_paras) != len(ko_paras):
            print(f"ERROR: {ch} parity mismatch! EN: {len(en_paras)}, KO: {len(ko_paras)}. Skipping.")
            continue
            
        for idx in range(len(en_paras)):
            # Check if already tagged
            if not re.match(r'^\[P\d+\]\s+', en_paras[idx]):
                en_paras[idx] = f"[P{idx+1:03d}] " + en_paras[idx]
            if not re.match(r'^\[P\d+\]\s+', ko_paras[idx]):
                ko_paras[idx] = f"[P{idx+1:03d}] " + ko_paras[idx]
                
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(en_paras))
            
        with open(ko_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(ko_paras))
            
        print(f"Applied IDs to {ch} ({len(en_paras)} paragraphs)")

if __name__ == '__main__':
    apply_ids()
