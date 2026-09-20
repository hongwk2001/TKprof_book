import json

translations = {
    "book3_ch_14.json__batch0005": [
        {"ko": "“내가 한 사람을 말하면서 다른 한 사람을 뺄 순 없지;", "en": "“I cannot speak of one without mentioning the other;”"},
        {"ko": "게다가 내가 침묵을 지킨 채, 여기 이 작은 시민에게 전적으로 사건을 맡길 수만도 없어.", "en": "“and I must not stay silent and leave the matter entirely to this little citizen here.”"},
        {"ko": "왜냐하면, 나 역시 나쁘지 않은 증인이니까.”", "en": "“Because I am not a bad witness myself.”"},
        {"ko": "복수의 여신과 Jacques Three는 그녀가 세상에서 가장 훌륭하고 경이로운 증인이라고 열렬히 주장하며 서로 경쟁하듯 떠들어댔다.", "en": "The Vengeance and Jacques Three competed with each other in their eager declarations that she was the most admirable and wonderful of witnesses."},
        {"ko": "작은 시민 역시 이에 질세라 그녀를 천상의 증인(celestial witness)이라고 선언했다.", "en": "Not wanting to be outdone, the little citizen declared her to be a heavenly witness."},
        {"ko": "“그는 자신의 운명(chance)을 받아들여야 해,” Madame Defarge가 말했다. “안 돼, 난 그를 살려둘 수 없어!", "en": "“He must take his chances,” said Madame Defarge. “No, I cannot spare him!”"},
        {"ko": "당신들은 세 시에 선약이 있지;", "en": "“You have an engagement at three o’clock;”"},
        {"ko": "오늘 처형될 무리(batch)를 보러 갈 거잖아.--당신도?”", "en": "“you are going to watch today's batch of executions.--Are you?”"},
        {"ko": "그 질문은 톱질꾼을 향한 것이었고, 그는 서둘러 그렇다고 대답했다:", "en": "The question was directed at the wood-sawyer, who quickly replied yes:"},
        {"ko": "그는 기회를 놓치지 않고 덧붙이기를, 자신은 가장 열렬한 공화국원이며 만약 기이한 국가 이발사(단두대를 가리킴)를 바라보며 오후의 파이프 담배를 즐기는 기쁨을 잃게 된다면 가장 비참한 공화국원이 될 것이라고 말했다.", "en": "taking the chance to add that he was the most passionate of Republicans, and that he would truly be the saddest of Republicans if anything kept him from the pleasure of smoking his afternoon pipe while watching the amusing national barber."}
    ],
    "book3_ch_14.json__batch0006": [
        {"ko": "그는 이 점에 대해 어찌나 호들갑스럽게 감정을 드러내는지, 그가 하루 중 매시간마다 자신의 개인적인 안전에 대해 자잘한 두려움을 품고 있을 것이라 의심받을 만했다(아마도 Madame Defarge의 머리에서 뿜어져 나오는, 그를 경멸조로 바라보는 어두운 눈동자에 의해 실제로 의심을 샀을 것이다).", "en": "He was so overly expressive about this that he might have been suspected (and perhaps was, by the dark eyes looking down at him with contempt from Madame Defarge’s face) of harboring small, personal fears for his own safety every hour of the day."},
        {"ko": "“나 역시,” 마담이 말했다. “같은 장소에 갈 예정이야.", "en": "“I,” said madame, “have an engagement at the exact same place.”"},
        {"ko": "그 일이 끝나면--오늘 밤 여덟 시쯤이라고 해두지--Saint Antoine 구역에 있는 내게로 와. 그러면 우리는 내 구역(Section)에서 이 사람들을 고발할 거야.”", "en": "“After it is finished—say, at eight tonight—come to me in Saint Antoine, and we will report these people to my Section.”"},
        {"ko": "톱질꾼은 여성 시민을 돕게 되어 자랑스럽고 영광이라고 말했다.", "en": "The wood-sawyer said he would be proud and honored to assist the citizeness."},
        {"ko": "여성 시민이 그를 쳐다보자, 그는 당황한 나머지 작은 개가 그러하듯 그녀의 시선을 피하고는 자신의 장작더미 사이로 물러나 톱 손잡이 위로 고개를 숙여 혼란스러움을 숨겼다.", "en": "When the citizeness looked at him, he grew embarrassed, avoided her gaze like a small dog would, retreated into his wood, and hid his confusion by leaning over the handle of his saw."},
        {"ko": "Madame Defarge는 배심원과 복수의 여신에게 문 쪽으로 조금 더 가까이 오라고 손짓한 뒤, 그곳에서 자신의 향후 계획을 다음과 같이 설명했다:", "en": "Madame Defarge motioned for the Juryman and The Vengeance to come a bit closer to the door, and there she explained her further plans to them like this:"},
        {"ko": "“그 여자는 지금 집에서 남편이 죽을 순간을 기다리고 있을 거야.", "en": "“She will be at home now, waiting for the moment of his death.”"},
        {"ko": "그녀는 애도하고 슬퍼하고 있겠지.", "en": "“She will be mourning and weeping.”"},
        {"ko": "그녀는 공화국의 정의를 탄핵할 만한 심리 상태에 있을 거야.", "en": "“She will be in a state of mind to challenge the justice of the Republic.”"},
        {"ko": "그녀는 공화국의 적들에 대한 동정심으로 가득 차 있을 거고.”", "en": "“She will be overflowing with sympathy for its enemies.”"}
    ],
    "book3_ch_14.json__batch0007": [
        {"ko": "내가 그녀에게 갈 테야.”", "en": "“I will go to her.”"},
        {"ko": "“이 얼마나 훌륭한 여인인가;", "en": "“What an admirable woman;”"},
        {"ko": "이 얼마나 사랑스러운 여인인가!” Jacques Three가 황홀경에 빠져 외쳤다. “아, 나의 소중한 사람!” 복수의 여신이 소리치며;", "en": "“what an adorable woman!” exclaimed Jacques Three in delight. “Ah, my precious one!” cried The Vengeance;"},
        {"ko": "그녀를 껴안았다.", "en": "and hugged her."},
        {"ko": "“내 뜨개질을 가져가,” Madame Defarge가 부관의 손에 뜨개질을 쥐여주며 말했다. “그리고 늘 앉던 내 자리에 그것을 준비해둬.", "en": "“Take my knitting,” said Madame Defarge, handing it to her lieutenant, “and have it ready for me at my usual seat.”"},
        {"ko": "내 평소 의자도 맡아두고.", "en": "“Save my regular chair for me.”"},
        {"ko": "당신은 곧장 그곳으로 가, 오늘은 평소보다 구경꾼 무리(concourse)가 더 많을 테니까.”", "en": "“Go straight there, because there will likely be a larger crowd than usual today.”"},
        {"ko": "“대장의 명령에 기꺼이 따르겠습니다,” 복수의 여신이 민첩하게 대답하고 그녀의 뺨에 입을 맞추며 말했다. “늦지 않으실 거죠?”", "en": "“I gladly obey my Chief's orders,” said The Vengeance quickly, kissing her cheek. “You won't be late, will you?”"},
        {"ko": "“시작하기 전에는 그곳에 갈 거야.”", "en": "“I will be there before it begins.”"},
        {"ko": "“그리고 죄수 호송 마차(tumbrils)가 도착하기 전에요.", "en": "“And before the death carts arrive.”"}
    ],
    "book3_ch_14.json__batch0008": [
        {"ko": "내 영혼이여, 반드시 그곳에 계셔야 해요.” 이미 거리로 접어든 그녀의 뒤에 대고 복수의 여신이 소리쳤다. “호송 마차가 도착하기 전에요!”", "en": "“Make sure you are there, my soul,” The Vengeance called after her, as she had already turned into the street, “before the death carts arrive!”"},
        {"ko": "Madame Defarge는 가볍게 손을 흔들어 알았다는 것과 제시간에 도착할 것임을 암시한 뒤, 진흙탕을 지나 감옥 담벼락 모퉁이를 돌아갔다.", "en": "Madame Defarge waved her hand slightly to show that she heard and could be trusted to arrive on time, and then walked through the mud and around the corner of the prison wall."},
        {"ko": "복수의 여신과 배심원은 멀어지는 그녀의 뒷모습을 보며, 그녀의 훌륭한 자태와 탁월한 도덕적 자질(혁명적 잔혹성을 칭송하는 반어적 표현)을 높이 평가했다.", "en": "The Vengeance and the Juryman watched her walk away, highly admiring her fine figure and her outstanding moral qualities."},
        {"ko": "그 당시에는 그 시대가 무서우리만치 흉측한 손길을 뻗친 여성들이 많았다;", "en": "There were many women in those days who had been terribly scarred by the harsh times;"},
        {"ko": "하지만, 지금 거리를 걸어가고 있는 이 무자비한 여인보다 더 두려운 존재는 그들 중 단 한 명도 없었다.", "en": "but among them, not one was more to be feared than this ruthless woman currently making her way down the streets."},
        {"ko": "강인하고 두려움 없는 성격, 예리한 감각과 기민함, 엄청난 결단력, 그리고 소유자에게 확고함과 적대감을 부여할 뿐만 아니라 타인에게 그러한 자질들을 본능적으로 인식하게 만드는 종류의 미모를 지닌 그녀는;", "en": "With a strong and fearless personality, sharp intelligence and quickness, great determination, and a kind of beauty that not only seemed to give its owner firmness and hostility, but also made others instinctively recognize those traits;"},
        {"ko": "어떤 상황에서든 이 혼란스러운 시대가 그녀를 위로 떠밀어 올렸을 것이다.", "en": "the troubled times would have pushed her to the top under any circumstances."},
        {"ko": "하지만, 어린 시절부터 스며든 뿌리 깊은 부당함에 대한 울분과 한 계급에 대한 만성적인 증오심이 기회와 맞물려 그녀를 암호랑이로 길러냈다.", "en": "But having grown up with a lingering sense of injustice and a deep-seated hatred for an entire social class, the opportunity had turned her into a tigress."},
        {"ko": "그녀에게는 동정심이라고는 전혀 없었다.", "en": "She was completely lacking in pity."},
        {"ko": "만약 그녀에게 한때 미덕이 있었다고 해도, 그것은 이미 그녀에게서 완전히 빠져나가고 없었다.", "en": "If she ever possessed any virtue, it had completely left her."}
    ],
    "book3_ch_14.json__batch0009": [
        {"ko": "무고한 자가 조상들의 죄로 인해 죽어야 한다는 사실은 그녀에게 아무런 문제도 되지 않았다;", "en": "It meant nothing to her that an innocent man was going to die for the sins of his ancestors;"},
        {"ko": "그녀는 그를 본 것이 아니라, 그들(귀족 계급)을 보았기 때문이다.", "en": "she didn't see him, but rather the class he represented."},
        {"ko": "그의 아내가 과부가 되고 그의 딸이 고아가 되어야 한다는 것도 그녀에게는 대수롭지 않았다;", "en": "It meant nothing to her that his wife would become a widow and his daughter an orphan;"},
        {"ko": "그것은 불충분한 형벌이었다. 왜냐하면 그들은 그녀의 타고난 적이자 먹잇감이었고, 따라서 살아갈 권리가 없었기 때문이다.", "en": "that was not enough punishment, because they were her natural enemies and prey, and therefore had no right to live."},
        {"ko": "그녀에게 호소하는 것은 희망 없는 일이었는데, 그녀는 심지어 자기 자신에 대해서도 일말의 동정심이 없었기 때문이다.", "en": "Pleading with her was hopeless because she had no sense of pity, not even for herself."},
        {"ko": "그녀가 가담했던 수많은 충돌 중 어느 곳에서든 그녀가 거리에 쓰러지게(laid low) 되었다 하더라도, 그녀는 스스로를 동정하지 않았을 것이다;", "en": "If she had been struck down in the streets during any of the many fights she took part in, she would not have felt sorry for herself;"},
        {"ko": "또한, 만약 그녀가 내일 단두대로 가라는 명령을 받았다 하더라도, 그녀를 그곳으로 보낸 자와 자리를 바꾸고 싶다는 맹렬한 욕망 외에는 어떤 유약한 감정도 없이 단두대를 향해 나아갔을 것이다.", "en": "nor, if she were ordered to be executed tomorrow, would she have gone to the block with any softer feeling than a fierce desire to trade places with the person who sent her there."},
        {"ko": "이런 마음을 품은 Madame Defarge가 거친 겉옷 아래로 걸음을 옮기고 있었다.", "en": "This was the kind of heart Madame Defarge carried beneath her rough clothes."},
        {"ko": "무심하게 걸쳐 입은 그 옷은 묘하게도 그녀에게 꽤 잘 어울렸고, 그녀의 어두운 머리칼은 투박한 빨간 모자 아래서 풍성해 보였다.", "en": "Though worn carelessly, the dress suited her in a strange way, and her dark hair looked full and rich under her coarse red cap."},
        {"ko": "그녀의 가슴팍에 몰래 숨겨져 있는 것은, 장전된 권총이었다.", "en": "Hidden away in her clothing was a loaded pistol."}
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

print("Batches 5-9 done")
