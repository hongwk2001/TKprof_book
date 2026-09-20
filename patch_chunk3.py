import json

data_dict = {
"P038_1": {"ko": "'내 친애하는 다네이, 내가 당신에게 문 밖으로 나가자고 하던가요?", "en": "'Do I ask you, my dear Darnay, to pass the door?"},
"P038_2": {"ko": "제가 그걸 요구하면, 그때 거절하십시오.", "en": "When I ask that, refuse."},
"P038_3": {"ko": "이 탁자 위에 펜과 잉크와 종이가 있습니다.", "en": "There are pen and ink and paper on this table."},
"P038_4": {"ko": "글을 쓸 만큼 손이 안정되어 있습니까?'", "en": "Is your hand steady enough to write?'"},
"P040_1": {"ko": "'다시 손을 안정시키고 제가 부르는 대로 쓰십시오.", "en": "'Steady it again, and write what I shall dictate."},
"P040_2": {"ko": "빨리, 친구, 빨리요!'", "en": "Quick, friend, quick!'"},
"P041_1": {"ko": "어리둥절한 머리를 손으로 짚은 채, 다네이는 탁자에 앉았다.", "en": "Pressing his hand to his bewildered head, Darnay sat down at the table."},
"P041_2": {"ko": "카튼은 오른손을 가슴에 넣은 채 그의 곁에 바짝 섰다.", "en": "Carton, with his right hand in his breast, stood close beside him."},
"P047_1": {"ko": "죄수는 질문을 받을 때마다 올려다보았다.", "en": "The prisoner looked up at each question."},
"P047_2": {"ko": "카튼은 가슴에 손을 넣은 채 그의 위에 서서 내려다보았다.", "en": "Carton, standing over him with his hand in his breast, looked down."},
"P048_1": {"ko": "카튼이 불러주었다. '당신이 기억한다면, 오래전 우리 사이에 오갔던 말들을, 이것을 볼 때 당신은 쉽게 이해할 것입니다.", "en": "Carton dictated, 'If you remember the words that passed between us, long ago, you will readily comprehend this when you see it."},
"P048_2": {"ko": "당신이 그 말들을 기억하고 있다는 것을 저는 압니다.", "en": "You do remember them, I know."},
"P048_3": {"ko": "그것들을 잊는 것은 당신의 본성에 맞지 않으니까요.'", "en": "It is not in your nature to forget them.'"},
"P051_1": {"ko": "'다 썼습니다.", "en": "'I have."},
"P051_2": {"ko": "손에 쥐고 있는 게 무기입니까?'", "en": "Is that a weapon in your hand?'"},
"P054_1": {"ko": "'곧 알게 될 겁니다.", "en": "'You shall know directly."},
"P054_2": {"ko": "계속 쓰십시오; 몇 단어 안 남았습니다.' 그가 다시 불러주었다. '저는 그것들을 증명할 수 있는 때가 왔다는 것에 감사하고 있습니다.", "en": "Write on; there are but a few words more.' He dictated again. 'I am thankful that the time has come, when I can prove them."},
"P054_3": {"ko": "제가 그렇게 하는 것은 후회나 슬픔의 대상이 아닙니다.' 그가 글을 쓰는 사람에게 시선을 고정한 채 이 말들을 할 때, 그의 손은 글 쓰는 이의 얼굴 곁으로 느리고 부드럽게 내려갔다.", "en": "That I do so is no subject for regret or grief.' As he said these words with his eyes fixed on the writer, his hand slowly and softly moved down close to the writer's face."},
"P059_1": {"ko": "'아무것도 안 느껴집니다; 여기에 무언가 있을 리가 없죠.", "en": "'I am conscious of nothing; there can be nothing here."},
"P059_2": {"ko": "펜을 들고 끝내십시오.", "en": "Take up the pen and finish."},
"P059_3": {"ko": "서두르십시오, 빨리!'", "en": "Hurry, hurry!'"},
"P060_1": {"ko": "마치 기억력이 손상되거나 기능에 이상이 생긴 것처럼, 죄수는 주의력을 모으려 애썼다.", "en": "As if his memory were impaired, or his faculties disordered, the prisoner made an effort to rally his attention."},
"P060_2": {"ko": "흐릿한 눈빛과 달라진 숨소리로 그가 카튼을 쳐다보았을 때, 카튼은 다시 가슴에 손을 넣고 그를 빤히 바라보았다.", "en": "As he looked at Carton with clouded eyes and with an altered manner of breathing, Carton—his hand again in his breast—looked steadily at him."},
"P063_1": {"ko": "'만약 그렇지 않았다면;' 카튼의 손이 다시 조심스럽고 부드럽게 내려오고 있었다. '저는 결코 더 긴 기회를 사용하지 않았을 것입니다.", "en": "'If it had been otherwise;' Carton's hand was again watchfully and softly stealing down; 'I never should have used the longer opportunity."},
"P063_2": {"ko": "만약 그렇지 않았다면;' 그 손은 죄수의 얼굴에 닿았다. '저는 훨씬 더 많은 것에 책임져야 했을 것입니다.", "en": "If it had been otherwise;' the hand was at the prisoner's face; 'I should but have had so much the more to answer for."},
"P063_3": {"ko": "만약 그렇지 않았다면--' 카튼이 펜을 보니 그것이 알아볼 수 없는 기호들로 꼬리를 감추고 있는 것을 보았다.", "en": "If it had been otherwise—' Carton looked at the pen and saw it was trailing off into unintelligible signs."},
"P064_1": {"ko": "카튼의 손은 더 이상 가슴으로 돌아가지 않았다.", "en": "Carton's hand moved back to his breast no more."},
"P064_2": {"ko": "죄수는 원망스러운 눈빛으로 벌떡 일어났으나, 카튼의 손은 그의 콧구멍에 바짝 밀착되어 있었고, 카튼의 왼팔은 그의 허리를 감쌌다.", "en": "The prisoner sprang up with a reproachful look, but Carton's hand was close and firm at his nostrils, and Carton's left arm caught him round the waist."},
"P064_3": {"ko": "몇 초 동안 그는 자신을 위해 목숨을 바치러 온 남자와 희미하게 실랑이를 벌였지만, 채 1분도 안 되어 의식을 잃고 바닥에 뻗어버렸다.", "en": "For a few seconds he faintly struggled with the man who had come to lay down his life for him; but, within a minute or so, he was stretched insensible on the ground."},
"P065_1": {"ko": "신속하게, 하지만 그의 마음만큼이나 목적에 충실한 손놀림으로 카튼은 죄수가 벗어둔 옷을 입고, 머리를 뒤로 빗어 죄수가 묶었던 리본으로 묶었다.", "en": "Quickly, but with hands as true to the purpose as his heart was, Carton dressed himself in the clothes the prisoner had laid aside, combed back his hair, and tied it with the ribbon the prisoner had worn."},
"P065_2": {"ko": "그런 다음 그가 부드럽게 불렀다. '안으로 들어오시오!", "en": "Then, he softly called, 'Enter there!"},
"P065_3": {"ko": "들어와요!' 그러자 그 스파이(Spy)가 모습을 드러냈다.", "en": "Come in!' and the Spy presented himself."},
"P068_1": {"ko": "'두려워하지 마시오.", "en": "'Don't fear me."},
"P068_2": {"ko": "죽을 때까지 신의를 지키겠소.'", "en": "I will be true to the death.'"},
"P069_3": {"ko": "당신이 그 옷을 입고 제대로 일을 처리해 준다면, 두려울 게 없소.'", "en": "Being made right by you in that dress, I shall have no fear.'"},
"P070_1": {"ko": "'두려워하지 마시오!", "en": "'Have no fear!"},
"P070_2": {"ko": "난 곧 당신에게 해를 끼칠 수 없는 곳으로 떠날 것이고, 다른 사람들도 곧 여기서 멀리 벗어날 것이오. 신이여, 제발!", "en": "I shall soon be out of the way of harming you, and the rest will soon be far from here, please God!"},
"P070_3": {"ko": "자, 도움을 청해서 나를 마차로 데려가시오.'", "en": "Now, get assistance and take me to the coach.'"},
"P072_1": {"ko": "'이 사람이오, 내가 역할을 바꾼 사람 말이오.", "en": "'Him, man, with whom I have exchanged."},
"P072_2": {"ko": "당신이 나를 데리고 들어왔던 그 문으로 나갈 거요?'", "en": "You go out at the gate by which you brought me in?'"}
}

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_13.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
for block in data:
    if block.get('tag') in data_dict:
        block['ko'] = data_dict[block['tag']]['ko']
        block['en'] = data_dict[block['tag']]['en']
        count += 1

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Patched {count} blocks")
