import json

data_dict = {
"P017_1": {"ko": "그는 마지막 시간이 3시라고 통보받았고, 사형수 호송차가 거리를 무겁고 느리게 덜컹거리며 지나가야 하므로 그보다 더 일찍 소환될 것임을 알고 있었다.", "en": "He had been informed that the final hour was Three, and he knew he would be summoned somewhat earlier, since the tumbrils jolted heavily and slowly through the streets."},
"P017_2": {"ko": "그러므로 그는 2시를 그 시간으로 마음속에 정해두고, 그 사이 스스로를 강하게 다잡아 그 시간 이후에는 다른 사람들에게 힘을 줄 수 있게 되기로 결심했다.", "en": "Therefore, he decided to fix Two in his mind as the hour, and to strengthen himself in the interval so that, after that time, he might be able to strengthen others."},
"P018_1": {"ko": "가슴에 팔을 엇갈려 안은 채 규칙적으로 이리저리 걷는 그는 라 포르스 감옥에서 서성였던 그 죄수와는 완전히 다른 사람이 되어, 1시가 자신에게서 멀어지는 종소리를 놀라지 않고 들었다.", "en": "Pacing regularly to and fro with his arms folded across his chest, a completely different man from the prisoner who had paced back and forth at La Force, he heard One strike away from him without any surprise."},
"P018_2": {"ko": "그 시간은 여느 다른 시간들과 마찬가지로 흘러갔다.", "en": "The hour had measured out like most other hours."},
"P018_3": {"ko": "평정심을 되찾은 것에 대해 하늘에 깊이 감사하며 그는 '이제 한 시간밖에 남지 않았군'이라고 생각하고 다시 몸을 돌려 걸었다.", "en": "Deeply thankful to Heaven for recovering his self-possession, he thought, 'There is only one more hour left now,' and turned to walk again."},
"P019_1": {"ko": "문밖 돌복도에서 발소리가 났다.", "en": "There were footsteps in the stone hallway outside the door."},
"P019_2": {"ko": "그는 멈춰 섰다.", "en": "He stopped."},
"P020_1": {"ko": "열쇠가 자물쇠에 꽂히고 돌아갔다.", "en": "The key was inserted into the lock and turned."},
"P020_2": {"ko": "문이 열리기 전, 혹은 문이 열릴 때 어떤 남자가 영어로 낮게 말했다: '저자는 여기서 나를 본 적이 없소. 난 줄곧 그의 눈에 띄지 않게 피했으니까.", "en": "Before the door opened, or just as it opened, a man said in a low voice in English: 'He has never seen me here; I have kept out of his sight."},
"P020_3": {"ko": "당신 혼자 들어가시오. 난 근처에서 기다리겠소.", "en": "You go in alone; I will wait nearby."},
"P020_4": {"ko": "시간을 지체하지 마시오!'", "en": "Don't waste any time!'"},
"P022_1": {"ko": "그의 표정에는 너무나도 밝고 놀라운 무언가가 있어서 처음 그 순간, 죄수는 그를 자기 상상이 만들어낸 환영이 아닌가 의심했다.", "en": "There was something so bright and remarkable in his appearance that, for the first moment, the prisoner suspected him to be an apparition created by his own imagination."},
"P022_2": {"ko": "하지만 그가 말했고 그것은 그의 목소리였다. 그가 죄수의 손을 잡았고 그것은 진짜 그의 손길이었다.", "en": "But then he spoke, and it was his voice; he took the prisoner's hand, and it was a real grasp."},
"P024_1": {"ko": "'당신일 거라곤 믿을 수 없었소.", "en": "'I could not believe it was you."},
"P024_2": {"ko": "지금도 거의 믿기지 않소.", "en": "I can hardly believe it even now."},
"P024_3": {"ko": "당신도 설마...' 갑자기 두려움이 그의 뇌리를 스쳤다. '...죄수요?'", "en": "Are you not'—a sudden fear crossed his mind—'a prisoner?'"},
"P025_1": {"ko": "'아닙니다.", "en": "'No."},
"P025_2": {"ko": "저는 우연히 이곳 간수 중 한 명에 대한 통제력을 얻게 되었고, 그 힘 덕분에 당신 앞에 서 있는 겁니다.", "en": "I accidentally gained a power over one of the guards here, and by virtue of that power, I stand before you."},
"P025_3": {"ko": "그녀, 즉 당신의 아내가 저를 보냈습니다, 친애하는 다네이.'", "en": "I have come from her—your wife, dear Darnay.'"},
"P031_1": {"ko": "'제가 왜 이걸 가져왔는지, 무슨 의미인지 물어볼 시간이 없습니다; 제게도 그걸 말해줄 시간이 없고요.", "en": "'You have no time to ask me why I brought this, or what it means; and I have no time to tell you."},
"P031_2": {"ko": "당신은 무조건 따라야 합니다--지금 신고 있는 장화를 벗고 내 장화를 신으십시오.'", "en": "You must simply comply—take off the boots you are wearing, and put on these boots of mine.'"},
"P032_1": {"ko": "감방 벽 쪽, 죄수 등 뒤로 의자가 하나 있었다.", "en": "There was a chair against the cell wall, behind the prisoner."},
"P032_2": {"ko": "카튼이 앞으로 밀어붙이듯 다가가 번개 같은 속도로 그를 의자에 주저앉혔고, 맨발로 그를 내려다보며 섰다.", "en": "Carton, pushing forward, had already forced him down into it with lightning speed, and stood over him, barefoot."},
"P033_1": {"ko": "'내 장화를 신으십시오.", "en": "'Put on these boots of mine."},
"P033_2": {"ko": "그 장화로 손을 움직이고, 의지를 집중하십시오.", "en": "Use your hands on them; put your will into them."},
"P033_3": {"ko": "빨리요!'", "en": "Quickly!'"},
"P034_1": {"ko": "'카튼, 이 곳에서는 결코 탈출할 수 없소; 절대로 불가능한 일이오.", "en": "'Carton, there is no escaping from this place; it can never be done."},
"P034_2": {"ko": "당신은 그저 나와 함께 죽게 될 뿐이오.", "en": "You will only end up dying with me."},
"P034_3": {"ko": "이건 미친 짓이오.'", "en": "This is madness.'"},
"P035_1": {"ko": "'제가 당신에게 탈출하자고 했다면 미친 짓이겠죠; 하지만 제가 그렇게 말했습니까?", "en": "'It would be madness if I asked you to escape; but do I?"},
"P035_2": {"ko": "제가 저 문 밖으로 나가자고 할 때, 그게 미친 짓이라고 말하고 여기에 남으십시오.", "en": "When I ask you to pass out that door, tell me it is madness and remain here."},
"P035_3": {"ko": "그 크라바트를 내 것과 바꾸고, 그 코트도 내 것과 바꾸십시오.", "en": "Exchange that cravat for mine, and that coat for mine."},
"P035_4": {"ko": "그러는 동안, 제가 당신 머리의 이 리본을 풀어서 당신 머리를 내 머리처럼 헝클어뜨리게 두십시오!'", "en": "While you do that, let me take this ribbon from your hair and shake your hair out to look like mine!'"},
"P036_1": {"ko": "경이로울 만큼 빠른 속도로, 그리고 완전히 초자연적으로 보이는 의지와 행동력으로, 그는 이 모든 변화를 강행했다.", "en": "With wonderful speed, and with a strength of both will and action that seemed quite supernatural, he forced all these changes upon him."},
"P036_2": {"ko": "죄수는 그의 손에 쥐어진 어린아이와 같았다.", "en": "The prisoner was like a little child in his hands."},
"P037_1": {"ko": "'카튼!", "en": "'Carton!"},
"P037_2": {"ko": "친애하는 카튼!", "en": "Dear Carton!"},
"P037_3": {"ko": "이건 미친 짓이오.", "en": "It is madness."},
"P037_4": {"ko": "성공할 수 없고, 절대로 일어날 수 없소. 시도한 적은 있었지만 늘 실패했다오.", "en": "It cannot be accomplished, it can never be done, it has been attempted, and has always failed."},
"P037_5": {"ko": "내 죽음의 비통함에 당신의 죽음까지 더하지 말아 달라고 간청하오.'", "en": "I beg you not to add your death to the bitterness of mine.'"}
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
