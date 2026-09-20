import json

data_dict = {
"P074_1": {"ko": "'당신이 나를 데리고 들어왔을 때도 나는 허약하고 기진맥진해 있었고, 지금 당신이 나를 데리고 나갈 때는 더 쇠약해져 있소.", "en": "'I was weak and faint when you brought me in, and I am fainter now you take me out."},
"P074_2": {"ko": "이별의 면회가 나를 압도해 버렸소.", "en": "The parting interview has overpowered me."},
"P074_3": {"ko": "이런 일은 이곳에서 종종, 아주 자주 일어났소.", "en": "Such a thing has happened here, often, and too often."},
"P074_4": {"ko": "당신 목숨은 당신 손에 달려 있소.", "en": "Your life is in your own hands."},
"P074_5": {"ko": "빨리! 사람들을 부르시오!'", "en": "Quick! Call assistance!'"},
"P076_1": {"ko": "'이봐, 이 사람아!' 카튼이 발을 구르며 대꾸했다. '내가 이 일을 끝까지 해내겠다고 이미 엄숙하게 맹세하지 않았소? 그런데 지금 이 소중한 시간들을 낭비하는 거요?", "en": "'Man, man!' returned Carton, stamping his foot; 'have I sworn by no solemn vow already, to go through with this, that you waste the precious moments now?"},
"P077_1": {"ko": "스파이는 물러갔고, 카튼은 두 손으로 이마를 짚고 탁자에 앉았다.", "en": "The Spy withdrew, and Carton seated himself at the table, resting his forehead on his hands."},
"P077_2": {"ko": "스파이는 곧바로 두 남자와 함께 돌아왔다.", "en": "The Spy returned immediately, with two men."},
"P084_1": {"ko": "문이 닫히고, 카튼은 홀로 남았다.", "en": "The door closed, and Carton was left alone."},
"P084_2": {"ko": "그는 청력을 극한으로 곤두세운 채, 의심이나 경고를 알릴 만한 어떤 소리라도 들릴까 귀를 기울였다.", "en": "Straining his powers of listening to the utmost, he listened for any sound that might denote suspicion or alarm."},
"P084_3": {"ko": "아무런 소리도 없었다.", "en": "There was none."},
"P084_4": {"ko": "열쇠 돌아가는 소리, 문이 부딪히는 소리, 먼 복도를 따라 지나가는 발소리: 기이해 보이는 외침도, 서두르는 기색도 없었다.", "en": "Keys turned, doors clashed, footsteps passed along distant passages: no cry was raised, or hurry made, that seemed unusual."},
"P084_5": {"ko": "잠시 후 조금 더 편안하게 숨을 쉬며, 그는 탁자에 앉아 시계가 2시를 칠 때까지 다시 귀를 기울였다.", "en": "Breathing more freely in a little while, he sat down at the table, and listened again until the clock struck Two."},
"P085_1": {"ko": "그 의미를 짐작했기에 두렵지 않은 소리들이 이내 들리기 시작했다.", "en": "Sounds that he was not afraid of, for he divined their meaning, then began to be audible."},
"P085_2": {"ko": "여러 개의 문이 차례로 열렸고, 마침내 그의 문이 열렸다.", "en": "Several doors were opened in succession, and finally his own."},
"P085_3": {"ko": "명단을 손에 든 간수 하나가 안을 들여다보며 단순히 말했다. '나를 따라오라, 에브레몽(Evrémonde)!' 그리고 그는 멀리 떨어진 크고 어두운 방으로 간수를 따라갔다.", "en": "A gaoler, with a list in his hand, looked in, merely saying, 'Follow me, Evrémonde!' and he followed into a large dark room, at a distance."},
"P085_4": {"ko": "어두운 겨울날이었고, 안팎의 그림자 때문에 팔이 묶이기 위해 그곳에 끌려온 다른 사람들을 희미하게 식별할 수 있을 뿐이었다.", "en": "It was a dark winter day, and what with the shadows within, and what with the shadows without, he could but dimly discern the others who were brought there to have their arms bound."},
"P085_5": {"ko": "어떤 이들은 서 있었고 어떤 이들은 앉아 있었다.", "en": "Some were standing; some seated."},
"P085_6": {"ko": "탄식하며 안절부절못하는 이들도 있었으나 소수에 불과했다.", "en": "Some were lamenting, and in restless motion; but, these were few."},
"P085_7": {"ko": "대다수는 말없이 고요하게 땅을 응시하고 있었다.", "en": "The great majority were silent and still, looking fixedly at the ground."},
"P086_1": {"ko": "그가 어두운 구석의 벽 곁에 서 있는 동안, 쉰두 명 중 일부가 그를 뒤따라 들어왔고 그중 한 남자가 지나가다 멈춰 서서 그를 아는 체하며 포옹했다.", "en": "As he stood by the wall in a dim corner, while some of the fifty-two were brought in after him, one man stopped in passing, to embrace him, as having a knowledge of him."},
"P086_2": {"ko": "발각될까 봐 큰 두려움에 몸서리쳤지만, 그 남자는 그냥 지나갔다.", "en": "It thrilled him with a great dread of discovery; but the man went on."},
"P086_3": {"ko": "그로부터 아주 잠시 후, 핏기가 전혀 없는 예쁘고 야윈 얼굴에 인내심을 담아 커다랗게 뜬 눈을 가진, 가냘픈 소녀 같은 모습의 젊은 여자가 그가 관찰했던 자리에서 일어나 그에게 말을 걸러 다가왔다.", "en": "A very few moments after that, a young woman, with a slight girlish form, a sweet spare face in which there was no vestige of colour, and large widely opened patient eyes, rose from the seat where he had observed her sitting, and came to speak to him."},
"P088_1": {"ko": "그가 중얼거리듯 대답했다. '그렇소.", "en": "He murmured for answer: 'True."},
"P088_2": {"ko": "무슨 죄목이었는지 깜빡했군?'", "en": "I forget what you were accused of?'"},
"P089_1": {"ko": "'음모요.", "en": "'Plots."},
"P089_2": {"ko": "하지만 공의로우신 하늘은 제가 아무런 잘못이 없다는 것을 아시지요.", "en": "Though the just Heaven knows that I am innocent of any."},
"P089_3": {"ko": "그게 말이 되나요?", "en": "Is it likely?"},
"P089_4": {"ko": "나같이 가엾고 작고 연약한 존재와 음모를 꾸밀 생각을 누가 하겠어요?'", "en": "Who would think of plotting with a poor little weak creature like me?'"},
"P091_1": {"ko": "'죽는 것은 두렵지 않아요, 시민 에브레몽, 하지만 전 아무 짓도 하지 않았어요.", "en": "'I am not afraid to die, Citizen Evrémonde, but I have done nothing."},
"P091_2": {"ko": "우리 같은 가난한 사람들에게 많은 선행을 베풀 공화국(Republic)이 저의 죽음으로 이익을 얻는다면 죽는 것을 마다하지 않겠어요. 하지만 그것이 어떻게 가능한지 모르겠어요, 시민 에브레몽.", "en": "I am not unwilling to die, if the Republic which is to do so much good to us poor, will profit by my death; but I do not know how that can be, Citizen Evrémonde."},
"P091_3": {"ko": "이렇게 가엾고 약하고 작은 존재인데!'", "en": "Such a poor weak little creature!'"},
"P093_1": {"ko": "'풀려나셨다고 들었는데, 시민 에브레몽.'", "en": "'I heard you were released, Citizen Evrémonde.'"}
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
