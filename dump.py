import json

with open('c:/git_repo/TKprof_book/scratch_200_299.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

for i in items:
    if i.get('status') == 'pending':
        en = i.get('target_en', '').strip()
        is_header = i.get('is_header', False)
        print(f"ID: {i['id']} | HEADER: {is_header} | EN: {en}")
