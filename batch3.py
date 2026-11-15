import json
import os

translations = {
    168: {"ko": "그 불쾌한 단어에 자연스럽게 충격을 받은 찰스 다네이는 자신이 국가의 혼란스러운 상태가 부과한, 그리고 그가 비용을 지불한 호위병과 함께 이동하는 자유로운 여행자이자 프랑스 시민이라는 점에 유의해 달라고 말한 사람에게 요청했다.", "en": "Naturally struck by the disagreeable word, Charles Darnay requested the speaker to take notice that he was a free traveller and French citizen, in charge of an escort which the disturbed state of the country had imposed upon him, and which he had paid for."},
    169: {"ko": "\"어디에,\" 같은 인물이 그에게 전혀 주의를 기울이지 않고 반복했다. \"이 죄수의 서류가 있는가?\"", "en": "\"Where,\" repeated the same personage, without taking any heed of him whatever, \"are the papers of this prisoner?\""},
    170: {"ko": "술 취한 애국자가 그것들을 모자 속에 가지고 있다가 꺼내 주었다.", "en": "The drunken patriot had them in his cap, and produced them."},
    171: {"ko": "권위 있는 같은 인물은 가벨의 편지를 훑어보더니 약간의 혼란과 놀라움을 보였고, 다네이를 주의 깊게 쳐다보았다.", "en": "Casting his eyes over Gabelle's letter, the same personage in authority showed some disorder and surprise, and looked at Darnay with a close attention."},
    172: {"ko": "하지만 그는 아무 말 없이 호위병과 호위받는 자를 남겨두고 위병소 안으로 들어갔다;", "en": "He left escort and escorted without saying a word, however, and went into the guard-room;"},
    173: {"ko": "그동안 그들은 성문 밖에서 말 위에 앉아 있었다.", "en": "meanwhile, they sat upon their horses outside the gate."},
    174: {"ko": "이러한 불확실한 상태에서 주위를 둘러보던 중 찰스 다네이는 성문이 군인과 애국자의 혼합된 경비대에 의해 통제되고 있으며 후자가 전자보다 훨씬 많다는 것을 관찰했다;", "en": "Looking about him while in this state of suspense, Charles Darnay observed that the gate was held by a mixed guard of soldiers and patriots, the latter far outnumbering the former;"},
    175: {"ko": "그리고 보급품을 싣고 들어오는 농부들의 수레와 비슷한 통행 및 상인들의 도시 진입은 충분히 쉬웠지만, 가장 평범한 사람들의 이탈조차도 매우 어려웠다는 것도 관찰했다.", "en": "and that while ingress into the city for peasants' carts bringing in supplies, and for similar traffic and traffickers, was easy enough, egress, even for the homeliest people, was very difficult."},
    176: {"ko": "다양한 종류의 짐승과 수레는 말할 것도 없고, 수많은 남녀 무리가 나가기 위해 기다리고 있었다;", "en": "A numerous medley of men and women, not to mention beasts and vehicles of various sorts, was waiting to issue forth;"},
    177: {"ko": "하지만, 사전 신원 확인이 매우 엄격해서 그들은 장벽을 매우 천천히 통과하고 있었다.", "en": "but, the previous identification was so strict, that they filtered through the barrier very slowly."},
    178: {"ko": "이 사람들 중 일부는 검사를 받을 자신의 차례가 너무 멀었다는 것을 알고 땅에 누워 자거나 담배를 피웠고, 다른 이들은 함께 이야기를 나누거나 어슬렁거렸다.", "en": "Some of these people knew their turn for examination to be so far off, that they lay down on the ground to sleep or smoke, while others talked together, or loitered about."},
    179: {"ko": "붉은 모자와 삼색 기장은 남녀 모두에게 보편적이었다.", "en": "The red cap and tri-colour cockade were universal, both among men and women."},
    180: {"ko": "그가 이런 것들을 메모하며 30분 정도 안장에 앉아 있었을 때, 다네이는 자신을 직면한 같은 권위자가 경비대에게 장벽을 열라고 지시하는 것을 발견했다.", "en": "When he had sat in his saddle some half-hour, taking note of these things, Darnay found himself confronted by the same man in authority, who directed the guard to open the barrier."},
    181: {"ko": "그런 다음 그는 술에 취하고 술에 깬 호위병에게 호위 대상자에 대한 영수증을 전달하고, 그에게 말에서 내릴 것을 요청했다.", "en": "Then he delivered to the escort, drunk and sober, a receipt for the escorted, and requested him to dismount."},
    182: {"ko": "그는 그렇게 했고, 두 애국자는 그의 지친 말을 이끌고 도시에 들어가지 않고 몸을 돌려 떠났다.", "en": "He did so, and the two patriots, leading his tired horse, turned and rode away without entering the city."},
    183: {"ko": "그는 안내자를 따라 싸구려 포도주와 담배 냄새가 나는 위병소 안으로 들어갔는데, 그곳에는 몇몇 군인과 애국자들이 자거나 깨어 있고, 취하거나 깨어 있었으며, 잠과 깸, 취함과 맨 정신 사이의 다양한 중립적 상태에서 서 있거나 누워 있었다.", "en": "He accompanied his conductor into a guard-room, smelling of common wine and tobacco, where certain soldiers and patriots, asleep and awake, drunk and sober, and in various neutral states between sleeping and waking, drunkenness and sobriety, were standing and lying about."},
    184: {"ko": "위병소의 빛은 절반은 밤의 희미해지는 기름 램프에서, 절반은 흐린 낮에서 비롯되어 상응하게 불확실한 상태였다.", "en": "The light in the guard-house, half derived from the waning oil-lamps of the night, and half from the overcast day, was in a correspondingly uncertain condition."},
    185: {"ko": "책상 위에는 몇 권의 장부가 펼쳐져 있었고, 거칠고 어두운 인상의 한 장교가 그것들을 주재하고 있었다.", "en": "Some registers were lying open on a desk, and an officer of a coarse, dark aspect, presided over these."},
    186: {"ko": "\"드파르주 시민,\" 그가 무언가를 쓰기 위해 종이 한 장을 집어 들며 다네이의 안내자에게 말했다. \"이 자가 망명자 에브레몽드인가?\"", "en": "\"Citizen Defarge,\" said he to Darnay's conductor, as he took a slip of paper to write on. \"Is this the emigrant Evrémonde?\""},
    187: {"ko": "\"이 사람이 그 사람입니다.\"", "en": "\"This is the man.\""},
    188: {"ko": "\"당신의 나이, 에브레몽드?\"", "en": "\"Your age, Evrémonde?\""},
    189: {"ko": "\"서른일곱.\"", "en": "\"Thirty-seven.\""},
    190: {"ko": "\"결혼했나, 에브레몽드?\"", "en": "\"Married, Evrémonde?\""},
    191: {"ko": "\"그렇소.\"", "en": "\"Yes.\""},
    192: {"ko": "\"어디서 결혼했나?\"", "en": "\"Where married?\""},
    193: {"ko": "\"영국에서요.\"", "en": "\"In England.\""},
    194: {"ko": "\"의심의 여지 없이.", "en": "\"Without doubt."},
    195: {"ko": "당신의 아내는 어디 있소, 에브레몽드?\"", "en": "Where is your wife, Evrémonde?\""},
    196: {"ko": "\"영국에 있소.\"", "en": "\"In England.\""},
    197: {"ko": "\"의심의 여지 없이.", "en": "\"Without doubt."},
    198: {"ko": "당신은 라 포스(La Force) 감옥으로 보내질 것이오, 에브레몽드.\"", "en": "You are consigned, Evrémonde, to the prison of La Force.\""},
    199: {"ko": "\"세상에!\" 다네이가 소리쳤다. \"어떤 법에 의해서, 그리고 어떤 죄목으로 말입니까?\"", "en": "\"Just Heaven!\" exclaimed Darnay. \"Under what law, and for what offence?\""},
    200: {"ko": "장교는 잠시 종이에서 눈을 들어 올려다보았다.", "en": "The officer looked up from his slip of paper for a moment."}
}

with open('c:/git_repo/TKprof_book/work_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

for i in range(168, 201):
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

print("Batch 3 completed!")
