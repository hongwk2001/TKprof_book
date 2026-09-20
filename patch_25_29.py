import json

translations = {
    "book3_ch_14.json__batch0025": [
        {"ko": "“그 사람들이 그 방에 있는지 없는지 모르는 한, 당신은 무엇을 해야 할지 확신하지 못하겠지,” Miss Pross가 속으로 말했다;", "en": "“As long as you don't know whether they are in that room or not, you are unsure of what to do,” Miss Pross said to herself;"},
        {"ko": "“그리고 내가 막을 수 있다면, 당신은 그걸 영영 모를 테고;", "en": "“and you will not find out, if I can stop you;”"},
        {"ko": "그걸 알든 모르든 간에, 내가 당신을 붙잡고 있는 한 여기서 나가지 못할 거다.”", "en": "“and whether you know it or not, you won't leave this place as long as I can hold you.”"},
        {"ko": "“난 처음부터 줄곧 거리에 있었지만 아무것도 날 막지 못했어. 널 갈기갈기 찢어발기더라도 널 그 문에서 치워버리겠다,” Madame Defarge가 말했다.", "en": "“I have been in the streets from the very beginning, and nothing has stopped me. I will tear you to pieces, but I will move you from that door,” said Madame Defarge."},
        {"ko": "“우리는 지금 외진 안뜰에 있는 높은 집 꼭대기에 단둘이 있어서 누가 우리 소리를 들을 일도 없을 테지. 그러니 당신을 여기 붙잡아 둘 수 있는 육체적인 힘을 주시기를 기도할 수밖에. 당신이 여기 묶여 있는 1분 1초가 우리 아가씨에게는 10만 기니(guineas)의 가치가 있으니까,” Miss Pross가 말했다.", "en": "“We are alone at the top of a tall house in a quiet courtyard, so no one is likely to hear us. I pray for the physical strength to keep you here, because every minute you are trapped here is worth a hundred thousand guineas to my darling,” said Miss Pross."},
        {"ko": "Madame Defarge가 문을 향해 돌진했다.", "en": "Madame Defarge lunged at the door."},
        {"ko": "Miss Pross는 순간적인 본능으로 두 팔을 뻗어 그녀의 허리를 꽉 끌어안았다.", "en": "Acting on instinct, Miss Pross grabbed her tightly around the waist with both arms."},
        {"ko": "Madame Defarge가 발버둥 치며 때려 보았지만 헛수고였다;", "en": "It was useless for Madame Defarge to struggle and hit;"},
        {"ko": "언제나 증오보다 훨씬 더 강한 사랑의 끈질긴 힘으로 무장한 Miss Pross가 그녀를 단단히 껴안았고, 몸싸움 중에 심지어 그녀를 바닥에서 번쩍 들어 올리기까지 했다.", "en": "Miss Pross, fueled by the fierce strength of love—which is always so much stronger than hate—held her tightly, even lifting her off the floor during their struggle."},
        {"ko": "Madame Defarge의 두 손이 Miss Pross의 얼굴을 마구 치고 할퀴었다;", "en": "Madame Defarge's hands beat and tore at her face;"}
    ],
    "book3_ch_14.json__batch0026": [
        {"ko": "하지만 Miss Pross는 고개를 숙인 채 그녀의 허리를 꽉 붙잡고, 물에 빠진 여자가 매달리는 것보다 더 악착같이 그녀에게 매달렸다.", "en": "but Miss Pross kept her head down, held her tightly around the waist, and clung to her with a grip stronger than that of a drowning woman."},
        {"ko": "이내 Madame Defarge의 두 손이 때리기를 멈추더니, 자신을 조이고 있는 허리춤을 더듬었다. “내 팔 밑에 있군,” Miss Pross가 억눌린 목소리로 말했다. “넌 그걸 뽑지 못할 거다.", "en": "Soon, Madame Defarge’s hands stopped striking and felt around her own gripped waist. “It is under my arm,” said Miss Pross in a muffled voice, “and you will not pull it out.”"},
        {"ko": "내가 너보다 힘이 세니, 하늘에 감사할 따름이지.", "en": "“I am stronger than you, and I thank Heaven for it.”"},
        {"ko": "우리 둘 중 하나가 기절하거나 죽을 때까지 널 놔주지 않겠다!”", "en": "“I will hold you until one of us faints or dies!”"},
        {"ko": "Madame Defarge의 두 손이 그녀의 가슴팍으로 향했다.", "en": "Madame Defarge’s hands went to her own chest."},
        {"ko": "Miss Pross가 고개를 들어 그것이 무엇인지 보았고, 그것을 내리쳤다. 번쩍하는 섬광과 굉음이 터져 나왔고, 그녀는 연기에 눈이 멀어 홀로 서 있었다.", "en": "Miss Pross looked up, saw what it was, and struck at it. A flash and a loud crash followed, and she found herself standing alone, blinded by the smoke."},
        {"ko": "이 모든 일은 순식간에 일어났다.", "en": "All of this happened in a split second."},
        {"ko": "연기가 걷히면서 무서운 정적이 찾아왔고, 바닥에 생명 없이 누워 있는 광분한 여인의 영혼처럼 그 연기는 공기 중으로 흩어졌다.", "en": "As the smoke cleared, leaving a terrifying silence, it drifted away into the air like the soul of the furious woman whose lifeless body now lay on the floor."},
        {"ko": "자신이 처한 상황에 대한 첫 공포와 경악 속에서, Miss Pross는 그 시체에서 최대한 멀리 떨어져 지나간 뒤, 소용없는 도움을 청하려 계단을 뛰어 내려갔다.", "en": "In the initial shock and horror of the situation, Miss Pross backed as far away from the body as she could and ran down the stairs to call for help, even though it was useless."},
        {"ko": "다행히도 그녀는 자신이 저지른 일의 결과를 제때에 깨닫고는, 걸음을 멈추고 다시 되돌아갔다.", "en": "Fortunately, she thought about the consequences of what she had done just in time to stop herself and go back."}
    ],
    "book3_ch_14.json__batch0027": [
        {"ko": "다시 그 문으로 들어가는 것은 끔찍한 일이었다;", "en": "It was terrifying to go back through that door;"},
        {"ko": "하지만 그녀는 들어갔고, 심지어 모자와 자신이 꼭 입어야 할 다른 물건들을 챙기기 위해 시체 근처까지 갔다.", "en": "but she did go in, and even went near the body to grab her bonnet and the other things she needed to wear."},
        {"ko": "그녀는 계단 밖으로 나와 먼저 문을 닫고 잠근 뒤 열쇠를 빼내고 나서야 챙겨 온 것들을 입었다.", "en": "She put them on out on the staircase, after first shutting and locking the door and taking the key with her."},
        {"ko": "그런 다음 그녀는 계단에 잠시 주저앉아 숨을 고르며 눈물을 흘렸고, 이내 일어나 서둘러 그곳을 떠났다.", "en": "Then she sat down on the stairs for a few moments to catch her breath and cry, before getting up and hurrying away."},
        {"ko": "운 좋게도 그녀의 모자에 베일이 달려 있어서 망정이지, 그렇지 않았다면 거리를 지나가다 사람들에게 붙잡히지 않을 수 없었을 것이다.", "en": "Luckily, she had a veil on her bonnet, or she barely could have walked through the streets without being stopped."},
        {"ko": "게다가 운 좋게도, 그녀는 본래 외모가 유별나서 다른 여인들처럼 흉해진 모습(싸움의 흔적)이 잘 눈에 띄지 않았다.", "en": "Fortunately, too, her appearance was naturally so unusual that the disfigurement didn't show as clearly as it would have on any other woman."},
        {"ko": "꽉 쥐어진 손가락 자국이 얼굴에 깊게 남았고, 머리카락은 뜯겨 나갔으며, (떨리는 손으로 서둘러 수습한) 옷은 백 군데나 움켜쥐어지고 찢겨 있었기에 그녀에게는 그 두 가지 이점이 모두 필요했다.", "en": "She needed both of these advantages, because the marks of gripping fingers were deep in her face, her hair was torn, and her dress (which she had hurriedly put back together with shaking hands) was clutched and dragged in a hundred different ways."},
        {"ko": "다리를 건너면서, 그녀는 방 열쇠를 강물에 떨어뜨렸다.", "en": "While crossing the bridge, she dropped the door key into the river."},
        {"ko": "호위병(Mr. Cruncher)보다 몇 분 일찍 대성당에 도착해 기다리면서, 그녀는 만약 그 열쇠가 벌써 그물에 걸려 건져 올려졌다면 어쩌지, 만약 그게 식별된다면, 만약 그 문이 열려 시신이 발견된다면, 만약 자신이 성문에서 붙잡혀 감옥으로 보내지고 살인죄로 기소된다면 어쩌지 하는 생각에 사로잡혔다!", "en": "Arriving at the cathedral a few minutes before her escort and waiting there, she began to worry: what if the key had already been caught in a net? What if it was identified? What if the door was opened and the body discovered? What if she was stopped at the city gate, sent to prison, and charged with murder!"},
        {"ko": "이런 불안한 생각들이 맴도는 가운데 호위병이 나타나 그녀를 태우고 그곳을 떠났다.", "en": "In the midst of these racing thoughts, her escort appeared, took her into the carriage, and drove her away."}
    ],
    "book3_ch_14.json__batch0028": [
        {"ko": "“거리에 무슨 소리가 들리나요?” 그녀가 그에게 물었다.", "en": "“Is there any noise in the streets?” she asked him."},
        {"ko": "“평소 나는 소리들이죠,” Mr.", "en": "“The usual noises,” replied Mr."},
        {"ko": "Cruncher가 대답했다;", "en": "Cruncher;"},
        {"ko": "그리고 그녀의 질문과 표정에 놀란 듯 그녀를 쳐다보았다.", "en": "and he looked surprised by both her question and her appearance."},
        {"ko": "“안 들려요,” Miss Pross가 말했다. “뭐라고 하셨죠?”", "en": "“I can't hear you,” said Miss Pross. “What did you say?”"},
        {"ko": "Mr.", "en": "It was useless for Mr."},
        {"ko": "Cruncher가 자신이 한 말을 반복해 보았지만 헛수고였다;", "en": "Cruncher to repeat what he had said;"},
        {"ko": "Miss Pross는 그의 말을 들을 수 없었다. “그래서 고개를 끄덕여야겠군,” 놀란 Mr.", "en": "Miss Pross could not hear him. “So I'll just nod my head,” thought the amazed Mr."},
        {"ko": "Cruncher가 속으로 생각했다. “어찌 됐든 그건 볼 수 있을 테니까.” 그리고 그녀는 정말로 고개 끄덕이는 것은 보았다.", "en": "Cruncher. “At least she'll be able to see that.” And she did."},
        {"ko": "“지금 거리에 무슨 소리가 들리나요?” 이내 Miss Pross가 다시 물었다.", "en": "“Is there any noise in the streets now?” Miss Pross asked again a moment later."}
    ],
    "book3_ch_14.json__batch0029": [
        {"ko": "다시 Mr.", "en": "Once again, Mr."},
        {"ko": "Cruncher는 고개를 끄덕였다.", "en": "Cruncher nodded his head."},
        {"ko": "“나는 안 들려요.”", "en": "“I don't hear it.”"},
        {"ko": "“한 시간 만에 귀가 먹었다고?” Mr.", "en": "“Gone deaf in an hour?” said Mr."},
        {"ko": "Cruncher가 심란한 마음으로 깊은 생각에 잠겨 중얼거렸다;", "en": "Cruncher, thinking it over with a very troubled mind;"},
        {"ko": "“이 여자한테 무슨 일이 생긴 거지?”", "en": "“what has happened to her?”"},
        {"ko": "“마치,” Miss Pross가 말했다. “번쩍하는 섬광과 굉음이 있었던 것 같은데, 그 굉음이 이생에서 내가 마지막으로 듣는 소리일 것만 같은 기분이에요.”", "en": "“I feel,” said Miss Pross, “as if there was a flash and a crash, and that crash was the last thing I will ever hear in this life.”"},
        {"ko": "“빌어먹을, 여자 상태가 영 이상하구만!” Mr.", "en": "“I'll be damned if she isn't in a strange state!” said Mr."},
        {"ko": "Cruncher가 점점 더 불안해하며 말했다. “용기를 잃지 않으려고 뭘 들이켠(복용한) 거지?", "en": "Cruncher, growing more and more disturbed. “What could she have taken to keep her courage up?”"},
        {"ko": "들어보쇼!", "en": "“Listen!”"}
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

print("Batches 25-29 done")
