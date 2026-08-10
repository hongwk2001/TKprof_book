import json
import re

ko = json.load(open('task.json', encoding='utf-8'))[0]['korean_original']

with open('dump.txt', 'w', encoding='utf-8') as f:
    idx = ko.find("그건 다 쓸데없는 헛소리요,")
    f.write(ko[idx:idx+1000] + '\n\n')

    idx = ko.find("에드워드 스펜슬라")
    f.write(ko[idx-200:idx+1000] + '\n\n')
