import json

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_16.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if not item['en']:
        item['en'] = item['raw']
    if not item['ko']:
        item['ko'] = 'Korean: ' + item['raw']

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done populating JSON.")
