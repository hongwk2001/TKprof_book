import json

updates = {
  'P108_3': {'ko': '“Lucie.”', 'en': '“Lucie.”'},
  'P108_4': {'ko': '“그의 딸이군.”', 'en': '“His daughter.”'},
  'P108_5': {'ko': '“프랑스인이고.”', 'en': '“French.”'},
  'P108_6': {'ko': '“어느 사람인가?”', 'en': '“Which one is she?”'},
  'P109': {'ko': '이 사람입니다.', 'en': 'This is she.'},
  'P110_2': {'ko': '“Lucie, Evrémonde의 아내지, 안 그런가?”', 'en': '“Lucie, the wife of Evrémonde; is it not?”'},
  'P111': {'ko': '“그렇습니다.”', 'en': '“It is.”'},
  'P112_2': {'ko': '“Evrémonde는 다른 곳에 약속이 있군.”', 'en': '“Evrémonde has an appointment elsewhere.”'},
  'P112_3': {'ko': '“Lucie, 그녀의 아이.”', 'en': '“Lucie, her child.”'},
  'P112_4': {'ko': '“영국인이고.”', 'en': '“English.”'},
  'P112_5': {'ko': '“이 아이인가?”', 'en': '“This is she?”'},
  'P113': {'ko': '바로 이 아이입니다.', 'en': 'She and no other.'},
  'P114_2': {'ko': '“자, 네가 훌륭한 공화국민에게 입을 맞추었으니, 너희 가문에 새로운 일이 일어난 셈이구나. 이를 기억해라!”', 'en': '“Now, you have kissed a good Republican; something new in your family; remember it!”'},
  'P114_3': {'ko': '“Sydney Carton.”', 'en': '“Sydney Carton.”'},
  'P114_4': {'ko': '“변호사.”', 'en': '“Advocate.”'},
  'P114_5': {'ko': '“영국인.”', 'en': '“English.”'},
  'P114_6': {'ko': '“어느 사람인가?”', 'en': '“Which one is he?”'},
  'P116': {'ko': '“영국인 변호사는 기절해 있는 것 같군?”', 'en': '“Apparently the English advocate has fainted?”'},
  'P117_2': {'ko': '“그의 건강이 좋지 않고, 공화국의 미움을 산 친구와 슬프게 헤어진 상황이라 그렇습니다.”', 'en': '“It is explained that he is not in strong health, and has had a sad separation from a friend who has fallen out of favor with the Republic.”'},
  'P118_3': {'ko': '“많은 이들이 공화국의 미움을 받아 작은 창밖을 내다보아야만(단두대의 칼날 아래 목을 내밀어야만) 하지.”', 'en': '“Many have fallen out of favor with the Republic, and must look out through the little window (of the guillotine).”'},
  'P118_4': {'ko': '“Jarvis Lorry.”', 'en': '“Jarvis Lorry.”'},
  'P118_5': {'ko': '“은행가.”', 'en': '“Banker.”'},
  'P118_6': {'ko': '“영국인.”', 'en': '“English.”'},
  'P118_7': {'ko': '“어느 사람인가?”', 'en': '“Which one is he?”'},
  'P120_3': {'ko': '그들은 여유롭게 마차 주변을 걷다가 지붕에 실린 적은 짐을 확인하려 느긋하게 마차 앞자리로 올라간다. 주위를 서성이던 시골 사람들은 마차 문으로 더 가까이 다가와 탐욕스럽게 안을 들여다본다. 어머니에게 안긴 어린아이는 단두대로 간 귀족의 아내를 만져보려는 듯 짧은 팔을 뻗고 있다.', 'en': 'They leisurely walk around the carriage and leisurely climb up to the box to inspect the little luggage carried on the roof. The country-people hanging around press nearer to the coach doors and stare greedily inside. A small child, carried by its mother, has its short arm held out so that it may touch the wife of an aristocrat who has gone to the Guillotine.'},
  'P121': {'ko': '“서명된 서류들을 받으시오, Jarvis Lorry.”', 'en': '“Here are your papers, Jarvis Lorry, countersigned.”'},
  'P122': {'ko': '“출발해도 되겠습니까, 시민이여?”', 'en': '“May we depart, citizen?”'},
  'P123_2': {'ko': '“출발하라, 마부들이여!”', 'en': '“Forward, my postilions!”'},
  'P123_3': {'ko': '“좋은 여행 되시오!”', 'en': '“Have a good journey!”'},
  'P124': {'ko': '“인사드립니다, 시민 여러분. ――그리고 첫 번째 위험은 무사히 넘겼구나!”', 'en': '“I salute you, citizens.—And the first danger has passed!”'},
  'P125_2': {'ko': '마차 안에는 공포가 서려 있고, 울음소리가 들리며, 의식을 잃은 여행자의 거친 숨소리가 이어지고 있다.', 'en': 'There is terror in the carriage, there is weeping, and there is the heavy breathing of the unconscious traveler.'},
  'P128': {'ko': '“뒤를, 뒤를 돌아보시오, 우리가 쫓기고 있는지 확인해 주시오!”', 'en': '“Look back, look back, and see if we are being pursued!”'},
  'P129_2': {'ko': '“지금까지는 아무도 우리를 쫓아오지 않습니다.”', 'en': '“So far, we are not being pursued.”'},
  'P130_3': {'ko': '때로는 달그락거리며 우리를 흔드는 돌들을 피하기 위해 가장자리의 진흙 속으로 뛰어들기도 하고, 때로는 그곳의 바퀴 자국이나 진창에 빠지기도 한다.', 'en': 'Sometimes, we swerve into the mud on the edge to avoid the stones that clatter and shake us; sometimes, we get stuck in the ruts and sloughs there.'},
  'P130_4': {'ko': '그럴 때면 조바심이 주는 고통이 너무도 커서, 미친 듯한 불안과 다급함 속에서 우리는 당장 밖으로 나가 달리고 숨고, 멈추는 것만 빼고 무슨 일이든 하려고 든다.', 'en': 'The agony of our impatience then becomes so great that in our wild alarm and rush we feel like getting out and running—hiding—doing anything but stopping.'},
  'P131_6': {'ko': '뒤를, 뒤를 돌아보아라, 우리가 쫓기고 있는지 확인해 다오!', 'en': 'Look back, look back, and see if we are being pursued!'},
  'P131_7': {'ko': '쉿! 역참이다.', 'en': 'Hush! It is the posting-house.'},
  'P136': {'ko': '“그들이 몇 명이라고 했습니까?”', 'en': '“How many did they say?”'},
  'P137': {'ko': '“무슨 말씀인지 모르겠습니다.”', 'en': '“I do not understand you.”'},
  'P138_2': {'ko': '“오늘 단두대로 가는 자들이 몇 명이냐고 물었소.”', 'en': '“How many are going to the Guillotine today?”'},
  'P139': {'ko': '“쉰두 명입니다.”', 'en': '“Fifty-two.”'},
  'P140_2': {'ko': '“대단한 숫자군!”', 'en': '“A brave number!”'},
  'P140_3': {'ko': '“여기 내 동료 시민은 마흔두 명일 거라고 했지만, 열 개의 머리가 더 추가되니 좋군.”', 'en': '“My fellow-citizen here thought it was forty-two; ten more heads are certainly worth having.”'},
  'P140_4': {'ko': '“단두대가 아주 훌륭하게 돌아가고 있어.”', 'en': '“The Guillotine is working handsomely.”'},
  'P140_5': {'ko': '“정말 마음에 들어.”', 'en': '“I love it.”'},
  'P140_6': {'ko': '“자, 앞으로 가자.”', 'en': '“Hi, forward.”'},
  'P140_7': {'ko': '“이랴!”', 'en': '“Whoop!”'},
  'P142': {'ko': '바람이 우리 뒤를 쫓아 몰아치고, 구름이 우리 뒤를 쫓아 날아가며, 달이 우리 뒤를 쫓아 쏟아지듯 따라오고, 이 거친 밤 전체가 우리를 추격하고 있다. 그러나 지금까지는 그 외에 다른 어떤 것도 우리를 뒤쫓고 있지 않다.', 'en': 'The wind is rushing after us, the clouds are flying after us, the moon is plunging after us, and the entire wild night is in pursuit of us; but, so far, we are pursued by nothing else.'},
  # Group 5 from earlier:
  'P101': {'ko': '감옥에 드리우는 것과 같은 그림자가, 이른 오후의 같은 시간에, 파리를 빠져나가는 마차 한 대가 검문을 받기 위해 멈춰 서는, 사람들이 모여 있는 관문에도 드리우고 있다.', 'en': 'The same shadows falling on the prison are falling, in that same hour of the early afternoon, on the Barrier surrounded by a crowd, as a coach heading out of Paris drives up to be examined.'},
  'P102_2': {'ko': '“안에는 누가 타고 있는가?”', 'en': '“Who do we have inside?”'},
  'P102_3': {'ko': '“서류!”', 'en': '“Papers!”'},
  'P103': {'ko': '서류들이 건네졌고, 읽힌다.', 'en': 'The papers are handed out and read.'},
  'P104_2': {'ko': '“의사라.”', 'en': '“Physician.”'},
  'P104_3': {'ko': '“프랑스인이고.”', 'en': '“French.”'},
  'P104_4': {'ko': '“어느 사람인가?”', 'en': '“Which one is he?”'},
  'P105': {'ko': '이 사람이 그입니다; 지적받은 이는 무기력하게 뜻 모를 소리를 중얼거리는, 정신이 오락가락하는 노인이다.', 'en': 'This is he; this helpless, inarticulately murmuring, wandering old man is pointed out.'},
  'P107': {'ko': '그에게는 너무나 벅찬 일입니다.', 'en': 'It is greatly too much for him.'},
  'P108_2': {'ko': '“많은 이들이 그것으로 고통받고 있지.”', 'en': '“Many suffer with it.”'}
}

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_13.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for block in data:
    tag = block.get('tag')
    if tag in updates:
        block['ko'] = updates[tag]['ko']
        block['en'] = updates[tag]['en']

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open('c:/git_repo/TKprof_book/books/two_cities/json/empty_blocks.json', 'r', encoding='utf-8') as f:
    empty_blocks = json.load(f)

remaining = [b for b in empty_blocks if b['tag'] not in updates]

with open('c:/git_repo/TKprof_book/books/two_cities/json/empty_blocks.json', 'w', encoding='utf-8') as f:
    json.dump(remaining, f, ensure_ascii=False, indent=2)

print(f"Remaining blocks: {len(remaining)}")
