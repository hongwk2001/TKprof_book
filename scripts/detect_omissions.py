import json
import glob
import os

suspicious = []

for filepath in glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/*.json'):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        raw = item.get('raw', '')
        en = item.get('en', '')
        
        if item.get('is_header') or not raw or not en:
            continue
            
        raw_words = len(raw.split())
        en_words = len(en.split())
        
        if raw_words < 3:
            continue
            
        ratio = en_words / raw_words
        
        if ratio < 0.5 and raw_words >= 8:
            suspicious.append({
                'file': os.path.basename(filepath),
                'tag': item['tag'],
                'raw': raw,
                'en': en,
                'ratio': round(ratio, 2)
            })

suspicious.sort(key=lambda x: x['ratio'])
print(f"Found {len(suspicious)} potentially omitted/severely truncated blocks.")
for s in suspicious[:10]:
    print(f"\n[{s['file']} | {s['tag']} | Ratio: {s['ratio']}]")
    print(f"RAW: {s['raw']}")
    print(f"EN : {s['en']}")
