import json

data_file = 'c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_02.json'

with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    "H001": {"ko": "[1부 2장: 우편 마차]", "en": "CHAPTER II. The Mail"},
    "P002_1": {"ko": "11월 하순의 어느 금요일 밤, 이 이야기의 첫 번째 인물 앞에 놓인 길은 도버로 향하는 길이었다.", "en": "On a Friday night in late November, the road that lay before the first person in this story was the road to Dover."},
    "P002_2": {"ko": "그에게 도버로 가는 길은, 슈터스 힐이라는 언덕을 힘들게 올라가는 도버행 우편 마차 너머로 뻗어 있었다.", "en": "To him, the road to Dover stretched out beyond the Dover mail coach, which was struggling up the hill called Shooter's Hill."},
    "P002_3": {"ko": "다른 승객들과 마찬가지로, 그도 우편 마차 옆 진흙탕을 걸어서 언덕을 올라갔다.", "en": "Like the rest of the passengers, he walked up the hill in the mud alongside the mail coach."},
    "P002_4": {"ko": "이런 상황에서 걷기 운동을 즐겨서가 아니었다. 언덕과 마구, 진흙, 그리고 마차까지 모든 것이 너무 무거웠기 때문이다. 말들은 벌써 세 번이나 멈춰 섰고, 한 번은 마차를 끌고 길을 가로질러 출발지인 블랙히스로 되돌아가려는 반항적인 태도를 보이기도 했다.", "en": "It was not because they enjoyed walking in these circumstances. It was because the hill, the harness, the mud, and the coach were all so heavy. The horses had already stopped three times, and once they even pulled the coach across the road with a rebellious intent to return to Blackheath, where they started."},
    "P002_5": {"ko": "하지만 고삐와 채찍, 마부와 호위병이 힘을 합쳐 말들을 통제했다. 짐승에게도 이성이 있다는 주장을 뒷받침할 만한 반항이었지만, 그들은 규율을 내세워 말들을 굴복시켰다.", "en": "However, the reins, the whip, the coachman, and the guard worked together to control the horses. It was a rebellion that supported the argument that animals have reason, but they enforced the rules to suppress it."},
    "P002_6": {"ko": "결국 말들은 항복하고 다시 마차를 끌기 시작했다.", "en": "Eventually, the horses surrendered and returned to pulling the coach."},
    "P003_1": {"ko": "말들은 고개를 푹 숙이고 꼬리를 파르르 떨며 진흙탕을 헤쳐 나갔다. 마치 큰 관절들이 산산조각 나는 것처럼 이리저리 비틀거리고 넘어질 뻔했다.", "en": "With their heads lowered and tails trembling, the horses waded through the thick mud. They stumbled and faltered, as if their large joints were falling apart."},
    "P003_2": {"ko": "마부가 조심스럽게 '워-워! 진정해라!'라고 외치며 말들을 멈춰 세우고 쉬게 할 때마다, 가장 앞쪽에 있는 말은 고개와 마구를 격렬하게 흔들었다. 마치 마차를 언덕 위로 끌어올릴 수 없다고 단호하게 부인하는 것처럼 보였다.", "en": "Whenever the driver carefully yelled, 'Wo-ho! Calm down!' and brought the horses to a stop to rest, the leading horse violently shook its head and harness. It seemed to firmly deny that the coach could be pulled up the hill."},
    "P003_3": {"ko": "앞말이 이렇게 요란한 소리를 낼 때마다, 그 승객은 불안한 사람처럼 깜짝깜짝 놀라며 마음이 편치 않았다.", "en": "Whenever the leading horse made this noisy rattle, the passenger startled like a nervous person, feeling uneasy in his mind."},
    "P004_1": {"ko": "움푹 파인 곳마다 김이 모락모락 나는 안개가 피어올랐다. 안개는 쉴 곳을 찾지 못한 악령처럼 쓸쓸하게 언덕을 기어오르고 있었다.", "en": "Steaming mist rose from all the hollows. The mist roamed up the hill in its loneliness like an evil spirit, seeking rest but finding none."},
    "P004_2": {"ko": "차갑고 끈적끈적한 안개는 불길한 바다의 물결처럼 공기 중을 천천히 퍼져나가며 겹겹이 밀려왔다.", "en": "A cold, sticky mist made its slow way through the air in ripples, spreading over one another like waves in an unwholesome sea."},
    "P004_3": {"ko": "안개는 너무 짙어서 마차 등불의 불빛을 차단했고, 등불 자체의 일렁임과 불과 몇 야드 앞의 길만 간신히 보일 뿐이었다.", "en": "The mist was dense enough to block everything from the light of the coach-lamps, leaving only the workings of the lamps themselves and a few yards of the road visible."},
    "P004_4": {"ko": "힘겹게 걷는 말들의 입김이 안개 속으로 섞여 들어가서, 마치 그 안개를 말들이 모두 뿜어낸 것 같았다.", "en": "The breath of the laboring horses steamed into the mist, as if they had created all of it."},
    "P005_1": {"ko": "그 한 명 외에도 두 명의 승객이 우편 마차 옆에서 언덕을 힘겹게 올라가고 있었다.", "en": "Besides that one passenger, two other passengers were trudging up the hill by the side of the mail coach."},
    "P005_2": {"ko": "세 사람 모두 광대뼈와 귀 위까지 목도리를 칭칭 감고 있었고, 긴 가죽 장화를 신고 있었다.", "en": "All three were wrapped in mufflers up to their cheekbones and over their ears, and they wore long leather boots."},
    "P005_3": {"ko": "세 사람 중 누구도 눈에 보이는 모습만으로는 다른 두 사람이 어떻게 생겼는지 말할 수 없었다.", "en": "None of the three could tell what the other two looked like based on what they saw."},
    "P005_4": {"ko": "그들은 두꺼운 외투로 온몸을 꽁꽁 싸매고 있어서, 육신의 눈뿐만 아니라 마음의 눈으로도 동행들의 속내를 파악할 수 없었다.", "en": "Each of them was hidden under so many layers of clothing that they were concealed from both the physical eyes and the mental eyes of their two companions."},
    "P005_5": {"ko": "그 시절에는 길에서 마주치는 사람이 강도이거나 강도와 한패일지도 몰랐기 때문에, 여행자들은 짧은 시간 안에 남을 믿고 속마음을 터놓는 것을 몹시 꺼렸다.", "en": "In those days, travelers were very hesitant to be trusting on short notice, because anyone on the road might be a robber or in league with robbers."},
    "P005_6": {"ko": "모든 역참과 술집마다 주인이든 말단 마구간지기든 강도 두목인 '대장'에게 돈을 받는 사람이 한 명쯤은 있을 법했기 때문에, 이는 충분히 가능성 있는 일이었다.", "en": "As for the latter, it was highly probable, since every posting-house and ale-house could produce someone in the pay of the robber 'Captain,' ranging from the landlord to the lowest stable hand."},
    "P005_7": {"ko": "그래서 1775년 11월의 그 금요일 밤, 슈터스 힐을 무겁게 올라가는 도버행 우편 마차의 호위병도 똑같은 생각을 하고 있었다. 그는 마차 뒤쪽 자기 자리에 서서 발을 동동 구르며, 앞에 있는 무기 상자를 예의주시하고 한 손을 얹어두었다. 그 상자 안에는 장전된 나팔총 한 자루와 예닐곱 자루의 장전된 기병용 권총이 짧은 칼들 위에 놓여 있었다.", "en": "So the guard of the Dover mail coach thought to himself on that Friday night in November 1775, as it lumbered up Shooter's Hill. He stood on his designated perch at the back of the coach, stamping his feet, keeping an eye and a hand on the weapon chest before him, where a loaded blunderbuss lay on top of six or eight loaded horse-pistols, resting on a layer of cutlasses."},
    "P006_1": {"ko": "도버행 우편 마차는 평소와 다름없이 불신으로 가득 찬 상태였다. 호위병은 승객들을 의심했고, 승객들은 서로와 호위병을 의심했으며, 모두가 다른 모든 사람을 의심했다. 마부는 오직 말들에 대해서만 확신을 가졌을 뿐, 다른 것은 아무것도 믿지 않았다.", "en": "The Dover mail coach was in its usual state of suspicion: the guard suspected the passengers, the passengers suspected each other and the guard, and everyone suspected everyone else. The coachman was sure of nothing except the horses;"},
    "P006_2": {"ko": "그리고 그 말들에 대해서도, 그는 양심의 가책 없이 성경 두 권을 걸고 그들이 이 여행에 부적합하다고 맹세할 수 있었다.", "en": "and as for those horses, he could have sworn with a clear conscience on the two Testaments that they were not fit for the journey."},
    "P007_1": {"ko": "마부가 말했다. '워-워! 자, 그럼!'", "en": "The coachman said, 'Wo-ho! So, then!'"},
    "P007_2": {"ko": "'한 번만 더 끌면 정상이야, 이 망할 것들아! 여기까지 끌고 오느라 고생 꽤나 했으니까! 조!'", "en": "'One more pull and you'll be at the top, damn you! I've had enough trouble getting you this far! Joe!'"},
    "P008_1": {"ko": "호위병이 대답했다. '어이!'", "en": "'Halloa!' the guard replied."},
    "P009_1": {"ko": "'지금 몇 시나 됐나, 조?'", "en": "'What time do you have, Joe?'"},
    "P010_1": {"ko": "'11시 10분쯤 됐어.'", "en": "'A good ten minutes past eleven.'"},
    "P011_1": {"ko": "'젠장!' 짜증 난 마부가 소리쳤다. '아직도 슈터스 힐 꼭대기에 못 왔다니!'", "en": "'My blood!' the vexed coachman exclaimed, 'and we aren't even at the top of Shooter's Hill yet!'"},
    "P011_2": {"ko": "'쯧!'", "en": "'Tst!'"},
    "P011_3": {"ko": "'이랴!'", "en": "'Yah!'"},
    "P011_4": {"ko": "'어서 가!'", "en": "'Get moving!'"}
}

for item in data:
    tag = item.get("tag")
    if tag in translations:
        item["ko"] = translations[tag]["ko"]
        item["en"] = translations[tag]["en"]

with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done translating chunk 1")
