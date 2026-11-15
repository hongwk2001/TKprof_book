import json
with open('temp_out.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

text = data['ko']['P087d']
with open('p087_ko_dump.txt', 'w', encoding='utf-8') as f:
    for s in text.split('. '):
        f.write(s + '\n')
