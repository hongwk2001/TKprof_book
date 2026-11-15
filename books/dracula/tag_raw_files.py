import os
import shutil

BACKUP_DIR = r'c:\git_repo\TKprof_book\books\dracula\chapters_backup'
TARGET_DIR = r'c:\git_repo\TKprof_book\books\dracula\chapters'

def tag_raw_files():
    for i in range(1, 28):
        ch = f"{i:02d}"
        in_path = os.path.join(BACKUP_DIR, f'raw_ch_{ch}.txt')
        out_path = os.path.join(TARGET_DIR, f'raw_ch_{ch}.txt')
        
        with open(in_path, 'r', encoding='utf-8') as f:
            paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
            
        tagged_paras = []
        for idx, p in enumerate(paras):
            tag = f"[P{idx+1:03d}]"
            tagged_paras.append(f"{tag} {p}")
            
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(tagged_paras))
            
        print(f"Tagged Ch {ch}: {len(paras)} paragraphs")

if __name__ == '__main__':
    tag_raw_files()
