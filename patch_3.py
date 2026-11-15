import json
import codecs

filepath = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_09.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    'P043_2': {'ko': '그녀가 당신을 위해 울어주지 않겠습니까?', 'en': 'Wouldn\'t She weep for you?'},
    'P043_3': {'ko': '그녀의 아이는 울어주지 않겠습니까?"', 'en': 'Wouldn\'t her child?"'},
    'P044_1': {'ko': '"네, 네, 감사한 일이지요.', 'en': '"Yes, yes, thank God.'},
    'P044_2': {'ko': '내 말은 전혀 그런 뜻이 아니었습니다."', 'en': 'I didn\'t quite mean what I said."'},
    'P045_1': {'ko': '"그것은 진정 하나님께 감사할 일입니다;', 'en': '"It _is_ a thing to thank God for;'},
    'P045_2': {'ko': '그렇지 않습니까?"', 'en': 'is it not?"'},
    'P046_1': {'ko': '"물론이죠, 물론입니다."', 'en': '"Surely, surely."'},
    'P047_1': {'ko': '"만약 당신이 오늘 밤, 당신의 쓸쓸한 마음에 대고 진실로 \'나는 그 어떤 사람의 사랑과 애착, 감사나 존경도 얻지 못했다;', 'en': '"If you could say, with truth, to your own solitary heart, to-night, \'I have secured to myself the love and attachment, the gratitude or respect, of no human creature;'},
    'P047_2': {'ko': '나는 어느 누구에게서도 다정한 자리를 차지하지 못했다;', 'en': 'I have won myself a tender place in no regard;'},
    'P047_3': {'ko': '나는 기억될 만한 선하고 유용한 일을 아무것도 하지 않았다!\'라고 말할 수 있다면, 당신의 일흔여덟 해는 일흔여덟 번의 무거운 저주일 것입니다;', 'en': 'I have done nothing good or serviceable to be remembered by!\' your seventy-eight years would be seventy-eight heavy curses;'},
    'P047_4': {'ko': '그렇지 않겠습니까?"', 'en': 'would they not?"'},
    'P048_3': {'ko': '내 생각에도 그럴 것 같소."', 'en': 'I think they would be."'},
    'P049_1': {'ko': '시드니는 다시 불길로 눈길을 돌렸고, 잠시 침묵한 뒤에 말했습니다:', 'en': 'Sydney turned his eyes again upon the fire, and, after a silence of a few moments, said:'},
    'P050_1': {'ko': '"당신에게 묻고 싶습니다:--당신의 어린 시절이 아득하게 느껴지십니까?', 'en': '"I should like to ask you:--Does your childhood seem far off?'},
    'P050_2': {'ko': '어머니의 무릎에 앉아 있던 그 시절이 아주 오래전의 날들처럼 느껴지십니까?"', 'en': 'Do the days when you sat at your mother\'s knee, seem days of very long ago?"'},
    'P052_1': {'ko': '"20년 전에는 그랬소;', 'en': '"Twenty years back, yes;'},
    'P052_2': {'ko': '내 인생의 지금 이 시점에는 그렇지 않다오.', 'en': 'at this time of my life, no.'},
    'P052_3': {'ko': '왜냐하면, 내가 끝에 점점 가까워짐에 따라, 나는 원을 그리며 시작에 점점 더 가까워지고 있기 때문이오.', 'en': 'For, as I draw closer and closer to the end, I travel in the circle, nearer and nearer to the beginning.'},
    'P052_4': {'ko': '그것은 길을 부드럽게 하고 준비해 주는 친절한 방법 중 하나인 것 같소.', 'en': 'It seems to be one of the kind smoothings and preparings of the way.'},
    'P052_5': {'ko': '나의 예쁘고 젊은 어머니(그리고 이렇게 늙어버린 나!)에 대한 오랫동안 잠들어 있던 많은 기억들과, 우리가 세상이라고 부르는 것이 내게 그렇게 실감 나지 않았고 내 잘못들이 내 안에 굳어지기 전의 날들에 대한 수많은 연상들에 의해, 지금 내 마음은 뭉클해진다오."', 'en': 'My heart is touched now, by many remembrances that had long fallen asleep, of my pretty young mother (and I so old!), and by many associations of the days when what we call the World was not so real with me, and my faults were not confirmed in me."'},
    'P053_1': {'ko': '"그 기분을 이해합니다!" 카턴이 얼굴을 붉히며 외쳤습니다. "그래서 당신은 그것 덕분에 더 나아지셨습니까?"', 'en': '"I understand the feeling!" exclaimed Carton, with a bright flush. "And you are the better for it?"'},
    'P054_1': {'ko': '"그러길 바라오."', 'en': '"I hope so."'},
    'P055_1': {'ko': '카턴은 자리에서 일어나 그가 외투 입는 것을 도와줌으로써 여기서 대화를 끝냈습니다;', 'en': 'Carton terminated the conversation here, by rising to help him on with his outer coat;'},
    'P056_1': {'ko': '"네," 카턴이 말했습니다. "나는 늙지 않았지만, 나의 젊은 시절 방식은 결코 나이 드는 사람을 위한 방식이 아니었습니다.', 'en': '"Yes," said Carton. "I am not old, but my young way was never the way to age.'},
    'P056_2': {'ko': '내 이야기는 이쯤 해두죠."', 'en': 'Enough of me."'},
    'P058_1': {'ko': '"당신과 함께 그녀의 집 앞까지 걷겠습니다.', 'en': '"I\'ll walk with you to her gate.'},
    'P058_2': {'ko': '당신은 나의 방랑하고 불안정한 습관을 알 것입니다.', 'en': 'You know my vagabond and restless habits.'},
    'P058_3': {'ko': '내가 거리를 오랫동안 배회하더라도 불안해하지 마십시오;', 'en': 'If I should prowl about the streets a long time, don\'t be uneasy;'},
    'P058_4': {'ko': '아침에는 다시 나타날 것입니다.', 'en': 'I shall reappear in the morning.'},
    'P058_5': {'ko': '내일 법정에 가십니까?"', 'en': 'You go to the Court to-morrow?"'},
    'P059_1': {'ko': '"네, 불행하게도 그렇소."', 'en': '"Yes, unhappily."'},
    'P060_1': {'ko': '"나도 그곳에 가겠지만, 단지 군중 중 한 명으로서 갈 것입니다.', 'en': '"I shall be there, but only as one of the crowd.'},
    'P060_2': {'ko': '나의 스파이가 내 자리를 마련해 줄 것입니다.', 'en': 'My Spy will find a place for me.'},
    'P060_3': {'ko': '내 팔을 잡으십시오, 선생님."', 'en': 'Take my arm, sir."'},
    'P061_5': {'ko': '카턴은 그를 그곳에 남겨두었습니다;', 'en': 'Carton left him there;'},
    'P061_6': {'ko': '하지만 조금 떨어진 곳에서 서성거리다가, 문이 닫힌 후 다시 문으로 돌아가 그것을 만져보았습니다.', 'en': 'but lingered at a little distance, and turned back to the gate again when it was shut, and touched it.'},
    'P061_7': {'ko': '그는 그녀가 매일 감옥에 간다는 것을 들었습니다. "그녀는 이리로 나와서," 그가 주위를 둘러보며 말했습니다, "이쪽으로 향했고, 이 돌들을 자주 밟았음에 틀림없어.', 'en': 'He had heard of her going to the prison every day. "She came out here," he said, looking about him, "turned this way, must have trod on these stones often.'},
    'P061_8': {'ko': '나도 그녀의 발자취를 따라가야겠어."', 'en': 'Let me follow in her steps."'},
    'P062_1': {'ko': '그녀가 수백 번 서 있었던 라 포르스 감옥 앞에 그가 섰을 때는 밤 10시였습니다.', 'en': 'It was ten o\'clock at night when he stood before the prison of La Force, where she had stood hundreds of times.'},
    'P062_2': {'ko': '몸집이 작은 나무 톱질꾼이 가게 문을 닫고 가게 문 앞에서 파이프를 피우고 있었습니다.', 'en': 'A little wood-sawyer, having closed his shop, was smoking his pipe at his shop-door.'}
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

