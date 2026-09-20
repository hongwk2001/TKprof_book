import json
file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_24.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

patches = {
    'P066_1': {
        'ko': '자신이 선택한 영국 가정의 행복, 항상 바쁘게 일해야만 했던 필요성(necessity of being always actively employed), 그리고 너무나 빨리 잇달아 일어나 이번 주의 사건이 지난주의 미숙한 계획을 무산시키고 다음 주의 사건이 모든 것을 다시 원점으로 돌려놓았던 시대의 빠르고 어지러운 변화들;',
        'en': 'The happiness of his chosen English home, the necessity of always being actively employed, and the swift changes and troubles of the times that followed one another so quickly that the events of this week wiped out the immature plans of last week, and the events of the following week made everything new again;'
    },
    'P066_2': {
        'ko': '그는 자신이 이러한 환경의 힘에 굴복했음을(yielded) 잘 알고 있었습니다:--불안감이 없었던 것은 아니지만, 그래도 지속적으로 쌓여가는 저항 없이 말입니다.',
        'en': 'he knew very well that he had yielded to the force of these circumstances:—not without unease, but still without continuous and mounting resistance.'
    },
    'P066_3': {
        'ko': '그가 행동에 나설 시기를 엿보았으나(watched the times for a time of action) 그 기회들이 엇갈리고 얽매이다가 결국 시기를 놓쳐버렸고, 귀족들이 프랑스의 모든 큰길과 샛길을 통해 무리 지어 도망치고 있으며, 그들의 재산이 몰수되고 파괴되는 중이고, 그들의 이름조차 지워지고 있다는 사실은, 그를 탄핵할지도 모르는 프랑스의 어떤 새로운 권력자 못지않게 그 자신도 잘 알고 있었습니다.',
        'en': 'That he had waited for a time to act, and that circumstances had shifted and struggled until the time had passed, and the nobility were fleeing France by every highway and byway, their property in the process of confiscation and destruction, and their very names being wiped out, was as well known to him as it could be to any new authority in France that might prosecute him for it.'
    },
    'P067_2': {
        'ko': '그는 가혹하게 세금 납부를 요구한 적이 없을 뿐만 아니라, 오히려 자발적으로 그것을 포기했고(relinquished them of his own will), 아무런 호의도 없는 세상에 몸을 던져 그곳에서 자신만의 자리를 잡고 스스로 생계를 꾸려왔습니다(earned his own bread).',
        'en': 'he was so far from having harshly demanded payment of his dues that he had voluntarily given them up, thrown himself into an unforgiving world, carved out his own private place there, and earned his own living.'
    },
    'P067_3': {
        'ko': 'Gabelle 씨는 문서화된 지시에 따라 그 빈곤하고 복잡하게 얽힌 영지(impoverished and involved estate)를 관리하면서, 사람들을 덜 괴롭히고, 줄 수 있는 것이 적더라도 주려 했으며--까다로운 채권자들이 겨울에 허용하는 만큼의 땔감과 여름에 같은 억압 속에서 건져낼 수 있는 수확물 등을 주려 했고--자신의 안전을 위해 그 사실을 변호하고 입증할 증거(plea and proof)를 남겨두었을 것이 틀림없으므로, 이제 그것이 드러나지 않을 수 없었습니다.',
        'en': 'Monsieur Gabelle had managed the impoverished and entangled estate under written instructions to spare the people, to give them what little there was to give—such fuel as the demanding creditors would allow them in the winter, and such produce as could be saved from the same grasp in the summer—and he had undoubtedly documented this as a plea and proof for his own safety, so that it could not help but come to light now.'
    },
    'P069_2': {
        'ko': '옛이야기 속 선원처럼, 바람과 해류가 그를 천연자석 바위(Loadstone Rock)의 영향권 안으로 몰아넣었고, 그것이 그를 끌어당기고 있었으므로, 그는 가야만 했습니다.',
        'en': 'Like the sailor in the old story, the winds and currents had driven him into the pull of the Loadstone Rock, and it was drawing him toward itself, and he had to go.'
    },
    'P069_3': {
        'ko': '그의 마음속에 떠오른 모든 것들이 그를 점점 더 빠르게, 점점 더 확고하게 그 무시무시한 이끌림(terrible attraction)을 향해 떠밀었습니다.',
        'en': 'Everything that came to his mind propelled him, faster and faster, more and more steadily, toward that terrible attraction.'
    },
    'P069_4': {
        'ko': '그의 잠재적인 불안감(latent uneasiness)은, 자신의 불행한 조국에서 악한 도구들에 의해 악한 목적들이 실행되고 있는데, 자신이 그들보다 낫다는 것을 모를 리 없는 그가 그곳에 가서 유혈 사태를 멈추고 자비와 인류애의 주장을 내세우려(assert the claims of mercy and humanity) 노력하지 않았다는 데 있었습니다.',
        'en': 'His underlying unease had been that wicked aims were being carried out in his own unhappy country by wicked instruments, and that he, who could not fail to know he was better than them, was not there trying to do something to stop the bloodshed and assert the rights of mercy and humanity.'
    },
    'P069_5': {
        'ko': '이 불안감이 반쯤 억눌린 채, 그리고 반쯤 그를 꾸짖는 상태에서, 그는 의무감이 그토록 강한 훌륭한 노신사와 자신을 대조(pointed comparison)해보게 되었습니다;',
        'en': 'With this unease half stifled and half reproaching him, he was brought to squarely compare himself with the brave old gentleman whose sense of duty was so strong;'
    },
    'P069_6': {
        'ko': '그 대조(자신에게 불리한) 직후에는 그를 쓰라리게 찔렀던 Monseigneur의 비웃음과, 무엇보다도 옛날의 이유들(old reasons)로 인해 저속하고 짜증 났던 Stryver의 비웃음이 잇따랐습니다.',
        'en': 'immediately following that comparison (which was unfavorable to himself) came the sneers of Monseigneur, which had stung him bitterly, and those of Stryver, which were especially coarse and irritating for old reasons.'
    },
    'P071_5': {
        'ko': '비록 그가 미완성으로 남겨두긴 했으나(left it incomplete), 그가 했던 행동을 이끈 그 의도는 그가 프랑스에 가서 그 의도를 분명히 밝힌다면 그곳에서 감사히 인정받을(gratefully acknowledged) 만한 모습으로 그의 앞에 떠올랐습니다.',
        'en': 'The intention behind what he had done, even though he had left it incomplete, presented itself to him in a light that would be gratefully acknowledged in France once he presented himself to assert it.'
    },
    'P071_6': {
        'ko': '그러자, 선의를 가진 많은 이들이 흔히 품게 되는 낙관적인 신기루(sanguine mirage)인, 선한 일을 하겠다는 영광스러운 환상이 그의 눈앞에 피어올랐고, 그는 심지어 너무나도 끔찍하게 날뛰고 있는 이 맹렬한 혁명을 자신이 일정한 영향력을 발휘해 인도하는 착각(illusion)에 빠지기도 했습니다.',
        'en': 'Then, that glorious vision of doing good, which is so often the hopeful mirage of many good minds, arose before him, and he even imagined himself in the illusion of having some influence to guide this raging Revolution that was running so frighteningly out of control.'
    },
    'P072_1': {
        'ko': '그는 결심을 굳힌 채 이리저리 거닐면서(walked to and fro), 자신이 떠날 때까지는 Lucie도 그녀의 아버지도 이 일을 알아서는 안 된다고(must know of it) 생각했습니다.',
        'en': 'As he paced back and forth with his decision made, he determined that neither Lucie nor her father must know of it until he was gone.'
    },
    'P072_3': {
        'ko': '그리고 프랑스에 얽힌 위험한 과거의 땅(dangerous ground of old)으로 생각을 돌리기를 늘 꺼렸던 그녀의 아버지도, 불안하고 의심스러운 저울질의 상태가 아니라 이미 취해진 조치(step taken)로서 이 결정을 알게 되어야 한다고 생각했습니다.',
        'en': 'and her father, who was always reluctant to turn his thoughts to the dangerous subject of the past, should learn of the step only after it had been taken, and not while it hung in the balance of suspense and doubt.'
    },
    'P072_4': {
        'ko': '자신의 불완전한 상황이 어느 정도나 그의 아버지 탓인지—마음속에서 프랑스와 관련된 옛 기억들을 되살리는 것(reviving old associations of France)을 피하려는 고통스러운 불안감 때문이었는지—그는 스스로와 논쟁하지 않았습니다.',
        'en': 'How much of the incompleteness of his situation was due to her father, through the painful anxiety to avoid reviving past associations with France in his mind, he did not debate with himself.'
    },
    'P073_1': {
        'ko': '그는 매우 바쁜 생각에 잠겨(thoughts very busy) Tellson 은행으로 돌아가 Lorry 씨에게 작별을 고할 시간이 될 때까지 이리저리 거닐었습니다.',
        'en': "He paced back and forth, his thoughts very active, until it was time to return to Tellson's and take leave of Mr."
    },
    'P073_3': {
        'ko': '파리에 도착하자마자 그는 이 오랜 친구를 찾아갈(present himself) 작정이지만, 지금은 자신의 의도에 대해 아무 말도 해서는 안 되었습니다.',
        'en': 'As soon as he arrived in Paris, he would present himself to this old friend, but he must say nothing of his plans now.'
    },
    'P075_2': {
        'ko': 'Lorry. "당신이 서면으로 된 답장을 맡는 것(charged with any written answer)에는 동의할 수 없지만, 구두로 된 답장이라면 가져가 주시겠습니까?"',
        'en': 'Lorry. "I would not consent to you being burdened with a written answer, but perhaps you will carry a verbal one?"'
    },
    'P086_2': {
        'ko': 'Lorry 씨가 수많은 코트와 망토(coats and cloaks)를 껴입는 것을 도왔고, 오래된 은행의 따뜻한 공기를 벗어나 안개 낀 Fleet-street로 그와 함께 나섰습니다. "Lucie와 어린 Lucie에게 내 사랑을 전해주게," Mr.',
        'en': 'Lorry wrap himself in several coats and cloaks, and went out with him from the warm atmosphere of the old Bank into the misty air of Fleet Street. "My love to Lucie, and to little Lucie," said Mr.'
    },
    'P086_3': {
        'ko': 'Lorry 씨가 헤어질 때 말했습니다. "그리고 내가 돌아올 때까지 그들을 아주 소중히 돌봐주게(take precious care of them)." Charles Darnay는 마차가 굴러갈 때 고개를 저으며 미심쩍은 듯 미소 지었습니다.',
        'en': 'Lorry at parting, "and take precious care of them until I come back." Charles Darnay shook his head and smiled doubtfully as the carriage rolled away.'
    },
    'P087_2': {
        'ko': '하나는 Lucie에게 보내는 것으로, 자신이 파리에 가야만 하는 강력한 의무(strong obligation)를 설명하고, 왜 자신이 그곳에서 어떤 개인적인 위험에도 휘말리지 않을 것이라고 확신하는지 그 이유를 길게 밝힌 것이었습니다;',
        'en': 'one was to Lucie, explaining the strong duty he felt to go to Paris, and detailing the reasons he had for feeling confident that he would not fall into any personal danger there;'
    },
    'P087_3': {
        'ko': '다른 하나는 의사(Doctor)에게 보내는 것으로, Lucie와 그들의 사랑스러운 아이를 그의 보살핌에 맡기며(confiding), 아주 강한 확신을 담아 같은 주제를 거듭 강조한 것이었습니다.',
        'en': 'the other was to the Doctor, entrusting Lucie and their dear child to his care, and dwelling on the same points with the strongest reassurances.'
    },
    'P087_4': {
        'ko': '두 사람 모두에게, 그는 도착 직후 자신의 안전을 증명할 편지를 띄우겠다고(despatch letters in proof of his safety) 썼습니다.',
        'en': 'To both, he wrote that he would send letters proving his safety immediately after his arrival.'
    },
    'P088_1': {
        'ko': '함께하는 그들의 삶에서 처음으로 비밀(first reservation of their joint lives)을 마음에 품은 채 그들 사이에 있어야 했던 그날은 참으로 힘든 하루였습니다.',
        'en': 'It was a difficult day, that day of being among them with the first secret of their shared lives on his mind.'
    },
    'P088_3': {
        'ko': '하지만 무척이나 행복하고 바쁘게 지내는 아내를 애정 어린 눈길로 쳐다보고 나자, 그녀에게 임박한 일(what impended)을 말하지 않기로 결심하게 되었고(그녀의 조용한 도움 없이 무언가를 행동에 옮기는 것이 너무나 낯설어서 반쯤은 말할 뻔하기도 했습니다), 하루는 빠르게 지나갔습니다.',
        'en': 'But an affectionate glance at his wife, so happy and busy, made him resolved not to tell her what was imminent (he had been half tempted to do it, so strange was it for him to act in anything without her quiet support), and the day passed quickly.'
    },
    'P088_4': {
        'ko': '초저녁에 그는 곧 돌아오겠다고 둘러대며 아내와 아내만큼이나 사랑스러운 같은 이름의 딸을 껴안았고(가상의 약속을 핑계로 밖으로 나섰으며, 미리 옷이 든 작은 여행 가방을 숨겨두었습니다), 그렇게 그는 더 무거운 마음(heavier heart)을 안고 짙은 안개가 낀 거리로 나섰습니다.',
        'en': 'Early in the evening he embraced her and her equally dear namesake, pretending that he would return shortly (an imaginary appointment took him out, and he had secretly packed a valise of clothes), and so he stepped out into the heavy mist of the gloomy streets with an even heavier heart.'
    },
    'P089_1': {
        'ko': '이제 보이지 않는 힘(unseen force)이 그를 그곳으로 빠르게 끌어당기고 있었고, 모든 조류와 바람이 그곳을 향해 일직선으로 강하게 불고 있었습니다.',
        'en': 'The unseen force was pulling him swiftly toward itself now, and all the tides and winds were blowing straight and strong toward it.'
    },
    'P089_2': {
        'ko': '그는 믿을 만한 짐꾼(trusty porter)에게 두 통의 편지를 맡기며, 자정 30분 전, 그보다 더 일찍은 말고 딱 그 시간에 배달해 달라고 당부했습니다;',
        'en': 'He left his two letters with a reliable porter, to be delivered exactly half an hour before midnight, and no sooner;'
    },
    'P089_4': {
        'ko': '그리고 여행을 시작했습니다. 이 세상에서 사랑하는 모든 것을 뒤로하고 천연자석 바위(Loadstone Rock)를 향해 떠내려가는 동안, 가라앉는 그의 마음(sinking heart)을 다잡아준 것은 "하늘과 정의, 관용, 그리고 나리의 고귀한 가문의 명예를 향한 사랑을 걸고!"라는 그 가엾은 죄수의 외침이었습니다.',
        'en': 'and began his journey. "For the love of Heaven, of justice, of generosity, of the honor of your noble name!" was the poor prisoner\'s cry that strengthened his sinking heart, as he left everything dear on earth behind him and drifted away toward the Loadstone Rock.'
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
