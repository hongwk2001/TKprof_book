import json
with open('c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_13.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
missing = [b for b in data if b.get('ko') == '' and not b.get('is_header', False)]
batch = missing[0:70]
for b in batch:
    print(b['tag'] + ':::' + b['raw'])
