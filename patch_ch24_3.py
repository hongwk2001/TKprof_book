import json
file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_24.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

patches = {
    'P027_4': {
        'ko': '완전히 고갈되어 하늘과 땅은 물론 스스로까지 마모시켜버린 상황(state of things)을 되돌리려는 Monseigneur의 터무니없는 음모와 결합된 그러한 허세(vapouring)는, 진실을 아는 제정신인 사람이라면 누구라도 항의하지 않고는 견디기 힘든 것이었습니다.',
        'en': 'Such blustering, combined with the extravagant plots of Monseigneur to restore a state of affairs that had utterly exhausted itself and worn out both Heaven and earth as well as itself, was hard for any sane man who knew the truth to endure without making some protest.'
    },
    'P027_5': {
        'ko': '그리고 자신의 머릿속 피가 골치 아프게 요동치는 것처럼 그의 귓가에서 울려 퍼지는 그 허세가, 잠재적인 불안감에 더해져 Charles Darnay를 이미 몹시 불안하게 만들었고, 그를 여전히 불안한 상태로(kept him so) 몰아넣었습니다.',
        'en': 'And it was such empty boasting all around his ears, like a troublesome confusion of blood in his own head, added to a latent uneasiness in his mind, which had already made Charles Darnay restless and continued to keep him so.'
    },
    'P028_1': {
        'ko': '이야기를 나누는 사람들 중에는 킹스 벤치 법정(King\'s Bench Bar) 소속으로 국가 고위직으로의 승진을 향해 탄탄대로를 달리고 있던 Stryver도 있었고, 그래서 그는 이 주제에 대해 목소리를 높였습니다:',
        'en': "Among those talking was Stryver, of the King's Bench Bar, well on his way to state promotion, and therefore loud on the topic:"
    },
    'P028_2': {
        'ko': 'Monseigneur에게 다가가 민중을 날려버리고 지상에서 몰살시킨 다음(exterminating them from the face of the earth) 그들 없이 살아가는 자신만의 계책을 꺼내놓기도 했습니다:',
        'en': 'suggesting to Monseigneur his schemes for blowing the people up, exterminating them from the face of the earth, and living without them:'
    },
    'P028_3': {
        'ko': '그리고 종족의 꼬리에 소금을 뿌려 독수리를 멸종시킨다는 것(abolition of eagles)과 본질적으로 유사한 여러 목표를 달성하기 위한 방법도 제시했습니다.',
        'en': 'and for accomplishing many similar goals that were in their nature comparable to eliminating eagles by sprinkling salt on their tails.'
    },
    'P028_5': {
        'ko': '그리고 Darnay가 더 이상 듣지 않으려고 자리를 뜰지, 아니면 남아서 한마디 거들지(interpose his word) 사이에서 망설이고 있을 때, 장차 일어날 일이 스스로 그 윤곽을 드러내기 시작했습니다(went on to shape itself out).',
        'en': 'and Darnay stood torn between walking away so he might hear no more, and staying to interpose a word, when the thing that was destined to happen began to take shape.'
    },
    'P029_2': {
        'ko': 'Lorry 씨에게 때 묻고 개봉하지 않은 편지를 내밀며, 편지의 수신인을 찾을 만한 실마리(traces)를 발견했는지 물었습니다.',
        'en': 'Lorry, and placing a soiled and unopened letter before him, asked if he had yet found any trace of the person it was addressed to.'
    },
    'P029_3': {
        'ko': '런던 본점은 그 편지를 Darnay의 아주 가까운 곳에 내려놓았고, 그래서 그는 발신인(direction)을 쉽게 볼 수 있었습니다. 그것이 그의 진짜 이름이었기 때문에(his own right name) 더욱 빨리 알아볼 수 있었습니다.',
        'en': 'The House laid the letter down so close to Darnay that he could see the address—and saw it all the more quickly because it was his own true name.'
    },
    'P031_1': {
        'ko': '결혼식 아침에, Doctor Manette는 이 이름의 비밀은—자신이, 즉 그 의사가 그 의무를 면제해주지 않는 한—그들 사이에서 절대 침해되지 않고(kept inviolate) 지켜져야 한다고 Charles Darnay에게 유일하고 간곡하게 요구했었습니다.',
        'en': 'On the morning of his marriage, Doctor Manette had made it his one urgent and explicit request to Charles Darnay that the secret of this name should be kept strictly inviolate between them, unless he, the Doctor, released him from the obligation.'
    },
    'P032_3': {
        'ko': '"아마 지금 여기 있는 모든 분께 여쭤봤을 텐데, 이 신사가 어디 있는지 아시는 분이 아무도 없군요."',
        'en': '"I think I have asked everyone here now, and no one can tell me where this gentleman is to be found."'
    },
    'P033_1': {
        'ko': '시곗바늘이 은행 문을 닫을 시간을 향해 가면서(verging upon), 이야기하던 사람들이 전반적으로 Lorry 씨 곁을 지나가려는 분위기(general set of the current)가 형성되었습니다.',
        'en': "As the hands of the clock neared the Bank's closing hour, there was a general movement of the talkers past Mr."
    },
    'P033_6': {
        'ko': '그리고 이 사람, 저 사람, 또 다른 사람 모두 불어로든 영어로든 행방불명된 그 후작에 대해 헐뜯는 말(something disparaging)을 한마디씩 보탰습니다.',
        'en': 'and This person, That person, and The Other all had something disparaging to say, in French or in English, about the Marquis who could not be found.'
    },
    'P034_1': {
        'ko': '"제 생각엔 조카이거나—어쨌든 퇴보한 후계자(degenerate successor)이겠지—살해당한 그 우아한 후작의 말이야." 한 사람이 말했습니다. "다행히도 난 그자를 모른다네."',
        'en': '"A nephew, I believe—but in any case a degenerate successor—of the polished Marquis who was murdered," said one. "I am happy to say I never knew him."'
    },
    'P035_1': {
        'ko': '"자신의 자리를 버린 겁쟁이(craven)," 다른 이가 말했습니다—수년 전 건초 더미 속에 다리를 위로 하고 반쯤 질식한 채 파리를 빠져나왔던 바로 그 Monseigneur였습니다.',
        'en': '"A coward who abandoned his post," said another—this Monseigneur had been smuggled out of Paris a few years ago, legs pointing up and half suffocated in a load of hay.'
    },
    'P036_2': {
        'ko': '"전임 후작과 반대편에 서서(set himself in opposition), 영지를 상속받자마자 그것을 버려두고 악당 무리(ruffian herd)의 손에 넘겨버렸지.',
        'en': '"He set himself in opposition to the late Marquis, abandoned the estates when he inherited them, and left them to the ruffian mob.'
    },
    'P044_4': {
        'ko': '여기 여태껏 알려진 가장 해롭고(pestilent) 신성 모독적인 악마주의 규범에 감염되어(infected), 사상 유례없는 대규모 살인(murder by wholesale)을 저지르는 세상에서 가장 비열한 찌꺼기 같은 놈들에게 자기 재산을 버려둔 녀석이 있습니다. 그런데 청년들을 가르치는 사람이 그런 자를 알고 있다는 것에 내가 왜 유감스러워하는지 묻는 겁니까?',
        'en': 'Here is a fellow who, infected by the most pestilential and blasphemous code of devilry ever known, abandoned his property to the vilest scum of the earth that ever committed wholesale murder, and you ask me why I am sorry that someone who instructs youth knows him?'
    },
    'P046_5': {
        'ko': '내 생각도 그에게 전해주시지요. 이 잔인한 폭도들(butcherly mob)에게 세상의 재산과 지위를 넘겨주었으니, 차라리 그자들의 우두머리(at the head of them)가 되어있지 않은 것이 의아할 지경이라고.',
        'en': "You may also tell him, from me, that after abandoning his worldly goods and position to this butcher-like mob, I'm surprised he isn't leading them."
    },
    'P046_6': {
        'ko': '하지만 안 그럴 겁니다, 여러분," Stryver가 사방을 둘러보고 손가락을 튕기며(snapping his fingers) 말했습니다. "내가 인간 본성을 좀 아는데, 이런 귀중한 보호 대상자들(precious protégés)의 자비에 제 목숨을 맡기는 녀석은 절대 찾아볼 수 없을 거라 단언합니다.',
        'en': 'But no, gentlemen," said Stryver, looking around and snapping his fingers, "I know something of human nature, and I tell you that you\'ll never find a fellow like this one trusting his life to the mercies of such precious protégés.'
    },
    'P050_1': {
        'ko': '"우리가 그것을 전달할 곳을 알지도 모른다는 희망에 이곳으로 보내진 것 같고(addressed here, on the chance of), 그래서 여기에 얼마간 보관되어 있었다는 점을 당신이 맡아서 설명해주시겠습니까?"',
        'en': '"Will you undertake to explain that we suppose it was sent here on the chance that we might know where to forward it, and that it has been here for some time?"'
    },
    'P054_1': {
        'ko': '자기 자신에게, 그리고 Stryver와 대부분의 다른 사람들에게 매우 불편한 감정을 느끼며(Very ill at ease), Darnay는 최선을 다해 인파를 헤치고 조용한 템플 지역으로 가서 편지를 열고 읽어 보았습니다.',
        'en': 'Very ill at ease with himself, and with Stryver and most other men, Darnay made his way as best he could to the quiet of the Temple, opened the letter, and read it.'
    },
    'P057_1': {
        'ko': '"마을 사람들에 의해 제 목숨이 오랫동안 위험에 처해 있던 끝에, 저는 극심한 폭력과 수모(great violence and indignity)를 당하며 사로잡혀서, 파리까지 멀고도 험한 길을 걸어서 끌려왔습니다.',
        'en': '"After my life was long in danger at the hands of the village, I was seized with great violence and indignity, and forced on a long journey on foot to Paris.'
    },
    'P058_1': {
        'ko': '"전(前) 후작 나리(Monsieur heretofore the Marquis), 제가 투옥된 죄목은, 그리고 제가 재판에 소환되어 (나리의 그토록 관대한 도움이 없다면) 목숨을 잃게 될(lose my life) 그 죄목은, 사람들이 제게 말하기를, 제가 망명자를 위해 그들에 대항해 행동했으므로(acted against them for an emigrant) 인민의 존엄에 반하는 반역죄라는 것입니다.',
        'en': '"The crime for which I am imprisoned, Monsieur heretofore the Marquis, and for which I shall be summoned before the tribunal and will lose my life (without your generous help), is, they tell me, treason against the majesty of the people, because I acted against them on behalf of an emigrant.'
    },
    'P058_3': {
        'ko': '망명자의 재산이 몰수되기 전에(sequestration of emigrant property), 사람들이 내기를 중단했던 세금을 제가 송금(remitted the imposts)했다고 해명해도 아무 소용이 없습니다;',
        'en': 'It is in vain that I represent that before the confiscation of emigrant property, I had sent back the taxes they had ceased to pay;'
    },
    'P059_5': {
        'ko': '아 전(前) 후작 나리, 파리에 널리 알려진 틸슨 대은행(great bank of Tilson)을 통하면 혹시 나리의 귀에 가닿을까 바라는 마음으로 이 바다 건너까지 저의 처절한 외침(desolate cry)을 보냅니다!',
        'en': 'Ah Monsieur heretofore the Marquis, I send my desolate cry across the sea, hoping it might perhaps reach your ears through the great bank of Tilson known in Paris!'
    },
    'P060_1': {
        'ko': '"하늘과 정의, 관용, 그리고 나리의 고귀한 가문의 명예를 향한 사랑을 걸고, 전(前) 후작 나리, 저를 구원하고 풀어주시기를(succour and release me) 간청합니다.',
        'en': '"For the love of Heaven, of justice, of generosity, and of the honor of your noble name, I beg you, Monsieur heretofore the Marquis, to help and release me.'
    },
    'P061_1': {
        'ko': '"매시간 점점 더 죽음에 가까워지고 있는(tend nearer and nearer to destruction) 이 공포의 감옥에서, 전(前) 후작 나리께 슬프고도 불행한 저의 봉사를 바칠 것을 확언합니다(assurance of my dolorous and unhappy service).',
        'en': '"From this prison of horror, where I draw nearer and nearer to destruction every hour, I send you, Monsieur heretofore the Marquis, the assurance of my sorrowful and unhappy service.'
    },
    'P064_2': {
        'ko': '자신과 가문에 충실했다는 것(fidelity to himself and his family)이 유일한 죄인 착하고 늙은 하인의 위험이 너무나 원망스럽게 그의 얼굴을 노려보았기에(stared him so reproachfully in the face), 그는 템플 지역을 이리저리 거닐며 어떻게 해야 할지 고민하는 동안 행인들로부터 자기 얼굴을 거의 숨기다시피 했습니다.',
        'en': 'The peril of an old and good servant, whose only crime was his loyalty to himself and his family, stared him so reproachfully in the face that, as he walked back and forth in the Temple considering what to do, he almost hid his face from the passersby.'
    },
    'P065_1': {
        'ko': '그는 오래된 가문이 저지른 악행과 악명이 정점에 달했던(culminated) 그 일에 대한 끔찍함 속에서, 삼촌을 향한 분개하는 의심 속에서, 그리고 자신이 유지해야 한다고 여겨졌던 그 무너져가는 체제(crumbling fabric)를 그의 양심이 바라보던 혐오감 속에서, 자신이 불완전하게 행동했음을 잘 알고 있었습니다.',
        'en': 'He knew very well that in his horror at the deed that had been the climax of the bad deeds and bad reputation of his old family house, in his resentful suspicions of his uncle, and in the disgust with which his conscience viewed the crumbling structure he was supposed to support, he had acted imperfectly.'
    },
    'P065_2': {
        'ko': '그는 Lucie에 대한 사랑 때문에, 자신의 사회적 지위를 포기한 일(renunciation of his social place)이 결코 마음속에 새로웠던 것은 아니었지만, 성급하고 불완전하게(hurried and incomplete) 이루어졌음을 잘 알고 있었습니다.',
        'en': 'He knew very well that out of his love for Lucie, his renunciation of his social position, though by no means a new idea to him, had been rushed and left incomplete.'
    },
    'P065_3': {
        'ko': '그는 그것을 체계적으로 해결하고 감독(systematically worked it out and supervised it)했어야 했다는 것을 알았고, 그렇게 할 의도였으나 결국 한 번도 실행되지 않았음(never been done)을 알고 있었습니다.',
        'en': 'He knew that he should have systematically worked it out and supervised it, and that he had intended to do so, but that it had never been done.'
    }
}
count = 0
for item in data:
    if item.get('tag') in patches:
        item['ko'] = patches[item['tag']]['ko']
        item['en'] = patches[item['tag']]['en']
        count += 1
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f'Patched {count} items.')
