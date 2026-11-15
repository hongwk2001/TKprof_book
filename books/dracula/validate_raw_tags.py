import os
import re

BACKUP_DIR = r'c:\git_repo\TKprof_book\books\dracula\chapters_backup'
TARGET_DIR = r'c:\git_repo\TKprof_book\books\dracula\chapters'

def strip_tags(text):
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())

def validate_raw_tags():
    errors = 0
    for i in range(1, 28):
        ch = f"{i:02d}"
        orig_path = os.path.join(BACKUP_DIR, f'raw_ch_{ch}.txt')
        new_path = os.path.join(TARGET_DIR, f'raw_ch_{ch}.txt')
        
        with open(orig_path, 'r', encoding='utf-8') as f:
            orig_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
            
        with open(new_path, 'r', encoding='utf-8') as f:
            new_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
            
        if len(orig_paras) != len(new_paras):
            print(f"ERROR: Ch {ch} length mismatch! Orig: {len(orig_paras)}, New: {len(new_paras)}")
            errors += 1
            continue
            
        for idx, (orig, new) in enumerate(zip(orig_paras, new_paras)):
            stripped_new = strip_tags(new)
            if orig != stripped_new:
                print(f"ERROR: Ch {ch} text mismatch at paragraph {idx+1}")
                print(f"Orig: {orig[:50]}...")
                print(f"New:  {stripped_new[:50]}...")
                errors += 1
                
        print(f"Ch {ch} validation PASS")
        
    if errors == 0:
        print("ALL VALIDATIONS PASSED. Zero errors.")
    else:
        print(f"FAILED with {errors} errors.")

if __name__ == '__main__':
    validate_raw_tags()
