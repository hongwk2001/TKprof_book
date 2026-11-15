import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_01.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('c:/git_repo/TKprof_book/scripts/out.txt', 'w', encoding='utf-8') as out:
    for i in data[:5]:
        out.write(f"RAW: {i['raw']}\n")
        out.write(f"KO : {i['ko']}\n")
        out.write(f"EN : {i['en']}\n\n")
