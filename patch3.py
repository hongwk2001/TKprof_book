import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_04.json', encoding='utf-8') as f:
    d = json.load(f)

fixes = {
  'P046_1': {'ko': '“선생님, 정말 감사합니다.', 'en': '“Sir, I thank you indeed.'},
  'P046_2': {'ko': '매우 깊이 감사드립니다.', 'en': 'I thank you very gratefully.'},
  'P046_3': {'ko': '은행으로부터 신사분께서 제게 이번 일의 세부 사항을 설명해 주실 것이며, 그것이 놀라운 내용일 테니 마음의 준비를 하라는 말을 들었습니다.', 'en': 'It was told me by the Bank that the gentleman would explain to me the details of the business, and that I must prepare myself to find them of a surprising nature.'},
  'P046_4': {'ko': '최선을 다해 마음의 준비를 했고, 당연히 그 내용이 무엇인지 강렬하고 간절한 관심을 가지고 있습니다.”', 'en': 'I have done my best to prepare myself, and I naturally have a strong and eager interest to know what they are.”'},
  'P047_1': {'ko': '“당연한 일이죠,” Mr.', 'en': '“Naturally,” said Mr.'},
  'P047_2': {'ko': 'Lorry 씨가 말했다. “네--제가--”', 'en': 'Lorry. “Yes--I--”'},
  'P048_1': {'ko': '잠시 말을 멈추었던 그는 다시 귀 옆의 빳빳한 금발 가발을 매만지며 덧붙였다. “말문을 열기가 매우 어렵군요.”', 'en': 'After a pause, he added, again settling the crisp flaxen wig at the ears, “It is very difficult to begin.”'},
  'P049_1': {'ko': '그는 말을 시작하지 못한 채 망설이다가 그녀의 시선과 마주쳤다.', 'en': 'He did not begin, but, in his indecision, met her glance.'},
  'P049_2': {'ko': '젊은 이마가 그 기묘한 표정으로 치켜올라갔지만--그것은 기묘할 뿐만 아니라 예쁘고 특징적이었다--그녀는 마치 스쳐 지나가는 그림자를 무심결에 잡으려 하거나 멈춰 세우려는 듯 손을 들어올렸다.', 'en': 'The young forehead lifted itself into that singular expression--but it was pretty and characteristic, besides being singular--and she raised her hand, as if with an involuntary action she caught at, or stayed some passing shadow.'},
  'P050_1': {'ko': '“선생님은 저를 전혀 모르시나요?”', 'en': '“Are you quite a stranger to me, sir?”'},
  'P051_1': {'ko': '“제가 모를까요?” Mr.', 'en': '“Am I not?” Mr.'},
  'P051_2': {'ko': 'Lorry 씨가 두 손을 펴서 바깥쪽으로 내밀며 따지듯 미소를 지었다.', 'en': 'Lorry opened his hands, and extended them outwards with an argumentative smile.'},
  'P052_1': {'ko': '눈썹 사이, 더없이 섬세하고 고운 선을 가진 작은 여성스러운 코 바로 위에서 표정이 짙어지더니 그녀는 여태껏 서 있던 의자에 생각에 잠긴 채 주저앉았다.', 'en': 'Between the eyebrows and just over the little feminine nose, the line of which was as delicate and fine as it was possible to be, the expression deepened itself as she took her seat thoughtfully in the chair by which she had hitherto remained standing.'},
  'P052_2': {'ko': '그는 그녀가 사색에 잠긴 모습을 지켜보다가, 그녀가 다시 눈을 치켜뜨는 순간 말을 이었다:', 'en': 'He watched her as she mused, and the moment she raised her eyes again, went on:'},
  'P053_1': {'ko': '“아가씨의 양국인 이곳에서 제가 아가씨를 젊은 영국 숙녀, Manette 양으로 대하는 편이 가장 좋겠지요?”', 'en': '“In your adopted country, I presume, I cannot do better than address you as a young English lady, Miss Manette?”'},
  'P054_1': {'ko': '“그러시다면요, 선생님.”', 'en': '“If you please, sir.”'},
  'P055_1': {'ko': '“Manette 양, 저는 사업을 하는 사람입니다.', 'en': '“Miss Manette, I am a man of business.'},
  'P055_2': {'ko': '저에게는 해내야 할 업무상 책임이 있습니다.', 'en': 'I have a business charge to acquit myself of.'},
  'P055_3': {'ko': '제 말을 들으실 때, 저를 그저 말하는 기계라고 생각하고 더 이상 신경 쓰지 마십시오--사실, 저는 그 이상도 아닙니다.', 'en': 'In your reception of it, don’t heed me any more than if I was a speaking machine--truly, I am not much else.'},
  'P055_4': {'ko': '허락하신다면, 아가씨, 저희 고객 중 한 분의 이야기를 해드리겠습니다.”', 'en': 'I will, with your leave, relate to you, miss, the story of one of our customers.”'},
  'P056_1': {'ko': '“이야기요!”', 'en': '“Story!”'},
  'P057_1': {'ko': '그는 그녀가 반복한 단어를 고의로 잘못 알아들은 체하며 서둘러 덧붙였다. “네, 고객이요;', 'en': 'He seemed wilfully to mistake the word she had repeated, when he added, in a hurry, “Yes, customers;'},
  'P057_2': {'ko': '은행업에서는 보통 거래처를 고객이라고 부릅니다.', 'en': 'in the banking business we usually call our connection our customers.'},
  'P057_3': {'ko': '그분은 프랑스 신사였습니다;', 'en': 'He was a French gentleman;'},
  'P057_4': {'ko': '과학자이기도 했고;', 'en': 'a scientific gentleman;'},
  'P057_5': {'ko': '학식이 아주 뛰어난 사람--의사였습니다.”', 'en': 'a man of great acquirements--a Doctor.”'},
  'P058_1': {'ko': '“Beauvais 출신은 아니고요?”', 'en': '“Not of Beauvais?”'},
  'P059_1': {'ko': '“아, 네, Beauvais 출신입니다.', 'en': '“Why, yes, of Beauvais.'},
  'P059_2': {'ko': '아가씨의 아버님인 Manette 씨처럼, 그 신사분도 Beauvais 출신이었죠.', 'en': 'Like Monsieur Manette, your father, the gentleman was of Beauvais.'},
  'P059_3': {'ko': '아가씨의 아버님인 Manette 씨처럼, 그 신사분도 파리에서 명망이 높았습니다.', 'en': 'Like Monsieur Manette, your father, the gentleman was of repute in Paris.'},
  'P059_4': {'ko': '저는 그곳에서 그분을 알게 되는 영광을 누렸습니다.', 'en': 'I had the honour of knowing him there.'},
  'P059_5': {'ko': '우리 관계는 사업상의 관계였지만, 은밀한 사이였지요.', 'en': 'Our relations were business relations, but confidential.'},
  'P059_6': {'ko': '저는 그때 우리 프랑스 상사에 있었고--아! 20년이나 되었군요.”', 'en': 'I was at that time in our French House, and had been--oh! twenty years.”'},
  'P060_1': {'ko': '“그때라면--언제쯤인지 여쭤봐도 될까요, 선생님?”', 'en': '“At that time--I may ask, at what time, sir?”'},
  'P061_1': {'ko': '“아가씨, 20년 전 이야기를 하는 겁니다.', 'en': '“I speak, miss, of twenty years ago.'},
  'P061_2': {'ko': '그분은 영국 숙녀와 결혼하셨고--제가 신탁 관리인 중 한 명이었습니다.', 'en': 'He married--an English lady--and I was one of the trustees.'},
  'P061_3': {'ko': '그분의 일은 다른 많은 프랑스 신사나 프랑스 가문의 일과 마찬가지로 전적으로 Tellson 은행의 손에 달려 있었습니다.', 'en': 'His affairs, like the affairs of many other French gentlemen and French families, were entirely in Tellson’s hands.'},
  'P061_4': {'ko': '비슷한 방식으로 저는 수십 명의 고객들을 위해 어떤 형태로든 신탁 관리인 역할을 하고 있거나 해왔습니다.', 'en': 'In a similar way I am, or I have been, trustee of one kind or other for scores of our customers.'},
  'P061_5': {'ko': '이것은 순전히 사업상의 관계입니다, 아가씨;', 'en': 'These are mere business relations, miss;'},
  'P061_6': {'ko': '여기에는 어떤 우정도 없고, 특별한 관심도 없으며, 감정 같은 것도 없습니다.', 'en': 'there is no friendship in them, no particular interest, nothing like sentiment.'},
  'P061_7': {'ko': '저는 제 사업 인생 동안 이 고객에서 저 고객으로 옮겨 다녔습니다. 하루의 업무 시간 동안 한 고객에서 다른 고객으로 옮겨 다니듯이 말입니다;', 'en': 'I have passed from one to another, in the course of my business life, just as I pass from one of our customers to another in the course of my business day;'},
  'P061_8': {'ko': '간단히 말해, 제게는 감정이 없습니다;', 'en': 'in short, I have no feelings;'},
  'P061_9': {'ko': '저는 그저 기계일 뿐입니다.', 'en': 'I am a mere machine.'},
  'P061_10': {'ko': '계속하자면--”', 'en': 'To go on--”'},
  'P062_1': {'ko': '“하지만 이건 제 아버님 이야기잖아요, 선생님;', 'en': '“But this is my father’s story, sir;'},
  'P062_2': {'ko': '그리고 그런 생각이 들기 시작하네요”--기묘하게 찌푸린 이마가 그를 몹시 주시하고 있었다--“어머님이 아버님보다 2년밖에 더 사시지 못해 제가 고아가 되었을 때 저를 영국으로 데려온 분이 바로 선생님이셨군요.', 'en': 'and I begin to think”--the curiously roughened forehead was very intent upon him--“that when I was left an orphan through my mother’s surviving my father only two years, it was you who brought me to England.'},
  'P062_3': {'ko': '선생님이 틀림없는 것 같아요.”', 'en': 'I am almost sure it was you.”'},
  'P063_1': {'ko': 'Mr.', 'en': 'Mr.'},
  'P063_2': {'ko': 'Lorry 씨는 믿음을 가지고 자신에게 내밀어 온 주저하는 작은 손을 잡아 다소 격식을 차려 입술을 맞추었다.', 'en': 'Lorry took the hesitating little hand that confidingly advanced to take his, and he put it with some ceremony to his lips.'},
  'P063_3': {'ko': '그런 다음 젊은 숙녀를 곧바로 다시 의자로 안내하고는, 왼손으로는 의자 등받이를 잡고 오른손으로는 번갈아 턱을 문지르거나 귀 옆의 가발을 잡아당기거나 자신의 말에 요점을 짚으며, 그녀가 올려다보는 동안 내려다보며 섰다.', 'en': 'He then conducted the young lady straightway to her chair again, and, holding the chair-back with his left hand, and using his right by turns to rub his chin, pull his wig at the ears, or point what he said, stood looking down into her face while she sat looking up into his.'},
  'P064_1': {'ko': '“Manette 양, 그건 _저_였습니다.', 'en': '“Miss Manette, it _was_ I.'},
  'P064_2': {'ko': '그리고 제가 감정이 없고 동료 인간들과 맺는 모든 관계가 순전히 사업상의 관계일 뿐이라고 방금 전 스스로에 대해 얼마나 진실하게 말했는지는, 그 이후로 제가 아가씨를 한 번도 본 적이 없다는 사실을 생각해 보시면 알게 되실 겁니다.', 'en': 'And you will see how truly I spoke of myself just now, in saying I had no feelings, and that all the relations I hold with my fellow-creatures are mere business relations, when you reflect that I have never seen you since.'},
  'P064_3': {'ko': '없습니다;', 'en': 'No;'},
  'P064_4': {'ko': '아가씨는 그 후로 Tellson 상사의 피후견인이 되셨고, 저는 그 후로 Tellson 상사의 다른 업무들로 바빴습니다.', 'en': 'you have been the ward of Tellson’s House since, and I have been busy with the other business of Tellson’s House since.'},
  'P064_5': {'ko': '감정이라니요!', 'en': 'Feelings!'},
  'P064_6': {'ko': '제게는 그럴 시간도, 그럴 기회도 없습니다.', 'en': 'I have no time for them, no chance of them.'},
  'P064_7': {'ko': '아가씨, 제 평생은 거대한 금전의 맹글을 돌리는 데 쓰이고 있습니다.”', 'en': 'I pass my whole life, miss, in turning an immense pecuniary Mangle.”'},
  'P065_1': {'ko': '자신의 일상적인 업무에 대한 이 기묘한 설명이 끝난 뒤, Mr.', 'en': 'After this odd description of his daily routine of employment, Mr.'},
  'P065_2': {'ko': 'Lorry 씨는 두 손으로 금발 가발을 머리에 납작하게 눌렀다가 (그 반짝이는 표면은 그보다 더 납작해질 수 없었기에 그건 전혀 불필요한 행동이었다) 다시 예전의 자세를 취했다.', 'en': 'Lorry flattened his flaxen wig upon his head with both hands (which was most unnecessary, for nothing could be flatter than its shining surface was before), and resumed his former attitude.'},
  'P066_1': {'ko': '“여기까지가, 아가씨 (아가씨가 지적하셨듯), 돌아가신 아버님의 이야기입니다.', 'en': '“So far, miss (as you have remarked), this is the story of your regretted father.'},
  'P066_2': {'ko': '이제 다른 이야기가 시작됩니다.', 'en': 'Now comes the difference.'},
  'P066_3': {'ko': '만약 아버님께서 그때 돌아가시지 않았다면--놀라지 마십시오!', 'en': 'If your father had not died when he did--Don’t be frightened!'},
  'P066_4': {'ko': '어찌 그리 놀라십니까!”', 'en': 'How you start!”'},
  'P067_1': {'ko': '그녀는 정말로 소스라치게 놀랐다.', 'en': 'She did, indeed, start.'},
  'P067_2': {'ko': '그리고 두 손으로 그의 손목을 꽉 잡았다.', 'en': 'And she caught his wrist with both her hands.'},
  'P068_1': {'ko': '“제발,” Mr.', 'en': '“Pray,” said Mr.'},
  'P068_2': {'ko': 'Lorry 씨가 달래는 듯한 목소리로 말하며, 의자 등받이에 얹어둔 왼손을 가져와 너무도 심하게 떨며 그를 부여잡은 애원하는 손가락들 위에 얹었다:', 'en': 'Lorry, in a soothing tone, bringing his left hand from the back of the chair to lay it on the supplicatory fingers that clasped him in so violent a tremble:'},
  'P068_3': {'ko': '“제발 동요를 가라앉히십시오--사업상의 문제입니다.', 'en': '“pray control your agitation--a matter of business.'}
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
