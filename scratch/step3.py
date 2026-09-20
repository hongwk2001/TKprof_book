import json

translations = {
    81: {"ko": "드파르주가 난간과 테이블을 훌쩍 뛰어넘어 비참한 꼴의 늙은이를 치명적인 포옹으로 움켜잡았을 때, 마담 드파르주가 뒤따라가 그를 묶고 있던 밧줄 중 하나에 손을 감았을 때, '복수'와 자크 3호는 아직 그들에게 다가가지 못했고, 창문에 있던 남자들도 맹금류처럼 높은 횃대에서 심문실로 뛰어내리지도 않았을 때였다. 그때 도시 전역에서 이런 외침이 울려 퍼지는 듯했다. \"그놈을 끌어내라!", "en": "Defarge had merely vaulted over a railing and a table to grasp the wretched old man in a deadly embrace, and Madame Defarge had followed to twist her hand into one of the ropes binding him—The Vengeance and Jacques Three had not yet reached them, nor had the men at the windows swooped down into the Hall like birds of prey from high perches—when a cry seemed to erupt all over the city. \"Drag him out!"},
    82: {"ko": "그놈을 가로등으로 끌고 가라!\"", "en": "Drag him to the street lamp!\""},
    83: {"ko": "넘어지고, 일어나고, 건물 계단에 머리를 처박으며,", "en": "Down, up, and headfirst onto the steps of the building;"},
    84: {"ko": "때로는 무릎을 꿇고,", "en": "now on his knees;"},
    85: {"ko": "때로는 발로 서서,", "en": "now on his feet;"},
    86: {"ko": "때로는 등을 땅에 댄 채,", "en": "now on his back;"},
    87: {"ko": "그는 질끌려가고, 구타당하고, 수백 개의 손이 그의 얼굴에 쑤셔 넣는 풀과 짚단에 숨이 막혔다.", "en": "he was dragged, beaten, and suffocated by bunches of grass and straw thrust into his face by hundreds of hands;"},
    88: {"ko": "찢기고, 멍들고, 헐떡이고, 피를 흘리면서도, 그는 언제나 자비를 구하며 애원하고 빌었다.", "en": "torn, bruised, panting, bleeding, yet always begging and pleading for mercy;"},
    89: {"ko": "때로는 격렬한 고통에 몸부림쳤고, 사람들이 구경하기 위해 서로를 뒤로 밀치면서 그의 주변에 작은 빈 공간이 생기기도 했다.", "en": "now struggling in fierce agony, with a small open space forming around him as the people pushed each other back to get a better look;"},
    90: {"ko": "때로는 다리들의 숲 사이로 끌려가는 한 토막의 죽은 통나무 같기도 했다.", "en": "now resembling a dead log dragged through a forest of legs;"},
    91: {"ko": "그는 치명적인 올가미가 매달려 있는 가장 가까운 길모퉁이로 끌려갔다. 그곳에서 마담 드파르주는 고양이가 쥐를 놓아주듯 그를 풀어주었다. 그리고 사람들이 사형 준비를 하는 동안, 그가 그녀에게 애원하는 동안에도 조용하고 침착하게 그를 지켜보았다.", "en": "he was hauled to the nearest street corner where a fatal lamp swung. There, Madame Defarge let him go—just as a cat might drop a mouse—and silently and calmly watched him while the preparations were made, and while he pleaded with her:"},
    92: {"ko": "여자들은 시종일관 그에게 분노의 비명을 질러댔고, 남자들은 입에 풀을 물린 채 그를 죽여버리라고 단호하게 외쳤다.", "en": "the women passionately screamed at him the whole time, and the men sternly shouted to have him killed with grass in his mouth."},
    93: {"ko": "그가 허공으로 한 번 매달렸을 때 밧줄이 끊어졌고, 사람들은 비명을 지르는 그를 붙잡았다.", "en": "Once he was strung up, and the rope broke, and they caught him screaming;"},
    94: {"ko": "그가 두 번째 매달렸을 때도 밧줄이 끊어졌고, 사람들은 비명을 지르는 그를 붙잡았다.", "en": "twice he was strung up, and the rope broke, and they caught him screaming;"},
    95: {"ko": "세 번째는 밧줄이 자비를 베풀어 그를 매달아 주었다. 그의 머리는 곧 창끝에 꽂혔고, 생앙투안 전체가 춤출 만큼 입 안에는 풀이 가득 물려 있었다.", "en": "then the rope was merciful and held him. His head was soon mounted on a pike, with enough grass stuffed in his mouth for all of Saint Antoine to dance at the sight of."},
    96: {"ko": "이것으로 그날의 끔찍한 일은 끝나지 않았다. 생앙투안 사람들은 소리 지르고 춤을 추며 분노의 피를 들끓게 한 나머지, 날이 저물 무렵 죽은 자의 사위이자 인민의 적이며 모욕자인 또 다른 자가 500명의 강력한 기병대 호위를 받으며 파리로 오고 있다는 소식을 듣고는 피가 다시 끓어올랐다.", "en": "Nor was this the end of the day's grim work. Saint Antoine shouted and danced its angry blood up so high that it boiled over once more upon hearing, at nightfall, that the dead man's son-in-law—another enemy and insulter of the people—was coming into Paris under an escort of five hundred cavalry."},
    97: {"ko": "생앙투안은 그의 죄목을 불타오르듯 시뻘건 종이에 적어 그를 붙잡았다. 군대의 품에서 그를 빼내 풀롱의 길동무로 만들려 했던 사람들은, 그의 머리와 심장을 창끝에 꽂고 그날의 전리품 세 개를 든 채 마치 늑대 떼처럼 거리를 행진했다.", "en": "Saint Antoine wrote his crimes on glaring sheets of paper, seized him (they would have torn him from the breast of an army to make him Foulon's companion), mounted his head and heart on pikes, and paraded the three spoils of the day through the streets in a wolf-like procession."},
    98: {"ko": "깜깜한 밤이 되어서야 남녀들은 울부짖고 빵도 없는 아이들에게 돌아갔다.", "en": "Not until pitch-black night did the men and women return to their wailing and breadless children."},
    99: {"ko": "그러고 나서 초라한 빵집은 형편없는 빵이라도 사려고 참을성 있게 기다리는 긴 줄로 둘러싸였다.", "en": "Then, the miserable bakeries were besieged by long lines of people, patiently waiting to buy bad bread;"},
    100: {"ko": "그들은 주린 배를 안고 기다리는 동안, 그날 거둔 승리를 기념하며 서로 안아주고 험담 속에서 다시금 승리를 재현하며 시간을 보냈다.", "en": "and while they waited with empty, fainting stomachs, they passed the time by embracing each other over the day's triumphs and reliving them through gossip."},
    101: {"ko": "점차 남루한 옷차림의 이 긴 줄은 짧아지고 흩어졌다.", "en": "Gradually, these lines of ragged people shortened and dispersed;"},
    102: {"ko": "그런 다음 높은 창문에서 희미한 불빛이 반짝이기 시작했고, 거리에 가느다란 불을 피워 이웃들이 함께 요리를 한 뒤 자기 집 문가에서 저녁을 먹었다.", "en": "and then weak lights began to shine from high windows. Slender fires were built in the streets, over which neighbors cooked communally, later eating their suppers at their doors."},
    103: {"ko": "그것은 형편없는 빵에 곁들일 소스는커녕 고기조차 구경할 수 없는 빈약하고 부족한 저녁 식사였다.", "en": "Those were meager and insufficient suppers, devoid of meat as well as most other sauces for the wretched bread."},
    104: {"ko": "하지만 인간적인 유대감은 돌덩이 같은 음식에 약간의 영양분을 불어넣었고, 그 속에서 일말의 유쾌한 불꽃을 일으켰다.", "en": "Yet, human fellowship infused some nourishment into the rock-hard food and struck a few sparks of cheerfulness out of it."},
    105: {"ko": "그날 최악의 상황 속에서 자기 몫을 다한 아버지와 어머니들은 앙상한 아이들과 부드럽게 놀아주었다.", "en": "Fathers and mothers who had fully partaken in the worst events of the day played gently with their emaciated children;"},
    106: {"ko": "그리고 연인들은 그들을 둘러싸고 그들 앞에 놓인 세상 속에서도 사랑하고 희망을 품었다.", "en": "and lovers, with such a world around them and before them, still loved and hoped."},
    107: {"ko": "동이 틀 무렵, 드파르주의 와인 가게에서 마지막 손님 무리가 떠나갔을 때, 드파르주 씨는 문을 잠그며 아내 마담에게 쉰 목소리로 말했다.", "en": "It was almost morning when Defarge's wine shop saw its last group of customers depart. Monsieur Defarge, locking the door, spoke to his wife in a husky voice:"},
    108: {"ko": "\"드디어 그날이 왔소, 여보!\"", "en": "\"It has finally come, my dear!\""},
    109: {"ko": "\"글쎄요!\" 마담이 대답했다. \"거의 왔죠.\"", "en": "\"Well!\" returned madame. \"Almost.\""},
    110: {"ko": "생앙투안은 잠들었고, 드파르주 부부도 잠들었다.", "en": "Saint Antoine slept, and the Defarges slept;"},
    111: {"ko": "심지어 '복수'도 굶주린 식료품 장수 남편과 함께 잠들었고, 북소리도 멈췄다.", "en": "even The Vengeance slept with her starving grocer, and the drum was silent."},
    112: {"ko": "생앙투안에서 유혈 사태와 광란의 혼란 속에서도 변하지 않은 목소리는 오직 북소리뿐이었다.", "en": "The drum's voice was the only one in Saint Antoine that the bloodshed and frantic rush had not changed."},
    113: {"ko": "북의 관리자인 '복수'는 그를 깨워 바스티유 감옥이 무너지기 전이나 늙은 풀롱이 잡히기 전과 똑같은 소리를 내게 할 수 있었다.", "en": "The Vengeance, as the drum's custodian, could have awakened him and produced the exact same sound as before the Bastille fell or old Foulon was captured;"},
    114: {"ko": "하지만 생앙투안의 가슴속에 있는 남녀들의 쉰 목소리는 그렇지 않았다.", "en": "but the same was not true for the hoarse voices of the men and women in the heart of Saint Antoine."}
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

print("Batch 3 completed")
