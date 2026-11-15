import json
import codecs

filepath = 'c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_09.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    'P024_1': {'ko': '"불쌍한 다네이 이야기로 돌아가서요," 카턴이 말했습니다. "그녀에게 이 면담이나 이 합의에 대해 말하지 마십시오.', 'en': '"To return to poor Darnay," said Carton. "Don\'t tell Her of this interview, or this arrangement.'},
    'P024_2': {'ko': '그렇다고 그녀가 그를 보러 갈 수 있게 되는 것도 아닐 테니까요.', 'en': 'It would not enable Her to go to see him.'},
    'P024_3': {'ko': '그녀는 최악의 경우를 대비하여 그에게 선고를 앞당길 수 있는 수단(자살)을 전달하기 위해 꾸며진 일이라고 생각할지도 모릅니다."', 'en': 'She might think it was contrived, in case of the worse, to convey to him the means of anticipating the sentence."'},
    'P025_3': {'ko': '그래 보였습니다;', 'en': 'It seemed to be;'},
    'P025_4': {'ko': '그는 그 시선을 마주 보았고, 분명히 그것을 이해했습니다.', 'en': 'he returned the look, and evidently understood it.'},
    'P026_1': {'ko': '"그녀는 수천 가지 생각을 할지도 모릅니다," 카턴이 말했습니다, "그리고 그중 어떤 것도 그녀의 걱정만 더할 뿐일 것입니다.', 'en': '"She might think a thousand things," Carton said, "and any of them would only add to her trouble.'},
    'P026_2': {'ko': '그녀에게 내 이야기는 하지 마십시오.', 'en': 'Don\'t speak of me to her.'},
    'P026_3': {'ko': '내가 처음 왔을 때 당신에게 말했듯, 나는 그녀를 만나지 않는 편이 낫습니다.', 'en': 'As I said to you when I first came, I had better not see her.'},
    'P026_4': {'ko': '그러지 않고도, 내 손이 찾을 수 있는 그녀를 위한 조그만 도움이라도 주기 위해 내 손을 내밀 수는 있습니다.', 'en': 'I can put my hand out to do any little helpful work for her that my hand can find to do, without that.'},
    'P026_5': {'ko': '그녀에게 가시는 거겠죠?', 'en': 'You are going to her, I hope?'},
    'P026_6': {'ko': '그녀는 오늘 밤 매우 쓸쓸할 것입니다."', 'en': 'She must be very desolate to-night."'},
    'P027_1': {'ko': '"지금 바로 갈 것입니다."', 'en': '"I am going now, directly."'},
    'P028_1': {'ko': '"그거 다행이군요.', 'en': '"I am glad of that.'},
    'P028_2': {'ko': '그녀는 당신에게 강한 애착과 의지를 갖고 있으니까요.', 'en': 'She has such a strong attachment to you and reliance on you.'},
    'P028_3': {'ko': '그녀는 어때 보입니까?"', 'en': 'How does she look?"'},
    'P029_1': {'ko': '"불안해하고 불행해 보이지만, 아주 아름답습니다."', 'en': '"Anxious and unhappy, but very beautiful."'},
    'P030_1': {'ko': '"아!"', 'en': '"Ah!"'},
    'P031_1': {'ko': '그것은 한숨처럼, 거의 흐느낌처럼 길고 슬픈 소리였습니다.', 'en': 'It was a long, grieving sound, like a sigh--almost like a sob.'},
    'P031_4': {'ko': '한 줄기 빛, 혹은 그늘이 (그 노신사는 어느 쪽인지 말할 수 없었을 것입니다) 거칠고 밝은 날 산비탈을 휩쓸고 지나가는 변화처럼 그의 얼굴을 빠르게 스쳐 지나갔고, 그는 앞으로 굴러떨어지는 불타는 작은 장작 하나를 제자리로 돌려놓으려 발을 들어 올렸습니다.', 'en': 'A light, or a shade (the old gentleman could not have said which), passed from it as swiftly as a change will sweep over a hillside on a wild bright day, and he lifted his foot to put back one of the little flaming logs, which was tumbling forward.'},
    'P031_5': {'ko': '그는 당시 유행하던 흰색 승마 코트와 톱부츠(목이 긴 장화)를 신고 있었는데, 장작불빛이 그 밝은 표면에 닿자 길고 다듬지 않은 갈색 머리를 늘어뜨린 그의 모습은 매우 창백해 보였습니다.', 'en': 'He wore the white riding-coat and top-boots, then in vogue, and the light of the fire touching their light surfaces made him look very pale, with his long brown hair, all untrimmed, hanging loose about him.'},
    'P031_8': {'ko': '불타는 장작이 발의 무게에 부서졌을 때에도 그의 부츠는 여전히 뜨거운 잉걸불 위에 있었습니다.', 'en': 'his boot was still upon the hot embers of the flaming log, when it had broken under the weight of his foot.'},
    'P032_1': {'ko': '"잊고 있었습니다," 그가 말했습니다.', 'en': '"I forgot it," he said.'},
    'P033_3': {'ko': '그 타고난 잘생긴 이목구비를 흐리게 하는 수척한 분위기를 알아차리고, 또 죄수들의 얼굴 표정이 아직 그의 마음속에 생생하게 남아 있던 터라, 그는 강렬하게 그 표정을 떠올리게 되었습니다.', 'en': 'Taking note of the wasted air which clouded the naturally handsome features, and having the expression of prisoners\' faces fresh in his mind, he was strongly reminded of that expression.'},
    'P034_1': {'ko': '"그리고 이곳에서의 당신의 임무도 끝나가고 있습니까, 선생님?" 그에게 돌아보며 카턴이 말했습니다.', 'en': '"And your duties here have drawn to an end, sir?" said Carton, turning to him.'},
    'P035_1': {'ko': '"네.', 'en': '"Yes.'},
    'P035_2': {'ko': '어젯밤 루시가 그렇게 예기치 않게 들어왔을 때 당신에게 말했듯, 마침내 나는 이곳에서 할 수 있는 모든 것을 다 했습니다.', 'en': 'As I was telling you last night when Lucie came in so unexpectedly, I have at length done all that I can do here.'},
    'P035_3': {'ko': '나는 그들을 완벽하게 안전한 상태로 남겨두고, 파리를 떠나기를 바랐습니다.', 'en': 'I hoped to have left them in perfect safety, and then to have quitted Paris.'},
    'P035_4': {'ko': '내게는 통행증이 있습니다.', 'en': 'I have my Leave to Pass.'},
    'P035_5': {'ko': '나는 떠날 준비가 되어 있었습니다."', 'en': 'I was ready to go."'},
    'P036_1': {'ko': '그들은 둘 다 말이 없었습니다.', 'en': 'They were both silent.'},
    'P037_1': {'ko': '"선생님께서 돌아보시는 삶은 참으로 기시군요?" 카턴이 생각에 잠겨 말했습니다.', 'en': '"Yours is a long life to look back upon, sir?" said Carton, wistfully.'},
    'P038_1': {'ko': '"일흔여덟 살입니다."', 'en': '"I am in my seventy-eighth year."'},
    'P039_1': {'ko': '"평생 동안 쓸모 있는 분이셨군요;', 'en': '"You have been useful all your life;'},
    'P039_2': {'ko': '꾸준하고 변함없이 바쁘셨고;', 'en': 'steadily and constantly occupied;'},
    'P039_3': {'ko': '신뢰받고, 존경받고, 우러러보임을 받으셨죠?"', 'en': 'trusted, respected, and looked up to?"'},
    'P040_1': {'ko': '"나는 어른이 된 이후로 줄곧 사업가였습니다.', 'en': '"I have been a man of business, ever since I have been a man.'},
    'P040_2': {'ko': '실로, 나는 소년 시절에도 사업가였다고 말할 수 있겠군요."', 'en': 'Indeed, I may say that I was a man of business when a boy."'},
    'P041_1': {'ko': '"일흔여덟의 나이에 얼마나 큰 자리를 차지하고 계신지 보십시오.', 'en': '"See what a place you fill at seventy-eight.'},
    'P041_2': {'ko': '당신이 그 자리를 비울 때 얼마나 많은 사람들이 당신을 그리워하겠습니까!"', 'en': 'How many people will miss you when you leave it empty!"'},
    'P043_1': {'ko': '"어떻게 그런 말을 할 수 있죠?', 'en': '"How can you say that?'}
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

