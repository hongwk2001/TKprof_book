import json

with open('scratch_200_299.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

with open('en_texts.txt', 'w', encoding='utf-8') as out:
    for i in items:
        out.write(f"{i['file']}|{i['id']}|{i.get('target_en','')}\n")
