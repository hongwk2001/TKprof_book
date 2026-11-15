import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_14.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in data:
    if i.get('tag') in ['P011_2', 'P025_2']:
        print(f"TAG: {i['tag']}")
        print(f"RAW: {i['raw']}")
        print(f"EN : {i['en']}\n")
