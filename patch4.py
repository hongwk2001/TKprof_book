import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_04.json', encoding='utf-8') as f:
    d = json.load(f)

fixes = {
  'P068_4': {'ko': '방금 말씀드렸듯이--”', 'en': 'As I was saying--”'},
  'P069_1': {'ko': '그녀의 표정이 그를 너무나 당황하게 만들었기에, 그는 말을 멈추고 주춤거리다 다시 시작했다:', 'en': 'Her look so discomposed him that he stopped, wandered, and began anew:'},
  'P070_1': {'ko': '“제가 말씀드렸듯이;', 'en': '“As I was saying;'},
  'P070_2': {'ko': '만약 Manette 씨가 돌아가시지 않았다면;', 'en': 'if Monsieur Manette had not died;'},
  'P070_3': {'ko': '만약 그가 갑자기 조용히 사라졌다면;', 'en': 'if he had suddenly and silently disappeared;'},
  'P070_4': {'ko': '만약 그가 쥐도 새도 모르게 끌려갔다면;', 'en': 'if he had been spirited away;'},
  'P070_5': {'ko': '어떤 기술로도 그를 추적할 수는 없지만, 그가 어떤 끔찍한 곳으로 갔을지 짐작하기 어렵지 않았다면;', 'en': 'if it had not been difficult to guess to what dreadful place, though no art could trace him;'},
  'P070_6': {'ko': '만약 그에게 어떤 동포 원수가 있어서, 제가 살던 시절 바다 건너 저곳에서 가장 대담한 사람들조차 속삭이듯 말하기를 두려워했던 특권을 행사할 수 있었다면;', 'en': 'if he had an enemy in some compatriot who could exercise a privilege that I in my own time have known the boldest people afraid to speak of in a whisper, across the water there;'},
  'P070_7': {'ko': '예를 들어, 누구든 원하는 기간 동안 감옥의 망각 속에 가두어 버릴 수 있는 백지 영장에 서명할 특권 말입니다;', 'en': 'for instance, the privilege of filling up blank forms for the consignment of any one to the oblivion of a prison for any length of time;'},
  'P070_8': {'ko': '만약 그의 아내가 왕비, 왕, 궁정, 성직자들에게 그의 소식이라도 알려달라고 애원했지만 모두 헛수고였다면;--그렇다면 아가씨 아버님의 이야기는 바로 이 불행한 신사, Beauvais의 의사 이야기였을 것입니다.”', 'en': 'if his wife had implored the king, the queen, the court, the clergy, for any tidings of him, and all quite in vain;--then the history of your father would have been the history of this unfortunate gentleman, the Doctor of Beauvais.”'},
  'P071_1': {'ko': '“더 말씀해 주시기를 간청합니다, 선생님.”', 'en': '“I entreat you to tell me more, sir.”'},
  'P072_1': {'ko': '“그러겠습니다.', 'en': '“I will.'},
  'P072_2': {'ko': '그러려던 참입니다.', 'en': 'I am going to.'},
  'P072_3': {'ko': '견뎌내실 수 있겠습니까?”', 'en': 'You can bear it?”'},
  'P073_1': {'ko': '“지금 이 순간 선생님이 제게 남겨주신 불확실성만 아니라면 무엇이든 견딜 수 있습니다.”', 'en': '“I can bear anything but the uncertainty you leave me in at this moment.”'},
  'P074_1': {'ko': '“차분하게 말씀하시는군요, 그리고 아가씨는--차분하십니다.', 'en': '“You speak collectedly, and you--_are_ collected.'},
  'P074_2': {'ko': '다행입니다!” (비록 그의 태도는 그의 말만큼 흡족해 보이지 않았지만.) “사업상의 문제입니다.', 'en': 'That’s good!” (Though his manner was less satisfied than his words.) “A matter of business.'},
  'P074_3': {'ko': '이것을 사업상의 문제--반드시 해내야 할 일로 여기십시오.', 'en': 'Regard it as a matter of business--business that must be done.'},
  'P074_4': {'ko': '이제 만약 이 의사의 아내가, 비록 대단한 용기와 기개를 지닌 숙녀였지만, 이 일로 인해 어린아이가 태어나기도 전에 너무나 극심한 고통을 겪었다면--”', 'en': 'Now if this doctor’s wife, though a lady of great courage and spirit, had suffered so intensely from this cause before her little child was born--”'},
  'P075_1': {'ko': '“그 어린아이는 딸이었습니다, 선생님.”', 'en': '“The little child was a daughter, sir.”'},
  'P076_1': {'ko': '“딸이었죠.', 'en': '“A daughter.'},
  'P076_2': {'ko': '사-사-사업상의 문제입니다--괴로워하지 마십시오.', 'en': 'A-a-matter of business--don’t be distressed.'},
  'P076_3': {'ko': '아가씨, 만약 그 불쌍한 숙녀가 아이가 태어나기도 전에 너무나 극심한 고통을 겪은 나머지, 아이의 아버지가 죽었다고 믿게 키움으로써 자신이 겪은 고통의 그 어떤 부분도 불쌍한 아이에게 물려주지 않기로 결심했다면--아, 무릎 꿇지 마십시오!', 'en': 'Miss, if the poor lady had suffered so intensely before her little child was born, that she came to the determination of sparing the poor child the inheritance of any part of the agony she had known the pains of, by rearing her in the belief that her father was dead--No, don’t kneel!'},
  'P076_4': {'ko': '제발 제게 왜 무릎을 꿇으십니까!”', 'en': 'In Heaven’s name why should you kneel to me!”'},
  'P077_1': {'ko': '“진실을 위해서요.', 'en': '“For the truth.'},
  'P077_2': {'ko': '오, 친절하고 다정하고 자애로우신 선생님, 진실을 위해서요!”', 'en': 'O dear, good, compassionate sir, for the truth!”'},
  'P078_1': {'ko': '“사--사업상의 문제입니다.', 'en': '“A--a matter of business.'},
  'P078_2': {'ko': '절 혼란스럽게 하시는군요, 제가 혼란스러우면 어떻게 사업을 처리하겠습니까?', 'en': 'You confuse me, and how can I transact business if I am confused?'},
  'P078_3': {'ko': '머리를 맑게 합시다.', 'en': 'Let us be clear-headed.'},
  'P078_4': {'ko': '예를 들어, 9곱하기 9펜스가 얼마인지, 20기니가 몇 실링인지 지금 친절하게 말씀해 주신다면 큰 격려가 될 겁니다.', 'en': 'If you could kindly mention now, for instance, what nine times ninepence are, or how many shillings in twenty guineas, it would be so encouraging.'},
  'P078_5': {'ko': '그러면 아가씨의 심리 상태에 대해 훨씬 더 안심할 수 있을 텐데요.”', 'en': 'I should be so much more at my ease about your state of mind.”'},
  'P079_1': {'ko': '이 호소에 직접 대답하는 대신, 그가 매우 부드럽게 일으켜 세웠을 때 그녀는 너무나 조용히 앉아 있었고, 그의 손목을 꽉 쥔 채 놓지 않던 손도 전보다 훨씬 안정되어 있어서, 그 모습은 Mr.', 'en': 'Without directly answering to this appeal, she sat so still when he had very gently raised her, and the hands that had not ceased to clasp his wrists were so much more steady than they had been, that she communicated some reassurance to Mr.'},
  'P079_2': {'ko': 'Jarvis Lorry에게 어느 정도 안도감을 전해주었다.', 'en': 'Jarvis Lorry.'},
  'P080_1': {'ko': '“좋습니다, 좋아요.', 'en': '“That’s right, that’s right.'},
  'P080_2': {'ko': '용기를 내세요!', 'en': 'Courage!'},
  'P080_3': {'ko': '사업입니다!', 'en': 'Business!'},
  'P080_4': {'ko': '아가씨 앞에는 사업이,', 'en': 'You have business before you;'},
  'P080_5': {'ko': '유익한 사업이 있습니다.', 'en': 'useful business.'},
  'P080_6': {'ko': 'Manette 양, 아가씨의 어머님은 아가씨를 위해 이런 길을 택하셨습니다.', 'en': 'Miss Manette, your mother took this course with you.'},
  'P080_7': {'ko': '그리고 어머님께서 돌아가셨을 때--가슴이 찢어지는 고통 속에서 돌아가셨을 거라 믿습니다--아버님을 찾는 헛된 노력을 결코 늦추지 않으셨던 어머님은, 아버님이 감옥에서 애타게 그리워하다 곧 돌아가셨는지 아니면 길고 긴 세월 동안 그곳에서 쇠약해지셨는지 모르는 불확실성 속에서 살아가는 암운을 아가씨에게 씌우지 않기 위해, 두 살배기 아가씨를 남겨두고 아가씨가 생기 넘치고 아름답고 행복하게 자라도록 하셨습니다.”', 'en': 'And when she died--I believe broken-hearted--having never slackened her unavailing search for your father, she left you, at two years old, to grow to be blooming, beautiful, and happy, without the dark cloud upon you of living in uncertainty whether your father soon wore his heart out in prison, or wasted there through many lingering years.”'},
  'P081_1': {'ko': '그 말을 하며 그는 경이로움이 섞인 연민의 눈길로 흘러내리는 금발을 내려다보았다;', 'en': 'As he said the words he looked down, with an admiring pity, on the flowing golden hair;'},
  'P081_2': {'ko': '마치 그 머리칼이 이미 회색으로 물들었을지도 모른다고 상상이나 하듯.', 'en': 'as if he pictured to himself that it might have been already tinged with grey.'},
  'P082_1': {'ko': '“부모님께서 큰 재산을 갖지 못하셨고, 그나마 있던 것도 어머님과 아가씨에게 안전하게 물려졌다는 것은 아실 겁니다.', 'en': '“You know that your parents had no great possession, and that what they had was secured to your mother and to you.'},
  'P082_2': {'ko': '돈이나 다른 재산이 새로 발견된 것은 아닙니다;', 'en': 'There has been no new discovery, of money, or of any other property;'},
  'P082_3': {'ko': '하지만--”', 'en': 'but--”'},
  'P083_1': {'ko': '그는 자신의 손목이 더 꽉 쥐어지는 것을 느끼고 말을 멈췄다.', 'en': 'He felt his wrist held closer, and he stopped.'},
  'P083_2': {'ko': '그의 주의를 몹시도 끌었던, 이제는 미동도 없는 그 이마의 표정은 고통과 공포의 표정으로 깊어져 있었다.', 'en': 'The expression in the forehead, which had so particularly attracted his notice, and which was now immovable, had deepened into one of pain and horror.'},
  'P084_1': {'ko': '“하지만 아버님이--발견되었습니다.', 'en': '“But he has been--been found.'},
  'P084_2': {'ko': '살아 계십니다.', 'en': 'He is alive.'},
  'P084_3': {'ko': '크게 변하셨을 가능성이 아주 큽니다;', 'en': 'Greatly changed, it is too probable;'},
  'P084_4': {'ko': '거의 폐인이 되셨을 수도 있고요;', 'en': 'almost a wreck, it is possible;'},
  'P084_5': {'ko': '물론 우리는 최선을 희망할 테지만요.', 'en': 'though we will hope the best.'},
  'P084_6': {'ko': '어쨌든, 살아 계십니다.', 'en': 'Still, alive.'},
  'P084_7': {'ko': '아버님은 파리의 옛 하인 집으로 모셔졌고, 우리는 지금 그곳으로 가는 길입니다:', 'en': 'Your father has been taken to the house of an old servant in Paris, and we are going there:'},
  'P084_8': {'ko': '저는, 할 수 있다면 그분이 맞는지 확인하기 위해 가고:', 'en': 'I, to identify him if I can:'},
  'P084_9': {'ko': '아가씨는, 그분에게 삶, 사랑, 의무, 안식, 위안을 되찾아 드리기 위해 가는 겁니다.”', 'en': 'you, to restore him to life, love, duty, rest, comfort.”'},
  'P085_1': {'ko': '그녀의 온몸에 전율이 일었고, 그 떨림은 그녀를 통해 그에게로 전해졌다.', 'en': 'A shiver ran through her frame, and from it through his.'},
  'P085_2': {'ko': '그녀는 마치 꿈속에서 말하듯 낮고 또렷하며 경외심에 찬 목소리로 말했다.', 'en': 'She said, in a low, distinct, awe-stricken voice, as if she were saying it in a dream,'},
  'P086_1': {'ko': '“제가 그분의 유령을 보러 가는 거군요!', 'en': '“I am going to see his Ghost!'},
  'P086_2': {'ko': '그분이 아니라 유령일 거예요!”', 'en': 'It will be his Ghost--not him!”'},
  'P087_1': {'ko': 'Mr.', 'en': 'Mr.'},
  'P087_2': {'ko': 'Lorry 씨는 자기 팔을 잡고 있는 그녀의 손을 조용히 문질렀다. “자, 자, 자!', 'en': 'Lorry quietly chafed the hands that held his arm. “There, there, there!'},
  'P087_3': {'ko': '이제 보세요, 이제 보세요!', 'en': 'See now, see now!'},
  'P087_4': {'ko': '이제 최선의 상황과 최악의 상황을 모두 아시지 않습니까.', 'en': 'The best and the worst are known to you, now.'},
  'P087_5': {'ko': '아가씨는 억울한 일을 당한 그 가엾은 신사에게 가는 길을 순조롭게 가고 계시며, 순탄한 바다 여행과 육로 여행을 거치면 곧 그의 사랑스러운 곁에 있게 되실 겁니다.”', 'en': 'You are well on your way to the poor wronged gentleman, and, with a fair sea voyage, and a fair land journey, you will be soon at his dear side.”'},
  'P088_1': {'ko': '그녀는 속삭임으로 잦아든 같은 어조로 반복했다. “나는 자유로웠고, 행복했는데, 그분의 유령은 단 한 번도 나를 찾아오지 않았어!”', 'en': 'She repeated in the same tone, sunk to a whisper, “I have been free, I have been happy, yet his Ghost has never haunted me!”'},
  'P089_1': {'ko': '“딱 한 가지만 더 말씀드리죠,” Mr.', 'en': '“Only one thing more,” said Mr.'},
  'P089_2': {'ko': 'Lorry 씨가 그녀의 주의를 끌기 위한 건전한 방법으로 강조하며 말했다:', 'en': 'Lorry, laying stress upon it as a wholesome means of enforcing her attention:'},
  'P089_3': {'ko': '“아버님은 다른 이름으로 발견되셨습니다;', 'en': '“he has been found under another name;'},
  'P089_4': {'ko': '자신의 본명은 오래전에 잊혔거나 숨겨진 채로요.”', 'en': 'his own, long forgotten or long concealed.'}
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
