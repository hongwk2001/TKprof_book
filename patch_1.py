import json
import codecs

filepath = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_09.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    'P002_3': {'ko': '그 정직한 상인이 그 시선을 받는 태도는 신뢰를 주지 않았습니다;', 'en': 'That honest tradesman\'s manner of receiving the look did not inspire confidence;'},
    'P002_4': {'ko': '그는 마치 그런 다리를 쉰 개쯤 가지고 있어서 그 모든 다리를 시험해 보기라도 하는 것처럼, 자신이 딛고 서 있는 다리를 자주 바꿨습니다;', 'en': 'he changed the leg on which he rested as often as if he had fifty of those limbs and were trying them all;'},
    'P002_5': {'ko': '그는 매우 의심스러울 정도로 세밀하게 주의를 기울이며 자신의 손톱을 살폈습니다;', 'en': 'he examined his fingernails with a very questionable closeness of attention;'},
    'P005_1': {'ko': '"당신은 메신저 외에 또 무슨 일을 했습니까?"', 'en': '"What have you been besides a messenger?"'},
    'P007_3': {'ko': '만약 당신이 그랬다면, 당신이 영국으로 돌아갔을 때 내가 당신의 친구가 되어줄 거라고 기대하지 마십시오.', 'en': 'If you have, don\'t expect me to befriend you when you get back to England.'},
    'P007_4': {'ko': '만약 당신이 그랬다면, 내가 당신의 비밀을 지켜줄 거라고 기대하지 마십시오.', 'en': 'If you have, don\'t expect me to keep your secret.'},
    'P007_5': {'ko': '텔슨 은행은 속아 넘어가지 않을 것입니다."', 'en': 'Tellson\'s shall not be imposed upon."'},
    'P008_3': {'ko': '그리고 만약 그랬다고 하더라도, 그조차 일방적인 것만은 아닐 거라는 점을 고려해야만 합니다.', 'en': 'And which it is to be taken into account that if it was, it wouldn\'t, even then, be all on one side.'},
    'P008_4': {'ko': '거기에는 양면이 있을 것입니다.', 'en': 'There would be two sides to it.'},
    'P008_5': {'ko': '정직한 상인이 자신의 파딩(영국의 옛 동전)--파딩! 아니, 그의 반 파딩--반 파딩! 아니, 그의 4분의 1 파딩조차도 줍지 못하는 곳에서, 자신들의 기니(영국의 옛 금화)를 주워 모으는 의사들이 지금 이 시간에도 있을 수 있습니다--텔슨 은행에 연기처럼 돈을 맡겨두고, 몰래 그 상인에게 의학적인 시선을 치켜뜨며, 자신들의 마차를 타고 들어가고 나가는--아! 그렇지 않다 하더라도 연기처럼 말입니다.', 'en': 'There might be medical doctors at the present hour picking up their guineas where an honest tradesman doesn\'t pick up his farthings--farthings! no, nor yet his half farthings--half farthings! no, nor yet his quarter--banking away like smoke at Tellson\'s, and cocking their medical eyes at that tradesman on the sly, going in and going out to their own carriages--ah! equally like smoke, if not more so.'},
    'P008_6': {'ko': '글쎄요, 그것 또한 텔슨 은행을 속이는 일이 될 것입니다.', 'en': 'Well, that would be imposing, too, on Tellson\'s.'},
    'P008_7': {'ko': '왜냐하면 당신은 암거위에게 양념을 치면서 수거위에게는 치지 않을 수는 없기 때문입니다.', 'en': 'For you cannot sauce the goose and not the gander.'},
    'P008_10': {'ko': '반면에 저 의사들의 아내들은 털썩 주저앉아 기도하지 않습니다--그들이 그러는 걸 한 번 잡아보시죠!', 'en': 'Whereas those medical doctors\' wives don\'t flop--catch them at it!'},
    'P008_11': {'ko': '아니면, 그들이 털썩 주저앉아 기도한다면, 그들의 기도는 더 많은 환자를 바라는 쪽으로 갈 테고, 어떻게 당신은 다른 하나 없이 하나만 온전히 가질 수 있겠습니까?', 'en': 'Or, if they flop, their floppings go in favor of more patients, and how can you rightly have one without the other?'},
    'P008_12': {'ko': '그러고 나서, 장의사들이 어쩌고, 교구 서기들이 어쩌고, 묘지기들이 어쩌고, 그리고 사설 야경꾼들이 어쩌고(모두 탐욕스럽고 모두 한통속입니다) 한다면, 가령 그랬다고 하더라도 사람은 그것으로 많은 것을 얻지 못할 것입니다.', 'en': 'Then, what with undertakers, and what with parish clerks, and what with sextons, and what with private watchmen (all avaricious and all in it), a man wouldn\'t get much by it, even if it was so.'},
    'P008_15': {'ko': '그는 그것에서 어떤 이득도 얻지 못할 것입니다;', 'en': 'He would never have any good of it;'},
    'P008_16': {'ko': '가령 그랬다 할지라도--그가 일단 그 업계에 발을 들여놓은 이상 빠져나갈 길을 찾을 수만 있다면 그는 내내 그 일에서 벗어나고 싶어 할 것입니다."', 'en': 'he would want all along to be out of the line, if he could see his way out, being once in--even if it was so."'},
    'P012_3': {'ko': '저기 저 바의 저 의자 위에, 남자로 자라고 성장한 저의 저 아들이 앉아 있는데, 만약 그것이 당신의 바람이라면, 당신의 발뒤꿈치가 당신의 머리가 있는 곳에 올 때까지(당신이 죽을 때까지) 당신의 심부름을 하고, 메시지를 전하고, 일반적인 잡일을 해줄 것입니다.', 'en': 'Upon that stool there, at that Bar there, sits that boy of mine, brought up and grown up to be a man, who will run errands for you, take messages for you, and do general light jobs for you, until your heels are where your head is, if such should be your wishes.'},
    'P012_4': {'ko': '아직 그렇다고 말하지는 않겠지만 (선생님께 거짓말을 하지는 않을 테니까요), 만약 그랬다면, 저기 저 아들이 아버지의 자리를 지키고 어머니를 돌보게 해주십시오;', 'en': 'If it was so, which I still don\'t say it is (for I will not prevaricate to you, sir), let that boy there keep his father\'s place, and take care of his mother;'},
    'P012_5': {'ko': '그 아이의 아버지를 밀고하지 마십시오--그러지 마십시오, 선생님--그리고 그 아버지가 정식으로 무덤을 파는 일(매장)을 하게 하시고, 만약 그랬다면, 파냈을지도 모를 것들에 대해 기꺼이, 그리고 그것들을 안전하게 영구히 지키겠다는 신념을 가지고 무덤을 파서 묻음으로써 속죄하게 해주십시오.', 'en': 'don\'t blow upon that boy\'s father--do not do it, sir--and let that father go into the line of the regular digging, and make amends for what he would have undug--if it was so--by digging them in with a will, and with convictions respecting the future keeping of them safe.'},
    'P012_8': {'ko': '자신의 이야기가 결론에 도달했음을 알리듯 팔로 이마를 닦으며 크런처가 말했습니다, "그것이 제가 선생님께 정중히 제안하고 싶은 것입니다.', 'en': 'Cruncher, wiping his forehead with his arm, as an announcement that he had arrived at the peroration of his discourse, "is what I would respectfully offer to you, sir.'},
    'P012_9': {'ko': '사람은 자신을 둘러싸고 일어나는 이 모든 끔찍한 일들, 맙소사, 머리 없는 시체들이 짐꾼 삯으로 가격을 떨어뜨릴 만큼, 아니 그조차도 안 될 만큼 충분히 흔해 빠진 상황을 보면서 사물에 대한 진지한 생각을 가지지 않을 수 없습니다.', 'en': 'A man doesn\'t see all this going on dreadfully round him here, in the way of Subjects without heads, dear me, plentiful enough to bring the price down to porterage and hardly that, without having his serious thoughts of things.'},
    'P012_10': {'ko': '그리고 만약 그랬다면 이것들이 제 생각일 것입니다, 제가 숨길 수도 있었을 때 대의를 위해 일어서서 방금 말씀드린 것을 마음속에 새겨주시기를 간청하면서 말입니다."', 'en': 'And these here would be mine, if it was so, entreating of you to bear in mind that what I said just now, I up and said in the good cause when I might have kept it back."'},
    'P013_3': {'ko': '당신이 그럴 자격이 있고, 말이 아닌 행동으로 회개한다면, 나는 여전히 당신의 친구로 남을 수 있을 것입니다.', 'en': 'It may be that I shall yet stand your friend, if you deserve it, and repent in action--not in words.'},
    'P013_4': {'ko': '더 이상 말은 필요 없습니다."', 'en': 'I want no more words."'},
    'P014_3': {'ko': '바사드," 전자가 말했습니다;', 'en': 'Barsad," said the former;'},
    'P014_4': {'ko': '"이렇게 우리의 협정이 맺어졌으니, 당신은 나에게서 두려울 것이 없습니다."', 'en': '"our arrangement thus made, you have nothing to fear from me."'},
    'P016_1': {'ko': '"많지 않습니다.', 'en': '"Not much.'},
    'P016_2': {'ko': '만약 죄수에게 일이 잘못 돌아간다면, 내가 그에게 한 번 접근할 수 있도록 확실히 해두었습니다."', 'en': 'If it should go ill with the prisoner, I have ensured access to him, once."'},
    'P018_1': {'ko': '"내가 할 수 있는 전부였습니다," 카턴이 말했습니다. "너무 많은 것을 제안하는 것은 이 남자의 머리를 도끼 아래에 놓는 것이 될 테고, 그 자신이 말했듯, 그가 고발당한다면 그에게 그보다 더 나쁜 일은 일어날 수 없기 때문입니다.', 'en': '"It is all I could do," said Carton. "To propose too much, would be to put this man\'s head under the axe, and, as he himself said, nothing worse could happen to him if he were denounced.'},
    'P018_2': {'ko': '그것이 분명히 입장의 약점이었습니다.', 'en': 'It was obviously the weakness of the position.'},
    'P018_3': {'ko': '어쩔 수 없는 일입니다."', 'en': 'There is no help for it."'},
    'P020_1': {'ko': '"나는 그것이 그럴 것이라고 말한 적이 없습니다."', 'en': '"I never said it would."'},
    'P021_3': {'ko': '사랑하는 딸에 대한 그의 연민과, 두 번째 체포로 인한 무거운 실망감이 그들을 점차 약화시켰습니다;', 'en': 'his sympathy with his darling, and the heavy disappointment of his second arrest, gradually weakened them;'},
    'P021_4': {'ko': '그는 이제 노인이었고, 최근의 불안감에 짓눌려 있었으며, 그의 눈물이 떨어졌습니다.', 'en': 'he was an old man now, overborne with anxiety of late, and his tears fell.'},
    'P022_1': {'ko': '"당신은 좋은 사람이고 진실한 친구입니다," 카턴이 변한 목소리로 말했습니다. "당신이 감동받은 것을 제가 알아챈다면 용서해 주십시오.', 'en': '"You are a good man and a true friend," said Carton, in an altered voice. "Forgive me if I notice that you are affected.'},
    'P022_2': {'ko': '나는 내 아버지가 우시는 것을 무심하게 곁에 앉아서 보고 있을 수는 없을 것입니다.', 'en': 'I could not see my father weep, and sit by, careless.'},
    'P022_3': {'ko': '그리고 당신이 내 아버지라 해도, 당신의 슬픔을 이보다 더 존중할 수는 없을 것입니다.', 'en': 'And I could not respect your sorrow more, if you were my father.'},
    'P022_4': {'ko': '하지만 당신은 그런 불행에서는 자유롭군요."', 'en': 'You are free from that misfortune, however."'},
    'P023_3': {'ko': '그는 그에게 손을 내밀었고, 카턴은 그것을 부드럽게 쥐었습니다.', 'en': 'He gave him his hand, and Carton gently pressed it.'}
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

import io
for b in empty_blocks[:40]:
    print(b['tag'] + '|' + b['raw'])

