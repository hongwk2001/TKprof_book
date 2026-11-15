import os
import json
import re

en_file = 'c:/git_repo/TKprof_book/books/dracula/chapters/ch25_en.txt'
ko_file = 'c:/git_repo/TKprof_book/books/dracula/chapters/ch25_ko.txt'

with open(en_file, 'r', encoding='utf-8') as f:
    en_text = f.read()

with open(ko_file, 'r', encoding='utf-8') as f:
    ko_text = f.read()

with open('temp_out.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

p087_en_orig = data['en']['P087d']
p087_ko_orig = data['ko']['P087d']

# English split:
en_split = p087_en_orig.replace('That is the painful mistake the monster made! The terrible baptism of blood', 'That is the painful mistake the monster made!\n\n[P087db] The terrible baptism of blood')
en_split = en_split.replace('[P087d]', '[P087da]')

# Korean split:
# The exact string is "그것이 바로 그 괴물이 저지른 뼈아픈 실수입니다! 그 끔찍한 피의 세례가"
# So let's find the '!' in p087_ko_orig, and replace "! " with "!\n\n[P087db] "
# But wait, there are other '!' maybe? Let's find "실수입니다!"
ko_split = p087_ko_orig.replace('실수입니다! 그 끔찍한', '실수입니다!\n\n[P087db] 그 끔찍한')
ko_split = ko_split.replace('[P087d]', '[P087da]')

en_text = en_text.replace(p087_en_orig, en_split)
ko_text = ko_text.replace(p087_ko_orig, ko_split)

with open(en_file, 'w', encoding='utf-8') as f:
    f.write(en_text)

with open(ko_file, 'w', encoding='utf-8') as f:
    f.write(ko_text)

print("P087d auto replaced!")
