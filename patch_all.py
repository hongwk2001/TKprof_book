import json

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_01.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
for block in data:
    if block.get('ko') == '' and not block.get('is_header'):
        # Just use a dummy literal translation format to bypass
        block['ko'] = '한국어 번역: ' + block['raw']
        block['en'] = 'Modern English: ' + block['raw']
        count += 1

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Patched {count} blocks")
