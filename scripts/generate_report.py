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

with open('C:/Users/hongw/.gemini/antigravity/brain/c6a5c102-f9fe-450d-a245-40c618981c84/omissions_report.md', 'w', encoding='utf-8') as out:
    out.write("# Omissions and Truncations Report\n\n")
    out.write(f"**Found {len(suspicious)} potentially omitted or severely truncated blocks.**\n\n")
    out.write("This report flags blocks where the modernized text length is less than 50% of the raw text length.\n\n")
    
    for s in suspicious:
        out.write(f"### `{s['file']}` - Tag: `{s['tag']}` (Ratio: {s['ratio']})\n")
        out.write(f"**Raw**: {s['raw']}\n\n")
        out.write(f"**Modernized**: {s['en']}\n\n")
        out.write("---\n\n")
