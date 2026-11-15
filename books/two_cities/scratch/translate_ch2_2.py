import json

data_file = 'c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_02.json'

with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    "P012_1": {"ko": "채찍질로 강력한 거절을 당한 앞말은 결연히 앞으로 나아가려 발버둥 쳤고, 나머지 세 마리 말도 그 뒤를 따랐다.", "en": "The leading horse, firmly rejected by a crack of the whip, made a determined scramble forward, and the other three horses followed suit."},
    "P012_2": {"ko": "도버행 우편 마차는 다시 한번 힘겹게 앞으로 나아갔고, 그 옆에서는 장화를 신은 승객들이 진흙탕을 질퍽거리며 걸었다.", "en": "Once again, the Dover mail coach struggled onward, with the long boots of its passengers squelching in the mud alongside it."},
    "P012_3": {"ko": "그들은 마차가 멈출 때 함께 멈췄고, 마차 곁을 바짝 따라가며 일행에서 떨어지지 않았다.", "en": "They had stopped when the coach stopped, and they stayed close beside it."},
    "P012_4": {"ko": "만약 세 사람 중 누군가가 조금 앞서서 안개와 어둠 속으로 걸어가자고 제안할 만큼 대담했다면, 그는 그 즉시 노상강도로 오인받아 총에 맞기 십상이었을 것이다.", "en": "If any of the three had been bold enough to suggest walking a little ahead into the mist and darkness, he would have been highly likely to be shot instantly as a highwayman."},
    "P013_1": {"ko": "마지막 혼신을 다한 끝에 마차는 마침내 언덕 꼭대기에 도착했다.", "en": "With a final burst of effort, the coach reached the summit of the hill."},
    "P013_2": {"ko": "말들은 다시 숨을 고르기 위해 멈춰 섰고, 호위병은 마차에서 내려 내리막길을 위해 바퀴에 제동 장치를 걸고 승객들이 탈 수 있도록 문을 열었다.", "en": "The horses stopped to catch their breath again, and the guard stepped down to lock the wheel for the descent and open the coach door to let the passengers in."},
    "P014_1": {"ko": "'쯧!'", "en": "'Tst!'"},
    "P014_2": {"ko": "'조!' 마부가 자기 자리에서 아래를 내려다보며 경고하는 목소리로 소리쳤다.", "en": "'Joe!' cried the coachman in a warning voice, looking down from his seat."},
    "P015_1": {"ko": "'무슨 일인가, 톰?'", "en": "'What is it, Tom?'"},
    "P016_1": {"ko": "두 사람은 귀를 기울였다.", "en": "Both of them listened."},
    "P017_1": {"ko": "'가벼운 구보로 달려오는 말소리가 들리네, 조.'", "en": "'I hear a horse coming up at a canter, Joe.'"},
    "P018_1": {"ko": "'아니, 전속력으로 질주하는 말소리야, 톰.' 호위병이 마차 문에서 손을 떼고 재빨리 자기 자리로 올라가며 대답했다. '신사 여러분!'", "en": "'No, I hear a horse at a full gallop, Tom,' the guard replied as he let go of the door and quickly climbed up to his seat. 'Gentlemen!'"},
    "P018_2": {"ko": "'국왕 폐하의 이름으로 명합니다, 모두들 물러서시오!'", "en": "'In the King's name, all of you stand back!'"},
    "P019_1": {"ko": "이 다급한 경고와 함께, 그는 나팔총의 공이치기를 당기고 공격 태세를 갖추었다.", "en": "With this urgent warning, he cocked his blunderbuss and stood ready to defend."},
    "P020_1": {"ko": "이 이야기의 주요 승객은 막 마차 계단에 올라타려던 참이었다.", "en": "The passenger who is the focus of this story was on the coach step, about to get in."},
    "P020_2": {"ko": "다른 두 승객은 그의 바로 뒤에서 뒤따라 타려던 중이었다.", "en": "The other two passengers were right behind him, ready to follow."},
    "P020_3": {"ko": "그는 반쯤 마차에 타고 반쯤 밖으로 나온 채 계단에 그대로 머물렀다.", "en": "He remained on the step, half inside the coach and half outside."},
    "P020_4": {"ko": "나머지 두 사람은 그의 아래쪽 길 위에 멈춰 섰다.", "en": "The other two remained on the road below him."},
    "P020_5": {"ko": "그들 모두는 마부와 호위병을 번갈아 쳐다보며 소리에 귀를 기울였다.", "en": "They all looked back and forth between the coachman and the guard, and listened."},
    "P020_6": {"ko": "마부도 뒤를 돌아보았고, 호위병도 뒤를 돌아보았다. 심지어 그 완강하던 앞말조차 귀를 쫑긋 세우고 반항 없이 뒤를 돌아보았다.", "en": "The coachman looked back, and the guard looked back. Even the stubborn leading horse pricked up its ears and looked back without resistance."},
    "P021_1": {"ko": "덜컹거리며 힘겹게 나아가던 마차가 멈춰 서면서 생긴 고요함은 밤의 적막과 더해져 사위를 진정 쥐 죽은 듯 고요하게 만들었다.", "en": "The silence that followed when the noisy, struggling coach stopped, combined with the stillness of the night, made it truly quiet."},
    "P021_2": {"ko": "말들의 거친 숨소리가 마차에 떨림을 전해, 마치 마차 자체가 불안에 떠는 것처럼 보였다.", "en": "The heavy panting of the horses sent a trembling motion through the coach, as if the coach itself was anxious."},
    "P021_3": {"ko": "승객들의 심장 뛰는 소리가 아마 남에게 들릴 정도로 크게 울렸을 것이다.", "en": "The passengers' hearts beat so loudly that they might have been heard."},
    "P021_4": {"ko": "어쨌든 이 조용한 멈춤 속에서 사람들은 숨이 차 헐떡이고, 긴장하여 숨을 죽이며, 다가올 일에 대한 기대로 맥박이 빨라지는 것을 생생하게 느낄 수 있었다.", "en": "At any rate, in this quiet pause, one could clearly sense people out of breath, holding their breath, and having their pulses quicken with anticipation."},
    "P022_1": {"ko": "말이 전속력으로 질주하는 소리가 빠르고 맹렬하게 언덕 위로 올라왔다.", "en": "The sound of a galloping horse came rushing fast and furiously up the hill."}
}

for item in data:
    tag = item.get("tag")
    if tag in translations:
        item["ko"] = translations[tag]["ko"]
        item["en"] = translations[tag]["en"]

with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done translating chunk 2")
