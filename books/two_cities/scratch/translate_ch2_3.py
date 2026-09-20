import json

data_file = 'c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_02.json'

with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

translations = {
    "P023_1": {"ko": "호위병이 목청껏 소리쳤다. '워-워! 거기 멈춰라!'", "en": "The guard yelled as loud as he could. 'Wo-ho! Halt there!'"},
    "P023_2": {"ko": "'정지!'", "en": "'Stand!'"},
    "P023_3": {"ko": "'발포하겠다!'", "en": "'I will fire!'"},
    "P024_1": {"ko": "말발굽 소리가 갑자기 멈췄고, 첨벙거리고 허우적대는 소리와 함께 안개 속에서 한 남자의 목소리가 들려왔다. '그게 도버행 우편 마차요?'", "en": "The pace was suddenly checked, and with much splashing and floundering, a man's voice called out from the mist, 'Is that the Dover mail?'"},
    "P025_1": {"ko": "호위병이 쏘아붙였다. '그게 뭔지 넌 신경 쓰지 마! 넌 정체가 뭐야?'", "en": "The guard retorted. 'Never mind what it is! What are you?'"},
    "P026_1": {"ko": "'그게 도버행 우편 마차냐고요?'", "en": "'Is that the Dover mail?'"},
    "P027_1": {"ko": "'왜 알려고 하는데?'", "en": "'Why do you want to know?'"},
    "P028_1": {"ko": "'맞다면, 승객 한 명을 찾고 있소.'", "en": "'I am looking for a passenger, if it is.'"},
    "P029_1": {"ko": "'무슨 승객?'", "en": "'Which passenger?'"},
    "P030_1": {"ko": "'자비스 롤리 씨요.'", "en": "'Mr. Jarvis Lorry.'"},
    "P030_2": {"ko": "", "en": ""},
    "P031_1": {"ko": "장부에 적혀 있던 승객은 즉시 그것이 자신의 이름이라고 밝혔다.", "en": "Our booked passenger immediately showed that it was his name."},
    "P031_2": {"ko": "호위병, 마부, 그리고 다른 두 명의 승객은 불신이 가득한 눈으로 그를 쳐다보았다.", "en": "The guard, the coachman, and the other two passengers eyed him with distrust."},
    "P032_1": {"ko": "호위병이 안개 속의 목소리를 향해 외쳤다. '거기 가만히 있어! 내가 실수로 총을 쏘면, 네 평생 돌이킬 수 없을 테니까.'", "en": "The guard called out to the voice in the mist. 'Keep where you are! Because if I make a mistake, it can never be set right in your lifetime.'"},
    "P032_2": {"ko": "'롤리라는 이름의 신사분은 솔직하게 대답하십시오.'", "en": "'Gentleman named Lorry, answer straight.'"},
    "P033_1": {"ko": "승객은 약간 떨리는 목소리로 물었다. '무슨 일입니까? 누가 나를 찾소?'", "en": "The passenger asked in a slightly trembling voice. 'What is the matter? Who wants me?'"},
    "P033_2": {"ko": "'제리인가?'", "en": "'Is it Jerry?'"},
    "P034_1": {"ko": "('제리라면, 난 저 목소리가 마음에 안 들어.' 호위병이 혼잣말로 투덜거렸다. '내 생각보다 목이 훨씬 쉬었잖아, 제리라는 자는.')", "en": "('I don't like Jerry's voice, if it is Jerry,' the guard growled to himself. 'He's hoarser than I like, this Jerry.')"},
    "P035_1": {"ko": "'네, 롤리 선생님.'", "en": "'Yes, Mr. Lorry.'"},
    "P035_2": {"ko": "", "en": ""},
    "P036_1": {"ko": "'무슨 일인가?'", "en": "'What is the matter?'"},
    "P037_1": {"ko": "'선생님을 쫓아 급히 편지를 보냈습니다.'", "en": "'A dispatch was sent after you from back there.'"},
    "P037_2": {"ko": "'T. and Co.(텔슨 은행)에서요.'", "en": "'From T. and Co.'"},
    "P038_1": {"ko": "'이 심부름꾼은 내가 아는 사람입니다, 호위병.'", "en": "'I know this messenger, guard,' said Mr. Lorry."},
    "P038_2": {"ko": "롤리 씨가 길로 내려서며 말했다. 뒤에 있던 두 승객은 서둘러 마차에 올라타 문을 닫고 창문을 올렸는데, 예의를 갖추기보다는 자신들이 먼저 살겠다고 그를 밀어내듯 굴었다. '가까이 와도 괜찮습니다. 아무 문제 없습니다.'", "en": "Mr. Lorry, getting down into the road—assisted from behind more swiftly than politely by the other two passengers, who immediately scrambled into the coach, shut the door, and pulled up the window. 'He may come close; there's nothing wrong.'"},
    "P038_3": {"ko": "", "en": ""},
    "P039_1": {"ko": "'문제가 없기를 바라지만, 난 그 말을 완전히 믿을 수는 없소.' 호위병이 퉁명스럽게 혼잣말을 했다. '어이! 너!'", "en": "'I hope there isn't, but I can't be entirely sure of that,' said the guard in a gruff soliloquy. 'Hallo, you!'"},
    "P040_1": {"ko": "'네!'", "en": "'Well!'"},
    "P040_2": {"ko": "'어이, 너 말이야!' 제리가 전보다 더 쉰 목소리로 대답했다.", "en": "'And hallo to you!' said Jerry, hoarser than before."},
    "P041_1": {"ko": "'천천히 걸어서 다가와! 내 말 알아들었어?'", "en": "'Come forward at a walking pace! Do you hear me?'"},
    "P041_2": {"ko": "'안장에 권총집이 달려있어도, 거기에 손을 가까이 대지 마.'", "en": "'And if you have holsters on that saddle of yours, don't let me see your hand go near them.'"},
    "P041_3": {"ko": "'나는 오해하면 앞뒤 안 가리고 방아쇠부터 당기는 놈이니까.'", "en": "'For I'm a devil at making quick mistakes, and when I do, it comes out as lead.'"},
    "P041_4": {"ko": "'자, 이제 네 얼굴 좀 보자.'", "en": "'So now, let's take a look at you.'"},
    "P042_1": {"ko": "말과 기수의 형체가 소용돌이치는 안개를 뚫고 천천히 나타나, 승객이 서 있는 마차 옆으로 다가왔다.", "en": "The figures of a horse and rider came slowly through the swirling mist, and reached the side of the coach where the passenger stood."},
    "P042_2": {"ko": "기수는 몸을 굽힌 채 호위병을 곁눈질하며 승객에게 작게 접힌 종이 한 장을 건넸다.", "en": "The rider leaned down and, casting his eyes up at the guard, handed the passenger a small folded paper."},
    "P042_3": {"ko": "기수가 탄 말은 숨을 헐떡이고 있었고, 말굽부터 기수의 모자까지 두 사람 모두 진흙투성이였다.", "en": "The rider's horse was out of breath, and both horse and rider were covered in mud from the horse's hooves to the man's hat."},
    "P043_1": {"ko": "'호위병!' 승객이 차분하고 사무적인 어조로 불렀다.", "en": "'Guard!' said the passenger, in a tone of calm, business-like confidence."},
    "P044_1": {"ko": "경계를 늦추지 않은 호위병은 오른손으로는 들어 올린 나팔총의 개머리판을 잡고, 왼손으로는 총열을 쥔 채 기수를 노려보며 퉁명스럽게 대답했다. '말씀하십시오.'", "en": "The watchful guard, with his right hand on the stock of his raised blunderbuss, his left on the barrel, and his eye fixed on the horseman, answered curtly, 'Sir.'"},
    "P045_1": {"ko": "'걱정할 것 없습니다.'", "en": "'There is nothing to fear.'"},
    "P045_2": {"ko": "'나는 텔슨 은행 소속이오.'", "en": "'I belong to Tellson's Bank.'"},
    "P045_3": {"ko": "'런던에 있는 텔슨 은행을 알 거요.'", "en": "'You must know Tellson's Bank in London.'"},
    "P045_4": {"ko": "'나는 업무차 파리로 가는 길입니다.'", "en": "'I am going to Paris on business.'"},
    "P045_5": {"ko": "'술값으로 크라운(화폐 단위) 하나 주겠소.'", "en": "'Here is a crown for a drink.'"},
    "P045_6": {"ko": "'이걸 읽어봐도 되겠소?'", "en": "'May I read this?'"},
    "P046_1": {"ko": "'빨리 읽으신다면요, 선생님.'", "en": "'If you can be quick about it, sir.'"},
    "P047_1": {"ko": "그는 자기 쪽 마차 등불 불빛에 종이를 펴고, 먼저 혼자서 읽은 다음 소리 내어 읽었다.", "en": "He opened it in the light of the coach-lamp on his side, and read it—first to himself, and then aloud:"},
    "P047_2": {"ko": "''도버에서 마드무아젤(아가씨)을 기다리시오.' 보시오, 호위병. 길지 않소.'", "en": "''Wait at Dover for Mam'selle.' It is not long, as you can see, guard.'"},
    "P047_3": {"ko": "'제리, 내 대답은 '삶으로 소환됨(RECALLED TO LIFE)'이라고 전하게.'", "en": "'Jerry, tell them my answer was: RECALLED TO LIFE.'"},
    "P048_1": {"ko": "제리는 안장 위에서 깜짝 놀랐다. '그거 참 기가 막히게 이상한 대답이군.' 그가 최대한 쉰 목소리로 말했다.", "en": "Jerry started in his saddle. 'That's a blazing strange answer, too,' he said in his hoarsest voice."},
    "P049_1": {"ko": "'그 메시지를 가져가면, 내가 답장을 쓴 것과 다름없이 편지를 잘 받았다는 걸 그들도 알 거네.'", "en": "'Take that message back, and they will know that I received this, just as well as if I had written a reply.'"},
    "P049_2": {"ko": "'조심히 돌아가게.'", "en": "'Make the best of your journey.'"},
    "P049_3": {"ko": "'잘 가시게.'", "en": "'Good night.'"},
    "P050_1": {"ko": "그 말을 남기고 승객은 마차 문을 열고 올라탔다.", "en": "With those words, the passenger opened the coach door and got inside;"},
    "P050_2": {"ko": "동승객들은 시계와 지갑을 재빨리 장화 속에 숨기고 자는 척하느라 그를 전혀 도와주지 않았다.", "en": "without any help from his fellow passengers, who had hurriedly hidden their watches and purses in their boots and were now pretending to be asleep."},
    "P050_3": {"ko": "그들은 어떠한 행동에도 나서지 않음으로써 위험을 피하려는 속셈뿐이었다.", "en": "They had no other purpose than to avoid the risk of starting any kind of action."},
    "P051_1": {"ko": "마차는 내리막길에 접어들며 더욱 짙어지는 안개에 휩싸인 채 다시 무겁게 덜컹거리며 나아갔다.", "en": "The coach lumbered on again, with heavier clouds of mist closing around it as it began the descent."},
    "P051_2": {"ko": "호위병은 곧 무기 상자에 나팔총을 집어넣고, 상자 안의 다른 무기들과 허리띠에 찬 보조 권총들을 확인한 뒤, 의자 밑에 있는 작은 상자를 살폈다. 그 안에는 대장장이 도구 몇 개와 횃불 두 개, 그리고 부싯깃 통이 들어 있었다.", "en": "The guard soon placed his blunderbuss back into the weapon chest. After checking the rest of its contents and the extra pistols in his belt, he looked into a smaller chest under his seat, which contained a few smith's tools, a couple of torches, and a tinderbox."},
    "P051_3": {"ko": "가끔 돌풍이 불어 마차 등불이 꺼지는 일이 생겨도 그는 만반의 준비를 갖추고 있었다. 그럴 땐 마차 안으로 들어가 짚단에 불꽃이 튀지 않도록 주의하며 부싯돌을 쳐서, 운이 좋으면 5분 안에 꽤 안전하고 쉽게 불을 피울 수 있었다.", "en": "He was fully prepared so that if the coach-lamps were blown out by a storm—which occasionally happened—he only had to shut himself inside, keep the sparks from the flint and steel away from the straw, and safely get a light in about five minutes, if he was lucky."},
    "P052_1": {"ko": "마차 지붕 너머로 부드러운 목소리가 들렸다. '톰!'", "en": "A voice called softly over the coach roof, 'Tom!'"},
    "P053_1": {"ko": "'어이, 조.'", "en": "'Hallo, Joe.'"},
    "P054_1": {"ko": "'그 메시지 들었어?'", "en": "'Did you hear the message?'"},
    "P055_1": {"ko": "'들었어, 조.'", "en": "'I did, Joe.'"},
    "P056_1": {"ko": "'도대체 무슨 뜻인 것 같아, 톰?'", "en": "'What do you make of it, Tom?'"},
    "P057_1": {"ko": "'전혀 모르겠어, 조.'", "en": "'Nothing at all, Joe.'"},
    "P058_1": {"ko": "'그것 참 우연이군,' 호위병이 중얼거렸다. '나도 전혀 모르겠거든.'", "en": "'That's a coincidence, too,' the guard mused, 'because I made the same of it myself.'"},
    "P059_1": {"ko": "한편, 안개와 어둠 속에 홀로 남겨진 제리는 지친 말을 쉬게 할 겸 말에서 내렸다. 그는 얼굴의 진흙을 닦아내고, 반 갤런(약 2리터)의 물은 족히 들어갈 만큼 흠뻑 젖은 모자챙의 물기를 털어냈다.", "en": "Meanwhile, Jerry, left alone in the mist and darkness, dismounted not only to rest his exhausted horse but also to wipe the mud from his face and shake the water out of his hat brim, which could have held about half a gallon."},
    "P059_2": {"ko": "그는 진흙투성이가 된 팔에 고삐를 걸치고 서서 우편 마차 바퀴 소리가 더 이상 들리지 않고 밤이 다시 고요해질 때까지 기다렸다가, 언덕을 걸어 내려가기 시작했다.", "en": "He stood with the reins draped over his heavily splashed arm until the wheels of the mail coach could no longer be heard and the night grew completely still again, then he turned to walk down the hill."},
    "P060_1": {"ko": "쉰 목소리의 사자는 자신의 암말을 힐끗 보며 말했다. '템플 바에서부터 그렇게 전력 질주를 했으니, 늙은 암말아, 평지에 도착하기 전까지는 네 앞다리를 못 믿겠구나.' ''삶으로 소환됨'이라니. 참으로 기가 막히게 이상한 메시지군.'", "en": "Glancing at his mare, this hoarse messenger said, 'After that gallop from Temple Bar, old lady, I won't trust your front legs until I get you on level ground.' ''Recalled to life.' That is a blazing strange message.'"},
    "P060_2": {"ko": "'제리, 그런 일이 잦아지면 곤란할 텐데!'", "en": "'That kind of thing wouldn't be good for you, Jerry!'"},
    "P060_3": {"ko": "'이봐, 제리!'", "en": "'I say, Jerry!'"},
    "P060_4": {"ko": "'죽은 자가 삶으로 다시 소환되는 게 유행이 된다면, 넌 정말 기가 막히게 곤란해질 거야, 제리!'", "en": "'You would be in a blazing bad way if recalling to life came into fashion, Jerry!'"}
}

# Handle splitting items manually if multiple parts are under same tag but we don't have separate tag
# e.g., P030_1 and P030_2. I'll just merge them if needed or they will just get empty strings.
# Wait, the data has P030_2 separately. I will merge the translations to avoid empty ones.

for item in data:
    tag = item.get("tag")
    if tag in translations:
        # if dictionary has non-empty translation, we update it.
        # Note: some were left empty in my dict above to not double-translate.
        if translations[tag]["ko"] != "":
            item["ko"] = translations[tag]["ko"]
            item["en"] = translations[tag]["en"]

with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Done translating chunk 3")
