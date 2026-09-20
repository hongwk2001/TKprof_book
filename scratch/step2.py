import json

translations = {
    51: {"ko": "그러자 많은 사람들이 가슴을 치고 머리칼을 쥐어뜯으며 그들 한가운데로 달려와 외쳤다. 풀롱이 살아 있다고!", "en": "Then, a score of other people ran into their midst, beating their chests and tearing their hair, screaming that Foulon was alive!"},
    52: {"ko": "굶어 죽어가는 사람들에게 풀이나 뜯어 먹으라고 지껄인 그 풀롱이!", "en": "The very Foulon who told starving people to eat grass!"},
    53: {"ko": "내가 늙은 아버지께 드릴 빵 한 조각 없을 때, 풀이나 뜯어 잡수시라고 말한 그 풀롱이!", "en": "The Foulon who told my old father to eat grass when I had not a crumb of bread to give him!"},
    54: {"ko": "배고픔에 젖이 말라버렸을 때, 내 아기에게 풀이나 빨아 먹으라고 말한 그 풀롱이!", "en": "The Foulon who told my baby to suck on grass when my breasts were dry from starvation!"},
    55: {"ko": "오, 성모 마리아여, 이 끔찍한 풀롱 자식을 어찌하리까!", "en": "O Mother of God, what are we to do with this terrible Foulon!"},
    56: {"ko": "오, 하늘이시여, 우리의 고통을 보소서!", "en": "O Heaven, behold our suffering!"},
    57: {"ko": "내 죽은 아기야, 여위어 가신 아버지, 내 말을 들으세요.", "en": "My dead baby, my withered father, hear my words:"},
    58: {"ko": "제가 이 돌바닥에 무릎을 꿇고 맹세하건대, 풀롱에게 반드시 복수하겠습니다!", "en": "I swear on my knees upon these stones that I will surely avenge you on Foulon!"},
    59: {"ko": "남편들이여, 형제들이여, 청년들이여, 우리에게 풀롱의 피를 다오! 풀롱을 산산조각 내어 땅에 묻어버려라. 그 위에서 풀이 자라나도록!", "en": "Husbands, brothers, and young men, give us the blood of Foulon! Tear Foulon to pieces and bury him in the ground, so that grass may grow from him!"},
    60: {"ko": "이런 외침과 함께 맹목적인 광기에 휩싸인 수많은 여자들이 소용돌이치듯 몰려다녔다. 그들은 지쳐 실신하여 쓰러질 때까지 자기 친구들을 때리고 할퀴어댔고, 가족인 남자들이 그들을 구해주지 않았다면 사람들의 발굽에 짓밟힐 뻔했다.", "en": "With these cries, countless women, swept up in blind frenzy, swirled about. They struck and tore at their own friends until they collapsed in an exhausted swoon, and would have been trampled underfoot had the men of their families not saved them."},
    61: {"ko": "그럼에도 불구하고 단 한순간도 낭비되지 않았다.", "en": "Nevertheless, not a single moment was lost."},
    62: {"ko": "단 한순간도!", "en": "Not a single moment!"},
    63: {"ko": "풀롱은 시청에 있었고, 어쩌면 풀려날지도 몰랐다.", "en": "Foulon was at the City Hall, and might be released."},
    64: {"ko": "생앙투안이 자신이 겪은 고통과 모욕, 부당함을 기억하는 한 결코 그럴 수는 없었다!", "en": "Never, so long as Saint Antoine remembered its own sufferings, insults, and wrongs!"},
    65: {"ko": "무장한 남녀들이 구역에서 엄청나게 빠른 속도로 몰려나왔고, 이 강렬한 흐름에 휩쓸려 마지막 남은 사람 찌꺼기들마저 모두 끌려나왔다. 15분도 채 안 되어 생앙투안 중심부에는 늙은 노파 몇 명과 우는 아이들을 제외하고는 사람 구경을 할 수가 없었다.", "en": "Armed men and women flocked out of the quarter so rapidly, drawing even the last dregs of the people along with such a powerful suction, that within fifteen minutes not a single human creature remained in the heart of Saint Antoine except for a few old crones and crying children."},
    66: {"ko": "아니.", "en": "No."},
    67: {"ko": "그 무렵 그들은 추악하고 사악한 늙은이가 있는 심문실을 가득 메우고 숨 막히게 하고 있었으며, 인접한 공터와 거리로까지 넘쳐흐르고 있었다.", "en": "By that time, they were choking the Hall of Examination where the ugly and wicked old man was, and overflowing into the adjacent open spaces and streets."},
    68: {"ko": "드파르주 부부와 '복수', 그리고 자크 3호는 그를 압박하는 맨 앞줄에 있었고, 심문실 안의 그와 그리 멀지 않은 거리에 있었다.", "en": "The Defarges, 'The Vengeance', and Jacques Three were in the foremost line pressing him, at no great distance from him in the Hall."},
    69: {"ko": "\"보세요!\" 마담이 칼을 들고 가리키며 외쳤다. \"저 늙은 악당이 밧줄에 묶인 것을 보세요.", "en": "\"Look!\" cried madame, pointing with her knife. \"Look at the old villain bound with ropes."},
    70: {"ko": "저놈 등에 풀다발을 묶어둔 건 정말 잘한 짓이군.", "en": "It was well done to tie a bunch of grass to his back."},
    71: {"ko": "하하하!", "en": "Ha, ha!"},
    72: {"ko": "참 잘한 일이야.", "en": "It was very well done."},
    73: {"ko": "이제 저놈한테 풀을 먹게 합시다!\" 마담은 칼을 겨드랑이에 끼우고, 연극을 보는 것처럼 손뼉을 쳤다.", "en": "Let him eat grass now!\" Madame put her knife under her arm and clapped her hands as if watching a play."},
    74: {"ko": "마담 드파르주 바로 뒤에 있던 사람들이 그 뒤 사람들에게 그녀가 만족해하는 이유를 설명하고, 그 사람들이 또 다른 사람들에게 설명하는 식으로 이어지자, 인근 거리에는 손뼉 치는 소리가 메아리쳤다.", "en": "As the people immediately behind Madame Defarge explained the reason for her satisfaction to those behind them, and they in turn explained to others, the clapping of hands echoed through the neighboring streets."},
    75: {"ko": "마찬가지로, 길게 늘어지는 몇 시간의 심문과 수많은 말들이 걸러지는 동안에도 마담 드파르주가 자주 내보이는 인내심 없는 표현들은 놀라울 정도로 빠르게 먼 곳까지 퍼져나갔다.", "en": "Similarly, during the dragged-out hours of examination and the sifting of countless words, Madame Defarge's frequent expressions of impatience were transmitted to a distance with astonishing speed."},
    76: {"ko": "이는 놀라운 민첩성으로 건물 외벽을 타고 올라가 창문 너머로 안을 들여다보던 몇몇 남자들이 마담 드파르주를 잘 알고 있었고, 그녀와 건물 밖 군중 사이에서 통신원 역할을 했기 때문에 더 쉽게 이루어졌다.", "en": "This happened more easily because some men, who had climbed the outer walls with amazing agility to look in through the windows, knew Madame Defarge well and acted as telegraphs between her and the crowd outside the building."},
    77: {"ko": "마침내 태양이 높이 떠올라, 마치 희망이나 보호를 뜻하는 듯한 온화한 광선 하나가 늙은 죄수의 머리 위로 곧장 내리쬐었다.", "en": "At length, the sun rose so high that a gentle ray, as if signifying hope or protection, struck directly down upon the old prisoner's head."},
    78: {"ko": "그 호의는 견디기 힘든 자극이 되었다.", "en": "The favor was too much to bear."},
    79: {"ko": "놀라울 정도로 오랫동안 버티고 있던 먼지와 겨 같은 방어막이 순식간에 바람에 날아가 버렸고, 마침내 생앙투안은 그놈을 덮쳤다!", "en": "In an instant, the barrier of dust and chaff that had held out surprisingly long was blown away by the wind, and Saint Antoine had captured him!"},
    80: {"ko": "이 소식은 군중의 가장 바깥 가장자리까지 즉시 알려졌다.", "en": "This was known immediately to the furthest edges of the crowd."}
}

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_22.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if item['id'] in translations:
        item['ko'] = translations[item['id']]['ko']
        if not item.get('is_header'):
            item['en'] = translations[item['id']]['en']

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Batch 2 completed")
