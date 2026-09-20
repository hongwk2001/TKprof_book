import json

translations = {
    "book3_ch_14.json__batch0000": [
        {"ko": "[3부 14장: 뜨개질이 끝나다]", "en": ""},
        {"ko": "쉰두 명의 죄수들이 자신들의 운명을 기다리고 있던 그 동일한 시간대에(juncture of time), Madame Defarge는 복수의 여신(The Vengeance)과 혁명 재판소 배심원인 Jacques Three와 함께 음침하고 불길한 회의를 열었다.", "en": "At that exact time when the fifty-two prisoners were awaiting their fate, Madame Defarge held a dark and ominous council with The Vengeance and Jacques Three of the Revolutionary Jury."},
        {"ko": "Madame Defarge가 이 측근들(ministers)과 협의한 곳은 와인 가게가 아니라, 예전에 도로 보수공이었던 톱질꾼의 헛간이었다.", "en": "Madame Defarge did not confer with these ministers in the wine-shop, but rather in the shed of the wood-sawyer who had formerly been a mender of roads."},
        {"ko": "톱질꾼 본인은 회의에 참여하지 않고 약간 떨어진 곳에 머물렀는데, 이는 마치 지시를 받을 때까지 말하거나 질문받기 전까지 의견을 내지 않아야 하는 외곽 위성(outer satellite) 같았다.", "en": "The sawyer himself did not take part in the conference but waited a short distance away, like an outer satellite that was not allowed to speak until ordered or offer an opinion unless asked."},
        {"ko": "“하지만 우리의 Defarge는,” Jacques Three가 말했다. “틀림없이 훌륭한 공화국원이겠지? 안 그런가?”", "en": "“But our Defarge,” said Jacques Three, “is undoubtedly a good Republican, isn't he?”"},
        {"ko": "“그보다 더 나은 사람은 없어요,” 수다스러운 복수의 여신이 날카로운 목소리로 항변했다. “프랑스 전체에서요.”", "en": "“There is no better Republican in all of France,” the talkative Vengeance protested in a shrill voice."},
        {"ko": "“조용히 해, 꼬마 Vengeance.” Madame Defarge가 가볍게 찌푸린 얼굴로 부관의 입술에 손을 얹으며 말했다. “내 말 들어봐.", "en": "“Quiet, little Vengeance,” said Madame Defarge, placing her hand on her lieutenant’s lips with a slight frown. “Listen to me.”"},
        {"ko": "내 남편인 동지는 훌륭한 공화국원이고 대담한 남자야.", "en": "“My husband, comrade, is a good Republican and a brave man;”"},
        {"ko": "그는 공화국에 공로가 있고, 공화국의 신임을 받고 있어.", "en": "“he has earned the respect of the Republic and holds its trust.”"},
        {"ko": "하지만 내 남편에게도 약점이 있는데, 그는 이 의사(Doctor)에게 마음이 약해질(relent) 정도로 나약해.”", "en": "“But my husband has his weaknesses, and he is weak enough to show mercy toward this Doctor.”"}
    ],
    "book3_ch_14.json__batch0001": [
        {"ko": "“그것 참 유감이군요,” Jacques Three가 굶주린 입가에 잔인한 손가락을 댄 채 의심스럽다는 듯 머리를 흔들며 쉰 목소리로 말했다.", "en": "“It is a great pity,” croaked Jacques Three, shaking his head doubtfully, with his cruel fingers touching his hungry mouth;"},
        {"ko": "“그건 훌륭한 시민답지 못해요.", "en": "“that is not at all like a good citizen;”"},
        {"ko": "참으로 안타까운 일입니다.”", "en": "“it is something to be regretted.”"},
        {"ko": "“보세요,” 마담이 말했다. “나로서는, 이 의사에게 아무 관심도 없어요.", "en": "“Look,” said madame, “I care nothing for this Doctor.”"},
        {"ko": "그가 목을 유지하든(wear his head) 잃든, 내게는 그에 대한 어떤 사적인 이해관계도 없으니까요.", "en": "“Whether he keeps his head or loses it matters little to me, for I have no interest in him;”"},
        {"ko": "내겐 다 똑같아요.", "en": "“it is all the same to me.”"},
        {"ko": "하지만, Evrémonde 일가는 몰살되어야만 하고(exterminated), 아내와 아이도 남편과 아버지를 따라야만 해요.”", "en": "“But the Evrémonde family must be wiped out, and the wife and child must follow the husband and father.”"},
        {"ko": "“그 여자는 이 일에 아주 잘 어울리는 머리를 가졌지,” Jacques Three가 쉰 목소리로 말했다. “거기서 파란 눈과 금발을 보았는데, Samson이 그걸 집어 들었을 때 정말 매력적으로 보였거든.” 그는 마치 미식가(epicure)처럼 말하는 오우거(Ogre) 같았다.", "en": "“She has a fine head for it,” croaked Jacques Three. “I have seen blue eyes and golden hair up there, and they looked lovely when Samson held them up.” Like the ogre he was, he spoke as if he were a fine dining expert."},
        {"ko": "Madame Defarge는 시선을 아래로 깔고 잠시 생각에 잠겼다.", "en": "Madame Defarge looked down and thought for a moment."},
        {"ko": "“그 아이 역시,” Jacques Three가 자신의 말을 음미하듯 즐기며 덧붙였다. “금발에 파란 눈을 가졌지.", "en": "“The child, too,” observed Jacques Three, enjoying his own words thoughtfully, “has golden hair and blue eyes.”"}
    ],
    "book3_ch_14.json__batch0002": [
        {"ko": "그리고 우리는 그곳(단두대)에 아이를 올리는 일이 드물지.", "en": "“And it is rare that we have a child up there.”"},
        {"ko": "아주 예쁜 구경거리가 될 거야!”", "en": "“It will be a pretty sight!”"},
        {"ko": "“한마디로 말해서,” 잠시 상념에서 빠져나온 Madame Defarge가 말했다. “이 문제에 있어서 난 내 남편을 믿을 수 없어.", "en": "“In short,” said Madame Defarge, snapping out of her brief thought, “I cannot trust my husband with this matter.”"},
        {"ko": "어젯밤 이후로, 내 계획의 세부사항을 그에게 털어놓을 엄두가 나지 않을 뿐만 아니라;", "en": "“Not only have I felt, since last night, that I dare not share the details of my plans with him;”"},
        {"ko": "내가 지체한다면 그가 경고를 해줄 위험이 있고, 그러면 그들이 도망칠지도 모른다는 느낌이 들기 때문이야.”", "en": "“but I also feel that if I wait, there is a risk he might warn them, and then they could escape.”"},
        {"ko": "“그런 일은 결코 있어서는 안 돼,” Jacques Three가 쉰 목소리로 말했다.", "en": "“That must never happen,” croaked Jacques Three;"},
        {"ko": "“아무도 도망쳐선 안 돼.", "en": "“no one must escape.”"},
        {"ko": "지금으로선 머리(사형수)의 수가 절반도 충분치 않으니까.", "en": "“We do not have even half enough heads as it is.”"},
        {"ko": "우리는 하루에 120명(six score)은 처형해야 해.”", "en": "“We should have a hundred and twenty a day.”"},
        {"ko": "“한마디로,” Madame Defarge가 계속했다. “내 남편은 이 가족을 파멸로 몰고 갈 나만의 이유가 없고, 나 역시 이 의사를 동정심(sensibility)을 갖고 바라볼 그만의 이유가 없어.", "en": "“In short,” Madame Defarge continued, “my husband does not share my reasons for pursuing this family to their destruction, and I do not share his reasons for feeling any sympathy toward this Doctor.”"}
    ],
    "book3_ch_14.json__batch0003": [
        {"ko": "그러므로 나는 나를 위해 행동해야만 해.", "en": "“Therefore, I must act on my own.”"},
        {"ko": "이리 와봐, 작은 시민.”", "en": "“Come here, little citizen.”"},
        {"ko": "톱질꾼은 그녀에 대한 존경심과 죽음의 공포에서 비롯된 복종심으로, 빨간 모자에 손을 얹은 채 앞으로 다가왔다.", "en": "The wood-sawyer, holding her in respect and submitting out of mortal fear, stepped forward with his hand touching his red cap."},
        {"ko": "“그 신호들 말인데, 작은 시민,” Madame Defarge가 엄격하게 말했다. “그 여자가 죄수들에게 보냈던 신호들 말이야;", "en": "“Regarding those signals, little citizen,” Madame Defarge said strictly, “the ones she made to the prisoners;”"},
        {"ko": "오늘 당장 그것들에 대해 증언할 준비가 되어 있겠지?”", "en": "“are you ready to testify about them this very day?”"},
        {"ko": "“예, 예, 물론이죠!” 톱질꾼이 외쳤다. “매일, 날씨에 상관없이 두 시부터 네 시까지 항상 신호를 보냈죠. 때로는 그 어린아이와 함께, 때로는 혼자서요.", "en": "“Yes, yes, why not!” cried the sawyer. “Every day, in all kinds of weather, from two to four, she was always signalling, sometimes with the little one, sometimes alone.”"},
        {"ko": "전 제가 아는 걸 압니다.", "en": "“I know what I know.”"},
        {"ko": "제 두 눈으로 똑똑히 봤으니까요.”", "en": "“I have seen it with my own eyes.”"},
        {"ko": "그는 말을 하면서 온갖 몸짓을 지어 보였는데, 이는 그가 결코 본 적 없는 매우 다양한 신호들 중 일부를 우발적으로 흉내 내는 것 같았다.", "en": "He made all sorts of gestures as he spoke, as if casually imitating some of the wide variety of signals he had never actually seen."},
        {"ko": "“명백한 음모군,” Jacques Three가 말했다. “투명할 정도로 뻔해!”", "en": "“Clear plots,” said Jacques Three. “Transparent ones!”"}
    ],
    "book3_ch_14.json__batch0004": [
        {"ko": "“배심원들에 대해서는 의심의 여지가 없겠지?” Madame Defarge가 우울한 미소를 지으며 시선을 그에게 돌리며 물었다.", "en": "“There is no doubt about the Jury, is there?” asked Madame Defarge, turning her eyes toward him with a gloomy smile."},
        {"ko": "“애국적인 배심원들을 믿으십시오, 친애하는 여성 시민이여.", "en": "“Rely on the patriotic Jury, dear citizeness.”"},
        {"ko": "제 동료 배심원들은 제가 보증합니다.”", "en": "“I can vouch for my fellow Jurymen.”"},
        {"ko": "“자, 어디 보자,” Madame Defarge가 다시 곰곰이 생각하며 말했다. “그런데 한 번 더 생각해볼까!", "en": "“Now, let me see,” said Madame Defarge, pondering once more. “Yet one more thing!”"},
        {"ko": "내가 내 남편을 위해 이 의사를 살려둘 수 있을까?", "en": "“Can I spare this Doctor for my husband's sake?”"},
        {"ko": "나는 어느 쪽이든 아무런 감정이 없어.", "en": "“I have no feelings either way.”"},
        {"ko": "그를 살려둘 수 있을까?”", "en": "“Can I spare him?”"},
        {"ko": "“그는 한 명 몫의 머리(사형수)로 계산될 텐데요,” Jacques Three가 낮은 목소리로 거들었다. “우리는 정말 머리가 충분치 않습니다;", "en": "“He would count as one head,” Jacques Three noted in a low voice. “We really do not have enough heads;”"},
        {"ko": "그러니 참으로 아까운 일이 될 겁니다.”", "en": "“it would be a pity, I think.”"},
        {"ko": "“내가 봤을 때, 그도 그 여자와 함께 신호를 보내고 있었어,” Madame Defarge가 주장했다;", "en": "“He was signalling with her when I saw her,” argued Madame Defarge;"}
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

print("Batches 0-4 done")
