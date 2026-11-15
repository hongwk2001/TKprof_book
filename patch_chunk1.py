import json

data_dict = {
"P002_1": {"ko": "콩시에르주리의 어두운 감옥에서, 그날 사형을 선고받은 이들이 운명을 기다리고 있었다.", "en": "In the dark prison of the Conciergerie, the doomed of the day awaited their fate."},
"P002_2": {"ko": "그들의 숫자는 일 년의 주(weeks) 수와 같았다.", "en": "Their number was the same as the weeks of the year."},
"P002_3": {"ko": "쉰두 명의 사람들이 그날 오후 도시의 생명의 흐름을 타고 끝없는 영원의 바다로 휩쓸려 갈 예정이었다.", "en": "Fifty-two were to roll that afternoon on the life-tide of the city to the boundless everlasting sea."},
"P002_4": {"ko": "그들이 감방을 비우기도 전에 새로운 수감자들이 배정되었고, 그들의 피가 어제 흘린 피와 섞이기도 전에 내일 그들의 피와 섞일 피가 이미 따로 마련되어 있었다.", "en": "Before their cells were emptied of them, new occupants were appointed; before their blood ran into the blood spilled yesterday, the blood that was to mingle with theirs tomorrow was already set apart."},
"P003_1": {"ko": "쉰두 명이 선발되었다.", "en": "Two score and twelve were told off."},
"P003_2": {"ko": "자신의 목숨을 살 수 없었던 일흔 살의 징세관(farmer-general)부터, 가난과 무명으로도 목숨을 구할 수 없었던 스무 살의 재봉사에 이르기까지.", "en": "From the seventy-year-old farmer-general whose riches could not buy his life, to the twenty-year-old seamstress whose poverty and obscurity could not save her."},
"P003_3": {"ko": "인간의 악덕과 방치에서 생겨난 육체적 질병이 모든 계층의 희생자를 덮치듯, 말할 수 없는 고통과 참을 수 없는 억압, 무자비한 무관심에서 태어난 끔찍한 도덕적 혼란 역시 차별 없이 그들을 내리쳤다.", "en": "Just as physical diseases, born of human vices and neglect, seize victims of all classes, so the frightful moral disorder, born of unspeakable suffering, intolerable oppression, and heartless indifference, struck equally without distinction."},
"P004_1": {"ko": "감방에 홀로 남은 찰스 다네이(Charles Darnay)는 재판소에서 돌아온 이후 어떠한 헛된 망상으로도 자신을 위로하지 않았다.", "en": "Alone in his cell, Charles Darnay had not comforted himself with any false delusion since returning from the Tribunal."},
"P004_2": {"ko": "자신이 들은 이야기의 모든 구절에서, 그는 자신에 대한 사형 선고를 들었다.", "en": "In every line of the narrative he had heard, he had heard his own condemnation."},
"P004_3": {"ko": "그는 어떤 개인적 영향력으로도 자신을 구할 수 없으며, 사실상 수백만 명에 의해 선고를 받은 것이라 소수의 힘으로는 아무 소용이 없다는 것을 완전히 이해하고 있었다.", "en": "He fully understood that no personal influence could possibly save him, that he was virtually sentenced by millions, and that individuals could do nothing for him."},
"P005_1": {"ko": "그럼에도 불구하고, 사랑하는 아내의 얼굴이 눈앞에 아른거리는 가운데 다가올 운명을 견뎌내도록 마음을 가라앉히는 것은 쉽지 않았다.", "en": "Nevertheless, with the face of his beloved wife fresh in his mind, it was not easy to compose himself for what he must bear."},
"P005_2": {"ko": "삶에 대한 그의 애착은 강렬했고 그것을 놓아버리기는 너무나도 힘들었다. 점차 노력하여 한쪽을 조금 풀면 다른 쪽이 더 꽉 쥐어졌고, 온 힘을 다해 긴장을 풀면 다시 단단히 움켜쥐어졌다.", "en": "His hold on life was strong and very hard to let go; as he made gradual efforts and relaxed a little here, it clenched tighter there; and when he focused his strength to loosen that grip, it closed tightly again."},
"P005_3": {"ko": "그의 모든 생각 속에는 조급함이 있었고, 체념에 맞서 싸우는 요동치고 격양된 마음의 움직임이 있었다.", "en": "There was also a rushed urgency in all his thoughts, and a turbulent, heated stirring of his heart that fought against resignation."},
"P005_4": {"ko": "순간적으로나마 그가 체념을 느꼈을 때도, 그가 떠난 후 살아남아야 할 아내와 아이가 반발하며 그것을 이기적인 행동으로 만드는 것 같았다.", "en": "Even if he felt resigned for a moment, it seemed his wife and child, who had to live on after him, protested and made it feel like a selfish act."},
"P006_1": {"ko": "하지만 이 모든 것은 처음뿐이었다.", "en": "But all this was only at first."},
"P006_2": {"ko": "얼마 지나지 않아, 자신이 맞이해야 할 운명에 아무런 수치가 없으며, 수많은 사람들이 억울하게 같은 길을 가고 또 매일 그 길을 의연하게 걷는다는 생각이 떠올라 그를 격려했다.", "en": "Before long, the thought that there was no shame in the fate he must meet, and that countless others wrongfully walked the same path and bravely trod it every day, sprang up to encourage him."},
"P006_3": {"ko": "다음으로는 사랑하는 이들이 누릴 앞으로의 마음의 평화 중 많은 부분이 자신의 차분한 인내심에 달려 있다는 생각이 이어졌다.", "en": "Next came the thought that much of the future peace of mind his loved ones might enjoy depended on his calm fortitude."},
"P006_4": {"ko": "그리하여 그는 점차 평온을 되찾아 더 나은 상태가 되었고, 생각을 훨씬 더 높은 곳으로 끌어올려 위안을 얻을 수 있었다.", "en": "Thus, he gradually calmed into a better state, where he could raise his thoughts much higher and draw comfort from them."},
"P007_1": {"ko": "그에게 사형이 선고된 밤 어둠이 깔리기 전에, 그는 마지막 길에서 이만큼이나 멀리 여행한 셈이었다.", "en": "Before darkness fell on the night he was sentenced, he had already traveled this far along his final journey."},
"P007_2": {"ko": "글을 쓸 도구와 불빛을 살 수 있도록 허락을 받은 그는 감옥의 램프가 꺼질 때까지 글을 쓰기 위해 자리에 앉았다.", "en": "Having been allowed to buy writing materials and a light, he sat down to write until the prison lamps would be extinguished."},
"P008_1": {"ko": "그는 루시에게 긴 편지를 써서, 그녀에게 직접 듣기 전까지는 장인의 투옥에 대해 전혀 몰랐으며, 그 문서를 읽기 전까지는 장인과 삼촌이 그 불행에 책임이 있다는 사실을 그녀만큼이나 몰랐다고 밝혔다.", "en": "He wrote a long letter to Lucie, explaining that he had known nothing of her father's imprisonment until she told him, and that until he read the paper, he was as ignorant as she that his father and uncle were responsible for that misery."},
"P008_2": {"ko": "자신이 버린 이름을 그녀에게 숨긴 것은 장인이 약혼에 단 하나 내건 조건(이제는 완전히 이해할 수 있는)이었으며, 결혼식 아침에 여전히 요구했던 단 하나의 약속이었다고 이미 그녀에게 설명했었다.", "en": "He had already explained to her that keeping his abandoned name a secret was the only condition—now completely understandable—her father had attached to their betrothal, and it was the single promise he had still insisted upon on the morning of their marriage."},
"P008_3": {"ko": "그는 그녀에게 장인을 위해, 오래전 일요일 정원의 플라타너스 나무 아래에서 런던 탑 이야기를 듣고 장인이 그 문서의 존재를 잊고 있었는지, 아니면 다시 떠올렸는지 결코 알려고 하지 말아 달라고 간청했다.", "en": "He pleaded with her, for her father's sake, never to seek to know whether her father had forgotten the paper's existence, or if the story of the Tower on that old Sunday under the dear plane-tree in the garden had recalled it to him."},
"P008_4": {"ko": "만약 그가 그것을 분명히 기억하고 있었다면, 군중이 바스티유에서 발견하여 온 세상에 알려진 죄수들의 유품 속에서 아무런 언급도 찾지 못했을 때 그것이 바스티유와 함께 파괴되었다고 생각했음이 틀림없었다.", "en": "If he had retained any clear memory of it, there was no doubt he assumed it had been destroyed along with the Bastille, since he found no mention of it among the prisoners' relics discovered by the populace and described to the whole world."},
"P008_5": {"ko": "그는 비록 불필요한 줄 알지만, 아버지가 자책할 만한 일은 아무것도 하지 않았으며 부부를 위해 한결같이 자신을 희생했다는 진실을 모든 다정한 방법을 동원해 일깨워줌으로써 아버지를 위로해달라고 간청했다.", "en": "He besought her—though adding he knew it was needless—to comfort her father by impressing upon him through every tender means possible the truth that he had done nothing for which he could justly reproach himself, but had uniformly forgotten himself for their joint sakes."},
"P008_6": {"ko": "자신의 마지막 사랑과 축복을 간직하고 슬픔을 이겨내 아이에게 헌신해 달라는 당부와 함께, 그는 천국에서 만날 때처럼 아버지를 위로해줄 것을 간절히 부탁했다.", "en": "Next to her preserving his own last grateful love and blessing, and her overcoming her sorrow to devote herself to their dear child, he solemnly adjured her, as they would meet in Heaven, to comfort her father."},
"P009_1": {"ko": "그녀의 아버지에게도 같은 어조로 편지를 썼지만, 아내와 아이를 명시적으로 그의 보살핌에 맡긴다고 말했다.", "en": "He wrote to her father in the same tone, but told him expressly that he confided his wife and child to his care."},
"P009_2": {"ko": "장인이 빠져들 수도 있는 낙담이나 위험한 과거 회상으로부터 그를 일깨우고자 하는 희망에서 매우 강하게 이 사실을 전했다.", "en": "And he stated this very strongly, hoping it would rouse him from any despair or dangerous dwelling on the past toward which he foresaw he might be tending."},
"P010_3": {"ko": "그렇게 감사하는 우정과 따뜻한 애정이 담긴 문장들을 덧붙인 뒤 모든 것이 끝났다.", "en": "That done, with many added sentences of grateful friendship and warm attachment, all was finished."},
"P010_4": {"ko": "그는 카튼에 대해서는 전혀 생각하지 못했다.", "en": "He never thought of Carton."},
"P010_5": {"ko": "그의 마음은 다른 사람들로 너무 가득 차 있어서, 카튼은 단 한 번도 떠올리지 않았다.", "en": "His mind was so full of the others that he never once thought of him."},
"P011_1": {"ko": "그는 불이 꺼지기 전에 이 편지들을 마칠 시간이 있었다.", "en": "He had time to finish these letters before the lights were put out."},
"P011_2": {"ko": "짚으로 된 침대에 누웠을 때, 그는 이 세상과 작별했다고 생각했다.", "en": "When he lay down on his straw bed, he thought he had done with this world."},
"P012_1": {"ko": "하지만 세상은 잠든 그를 다시 불렀고 반짝이는 모습으로 나타났다.", "en": "But the world beckoned him back in his sleep, revealing itself in shining forms."},
"P012_2": {"ko": "자유롭고 행복한 모습으로 소호의 옛집에 돌아온 그는 설명할 수 없을 만큼 홀가분한 마음으로 다시 루시와 함께 있었고, 그녀는 모든 것이 꿈이며 그가 결코 떠난 적이 없다고 말했다.", "en": "Free and happy, back in the old house in Soho, unaccountably released and light of heart, he was with Lucie again, and she told him it was all a dream and he had never gone away."},
"P012_3": {"ko": "망각의 시간이 지나고, 그는 고통을 겪고 평화롭게 죽어 그녀에게 돌아왔으나 그에게는 아무런 변화도 없었다.", "en": "A pause of forgetfulness followed, and then he had even suffered and come back to her, dead and at peace, yet there was no difference in him."},
"P012_4": {"ko": "또 한 번 망각의 시간이 흐르고 어스름한 아침에 깨어난 그는 자신이 어디에 있는지 무슨 일이 일어났는지 모르다가 불현듯 '오늘이 내가 죽는 날이구나!' 하고 깨달았다.", "en": "Another pause of oblivion, and he awoke in the gloomy morning, unaware of where he was or what had happened, until it flashed into his mind: 'This is the day of my death!'"},
"P013_1": {"ko": "그렇게 그는 시간을 보내며 쉰두 개의 머리가 떨어질 날에 이르렀다.", "en": "Thus he had lived through the hours up to the day when the fifty-two heads were to fall."},
"P013_2": {"ko": "이제 평온을 되찾아 조용한 영웅심으로 최후를 맞이할 수 있기를 바랄 때, 깨어있는 그의 생각 속에 새로운 작용이 시작되었고 이를 억제하기는 매우 어려웠다.", "en": "And now, while he was composed and hoped to meet the end with quiet heroism, a new mental process began in his waking thoughts which was very difficult to control."},
"P014_1": {"ko": "그는 자신의 생명을 끝낼 그 기구를 한 번도 본 적이 없었다.", "en": "He had never seen the instrument that was to end his life."},
"P014_2": {"ko": "그것이 땅에서 얼마나 높은지, 계단은 몇 개인지, 어디에 서게 될지, 사람들이 자기를 어떻게 만질지, 자기를 만지는 손이 붉게 물들어 있을지, 얼굴은 어느 쪽을 향할지, 자기가 첫 번째일지 마지막일지 등 의지와 무관한 질문들이 수없이 계속해서 떠올랐다.", "en": "How high it was from the ground, how many steps it had, where he would stand, how he would be touched, whether the touching hands would be dyed red, which way his face would turn, whether he would go first or last: these and similar questions intruded on his mind countless times."},
"P014_3": {"ko": "그것들은 두려움과도 무관했다: 그는 아무런 두려움도 느끼지 못했다.", "en": "Nor were they connected to fear: he was conscious of no fear."},
"P014_4": {"ko": "오히려 그것들은 때가 오면 무엇을 해야 할지 알고 싶어 하는 기이한 강박에서 비롯되었고, 다가올 짧은 순간에 비하면 지나치게 거대한 욕망이자 자신의 것이라기보다 자기 안의 다른 영혼의 궁금증에 더 가까웠다.", "en": "Rather, they stemmed from a strange, obsessive desire to know what to do when the time came; a desire disproportionately huge compared to the swift moments it concerned; a wondering that felt more like another spirit's than his own."},
"P015_1": {"ko": "이리저리 서성이는 동안 시간은 흘러갔고, 시계는 다시는 듣지 못할 숫자를 알리며 종을 울렸다.", "en": "The hours passed as he paced to and fro, and the clocks struck the numbers he would never hear again."},
"P015_2": {"ko": "아홉 시가 영원히 지나가고, 열 시가 영원히 지나가고, 열한 시가 영원히 지나가고, 열두 시가 다가와 지나가고 있었다.", "en": "Nine gone forever, ten gone forever, eleven gone forever, twelve coming on to pass away."},
"P015_3": {"ko": "마지막으로 그를 괴롭혔던 기이한 생각들과 힘겨운 싸움을 벌인 끝에, 그는 마침내 그것을 이겨냈다.", "en": "After a hard struggle with that strange mental activity which had recently troubled him, he overcame it."},
"P015_4": {"ko": "그는 위아래로 걸으며 그들의 이름을 속으로 조용히 되뇌었다.", "en": "He walked up and down, softly repeating their names to himself."},
"P015_5": {"ko": "가장 힘든 내적 갈등은 끝났다.", "en": "The worst of the struggle was over."},
"P015_6": {"ko": "그는 산만한 공상에서 벗어나, 자신과 그들을 위해 기도하며 걸을 수 있었다.", "en": "He could walk up and down, free from distracting illusions, praying for himself and for them."}
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
