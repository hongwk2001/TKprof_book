import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_04.json', encoding='utf-8') as f:
    d = json.load(f)

fixes = {
  'P045_2': {'ko': 'Lorry 씨가 말했다, “그 책임을 맡게 되어서 말입니다.', 'en': 'Lorry, “to be entrusted with the charge.'},
  'P045_3': {'ko': '그것을 수행하게 되면 더 기쁠 것입니다.”', 'en': 'I shall be more happy to execute it.”'}
}

count = 0
for b in d:
    if b['tag'] in fixes:
        b['ko'] = fixes[b['tag']]['ko']
        b['en'] = fixes[b['tag']]['en']
        count += 1

with open('c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_04.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Patched {count} blocks.")
