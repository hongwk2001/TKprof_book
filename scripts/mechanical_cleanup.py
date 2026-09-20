import json
import glob
import os

files = sorted(glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/book*_ch_*.json'))
bad_patterns = [
    '상황의 전개를 묘사하며',
    '이 문장은 원문을 자연스럽게 번역한 것입니다',
    'They looked at each other quietly',
    '조용히 서로를 바라보며',
    'highly complex and detailed descriptions',
    '매우 복잡하고',
    'Explanatory translation:',
    'This sentence is a natural translation',
    '이 문장은 자연스러운_',
    'The updated sentence is modern_'
]

total_fixed = 0

for f in files:
    try:
        data = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        continue
        
    changed = False
    for b in data:
        if not isinstance(b, dict): continue
        raw = b.get('raw', '')
        en = b.get('en', '')
        ko = b.get('ko', '')
        
        is_bad = False
        if any(p in en or p in ko for p in bad_patterns):
            is_bad = True
        elif len(raw) < 50 and len(ko) > 100:
            is_bad = True
            
        if is_bad:
            # If it's a short fragment, just copy the raw text over to avoid LLM hallucinations
            if len(raw) < 50:
                b['ko'] = raw
                b['en'] = raw
            else:
                # If it's a long sentence that got corrupted, wipe it so it gets re-translated
                b['ko'] = ''
                b['en'] = ''
            changed = True
            total_fixed += 1
            
    if changed:
        with open(f, 'w', encoding='utf-8') as out:
            json.dump(data, out, ensure_ascii=False, indent=2)

print(f"Mechanical cleanup complete. Fixed {total_fixed} bad blocks across all files.")
