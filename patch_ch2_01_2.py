import json

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_01.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

patches = {
    "P035_2": {
        "ko": '시작부터 이른 일거리가 들어왔네요!"',
        "en": 'Here is an early job to begin with!"'
    },
    "P036_1": {
        "ko": '이렇게 아버지에게 행운을 빌어준 후, 어린 Jerry는 의자에 앉아 아버지가 씹던 짚에 대한 자신의 상속권(reversionary interest: 물려받을 권리를 뜻하는 법률 용어)을 행사하기 시작하며 곰곰이 생각에 잠겼습니다.',
        "en": 'Having thus wished his parent God speed, young Jerry sat down on the stool, took up his reversionary interest in the straw his father had been chewing, and cogitated.'
    },
    "P037_1": {
        "ko": '"항상 녹슬었어!',
        "en": '"Always rusty!'
    },
    "P037_2": {
        "ko": '아버지 손가락은 항상 녹슬어 있단 말이야!" 어린 Jerry가 중얼거렸습니다. "아버지는 저 쇠녹을 다 어디서 묻혀 오는 거지?',
        "en": 'His fingers are always rusty!" muttered young Jerry. "Where does my father get all that iron rust from?'
    },
    "P037_3": {
        "ko": '여기서는 쇠녹이 묻을 일이 없는데 말이야!"',
        "en": 'He doesn\'t get any iron rust here!"'
    }
}

for item in data:
    if item['tag'] in patches:
        item['ko'] = patches[item['tag']]['ko']
        item['en'] = patches[item['tag']]['en']

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Patch 2 done")
