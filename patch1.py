import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_04.json', encoding='utf-8') as f:
    d = json.load(f)

fixes = {
  'P010_6': {'ko': '그의 셔츠는 양말만큼 고운 재질은 아니었지만, 인근 해변에 부서지는 파도의 꼭대기나 먼 바다 햇살에 반짝이는 돛의 작은 조각만큼이나 하얬다.', 'en': 'His linen, though not of a fineness in accordance with his stockings, was as white as the tops of the waves that broke upon the neighbouring beach, or the specks of sail that glinted in the sunlight far at sea.'},
  'P010_7': {'ko': '습관적으로 억눌려 있고 차분한 얼굴은 그 기묘한 가발 아래에서, 과거 어느 시절 주인이 Tellson 은행의 침착하고 내성적인 표정에 맞게 길들이느라 꽤나 애먹었을 법한 촉촉하게 빛나는 두 눈 덕분에 여전히 환했다.', 'en': 'A face habitually suppressed and quieted, was still lighted up under the quaint wig by a pair of moist bright eyes that it must have cost their owner, in years gone by, some pains to drill to the composed and reserved expression of Tellson’s Bank.'},
  'P010_8': {'ko': '그의 양 볼은 건강한 혈색을 띠었고, 얼굴은 비록 주름지긴 했으나 불안한 기색은 거의 보이지 않았다.', 'en': 'He had a healthy colour in his cheeks, and his face, though lined, bore few traces of anxiety.'},
  'P010_9': {'ko': '하지만 아마도 Tellson 은행의 은밀한 독신 사무원들은 주로 남의 걱정거리들에 얽매여 있었고;', 'en': 'But, perhaps the confidential bachelor clerks in Tellson’s Bank were principally occupied with the cares of other people;'},
  'P010_10': {'ko': '어쩌면 중고 의류처럼 중고 걱정거리도 쉽게 입고 벗을 수 있는 모양이었다.', 'en': 'and perhaps second-hand cares, like second-hand clothes, come easily off and on.'},
  'P011_1': {'ko': '초상화 모델로 앉아 있는 사람과 완벽하게 닮아간, Mr.', 'en': 'Completing his resemblance to a man who was sitting for his portrait, Mr.'},
  'P011_2': {'ko': 'Lorry 씨는 잠에 빠져들었다.', 'en': 'Lorry dropped off to sleep.'},
  'P011_3': {'ko': '아침 식사가 도착하자 그는 잠에서 깨어났고, 의자를 끌어당기며 종업원에게 말했다:', 'en': 'The arrival of his breakfast roused him, and he said to the drawer, as he moved his chair to it:'},
  'P012_1': {'ko': '“오늘 언제든 이곳에 올 수 있는 젊은 숙녀분을 위해 숙소를 준비해 주었으면 하네.', 'en': '“I wish accommodation prepared for a young lady who may come here at any time to-day.'},
  'P012_2': {'ko': '그녀는 Mr. 를 찾을지도 모른다네.', 'en': 'She may ask for Mr.'},
  'P012_3': {'ko': 'Jarvis Lorry, 혹은 텔슨 은행에서 온 신사를 찾을지도 모르지.', 'en': 'Jarvis Lorry, or she may only ask for a gentleman from Tellson’s Bank.'},
  'P012_4': {'ko': '그러면 내게 알려주게.”', 'en': 'Please to let me know.”'},
  'P013_1': {'ko': '“네, 선생님.', 'en': '“Yes, sir.'},
  'P013_2': {'ko': '런던의 Tellson 은행 말씀이신가요, 선생님?”', 'en': 'Tellson’s Bank in London, sir?”'},
  'P014_1': {'ko': '“그렇다네.”', 'en': '“Yes.”'},
  'P015_1': {'ko': '“네, 선생님.', 'en': '“Yes, sir.'},
  'P015_2': {'ko': '저희는 런던과 파리를 오가시는 신사분들을 종종 모실 영광을 누리고 있습니다, 선생님.', 'en': 'We have oftentimes the honour to entertain your gentlemen in their travelling backwards and forwards betwixt London and Paris, sir.'},
  'P015_3': {'ko': 'Tellson 상사에서는 여행을 엄청나게 많이 하시지요, 선생님.”', 'en': 'A vast deal of travelling, sir, in Tellson and Company’s House.”'},
  'P016_1': {'ko': '“그렇지.', 'en': '“Yes.'},
  'P016_2': {'ko': '우리는 영국 상사이자 완전히 프랑스 상사이기도 하니까.”', 'en': 'We are quite a French House, as well as an English one.”'},
  'P017_1': {'ko': '“네, 선생님.', 'en': '“Yes, sir.'},
  'P017_2': {'ko': '선생님 본인께서는 그런 여행을 별로 하지 않으시는 것 같은데요?”', 'en': 'Not much in the habit of such travelling yourself, I think, sir?”'},
  'P018_1': {'ko': '“최근 몇 년간은 하지 않았지.', 'en': '“Not of late years.'},
  'P018_2': {'ko': '우리가--내가--마지막으로 프랑스에서 온 지 15년이 되었네.”', 'en': 'It is fifteen years since we--since I--came last from France.”'},
  'P019_1': {'ko': '“정말입니까, 선생님?', 'en': '“Indeed, sir?'},
  'P019_2': {'ko': '제가 이곳에 오기 전의 일이로군요, 선생님.', 'en': 'That was before my time here, sir.'},
  'P019_3': {'ko': '저희 직원들이 오기 전의 일입니다, 선생님.', 'en': 'Before our people’s time here, sir.'},
  'P019_4': {'ko': '그 당시 조지 여관은 다른 사람 손에 있었습니다, 선생님.”', 'en': 'The George was in other hands at that time, sir.”'}
}

count = 0
for b in d:
    if b['tag'] in fixes:
        b['ko'] = fixes[b['tag']]['ko']
        b['en'] = fixes[b['tag']]['en']
        count += 1

with open('c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_04.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Patched {count} blocks.")
