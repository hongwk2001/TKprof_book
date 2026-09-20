import json
import codecs

filepath = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_09.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    'P084_1': {'ko': '"이것들을 따로 보관하도록 조심하시겠지, 시민 동지?', 'en': '"You will be careful to keep them separate, citizen?'},
    'P084_2': {'ko': '이것들을 섞으면 어떻게 되는지 알 테니까?"', 'en': 'You know the consequences of mixing them?"'},
    'P085_1': {'ko': '"완벽히 알고 있소."', 'en': '"Perfectly."'},
    'P086_1': {'ko': '어떤 작은 꾸러미들이 만들어져 그에게 건네졌습니다.', 'en': 'Certain small packets were made and given to him.'},
    'P086_2': {'ko': '그는 그것들을 하나씩 안주머니에 넣고, 약값을 세어 낸 뒤, 신중하게 가게를 나섰습니다. "더 이상 할 일이 없군," 그는 달을 올려다보며 말했습니다, "내일까지는."', 'en': 'He put them, one by one, in the breast of his inner coat, counted out the money for them, and deliberately left the shop. "There is nothing more to do," said he, glancing upward at the moon, "until to-morrow.'},
    'P086_3': {'ko': '잠이 오지 않는군."', 'en': 'I can\'t sleep."'},
    'P087_1': {'ko': '구름이 빠르게 흘러가는 아래에서 그가 이 말들을 소리 내어 말한 태도는 무모한 태도가 아니었으며, 반항이라기보다는 무심함을 표현하는 것도 아니었습니다.', 'en': 'It was not a reckless manner, the manner in which he said these words aloud under the fast-sailing clouds, nor was it more expressive of negligence than defiance.'},
    'P087_2': {'ko': '그것은 헤매고 발버둥 치며 길을 잃었으나, 마침내 자신의 길로 접어들어 그 끝을 보게 된 지친 남자의 차분한 태도였습니다.', 'en': 'It was the settled manner of a tired man, who had wandered and struggled and got lost, but who at length struck into his road and saw its end.'},
    'P088_1': {'ko': '오래전, 그가 가장 초기의 경쟁자들 사이에서 대단히 전도유망한 젊은이로 유명했을 때, 그는 그의 아버지를 무덤까지 따라갔었습니다.', 'en': 'Long ago, when he had been famous among his earliest competitors as a youth of great promise, he had followed his father to the grave.'},
    'P088_2': {'ko': '그의 어머니는 수년 전에 돌아가셨습니다.', 'en': 'His mother had died, years before.'},
    'P088_3': {'ko': '달과 구름이 그의 머리 위 높이 흘러가는 가운데, 그가 짙은 그림자 사이로 어두운 거리를 걸어갈 때 아버지의 무덤에서 낭독되었던 이 장엄한 말씀이 그의 마음속에 떠올랐습니다. "나는 부활이요 생명이니, 주께서 말씀하시기를:', 'en': 'These solemn words, which had been read at his father\'s grave, arose in his mind as he went down the dark streets, among the heavy shadows, with the moon and the clouds sailing on high above him. "I am the resurrection and the life, saith the Lord:'},
    'P088_4': {'ko': '나를 믿는 자는 죽어도 살겠고:', 'en': 'he that believeth in me, though he were dead, yet shall he live:'},
    'P088_5': {'ko': '무릇 살아서 나를 믿는 자는 영원히 죽지 아니하리라."', 'en': 'and whosoever liveth and believeth in me, shall never die."'},
    'P089_1': {'ko': '도끼가 지배하는 도시에서, 밤에 홀로, 그날 처형된 예순세 명과 감옥에서 자신들의 운명을 기다리고 있는 내일의 희생자들, 그리고 또 내일과 내일의 희생자들에 대한 자연스러운 슬픔이 그의 안에서 솟아오르는 가운데, 마치 심해에서 끌어올린 녹슨 낡은 배의 닻처럼 그 말씀을 마음에 와닿게 한 연상의 사슬은 쉽게 발견될 수 있었을 것입니다.', 'en': 'In a city dominated by the axe, alone at night, with natural sorrow rising in him for the sixty-three who had been that day put to death, and for to-morrow\'s victims then awaiting their doom in the prisons, and still of to-morrow\'s and to-morrow\'s, the chain of association that brought the words home, like a rusty old ship\'s anchor from the deep, might have been easily found.'},
    'P089_2': {'ko': '그는 그것을 찾으려 하지 않았지만, 그 말씀들을 되뇌며 계속 걸어갔습니다.', 'en': 'He did not seek it, but repeated them and went on.'},
    'P090_1': {'ko': '몇 시간의 고요함을 통해 자신들을 둘러싼 공포를 잊은 채 사람들이 잠자리에 들고 있는 불 켜진 창문들에 대한 경건한 관심과 함께;', 'en': 'With a solemn interest in the lighted windows where the people were going to rest, forgetful through a few calm hours of the horrors surrounding them;'},
    'P090_2': {'ko': '어떤 기도도 올려지지 않는 교회의 탑들, 수년간의 사제 사기꾼들, 약탈자들, 난봉꾼들로 인해 대중의 반감이 자멸의 극치에 달해 있었기에;', 'en': 'in the towers of the churches, where no prayers were said, for the popular revulsion had even travelled that length of self-destruction from years of priestly impostors, plunderers, and profligates;'},
    'P090_3': {'ko': '사람들이 그 문에 \'영원한 수면을 위하여\'라고 적어 놓은, 저 멀리 떨어진 묘지들에 대한;', 'en': 'in the distant burial-places, reserved, as they wrote upon the gates, for Eternal Sleep;'},
    'P090_4': {'ko': '넘쳐나는 감옥들에 대한;', 'en': 'in the abounding gaols;'},
    'P090_5': {'ko': '그리고 기요틴의 모든 작업에서 기인하여 원혼이 출몰한다는 슬픈 이야기가 사람들 사이에 한 번도 퍼지지 않았을 정도로 너무도 흔하고 물질적인 것이 되어버린 죽음을 향해 예순 명 남짓의 사람들이 수레에 실려 굴러갔던 거리들에 대한;', 'en': 'and in the streets along which the sixties rolled to a death which had become so common and material, that no sorrowful story of a haunting Spirit ever arose among the people out of all the working of the Guillotine;'},
    'P090_6': {'ko': '광란 속에서 짧은 밤의 휴식으로 가라앉고 있는 도시의 삶과 죽음 전체에 대한 경건한 관심과 함께;', 'en': 'with a solemn interest in the whole life and death of the city settling down to its short nightly pause in fury;'},
    'P090_7': {'ko': '시드니 카턴은 더 밝은 거리들을 향해 다시 센 강을 건넜습니다.', 'en': 'Sydney Carton crossed the Seine again for the lighter streets.'},
    'P091_1': {'ko': '거리에 마차는 거의 없었는데, 마차에 탄 사람들은 의심받기 십상이었고, 귀족 계급은 붉은 나이트캡(혁명 모자)을 쓰고 머리를 숨긴 채 무거운 신발을 신고 터덜터덜 걸었기 때문이었습니다.', 'en': 'Few coaches were abroad, for riders in coaches were liable to be suspected, and gentility hid its head in red nightcaps, and put on heavy shoes, and trudged.'},
    'P091_2': {'ko': '하지만, 극장들은 모두 꽉 차 있었고, 그가 지나갈 때 사람들이 유쾌하게 쏟아져 나와 수다를 떨며 집으로 돌아가고 있었습니다.', 'en': 'But, the theatres were all well filled, and the people poured cheerfully out as he passed, and went chatting home.'},
    'P091_3': {'ko': '어느 극장 문 앞에는 한 어린 소녀가 어머니와 함께 진흙투성이 거리를 건널 길을 찾고 있었습니다.', 'en': 'At one of the theatre doors, there was a little girl with a mother, looking for a way across the street through the mud.'},
    'P091_4': {'ko': '그는 그 아이를 안아서 건네주었고, 조심스러운 팔이 그의 목에서 풀리기 전에 아이에게 뽀뽀를 해달라고 부탁했습니다.', 'en': 'He carried the child over, and before the timid arm was loosed from his neck asked her for a kiss.'},
    'P092_1': {'ko': '"나는 부활이요 생명이니, 주께서 말씀하시기를:', 'en': '"I am the resurrection and the life, saith the Lord:'},
    'P092_2': {'ko': '나를 믿는 자는 죽어도 살겠고:', 'en': 'he that believeth in me, though he were dead, yet shall he live:'},
    'P092_3': {'ko': '무릇 살아서 나를 믿는 자는 영원히 죽지 아니하리라."', 'en': 'and whosoever liveth and believeth in me, shall never die."'},
    'P093_1': {'ko': '이제 거리는 조용해지고 밤이 깊어가자, 그 말씀은 그의 발소리의 메아리 속에 있었고, 공기 중에 있었습니다.', 'en': 'Now, that the streets were quiet, and the night wore on, the words were in the echoes of his feet, and were in the air.'},
    'P093_2': {'ko': '완벽하게 차분하고 흔들림 없이, 그는 걸으면서 때때로 그 말씀들을 혼자서 되뇌었습니다;', 'en': 'Perfectly calm and steady, he sometimes repeated them to himself as he walked;'},
    'P093_3': {'ko': '하지만, 그는 항상 그 말씀들을 듣고 있었습니다.', 'en': 'but, he heard them always.'},
    'P094_1': {'ko': '밤이 다 지나가고, 그가 다리 위에 서서 파리의 시테 섬 강변 벽에 부딪혀 튀어 오르는 물소리에 귀를 기울이고 있을 때, 그림같이 어우러진 집들과 성당이 달빛에 밝게 빛나고 있는 가운데 날이 차갑게 밝아왔고, 그것은 마치 하늘에서 내민 죽은 자의 얼굴 같았습니다.', 'en': 'The night wore out, and, as he stood upon the bridge listening to the water as it splashed the river-walls of the Island of Paris, where the picturesque confusion of houses and cathedral shone bright in the light of the moon, the day came coldly, looking like a dead face out of the sky.'},
    'P094_2': {'ko': '그러고 나서 달과 별이 있던 밤은 창백해지며 죽어갔고, 잠시 동안 마치 창조물이 죽음의 지배에 넘겨진 것 같았습니다.', 'en': 'Then, the night, with the moon and the stars, turned pale and died, and for a little while it seemed as if Creation were delivered over to Death\'s dominion.'}
}

for i in range(len(data)):
    t = data[i].get('tag')
    if t in translations:
        data[i]['ko'] = translations[t]['ko']
        data[i]['en'] = translations[t]['en']

with codecs.open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

empty_blocks = [b for b in data if b.get('ko') == '' and not b.get('is_header', False)]
print('Remaining empty:', len(empty_blocks))

if len(empty_blocks) > 0:
    for b in empty_blocks:
        print(b['tag'] + '|' + b['raw'])

