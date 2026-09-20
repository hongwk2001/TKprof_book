import json

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_24.json'

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

patches = {
    'P002_1': {
        'ko': '불길이 솟아오르고 바다가 솟구치는 듯한 혼란 속에서(risings of fire and risings of sea)—단단한 대지는 썰물 없이 계속해서 밀려들며 점점 더 높이 차오르는 성난 바다의 맹렬한 기세에 흔들렸고, 물가에서 이를 지켜보는 이들(beholders on the shore)은 공포와 경이에 휩싸였습니다—그렇게 폭풍 같은 3년의 세월이 흘러갔습니다.',
        'en': 'In such turmoil of surging fire and rising seas—the solid earth shaken by the fierce rushes of an angry ocean that no longer had an ebb, but constantly flowed higher and higher, to the terror and awe of those watching on the shore—three tempestuous years passed by.'
    },
    'P002_2': {
        'ko': '어린 Lucie의 생일이 세 번 더 지나갔고, 이 시간들은 황금 실(golden thread)에 의해 그녀 가정의 평화로운 삶의 직물 속으로 짜여 들어갔습니다.',
        'en': "Three more birthdays of little Lucie passed, and these times were woven by the golden thread into the peaceful fabric of her family's life."
    },
    'P003_1': {
        'ko': '수많은 밤과 낮 동안 그 집의 거주자(inmates)들은 구석에서 울려 퍼지는 메아리에 귀를 기울였고, 몰려드는 발소리를 들을 때면 가슴이 철렁 내려앉았습니다.',
        'en': 'For many nights and days, the residents of the house listened to the echoes in the corner, and their hearts sank whenever they heard the sound of crowding footsteps.'
    },
    'P003_2': {
        'ko': '왜냐하면, 그들의 마음속에 그 발소리는 붉은 깃발 아래 소란을 피우고 조국이 위험에 처했다고 선언된 가운데, 오랫동안 지속된 끔찍한 마법(terrible enchantment)으로 인해 야수로 변해버린 군중의 발소리처럼 느껴졌기 때문입니다.',
        'en': 'This was because, in their minds, the footsteps sounded like those of a mob rioting under a red flag with their country declared in peril, having been turned into wild beasts by a terrible and long-lasting enchantment.'
    },
    'P004_2': {
        'ko': '프랑스에서 그가 전혀 환영받지 못하여, 그곳에서 쫓겨나고 이 목숨까지 잃게 될(receiving his dismissal from it, and this life together) 상당한 위험에 처해 있다는 것이었습니다.',
        'en': 'of him being so unwelcome in France that he faced the considerable danger of being expelled from it and losing his life as well.'
    },
    'P004_3': {
        'ko': '엄청난 수고를 들여 악마를 불러내고는 막상 그 모습을 보자 너무나 겁에 질린 나머지, 그 악마(Enemy)에게 아무것도 묻지 못하고 즉시 도망쳐버렸다는 전설 속의 농부(fabled rustic)처럼;',
        'en': "Like the legendary peasant who went to infinite trouble to summon the Devil, only to be so terrified at the sight of him that he couldn't ask the Enemy a single question and fled immediately;"
    },
    'P004_4': {
        'ko': "Monseigneur 역시 수년 동안 주기도문(Lord's Prayer)을 거꾸로 대담하게 외우고, 악마(Evil One)를 복종시키기 위한 여러 강력한 주문을 외웠음에도 불구하고, 그 끔찍한 악마의 모습을 보자마자 그의 고귀한 발걸음을 돌려 줄행랑을 쳤습니다(took to his noble heels).",
        'en': "so Monseigneur, after boldly reciting the Lord's Prayer backwards for many years and performing various other powerful spells to command the Evil One, no sooner saw his terrifying figure than he took to his noble heels and fled."
    },
    'P005_1': {
        'ko': "궁정의 빛나던 과녁(Bull's Eye)은 사라졌습니다. 만약 남아 있었더라면, 그것은 국가가 쏘아대는 폭풍 같은 총탄의 표적이 되었을 것입니다.",
        'en': "The shining Bull's Eye of the Court was gone, and had it remained, it would have been the target of a hurricane of the nation's bullets."
    },
    'P005_2': {
        'ko': '그것은 애초에 무엇을 제대로 볼 수 있는 좋은 눈이 아니었으며, 오랫동안 루시퍼(Lucifer)의 교만, 사르다나팔루스(Sardanapalus)의 사치, 그리고 두더지의 눈먼 상태라는 티끌(mote)이 끼어 있었지만, 결국 빠져나가 사라져 버렸습니다.',
        'en': "It had never been a useful eye for seeing—having long suffered from the speck of Lucifer's pride, Sardanapalus's luxury, and the blindness of a mole—but it had fallen out and was now gone."
    },
    'P005_3': {
        'ko': '배타적인 내부 계층부터 음모, 부패, 위선으로 가득 찬 썩어빠진 바깥쪽 외곽(outermost rotten ring)에 이르기까지, 궁정 전체가 한꺼번에 사라져 버렸습니다.',
        'en': 'The entire Court, from its exclusive inner circle to its outermost rotten ring of conspiracy, corruption, and hypocrisy, had all vanished together.'
    }
}

count = 0
for item in data:
    if item.get('tag') in patches:
        item['ko'] = patches[item['tag']]['ko']
        item['en'] = patches[item['tag']]['en']
        count += 1

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Patched {count} items.')
