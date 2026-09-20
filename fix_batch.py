import json

fix_dict = {
"It was the best of times, and it was the worst of times. It was an age of wisdom, and it was an age of foolishness. It was an epoch of belief, and it was an epoch of skepticism. It was a season of Light, and it was a season of Darkness. It was a spring of hope, and it was a winter of despair. We had everything ahead of us, and we had nothing ahead of us. We were all going straight to Heaven, and we were all going straight the other way. In short, the time was so much like our own that some of its loudest voices insisted that it could only be described in extremes, whether for better or for worse.": "최고의 시절이었고 최악의 시절이었습니다. 지혜의 시대였고, 어리석음의 시대였습니다. 믿음의 시대였고, 회의의 시대였습니다. 빛의 계절이었고, 어둠의 계절이었습니다. 희망의 봄이었고, 절망의 겨울이었습니다. 우리 앞에는 모든 것이 있었고, 우리 앞에는 아무것도 없었습니다. 우리는 모두 천국으로 곧장 가고 있었고, 우리 모두는 그 반대 방향으로 곧장 가고 있었습니다. 요컨대, 그 시대는 우리 시대와 너무나 비슷하여 가장 큰 목소리를 내는 사람들 중 일부는 좋든 나쁘든 극단적으로만 설명할 수 있다고 주장했습니다.",
"There was a king with a large jaw and a queen with a plain face on the throne of England. There was a king with a large jaw and a queen with a beautiful face on the throne of France.": "영국의 왕좌에는 턱이 큰 왕과 평범한 얼굴의 여왕이 있었습니다. 프랑스의 왕좌에는 턱이 큰 왕과 아름다운 얼굴의 여왕이 있었습니다.",
"In both countries, it was crystal clear to the wealthy lords who controlled the government's wealth and power that things in general were settled forever.": "두 나라 모두에서, 정부의 부와 권력을 지배하는 부유한 영주들에게는 일반적인 상황이 영원히 정착되었다는 것이 수정처럼 분명했습니다.",
"It was the year of Our Lord 1775.": "그 해는 주후 1775년이었습니다.",
"Spiritual revelations were granted to England during that favored time, just as they are today.": "오늘날과 마찬가지로 그 은총받은 시대에 영적인 계시가 영국에 주어졌습니다.",
"Southcott had recently turned twenty-five. Around the same time, a prophetic soldier in the Life Guards announced her arrival. He claimed that London and Westminster were about to be swallowed up by the earth.": "사우스콧은 최근에 25살이 되었습니다. 거의 같은 시기에 근위병 중 예언자적인 병사가 그녀의 도착을 알렸습니다. 그는 런던과 웨스트민스터가 곧 땅에 삼켜질 것이라고 주장했습니다.",
"Even the famous Cock Lane ghost had been put to rest only twelve years earlier, after tapping out its messages, just like the spirits of this past year, which were surprisingly unoriginal, tapped out theirs.": "유명한 콕 레인 유령조차도, 놀랍게도 독창적이지 않았던 지난 1년의 영혼들이 메시지를 두드린 것처럼 메시지를 두드린 후 불과 12년 전에야 안식을 취했습니다.",
"Meanwhile, much more down-to-earth messages had recently arrived for the English King and his people from a congress of British subjects in America. Strange as it seems, these letters turned out to be far more important to the human race than any messages ever received from the spirits of the Cock Lane family.": "한편, 최근 미국의 영국 신민 의회에서 영국 국왕과 그의 국민들에게 훨씬 더 현실적인 메시지가 도착했습니다. 이상하게 보일지 모르지만, 이 편지들은 콕 레인 가문의 영혼들로부터 받은 그 어떤 메시지보다 인류에게 훨씬 더 중요하다고 판명되었습니다.",
"France, which was generally less interested in spiritual matters than England, was rolling smoothly downhill, printing paper money and spending it quickly.": "영국보다 일반적으로 영적인 문제에 덜 관심이 있었던 프랑스는 지폐를 인쇄하고 빨리 쓰면서 내리막길을 순조롭게 굴러가고 있었습니다.",
"France was guided by her priests and amused herself with terrible violence. In one case, a young man was sentenced to have his hands cut off, his tongue torn out, and his body burned alive. His only crime was failing to kneel in the rain to show respect to a dirty group of monks passing by in the distance.": "프랑스는 성직자들의 인도를 받았고 끔찍한 폭력으로 즐거워했습니다. 한 번은 젊은이가 손을 잘리고 혀를 뽑히며 산 채로 화형에 처해지는 선고를 받았습니다. 그의 유일한 범죄는 비 속에서 무릎을 꿇고 멀리 지나가는 더러운 수도사 무리에게 존경을 표하지 않은 것이었습니다.",
"As always, Fate is the woodcutter working quietly. In the forests of France and Norway, he is growing trees. Soon, those trees will be cut down and sawed into wood. That wood will be used to build the guillotine, a terrifying machine with a heavy falling blade used to execute people.": "언제나 그렇듯이 운명은 조용히 일하는 나무꾼입니다. 프랑스와 노르웨이의 숲에서 그는 나무를 기르고 있습니다. 머지않아 그 나무들은 베어지고 톱으로 썰려 나무가 될 것입니다. 그 나무는 무거운 떨어지는 칼날을 사용하여 사람을 처형하는 무서운 기계인 단두대를 만드는 데 사용될 것입니다."
}

with open('c:/git_repo/TKprof_book/translated_batches/batch_0_99.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for x in d:
    en_text = x['ko']
    if 'Just one more pull and youll be' in en_text:
        x['ko'] = '한 번만 더 당기면 정상에 도착할 거야, 빌어먹을, 여기까지 오는 데 충분히 고생했으니까!, 조!'
    elif 'The guard grumbled to himself, "I dont like Jerrys voice' in en_text:
        x['ko'] = '호위병이 혼잣말로 투덜거렸습니다. "만약 저게 제리라면, 제리의 목소리는 마음에 안 들어. 목소리가 내 취향에는 너무 쉬었군, 그 제리라는 사람."'
    elif '"I hope not, but I cant be so sure of that,' in en_text:
        x['ko'] = '호위병이 혼잣말로 중얼거렸습니다. "그러길 바라지만 그렇게 확신할 순 없지." "어이 너!"'
    elif 'And if youve got holsters on that saddle' in en_text:
        x['ko'] = '그리고 네 그 안장에 권총집이 있다면, 네 손이 그 근처에 가는 걸 내 눈에 띄게 하지 마.'
    elif 'Because Im very quick to make a mistake' in en_text:
        x['ko'] = '왜냐하면 난 아주 빨리 실수를 저지르고, 그럴 땐 총알로 하거든.'
    elif en_text in fix_dict:
        x['ko'] = fix_dict[en_text]

with open('c:/git_repo/TKprof_book/translated_batches/batch_0_99.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

