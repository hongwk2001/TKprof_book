import os
import json

en_file = 'c:/git_repo/TKprof_book/books/dracula/chapters/ch25_en.txt'
ko_file = 'c:/git_repo/TKprof_book/books/dracula/chapters/ch25_ko.txt'

with open(en_file, 'r', encoding='utf-8') as f:
    en_text = f.read()

with open(ko_file, 'r', encoding='utf-8') as f:
    ko_text = f.read()

with open('temp_out.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

p078_en_orig = data['en']['P078']
p078_ko_orig = data['ko']['P078']

p078_en_split = p078_en_orig.replace('That is the terrifying power of experience. A true criminal always commits one type of crime.', 'That is the terrifying power of experience.\n\n[P078b] A true criminal always commits one type of crime.')
p078_en_split = p078_en_split.replace('[P078]', '[P078a]')

p078_ko_split = p078_ko_orig.replace('그것이 바로 경험이 지닌 그 무서운 힘이다. 진짜 범죄자는 항상 한 가지 유형의 범죄만 저지른다.', '그것이 바로 경험이 지닌 그 무서운 힘이다.\n\n[P078b] 진짜 범죄자는 항상 한 가지 유형의 범죄만 저지른다.')
p078_ko_split = p078_ko_split.replace('[P078]', '[P078a]')

en_text = en_text.replace(p078_en_orig, p078_en_split)
ko_text = ko_text.replace(p078_ko_orig, p078_ko_split)

with open(en_file, 'w', encoding='utf-8') as f:
    f.write(en_text)

with open(ko_file, 'w', encoding='utf-8') as f:
    f.write(ko_text)

print("P078 replaced!")
