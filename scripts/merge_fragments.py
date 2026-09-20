import json
import glob
import os
import re

files = sorted(glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/book*_ch_*.json'))

# Common abbreviations that shouldn't end a sentence
abbrevs = (
    'Mr.', 'Mrs.', 'Dr.', 'St.', 'Prof.', 'Rev.', 'Capt.', 'Col.', 'Gen.', 
    'Lieut.', 'Mt.', 'Vol.', 'Fig.', 'e.g.', 'i.e.', 'etc.'
)

total_merged = 0
files_changed = 0

for f in files:
    try:
        data = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        continue
        
    new_data = []
    i = 0
    changed = False
    
    while i < len(data):
        block = data[i]
        
        # Check if this block ends with an abbreviation
        if isinstance(block, dict) and not block.get('is_header'):
            raw = block.get('raw', '').strip()
            
            # If it ends with an abbreviation and there's a next block
            if raw.endswith(abbrevs) and i + 1 < len(data):
                next_block = data[i+1]
                if isinstance(next_block, dict) and not next_block.get('is_header'):
                    # Merge them!
                    print(f"Merging in {os.path.basename(f)}:\n  1: {raw}\n  2: {next_block.get('raw', '')[:50]}...")
                    
                    merged_block = {
                        "id": block["id"],
                        "tag": block["tag"], # Keep the first tag
                        "raw": raw + " " + next_block.get('raw', '').lstrip(),
                        "en": "", # Wipe translations so it gets re-translated cohesively
                        "ko": "",
                        "is_header": False
                    }
                    new_data.append(merged_block)
                    i += 2 # Skip the next block since we merged it
                    changed = True
                    total_merged += 1
                    continue
                    
        new_data.append(block)
        i += 1
        
    if changed:
        # We need to re-index the IDs and Tags just in case
        for idx, b in enumerate(new_data):
            if isinstance(b, dict):
                b['id'] = idx + 1
                # We don't strictly need to rename the tag (e.g. P002_1), but we can leave it as is
        
        with open(f, 'w', encoding='utf-8') as out:
            json.dump(new_data, out, ensure_ascii=False, indent=2)
        files_changed += 1

print(f"\nDone! Merged {total_merged} fragmented blocks across {files_changed} files.")
