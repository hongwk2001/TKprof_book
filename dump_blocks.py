import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_03.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

subset = data[261:348]

with open('c:/git_repo/TKprof_book/blocks_261_347.txt', 'w', encoding='utf-8') as f:
    for block in subset:
        f.write(f"ID: {block['id']} | TAG: {block['tag']}\n")
        f.write(f"RAW: {block['raw']}\n")
        f.write('---\n')
