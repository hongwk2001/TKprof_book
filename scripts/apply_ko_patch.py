import json
import glob
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read all the translated outputs from the subagents
translated_files = glob.glob('c:/git_repo/TKprof_book/translated_batches/batch_*.json')
translations = {}

for tf in translated_files:
    try:
        batch_data = json.load(open(tf, encoding='utf-8'))
        for item in batch_data:
            # Key format: filename_id
            key = f"{item['file']}_{item['id']}"
            translations[key] = item['ko']
    except Exception as e:
        print(f"Error reading {tf}: {e}")

if not translations:
    print("No translations found to patch.")
    sys.exit(1)

# Patch the master files
master_files = sorted(glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/book*_ch_*.json'))
patched = 0

for mf in master_files:
    file_name = mf.split('/')[-1].split('\\')[-1]
    try:
        data = json.load(open(mf, encoding='utf-8'))
        changed = False
        
        for b in data:
            if not isinstance(b, dict) or b.get('is_header'):
                continue
                
            key = f"{file_name}_{b.get('id')}"
            if key in translations:
                b['ko'] = translations[key]
                changed = True
                patched += 1
                
        if changed:
            with open(mf, 'w', encoding='utf-8') as out:
                json.dump(data, out, ensure_ascii=False, indent=2)
                
    except Exception as e:
        print(f"Error patching {file_name}: {e}")

print(f"Successfully and safely patched {patched} blocks into the master JSON files.")
