import json

translations = {
    99: {"ko": "여러 번 반복했습니다.", "en": "Over and over again."},
    100: {"ko": "순수한 애국심(sheer patriotism) 외에는 어떤 동기도 없었습니까?", "en": "No motives but motives of sheer patriotism?"},
    101: {"ko": "전혀 없었습니다.", "en": "None whatever."},
    102: {"ko": "이 고결한(virtuous) 하인 Roger Cly는 엄청난 기세로(at a great rate) 사건에 대한 증언을 거침없이 이어나갔다.", "en": "The virtuous servant, Roger Cly, swore his way through the case at a great rate."},
    103: {"ko": "그는 4년 전 선의와 순수한 마음으로 죄수를 모시게 되었다고 했다.", "en": "He had taken service with the prisoner, in good faith and simplicity, four years ago."},
    104: {"ko": "그는 칼레행 여객선(Calais packet)에서 죄수에게 쓸만한 일꾼(handy fellow)이 필요하지 않냐고 물었고, 죄수가 그를 고용했다고 했다.", "en": "He had asked the prisoner, aboard the Calais packet, if he wanted a handy fellow, and the prisoner had engaged him."},
    105: {"ko": "그는 자선(charity)의 차원에서 자기를 고용해달라고 죄수에게 부탁한 적이 없으며, 그런 생각은 해본 적도 없다고 했다.", "en": "He had not asked the prisoner to take the handy fellow as an act of charity--never thought of such a thing."},
    106: {"ko": "그는 그 직후부터 죄수를 의심하기 시작해 그를 예의주시했다(keep an eye upon)고 했다.", "en": "He began to have suspicions of the prisoner, and to keep an eye upon him, soon afterwards."},
    107: {"ko": "여행 중 죄수의 옷을 정리하다가 그의 주머니에서 이것들과 비슷한 명단들을 여러 번 발견했다고 했다.", "en": "In arranging his clothes, while travelling, he had seen similar lists to these in the prisoner’s pockets, over and over again."},
    108: {"ko": "그는 그 명단들을 죄수의 책상 서랍에서 꺼냈다고 했다.", "en": "He had taken these lists from the drawer of the prisoner’s desk."},
    109: {"ko": "그는 자신이 먼저 그곳에 명단들을 넣어둔 것이 아니라고 했다.", "en": "He had not put them there first."},
    110: {"ko": "그는 죄수가 칼레(Calais)에서 프랑스 신사들에게 바로 이 명단들을 보여주는 것을 보았으며, 칼레와 불로뉴(Boulogne) 두 곳 모두에서 프랑스 신사들에게 비슷한 명단들을 보여주는 것을 보았다고 했다.", "en": "He had seen the prisoner show these identical lists to French gentlemen at Calais, and similar lists to French gentlemen, both at Calais and Boulogne."},
    111: {"ko": "그는 자신의 조국을 사랑했고, 이를 참을 수 없어 정보를 제공(given information)했다고 했다.", "en": "He loved his country, and couldn’t bear it, and had given information."},
    112: {"ko": "그는 은 주전자를 훔쳤다는 의심을 받은 적이 한 번도 없었다고 했다.", "en": "He had never been suspected of stealing a silver tea-pot;"},
    113: {"ko": "겨자통(mustard-pot)에 관해 모함을 받은 적은 있지만, 그것은 도금된 것으로 밝혀졌다고 했다.", "en": "he had been maligned respecting a mustard-pot, but it turned out to be only a plated one."},
    114: {"ko": "그는 이전 증인을 7~8년 전부터 알고 지냈다고 했다.", "en": "He had known the last witness seven or eight years;"},
    115: {"ko": "그것은 단순한 우연의 일치(coincidence)였다고 했다.", "en": "that was merely a coincidence."},
    116: {"ko": "그는 그것을 특별히 기이한 우연의 일치라고 부르지 않겠다고 했다.", "en": "He didn’t call it a particularly curious coincidence;"},
    117: {"ko": "대부분의 우연은 기이한 법이니까.", "en": "most coincidences were curious."},
    118: {"ko": "진정한 애국심이 자신의 유일한 동기였다는 사실 역시 기이한 우연의 일치라고 부르지 않겠다고 했다.", "en": "Neither did he call it a curious coincidence that true patriotism was _his_ only motive too."},
    119: {"ko": "그는 진정한 영국인(true Briton)이며, 자신과 같은 이들이 많기를 바란다고 했다.", "en": "He was a true Briton, and hoped there were many like him."},
    120: {"ko": "큰 파리들(blue-flies)이 다시 윙윙거렸고, 검찰총장(Attorney-General)은 다음 사람을 호명했다.", "en": "The blue-flies buzzed again, and Mr. Attorney-General called Mr."},
    121: {"ko": "Jarvis Lorry.", "en": "Jarvis Lorry."},
    122: {"ko": "“Jarvis Lorry 씨, 당신은 Tellson 은행의 직원입니까?”", "en": "“Mr. Jarvis Lorry, are you a clerk in Tellson’s bank?”"},
    123: {"ko": "“그렇습니다.”", "en": "“I am.”"},
    124: {"ko": "“1775년 11월의 어느 금요일 밤, 업무차 우편마차(mail)를 타고 런던과 도버 사이를 여행한 적이 있습니까?”", "en": "“On a certain Friday night in November one thousand seven hundred and seventy-five, did business occasion you to travel between London and Dover by the mail?”"},
    125: {"ko": "“그렇습니다.”", "en": "“It did.”"},
    126: {"ko": "“그 우편마차에 다른 승객들도 있었습니까?”", "en": "“Were there any other passengers in the mail?”"},
    127: {"ko": "“두 명 있었습니다.”", "en": "“Two.”"},
    128: {"ko": "“그들은 밤중에 길에서 내렸습니까?”", "en": "“Did they alight on the road in the course of the night?”"},
    129: {"ko": "“그랬습니다.”", "en": "“They did.”"},
    130: {"ko": "“Lorry 씨, 죄수를 보십시오.", "en": "“Mr. Lorry, look upon the prisoner."},
    131: {"ko": "그가 그 두 승객 중 한 명이었습니까?”", "en": "Was he one of those two passengers?”"},
    132: {"ko": "“그가 그 사람이었다고 단언할(undertake to say) 수는 없습니다.”", "en": "“I cannot undertake to say that he was.”"},
    133: {"ko": "“그가 그 두 승객 중 어느 한 명과 닮았습니까?”", "en": "“Does he resemble either of these two passengers?”"},
    134: {"ko": "“두 사람 모두 외투로 단단히 싸매고 있었고 밤이 너무 어두웠으며 우리 모두 극도로 말을 아꼈기(reserved) 때문에, 그렇다고조차 단언할 수 없습니다.”", "en": "“Both were so wrapped up, and the night was so dark, and we were all so reserved, that I cannot undertake to say even that.”"},
    135: {"ko": "“Lorry 씨, 다시 죄수를 보십시오.", "en": "“Mr. Lorry, look again upon the prisoner."},
    136: {"ko": "그가 그 두 승객처럼 외투로 단단히 싸매고 있었다고 가정할 때, 그의 체격(bulk)이나 키로 보아 그가 그들 중 한 명이 아니었을 거라고 생각될 만한 점이 있습니까?”", "en": "Supposing him wrapped up as those two passengers were, is there anything in his bulk and stature to render it unlikely that he was one of them?”"},
    137: {"ko": "“없습니다.”", "en": "“No.”"},
    138: {"ko": "“Lorry 씨, 당신은 그가 그들 중 한 명이 아니었다고 맹세할 수 없겠군요?”", "en": "“You will not swear, Mr. Lorry, that he was not one of them?”"},
    139: {"ko": "“그렇습니다.”", "en": "“No.”"},
    140: {"ko": "“그렇다면 적어도 당신은 그가 그들 중 한 명이었을 수도 있다고 말하는 겁니까?”", "en": "“So at least you say he may have been one of them?”"},
    141: {"ko": "“예.", "en": "“Yes."},
    142: {"ko": "다만 두 사람 모두 저처럼 노상강도(highwaymen)를 겁냈던 것으로 기억하는데, 죄수에게서는 겁먹은(timorous) 기색이 보이지 않는다는 점은 다릅니다.”", "en": "Except that I remember them both to have been--like myself--timorous of highwaymen, and the prisoner has not a timorous air.”"},
    143: {"ko": "“Lorry 씨, 겁먹은 척 꾸며내는(counterfeit of timidity) 것을 본 적이 있습니까?”", "en": "“Did you ever see a counterfeit of timidity, Mr. Lorry?”"},
    144: {"ko": "“물론 본 적 있습니다.”", "en": "“I certainly have seen that.”"},
    145: {"ko": "“Lorry 씨, 죄수를 한 번 더 보십시오.", "en": "“Mr. Lorry, look once more upon the prisoner."},
    146: {"ko": "확실히 기억하건대(to your certain knowledge), 전에 그를 본 적이 있습니까?”", "en": "Have you seen him, to your certain knowledge, before?”"},
    147: {"ko": "“있습니다.”", "en": "“I have.”"},
    148: {"ko": "“언제입니까?”", "en": "“When?”"},
    149: {"ko": "“며칠 후 프랑스에서 돌아올 때였습니다. 칼레에서 죄수가 제가 타고 돌아올 여객선에 승선했고 저와 함께 항해했습니다.”", "en": "“I was returning from France a few days afterwards, and, at Calais, the prisoner came on board the packet-ship in which I returned, and made the voyage with me.”"},
    150: {"ko": "“그가 몇 시에 승선했습니까?”", "en": "“At what hour did he come on board?”"},
    151: {"ko": "“자정이 조금 지난 시간이었습니다.”", "en": "“At a little after midnight.”"},
    152: {"ko": "“한밤중(dead of the night)이었군요.", "en": "“In the dead of the night."},
    153: {"ko": "그토록 늦은 시간에 승선한 승객은 그 사람뿐이었습니까?”", "en": "Was he the only passenger who came on board at that untimely hour?”"},
    154: {"ko": "“어쩌다 보니(happened to be) 그 사람뿐이었습니다.”", "en": "“He happened to be the only one.”"},
    155: {"ko": "“'어쩌다 보니'라는 말은 신경 쓰지 마십시오, Lorry 씨.", "en": "“Never mind about ‘happening,’ Mr. Lorry."},
    156: {"ko": "한밤중에 승선한 승객은 그가 유일했습니까?”", "en": "He was the only passenger who came on board in the dead of the night?”"},
    157: {"ko": "“그가 유일했습니다.”", "en": "“He was.”"},
    158: {"ko": "“Lorry 씨, 당신은 혼자 여행 중이었습니까, 아니면 일행이 있었습니까?”", "en": "“Were you travelling alone, Mr. Lorry, or with any companion?”"},
    159: {"ko": "“일행이 두 명 있었습니다.", "en": "“With two companions."},
    160: {"ko": "어느 신사와 숙녀였습니다.", "en": "A gentleman and lady."},
    161: {"ko": "그분들도 이곳에 와 계십니다.”", "en": "They are here.”"},
    162: {"ko": "“이곳에 있군요.", "en": "“They are here."},
    163: {"ko": "당신은 죄수와 어떤 대화라도 나누었습니까?”", "en": "Had you any conversation with the prisoner?”"},
    164: {"ko": "“거의 없었습니다.", "en": "“Hardly any."},
    165: {"ko": "날씨에 폭풍우가 몰아치고 항해가 길고 험난해서(rough), 저는 해협을 건너는 내내 거의 소파에 누워 있었습니다.”", "en": "The weather was stormy, and the passage long and rough, and I lay on a sofa, almost from shore to shore.”"},
    166: {"ko": "“Lucie Manette 양!”", "en": "“Miss Manette!”"},
    167: {"ko": "이전에도 모든 사람들의 시선을 한 몸에 받았고 이제 다시 모든 시선이 향하고 있는 그 젊은 숙녀는 앉아 있던 자리에서 일어섰다.", "en": "The young lady, to whom all eyes had been turned before, and were now turned again, stood up where she had sat."},
    168: {"ko": "그녀의 아버지도 함께 일어나 그녀의 손을 자신의 팔에 낀 채로(drawn through his arm) 서 있었다.", "en": "Her father rose with her, and kept her hand drawn through his arm."},
    169: {"ko": "“Manette 양, 죄수를 보십시오.”", "en": "“Miss Manette, look upon the prisoner.”"},
    170: {"ko": "저토록 깊은 연민, 저토록 진실된 젊음과 아름다움을 마주하는 것은 그 군중 모두를 마주하는 것보다 피고인에게 훨씬 더 고통스러운(trying) 일이었다.", "en": "To be confronted with such pity, and such earnest youth and beauty, was far more trying to the accused than to be confronted with all the crowd."},
    171: {"ko": "무덤 가장자리에 그녀와 떨어져 선 듯한(apart with her on the edge of his grave) 상황에서, 쳐다보는 사람들의 모든 호기심 어린 시선들조차도 그 순간 그가 가만히 서 있을 수 있도록(nerve him to remain quite still) 만들지는 못했다.", "en": "Standing, as it were, apart with her on the edge of his grave, not all the staring curiosity that looked on, could, for the moment, nerve him to remain quite still."},
    172: {"ko": "그의 다급한 오른손은 정원에 있는 상상의 꽃밭인 양 앞에 놓인 허브들을 만지작거렸고(parcelled out),", "en": "His hurried right hand parcelled out the herbs before him into imaginary beds of flowers in a garden;"},
    173: {"ko": "호흡을 조절하고 진정시키려는(steady) 그의 노력에 입술이 떨렸고 그 입술에 있던 핏기가 심장으로 몰려들었다.", "en": "and his efforts to control and steady his breathing shook the lips from which the colour rushed to his heart."},
    174: {"ko": "커다란 파리들의 윙윙거리는 소리가 다시 커졌다.", "en": "The buzz of the great flies was loud again."},
    175: {"ko": "“Manette 양, 저 죄수를 전에 본 적이 있습니까?”", "en": "“Miss Manette, have you seen the prisoner before?”"},
    176: {"ko": "“예, 선생님(sir).”", "en": "“Yes, sir.”"},
    177: {"ko": "“어디서입니까?”", "en": "“Where?”"},
    178: {"ko": "“방금 언급하신 여객선에 탑승했을 때였습니다, 선생님. 그리고 방금 말씀하신 것과 동일한 때(same occasion)였습니다.”", "en": "“On board of the packet-ship just now referred to, sir, and on the same occasion.”"},
    179: {"ko": "“당신이 방금 언급된 그 젊은 숙녀입니까?”", "en": "“You are the young lady just now referred to?”"},
    180: {"ko": "“아! 너무나도 불행히 그렇습니다!”", "en": "“O! most unhappily, I am!”"},
    181: {"ko": "그녀의 애처로운(plaintive) 연민의 어조는 판사가 거칠게 말할 때의 다소 음악적이지 못한(less musical) 목소리에 묻혀버렸다.", "en": "The plaintive tone of her compassion merged into the less musical voice of the Judge, as he said something fiercely:"},
    182: {"ko": "“질문에 대답만 하고, 그에 대해 어떤 논평(remark)도 덧붙이지 마시오.”", "en": "“Answer the questions put to you, and make no remark upon them.”"},
    183: {"ko": "“Manette 양, 해협을 건너는 항해 중에 죄수와 어떤 대화라도 나누었습니까?”", "en": "“Miss Manette, had you any conversation with the prisoner on that passage across the Channel?”"},
    184: {"ko": "“예, 선생님.”", "en": "“Yes, sir.”"},
    185: {"ko": "“그 대화를 떠올려 보십시오.”", "en": "“Recall it.”"}
}

def update():
    import os
    work_queue_path = "c:/git_repo/TKprof_book/work_queue.json"
    book_file_path = "c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_03.json"
    
    # 1. Update work_queue.json
    with open(work_queue_path, "r", encoding="utf-8") as f:
        queue = json.load(f)
        
    for item in queue:
        if item["id"] in translations:
            item["ko"] = translations[item["id"]]["ko"]
            item["en"] = translations[item["id"]]["en"]
            item["status"] = "done"
            
    with open(work_queue_path, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)
        
    # 2. Update book2_ch_03.json
    if os.path.exists(book_file_path):
        with open(book_file_path, "r", encoding="utf-8") as f:
            book = json.load(f)
            
        for block in book:
            if block["id"] in translations:
                block["ko"] = translations[block["id"]]["ko"]
                block["en"] = translations[block["id"]]["en"]
                
        with open(book_file_path, "w", encoding="utf-8") as f:
            json.dump(book, f, ensure_ascii=False, indent=2)
    else:
        print(f"File not found: {book_file_path}")

if __name__ == "__main__":
    update()
    print("Done")
