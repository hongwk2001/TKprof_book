import json
import os

translations = {
    "book1_ch_02.json": {
        79: {"ko": "\"이 전령은 제가 압니다, 차장님,\" 로리 씨가 마차에서 내려 도로로 나오며 말했다. 다른 두 승객이 그를 빠르고 다소 무례하게 뒤에서 밀어내듯 도와주었고, 그들은 즉시 마차로 기어올라가 문을 닫고 창문을 올렸다. \"그가 가까이 와도 좋습니다;\"", "en": "\"I know this messenger, guard,\" said Mr. Lorry, getting down into the road--assisted from behind more swiftly than politely by the other two passengers, who immediately scrambled into the coach, shut the door, and pulled up the window. \"He may come close;\""}
    },
    "book1_ch_04.json": {
        7: {"ko": "승객인 로리 씨는 짚투성이 엉킨 거친 외투, 펄럭이는 모자, 진흙투성이 다리에서 묻은 것을 털어내며 일어났는데, 마치 커다란 개와 같았다.", "en": "Mr. Lorry, the passenger, shaking himself out of it in chains of straw, a tangle of shaggy wrapper, flapping hat, and muddy legs, was rather like a larger sort of dog."},
        35: {"ko": "자신의 초상화를 위해 앉아 있는 사람과 완벽하게 닮은 모습으로, 로리 씨는 잠에 빠져들었다.", "en": "Completing his resemblance to a man who was sitting for his portrait, Mr. Lorry dropped off to sleep."},
        38: {"ko": "그녀가 자비스 로리 씨를 찾거나 텔슨 은행에서 온 신사를 찾을지도 모릅니다.", "en": "She may ask for Mr. Jarvis Lorry, or she may only ask for a gentleman from Tellson’s Bank."},
        62: {"ko": "아침 식사를 마친 로리 씨는 해변을 산책하러 나갔다.", "en": "When Mr. Lorry had finished his breakfast, he went out for a stroll on the beach."},
        70: {"ko": "오후가 되어 한때 프랑스 해안이 보일 정도로 맑았던 공기가 다시 안개와 수증기로 가득 차자, 로리 씨의 생각도 함께 흐려지는 듯했다.", "en": "As the day declined into the afternoon, and the air, which had been at intervals clear enough to allow the French coast to be seen, became again charged with mist and vapour, Mr. Lorry’s thoughts seemed to cloud too."},
        73: {"ko": "오랫동안 아무 일 없이 시간을 보내던 로리 씨가 와인 병을 다 비운 혈색 좋은 노신사에게서나 볼 수 있는 완벽한 만족감을 보이며 마지막 와인 잔을 따랐을 때, 좁은 거리를 따라 바퀴 굴러가는 소리가 요란하게 들려오더니 여관 뜰 안으로 덜컹거리며 들어왔다.", "en": "Mr. Lorry had been idle a long time, and had just poured out his last glassful of wine with as complete an appearance of satisfaction as is ever to be found in an elderly gentleman of a fresh complexion who has got to the end of a bottle, when a rattling of wheels came up the narrow street, and rumbled into the inn-yard."},
        82: {"ko": "어둠이 너무 짙어 뚫어보기 어려웠기에 로리 씨는 낡은 터키 양탄자 위를 조심스레 걸으며 마네트 양이 잠시 옆방에 있을 것이라 생각했다. 그러나 두 개의 커다란 촛불을 지나치자, 그 촛불들과 난로 사이의 탁자 곁에 승마용 망토를 입고 밀짚 여행용 모자의 리본을 손에 든 열일곱 살도 안 되어 보이는 젊은 아가씨가 그를 맞이하러 서 있는 것을 보았다.", "en": "The obscurity was so difficult to penetrate that Mr. Lorry, picking his way over the well-worn Turkey carpet, supposed Miss Manette to be, for the moment, in some adjacent room, until, having got past the two tall candles, he saw standing to receive him by the table between them and the fire, a young lady of not more than seventeen, in a riding-cloak, and still holding her straw travelling-hat by its ribbon in her hand."},
        87: {"ko": "\"아가씨의 손에 입맞춥니다,\" 로리 씨가 다시 정중하게 인사를 하고 자리에 앉으며 구시대적인 예의를 갖추어 말했다.", "en": "\"I kiss your hand, miss,\" said Mr. Lorry, with the manners of an earlier date, as he made his formal bow again, and took his seat."},
        92: {"ko": "로리 씨는 의자에서 몸을 움직이며 병원 행렬 같은 흑인 큐피드들을 향해 근심 어린 시선을 던졌다.", "en": "Mr. Lorry moved in his chair, and cast a troubled look towards the hospital procession of negro cupids."},
        101: {"ko": "\"그 임무를 맡게 되어 기뻤습니다.\" 로리 씨가 말했다.", "en": "\"I was happy,\" said Mr. Lorry, \"to be entrusted with the charge.\""},
        107: {"ko": "\"당연합니다,\" 로리 씨가 말했다. \"네--저는--\"", "en": "\"Naturally,\" said Mr. Lorry. \"Yes--I--\""},
        112: {"ko": "\"제가 그렇지 않습니까?\" 로리 씨는 손을 펴고 밖으로 뻗으며 논증하는 듯한 미소를 지었다.", "en": "\"Am I not?\" Mr. Lorry opened his hands, and extended them outwards with an argumentative smile."},
        148: {"ko": "로리 씨는 믿음을 가지고 다가와 주춤거리는 작은 손을 잡아 다소 의례적으로 자신의 입술에 가져다 대었다.", "en": "Mr. Lorry took the hesitating little hand that confidingly advanced to take his, and he put it with some ceremony to his lips."},
        164: {"ko": "\"부탁입니다,\" 로리 씨가 달래는 듯한 목소리로 말하며, 의자 등받이에 두었던 왼손을 가져와 격렬하게 떨며 자신을 붙잡은 애원하는 손가락들 위에 얹었다.", "en": "\"Pray,\" said Mr. Lorry, in a soothing tone, bringing his left hand from the back of the chair to lay it on the supplicatory fingers that clasped him in so violent a tremble:"},
        225: {"ko": "로리 씨는 자신의 팔을 잡고 있는 그녀의 손을 조용히 문질렀다. \"자, 자, 자!\"", "en": "Mr. Lorry quietly chafed the hands that held his arm. \"There, there, there!\""},
        230: {"ko": "\"단 한 가지 더,\" 로리 씨가 그녀의 주의를 끌기 위한 유용한 수단으로 강조하며 말했다.", "en": "\"Only one thing more,\" said Mr. Lorry, laying stress upon it as a wholesome means of enforcing her attention:"},
        248: {"ko": "당황한 와중에도 로리 씨가 보기에 온통 붉은색을 띠고 붉은 머리를 했으며 유별나게 몸에 꼭 맞는 옷을 입고 머리에는 척탄병의 나무통이나 거대한 스틸턴 치즈 같은 엄청난 모자를 쓴 야성적으로 보이는 여성이 여관 하인들보다 먼저 방으로 달려 들어왔다. 그녀는 건장한 손을 그의 가슴에 얹고 그를 가장 가까운 벽으로 날려버림으로써 가엾은 젊은 아가씨에게서 그를 떼어내는 문제를 단숨에 해결했다.", "en": "A wild-looking woman, whom even in his agitation, Mr. Lorry observed to be all of a red colour, and to have red hair, and to be dressed in some extraordinary tight-fitting fashion, and to have on her head a most wonderful bonnet like a Grenadier wooden measure, and good measure too, or a great Stilton cheese, came running into the room in advance of the inn servants, and soon settled the question of his detachment from the poor young lady, by laying a brawny hand upon his chest, and sending him flying back against the nearest wall."},
        249: {"ko": "(\"이건 정말 남자임에 틀림없어!\"라고 로리 씨는 벽에 부딪힘과 동시에 숨 가쁘게 생각했다.)", "en": "(\"I really think this must be a man!\" was Mr. Lorry’s breathless reflection, simultaneously with his coming against the wall.)"},
        256: {"ko": "\"그리고 당신은 갈색 옷을 입고!\" 그녀가 로리 씨를 향해 분개하며 말했다.", "en": "\"And you in brown!\" she said, indignantly turning to Mr. Lorry;"},
        260: {"ko": "로리 씨는 대답하기 어려운 질문에 몹시 당황하여, 건장한 여자가 멍하니 서 있는 여관 하인들을 계속 그곳에 있으면 언급되지 않은 무언가를 '알게 해 주겠다'는 미스터리한 형벌로 위협해 쫓아낸 뒤, 쓰러진 아가씨의 고개를 자신의 어깨에 기대게 달래며 점차 회복시키는 동안 멀리서 훨씬 약해진 연민과 겸손함으로 지켜볼 수밖에 없었다.", "en": "Mr. Lorry was so exceedingly disconcerted by a question so hard to answer, that he could only look on, at a distance, with much feebler sympathy and humility, while the strong woman, having banished the inn servants under the mysterious penalty of “letting them know” something not mentioned if they stayed there, staring, recovered her charge by a regular series of gradations, and coaxed her to lay her drooping head upon her shoulder."},
        261: {"ko": "\"이제 괜찮아지길 바랍니다,\" 로리 씨가 말했다.", "en": "\"I hope she will do well now,\" said Mr. Lorry."},
        264: {"ko": "\"마네트 양과 함께 프랑스로 가시기를 바랍니다.\" 연민과 겸손함이 섞인 또 한 번의 약한 침묵 후에 로리 씨가 말했다.", "en": "\"I hope,\" said Mr. Lorry, after another pause of feeble sympathy and humility, \"that you accompany Miss Manette to France?\""},
        266: {"ko": "이것 역시 대답하기 어려운 질문이었기에, 자비스 로리 씨는 그것을 고려해 보기 위해 물러났다.", "en": "This being another question hard to answer, Mr. Jarvis Lorry withdrew to consider it."}
    },
    "book1_ch_05.json": {
        133: {"ko": "이렇게 와인 가게에서 나온 자비스 로리 씨와 마네트 양은, 드파르주가 방금 자신의 일행을 보냈던 출입구에서 그와 합류했다.", "en": "Mr. Jarvis Lorry and Miss Manette, emerging from the wine-shop thus, joined Monsieur Defarge in the doorway to which he had directed his own company just before."},
        141: {"ko": "천천히 시작하는 게 낫습니다.\" 계단을 오르기 시작할 때 드파르주가 엄격한 목소리로 로리 씨에게 말했다.", "en": "Better to begin slowly.” Thus, Monsieur Defarge, in a stern voice, to Mr. Lorry, as they began ascending the stairs."},
        154: {"ko": "그와 두 동반자가 점점 더 높이 올라갈수록 로리 씨의 마음은 점점 더 무거워졌다.", "en": "Mr. Lorry’s spirits grew heavier and heavier, as he and his two companions ascended higher and higher."},
        161: {"ko": "자신의 불안한 마음과 매 순간 더 커지는 젊은 동반자의 동요에 굴복하여, 자비스 로리 씨는 쉬기 위해 두 번이나 멈춰 섰다.", "en": "Yielding to his own disturbance of mind, and to his young companion’s agitation, which became greater every instant, Mr. Jarvis Lorry twice stopped to rest."},
        167: {"ko": "항상 조금 앞서 가며, 마치 젊은 아가씨에게 질문을 받을까 두려워하는 듯 로리 씨가 택한 쪽으로 걷던 와인 가게 주인은 여기서 몸을 돌려 어깨에 걸친 외투 주머니를 조심스럽게 더듬어 열쇠 하나를 꺼냈다.", "en": "The keeper of the wine-shop, always going a little in advance, and always going on the side which Mr. Lorry took, as though he dreaded to be asked any question by the young lady, turned himself about here, and, carefully feeling in the pockets of the coat he carried over his shoulder, took out a key."},
        168: {"ko": "\"문이 잠겨 있군요, 친구?\" 로리 씨가 놀라서 물었다.", "en": "\"The door is locked then, my friend?\" said Mr. Lorry, surprised."},
        176: {"ko": "\"이게 가능한 일입니까!\" 로리 씨가 외쳤다.", "en": "\"Is it possible!\" exclaimed Mr. Lorry."},
        182: {"ko": "그러나 그 무렵 그녀는 너무나 강한 감정에 휩싸여 떨고 있었고, 그녀의 얼굴은 너무나 깊은 불안과 무엇보다 끔찍한 두려움과 공포를 나타내고 있었기에 로리 씨는 안심시키는 말을 한두 마디 해야 할 의무감을 느꼈다.", "en": "But, by this time she trembled under such strong emotion, and her face expressed such deep anxiety, and, above all, such dread and terror, that Mr. Lorry felt it incumbent on him to speak a word or two of reassurance."},
        200: {"ko": "그 층에 다른 문이 없어 보였고, 그들만 남겨졌을 때 와인 가게 주인이 곧장 이 문으로 다가가자 로리 씨가 약간 화가 난 목소리로 그에게 속삭이며 물었다:", "en": "There appearing to be no other door on that floor, and the keeper of the wine-shop going straight to this one when they were left alone, Mr. Lorry asked him in a whisper, with a little anger:"},
        219: {"ko": "로리 씨는 딸의 허리를 팔로 단단히 감싸 안았다.", "en": "Mr. Lorry got his arm securely round the daughter’s waist, and held her;"}
    },
    "book1_ch_06.json": {
        38: {"ko": "\"오늘 그 구두 한 켤레를 다 끝내실 건가요?\" 드파르주가 로리 씨에게 앞으로 오라고 손짓하며 물었다.", "en": "\"Are you going to finish that pair of shoes to-day?\" asked Defarge, motioning to Mr. Lorry to come forward."},
        45: {"ko": "로리 씨는 딸을 문 곁에 둔 채 말없이 앞으로 나아갔다.", "en": "Mr. Lorry came silently forward, leaving the daughter by the door."},
        56: {"ko": "로리 씨는 그것을 손에 쥐었다.", "en": "Mr. Lorry took it in his hand."},
        76: {"ko": "\"원래 직업이 구두장이가 아니셨죠?\" 로리 씨가 그를 똑바로 바라보며 말했다.", "en": "\"You are not a shoemaker by trade?\" said Mr. Lorry, looking steadfastly at him."},
        88: {"ko": "그에게서 빼앗긴 구두를 받기 위해 손을 내밀며 로리 씨는 여전히 그의 얼굴을 똑바로 바라본 채 말했다:", "en": "As he held out his hand for the shoe that had been taken from him, Mr. Lorry said, still looking steadfastly in his face:"},
        92: {"ko": "로리 씨는 드파르주의 팔에 손을 얹었다.", "en": "Mr. Lorry laid his hand upon Defarge’s arm;"},
        97: {"ko": "오랜 세월 갇혀 지낸 죄수가 번갈아 가며 로리 씨와 드파르주를 빤히 바라보자, 이마 한가운데에 오랫동안 지워져 있던 적극적으로 의도하는 지성의 흔적들이 그에게 내려앉은 검은 안개를 뚫고 점차 모습을 드러냈다.", "en": "As the captive of many years sat looking fixedly, by turns, at Mr. Lorry and at Defarge, some long obliterated marks of an actively intent intelligence in the middle of the forehead, gradually forced themselves through the black mist that had fallen on him."},
        191: {"ko": "\"그를 방해하지 않고,\" 그녀가 반복해서 코를 푼 뒤 그들 위로 몸을 굽힌 로리 씨에게 손을 들어 올리며 말했다, \"우리가 즉시 파리를 떠날 수 있도록 모든 것이 준비된다면, 이 문에서부터 바로 그를 데려갈 수 있을 텐데요--\"", "en": "\"If, without disturbing him,\" she said, raising her hand to Mr. Lorry as he stooped over them, after repeated blowings of his nose, \"all could be arranged for our leaving Paris at once, so that, from the very door, he could be taken away--\""},
        193: {"ko": "그가 여행을 감당할 수 있을까요?\" 로리 씨가 물었다.", "en": "\"Is he fit for the journey?\" asked Mr. Lorry."},
        198: {"ko": "\"그게 바로 사업이죠,\" 로리 씨가 단번에 체계적인 태도를 되찾으며 말했다.", "en": "\"That’s business,\" said Mr. Lorry, resuming on the shortest notice his methodical manners;"},
        205: {"ko": "로리 씨와 드파르주 모두 이 방침에는 별로 마음이 내키지 않았고, 둘 중 한 명이 남는 쪽에 찬성했다.", "en": "Both Mr. Lorry and Defarge were rather disinclined to this course, and in favour of one of them remaining."},
        210: {"ko": "로리 씨와 드파르주는 여행을 위한 모든 준비를 마쳤고, 여행용 망토와 외투 외에도 빵과 고기, 와인, 그리고 뜨거운 커피를 챙겨 왔다.", "en": "Mr. Lorry and Monsieur Defarge had made all ready for the journey, and had brought with them, besides travelling cloaks and wrappers, bread and meat, wine, and hot coffee."},
        211: {"ko": "드파르주는 이 양식과 자신이 들고 있던 램프를 구두장인의 작업대에 올려놓았고(다락방에는 짚 매트리스 침대 외에는 아무것도 없었다), 그와 로리 씨는 갇힌 자를 깨워 그가 일어설 수 있도록 부축했다.", "en": "Monsieur Defarge put this provender, and the lamp he carried, on the shoemaker’s bench (there was nothing else in the garret but a pallet bed), and he and Mr. Lorry roused the captive, and assisted him to his feet."},
        221: {"ko": "드파르주가 램프를 들고 앞장섰고, 로리 씨가 작은 행렬의 맨 뒤를 따랐다.", "en": "Monsieur Defarge going first with the lamp, Mr. Lorry closing the little procession."},
        239: {"ko": "죄수는 마차에 올라탔고 그의 딸이 뒤를 따랐을 때, 그가 비참한 목소리로 구두 제작 도구와 미완성 구두를 요구하는 바람에 계단에서 로리 씨의 발이 멈춰 섰다.", "en": "The prisoner had got into a coach, and his daughter had followed him, when Mr. Lorry’s feet were arrested on the step by his asking, miserably, for his shoemaking tools and the unfinished shoes."},
        251: {"ko": "춥고 불안한 시간 내내 새벽이 올 때까지, 그들은 땅속에서 파낸 사람 맞은편에 앉아, 그가 영원히 잃어버린 미묘한 능력들이 무엇일지 또 무엇이 회복될 수 있을지 생각에 잠긴 자비스 로리 씨의 귓가에 다시 한번 예전의 그 질문을 속삭였다.", "en": "All through the cold and restless interval, until dawn, they once more whispered in the ears of Mr. Jarvis Lorry--sitting opposite the buried man who had been dug out, and wondering what subtle powers were for ever lost to him, and what were capable of restoration--the old inquiry:"}
    },
    "book2_ch_01.json": {
        43: {"ko": "배경은 화이트프라이어스 교수형 집행검 골목에 위치한 크런처 씨의 개인 숙소였다:", "en": "The scene was Mr. Cruncher’s private lodging in Hanging-sword-alley, Whitefriars:"},
        44: {"ko": "시간은 서기 1780년 바람 부는 3월의 어느 아침 7시 반이었다. (크런처 씨 자신은 서기(Anno Domini)를 항상 안나 도미노즈(Anna Dominoes)라고 불렀다:", "en": "the time, half-past seven of the clock on a windy March morning, Anno Domini seventeen hundred and eighty. (Mr. Cruncher himself always spoke of the year of our Lord as Anna Dominoes:"},
        46: {"ko": "크런처 씨의 방은 유리가 한 장 끼워진 옷장까지 하나로 친다 해도 단 두 개뿐이었으며, 주변 환경도 쾌적하지 못했다.", "en": "Mr. Cruncher’s apartments were not in a savoury neighbourhood, and were but two in number, even if a closet with a single pane of glass in it might be counted as one."},
        50: {"ko": "크런처 씨는 마치 집에 있는 할리퀸처럼 조각보 침대보 밑에서 잠을 자고 있었다.", "en": "Mr. Cruncher reposed under a patchwork counterpane, like a Harlequin at home."},
        55: {"ko": "\"뭐야!\" 침대 밖으로 장화를 찾으며 크런처 씨가 말했다. \"또 그 짓이야, 어?\"", "en": "\"What!\" said Mr. Cruncher, looking out of bed for a boot. \"You’re at it agin, are you?\""},
        57: {"ko": "그것은 진흙투성이의 장화였는데, 이는 은행 업무가 끝난 후 종종 깨끗한 장화를 신고 귀가하는 그가 다음 날 아침이면 같은 장화가 진흙으로 뒤덮여 있는 것을 발견한다는, 크런처 씨의 가정 경제와 관련된 기이한 상황을 잘 보여준다.", "en": "It was a very muddy boot, and may introduce the odd circumstance connected with Mr. Cruncher’s domestic economy, that, whereas he often came home after banking hours with clean boots, he often got up next morning to find the same boots covered with clay."},
        58: {"ko": "\"무슨 짓이냐고,\" 목표물을 빗맞힌 후 부르는 호칭을 바꾸며 크런처 씨가 말했다--\"무슨 수작을 부리는 거야, 홧거리(Aggerawayter)야?\"", "en": "\"What,\" said Mr. Cruncher, varying his apostrophe after missing his mark--\"what are you up to, Aggerawayter?\""},
        72: {"ko": "\"건방진 여자야, 네가 보기에 네 기도의 가치가 얼마나 될 것 같아?\" 크런처 씨가 무의식적으로 모순된 말을 내뱉으며 말했다.", "en": "\"And what do you suppose, you conceited female,\" said Mr. Cruncher, with unconscious inconsistency, \"that the worth of _your_ prayers may be?"},
        76: {"ko": "\"그 정도 가치밖에 안 돼,\" 크런처 씨가 반복했다. \"그렇다면 큰 가치는 없군.", "en": "\"Worth no more than that,\" repeated Mr. Cruncher. \"They ain’t worth much, then."},
        82: {"ko": "폭발할 것 같아!\" 그동안 줄곧 옷을 입고 있던 크런처 씨가 말했다, \"내가 신앙심이니 뭐니 하는 것들 때문에 지난주 내내 속아서 불쌍한 정직한 상인이 겪을 수 있는 최악의 불운을 맞이한 게 아니라면 말이야!\"", "en": "B-u-u-ust me!\" said Mr. Cruncher, who all this time had been putting on his clothes, \"if I ain’t, what with piety and one blowed thing and another, been choused this last week into as bad luck as ever a poor devil of a honest tradesman met with!"},
        90: {"ko": "넌 안 그래!\" 분노의 맷돌이 돌면서 또 다른 냉소적인 불꽃을 튀기며 크런처 씨는 장화 닦기와 사업을 위한 전반적인 준비에 착수했다.", "en": "Not you!\" and throwing off other sarcastic sparks from the whirling grindstone of his indignation, Mr. Cruncher betook himself to his boot-cleaning and his general preparation for business."},
        93: {"ko": "아침 식사를 할 때에도 크런처 씨의 화는 전혀 가라앉지 않았다.", "en": "Mr. Cruncher’s temper was not at all improved when he came to his breakfast."},
        94: {"ko": "그는 크런처 부인이 식전 기도를 하는 것에 대해 특별한 적대감을 보이며 분개했다.", "en": "He resented Mrs. Cruncher’s saying grace with particular animosity."},
        99: {"ko": "\"하지 마!\" 아내의 기도 덕분에 빵 덩어리가 마법처럼 사라질 것이라 예상하는 듯 주변을 두리번거리며 크런처 씨가 말했다. \"나는 축복받아 집에서 쫓겨날 생각 없어.\"", "en": "\"Don’t do it!\" said Mr. Crunches looking about, as if he rather expected to see the loaf disappear under the efficacy of his wife’s petitions. \"I ain’t a going to be blest out of house and home.\""}
    },
    "book2_ch_02.json": {
        5: {"ko": "그리고 로리 씨를 아시죠.\"", "en": "And you know Mr. Lorry.\""},
        6: {"ko": "\"베일리 재판소보다 로리 씨를 훨씬 잘 알죠, 나리.\"", "en": "\"I know Mr. Lorry, sir, much better than I know the Bailey.\""},
        9: {"ko": "증인들이 들어가는 문을 찾아 문지기에게 이 로리 씨 앞 쪽지를 보여주세요.", "en": "Find the door where the witnesses go in, and show the door-keeper this note for Mr. Lorry."},
        13: {"ko": "크런처 씨의 두 눈이 조금 더 가까워지며 서로에게 '이거 어떻게 생각해?'라고 묻는 듯했다.", "en": "Mr. Cruncher’s eyes seemed to get a little closer to one another, and to interchange the inquiry, \"What do you think of this?\""},
        16: {"ko": "문지기가 이 쪽지를 로리 씨에게 전달할 텐데, 그럼 시선을 끌 만한 몸짓을 해서", "en": "The door-keeper will pass the note to Mr. Lorry, and do you make any gesture that will attract Mr."},
        23: {"ko": "나이 든 직원이 천천히 쪽지를 접고 겉봉을 쓰는 동안 묵묵히 그를 지켜보다 압지 단계에 이르자 크런처 씨가 입을 열었다.", "en": "As the ancient clerk deliberately folded and superscribed the note, Mr. Cruncher, after surveying him in silence until he came to the blotting-paper stage, remarked:"},
        53: {"ko": "얼마간의 지체와 항의 끝에, 문이 아주 조금 마지못해 경첩을 돌리며 열렸고 제리 크런처 씨는 법정 안으로 몸을 밀어 넣을 수 있었다.", "en": "After some delay and demur, the door grudgingly turned on its hinges a very little way, and allowed Mr. Jerry Cruncher to squeeze himself into court."},
        64: {"ko": "여기서 크런처 씨의 시선은 로리 씨를 향해 다가가는 문지기에게 쏠렸다.", "en": "Mr. Cruncher’s attention was here diverted to the door-keeper, whom he saw making his way to Mr."},
        66: {"ko": "로리 씨는 가발을 쓴 신사들 사이에 있는 테이블에 앉아 있었다:", "en": "Mr. Lorry sat at a table, among the gentlemen in wigs:"},
        68: {"ko": "그리고 맞은편에는 호주머니에 손을 찔러 넣고 있는 가발을 쓴 또 다른 신사가 앉아 있었는데, 크런처 씨가 그 당시나 나중에 그를 보았을 때 그의 모든 주의는 오로지 법정의 천장에만 쏠려 있는 듯했다.", "en": "and nearly opposite another wigged gentleman with his hands in his pockets, whose whole attention, when Mr. Cruncher looked at him then or afterwards, seemed to be concentrated on the ceiling of the court."},
        69: {"ko": "몇 번 거칠게 기침을 하고 턱을 문지르며 손짓을 한 끝에, 제리는 자신을 찾으러 일어섰던 로리 씨의 주의를 끌었고, 로리 씨는 조용히 고개를 끄덕이곤 다시 자리에 앉았다.", "en": "After some gruff coughing and rubbing of his chin and signing with his hand, Jerry attracted the notice of Mr. Lorry, who had stood up to look for him, and who quietly nodded and sat down again."},
        100: {"ko": "그리고 법무장관이 발언할 준비를 하고 있다는 것을.", "en": "and that Mr. Attorney-General was making ready to speak."},
        133: {"ko": "시선을 그쪽으로 향했던 판사는 다시 시선을 거두고 의자에 기댄 채 자신의 손에 목숨이 달린 남자를 빤히 쳐다보았다. 한편 법무장관은 교수형 밧줄을 꼬고, 도끼를 갈고, 처형대에 못을 박기 위해 자리에서 일어섰다.", "en": "The Judge, whose eyes had gone in the general direction, recalled them, leaned back in his seat, and looked steadily at the man whose life was in his hand, as Mr. Attorney-General rose to spin the rope, grind the axe, and hammer the nails into the scaffold."}
    },
    "book2_ch_04.json": {
        2: {"ko": "법정의 어스름한 복도에서, 하루 종일 끓어오르던 인간 스튜의 마지막 찌꺼기가 걸러져 나갈 무렵, 마네트 박사와 그의 딸 루시 마네트, 피고 측 변호사 로리 씨와 변호인단이 모였다.", "en": "From the dimly-lighted passages of the court, the last sediment of the human stew that had been boiling there all day, was straining off, when Doctor Manette, Lucie Manette, his daughter, Mr. Lorry, the solicitor for the defence, and its counsel, Mr."},
        3: {"ko": "스트라이버가 막 죽음에서 풀려난 찰스 다네이 씨 주위에 모여서 무사한 것을 축하했다.", "en": "Stryver, stood gathered round Mr. Charles Darnay--just released--congratulating him on his escape from death."},
        13: {"ko": "다네이 씨는 그녀의 손에 열렬하고 감사한 마음을 담아 입을 맞추고 로리 씨를 향해 돌아서서", "en": "Mr. Darnay had kissed her hand fervently and gratefully, and had turned to Mr."},
        15: {"ko": "스트라이버 씨는 서른을 갓 넘긴 나이였지만 실제보다 이십 년은 더 늙어 보였고, 뚱뚱하고, 시끄럽고, 얼굴이 붉었으며, 퉁명스러웠고, 약간의 세심함조차 찾아볼 수 없었다. 그는 모임이나 대화 자리에 몸을 들이밀고 밀쳐내는(도덕적으로나 물리적으로나) 밀어붙이기 식의 방식을 가지고 있었는데, 이는 그의 인생에서 밀어붙이며 성공해 나갈 것을 잘 보여주었다.", "en": "Mr. Stryver, a man of little more than thirty, but looking twenty years older than he was, stout, loud, red, bluff, and free from any drawback of delicacy, had a pushing way of shouldering himself (morally and physically) into companies and conversations, that argued well for his shouldering his way up in life."},
        16: {"ko": "그는 여전히 가발과 법복을 걸친 채, 아무 죄 없는 로리 씨를 무리 밖으로 완전히 밀쳐낼 정도로 이전 의뢰인에게 당당하게 자세를 잡으며 말했다:", "en": "He still had his wig and gown on, and he said, squaring himself at his late client to that degree that he squeezed the innocent Mr. Lorry clean out of the group:"},
        17: {"ko": "\"당신을 명예롭게 구해내게 되어 기쁩니다, 다네이 씨.", "en": "\"I am glad to have brought you off with honour, Mr. Darnay."},
        21: {"ko": "\"당신을 위해 최선을 다했습니다, 다네이 씨;", "en": "\"I have done my best for you, Mr. Darnay;"},
        23: {"ko": "누군가는 \"훨씬 낫군요\"라고 말해야 하는 분위기였으므로 로리 씨가 그렇게 말했다;", "en": "It clearly being incumbent on some one to say, \"Much better,\" Mr. Lorry said it;"},
        25: {"ko": "\"그렇게 생각하십니까?\" 스트라이버 씨가 말했다. \"글쎄요! 당신은 하루 종일 그곳에 계셨으니 아실 겁니다.", "en": "\"You think so?\" said Mr. Stryver. \"Well! you have been present all day, and you ought to know."},
        27: {"ko": "\"그래서 말씀입니다만,\" 방금 전 무리에서 쫓겨났을 때처럼 다시 법을 잘 아는 변호사에 의해 무리 속으로 밀려 들어간 로리 씨가 말했다. \"그래서 마네트 박사님께 호소하여 이 모임을 해산하고 모두 각자의 집으로 돌아가게 해야겠습니다.", "en": "\"And as such,\" quoth Mr. Lorry, whom the counsel learned in the law had now shouldered back into the group, just as he had previously shouldered him out of it--\"as such I will appeal to Doctor Manette, to break up this conference and order us all to our homes."},
        28: {"ko": "루시 아가씨는 아파 보이고, 다네이 씨는 끔찍한 하루를 보냈고, 우리 모두 지쳐 있습니다.\"", "en": "Miss Lucie looks ill, Mr. Darnay has had a terrible day, we are worn out.\""},
        29: {"ko": "\"로리 씨, 당신 사정만 말하십시오.\" 스트라이버가 말했다;", "en": "\"Speak for yourself, Mr. Lorry,\" said Stryver;"},
        32: {"ko": "\"제 사정을 말하는 겁니다,\" 로리 씨가 대답했다. \"그리고 그분의 사정도요.", "en": "\"I speak for myself,\" answered Mr. Lorry, \"and for Mr."},
        43: {"ko": "아버지와 다네이 씨 사이에서 걷던 루시 마네트가 바깥 공기를 마시러 나갔다.", "en": "Walking between her father and Mr. Darnay, Lucie Manette passed into the open air."},
        45: {"ko": "스트라이버 씨는 복도에 그들을 남겨두고 옷을 갈아입는 방으로 밀쳐가며 돌아갔다.", "en": "Mr. Stryver had left them in the passages, to shoulder his way back to the robing-room."},
        47: {"ko": "그가 로리 씨와 다네이 씨가 있는 곳으로 다가왔다.", "en": "He now stepped up to where Mr. Lorry and Mr."},
        49: {"ko": "\"그래요, 로리 씨!", "en": "\"So, Mr. Lorry!"},
        50: {"ko": "이제 사업가들은 다네이 씨에게 말할 수 있겠지요?\"", "en": "Men of business may speak to Mr. Darnay now?\""},
        51: {"ko": "오늘 재판 과정에서 카턴 씨가 맡은 역할에 대해서는 아무도 아는 체하지 않았다;", "en": "Nobody had made any acknowledgment of Mr. Carton’s part in the day’s proceedings;"},
        54: {"ko": "\"선량한 충동과 비즈니스 측면 사이에서 분열될 때 비즈니스 마인드에 어떤 갈등이 일어나는지 안다면 재밌을 겁니다, 다네이 씨.\"", "en": "\"If you knew what a conflict goes on in the business mind, when the business mind is divided between good-natured impulse and business appearances, you would be amused, Mr. Darnay.\""},
        55: {"ko": "로리 씨는 얼굴을 붉히며 다소 격앙된 목소리로 말했다. \"선생, 그 이야기는 전에도 하셨소.", "en": "Mr. Lorry reddened, and said, warmly, \"You have mentioned that before, sir."},
        58: {"ko": "\"알죠, 알다마다요.\" 카턴 씨가 무심하게 대꾸했다. \"로리 씨, 너무 화내지 마십시오.", "en": "\"_I_ know, _I_ know,\" rejoined Mr. Carton, carelessly. \"Don’t be nettled, Mr."},
        62: {"ko": "\"그리고 참말로 선생님,\" 로리 씨는 그에게 개의치 않고 말을 이었다. \"선생이 이 문제와 무슨 상관이 있는지 정말 모르겠소.", "en": "\"And indeed, sir,\" pursued Mr. Lorry, not minding him, \"I really don’t know what you have to do with the matter."}
    }
}

for filename, data in translations.items():
    filepath = os.path.join("c:/git_repo/TKprof_book/books/two_cities/json/", filename)
    with open(filepath, "r", encoding="utf-8") as f:
        file_data = json.load(f)
    for block in file_data:
        block_id = block.get("id")
        if block_id in data:
            block["ko"] = data[block_id]["ko"]
            block["en"] = data[block_id]["en"]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(file_data, f, ensure_ascii=False, indent=2)

print("Real patch completed")
