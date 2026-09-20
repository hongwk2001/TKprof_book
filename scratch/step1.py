import json

translations = {
    1: {"ko": "[2부 22장: 바다는 여전히 차오른다]", "en": ""},
    2: {"ko": "굶주리고 지친 생앙투안(Saint Antoine) 사람들에게는 단 일주일의 환희만이 허락되었다. 마담 드파르주(Madame Defarge)가 평소처럼 계산대에 앉아 손님들을 맞이하고 있을 때, 그들은 빈약하고 딱딱한 빵을 형제애가 담긴 포옹과 축하로 애써 부드럽게 넘기며 그 일주일을 만끽했다.", "en": "The famished and exhausted people of Saint Antoine were granted only a single week of exultation. While Madame Defarge sat at her counter greeting customers as usual, they savored that week, struggling to swallow their meager and hard bread by softening it with fraternal embraces and congratulations."},
    3: {"ko": "마담 드파르주는 머리에 장미(스파이가 있음을 알리는 신호)를 꽂지 않았다. 단 일주일 만에 스파이 집단이 생앙투안 사람들의 자비를 믿고 나타나는 것을 극도로 꺼리게 되었기 때문이다.", "en": "Madame Defarge did not wear a rose (a signal that a spy was present) in her hair. This was because, in just a single week, the brotherhood of spies had become extremely reluctant to show themselves, no longer trusting the mercy of the people of Saint Antoine."},
    4: {"ko": "거리의 가로등은 불길할 정도로 탄력 있게 흔들리고 있었다 (가로등에 사람을 매달아 처형하는 광경을 암시함).", "en": "The street lamps were swinging with an ominously elastic motion (hinting at the sight of people being hanged from them)."},
    5: {"ko": "마담 드파르주는 팔짱을 낀 채 아침 햇살과 열기 속에 앉아 와인 가게와 거리를 응시하고 있었다.", "en": "Madame Defarge sat in the morning sunlight and heat with her arms folded, gazing at the wine shop and the street."},
    6: {"ko": "가게 안과 거리 모두에는 비참하고 남루한 몰골의 사람들이 무리를 지어 서성거리고 있었다. 그러나 이제 그들의 고통스러운 표정 위로는 권력을 쥐었다는 뚜렷한 자각이 자리 잡고 있었다.", "en": "Both inside the shop and on the street, groups of wretched and shabby people were lingering. Yet, above their anguished expressions, a clear realization of holding power was now firmly seated."},
    7: {"ko": "가장 비참한 머리 위에 비뚤어지게 얹힌 가장 너덜너덜한 수면 모자조차도 이런 뒤틀린 의미를 품고 있었다.", "en": "Even the most tattered nightcap, perched askew on the most wretched head, harbored this twisted meaning:"},
    8: {"ko": "\"이 모자를 쓴 내가 스스로의 목숨을 부지하는 것이 얼마나 끔찍하게 어려워졌는지 나는 잘 알고 있다.", "en": "\"I know all too well how terribly difficult it has become for me, the wearer of this hat, to simply sustain my own life."},
    9: {"ko": "하지만 이 모자를 쓴 내가 네 목숨을 빼앗는 것은 얼마나 쉬워졌는지 너는 아는가?\" 예전에는 일자리가 없어 놀고 있던 마르고 벌거벗은 팔들마다 이제는 언제든 타격을 가할 준비가 되어 있었다.", "en": "But do you know how easy it has become for me, the wearer of this hat, to take your life?\" Every thin, bare arm that previously had no work to do was now constantly ready to strike a blow."},
    10: {"ko": "뜨개질하는 여자들의 손가락은 무언가를 찢어발길 수 있다는 경험에서 우러나온 악의로 가득 차 있었다.", "en": "The fingers of the knitting women were filled with a viciousness born from the experience that they could tear things apart."},
    11: {"ko": "생앙투안 사람들의 겉모습에도 변화가 일어났다.", "en": "A change had also occurred in the outward appearance of the people of Saint Antoine."},
    12: {"ko": "수백 년 동안 가해진 억압이 사람들의 모습을 벼려왔고, 마침내 그 마지막 일격이 그들의 표정에 강력하게 새겨진 것이다.", "en": "The oppression inflicted over hundreds of years had forged the people's appearance, and finally, the finishing blow had been powerfully engraved upon their expressions."},
    13: {"ko": "마담 드파르주는 생앙투안 여성들의 지도자에게 걸맞은 억눌린 찬동의 눈빛으로 그 광경을 지켜보고 앉아 있었다.", "en": "Madame Defarge sat watching the scene with a gaze of suppressed approval befitting the leader of the women of Saint Antoine."},
    14: {"ko": "그녀의 자매 조직 중 한 명이 그녀 곁에서 뜨개질을 하고 있었다.", "en": "One of her sisterhood was knitting beside her."},
    15: {"ko": "굶주린 식료품 장수의 아내이자 두 아이의 어머니인 이 통통하고 키 작은 부관은 이미 '복수'라는 영광스러운 별명을 얻은 상태였다.", "en": "The short and plump wife of a starving grocer and mother of two children, this lieutenant had already earned the glorious nickname of 'The Vengeance'."},
    16: {"ko": "\"가만!\" '복수'가 말했다. \"다들 들어봐!", "en": "\"Wait!\" said The Vengeance. \"Listen, everyone!"},
    17: {"ko": "누가 오고 있지?\"", "en": "Who is coming?\""},
    18: {"ko": "생앙투안 구역의 가장 바깥 경계에서부터 와인 가게 문 앞까지 깔린 화약선에 갑자기 불이 붙은 것처럼, 웅성거리는 소리가 빠르게 퍼지며 밀려왔다.", "en": "Like a trail of gunpowder laid from the outermost boundary of the Saint Antoine Quarter to the door of the wine shop suddenly catching fire, a murmuring sound spread rapidly and rushed in."},
    19: {"ko": "\"드파르주예요.\" 마담이 말했다. \"애국자 여러분, 조용히!\"", "en": "\"It is Defarge,\" said madame. \"Silence, patriots!\""},
    20: {"ko": "드파르주는 숨을 헐떡이며 들어와 자신이 쓰고 있던 붉은 모자(자유의 모자)를 벗고 주위를 둘러보았다! \"모두 들으세요!\" 마담이 다시 말했다. \"그의 말을 들으세요!\" 문 밖에 모인 사람들의 열띤 눈빛과 벌어진 입들을 배경으로, 드파르주는 가쁜 숨을 몰아쉬며 서 있었다.", "en": "Defarge came in panting, took off his red cap (a cap of liberty), and looked around! \"Listen, everyone!\" madame said again. \"Listen to him!\" Against the backdrop of eager eyes and open mouths gathered outside the door, Defarge stood gasping for breath."},
    21: {"ko": "와인 가게 안에 있던 사람들은 모두 자리에서 벌떡 일어났다.", "en": "All the people inside the wine shop sprang to their feet."},
    22: {"ko": "\"어서 말해 봐요, 여보.", "en": "\"Speak up, dear."},
    23: {"ko": "무슨 일이죠?\"", "en": "What is it?\""},
    24: {"ko": "\"저승에서 온 소식이오!\"", "en": "\"News from the other world!\""},
    25: {"ko": "\"그게 무슨 소리죠?\" 마담이 경멸하듯 외쳤다. \"저승이라니요?\"", "en": "\"What do you mean?\" cried madame with contempt. \"The other world?\""},
    26: {"ko": "\"여기 있는 모두가 늙은 풀롱을 기억하시오? 굶주린 사람들에게 풀이나 뜯어 먹으라고 말하고는 죽어서 지옥에 간 그 자식 말이오.\"", "en": "\"Do all of you here remember old Foulon? The bastard who told the starving people to eat grass, and then died and went to hell.\""},
    27: {"ko": "\"모두 기억하지!\" 사람들의 목구멍에서 이구동성으로 터져 나왔다.", "en": "\"We all remember!\" burst forth unanimously from the throats of the people."},
    28: {"ko": "\"바로 그놈에 대한 소식이오.", "en": "\"The news is about him."},
    29: {"ko": "그놈이 우리 곁에 있소!\"", "en": "He is here among us!\""},
    30: {"ko": "\"우리 곁에 있다니!\" 사람들은 다시 한목소리로 외쳤다. \"죽은 놈이?\"", "en": "\"Among us!\" the people cried out in one voice again. \"A dead man?\""},
    31: {"ko": "\"죽지 않았소!", "en": "\"He is not dead!"},
    32: {"ko": "그놈은 우리를 너무나 두려워한 나머지 자기가 죽은 것처럼 위장하고 거창한 가짜 장례식까지 치렀소.", "en": "He was so terrified of us that he faked his own death and even held a grand mock funeral."},
    33: {"ko": "하지만 시골에 숨어 있던 그놈이 산 채로 발각되어 끌려왔소.", "en": "But he was found alive hiding in the countryside, and they dragged him in."},
    34: {"ko": "방금 전 시청으로 압송되어 가는 그 죄수의 모습을 내 두 눈으로 똑똑히 보았소.", "en": "I just clearly saw with my own two eyes that prisoner being escorted to the City Hall."},
    35: {"ko": "그놈이 우리를 두려워할 만한 이유가 있다고 아까 말했지.", "en": "I said earlier that he had reason to fear us."},
    36: {"ko": "다들 말해 보시오! 과연 그럴 이유가 있었소?\"", "en": "Tell me, everyone! Did he indeed have reason to?\""},
    37: {"ko": "70세가 넘은 비열하고 늙은 죄인이 그 사실을 아직 모르고 있었다 할지라도, 이에 화답하는 사람들의 울부짖음을 들었다면 마음 깊은 곳에서부터 뼈저리게 깨달았을 것이다.", "en": "Even if the despicable old sinner over the age of seventy had not yet known it, he would have deeply realized it in the core of his heart had he heard the howling response of the people."},
    38: {"ko": "순간 깊은 침묵이 흘렀다.", "en": "For a moment, a profound silence flowed."},
    39: {"ko": "드파르주와 그의 아내는 굳은 표정으로 서로를 응시했다.", "en": "Defarge and his wife gazed steadily at one another with stern expressions."},
    40: {"ko": "'복수'가 몸을 굽혔고, 계산대 뒤 발밑에서 그녀가 북을 움직이자 덜거덕거리는 북소리가 들려왔다.", "en": "The Vengeance bent down, and a rattling sound was heard as she moved a drum at her feet behind the counter."},
    41: {"ko": "\"애국자 여러분!\" 드파르주가 결연한 목소리로 말했다. \"준비되었소?\"", "en": "\"Patriots!\" Defarge said in a resolute voice. \"Are we ready?\""},
    42: {"ko": "그 즉시 마담 드파르주의 칼이 그녀의 허리띠에 꽂혔다.", "en": "Instantly, Madame Defarge's knife was thrust into her girdle."},
    43: {"ko": "거리에서는 마치 북과 북 치는 사람이 마법처럼 허공을 날아다니는 듯 북소리가 울려 퍼졌다.", "en": "In the streets, the beating of a drum echoed as if the drum and the drummer were magically flying through the air."},
    44: {"ko": "그리고 '복수'는 끔찍한 비명을 지르며 양팔을 머리 위로 휘두른 채 이 집 저 집을 뛰어다니며 여자들을 선동했다.", "en": "And The Vengeance, screaming terribly and flailing her arms above her head, dashed from house to house, inciting the women."},
    45: {"ko": "창밖을 내다보며 살의에 찬 분노를 번뜩이고, 손에 잡히는 무기는 무엇이든 집어 들고 거리로 쏟아져 나오는 남자들의 모습은 끔찍했다.", "en": "The men were a terrifying sight, flashing murderous anger as they looked out of windows, grabbing whatever weapons they could find, and pouring out into the streets."},
    46: {"ko": "하지만 가장 용감한 사람조차도 오싹하게 만들 만큼 섬뜩한 광경은 바로 여자들이었다.", "en": "However, the women presented a sight eerie enough to chill even the bravest soul."},
    47: {"ko": "그들은 지독한 가난 속에서 하던 집안일마저 내팽개쳤고, 노약자들과 아이들도 버려둔 채 헝클어진 머리를 휘날리며 뛰쳐나왔다. 그들은 광기에 찬 비명과 몸짓으로 스스로를 미치도록 부추겼다.", "en": "They abandoned the household chores born of desperate poverty, leaving behind the elderly and children, and rushed out with disheveled hair flying. They incited themselves into madness with frantic cries and gestures."},
    48: {"ko": "자매여, 악당 풀롱이 잡혔어!", "en": "Sister, the villain Foulon has been caught!"},
    49: {"ko": "어머니, 늙은 풀롱이 잡혔어요!", "en": "Mother, old Foulon has been caught!"},
    50: {"ko": "내 딸아, 짐승 같은 풀롱이 잡혔단다!", "en": "My daughter, the beastly Foulon has been caught!"}
}

file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_22.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if item['id'] in translations:
        item['ko'] = translations[item['id']]['ko']
        if not item.get('is_header'):
            item['en'] = translations[item['id']]['en']

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Batch 1 completed")
