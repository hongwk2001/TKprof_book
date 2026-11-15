import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_04.json', encoding='utf-8') as f:
    d = json.load(f)

fixes = {
  'P089_5': {'ko': '어느 쪽인지 알아보려 하는 것은 이제 무용지물보다 더 나쁜 일이 될 겁니다;', 'en': 'It would be worse than useless now to inquire which;'},
  'P089_6': {'ko': '그가 수년간 방치되어 있었는지, 아니면 항상 고의로 감금되어 있었는지 알아내려 하는 것도 무용지물보다 더 나쁜 일입니다.', 'en': 'worse than useless to seek to know whether he has been for years overlooked, or always designedly held prisoner.'},
  'P089_7': {'ko': '지금 어떤 조사를 하는 것은 무용지물보다 더 나쁠 겁니다. 위험할 테니까요.', 'en': 'It would be worse than useless now to make any inquiries, because it would be dangerous.'},
  'P089_8': {'ko': '어디서든 어떤 식으로든 이 문제를 언급하지 않는 편이 좋고, 어쨌든 당분간은--그분을 프랑스 밖으로 빼내는 편이 좋습니다.', 'en': 'Better not to mention the subject, anywhere or in any way, and to remove him--for a while at all events--out of France.'},
  'P089_9': {'ko': '영국인이라 안전한 저조차도, 그리고 프랑스 신용거래에서 중요한 Tellson 상사조차도, 이 문제에 대한 모든 언급을 피하고 있습니다.', 'en': 'Even I, safe as an Englishman, and even Tellson’s, important as they are to French credit, avoid all naming of the matter.'},
  'P089_10': {'ko': '저는 이 문제에 대해 공개적으로 언급하는 어떤 글귀도 지니고 다니지 않습니다.', 'en': 'I carry about me, not a scrap of writing openly referring to it.'},
  'P089_11': {'ko': '이것은 전적으로 비밀 임무입니다.', 'en': 'This is a secret service altogether.'},
  'P089_12': {'ko': '저의 신임장, 기록, 메모는 모두 ‘삶으로 소환됨’이라는 단 한 줄에 포함되어 있는데, 이건 뭐든 의미할 수 있지요.', 'en': 'My credentials, entries, and memoranda, are all comprehended in the one line, ‘Recalled to Life;’ which may mean anything.'},
  'P089_13': {'ko': '아니 무슨 일입니까!', 'en': 'But what is the matter!'},
  'P089_14': {'ko': '한 마디도 듣지 못하고 계시지 않습니까!', 'en': 'She doesn’t notice a word!'},
  'P089_15': {'ko': 'Manette 양!”', 'en': 'Miss Manette!”'},
  'P090_1': {'ko': '그녀는 의자 뒤로 쓰러지지도 않은 채 그의 손 아래에서 완전히 의식을 잃고 쥐 죽은 듯 조용히 앉아 있었다;', 'en': 'Perfectly still and silent, and not even fallen back in her chair, she sat under his hand, utterly insensible;'},
  'P090_2': {'ko': '두 눈은 뜬 채 그에게 고정되어 있었고, 그 마지막 표정은 마치 이마에 조각되거나 낙인찍힌 것처럼 보였다.', 'en': 'with her eyes open and fixed upon him, and with that last expression looking as if it were carved or branded into her forehead.'},
  'P090_3': {'ko': '그녀가 그의 팔을 어찌나 꽉 쥐고 있던지, 그는 혹여 그녀가 다칠까 봐 몸을 떼어낼 엄두를 내지 못했다;', 'en': 'So close was her hold upon his arm, that he feared to detach himself lest he should hurt her;'},
  'P090_4': {'ko': '그래서 그는 움직이지 않은 채 큰 소리로 도움을 청했다.', 'en': 'therefore he called out loudly for assistance without moving.'},
  'P091_1': {'ko': '당황한 와중에도 Mr.', 'en': 'A wild-looking woman, whom even in his agitation, Mr.'},
  'P091_2': {'ko': 'Lorry 씨의 눈에 온통 붉은색을 띠고 붉은 머리를 가졌으며 기묘하게 꽉 끼는 옷차림에 머리에는 척탄병의 나무통 같은, 그것도 꽤나 큰 스틸턴 치즈나 큼지막한 통 같은 기막힌 보닛을 쓴 야성적으로 보이는 여자가 여관 종업원들보다 앞서 방으로 뛰어 들어왔다. 그녀는 건장한 손을 그의 가슴에 얹고는 그를 가장 가까운 벽으로 날려 보내어, 가엾은 젊은 숙녀에게서 그를 떼어내는 문제를 단숨에 해결해버렸다.', 'en': 'Lorry observed to be all of a red colour, and to have red hair, and to be dressed in some extraordinary tight-fitting fashion, and to have on her head a most wonderful bonnet like a Grenadier wooden measure, and good measure too, or a great Stilton cheese, came running into the room in advance of the inn servants, and soon settled the question of his detachment from the poor young lady, by laying a brawny hand upon his chest, and sending him flying back against the nearest wall.'},
  'P092_1': {'ko': '(‘이 사람은 정말 남자임에 틀림없어!’ 벽에 부딪힘과 동시에 Mr.', 'en': '(“I really think this must be a man!” was Mr.'},
  'P092_2': {'ko': 'Lorry 씨가 숨 가쁘게 한 생각이었다.)', 'en': 'Lorry’s breathless reflection, simultaneously with his coming against the wall.)'},
  'P093_1': {'ko': '“아니, 다들 꼴 좀 봐!” 이 인물이 여관 종업원들을 향해 소리쳤다. “거기 서서 나만 빤히 쳐다보고 있지 말고 가서 물건들이나 좀 가져오지 그래?', 'en': '“Why, look at you all!” bawled this figure, addressing the inn servants. “Why don’t you go and fetch things, instead of standing there staring at me?'},
  'P093_2': {'ko': '내가 그렇게 볼 만하게 생기지는 않았잖아, 안 그래?', 'en': 'I am not so much to look at, am I?'},
  'P093_3': {'ko': '왜 가서 물건들을 가져오지 않는 거야?', 'en': 'Why don’t you go and fetch things?'},
  'P093_4': {'ko': '향정신성 소금이랑 찬물, 식초 당장 가져오지 않으면 가만 안 둘 테야.”', 'en': 'I’ll let you know, if you don’t bring smelling-salts, cold water, and vinegar, quick, I will.”'},
  'P094_1': {'ko': '이 회복제들을 찾으러 사람들이 즉시 흩어졌고, 그녀는 부드럽게 환자를 소파에 눕히고 훌륭한 솜씨와 다정함으로 그녀를 돌보았다:', 'en': 'There was an immediate dispersal for these restoratives, and she softly laid the patient on a sofa, and tended her with great skill and gentleness:'},
  'P094_2': {'ko': '“내 보물!” “내 새끼!”라고 부르며 엄청난 자부심과 정성을 담아 금발 머리를 어깨 너머로 펴주었다.', 'en': 'calling her “my precious!” and “my bird!” and spreading her golden hair aside over her shoulders with great pride and care.'},
  'P095_1': {'ko': '“그리고 거기 갈색 옷 입은 당신!” 그녀는 격분하여 Mr.', 'en': '“And you in brown!” she said, indignantly turning to Mr.'},
  'P095_2': {'ko': 'Lorry 씨를 돌아보며 말했다;', 'en': 'Lorry;'},
  'P095_3': {'ko': '“당신은 이 아가씨를 기절초풍하게 만들지 않고서는 할 말을 할 수 없었던 거야?', 'en': '“couldn’t you tell her what you had to tell her, without frightening her to death?'},
  'P095_4': {'ko': '이 아가씨 좀 봐, 창백하고 예쁜 얼굴에 손은 또 얼마나 찬지.', 'en': 'Look at her, with her pretty pale face and her cold hands.'},
  'P095_5': {'ko': '당신은 _그게_ 은행가가 할 짓이라고 생각해?”', 'en': 'Do you call _that_ being a Banker?”'},
  'P096_1': {'ko': 'Mr.', 'en': 'Mr.'},
  'P096_2': {'ko': 'Lorry 씨는 대답하기 몹시 어려운 질문을 받고 너무 당황한 나머지 그저 멀찍이 서서 훨씬 약해진 연민과 겸손함으로 지켜볼 수밖에 없었다. 그 사이 이 힘센 여자는, 여관 종업원들이 그곳에 머물며 빤히 쳐다본다면 언급되지 않은 뭔가를 ‘맛보게 해주겠다’는 알 수 없는 협박으로 그들을 내쫓은 뒤, 점진적으로 자신의 피보호자를 회복시키며 처진 고개를 어깨에 기대도록 달래고 있었다.', 'en': 'Lorry was so exceedingly disconcerted by a question so hard to answer, that he could only look on, at a distance, with much feebler sympathy and humility, while the strong woman, having banished the inn servants under the mysterious penalty of ‘letting them know’ something not mentioned if they stayed there, staring, recovered her charge by a regular series of gradations, and coaxed her to lay her drooping head upon her shoulder.'},
  'P097_1': {'ko': '“이제 좀 괜찮아지기를 바랍니다만,” Mr.', 'en': '“I hope she will do well now,” said Mr.'},
  'P097_2': {'ko': 'Lorry 씨가 말했다.', 'en': 'Lorry.'},
  'P098_1': {'ko': '“괜찮아지더라도 거기 갈색 옷 입은 당신 덕은 아니야.', 'en': '“No thanks to you in brown, if she does.'},
  'P098_2': {'ko': '내 예쁜 아가씨!”', 'en': 'My darling pretty!”'},
  'P099_1': {'ko': '“바라건대,” Mr.', 'en': '“I hope,” said Mr.'},
  'P099_2': {'ko': 'Lorry 씨는 미약한 연민과 겸손함이 섞인 침묵 끝에, “Manette 양과 프랑스에 동행하시는 건가요?”', 'en': 'Lorry, after another pause of feeble sympathy and humility, “that you accompany Miss Manette to France?”'},
  'P100_1': {'ko': '“그럴 리가!” 힘센 여자가 대답했다. “내가 짠물을 건너갈 운명이었다면, 신께서 나를 섬에 태어나게 하셨겠어?”', 'en': '“A likely thing, too!” replied the strong woman. “If it was ever intended that I should go across salt water, do you suppose Providence would have cast my lot in an island?”'},
  'P101_1': {'ko': '이 또한 대답하기 어려운 질문이었기에, Mr.', 'en': 'This being another question hard to answer, Mr.'},
  'P101_2': {'ko': 'Jarvis Lorry 씨는 생각해 보려 물러났다.', 'en': 'Jarvis Lorry withdrew to consider it.'}
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
