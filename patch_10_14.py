import json

translations = {
    "book3_ch_14.json__batch0010": [
        {"ko": "그렇게 무장하고, 어린 시절 습관처럼 갈색 바닷모래 위를 맨발과 맨다리로 걸었던 여인의 유연한 자유로움과 그러한 성격에 걸맞은 당당한 발걸음으로 걷는 Madame Defarge는 거리를 따라 나아갔다.", "en": "Armed in this way, and walking with the confident step fitting her character, as well as the flexible freedom of a woman who used to walk barefoot and bare-legged on brown sea-sand in her youth, Madame Defarge made her way along the streets."},
        {"ko": "한편, 바로 그 순간 승객들이 모두 타기를 기다리고 있던 여행용 마차의 어젯밤 일정 계획에서, Miss Pross를 그 마차에 태우는 문제의 어려움이 Mr.", "en": "Now, when the schedule for the traveling coach—which at that very moment was waiting to finish loading—was planned out last night, the difficulty of including Miss Pross had taken up much of Mr."},
        {"ko": "Lorry의 주의를 많이 끌었었다.", "en": "Lorry's attention."},
        {"ko": "마차에 사람을 너무 많이 태우는 것을 피하는 것이 바람직할 뿐만 아니라, 마차와 승객들을 검문하는 데 걸리는 시간을 최대한 줄이는 것이 무엇보다 중요했다;", "en": "It was not only a good idea to avoid overloading the coach, but it was also extremely important that the time spent examining the coach and its passengers be cut down as much as possible;"},
        {"ko": "왜냐하면 그들의 탈출은 곳곳에서 불과 몇 초를 절약하는 것에 달려 있을 수도 있기 때문이었다.", "en": "because their escape might depend on saving just a few seconds here and there."},
        {"ko": "결국, 고심 끝에 그는 도시를 떠날 자유가 있는 Miss Pross와 Jerry가 그 시대에 알려진 가장 바퀴가 가벼운 탈것을 타고 3시에 떠나야 한다고 제안했었다.", "en": "Finally, after careful thought, he had suggested that Miss Pross and Jerry, who were free to leave the city, should leave at three o'clock in the lightest-wheeled vehicle available at the time."},
        {"ko": "짐이 없으므로 그들은 곧 마차를 따라잡아 길에서 마차를 앞지른 뒤, 미리 마차용 말들을 주문해둠으로써 지체가 가장 두려운 소중한 밤 시간 동안 마차의 진행을 크게 수월하게 할 것이었다.", "en": "Without luggage to weigh them down, they would soon catch up to the coach, pass it on the road, order fresh horses in advance, and make its travel much smoother during the critical night hours when any delay was most dangerous."},
        {"ko": "이러한 계획에서 그 긴급한 위기 상황에 실질적인 도움을 줄 수 있다는 희망을 본 Miss Pross는 기쁨으로 그것을 환영했었다.", "en": "Seeing that this plan offered a chance to provide real help in such a pressing emergency, Miss Pross welcomed it with joy."},
        {"ko": "그녀와 Jerry는 마차가 출발하는 것을 지켜보았고, Solomon이 데려온 사람이 누구인지 알았으며, 극심한 긴장감 속에서 약 10분의 고문 같은 시간을 보낸 뒤, 이제 마차를 따라갈 준비를 마무리하고 있었다. 바로 그 순간, 거리를 지나오던 Madame Defarge가 그들이 상의를 나누고 있는, 지금은 텅 빈 숙소를 향해 점점 더 가까이 다가오고 있었다.", "en": "She and Jerry had watched the coach leave, recognized who Solomon had brought, endured about ten minutes of agonizing suspense, and were now finishing their plans to follow the coach—just as Madame Defarge, making her way through the streets, drew closer and closer to the otherwise empty lodging where they were holding their discussion."}
    ],
    "book3_ch_14.json__batch0011": [
        {"ko": "“자, 어떻게 생각해요, Mr.", "en": "“Now, what do you think, Mr."},
        {"ko": "Cruncher,” 흥분이 너무 심해서 말하기도, 서 있기도, 움직이기도, 숨 쉬고 살기도 힘들 지경인 Miss Pross가 말했다:", "en": "Cruncher,” said Miss Pross, who was so worked up that she could barely speak, stand, move, or even live:"},
        {"ko": "“우리가 이 안뜰에서 출발하지 않는 건 어떨까요?", "en": "“what do you think about us not leaving from this courtyard?”"},
        {"ko": "오늘 이미 마차가 한 대 나갔으니, 의심을 살 수도 있잖아요.”", "en": "“Since another carriage has already left from here today, it might cause suspicion.”"},
        {"ko": "“제 생각에도 아가씨,” Mr.가 대답했다.", "en": "“In my opinion, miss,” replied Mr."},
        {"ko": "Cruncher, “아가씨 말이 맞습니다.", "en": "Cruncher, “you are right.”"},
        {"ko": "또한 맞든 틀리든 전 아가씨 편에 설 겁니다.”", "en": "“And I will stand by you, whether you are right or wrong.”"},
        {"ko": "“우리 소중한 분들에 대한 두려움과 희망으로 정신이 너무 산만해져서,” Miss Pross가 미친 듯이 울부짖으며 말했다. “어떤 계획도 세울 수가 없어요.", "en": "“I am so torn apart by fear and hope for our precious ones,” said Miss Pross, crying wildly, “that I cannot form any plan at all.”"},
        {"ko": "당신은 어떤 계획이라도 세울 수 있나요, 친애하는 훌륭한 Mr.", "en": "“Are *you* able to form any plan, my dear, good Mr."},
        {"ko": "Cruncher?”", "en": "Cruncher?”"}
    ],
    "book3_ch_14.json__batch0012": [
        {"ko": "“미래의 삶의 영역에 관해서라면, 아가씨,” Mr.가 대답했다.", "en": "“As for my future sphere of life, miss,” replied Mr."},
        {"ko": "Cruncher, “저도 그러길 바랍니다.", "en": "Cruncher, “I hope so.”"},
        {"ko": "하지만 지금 이 축복받은 늙은 머리를 당장 써먹는 것에 관해서라면, 안 될 것 같군요.", "en": "“But as for any immediate use of this blessed old head of mine, I don't think so.”"},
        {"ko": "아가씨, 이 위기 상황에서 제가 기록으로 남기고 싶은 두 가지 약속과 맹세(wows는 vows의 오기)에 주목해 주시는 호의를 베풀어 주시겠습니까?”", "en": "“Would you do me a favor, miss, and listen to two promises and vows that I wish to record in this time of crisis?”"},
        {"ko": "“아, 제발요!” 여전히 미친 듯이 울면서 Miss Pross가 외쳤다. “훌륭한 분답게 지금 당장 기록해 버리고, 빨리 해치워 버리세요.”", "en": "“Oh, for goodness' sake!” cried Miss Pross, still weeping wildly, “record them right now and get them over with, like a good man.”"},
        {"ko": "“첫째,” Mr.가 말했다.", "en": "“First,” said Mr."},
        {"ko": "온몸을 떨며 잿빛의 엄숙한 얼굴로 말하는 Cruncher, “저 가엾은 분들이 여기서 무사히 빠져나가기만 한다면, 두 번 다시 그 짓(무덤 도굴을 의미함)을 하지 않겠습니다. 절대 다시는요!”", "en": "Cruncher, who was trembling all over and speaking with a pale, serious face, “if those poor people get safely out of this, I will never do it again, never again!”"},
        {"ko": "“저는 확신해요, Mr.", "en": "“I am quite sure, Mr."},
        {"ko": "Cruncher,” Miss Pross가 대답했다. “그게 무엇이든 간에 당신이 다시는 안 하실 거라는 걸요. 그러니 그게 정확히 뭔지 구체적으로 말할 필요는 없다고 생각해 주시길 부탁드려요.”", "en": "Cruncher,” replied Miss Pross, “that you will never do it again, whatever it is, and I beg you not to feel the need to explain exactly what it is.”"},
        {"ko": "“아닙니다, 아가씨,” Jerry가 대답했다. “아가씨께는 그 이름을 입에 올리지 않겠습니다.", "en": "“No, miss,” replied Jerry, “I will not name it to you.”"}
    ],
    "book3_ch_14.json__batch0013": [
        {"ko": "둘째:", "en": "“Second:”"},
        {"ko": "저 가엾은 분들이 무사히 빠져나가기만 한다면, 다시는 우리 마누라, Mrs.", "en": "“if those poor people get safely out of this, I will never again interfere with Mrs."},
        {"ko": "Cruncher의 엎드려 기도하는 짓(flopping)을 방해하지 않겠습니다. 절대 다시는요!”", "en": "Cruncher’s flopping [praying], never again!”"},
        {"ko": "“그게 어떤 집안일이든 간에,” 눈물을 닦고 마음을 진정시키려 애쓰며 Miss Pross가 말했다. “Mrs.", "en": "“Whatever housekeeping routine that may be,” said Miss Pross, trying to dry her eyes and calm herself, “I have no doubt it is best left entirely under Mrs."},
        {"ko": "Cruncher가 전적으로 관리하게 두는 게 최선일 거라 믿어 의심치 않아요.--아, 내 불쌍한 사랑하는 사람들!”", "en": "Cruncher's control.--Oh, my poor darlings!”"},
        {"ko": "“게다가 아가씨, 제가 감히 이런 말씀까지 드리겠습니다.” 계속해서 이어가는 Mr.", "en": "“I will even go so far as to say, miss,” continued Mr."},
        {"ko": "마치 설교단에서 연설하는 듯한 심히 우려스러운 경향을 보이며 Cruncher가 말했다-- “제 말을 적어두셨다가 아가씨를 통해 Mrs.", "en": "Cruncher, showing a very worrying tendency to preach as if from a pulpit—“and let my words be taken down and passed on to Mrs."},
        {"ko": "Cruncher에게 전해 주십시오--기도(flopping)에 대한 제 의견이 변했으며, 지금 제가 진심으로 바라는 건 오직 Mrs.", "en": "Cruncher through you—that my views on flopping have changed, and that what I hope for with all my heart is that Mrs."},
        {"ko": "Cruncher가 지금 이 순간에도 기도를 하고 있었으면 한다는 것뿐이라고요.”", "en": "Cruncher might be flopping at this very moment.”"},
        {"ko": "“그래요, 그래, 알겠어요!", "en": "“There, there, there!”"}
    ],
    "book3_ch_14.json__batch0014": [
        {"ko": "친애하는 당신, 그녀가 그러고 있길 바라요.” 반쯤 넋이 나간 Miss Pross가 외쳤다. “그리고 그게 그녀의 기대에 부응하길 바라요.”", "en": "“I hope she is, my dear man,” cried the frantic Miss Pross, “and I hope it meets her expectations.”"},
        {"ko": "“제발 그러지 않기를,” 계속해서 이어가는 Mr.", "en": "“Heaven forbid,” continued Mr."},
        {"ko": "Cruncher, 그는 더 엄숙해지고 더 느릿느릿해지며, 장황하게 연설하며 고집을 부리는 경향이 더해진 채 말했다. “제가 지금껏 한 말이나 행동이 저 가엾은 분들을 위한 제 간절한 소망에 벌로 되돌아오는 일(wisited = visited)만은 없기를!", "en": "Cruncher, with even more seriousness, more slowness, and an even greater tendency to preach and drag things out, “that anything I have ever said or done should bring bad luck upon my earnest wishes for those poor creatures now!”"},
        {"ko": "이 우울한 위험에서 그들을 빼낼 수만 있다면, 우리 모두가 엎드려 기도하지 못할 이유가(조금이라도 형편이 허락한다면) 없기를!", "en": "“Heaven forbid that we shouldn’t all flop (if it was at all convenient) to get them out of this dreadful danger!”"},
        {"ko": "제발 그러지 않기를, 아가씨!", "en": "“Heaven forbid, miss!”"},
        {"ko": "제 말은, 제발 그러지 _않기를!_” 이것이 더 나은 결론을 찾으려 길고도 헛된 노력을 한 끝에 Mr.", "en": "“What I mean is, heaven *forbid* it!” This was Mr."},
        {"ko": "Cruncher가 내린 결론이었다.", "en": "Cruncher’s final statement after a long but useless attempt to find a better one."},
        {"ko": "그리고 그동안 Madame Defarge는 거리를 지나 점점 더 가까이 다가오고 있었다.", "en": "And all the while, Madame Defarge was making her way along the streets, coming closer and closer."},
        {"ko": "“우리가 고국으로 돌아가게 된다면,” Miss Pross가 말했다. “제가 기억하고 이해할 수 있는 한도 내에서, 당신이 이토록 인상 깊게 한 말을 Mrs.", "en": "“If we ever make it back to our home country,” said Miss Pross, “you can trust that I will tell Mrs."},
        {"ko": "Cruncher에게 꼭 전해주겠다고 믿으셔도 좋아요.”", "en": "Cruncher as much as I can remember and understand of what you have so impressively said;”"}
    ]
}

chapter_file = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_14.json'
queue_file = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'

with open(chapter_file, 'r', encoding='utf-8') as f:
    chapter_data = json.load(f)

for batch_id, trans_list in translations.items():
    with open(queue_file, 'r', encoding='utf-8') as f:
        queue = json.load(f)
    
    batch = next(b for b in queue if b['batch_id'] == batch_id)
    tags = batch['tags']
    
    for block in chapter_data:
        if block['tag'] in tags:
            idx = tags.index(block['tag'])
            block['ko'] = trans_list[idx]['ko']
            block['en'] = trans_list[idx]['en']
            
    for b in queue:
        if b['batch_id'] == batch_id:
            b['status'] = 'done'
            
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2)

with open(chapter_file, 'w', encoding='utf-8') as f:
    json.dump(chapter_data, f, indent=2, ensure_ascii=False)

print("Batches 10-14 done")
