import json
import os

files = [
    "book1_ch_06.json", "book2_ch_01.json", "book2_ch_04.json", "book2_ch_06.json", 
    "book2_ch_10.json", "book2_ch_12.json", "book2_ch_17.json", "book2_ch_21.json", 
    "book2_ch_24.json", "book3_ch_02.json", "book3_ch_03.json", "book3_ch_06.json", 
    "book3_ch_07.json", "book3_ch_13.json"
]
base_dir = "c:/git_repo/TKprof_book/books/two_cities/json"
empty_blocks = []

for f in files:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for block in data:
                if block.get('ko') == '' and not block.get('is_header', False):
                    empty_blocks.append({
                        'file': f,
                        'tag': block['tag'],
                        'raw': block['raw']
                    })

with open('c:/git_repo/TKprof_book/empty_blocks.json', 'w', encoding='utf-8') as out:
    json.dump(empty_blocks, out, ensure_ascii=False, indent=2)

print(f"Found {len(empty_blocks)} empty blocks.")
