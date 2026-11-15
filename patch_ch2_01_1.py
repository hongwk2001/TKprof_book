import json

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_01.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

patches = {
    "P031_1": {
        "ko": '그가 자신을 "정직한 상인"이라고 즐겨 칭함에도 불구하고, 그것을 직업이라고 부르기에는 무리가 있었습니다. 그의 소도구라고는 등받이가 부서진 의자를 잘라 만든 나무 의자 하나가 전부였는데, 아버지의 곁을 걷던 어린 Jerry가 매일 아침 Temple Bar(템플 바: 런던 중심부에 위치한 역사적인 관문)에서 가장 가까운 은행 창문 아래로 그 의자를 옮겼습니다.',
        "en": 'Despite his favorite description of himself as "an honest tradesman," it could scarcely be called a trade. His only prop was a wooden stool made from a chair with a broken back cut down, which young Jerry, walking by his father\'s side, carried every morning to the banking-house window closest to Temple Bar:'
    },
    "P031_2": {
        "ko": '그곳에서 지나가는 마차에서 얻을 수 있는 첫 번째 짚더미를 주워다 잡역부의 발에서 느껴지는 추위와 습기를 막아주면, 그것으로 그날의 진지가 형성되었습니다.',
        "en": 'There, with the addition of the first handful of straw gleaned from passing vehicles to protect the odd-job-man\'s feet from the cold and damp, it formed the day\'s encampment.'
    },
    "P031_3": {
        "ko": '그의 이 자리에서, Mr.',
        "en": 'At this post of his, Mr.'
    },
    "P031_4": {
        "ko": 'Cruncher는 Temple Bar 그 자체만큼이나 Fleet-street와 Temple에 잘 알려져 있었고, 그 모습 또한 거의 비슷하게 험악했습니다(in-looking: 못생기고 험상궂은 모습을 뜻함).',
        "en": 'Cruncher was as well known to Fleet-street and the Temple as the Bar itself,--and was almost as ill-looking.'
    },
    "P032_1": {
        "ko": '9시 15분 전에 진지를 구축하고 Tellson 은행으로 들어가는 가장 나이 많은 남자들에게 삼각모를 만지며 인사하기 좋은 시간에, Jerry는 이 바람 부는 3월의 아침에 자신의 자리를 잡았습니다. 그의 옆에는 어린 Jerry가 서 있었는데, 그는 자신의 다정한 목적에 걸맞게 작고 만만한 지나가는 소년들에게 심각한 신체적, 정신적 상처를 입히기 위해 Temple Bar를 넘나들며 기습을 가하지 않을 때면 늘 그렇게 서 있었습니다.',
        "en": 'Having set up camp at a quarter to nine, well in time to tip his three-cornered hat to the oldest men as they went into Tellson\'s, Jerry took his post on this windy March morning. Young Jerry stood beside him, when he wasn\'t making raids through the Bar to inflict severe physical and mental injuries on passing boys small enough for his pleasant purpose.'
    },
    "P032_2": {
        "ko": '서로 무척이나 닮은 아버지와 아들은 두 사람의 눈 사이만큼이나 머리를 가까이 맞대고 Fleet-street의 아침 교통을 조용히 바라보는 모습이 원숭이 한 쌍과 상당히 닮아 보였습니다.',
        "en": 'Father and son, extremely alike, quietly watching the morning traffic on Fleet-street with their heads as close together as their own eyes, bore a strong resemblance to a pair of monkeys.'
    },
    "P032_3": {
        "ko": '다 자란 Jerry가 짚을 씹다 뱉어내는 우연한 상황과, 어린 Jerry의 반짝이는 눈이 Fleet-street의 다른 모든 것만큼이나 쉴 새 없이 아버지를 경계하며 지켜보는 모습은 그 닮은 꼴을 조금도 줄여주지 않았습니다.',
        "en": 'The resemblance was not diminished by the accidental circumstance of the mature Jerry biting and spitting out straw, while the twinkling eyes of the younger Jerry watched him as restlessly as they watched everything else on Fleet-street.'
    },
    "P033_1": {
        "ko": 'Tellson 은행에 소속된 정규 실내 사자(사환) 중 한 명의 머리가 문틈으로 나오며 지시가 떨어졌습니다.',
        "en": 'The head of one of the regular indoor messengers for Tellson\'s establishment appeared through the door, and the order was given:'
    },
    "P034_1": {
        "ko": '"짐꾼 필요해!"',
        "en": '"Porter wanted!"'
    },
    "P035_1": {
        "ko": '"만세, 아버지!',
        "en": '"Hooray, father!'
    }
}

for item in data:
    if item['tag'] in patches:
        item['ko'] = patches[item['tag']]['ko']
        item['en'] = patches[item['tag']]['en']

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Patch 1 done")
