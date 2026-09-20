import json

translations = {
    "book3_ch_14.json__batch0020": [
        {"ko": "“생긴 걸로 보아 당신은 루시퍼(악마)의 아내쯤 되겠군요,” Miss Pross가 숨을 헐떡이며 말했다. “그렇다 해도, 당신은 나를 이기지 못할 겁니다.", "en": "“From your appearance, you might be the wife of Lucifer,” said Miss Pross, breathing hard. “Nevertheless, you won't get the better of me.”"},
        {"ko": "나는 영국 여자거든요.”", "en": "“I am an Englishwoman.”"},
        {"ko": "Madame Defarge는 그녀를 경멸하듯 바라보았지만, Miss Pross가 그러했듯 두 사람이 지금 궁지에 몰린 채 대치하고 있다는 사실을 어느 정도 직감하고 있었다.", "en": "Madame Defarge looked at her with contempt, but she still shared something of Miss Pross’s own realization that the two of them were locked in a standoff."},
        {"ko": "그녀는 단단하고 억세며 강단 있는 여인을 마주하고 있었는데, 이는 과거에 Mr.", "en": "She saw a tight, hard, wiry woman standing before her, just as Mr."},
        {"ko": "Lorry가 같은 사람에게서 강인한 손길을 지닌 여인을 보았던 것과 같았다.", "en": "Lorry had seen in that same figure a woman with a strong hand, years ago."},
        {"ko": "그녀는 Miss Pross가 그 가족의 헌신적인 친구라는 것을 아주 잘 알고 있었고;", "en": "She knew perfectly well that Miss Pross was a devoted friend of the family;"},
        {"ko": "Miss Pross 역시 Madame Defarge가 그 가족의 악의적인 적이라는 것을 아주 잘 알고 있었다.", "en": "and Miss Pross knew perfectly well that Madame Defarge was the family’s spiteful enemy."},
        {"ko": "“저기 가는 길에,” 죽음의 장소를 향해 가볍게 손짓하며 Madame Defarge가 말했다. “사람들이 내 의자와 뜨개질을 맡아두고 있는 그곳으로 가는 길에, 지나가는 길에 그녀에게 안부나 전할까 해서 왔소.", "en": "“On my way over there,” said Madame Defarge, with a slight wave of her hand toward the place of execution, “where they are saving my chair and my knitting for me, I have come to pay my respects to her in passing.”"},
        {"ko": "그녀를 좀 보고 싶소만.”", "en": "“I wish to see her.”"},
        {"ko": "“당신의 의도가 악하다는 걸 알고 있어요,” Miss Pross가 말했다. “그리고 확실히 말해두지만, 나는 그 악의에 맞서 물러서지 않을 겁니다.”", "en": "“I know that your intentions are evil,” said Miss Pross, “and you can be sure that I will stand my ground against them.”"}
    ],
    "book3_ch_14.json__batch0021": [
        {"ko": "두 사람은 각자 자신의 모국어로 말했다;", "en": "Each of them spoke in her own language;"},
        {"ko": "누구도 상대방의 말을 이해하지 못했다;", "en": "neither understood the other’s words;"},
        {"ko": "하지만 두 사람 모두 매우 경계하며, 상대의 표정과 태도를 통해 그 알아들을 수 없는 말들이 무슨 뜻인지 추론하려 애썼다.", "en": "yet both were highly alert, intensely trying to guess what the unreadable words meant from the other's look and behavior."},
        {"ko": "“지금 이 순간 나한테서 숨어 있어 봤자 그녀에게 좋을 건 없을 텐데,” Madame Defarge가 말했다. “훌륭한 애국자들은 그게 무슨 뜻인지 알 거요.", "en": "“It won't do her any good to hide from me right now,” said Madame Defarge. “Good patriots will know what that implies.”"},
        {"ko": "그녀를 보게 해주시오.", "en": "“Let me see her.”"},
        {"ko": "가서 내가 그녀를 보고 싶어 한다고 전하시오.", "en": "“Go tell her that I want to see her.”"},
        {"ko": "내 말 안 들리소?”", "en": "“Do you hear me?”"},
        {"ko": "“당신의 저 두 눈이 침대 조임쇠(bed-winches)이고,” Miss Pross가 대답했다. “내가 영국식 기둥 네 개짜리 침대(four-poster)라 할지라도, 내게서 나무토막 하나 빼내지 못할 겁니다.", "en": "“If those eyes of yours were bed-winches,” replied Miss Pross, “and I were an English four-poster bed, they couldn't loosen a single splinter of me.”"},
        {"ko": "안 되지, 이 사악한 외국 여자야;", "en": "“No, you wicked foreign woman;”"},
        {"ko": "내가 당신의 적수다.”", "en": "“I am your match.”"}
    ],
    "book3_ch_14.json__batch0022": [
        {"ko": "Madame Defarge가 이 관용적인 표현들의 세부적인 의미까지 이해했을 리는 없었다;", "en": "Madame Defarge was unlikely to understand the exact meaning of these idiomatic phrases;"},
        {"ko": "하지만, 자신이 무시당하고 있다는 것을 눈치챌 정도로는 그 말뜻을 알아들었다.", "en": "but she understood enough to realize that she was being defied."},
        {"ko": "“멍청하고 돼지 같은 여자!” Madame Defarge가 인상을 찌푸리며 말했다. “당신의 대답 따윈 듣지 않겠소.", "en": "“Idiotic, pig-like woman!” said Madame Defarge, frowning. “I won't take an answer from you.”"},
        {"ko": "그녀를 보겠다고 요구하는 바요.", "en": "“I demand to see her.”"},
        {"ko": "내가 그녀를 보겠다고 요구한다고 전하든지, 아니면 문에서 비켜서서 내가 그녀에게 가게 놔두든지 하시오!”  그녀는 화가 나서 설명하듯 오른팔을 휘두르며 이렇게 말했다.", "en": "“Either tell her that I demand to see her, or get away from the door and let me go to her!” She said this with an angry, clarifying wave of her right arm."},
        {"ko": "“설마 내가,” Miss Pross가 말했다. “당신의 그 터무니없는 언어를 이해하고 싶어질 날이 올 거라곤 생각도 못 했어요;", "en": "“I never thought,” said Miss Pross, “that I would ever want to understand your nonsensical language;”"},
        {"ko": "하지만 당신이 진실을, 혹은 진실의 일부라도 의심하고 있는지 알 수만 있다면 내가 입은 옷만 빼고 가진 걸 다 주겠어요.”", "en": "“but I would give everything I own, except the clothes on my back, to know whether you suspect the truth, or any part of it.”"},
        {"ko": "두 사람은 단 한 순간도 상대방에게서 눈을 떼지 않았다.", "en": "Neither of them looked away from the other's eyes for even a second."},
        {"ko": "Madame Defarge는 Miss Pross가 그녀를 처음 발견했을 때 서 있던 자리에서 한 발짝도 움직이지 않았었지만;", "en": "Madame Defarge had not moved from the spot where she was standing when Miss Pross first noticed her;"},
        {"ko": "이제, 그녀가 한 걸음 앞으로 나섰다.", "en": "but now, she took one step forward."}
    ],
    "book3_ch_14.json__batch0023": [
        {"ko": "“나는 영국인입니다,” Miss Pross가 말했다. “나는 필사적이에요.", "en": "“I am a Briton,” said Miss Pross, “I am desperate.”"},
        {"ko": "내 안위 따윈 영국 동전 2펜스(Twopence)만큼도 신경 쓰지 않아요.", "en": "“I don't care two cents about myself.”"},
        {"ko": "내가 당신을 여기에 더 오래 묶어둘수록, 우리 예쁜 아가씨(Ladybird)에게 더 큰 희망이 생긴다는 걸 알아요.", "en": "“I know that the longer I keep you here, the more hope there is for my Ladybird.”"},
        {"ko": "내게 손가락 하나라도 까딱했다간, 당신 머리통에 그 검은 머리카락을 한 줌도 안 남겨 놓을 테니까!”", "en": "“If you lay a single finger on me, I won't leave a handful of that dark hair on your head!”"},
        {"ko": "Miss Pross는 속사포처럼 쏟아내는 문장 사이사이에 고개를 젓고 눈을 번뜩이며 이렇게 말했다. 문장 하나를 내뱉을 때마다 숨을 한 번씩 들이마셨다.", "en": "Miss Pross spoke like this, shaking her head and flashing her eyes between every rapid sentence, and taking a whole breath for every rapid sentence."},
        {"ko": "평생 남을 때려본 적 없는 Miss Pross가 이렇게 말한 것이다.", "en": "This was Miss Pross, who had never hit anyone in her entire life."},
        {"ko": "하지만, 그녀의 용기는 감정적인 성질의 것이어서 참을 수 없는 눈물을 핑 돌게 했다.", "en": "However, her courage was so deeply emotional that it brought unstoppable tears to her eyes."},
        {"ko": "이것은 Madame Defarge가 전혀 이해하지 못하여 나약함으로 착각한 용기였다. “하, 하!” 그녀가 비웃었다. “가엾은 비루한 것!", "en": "This was a kind of courage Madame Defarge understood so little that she mistook it for weakness. “Ha, ha!” she laughed, “you poor wretch!”"},
        {"ko": "네깟 게 무슨 가치가 있다고!", "en": "“What are you worth!”"},
        {"ko": "난 그 의사에게 말하러 온 거요.” 그러고 나서 그녀는 목소리를 높여 소리쳤다. “의사 동지!", "en": "“I am speaking to that Doctor.” Then she raised her voice and called out, “Citizen Doctor!”"}
    ],
    "book3_ch_14.json__batch0024": [
        {"ko": "Evrémonde의 아내!", "en": "“Wife of Evrémonde!”"},
        {"ko": "Evrémonde의 아이!", "en": "“Child of Evrémonde!”"},
        {"ko": "이 비참한 바보만 빼고 누구든, 여성 시민 Defarge에게 대답하시오!”", "en": "“Anyone besides this miserable fool, answer Citizeness Defarge!”"},
        {"ko": "어쩌면 뒤이은 침묵이, 어쩌면 Miss Pross의 얼굴 표정에 숨겨져 있던 무언가가 드러난 것이, 아니면 그 둘과는 별개의 갑작스러운 불길한 예감이 Madame Defarge에게 그들이 떠났다는 사실을 속삭여 주었을지도 모른다.", "en": "Perhaps it was the silence that followed, perhaps a hidden clue in Miss Pross’s expression, or perhaps a sudden feeling of doubt unrelated to either, but something whispered to Madame Defarge that they were gone."},
        {"ko": "그녀는 세 개의 문을 재빨리 열고 안을 들여다보았다.", "en": "She quickly opened three of the doors and looked inside."},
        {"ko": "“방들이 온통 어질러져 있고, 서둘러 짐을 꾸린 흔적이 있으며, 바닥에는 잡동사니들이 널려 있군.", "en": "“Those rooms are completely messy, there has been rushed packing, and random items are left on the floor.”"},
        {"ko": "네 뒤에 있는 그 방에는 아무도 없어!", "en": "“There is no one in that room behind you!”"},
        {"ko": "들여다보게 비켜.”", "en": "“Let me look.”"},
        {"ko": "“절대 안 돼!” Madame Defarge가 대답을 완벽하게 알아들었듯, 그 요구를 완벽하게 알아들은 Miss Pross가 말했다.", "en": "“Never!” said Miss Pross, who understood the demand just as perfectly as Madame Defarge understood her refusal."},
        {"ko": "“그 방에 없다면, 도망친 게 분명해. 뒤쫓아가서 잡아올 수 있어,” Madame Defarge가 혼잣말을 했다.", "en": "“If they are not in that room, they have fled, and they can be chased down and brought back,” Madame Defarge said to herself."}
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

print("Batches 20-24 done")
