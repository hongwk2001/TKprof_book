import json
file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_24.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

patches = {
    'P006_1': {
        'ko': '1792년 8월이 밝았고, 그때쯤 Monseigneur는 뿔뿔이 흩어져 있었습니다.',
        'en': 'The August of the year 1792 had arrived, and by this time Monseigneur was scattered far and wide.'
    },
    'P007_1': {
        'ko': '자연스럽게 런던에서 Monseigneur의 본부이자 주요 집결지는 Tellson 은행(Tellson\'s Bank)이었습니다.',
        'en': "As was natural, the headquarters and great gathering place for Monseigneur in London was Tellson's Bank."
    },
    'P007_2': {
        'ko': '유령은 자신들의 몸이 가장 자주 머물던 장소에 출몰한다고들 하는데, 수중에 1기니(guinea)도 없는 Monseigneur는 예전에 자신의 기니들이 있던 그 장소를 맴돌았습니다.',
        'en': "Spirits are said to haunt the places where their bodies most frequented, and Monseigneur, without a single guinea, haunted the place where his guineas used to be."
    },
    'P007_3': {
        'ko': '게다가 그곳은 가장 신뢰할 만한 프랑스 정보가 가장 빨리 도착하는 곳이었습니다.',
        'en': 'Moreover, it was the place where the most reliable French news arrived quickest.'
    },
    'P007_5': {
        'ko': 'Tellson 은행은 후한 곳이었고, 높은 지위에서 몰락한 옛 고객들에게 큰 관대함을 베풀었습니다.',
        'en': "Tellson's was a generous establishment, and extended great liberality to old customers who had fallen from their high status."
    },
    'P007_7': {
        'ko': '다가오는 폭풍을 제때 알아차리고 약탈이나 몰수를 예상하여 Tellson 은행으로 선견지명 있게 송금해둔 귀족들은, 그들의 궁핍한 동료들에 의해 그곳에서 항상 소식을 들을 수 있었습니다.',
        'en': "those nobles who had seen the approaching storm in time and, expecting plunder or confiscation, had wisely remitted funds to Tellson's, could always be heard of there by their needy peers."
    },
    'P007_8': {
        'ko': '여기에 프랑스에서 온 새로운 사람마다 거의 당연하게 Tellson 은행에 나타나 자신과 자신의 소식을 보고했다는 점을 덧붙여야 합니다.',
        'en': "To this it must be added that every newcomer from France reported themselves and their news at Tellson's, almost as a matter of course."
    },
    'P007_9': {
        'ko': '이런 다양한 이유로 인해, 당시 Tellson 은행은 프랑스 정보에 관해서는 일종의 대규모 거래소(High Exchange)와 같았습니다;',
        'en': "For such various reasons, Tellson's was at that time a kind of High Exchange for French intelligence;"
    },
    'P007_10': {
        'ko': '그리고 이것은 대중에게 너무나 잘 알려져 있었고, 그로 인해 그곳에서 이루어지는 문의가 매우 많았기 때문에, Tellson 은행은 때때로 최신 뉴스를 한 줄 정도로 적어 은행 창문에 붙여, Temple Bar를 지나가는 모든 사람이 읽을 수 있게 했습니다.',
        'en': "and this was so well known to the public, and the resulting inquiries were so numerous, that Tellson's sometimes wrote the latest news in a line or two and posted it in the Bank windows for anyone running through Temple Bar to read."
    },
    'P008_3': {
        'ko': '한때 은행 측과의 면담을 위해 따로 마련되어 있던 그 참회실 같은 골방(penitential den)은 이제 뉴스 거래소가 되어 발 디딜 틈 없이 가득 찼습니다.',
        'en': 'The penitential den that had once been set aside for interviews with the House was now the news-Exchange, and it was filled to overflowing.'
    },
    'P009_1': {
        'ko': '"하지만 비록 당신이 이 세상에서 가장 젊은 분(youngest man that ever lived)이긴 해도," Charles Darnay가 다소 망설이며 말했습니다. "그래도 이런 말씀을 드려야겠습니다--"',
        'en': '"But, even though you are the youngest man that ever lived," said Charles Darnay, rather hesitantly, "I must still suggest to you--"'
    },
    'P011_1': {
        'ko': '"변덕스러운 날씨, 긴 여정, 불확실한 이동 수단, 혼란에 빠진 나라, 심지어 당신에게 안전하지 않을 수도 있는 도시입니다."',
        'en': '"Unsettled weather, a long journey, uncertain means of travel, a disorganized country, a city that may not even be safe for you."'
    },
    'P012_5': {
        'ko': '더 간섭할 가치가 있는 사람들이 그곳에 그렇게 많은데, 여든에 가까운(hard upon fourscore) 늙은이에게 간섭하려고 신경 쓸 사람은 아무도 없을 겁니다.',
        'en': 'nobody will care to bother with an old man nearly eighty years old when there are so many people there much more worth interfering with.'
    },
    'P012_6': {
        'ko': '혼란에 빠진 도시라는 점에 대해서 말하자면, 만약 혼란에 빠진 도시가 아니라면 예전부터 그 도시와 업무를 잘 알고 Tellson 은행의 신임을 받는 누군가를 우리 런던 본점(House)에서 파리 지점(House)으로 보낼 이유가 없을 겁니다.',
        'en': "As for it being a disorganized city, if it were not a disorganized city, there would be no reason to send someone from our House here to our House there, who has long known the city and the business, and holds Tellson's confidence."
    },
    'P012_7': {
        'ko': '불확실한 이동 수단, 긴 여정, 겨울 날씨에 관해 말하자면, 내가 지난 오랜 세월이 지난 지금 Tellson 은행을 위해 약간의 불편함을 감수할 준비가 되어 있지 않다면, 도대체 누가 감수해야 하겠습니까?"',
        'en': 'As for the uncertain travel, the long journey, and the winter weather, if I were not ready to endure a few inconveniences for Tellson\'s sake after all these years, who should be?"'
    },
    'P013_1': {
        'ko': '"나 자신이 직접 갔으면 좋겠습니다," Charles Darnay가 다소 불안한 듯, 혼잣말(thinking aloud)을 하듯 말했습니다.',
        'en': '"I wish I were going myself," said Charles Darnay, somewhat restlessly, and like someone thinking aloud.'
    },
    'P015_2': {
        'ko': 'Lorry 씨, 내가 프랑스 태생이기에 (하지만 여기서 입 밖에 낼 생각은 없었던) 그런 생각이 내 마음속을 자주 스쳐 지나갔습니다.',
        'en': "Lorry, it is because I was born a Frenchman that the thought (which I didn't intend to express here, though) has often crossed my mind."
    },
    'P015_3': {
        'ko': '그 비참한 사람들에게 동정심을 가졌었고 그들에게 무언가를 양보했었기에," 그는 예전의 생각에 잠긴 태도로 말했습니다, "내 말을 들어줄지도 모르고, 그들이 어느 정도 자제하도록 설득할 수 있는 힘이 있을지도 모른다는 생각을 떨칠 수가 없습니다.',
        'en': 'One cannot help thinking, having felt some sympathy for the miserable people and having given up something to them," he said, returning to his former thoughtful manner, "that one might be listened to, and might have the power to persuade them to show some restraint.'
    },
    'P017_1': {
        'ko': '"어쨌든, 나는 가지 않습니다," Charles Darnay가 미소를 지으며 말했습니다. "당신이 간다고 하시는 게 더 중요한 문제죠(more to the purpose)."',
        'en': '"However, I am not going," said Charles Darnay with a smile. "It is more relevant that you say you are."'
    },
    'P018_3': {
        'ko': 'Lorry 씨는 멀리 은행 쪽(House)을 힐끗 보더니 목소리를 낮췄습니다, "우리 업무를 처리하는 데 얼마나 어려움이 따르는지, 저편에 있는 우리 장부와 서류들이 얼마나 위험에 처해 있는지 당신은 상상도 못 할 겁니다.',
        'en': 'Lorry glanced toward the distant House and lowered his voice, "You can\'t conceive the difficulty with which our business is conducted, and the danger that our books and papers over there are in.'
    },
    'P018_4': {
        'ko': '만약 우리 서류 중 일부가 압수되거나 파기된다면, 얼마나 많은 사람들에게 치명적인 결과(compromising consequences)가 미칠지 하늘만이 아십니다;',
        'en': 'Only the Lord above knows what the damaging consequences would be to numerous people if some of our documents were seized or destroyed;'
    },
    'P018_5': {
        'ko': '그리고 그런 일은 언제든 일어날 수 있습니다, 아시겠지만, 오늘 파리에 불이 나지 않는다거나 내일 파리가 약탈당하지 않으리라고 누가 장담할 수 있겠습니까!',
        'en': "and they might be, at any time, you know, for who can guarantee that Paris won't be set on fire today or sacked tomorrow!"
    },
    'P018_6': {
        'ko': '자, 가능한 한 지체 없이 이것들 중에서 신중하게 문서를 골라내어(judicious selection) 땅에 묻거나 다른 안전한 곳으로 빼내는 일은, (귀중한 시간의 낭비 없이) 처리할 수 있는 사람은, 설령 누군가 있다 해도, 나 외에는 거의 아무도 없습니다.',
        'en': "Now, making a careful selection from these with the least possible delay, and burying them, or otherwise getting them out of harm's way, is something that hardly anyone but myself is capable of doing (without wasting precious time), if anyone at all."
    },
    'P018_7': {
        'ko': '그런데 Tellson 은행이 이 사실을 알고 그렇게 말하고 있는데—지난 60년 동안 그곳의 밥을 먹어 온(bread I have eaten) 내가 관절이 좀 뻣뻣하다고 해서 뒤로 물러서야 하겠습니까?',
        'en': "And should I hold back, when Tellson's knows this and says this—Tellson's, whose bread I have eaten for these sixty years—just because my joints are a little stiff?"
    },
    'P020_3': {
        'ko': 'Lorry 씨가 다시 은행 쪽을 힐끗 보며, "당신은 기억해야 합니다. 지금 이 시기에 파리에서 물건을 빼내는 것은, 그것이 무엇이든 간에, 불가능에 가깝다는 것을 말입니다.',
        'en': 'Lorry, glancing at the House again, "you must remember that getting things out of Paris at this present time, no matter what they are, is next to impossible.'
    },
    'P020_5': {
        'ko': '당신에게라도 속삭이듯 말하는 건 업무상 적절치 않지만), 당신이 상상할 수 있는 가장 기이한 전달자들에 의해 전해졌습니다. 그들 각자는 바리케이드(Barriers)를 지날 때마다 목숨이 간당간당한(head hanging on by a single hair) 상태였습니다.',
        'en': "it is not business-like to whisper it, even to you), by the strangest messengers you can imagine, every one of whom risked their lives by a hair's breadth as they passed the Barriers."
    },
    'P024_4': {
        'ko': '아무도 Jerry를 영국의 불독(English bull-dog) 이외의 것으로 의심하지 않을 것이며, 그의 주인을 건드리는 사람에게 덤벼드는 것 외에 그의 머릿속에 다른 어떤 목적이 있을 거라고 의심하지도 않을 것입니다."',
        'en': 'No one will suspect Jerry of being anything other than an English bulldog, or of having any plan in his head other than attacking anyone who touches his master."'
    },
    'P026_2': {
        'ko': '이 작은 임무(little commission)를 마치고 나면, 아마도 은퇴해서 편안하게 살라는 Tellson 은행의 제안을 받아들일지도 모르겠습니다.',
        'en': "When I have completed this little assignment, I shall perhaps accept Tellson's offer to retire and live comfortably."
    },
    'P027_2': {
        'ko': 'Lorry 씨의 평소 책상 주변으로 1, 2야드 내에 Monseigneur들이 바글거렸고(swarming), 그들은 머지않아 저 악당 같은 무리(rascal-people)에게 복수하기 위해 자신이 무엇을 할 것인지 호언장담하고 있었습니다.',
        'en': "Lorry's usual desk, with Monseigneur swarming within a yard or two of it, boasting about what he would soon do to take revenge on the rascal-people."
    },
    'P027_3': {
        'ko': '망명자로서 역경을 겪는 Monseigneur가, 그리고 영국의 전형적인 보수주의(native British orthodoxy)가, 이 끔찍한 혁명을 마치 하늘 아래 씨 뿌려지지 않은 유일한 수확물인 양—마치 그것을 초래한 어떤 일도 행해지거나 방치된 적이 없는 양—마치 프랑스의 비참한 수백만 명과 그들을 번영하게 했어야 할 잘못 사용되고 왜곡된 자원들을 관찰한 자들이 수년 전에 혁명이 필연적으로 다가오는 것을 보지 못했고 그들이 본 것을 분명한 말로 기록하지 않았던 양 떠들어대는 것은 너무나 지나친 처사였습니다.',
        'en': "It was entirely too characteristic of Monseigneur in his misfortunes as a refugee, and entirely too characteristic of the typical British orthodoxy, to talk about this terrible Revolution as if it were the only harvest ever known under the sun that hadn't been sown—as if nothing had ever been done, or left undone, that led to it—as if those observing the miserable millions in France, and the abused and distorted resources that should have made them prosperous, had not foreseen its inevitable arrival years before, and had not plainly recorded what they saw."
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
