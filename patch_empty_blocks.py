import json
import os

translations = {
    "book1_ch_06.json": {
        "P088_5": {"ko": "어쨌든 돌아오실 때까지 제가 그를 돌볼 테니, 그 후에 그를 바로 옮기도록 하죠.", "en": "In any case, I will take care of him until you return, and then we will remove him straight."}
    },
    "book2_ch_01.json": {
        "P012_1": {"ko": "“젠장, 저 여자가 또 저러고 있네!”", "en": "Bust me, if she ain't at it again!"},
        "P022_3": {"ko": "당신의 그 기도에 매긴 값이 얼만지 말해봐!”", "en": "Name the price that you put your prayers at!"},
        "P023_1": {"ko": "“기도는 그저 마음에서 우러나오는 거예요, 제리.", "en": "They only come from the heart, Jerry."},
        "P027_1": {"ko": "“자, 짜증 유발자 부인!", "en": "Now, Aggerawayter!"},
        "P027_2": {"ko": "뭐 하는 거야?", "en": "What are you up to?"}
    },
    "book2_ch_04.json": {
        "P025_3": {"ko": "로리.", "en": "Lorry."}
    },
    "book2_ch_06.json": {
        "P085_6": {"ko": "저요.", "en": "I."},
        "P111_3": {"ko": "다네이.", "en": "Darnay."}
    },
    "book2_ch_10.json": {
        "P010_1": {"ko": "“찰스 다네이!", "en": "Charles Darnay!"}
    },
    "book2_ch_12.json": {
        "P009_3": {"ko": "스트라이버?", "en": "Stryver?"}
    },
    "book2_ch_17.json": {
        "P006_4": {"ko": "하지만 이번은 여느 때와는 전혀 달랐고, 그 어떤 것도 예전처럼 만들 수는 없었다.", "en": "but this time was not quite like any other, and nothing could make it so."},
        "P007_1": {"ko": "“아버지, 저는 오늘 밤 너무나도 행복해요.", "en": "And I am very happy tonight, dear father."},
        "P007_2": {"ko": "하늘이 축복해 주신 이 사랑, 찰스를 향한 저의 사랑과 저를 향한 찰스의 사랑 안에서 저는 깊은 행복을 느껴요.", "en": "I am deeply happy in the love that Heaven has so blessed--my love for Charles, and Charles's love for me."},
        "P007_3": {"ko": "하지만, 만약 제 삶이 여전히 아버지께 바쳐지지 않는다면, 혹은 제 결혼이 우리를 몇 블록의 거리만큼이라도 떼어놓도록 정해졌다면, 저는 지금 말로 다 할 수 없을 만큼 불행하고 자책감에 시달렸을 거예요.", "en": "But, if my life were not to be still consecrated to you, or if my marriage were so arranged as that it would part us, even by the length of a few of these streets, I should be more unhappy and self-reproachful now than I can tell you."},
        "P007_4": {"ko": "지금 이대로도--”", "en": "Even as it is--\""},
        "P008_1": {"ko": "그런 상황에서도 그녀는 목소리를 제대로 가눌 수 없었다.", "en": "Even as it was, she could not command her voice."},
        "P009_1": {"ko": "슬픈 달빛 속에서, 그녀는 그의 목을 끌어안고 그의 가슴에 얼굴을 묻었다.", "en": "In the sad moonlight, she clasped him by the neck, and laid her face upon his breast."},
        "P009_2": {"ko": "태양 빛 자체가 그러하듯, 그리고 인간의 삶이라 불리는 빛이 피어나고 저물 때 그러하듯, 언제나 슬픔을 머금고 있는 달빛 아래에서.", "en": "In the moonlight which is always sad, as the light of the sun itself is--as the light called human life is--at its coming and its going."},
        "P010_1": {"ko": "“사랑하는 아버지!", "en": "Dearest dear!"},
        "P010_2": {"ko": "마지막으로 제게 확실하게 말씀해 주시겠어요? 저의 그 어떤 새로운 애정이나 새로운 의무도 우리 사이에 결코 끼어들지 않을 거라는 걸 완전히 확신하신다고요. 저는 잘 알고 있지만, 아버지도 알고 계신가요?", "en": "Can you tell me, this last time, that you feel quite, quite sure, no new affections of mine, and no new duties of mine, will ever interpose between us? I know it well, but do you know it?"}
    },
    "book2_ch_21.json": {
        "P069_1": {"ko": "“에이.", "en": "A."}
    },
    "book2_ch_24.json": {
        "P029_4": {"ko": "영어로 번역된 그 주소는 이러했다.", "en": "The address, turned into English, ran:"}
    },
    "book3_ch_02.json": {
        "P030_3": {"ko": "전부 합쳐서 마흔 명이나 쉰 명 남짓이었다.", "en": "not more than forty or fifty in all."},
        "P034_3": {"ko": "만약 당신의 말이 확실하다면;", "en": "If you are sure of what you say;"}
    },
    "book3_ch_03.json": {
        "P030_3": {"ko": "“거리에서는 폭동이 빈번하게 일어나고 있어요.", "en": "there are frequent risings in the streets;"}
    },
    "book3_ch_06.json": {
        "P043_1": {"ko": "“루시!", "en": "Lucie!"}
    },
    "book3_ch_07.json": {
        "P019_2": {"ko": "우린 그런 건 이제 충분히 겪었어요.” 프로스 양이 말했다.", "en": "we have quite enough of that,” said Miss Pross."},
        "P020_1": {"ko": "“쉿, 얘야!", "en": "Hush, dear!"},
        "P037_1": {"ko": "“내가 그를 찾고 있소.", "en": "I seek him."}
    },
    "book3_ch_13.json": {
        "P102_1": {"ko": "“거기 누구냐?", "en": "Who goes here?"},
        "P108_3": {"ko": "루시.", "en": "Lucie."},
        "P114_3": {"ko": "시드니 칼튼.", "en": "Sydney Carton."},
        "P118_2": {"ko": "그건 별로 대단한 일이 아니잖아!", "en": "It is not a great deal, that!"},
        "P118_4": {"ko": "자비스 로리.", "en": "Jarvis Lorry."},
        "P126_1": {"ko": "“우리 너무 천천히 가고 있는 거 아니에요?", "en": "Are we not going too slowly?"},
        "P131_3": {"ko": "여기 아까 왔던 곳 아닌가?", "en": "Is not this the same place twice over?"},
        "P131_5": {"ko": "어떤 마을이었다.", "en": "A village."},
        "P133_4": {"ko": "우리가 쫓기고 있다고?", "en": "We are pursued?"},
        "P134_1": {"ko": "“워!", "en": "Ho!"},
        "P134_2": {"ko": "거기 마차 안에 있는 사람들.", "en": "Within the carriage there."},
        "P134_3": {"ko": "대답해!”", "en": "Speak then!"}
    }
}

base_dir = "c:/git_repo/TKprof_book/books/two_cities/json"
for f, items in translations.items():
    path = os.path.join(base_dir, f)
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    modified = False
    for block in data:
        if block['tag'] in items:
            block['ko'] = items[block['tag']]['ko']
            block['en'] = items[block['tag']]['en']
            modified = True
    
    if modified:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            
print("Patching complete.")
