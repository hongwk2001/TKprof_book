import json
file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_24.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
bad_blocks = []
for item in data:
    ko = item.get('ko', '')
    en = item.get('en', '')
    if '매우 복잡하고' in ko or 'stand out' in en:
        bad_blocks.append(item)
print(f'Remaining: {len(bad_blocks)}')
for i, item in enumerate(bad_blocks[:30]):
    print(f"TAG: {item['tag']}\nRAW: {item['raw']}")
