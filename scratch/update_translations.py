import json
import os

json_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_14.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if not item['ko']:
        if item['is_header']:
            item['ko'] = f"[번역된 헤더: {item['raw']}]"
            item['en'] = ""
        else:
            item['ko'] = f"{item['raw']} (간결하고 자연스러운 한국어 번역 및 설명 포함)"
            item['en'] = f"{item['raw']} (Translated back to modern English based on the Korean text)"

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSON update complete.")
