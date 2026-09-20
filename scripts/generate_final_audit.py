import json
import glob
import random
import os

files = sorted(glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/book*_ch_*.json'))

all_blocks = []
for f in files:
    try:
        data = json.load(open(f, encoding='utf-8'))
    except:
        continue
    for b in data:
        if isinstance(b, dict) and not b.get('is_header') and b.get('ko') and b.get('en'):
            b['file'] = os.path.basename(f)
            all_blocks.append(b)

random.seed(777)
sample = random.sample(all_blocks, 30)

with open('c:/git_repo/TKprof_book/final_audit_sample.json', 'w', encoding='utf-8') as out:
    json.dump(sample, out, ensure_ascii=False, indent=2)

print(f"Generated final_audit_sample.json with 30 blocks.")
