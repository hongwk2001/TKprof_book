import json

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_07.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

patches = {
    "P055_1": {
        "ko": "\"글쎄요!",
        "en": "\"Well!"
    },
    "P055_2": {
        "ko": "정말로 이것은 규정 위반이오.",
        "en": "It really is against the rules."
    },
    "P055_3": {
        "ko": "하지만 그는 시민 Defarge와 여성 시민 Defarge에 의해 고발당했소—그것도 심각하게 말이오.",
        "en": "But he has been denounced—and severely at that—by Citizen Defarge and Citizeness Defarge."
    },
    "P055_4": {
        "ko": "그리고 다른 한 사람에게도 말이오.\"",
        "en": "And by one other person.\""
    },
    "P056_1": {
        "ko": "\"다른 한 사람이라니?\"",
        "en": "\"What other person?\""
    },
    "P057_1": {
        "ko": "\"당신이 묻는 거요, 시민 의사(Manette 박사)?\"",
        "en": "\"Are you the one asking, Citizen Doctor?\""
    },
    "P058_1": {
        "ko": "\"그렇소.\"",
        "en": "\"Yes.\""
    },
    "P059_1": {
        "ko": "\"그렇다면,\" Saint Antoine에서 온 그 남자가 묘한 표정을 지으며 말했다. \"내일 대답을 듣게 될 거요.",
        "en": "\"Then,\" said the man from Saint Antoine with a strange look, \"you will receive an answer tomorrow."
    },
    "P059_2": {
        "ko": "이제, 나는 입을 다물겠소!\"",
        "en": "Now, I will keep my mouth shut!\""
    }
}

count = 0
for d in data:
    if d['tag'] in patches:
        d['ko'] = patches[d['tag']]['ko']
        d['en'] = patches[d['tag']]['en']
        count += 1

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Patched {count} blocks.")
