import json

translations = {
    0: {"ko": "미덕(Virtue)이란, 시인들이 관찰한 바와 같이 (검찰총장은 배심원들이 그 구절들을 토씨 하나 틀리지 않고 입가에 맴돌 정도로 잘 알고 있을 것이라 확신했습니다만),", "en": "Virtue, as observed by the poets (in passages the Attorney-General was sure the jury knew word for word, ready to quote),"},
    1: {"ko": "(이 말에 배심원들의 얼굴에는 그 구절들에 대해 아무것도 모른다는 죄책감 섞인 당혹감이 드러났습니다) 어느 정도 전염성이 있다는 것이었습니다.", "en": "(at which the jury's faces showed a guilty awareness that they knew nothing about those passages) was somewhat contagious;"},
    2: {"ko": "특히 애국심(patriotism), 즉 조국에 대한 사랑으로 알려진 빛나는 미덕은 더욱 그러하다는 것이었습니다.", "en": "especially the shining virtue known as patriotism, or love for one's country."},
    3: {"ko": "또한, 비록 보잘것없는 자신이지만 언급하는 것조차 영광인, 이 결백하고 흠잡을 데 없는 국왕 측 증인의 숭고한 모범(lofty example)이 죄수의 하인에게 전해져, 그 하인으로 하여금 주인의 책상 서랍과 주머니를 뒤지고 서류를 몰래 빼내려는 거룩한 결의(holy determination)를 품게 했다는 것이었습니다.", "en": "Furthermore, the noble example of this flawless and unimpeachable witness for the Crown—whom it was an honor merely to mention, however inadequately—had influenced the prisoner's servant, inspiring him with a sacred resolve to search his master's desk drawers and pockets, and secretly remove his papers."},
    4: {"ko": "자신(검찰총장)은 이 훌륭한 하인에 대해 어떤 식으로든 비하하려는(disparagement) 시도를 들을 각오가 되어 있다는 것이었습니다.", "en": "He (the Attorney-General) was prepared to hear some attempts to belittle this admirable servant;"},
    5: {"ko": "하지만 일반적으로 자신은 그 하인을 자신의(검찰총장 본인의) 형제자매보다 더 좋아하며, 자신의", "en": "but generally speaking, he preferred the servant to his own (the Attorney-General's) brothers and sisters, and respected him more than his own"},
    6: {"ko": "(검찰총장 본인의) 부모님보다 그를 더 존경한다는 것이었습니다.", "en": "(the Attorney-General's) father and mother."},
    7: {"ko": "그래서 그는 배심원단에게 자신 있게 나서서 이와 같이 행동해 줄 것을 촉구했습니다.", "en": "He confidently urged the jury to step forward and do the same."},
    8: {"ko": "이 두 증인의 증언과 그들이 발견하여 제출될 문서들을 함께 살펴보면, 죄수가 육해공 양면으로 국왕 폐하의 군대 목록과 그 부대 배치 및 준비 상황에 대한 정보를 제공받았음을 보여줄 것이며, 그가 그러한 정보를 적국(hostile power)에 상습적으로 넘겼다는 사실에 추호의 의심도 남기지 않을 것이라는 점이었습니다.", "en": "The testimony of these two witnesses, combined with the documents they discovered which would be presented, would show that the prisoner had received lists of His Majesty's military forces, including their deployment and readiness by land and sea, leaving no doubt that he habitually passed such information to an enemy power."},
    9: {"ko": "물론 이 문서들이 죄수의 필적(handwriting)으로 작성되었다는 것을 증명할 수는 없다는 것이었습니다.", "en": "Of course, it could not be proven that these lists were in the prisoner's handwriting;"},
    10: {"ko": "하지만 그것은 매한가지(all the same)로 아무 상관이 없다는 점이었습니다.", "en": "but that made no difference at all;"},
    11: {"ko": "참으로, 그것은 죄수가 자신의 범행을 은폐하는 데 매우 교묘했다(artful in his precautions)는 것을 보여주기 때문에 오히려 검찰 측에 유리하다는 것이었습니다.", "en": "in fact, it was rather advantageous for the prosecution, as it showed the prisoner was cunning in covering his tracks."},
    12: {"ko": "그 증거는 5년 전으로 거슬러 올라가며, 영국군과 미국인들(Americans) 사이에 벌어진 최초의 전투가 일어나기 불과 몇 주 전에 이미 죄수가 이토록 치명적인 간첩 임무(pernicious missions)에 가담하고 있었음을 보여줄 것이라는 점이었습니다.", "en": "The evidence would date back five years, showing the prisoner was already involved in these deadly spy missions just a few weeks before the very first battle between British troops and the Americans."},
    13: {"ko": "이러한 이유들로 인해, 배심원단은 (그가 알고 있듯) 충성스러운 배심원들이고, (그들 스스로 알고 있듯) 책임감 있는 배심원들이므로, 그들이 원하든 원하지 않든 반드시 죄수에게 유죄 판결을 내리고 그의 목숨을 끝장내야 한다는 것이었습니다.", "en": "For these reasons, the jury—being a loyal jury (as he knew they were) and a responsible jury (as they themselves knew they were)—must absolutely find the prisoner Guilty and finish him off, regardless of whether they wanted to or not."},
    14: {"ko": "그렇지 않으면, 그들은 결코 베개에 머리를 눕히고 편히 잠들 수 없을 것이라는 점이었습니다.", "en": "Otherwise, they would never be able to rest their heads peacefully on their pillows;"},
    15: {"ko": "또한, 그들은 자신들의 아내들이 베개에 머리를 눕히는 것조차 도저히 견딜 수 없을 것이라는 점이었습니다.", "en": "they could never tolerate the thought of their wives resting their heads on their pillows;"},
    16: {"ko": "그리고 자신들의 아이들이 베개에 머리를 눕히는 상상조차 결코 참을 수 없을 것이라는 점이었습니다.", "en": "and they could never endure the idea of their children resting their heads on their pillows;"},
    17: {"ko": "요컨대, 죄수의 목이 날아가지(taken off) 않는 한, 그들이나 그들의 가족이 베개에 머리를 눕히고 잠을 청하는 일은 두 번 다시 없을 것이라는 것이었습니다.", "en": "in short, there could be no more resting of heads on pillows for them or their families unless the prisoner's head was cut off."},
    18: {"ko": "검찰총장은 자신이 생각할 수 있는 강력한 의미를 담은 모든 것들의 이름으로, 그리고 이미 죄수를 죽어서 사라진 것이나 다름없는 사람으로 간주하고 있다는 자신의 엄숙한 단언(solemn asseveration)에 걸고, 배심원들에게 그 머리를 내놓을 것을 요구하며 발언을 마쳤습니다.", "en": "The Attorney-General concluded by demanding that head from them, in the name of every weighty concept he could think of, and on the strength of his solemn declaration that he already considered the prisoner as good as dead and gone."},
    19: {"ko": "검찰총장의 연설이 끝나자, 마치 커다란 금파리 떼(great blue-flies)가 죄수가 곧 시체가 될 것을 예상하고 그의 주변으로 몰려드는 것처럼 법정 안에 웅성거리는 소리가 일었습니다.", "en": "When the Attorney-General finished, a buzzing sound filled the courtroom, as if a swarm of large blue-flies were gathering around the prisoner, anticipating the corpse he was soon to become."},
    20: {"ko": "소란이 다시 가라앉았을 때, 흠잡을 데 없는 애국자가 증인석에 나타났습니다.", "en": "When the noise quieted down again, the flawless patriot appeared in the witness box."},
    21: {"ko": "이어 법무차관(Solicitor-General)이 상관의 뜻에 따라 그 애국자를 심문했습니다.", "en": "Then the Solicitor-General, following his superior's lead, questioned the patriot:"},
    22: {"ko": "이름은 존 바사드(John Barsad), 신분은 신사(gentleman)였습니다.", "en": "His name was John Barsad, a gentleman."},
    23: {"ko": "그의 순결한 영혼에 대한 이야기는 검찰총장이 묘사한 것과 정확히 일치했는데, 굳이 흠을 잡자면 조금 지나치게 정확하다는 것이었습니다.", "en": "The story of his pure soul matched exactly what the Attorney-General had described—perhaps, if it had any flaw, it matched a little too perfectly."},
    24: {"ko": "그는 자신의 고결한 가슴속에 있던 짐을 내려놓은 뒤 겸손하게 물러나려 했으나, Lorry(로리) 씨에게서 멀지 않은 곳에 서류를 앞에 두고 앉아 있던 가발을 쓴 신사(wigged gentleman)가 몇 가지 질문을 허락해 달라고 청하는 바람에 그러지 못했습니다.", "en": "After unloading the burden from his noble heart, he would have modestly stepped down, except that the wig-wearing gentleman sitting near Mr. Lorry, with papers in front of him, asked to put a few questions to him."},
    25: {"ko": "그 반대편에 앉아 있던 가발을 쓴 다른 신사는 여전히 법정의 천장만을 바라보고 있었습니다.", "en": "Another wig-wearing gentleman sitting opposite him was still staring at the courtroom ceiling."},
    26: {"ko": "그 자신이 스파이 노릇을 한 적이 있는지?", "en": "Had he ever been a spy himself?"},
    27: {"ko": "아닙니다, 그는 그런 비열한 암시(base insinuation)를 경멸했습니다.", "en": "No, he despised such a shameful implication."},
    28: {"ko": "무엇으로 생계를 유지하는지?", "en": "How did he make a living?"},
    29: {"ko": "그의 재산으로 유지한다고 했습니다.", "en": "Off his property."},
    30: {"ko": "그의 재산은 어디에 있는지?", "en": "Where was his property located?"},
    31: {"ko": "그는 그것이 어디에 있는지 정확히 기억하지 못했습니다.", "en": "He couldn't exactly remember where it was."},
    32: {"ko": "그것이 대체 무엇인지?", "en": "What exactly was it?"},
    33: {"ko": "남이 알 바 아니라고 했습니다.", "en": "It was nobody's business."},
    34: {"ko": "그것을 물려받았는지?", "en": "Had he inherited it?"},
    35: {"ko": "네, 그렇다고 했습니다.", "en": "Yes, he had."},
    36: {"ko": "누구에게서 물려받았는지?", "en": "From whom?"},
    37: {"ko": "먼 친척에게서라고 했습니다.", "en": "A distant relative."},
    38: {"ko": "매우 먼 친척인지?", "en": "A very distant one?"},
    39: {"ko": "다소 그렇다고 했습니다.", "en": "Rather distant."},
    40: {"ko": "감옥에 간 적이 있는지?", "en": "Had he ever been in prison?"},
    41: {"ko": "절대 없다고 했습니다.", "en": "Absolutely not."},
    42: {"ko": "채무자 감옥(debtors' prison)에 갇힌 적도 없는지?", "en": "Never in a debtors' prison?"},
    43: {"ko": "그것이 이 사건과 무슨 상관인지 모르겠다고 대답했습니다.", "en": "He didn't see what that had to do with the case."},
    44: {"ko": "채무자 감옥에 간 적이 결코 없단 말인가? 자, 다시 한 번 묻겠네.", "en": "Never in a debtors' prison? Come now, answer again."},
    45: {"ko": "결코 없었는지?", "en": "Never?"},
    46: {"ko": "그렇다고 했습니다. (예, 간 적 있습니다.)", "en": "Yes, he had."},
    47: {"ko": "몇 번이나 갔는지?", "en": "How many times?"},
    48: {"ko": "두세 번이라고 했습니다.", "en": "Two or three times."},
    49: {"ko": "대여섯 번은 아닌지?", "en": "Not five or six times?"},
    50: {"ko": "아마 그럴지도 모른다고 했습니다.", "en": "Perhaps."},
    51: {"ko": "직업이 무엇인지?", "en": "What was his profession?"},
    52: {"ko": "신사(Gentleman)라고 대답했습니다.", "en": "A gentleman."},
    53: {"ko": "발길질을 당한 적이 있는지?", "en": "Had he ever been kicked?"},
    54: {"ko": "그랬을지도 모른다고 했습니다.", "en": "He might have been."},
    55: {"ko": "자주 그랬는지?", "en": "Frequently?"},
    56: {"ko": "아니라고 했습니다.", "en": "No."},
    57: {"ko": "계단 아래로 차인 적이 있는지?", "en": "Had he ever been kicked down the stairs?"},
    58: {"ko": "단연코 없다고 했습니다;", "en": "Absolutely not;"},
    59: {"ko": "한 번은 계단 꼭대기에서 발로 차인 적이 있지만, 그 후로는 자기 발로 알아서 굴러떨어졌다고(fell downstairs of his own accord) 주장했습니다.", "en": "he once received a kick at the top of the stairs, but fell down the rest of the way on his own."},
    60: {"ko": "그때 주사위 사기를 치다(cheating at dice) 차인 것은 아닌지?", "en": "Was he kicked on that occasion for cheating at dice?"},
    61: {"ko": "폭행을 저지른 술 취한 거짓말쟁이가 그런 식의 말을 하긴 했지만, 사실이 아니라고 했습니다.", "en": "The drunken liar who assaulted him said something like that, but it wasn't true."},
    62: {"ko": "사실이 아니라고 맹세할 수 있는지?", "en": "Could he swear it wasn't true?"},
    63: {"ko": "확실히 맹세할 수 있다고 했습니다.", "en": "Absolutely."},
    64: {"ko": "도박에서 속임수를 써서(cheating at play) 생계를 유지한 적이 있는지?", "en": "Had he ever made a living by cheating at gambling?"},
    65: {"ko": "결코 없다고 했습니다.", "en": "Never."},
    66: {"ko": "도박으로 생계를 유지한 적은 있는지?", "en": "Had he ever made a living by gambling?"},
    67: {"ko": "다른 신사들이 하는 정도 이상은 아니라고 했습니다.", "en": "No more than other gentlemen do."},
    68: {"ko": "죄수에게 돈을 빌린 적이 있는지?", "en": "Had he ever borrowed money from the prisoner?"},
    69: {"ko": "그렇다고 대답했습니다.", "en": "Yes."},
    70: {"ko": "그 돈을 갚았는지?", "en": "Had he ever paid him back?"},
    71: {"ko": "아니라고 했습니다.", "en": "No."},
    72: {"ko": "죄수와의 이런 친분이란 사실 매우 얄팍한 것이며, 마차나 여관, 여객선(packets) 등에서 죄수에게 강요한 친분이 아닌지?", "en": "Wasn't this friendship with the prisoner actually very superficial, and forced upon the prisoner in stagecoaches, inns, and passenger ships?"},
    73: {"ko": "아니라고 대답했습니다.", "en": "No."},
    74: {"ko": "죄수가 이 목록들을 가지고 있는 것을 확실히 보았는지?", "en": "Was he sure he saw the prisoner with these lists?"},
    75: {"ko": "확실하다고 대답했습니다.", "en": "Certain."},
    76: {"ko": "그 목록들에 대해 더 아는 것은 없는지?", "en": "Did he know anything more about the lists?"},
    77: {"ko": "없다고 했습니다.", "en": "No."},
    78: {"ko": "예를 들어, 그 목록들을 본인이 직접 구한 것은 아닌지?", "en": "Had he not obtained them himself, for instance?"},
    79: {"ko": "아니라고 했습니다.", "en": "No."},
    80: {"ko": "이 증언을 통해 무언가 대가를 바라고 있는지?", "en": "Did he expect to get anything in return for this testimony?"},
    81: {"ko": "아니라고 했습니다.", "en": "No."},
    82: {"ko": "덫을 놓기 위해(to lay traps) 정부에 정식으로 고용되어 정기적인 보수를 받고 있는 것은 아닌지?", "en": "Was he not regularly employed and paid by the government to set traps?"},
    83: {"ko": "오, 절대 아니라고 했습니다.", "en": "Oh, absolutely not."},
    84: {"ko": "아니면 다른 무슨 일이라도 하기 위해 고용된 것은 아닌지?", "en": "Or to do anything else for them?"},
    85: {"ko": "오, 절대 아니라고 거듭 부인했습니다.", "en": "Oh, absolutely not."},
    86: {"ko": "그것을 맹세할 수 있는지?", "en": "Could he swear to that?"}
}

queue_file = 'c:/git_repo/TKprof_book/work_queue.json'
with open(queue_file, 'r', encoding='utf-8') as f:
    q = json.load(f)

# we need to find the specific items for book2_ch_03
# the user said we are strictly responsible for blocks at index 0 through 86 (87 blocks total) of work_queue.json
# let's assume q is a flat list
my_ids = []
for i in range(87):
    q[i]['ko'] = translations[i]['ko']
    q[i]['en'] = translations[i]['en']
    q[i]['status'] = 'done'
    my_ids.append(q[i]['id'])

# write back to work_queue.json
with open(queue_file, 'w', encoding='utf-8') as f:
    json.dump(q, f, ensure_ascii=False, indent=2)

# Now patch the actual chapter file
chapter_file = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_03.json'
with open(chapter_file, 'r', encoding='utf-8') as f:
    chap = json.load(f)

# map translations by id
updates = {q[i]['id']: translations[i] for i in range(87)}

for item in chap:
    if item['id'] in updates:
        item['ko'] = updates[item['id']]['ko']
        item['en'] = updates[item['id']]['en']

with open(chapter_file, 'w', encoding='utf-8') as f:
    json.dump(chap, f, ensure_ascii=False, indent=2)

print("Successfully translated and patched 87 blocks.")
