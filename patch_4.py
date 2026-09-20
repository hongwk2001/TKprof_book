import json
import codecs

filepath = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_09.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    'P063_1': {'ko': '"안녕히 주무십시오, 시민 동지," 시드니 카턴이 지나가다 멈춰 서서 말했습니다;', 'en': '"Good night, citizen," said Sydney Carton, pausing in going by;'},
    'P063_2': {'ko': '왜냐하면, 그 남자가 그를 호기심 어린 눈으로 바라보았기 때문이었습니다.', 'en': 'for, the man eyed him inquisitively.'},
    'P064_1': {'ko': '"안녕히 가시오, 시민 동지."', 'en': '"Good night, citizen."'},
    'P065_1': {'ko': '"공화국은 잘 돌아가고 있습니까?"', 'en': '"How goes the Republic?"'},
    'P066_1': {'ko': '"기요틴을 말하는 거군.', 'en': '"You mean the Guillotine.'},
    'P066_2': {'ko': '나쁘지 않소.', 'en': 'Not ill.'},
    'P066_3': {'ko': '오늘은 예순세 명이었소.', 'en': 'Sixty-three to-day.'},
    'P066_4': {'ko': '곧 백 명까지 올라갈 거요.', 'en': 'We shall mount to a hundred soon.'},
    'P066_5': {'ko': '삼손과 그의 부하들은 가끔 기진맥진하다고 불평한다오.', 'en': 'Samson and his men complain sometimes, of being exhausted.'},
    'P066_6': {'ko': '하, 하, 하!', 'en': 'Ha, ha, ha!'},
    'P066_7': {'ko': '그는 참으로 우스꽝스럽소, 그 삼손이란 자는.', 'en': 'He is so droll, that Samson.'},
    'P066_8': {'ko': '대단한 이발사(단두대 사형집행인)지!"', 'en': 'Such a Barber!"'},
    'P067_1': {'ko': '"그를 보러 자주 가십니까--"', 'en': '"Do you often go to see him--"'},
    'P068_1': {'ko': '"면도하는 걸?', 'en': '"Shave?'},
    'P068_2': {'ko': '항상.', 'en': 'Always.'},
    'P068_3': {'ko': '매일 가지.', 'en': 'Every day.'},
    'P068_4': {'ko': '정말 대단한 이발사요!', 'en': 'What a barber!'},
    'P068_5': {'ko': '당신도 그가 일하는 걸 본 적 있소?"', 'en': 'You have seen him at work?"'},
    'P069_1': {'ko': '"결코 없습니다."', 'en': '"Never."'},
    'P070_1': {'ko': '"그가 좋은(많은) 무리를 다룰 때 한 번 보러 가시오.', 'en': '"Go and see him when he has a good batch.'},
    'P070_2': {'ko': '이것 좀 생각해 보시오, 시민 동지;', 'en': 'Figure this to yourself, citizen;'},
    'P070_3': {'ko': '오늘 그는 파이프 담배 두 대를 채 피우기도 전에 예순세 명을 면도(처형)했다오!', 'en': 'he shaved the sixty-three to-day, in less than two pipes!'},
    'P070_4': {'ko': '파이프 두 대도 채 안 걸렸단 말이오.', 'en': 'Less than two pipes.'},
    'P070_5': {'ko': '내 명예를 걸고 사실이오!"', 'en': 'Word of honour!"'},
    'P071_1': {'ko': '히죽거리며 웃는 그 작은 남자가 자기가 어떻게 사형집행인의 시간을 재었는지 설명하기 위해 피우던 파이프를 내밀었을 때, 카턴은 그를 때려죽이고 싶은 충동이 치밀어 오르는 것을 너무도 강하게 느껴서 고개를 돌려버렸습니다.', 'en': 'As the grinning little man held out the pipe he was smoking, to explain how he timed the executioner, Carton was so sensible of a rising desire to strike the life out of him, that he turned away.'},
    'P072_1': {'ko': '"그런데 영국 옷을 입고 있긴 하지만," 톱질꾼이 말했습니다, "당신은 영국인이 아니군?"', 'en': '"But you are not English," said the wood-sawyer, "though you wear English dress?"'},
    'P073_1': {'ko': '"맞습니다," 카턴이 다시 걸음을 멈추고 어깨 너머로 대답했습니다.', 'en': '"Yes," said Carton, pausing again, and answering over his shoulder.'},
    'P074_1': {'ko': '"당신은 프랑스인처럼 말하는군."', 'en': '"You speak like a Frenchman."'},
    'P075_1': {'ko': '"나는 이곳에서 오래 공부한 학생이었습니다."', 'en': '"I am an old student here."'},
    'P076_1': {'ko': '"아하, 완벽한 프랑스인이군!', 'en': '"Aha, a perfect Frenchman!'},
    'P076_2': {'ko': '안녕히 가시오, 영국인."', 'en': 'Good night, Englishman."'},
    'P077_1': {'ko': '"안녕히 주무십시오, 시민 동지."', 'en': '"Good night, citizen."'},
    'P078_1': {'ko': '"하지만 저 우스꽝스러운 개자식을 한 번 보러 가시오," 작은 남자는 그의 등 뒤에 대고 외치며 고집스럽게 덧붙였습니다. "그리고 파이프를 가져가시오!"', 'en': '"But go and see that droll dog," the little man persisted, calling after him. "And take a pipe with you!"'},
    'P079_1': {'ko': '시드니는 시야에서 멀리 사라지기 전에 깜박이는 램프 불빛 아래 길 한가운데 멈춰 서서 종잇조각에 연필로 무언가를 적었습니다.', 'en': 'Sydney had not gone far out of sight, when he stopped in the middle of the street under a glimmering lamp, and wrote with his pencil on a scrap of paper.'},
    'P079_2': {'ko': '그러고는, 그 공포의 시대에는 가장 좋은 공공 도로조차 청소되지 않은 채 남아 있었기 때문에 평소보다 훨씬 더 더러운, 어둡고 더러운 거리 몇 군데를 길을 잘 아는 사람처럼 확고한 걸음으로 가로질러서--주인이 직접 문을 닫고 있는 어느 약국 앞에 멈춰 섰습니다.', 'en': 'Then, traversing with the decided step of one who remembered the way well, several dark and dirty streets--much dirtier than usual, for the best public thoroughfares remained uncleansed in those times of terror--he stopped at a chemist\'s shop, which the owner was closing with his own hands.'},
    'P079_3': {'ko': '작고 희미하고 구부정해 보이는 남자가 구불구불한 오르막길에서 운영하는 작고 어두침침하고 삐딱한 약국이었습니다.', 'en': 'A small, dim, crooked shop, kept in a tortuous, up-hill thoroughfare, by a small, dim, crooked man.'},
    'P080_1': {'ko': '계산대에서 그와 마주치자 이 시민에게도 저녁 인사를 건네며, 그는 그 종잇조각을 그의 앞에 내려놓았습니다. "휴!" 그것을 읽으며 약사는 가볍게 휘파람을 불었습니다. "히! 히! 히!"', 'en': 'Giving this citizen, too, good night, as he confronted him at his counter, he laid the scrap of paper before him. "Whew!" the chemist whistled softly, as he read it. "Hi! hi! hi!"'},
    'P081_1': {'ko': '시드니 카턴이 신경 쓰지 않자, 약사가 말했습니다:', 'en': 'Sydney Carton took no heed, and the chemist said:'},
    'P082_1': {'ko': '"당신을 위한 거요, 시민 동지?"', 'en': '"For you, citizen?"'},
    'P083_1': {'ko': '"나를 위한 거요."', 'en': '"For me."'}
}

for i in range(len(data)):
    t = data[i].get('tag')
    if t in translations:
        data[i]['ko'] = translations[t]['ko']
        data[i]['en'] = translations[t]['en']

with codecs.open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

empty_blocks = [b for b in data if b.get('ko') == '' and not b.get('is_header', False)]
print('Remaining empty:', len(empty_blocks))

import io
for b in empty_blocks[:40]:
    print(b['tag'] + '|' + b['raw'])

