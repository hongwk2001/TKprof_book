import json
import os

queue_path = "c:/git_repo/TKprof_book/work_queue.json"
with open(queue_path, 'r', encoding='utf-8') as f:
    queue = json.load(f)

translations = {
    "210": {"ko": "그것은 간수의 손에 닫혔다;", "en": "it closed under the gaoler’s hand;"},
    "211": {"ko": "그리고 그 환영들은 그의 시야에서 영원히 사라졌다.", "en": "and the apparitions vanished from his sight forever."},
    "212": {"ko": "그 작은 문은 위로 이어지는 돌계단으로 열렸다.", "en": "The wicket opened on a stone staircase, leading upward."},
    "213": {"ko": "그들이 마흔 계단을 올라갔을 때 (이미 30분 동안 죄수는 그것들을 세고 있었다), 간수는 낮고 검은 문을 열었고, 그들은 독방으로 들어갔다.", "en": "When they had ascended forty steps (the prisoner of half an hour already counted them), the gaoler opened a low black door, and they passed into a solitary cell."},
    "214": {"ko": "그곳은 차갑고 축축했지만 어둡지는 않았다.", "en": "It struck cold and damp, but was not dark."},
    "215": {"ko": "“당신의 방이오.” 간수가 말했다.", "en": "“Yours,” said the gaoler."},
    "216": {"ko": "“왜 나 혼자 갇히는 거요?”", "en": "“Why am I confined alone?”"},
    "217": {"ko": "“내가 어떻게 알겠소!”", "en": "“How do I know!”"},
    "218": {"ko": "“펜, 잉크, 종이를 살 수 있소?”", "en": "“I can buy pen, ink, and paper?”"},
    "219": {"ko": "“내게 그런 명령은 없었소.", "en": "“Such are not my orders."},
    "220": {"ko": "당신에게 방문객이 올 테니 그때 물어보시오.", "en": "You will be visited, and can ask then."},
    "221": {"ko": "현재로서는 음식을 살 수 있을 뿐, 그 이상은 안 되오.”", "en": "At present, you may buy your food, and nothing more.”"},
    "222": {"ko": "독방 안에는 의자, 탁자, 짚 매트리스가 있었다.", "en": "There were in the cell, a chair, a table, and a straw mattress."},
    "223": {"ko": "간수가 나가기 전에 이 물건들과 네 벽을 전반적으로 검사할 때, 반대편 벽에 기대어 있던 죄수의 마음속에는 이 간수가 얼굴과 몸이 너무 병적으로 부어 있어서 마치 물에 빠져 물로 가득 찬 사람처럼 보인다는 몽상적인 생각이 스쳐 지나갔다.", "en": "As the gaoler made a general inspection of these objects, and of the four walls, before going out, a wandering fancy wandered through the mind of the prisoner leaning against the wall opposite to him, that this gaoler was so unwholesomely bloated, both in face and person, as to look like a man who had been drowned and filled with water."},
    "224": {"ko": "간수가 떠나자, 그는 같은 몽상적인 방식으로 생각했다. “이제 나는 죽은 사람처럼 남겨졌구나.” 그런 다음 매트리스를 내려다보려고 멈춰 선 그는 역겨움을 느끼며 고개를 돌렸고, 생각했다. “그리고 여기 기어다니는 이 생물들 속에 죽음 이후 몸의 첫 번째 상태가 있구나.”", "en": "When the gaoler was gone, he thought in the same wandering way, “Now am I left, as if I were dead.” Stopping then, to look down at the mattress, he turned from it with a sick feeling, and thought, “And here in these crawling creatures is the first condition of the body after death.”"},
    "225": {"ko": "“다섯 걸음에 네 걸음 반, 다섯 걸음에 네 걸음 반, 다섯 걸음에 네 걸음 반.” 죄수는 치수를 세며 독방 안을 이리저리 걸었고, 도시의 굉음은 둔탁한 북소리처럼 울렸으며 거기에 거친 목소리의 웅성거림이 더해졌다. “그는 신발을 만들었다, 그는 신발을 만들었다, 그는 신발을 만들었다.” 죄수는 다시 치수를 세며 그 마지막 반복으로부터 자신의 마음을 이끌어내기 위해 더 빨리 걸었다. “작은 문이 닫힐 때 사라진 유령들.", "en": "“Five paces by four and a half, five paces by four and a half, five paces by four and a half.” The prisoner walked to and fro in his cell, counting its measurement, and the roar of the city arose like muffled drums with a wild swell of voices added to them. “He made shoes, he made shoes, he made shoes.” The prisoner counted the measurement again, and paced faster, to draw his mind with him from that latter repetition. “The ghosts that vanished when the wicket closed."},
    "226": {"ko": "그들 가운데 검은 옷을 입은 한 부인의 환영이 있었는데, 그녀는 창틀에 기대어 있었고, 금발 머리에는 빛이 비치고 있었으며, 그녀는 마치 * * * * 제발 다시 달려가자, 모든 사람들이 깨어 있는 불 밝혀진 마을을 지나! * * * * 그는 신발을 만들었다, 그는 신발을 만들었다, 그는 신발을 만들었다. * * * * 다섯 걸음에 네 걸음 반.” 마음속 깊은 곳에서 이런 조각들이 위로 솟아올라 뒹구는 가운데, 죄수는 고집스럽게 세고 또 세며 점점 더 빨리 걸었다;", "en": "There was one among them, the appearance of a lady dressed in black, who was leaning in the embrasure of a window, and she had a light shining upon her golden hair, and she looked like * * * * Let us ride on again, for God’s sake, through the illuminated villages with the people all awake! * * * * He made shoes, he made shoes, he made shoes. * * * * Five paces by four and a half.” With such scraps tossing and rolling upward from the depths of his mind, the prisoner walked faster and faster, obstinately counting and counting;"},
    "227": {"ko": "그리고 도시의 굉음은 이런 정도로 변했다--여전히 둔탁한 북소리처럼 굴러 들어오긴 했지만, 그 위로 솟아오르는 웅성거림 속에 그가 아는 목소리의 울부짖음이 섞여 있었다.", "en": "and the roar of the city changed to this extent--that it still rolled in like muffled drums, but with the wail of voices that he knew, in the swell that rose above them."},
    "3": {"ko": "바구니를 든 Mr. Cruncher가 그녀의 곁에서 걸었다.", "en": "Mr. Cruncher, with the basket, walked at her side."},
    "11": {"ko": "Miss Pross는 Mr. Cruncher의 의중을 떠보고 그가 자신과 같은 의견임을 알고는, 자신의 기사를 대동하고 고대의 훌륭한 공화주의자 브루투스에게 의지했다.", "en": "Sounding Mr. Cruncher, and finding him of her opinion, Miss Pross resorted to the Good Republican Brutus of Antiquity, attended by her cavalier."},
    "28": {"ko": "왜냐하면, Miss Pross가 놀라움과 동요에 빠졌을 뿐만 아니라, Mr. Cruncher 또한--비록 그 자신의 별개적이고 개인적인 이유인 듯했지만--가장 큰 경이로움의 상태에 있었다는 것이 기록되어야 하기 때문이다.", "en": "For, it must be recorded, that not only was Miss Pross lost in amazement and agitation, but, Mr. Cruncher--though it seemed on his own separate and individual account--was in a state of the greatest wonder."},
    "38": {"ko": "Miss Pross는 결코 다정하지 않은 오빠를 향해 애정 어리고 낙담한 고개를 저으며 눈물을 흘리며 말했다. “Mr. Cruncher.”", "en": "Miss Pross, shaking her loving and dejected head at her by no means affectionate brother, said through her tears, “Mr. Cruncher.”"},
    "40": {"ko": "겉보기로 판단하건대, 분명히 Mr. Cruncher는 그러했다.", "en": "Apparently, Mr. Cruncher did, to judge from his looks."},
    "65": {"ko": "마치 Mr. Lorry가 몇 년 전 소호의 조용한 구석에서 이 귀중한 오빠가 그녀의 돈을 다 써버리고 그녀를 떠났다는 사실을 몰랐던 것처럼!", "en": "As if Mr. Lorry had not known it for a fact, years ago, in the quiet corner in Soho, that this precious brother had spent her money and left her!"},
    "66": {"ko": "그러나 그들의 상대적인 가치와 위치가 뒤바뀌었다면 (전 세계 어디서나 항상 그렇듯이) 그가 보일 수 있었던 것보다 훨씬 더 마지못한 겸손과 시혜적인 태도로 애정 어린 말을 하고 있었을 때, Mr. Cruncher가 그의 어깨를 두드리며 쉰 목소리로 뜻밖에 다음과 같은 기묘한 질문을 던지며 끼어들었다.", "en": "He was saying the affectionate word, however, with a far more grudging condescension and patronage than he could have shown if their relative merits and positions had been reversed (which is invariably the case, all the world over), when Mr. Cruncher, touching him on the shoulder, hoarsely and unexpectedly interposed with the following singular question:"},
    "72": {"ko": "“이보시오!” Mr. Cruncher가 말했다. “솔직히 말해보쇼, 알잖소.” (그런데 이것은 그가 할 수 있는 그 이상의 것이었다.) “John Solomon이오, 아니면 Solomon John이오?", "en": "“Come!” said Mr. Cruncher. “Speak out, you know.” (Which, by the way, was more than he could do himself.) “John Solomon, or Solomon John?"},
    "92": {"ko": "그는 승마 코트 자락 아래에 두 손을 뒤로 감추고, 마치 올드 베일리 자체에 서 있는 것처럼 무심하게 Mr. Cruncher의 팔꿈치 곁에 서 있었다.", "en": "He had his hands behind him under the skirts of his riding-coat, and he stood at Mr. Cruncher’s elbow as negligently as he might have stood at the Old Bailey itself."},
    "94": {"ko": "어제저녁에 Mr. Lorry의 집에 도착했소, 그가 놀랍게도;", "en": "I arrived at Mr. Lorry’s, to his surprise, yesterday evening;"},
    "97": {"ko": "당신에게 Mr. Barsad보다 더 나은 직업을 가진 오빠가 있었더라면 좋았을 텐데요.", "en": "I wish you had a better employed brother than Mr. Barsad."},
    "98": {"ko": "당신을 위해서라도 Mr. Barsad가 감옥의 양(밀정)이 아니기를 바랐소.”", "en": "I wish for your sake Mr. Barsad was not a Sheep of the Prisons.”"},
    "101": {"ko": "“내가 말해주지,” Sydney가 말했다. “한 시간쯤 전에 내가 벽을 응시하고 있는 동안 콩시에르주리 감옥에서 나오는 당신과 마주쳤지, Mr. Barsad.", "en": "“I’ll tell you,” said Sydney. “I lighted on you, Mr. Barsad, coming out of the prison of the Conciergerie while I was contemplating the walls, an hour or more ago."},
    "106": {"ko": "그러다 점차, 내가 무작위로 했던 행동이 어떤 목적을 띠게 되는 것 같더군, Mr. Barsad.”", "en": "And gradually, what I had done at random, seemed to shape itself into a purpose, Mr. Barsad.”"},
    "130": {"ko": "그리고 당신의 호위병이 Mr. Barsad를 알고 있으니, 내가 그를 Mr. Lorry에게 초대하겠소.", "en": "and as your escort knows Mr. Barsad, I will invite him to Mr."},
    "136": {"ko": "그들은 길모퉁이에서 그녀와 헤어졌고, Carton은 걸어서 몇 분 거리에 있는 Mr. Lorry의 집으로 길을 안내했다.", "en": "They left her at the corner of the street, and Carton led the way to Mr. Lorry’s, which was within a few minutes’ walk."},
    "138": {"ko": "Mr. Lorry는 방금 저녁 식사를 마치고 유쾌한 작은 장작 불꽃 두 개 앞에 앉아 있었다--아마도 그 불길 속에서 수년 전 도버의 로열 조지 호텔에서 붉은 석탄을 들여다보던 텔슨 은행의 그 젊었던 노신사의 모습을 찾고 있었을지도 모른다.", "en": "Mr. Lorry had just finished his dinner, and was sitting before a cheery little log or two of fire--perhaps looking into their blaze for the picture of that younger elderly gentleman from Tellson’s, who had looked into the red coals at the Royal George at Dover, now a good many years ago."},
    "140": {"ko": "“Miss Pross의 오빠입니다, 선생님,” Sydney가 말했다. “Mr. Barsad입니다.”", "en": "“Miss Pross’s brother, sir,” said Sydney. “Mr. Barsad.”"},
    "143": {"ko": "“내가 당신 얼굴이 인상 깊다고 했지, Mr. Barsad,” Carton이 차분하게 관찰하듯 말했다. “부디 앉으시오.”", "en": "“I told you you had a remarkable face, Mr. Barsad,” observed Carton, coolly. “Pray sit down.”"},
    "144": {"ko": "스스로 의자에 앉으며, 그는 찡그린 얼굴로 Mr. Lorry에게 말함으로써 그가 필요로 하던 연결 고리를 제공했다. “그 재판의 증인입니다.” Mr. Lorry는", "en": "As he took a chair himself, he supplied the link that Mr. Lorry wanted, by saying to him with a frown, “Witness at that trial.” Mr."},
    "146": {"ko": "“Mr. Barsad는 선생님이 들으셨던 그 애정 어린 오빠로 Miss Pross에게 방금 인지되었습니다,” Sydney가 말했다, “그리고 그 관계를 인정했고요.", "en": "“Mr. Barsad has been recognised by Miss Pross as the affectionate brother you have heard of,” said Sydney, “and has acknowledged the relationship."},
    "152": {"ko": "그 일이 언제 행해졌소, Mr. Barsad?”", "en": "When was it done, Mr. Barsad?”"},
    "154": {"ko": "“Mr. Barsad는 가능한 최고의 권위자입니다, 선생님,” Sydney가 말했다. “그리고 저는 그것을 Mr. Barsad에게서 직접 들었습니다.", "en": "“Mr. Barsad is the best authority possible, sir,” said Sydney, “and I have it from Mr."},
    "158": {"ko": "Mr. Lorry의 업무용 눈빛은 말하는 이의 얼굴을 읽고 그 점에 대해 더 이야기하는 것은 시간 낭비라는 것을 알았다.", "en": "Mr. Lorry’s business eye read in the speaker’s face that it was loss of time to dwell upon the point."},
    "160": {"ko": "“이제 나는 믿습니다,” Sydney가 그에게 말했다, “Doctor Manette의 이름과 영향력이 내일 그에게 똑같이 좋은 역할을 할 수 있으리라고--당신이 내일 그가 재판소에 다시 서게 될 거라고 말했지, Mr. Barsad?--”", "en": "“Now, I trust,” said Sydney to him, “that the name and influence of Doctor Manette may stand him in as good stead to-morrow--you said he would be before the Tribunal again to-morrow, Mr. Barsad?--”"},
    "165": {"ko": "선생님께 고백하건대, 저는 Doctor Manette가 이 체포를 막을 힘이 없었다는 것에 충격을 받았습니다, Mr. Lorry.”", "en": "I own to you, I am shaken, Mr. Lorry, by Doctor Manette’s not having had the power to prevent this arrest.”"},
    "166": {"ko": "“그는 사전에 그것을 몰랐을 수도 있네,” Mr. Lorry가 말했다.", "en": "“He may not have known of it beforehand,” said Mr. Lorry."},
    "168": {"ko": "“그것은 사실이오,” Mr. Lorry는 불안한 손을 턱에 대고, 불안한 눈으로 Carton을 바라보며 인정했다.", "en": "“That’s true,” Mr. Lorry acknowledged, with his troubled hand at his chin, and his troubled eyes on Carton."},
    "175": {"ko": "그리고 내가 내 편으로 만들고자 하는 친구는, 바로 Mr. Barsad입니다.”", "en": "And the friend I purpose to myself to win, is Mr. Barsad.”"},
    "178": {"ko": "내가 어떤 패를 쥐고 있는지 보겠소,--Mr. Lorry, 내가 얼마나 짐승 같은 놈인지 아실 텐데요;", "en": "I’ll see what I hold,--Mr. Lorry, you know what a brute I am;"},
    "181": {"ko": "“Mr. Barsad,” 그가 마치 카드의 패를 내려다보는 사람의 어조로 계속했다:", "en": "“Mr. Barsad,” he went on, in the tone of one who really was looking over a hand at cards:"},
    "184": {"ko": "지금은 공화국 프랑스 정부의 고용인이지만, 전에는 귀족주의적인 영국 정부, 즉 프랑스와 자유의 적의 고용인이었던 Mr. Barsad.", "en": "Mr. Barsad, now in the employ of the republican French government, was formerly in the employ of the aristocratic English government, the enemy of France and freedom."},
    "186": {"ko": "이러한 의심의 지역에서, 여전히 귀족주의 영국 정부의 급여를 받고 있는 Mr. Barsad가 피트의 스파이이자 공화국의 품에 웅크리고 있는 배신자적인 적이며, 그토록 많이 거론되고 찾아내기 어려운 모든 해악의 영국 반역자이자 요원이라는 추론은 대낮처럼 분명하지.", "en": "Inference clear as day in this region of suspicion, that Mr. Barsad, still in the pay of the aristocratic English government, is the spy of Pitt, the treacherous foe of the Republic crouching in its bosom, the English traitor and agent of all mischief so much spoken of and so difficult to find."},
    "188": {"ko": "내 패를 따라왔소, Mr. Barsad?”", "en": "Have you followed my hand, Mr. Barsad?”"},
    "190": {"ko": "“내 에이스 카드를 내지, 가장 가까운 구역 위원회에 Mr. Barsad를 고발하는 것.", "en": "“I play my Ace, Denunciation of Mr. Barsad to the nearest Section Committee."},
    "191": {"ko": "당신의 패를 살펴보시오, Mr. Barsad, 그리고 무엇을 가졌는지 보시오.", "en": "Look over your hand, Mr. Barsad, and see what you have."},
    "196": {"ko": "“당신의 패를 주의 깊게 살펴보시오, Mr. Barsad.", "en": "“Look over your hand carefully, Mr. Barsad."},
    "199": {"ko": "Mr. Barsad는 그 속에서 Sydney Carton이 전혀 알지 못하는 지는 패들을 보았다.", "en": "Mr. Barsad saw losing cards in it that Sydney Carton knew nothing of."},
    "216": {"ko": "“선생님,” 밀정은 가장 비열한 태도로 Mr. Lorry에게 몸을 돌리며 말했다, “선생님의 연륜과 자비로움에 호소하건대, 선생님보다 훨씬 연하인 이 분에게, 그 어떤 상황에서도 그가 말한 그 에이스 카드를 내는 것이 자신의 지위에 어울리는 일인지 물어봐 주실 수 있는지요.", "en": "“I think, sir,” said the spy, in the meanest manner, as he turned to Mr. Lorry, “I may appeal to a gentleman of your years and benevolence, to put it to this other gentleman, so much your junior, whether he can under any circumstances reconcile it to his station to play that Ace of which he has spoken."},
    "219": {"ko": "“내 에이스 카드를 내겠소, Mr. Barsad,” Carton이 대답을 스스로 떠맡으며 시계를 바라보고 말했다, “아무런 거리낌 없이, 단 몇 분 안에.”", "en": "“I play my Ace, Mr. Barsad,” said Carton, taking the answer on himself, and looking at his watch, “without any scruple, in a very few minutes.”"},
    "220": {"ko": "“두 분 신사분들께서,” 밀정이 항상 Mr. Lorry를 논의에 끌어들이려고 애쓰며 말했다, “내 여동생에 대한 존중으로--”", "en": "“I should have hoped, gentlemen both,” said the spy, always striving to hook Mr. Lorry into the discussion, “that your respect for my sister--”"},
    "255": {"ko": "여기서 Mr. Lorry는 앉아 있던 자리에서 벽에 비친 가장 기이한 고블린 같은 그림자를 알아차렸다.", "en": "Here, Mr. Lorry became aware, from where he sat, of a most remarkable goblin shadow on the wall."},
    "256": {"ko": "그 근원을 추적해 보니, 그것은 Mr. Cruncher의 머리에 있는 뻣뻣한 머리카락 전체가 갑작스럽고 기이하게 솟아오르며 뻣뻣해진 데서 기인한다는 것을 발견했다.", "en": "Tracing it to its source, he discovered it to be caused by a sudden extraordinary rising and stiffening of all the risen and stiff hair on Mr. Cruncher’s head."},
    "263": {"ko": "여기서, Mr. Lorry는 벽에 비친 그림자가 길어지는 것을 알아차렸다, 그리고 Mr. Cruncher가", "en": "Here, Mr. Lorry perceived the reflection on the wall to elongate, and Mr."},
    "266": {"ko": "밀정이 보지 못한 사이, Mr. Cruncher는 그의 곁에 서서 마치 유령 집행관처럼 그의 어깨를 두드렸다.", "en": "Unseen by the spy, Mr. Cruncher stood at his side, and touched him on the shoulder like a ghostly bailiff."},
    "267": {"ko": "“그 Roger Cly 말입니다, 나리,” 무뚝뚝하고 굳은 표정의 Mr. Cruncher가 말했다. “당신이 그를 관에 넣었소?”", "en": "“That there Roger Cly, master,” said Mr. Cruncher, with a taciturn and iron-bound visage. “So _you_ put him in his coffin?”"},
    "271": {"ko": "“내 말은,” Mr. Cruncher가 말했다, “그는 한 번도 거기에 들어간 적이 없다는 거요.", "en": "“I mean,” said Mr. Cruncher, “that he warn’t never in it."},
    "283": {"ko": "이런!” Mr. Cruncher가 으르렁거렸다, “내가 오래된 원한을 품고 있는 게 바로 당신이었군, 상인들에 대한 그 부끄러운 사기 행각으로 말이오!", "en": "Ecod!” growled Mr. Cruncher, “it’s you I have got a old grudge again, is it, with your shameful impositions upon tradesmen!"},
    "285": {"ko": "이 사건의 반전에 Mr. Lorry와 함께 놀라움에 빠져 있던 Sydney Carton이 여기서 Mr. Cruncher에게 요청했다.", "en": "Sydney Carton, who, with Mr. Lorry, had been lost in amazement at this turn of the business, here requested Mr."},
    "289": {"ko": "그가 단 한 음절이라도 그렇다고 말하게 해보시오, 그러면 반 기니에 그의 목구멍을 잡고 숨을 막아버릴 테니;” Mr. Cruncher는 이것을 꽤 관대한 제안인 듯 강조했다;", "en": "Let him say he was, in so much as a word of one syllable, and I’ll either catch hold of his throat and choke him for half a guinea;” Mr. Cruncher dwelt upon this as quite a liberal offer;"},
    "292": {"ko": "한 가지는 알겠군,” Carton이 말했다. “내가 다른 카드를 쥐고 있소, Mr. Barsad.", "en": "I see one thing,” said Carton. “I hold another card, Mr. Barsad."},
    "300": {"ko": "“이 사람에 대해서는 신경 쓰지 마시오,” 논쟁을 좋아하는 Mr. Cruncher가 쏘아붙였다;", "en": "“Never you trouble your head about this man,” retorted the contentious Mr. Cruncher;"},
    "303": {"ko": "한 번만 더!”--Mr. Cruncher는 자신의 관대함을 꽤 과시적으로 뽐내는 것을 억제할 수 없었다--“반 기니에 당신의 목구멍을 잡고 숨을 막아버릴 테니.”", "en": "Once more!”--Mr. Cruncher could not be restrained from making rather an ostentatious parade of his liberality--“I’d catch hold of your throat and choke you for half a guinea.”"},
    "2": {"ko": "Sydney Carton과 감옥의 양이 소리가 새어나가지 않도록 낮은 목소리로 인접한 어두운 방에서 대화하는 동안, Mr. Lorry는 상당한 의심과 불신으로 Jerry를 바라보았다.", "en": "While Sydney Carton and the Sheep of the prisons were in the adjoining dark room, speaking so low that not a sound was heard, Mr. Lorry looked at Jerry in considerable doubt and mistrust."},
    "6": {"ko": "그리고 Mr. Lorry의 시선이 그와 마주칠 때마다, 그는 손을 오목하게 모아 입을 가리고 짧은 기침을 하는 특이한 발작을 일으켰는데, 이는 완벽히 솔직한 성격에 수반되는 병으로는 거의 알려진 바 없는 것이었다.", "en": "and whenever Mr. Lorry’s eye caught his, he was taken with that peculiar kind of short cough requiring the hollow of a hand before it, which is seldom, if ever, known to be an infirmity attendant on perfect openness of character."},
    "8": {"ko": "Mr. Cruncher는 한쪽 어깨를 앞으로 내민 채 비스듬히 다가왔다.", "en": "Mr. Cruncher came forward sideways, with one of his shoulders in advance of him."},
    "10": {"ko": "잠시 생각에 잠긴 후 후원자를 유심히 바라보며, Mr. Cruncher는 대답할 기발한 생각을 떠올렸다. “농업적인 성격입니다.”", "en": "After some cogitation, accompanied with an intent look at his patron, Mr. Cruncher conceived the luminous idea of replying, “Agicultooral character.”"},
    "11": {"ko": "“내 마음이 몹시 불안하네,” Mr. Lorry가 그를 향해 집게손가락을 화가 난 듯 흔들며 말했다, “자네가 텔슨의 훌륭하고 위대한 은행을 눈가림으로 이용했고, 불명예스러운 묘사의 불법적인 직업을 가졌다는 것이.", "en": "“My mind misgives me much,” said Mr. Lorry, angrily shaking a forefinger at him, “that you have used the respectable and great house of Tellson’s as a blind, and that you have had an unlawful occupation of an infamous description."},
    "15": {"ko": "“바라옵건대, 나리,” 당황한 Mr. Cruncher가 애원했다, “제가 머리가 희어지도록 허드렛일을 해 모신 나리 같은 신사분이라면, 설령 그렇다 하더라도 저를 해치는 일에 대해 두 번은 생각해주실 겁니다--그렇다는 건 아니지만, 설령 그렇다 하더라도요.", "en": "“I hope, sir,” pleaded the abashed Mr. Cruncher, “that a gentleman like yourself wot I’ve had the honour of odd jobbing till I’m grey at it, would think twice about harming of me, even if it wos so--I don’t say it is, but even if it wos."},
    "21": {"ko": "그리고 여기 Mrs. Cruncher가 있습니다, 아니 적어도 옛 잉글랜드 시절엔 있었죠, 그리고 명분만 주어진다면 내일이라도 그 사업에 반대하며 풀썩 주저앉아 완전히 망쳐놓을 겁니다--완전히 망쳐놓을 거예요!", "en": "And here’s Mrs. Cruncher, or leastways wos in the Old England times, and would be to-morrow, if cause given, a floppin’ again the business to that degree as is ruinating--stark ruinating!"},
    "25": {"ko": "게다가 사람이 조금 얻은 것으로는 절대 번창할 수 없을 겁니다, Mr. Lorry.", "en": "And wot little a man did get, would never prosper with him, Mr. Lorry."},
    "28": {"ko": "“으휴!” Mr. Lorry가 다소 누그러지면서도 외쳤다, “자네 꼴을 보니 충격적이군.”", "en": "“Ugh!” cried Mr. Lorry, rather relenting, nevertheless, “I am shocked at the sight of you.”"},
    "29": {"ko": "“자, 나리께 겸손히 제안하고 싶은 것은,” Mr. Cruncher가 계속했다, “설령 그렇다 하더라도, 그렇다는 건 아니지만요--”", "en": "“Now, what I would humbly offer to you, sir,” pursued Mr. Cruncher, “even if it wos so, which I don’t say it is--”"},
    "30": {"ko": "“얼버무리지 마,” Mr. Lorry가 말했다.", "en": "“Don’t prevaricate,” said Mr. Lorry."},
    "31": {"ko": "“아닙니다, 그러지 _않겠습니다_, 나리,” Mr. Crunches는 그런 것이 자신의 생각이나 관행과는 전혀 거리가 멀다는 듯 대답했다--“그렇다는 건 아니지만요--나리께 겸손히 제안하고 싶은 것은 이렇습니다.", "en": "“No, I will _not_, sir,” returned Mr. Crunches as if nothing were further from his thoughts or practice--“which I don’t say it is--wot I would humbly offer to you, sir, would be this."},
    "35": {"ko": "그렇습니다, Mr. Lorry,” Mr. Cruncher가 말했다.", "en": "That, Mr. Lorry,” said Mr."},
    "39": {"ko": "“적어도 그것은 사실이군,” Mr. Lorry가 말했다. “지금은 더 말하지 말게.", "en": "“That at least is true,” said Mr. Lorry. “Say no more now."},
    "42": {"ko": "Sydney Carton과 밀정이 어두운 방에서 돌아오자, Mr. Cruncher는 이마를 짚으며 인사했다. “안녕히, Mr. Lorry.”", "en": "Mr. Cruncher knuckled his forehead, as Sydney Carton and the spy returned from the dark room. “Adieu, Mr."},
    "45": {"ko": "그는 Mr. Lorry 맞은편 난로가에 있는 의자에 앉았다.", "en": "He sat down in a chair on the hearth, over against Mr. Lorry."},
    "46": {"ko": "그들이 단둘이 되자, Mr. Lorry는 그에게 무슨 짓을 했는지 물었다.", "en": "When they were alone, Mr. Lorry asked him what he had done?"},
    "49": {"ko": "Mr. Lorry의 얼굴빛이 어두워졌다.", "en": "Mr. Lorry’s countenance fell."},
    "53": {"ko": "“하지만 그에게 접근하는 것만으로는,” Mr. Lorry가 말했다, “재판에서 일이 안 좋게 흘러간다면 그를 구할 수 없을 텐데.”", "en": "“But access to him,” said Mr. Lorry, “if it should go ill before the Tribunal, will not save him.”"},
    "55": {"ko": "Mr. Lorry의 시선이 천천히 불길을 향했다;", "en": "Mr. Lorry’s eyes gradually sought the fire;"},
    "62": {"ko": "비록 그가 마지막 말은 평소 태도로 돌아가 내뱉었지만, 그의 말투와 손길에는 Mr. Lorry가 그에게서 한 번도 본 적 없는, 진실한 감정과 존중이 배어 있었기에, 전혀 준비되지 않은 상태였다.", "en": "Though he said the last words, with a slip into his usual manner, there was a true feeling and respect both in his tone and in his touch, that Mr. Lorry, who had never seen the better side of him, was wholly unprepared for."},
    "67": {"ko": "Mr. Lorry는 그것에 대해 생각하지 못했기에, 그것이 그의 마음속에 있는지 보려고 재빨리 Carton을 바라보았다.", "en": "Mr. Lorry had not thought of that, and he looked quickly at Carton to see if it were in his mind."},
    "83": {"ko": "그것이 불길을 향해 돌려진 Carton의 얼굴로 Mr. Lorry의 시선을 끌었다.", "en": "It attracted Mr. Lorry’s eyes to Carton’s face, which was turned to the fire."},
    "86": {"ko": "불에 대한 그의 무관심은 Mr. Lorry로부터 훈계의 말을 이끌어낼 만큼 충분히 눈에 띄었다;", "en": "His indifference to fire was sufficiently remarkable to elicit a word of remonstrance from Mr. Lorry;"},
    "89": {"ko": "Mr. Lorry의 눈이 다시 그의 얼굴로 이끌렸다.", "en": "Mr. Lorry’s eyes were again attracted to his face."},
    "107": {"ko": "“외로운 늙은 독신자지,” 고개를 저으며 Mr. Lorry가 대답했다. “나를 위해 울어줄 사람은 아무도 없다네.”", "en": "“A solitary old bachelor,” answered Mr. Lorry, shaking his head. “There is nobody to weep for me.”"},
    "120": {"ko": "“정말 옳은 말이네, Mr. Carton;", "en": "“You say truly, Mr. Carton;"},
    "125": {"ko": "부드러워진 그의 태도에 응하며, Mr. Lorry가 대답했다:", "en": "Responding to his softened manner, Mr. Lorry answered:"},
    "134": {"ko": "“하지만 자네는,” 주제를 되돌리며 Mr. Lorry가 말했다, “자네는 젊지 않은가.”", "en": "“But you,” said Mr. Lorry, reverting to the theme, “you are young.”"}
}

import collections
file_updates = collections.defaultdict(dict)

# update batch items
for i in range(301, 401):
    item = queue[i]
    tid = str(item['id'])
    if tid in translations:
        item['ko'] = translations[tid]['ko']
        item['en'] = translations[tid]['en']
        item['status'] = 'done'
        
        file_updates[item['file']][item['id']] = {
            'ko': translations[tid]['ko'],
            'en': translations[tid]['en']
        }

# write work_queue.json
with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2, ensure_ascii=False)

# patch individual files
base_dir = "c:/git_repo/TKprof_book/books/two_cities/json"
for filename, changes in file_updates.items():
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        file_data = json.load(f)
    
    for block in file_data:
        bid = str(block['id'])
        if bid in translations:
            block['ko'] = translations[bid]['ko']
            block['en'] = translations[bid]['en']
            
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(file_data, f, indent=2, ensure_ascii=False)

print("Patching complete!")
