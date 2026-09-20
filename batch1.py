import json
import os

translations = {
    101: {"ko": "\"세상에, 나는 할 일이 없소.\" 카턴 씨가 말했다.", "en": "\"Bless you, I have no business,\" said Mr. Carton."},
    102: {"ko": "\"만약 할 일이 있다면,\" 로리 씨가 계속해서 말했다. \"아마도 당신은 그것에 신경을 쓸 텐데요.\"", "en": "\"If you had,\" pursued Mr. Lorry, \"perhaps you would attend to it.\""},
    103: {"ko": "\"세상에, 아니오!--나는 그렇지 않을 거요,\" 카턴 씨가 말했다.", "en": "\"Lord love you, no!--I shouldn't,\" said Mr. Carton."},
    104: {"ko": "\"글쎄요, 선생님!\" 로리 씨가 그의 무관심에 완전히 화가 나서 외쳤다. \"사업은 아주 좋은 것이고, 아주 존경받을 만한 것입니다.", "en": "\"Well, sir!\" cried Mr. Lorry, thoroughly heated by his indifference, \"business is a very good thing, and a very respectable thing."},
    105: {"ko": "그리고 선생님, 만약 사업이 그 나름의 제약과 침묵, 장애물을 부과하더라도, 관대한 젊은 신사인 다네이 씨는 그러한 상황을 감안할 줄 압니다.", "en": "And, sir, if business imposes its restraints and its silences and impediments, Mr. Darnay as a young gentleman of generosity knows how to make allowance for that circumstance."},
    106: {"ko": "다네이 씨, 안녕히 주무십시오, 신의 축복이 있기를!", "en": "Mr. Darnay, good night, God bless you, sir!"},
    107: {"ko": "아마도 변호사에게 화가 난 만큼 자신에게도 약간 화가 났는지, 로리 씨는 서둘러 의자에 올라타서 텔슨 은행으로 실려 갔다.", "en": "Perhaps a little angry with himself, as well as with the barrister, Mr. Lorry bustled into the chair, and was carried off to Tellson's."},
    108: {"ko": "아베이(Abbaye) 감옥에서 온 고통받는 가벨의 편지를 제시하지 않았다면 그가 여기까지 오지도 못했을 것이다.", "en": "Nothing but the production of the afflicted Gabelle's letter from his prison of the Abbaye would have got him on so far."},
    109: {"ko": "이 작은 마을의 위병소에서의 어려움이 너무 컸기 때문에, 그는 자신의 여행이 위기에 처했다고 느꼈다.", "en": "His difficulty at the guard-house in this small place had been such, that he felt his journey to have come to a crisis."},
    110: {"ko": "그러므로 그는 아침까지 머물도록 배정받은 작은 여관에서 한밤중에 깨어났을 때, 사람이 느낄 수 있는 한 가장 적게 놀랐다.", "en": "And he was, therefore, as little surprised as a man could be, to find himself awakened at the small inn to which he had been remitted until morning, in the middle of the night."},
    111: {"ko": "\"망명자여,\" 관리가 말했다. \"호위병을 붙여서 당신을 파리로 보낼 것이오.\"", "en": "\"Emigrant,\" said the functionary, \"I am going to send you on to Paris, under an escort.\""},
    112: {"ko": "\"시민이여, 나는 파리로 가는 것 외에는 바라는 것이 없소. 비록 호위병 없이도 갈 수 있지만 말이오.\"", "en": "\"Citizen, I desire nothing more than to get to Paris, though I could dispense with the escort.\""},
    113: {"ko": "\"조용히 해!\" 머스킷 총의 개머리판으로 침대 덮개를 내리치며 빨간 모자를 쓴 남자가 으르렁거렸다. \"조용히 해, 귀족!\"", "en": "\"Silence!\" growled a red-cap, striking at the coverlet with the butt-end of his musket. \"Peace, aristocrat!\""},
    114: {"ko": "\"훌륭한 애국자가 말하는 대로요,\" 소심한 관리가 관찰하듯 말했다. \"당신은 귀족이고, 호위병이 있어야 하며--그 비용을 지불해야 하오.\"", "en": "\"It is as the good patriot says,\" observed the timid functionary. \"You are an aristocrat, and must have an escort--and must pay for it.\""},
    115: {"ko": "\"나에겐 선택권이 없군,\" 찰스 다네이가 말했다.", "en": "\"I have no choice,\" said Charles Darnay."},
    116: {"ko": "\"선택권이라니!", "en": "\"Choice!"},
    117: {"ko": "그의 말을 들어보라지!\" 가로등 철조망(교수형)에서 보호받는 것이 특혜가 아니라는 듯이! 같은 붉은 모자가 얼굴을 찌푸리며 소리쳤다.", "en": "Listen to him!\" cried the same scowling red-cap. \"As if it was not a favour to be protected from the lamp-iron!\""},
    118: {"ko": "\"항상 훌륭한 애국자가 말하는 대로요,\" 관리가 말했다. \"일어나서 옷을 입으시오, 망명자.\"", "en": "\"It is always as the good patriot says,\" observed the functionary. \"Rise and dress yourself, emigrant.\""},
    119: {"ko": "다네이는 순순히 따랐고, 거친 빨간 모자를 쓴 다른 애국자들이 모닥불 옆에서 담배를 피우고, 술을 마시고, 잠을 자고 있는 위병소로 다시 끌려갔다.", "en": "Darnay complied, and was taken back to the guard-house, where other patriots in rough red caps were smoking, drinking, and sleeping, by a watch-fire."},
    120: {"ko": "여기서 그는 호위병에 대한 비싼 대가를 치렀고, 새벽 세 시에 비에 젖고 젖은 길을 그들과 함께 출발했다.", "en": "Here he paid a heavy price for his escort, and hence he started with it on the wet, wet roads at three o'clock in the morning."},
    121: {"ko": "호위병은 붉은 모자와 삼색 기장을 달고 국가의 머스킷과 사브르로 무장한 말을 탄 두 명의 애국자였으며, 그의 양쪽에서 한 명씩 말을 탔다.", "en": "The escort were two mounted patriots in red caps and tri-coloured cockades, armed with national muskets and sabres, who rode one on either side of him."},
    122: {"ko": "호위를 받는 그는 자신의 말을 몰았지만, 느슨한 밧줄이 그의 고삐에 매달려 있었고 그 끝을 애국자 중 한 명이 자신의 손목에 감고 있었다.", "en": "The escorted governed his own horse, but a loose line was attached to his bridle, the end of which one of the patriots kept girded round his wrist."},
    123: {"ko": "이런 상태로 그들은 날카로운 비가 얼굴에 들이치는 가운데 길을 나섰다:", "en": "In this state they set forth with the sharp rain driving in their faces:"},
    124: {"ko": "무거운 기병의 빠른 걸음으로 울퉁불퉁한 마을 포장도로를 덜그럭거리며 달려 진흙투성이 길로 나섰다.", "en": "clattering at a heavy dragoon trot over the uneven town pavement, and out upon the mire-deep roads."},
    125: {"ko": "이런 상태로 그들은 말과 속도를 바꾸는 것 외에는 아무런 변화 없이 그들과 수도 사이에 놓인 진흙 깊은 수 마일을 가로질렀다.", "en": "In this state they traversed without change, except of horses and pace, all the mire-deep leagues that lay between them and the capital."},
    126: {"ko": "그들은 밤에 여행하며 동틀 녘 이후 한두 시간 멈추었고, 황혼이 질 때까지 쉬었다.", "en": "They travelled in the night, halting an hour or two after daybreak, and lying by until the twilight fell."},
    127: {"ko": "호위병들은 너무나 형편없는 옷차림을 하고 있어서, 젖지 않기 위해 맨다리에 짚을 꼬아 감고 너덜너덜한 어깨를 덮었다.", "en": "The escort were so wretchedly clothed, that they twisted straw round their bare legs, and thatched their ragged shoulders to keep the wet off."},
    128: {"ko": "이런 호위를 받는 개인적인 불편함과는 별개로, 애국자 중 한 명이 만성적으로 취해 있고 그의 머스킷을 매우 무모하게 다루는 데서 발생하는 현재의 위험에 대한 고려와는 별개로, 찰스 다네이는 자신에게 가해진 구속이 그의 가슴에 어떤 심각한 두려움도 일깨우도록 내버려 두지 않았다;", "en": "Apart from the personal discomfort of being so attended, and apart from such considerations of present danger as arose from one of the patriots being chronically drunk, and carrying his musket very recklessly, Charles Darnay did not allow the restraint that was laid upon him to awaken any serious fears in his breast;"},
    129: {"ko": "왜냐하면, 그는 그것이 아직 진술되지 않은 개별 사건의 장단점이나 아베이에 있는 죄수에 의해 확인될 수 있는, 아직 이루어지지 않은 변론과는 아무런 관련이 없을 것이라고 스스로 이치에 맞게 생각했기 때문이다.", "en": "for, he reasoned with himself that it could have no reference to the merits of an individual case that was not yet stated, and of representations, confirmable by the prisoner in the Abbaye, that were not yet made."},
    130: {"ko": "그러나 그들이 보베(Beauvais) 시에 도착했을 때--저녁 무렵 거리가 사람들로 가득 찼을 때 그들이 그랬듯이--그는 상황의 국면이 매우 우려스럽다는 것을 스스로에게 숨길 수 없었다.", "en": "But when they came to the town of Beauvais--which they did at eventide, when the streets were filled with people--he could not conceal from himself that the aspect of affairs was very alarming."},
    131: {"ko": "그가 역마차 마당에서 말에서 내리는 것을 보기 위해 불길한 군중이 모여들었고, 많은 목소리들이 큰 소리로 외쳤다. \"망명자를 타도하라!\"", "en": "An ominous crowd gathered to see him dismount of the posting-yard, and many voices called out loudly, \"Down with the emigrant!\""},
    132: {"ko": "그는 안장에서 몸을 빼려던 동작을 멈추고, 가장 안전한 장소인 그곳으로 다시 돌아가며 말했다:", "en": "He stopped in the act of swinging himself out of his saddle, and, resuming it as his safest place, said:"},
    133: {"ko": "\"망명자라니, 내 친구들!", "en": "\"Emigrant, my friends!"},
    134: {"ko": "내가 여기, 프랑스에 내 자유 의지로 와 있는 것이 보이지 않소?\"", "en": "Do you not see me here, in France, of my own will?\""}
}

with open('c:/git_repo/TKprof_book/work_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

for i in range(101, 135):
    entry = queue[i]
    if i in translations:
        # Patch the file
        filepath = os.path.join('c:/git_repo/TKprof_book/books/two_cities/json', entry['file'])
        with open(filepath, 'r', encoding='utf-8') as jf:
            file_data = json.load(jf)
        for block in file_data:
            if block.get('target_raw') == entry['target_raw'] or block.get('tag') == entry['target_raw']:
                block['ko'] = translations[i]['ko']
                block['en'] = translations[i]['en']
                break
        with open(filepath, 'w', encoding='utf-8') as jf:
            json.dump(file_data, jf, ensure_ascii=False, indent=2)
        # Update queue
        entry['status'] = 'done'

with open('c:/git_repo/TKprof_book/work_queue.json', 'w', encoding='utf-8') as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)

print("Batch 1 completed!")
