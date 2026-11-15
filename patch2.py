import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_04.json', encoding='utf-8') as f:
    d = json.load(f)

fixes = {
  'P020_1': {'ko': '“나도 그렇게 생각하네.”', 'en': '“I believe so.”'},
  'P021_1': {'ko': '“하지만 15년 전은 말할 것도 없고, 50년 전에도 Tellson 상사와 같은 곳이 번창하고 있었다는 데 꽤 큰 돈을 걸 수 있습니다, 선생님.”', 'en': '“But I would hold a pretty wager, sir, that a House like Tellson and Company was flourishing, a matter of fifty, not to speak of fifteen years ago?”'},
  'P022_1': {'ko': '“그의 3배, 아니 150년 전이라고 해도 진실에서 크게 벗어나지 않을 걸세.”', 'en': '“You might treble that, and say a hundred and fifty, yet not be far from the truth.”'},
  'P023_1': {'ko': '“정말입니까, 선생님!”', 'en': '“Indeed, sir!”'},
  'P024_1': {'ko': '종업원은 입을 동그랗게 모으고 두 눈을 크게 뜬 채 식탁에서 뒤로 물러나더니 냅킨을 오른팔에서 왼팔로 옮기고는 편안한 자세로 서서 손님이 먹고 마시는 모습을 마치 전망대나 망루에서 보듯 지켜보았다.', 'en': 'Rounding his mouth and both his eyes, as he stepped backward from the table, the waiter shifted his napkin from his right arm to his left, dropped into a comfortable attitude, and stood surveying the guest while he ate and drank, as from an observatory or watchtower.'},
  'P024_2': {'ko': '모든 시대 종업원들의 태곳적부터의 관습에 따라.', 'en': 'According to the immemorial usage of waiters in all ages.'},
  'P025_1': {'ko': 'Mr.', 'en': 'When Mr.'},
  'P025_2': {'ko': 'Lorry 씨가 아침 식사를 마쳤을 때, 그는 해변을 산책하러 나갔다.', 'en': 'Lorry had finished his breakfast, he went out for a stroll on the beach.'},
  'P025_3': {'ko': '작고 좁고 구불구불한 도버 마을은 해변에서 숨어 백악 절벽 안으로 머리를 들이밀고 있었는데, 마치 바다 타조 같았다.', 'en': 'The little narrow, crooked town of Dover hid itself away from the beach, and ran its head into the chalk cliffs, like a marine ostrich.'},
  'P025_4': {'ko': '해변은 요동치는 바다와 돌무더기의 사막이었고, 바다는 제멋대로 굴었으며 바다가 좋아하는 것은 바로 파괴였다.', 'en': 'The beach was a desert of heaps of sea and stones tumbling wildly about, and the sea did what it liked, and what it liked was destruction.'},
  'P025_5': {'ko': '바다는 마을을 향해 천둥을 쳤고, 절벽을 향해 천둥을 쳤으며, 해안을 미친 듯이 무너뜨렸다.', 'en': 'It thundered at the town, and thundered at the cliffs, and brought the coast down, madly.'},
  'P025_6': {'ko': '집들 사이의 공기에서는 생선 냄새가 어찌나 강하게 나던지, 병든 사람들이 바닷물에 몸을 담그려 내려가듯 병든 물고기들이 몸을 담그려 올라왔을 거라고 생각할 법했다.', 'en': 'The air among the houses was of so strong a piscatory flavour that one might have supposed sick fish went up to be dipped in it, as sick people went down to be dipped in the sea.'},
  'P025_7': {'ko': '항구에서는 약간의 낚시가 이루어졌고, 밤이 되면 바다를 향해 어슬렁거리는 일이 다반사였다:', 'en': 'A little fishing was done in the port, and a quantity of strolling about by night, and looking seaward:'},
  'P025_8': {'ko': '특히 밀물이 밀려와 만조에 가까워졌을 때는 더욱 그랬다.', 'en': 'particularly at those times when the tide made, and was near flood.'},
  'P025_9': {'ko': '아무런 장사도 하지 않는 작은 상인들이 때로는 알 수 없는 이유로 큰 재산을 모으기도 했고, 이웃 사람들이 가로등 켜는 사람을 견디지 못한다는 것은 놀라운 일이었다.', 'en': 'Small tradesmen, who did no business whatever, sometimes unaccountably realised large fortunes, and it was remarkable that nobody in the neighbourhood could endure a lamplighter.'},
  'P026_1': {'ko': '오후가 저물어가고, 이따금씩 프랑스 해안이 보일 정도로 맑았던 공기가 다시 안개와 수증기로 가득 차자, Mr.', 'en': 'As the day declined into the afternoon, and the air, which had been at intervals clear enough to allow the French coast to be seen, became again charged with mist and vapour, Mr.'},
  'P026_2': {'ko': 'Lorry 씨의 생각도 덩달아 흐려지는 듯했다.', 'en': 'Lorry’s thoughts seemed to cloud too.'},
  'P026_3': {'ko': '어두워지자 그는 커피룸 난로 앞에 앉아 아침 식사를 기다렸던 것처럼 저녁 식사를 기다렸는데, 그의 마음은 붉게 타오르는 석탄 속을 바쁘게 파고, 파고, 또 파고 있었다.', 'en': 'When it was dark, and he sat before the coffee-room fire, awaiting his dinner as he had awaited his breakfast, his mind was busily digging, digging, digging, in the live red coals.'},
  'P027_1': {'ko': '저녁 식사 후의 질 좋은 클라레 한 병은 붉은 석탄을 캐는 사람에게 해를 끼치지 않지만, 그를 실직 상태로 몰아넣는 경향이 있다는 점만은 예외이다.', 'en': 'A bottle of good claret after dinner does a digger in the red coals no harm, otherwise than as it has a tendency to throw him out of work.'},
  'P027_2': {'ko': 'Mr.', 'en': 'Mr.'},
  'P027_3': {'ko': 'Lorry 씨는 오랫동안 빈둥거리다가 병을 다 비운 혈색 좋은 노신사에게서나 볼 수 있는 완벽한 만족감을 드러내며 마지막 와인 잔을 막 따랐는데, 그때 좁은 길 위로 바퀴 덜컹거리는 소리가 나더니 여관 마당으로 굴러 들어왔다.', 'en': 'Lorry had been idle a long time, and had just poured out his last glassful of wine with as complete an appearance of satisfaction as is ever to be found in an elderly gentleman of a fresh complexion who has got to the end of a bottle, when a rattling of wheels came up the narrow street, and rumbled into the inn-yard.'},
  'P028_1': {'ko': '그는 손도 대지 않은 잔을 내려놓았다. “아가씨로군!” 그가 말했다.', 'en': 'He set down his glass untouched. “This is Mam’selle!” said he.'},
  'P029_1': {'ko': '불과 몇 분 후 종업원이 들어와 Manette 양이 런던에서 도착했으며 Tellson 은행의 신사분을 뵈면 기뻐할 것이라고 알렸다.', 'en': 'In a very few minutes the waiter came in to announce that Miss Manette had arrived from London, and would be happy to see the gentleman from Tellson’s.'},
  'P030_1': {'ko': '“그렇게 빨리?”', 'en': '“So soon?”'},
  'P031_1': {'ko': 'Manette 양은 길에서 다과를 좀 들었기에 지금은 필요 없으며, 상대의 뜻과 편의에 맞다면 Tellson 은행의 신사분을 즉시 뵙고 싶어 무척 안달이 나 있었다.', 'en': 'Miss Manette had taken some refreshment on the road, and required none then, and was extremely anxious to see the gentleman from Tellson’s immediately, if it suited his pleasure and convenience.'},
  'P032_1': {'ko': 'Tellson 은행의 신사는 무덤덤한 절망의 표정으로 와인 잔을 비우고, 귀 옆의 이상하고 작은 금발 가발을 매만진 뒤 종업원을 따라 Manette 양의 방으로 가는 수밖에 없었다.', 'en': 'The gentleman from Tellson’s had nothing left for it but to empty his glass with an air of stolid desperation, settle his odd little flaxen wig at the ears, and follow the waiter to Miss Manette’s apartment.'},
  'P032_2': {'ko': '그곳은 검은 말총으로 음울하게 장식되어 있고 크고 어두운 테이블들로 꽉 찬, 크고 어두운 방이었다.', 'en': 'It was a large, dark room, furnished in a funereal manner with black horsehair, and loaded with heavy dark tables.'},
  'P032_3': {'ko': '이 테이블들은 어찌나 기름칠을 하고 또 했는지, 방 한가운데 놓인 테이블 위의 길쭉한 두 양초가 나뭇잎 하나하나에 우울하게 반사될 정도였다;', 'en': 'These had been oiled and oiled, until the two tall candles on the table in the middle of the room were gloomily reflected on every leaf;'},
  'P032_4': {'ko': '마치 그 잎사귀들이 검은 마호가니의 깊은 무덤 속에 묻혀 있어서, 파내기 전에는 빛이라고는 기대할 수 없을 것만 같았다.', 'en': 'as if _they_ were buried, in deep graves of black mahogany, and no light to speak of could be expected from them until they were dug out.'},
  'P033_1': {'ko': '방이 어찌나 어두워 꿰뚫어 보기 힘들었던지, Mr.', 'en': 'The obscurity was so difficult to penetrate that Mr.'},
  'P033_2': {'ko': 'Lorry 씨는 닳고 닳은 칠면조 카펫 위를 조심스레 걸으며 Manette 양이 잠시 인접한 방에 있을 거라 생각했지만, 긴 양초 두 개를 지나고 나서야 자신을 맞이하기 위해 테이블과 난로 사이에 서 있는, 승마용 외투를 입고 밀짚 여행용 모자를 리본으로 손에 든 열일곱 살쯤 되어 보이는 젊은 숙녀를 발견했다.', 'en': 'Lorry, picking his way over the well-worn Turkey carpet, supposed Miss Manette to be, for the moment, in some adjacent room, until, having got past the two tall candles, he saw standing to receive him by the table between them and the fire, a young lady of not more than seventeen, in a riding-cloak, and still holding her straw travelling-hat by its ribbon in her hand.'},
  'P033_3': {'ko': '자그마하고 갸냘프며 예쁜 체구, 풍성한 금발, 탐색하는 듯한 표정으로 자신의 눈을 마주치는 파란 눈, 그리고 (그 이마가 얼마나 어리고 매끄러웠는지를 기억하면) 단지 당혹감이나 놀라움, 경계심, 혹은 밝고 고정된 관심 중 어느 하나라고 단정할 수는 없으나 그 네 가지 표정을 모두 포함하여 스스로를 찡그리고 찌푸리는 기묘한 능력을 지닌 이마에 그의 시선이 머물렀을 때--이 모든 것에 그의 시선이 머물렀을 때, 우박이 세차게 내리고 파도가 거칠게 일던 어느 추운 날 바로 그 해협을 건널 때 그의 품에 안겨 있던 한 아이의 생생한 모습이 홀연히 스쳐 지나갔다.', 'en': 'As his eyes rested on a short, slight, pretty figure, a quantity of golden hair, a pair of blue eyes that met his own with an inquiring look, and a forehead with a singular capacity (remembering how young and smooth it was), of rifting and knitting itself into an expression that was not quite one of perplexity, or wonder, or alarm, or merely of a bright fixed attention, though it included all the four expressions--as his eyes rested on these things, a sudden vivid likeness passed before him, of a child whom he had held in his arms on the passage across that very Channel, one cold time, when the hail drifted heavily and the sea ran high.'},
  'P033_4': {'ko': '그 환영은 그녀 뒤에 있는 앙상한 선반 거울의 표면을 스치는 입김처럼 사라졌고, 거울의 틀에는 병원 행렬 같은 흑인 큐피드들이 여럿 목이 잘린 채 모두 절름발이인 모습으로 검은 사해 과일 바구니를 여성 신들에게 바치고 있었다--그리고 그는 Manette 양에게 정중히 절을 했다.', 'en': 'The likeness passed away, like a breath along the surface of the gaunt pier-glass behind her, on the frame of which, a hospital procession of negro cupids, several headless and all cripples, were offering black baskets of Dead Sea fruit to black divinities of the feminine gender--and he made his formal bow to Miss Manette.'},
  'P034_1': {'ko': '“자리에 앉으시죠, 선생님.” 매우 맑고 상냥한 젊은 목소리였고;', 'en': '“Pray take a seat, sir.” In a very clear and pleasant young voice;'},
  'P034_2': {'ko': '약간의 이국적인 억양이 있었지만, 그 정도는 아주 미미했다.', 'en': 'a little foreign in its accent, but a very little indeed.'},
  'P035_1': {'ko': '“손에 키스하겠습니다, 아가씨.” Mr.', 'en': '“I kiss your hand, miss,” said Mr.'},
  'P035_2': {'ko': 'Lorry 씨가 과거의 예의범절을 갖추어 다시 정중하게 인사를 한 뒤 자리에 앉으며 말했다.', 'en': 'Lorry, with the manners of an earlier date, as he made his formal bow again, and took his seat.'},
  'P036_1': {'ko': '“어제 은행으로부터 편지를 받았습니다, 선생님. 어떤 정보--혹은 발견--에 대해서 알려주는 내용이었어요”', 'en': '“I received a letter from the Bank, sir, yesterday, informing me that some intelligence--or discovery--”'},
  'P037_1': {'ko': '“어떤 단어든 중요하지 않습니다, 아가씨.', 'en': '“The word is not material, miss;'},
  'P037_2': {'ko': '둘 다 상관없습니다.”', 'en': 'either word will do.”'},
  'P038_1': {'ko': '“--제가 한 번도 뵌 적 없는 제 불쌍한 아버님, 돌아가신 지 오래된 분의 작은 재산에 관한 내용이었습니다--”', 'en': '“--respecting the small property of my poor father, whom I never saw--so long dead--”'},
  'P039_1': {'ko': 'Mr.', 'en': 'Mr.'},
  'P039_2': {'ko': 'Lorry 씨는 의자를 당겨 앉으며 흑인 큐피드들의 병원 행렬을 향해 근심 어린 시선을 던졌다.', 'en': 'Lorry moved in his chair, and cast a troubled look towards the hospital procession of negro cupids.'},
  'P039_3': {'ko': '그 터무니없는 바구니가 누구에게든 도움이 될 수 있을 것처럼!', 'en': 'As if _they_ had any help for anybody in their absurd baskets!'},
  'P040_1': {'ko': '“--그래서 제가 파리로 가야 한다고 했어요. 그 목적을 위해 파리로 파견되는 친절한 은행 신사분과 연락하기 위해서요.”', 'en': '“--rendered it necessary that I should go to Paris, there to communicate with a gentleman of the Bank, so good as to be despatched to Paris for the purpose.”'},
  'P041_1': {'ko': '“접니다.”', 'en': '“Myself.”'},
  'P042_1': {'ko': '“들을 준비가 되어 있었습니다, 선생님.”', 'en': '“As I was prepared to hear, sir.”'},
  'P043_1': {'ko': '그녀는 그에게 절을 했다 (그 시절 젊은 숙녀들은 그렇게 절을 했다). 자신이 그보다 얼마나 어리고 부족한지 느끼고 있음을 전하고픈 예쁜 마음을 담아서.', 'en': 'She curtseyed to him (young ladies made curtseys in those days), with a pretty desire to convey to him that she felt how much older and wiser he was than she.'},
  'P043_2': {'ko': '그는 그녀에게 다시 인사를 건넸다.', 'en': 'He made her another bow.'},
  'P044_1': {'ko': '“선생님, 은행에 답장을 보냈습니다. 잘 아시고 제게 조언해주시는 고마운 분들이 제가 프랑스로 가야 한다고 하시고, 저는 고아이고 동행할 친구도 없으므로, 여행하는 동안 훌륭한 신사분의 보호를 받게 허락해주신다면 대단히 감사하겠다고요.', 'en': '“I replied to the Bank, sir, that as it was considered necessary, by those who know, and who are so kind as to advise me, that I should go to France, and that as I am an orphan and have no friend who could go with me, I should esteem it highly if I might be permitted to place myself, during the journey, under that worthy gentleman’s protection.'},
  'P044_2': {'ko': '신사분께서 런던을 떠나셨지만, 아마 전령을 보내어 이곳에서 저를 기다려주십사 부탁드렸을 겁니다.”', 'en': 'The gentleman had left London, but I think a messenger was sent after him to beg the favour of his waiting for me here.”'},
  'P045_1': {'ko': '“기쁜 마음으로 기다렸습니다,” Mr.', 'en': '“I was happy,” said Mr.'}
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
