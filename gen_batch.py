import json
import os

ko_dict = {
"As always, Death is the farmer working quietly. He has already chosen his wooden carts. Right now, these rough carts are sitting in simple barns near Paris. They are covered in country mud. Pigs sniff at them, and chickens use them to rest.": "항상 그렇듯, 죽음은 조용히 일하는 농부입니다. 그는 이미 나무 수레를 선택했습니다. 지금 당장, 이 거친 수레들은 파리 근처의 소박한 헛간에 놓여 있습니다. 그것들은 시골 진흙으로 덮여 있습니다. 돼지들이 냄새를 맡고, 닭들이 그것을 쉼터로 사용합니다.",
"But very soon, during the coming Revolution, these exact carts will carry prisoners to their deaths. No one heard the woodcutter or the farmer walking around. Suggesting they were even active was considered unpatriotic and against God.": "그러나 머지않아 다가올 혁명 동안 이 수레들이 바로 죄수들을 죽음으로 실어 나를 것입니다. 아무도 나무꾼이나 농부가 돌아다니는 소리를 듣지 못했습니다. 그들이 활동하고 있다는 것을 암시하는 것조차 비애국적이고 신에 어긋나는 것으로 여겨졌습니다.",
"In England, there was hardly enough law and order to brag about. Bold burglaries by armed men and highway robberies happened in the capital city itself every single night. Families were publicly warned not to leave town without storing their furniture in secure warehouses. The nighttime robber was often a respectable shopkeeper by day. Sometimes, a fellow merchant would recognize him during a robbery.": "영국에서는 자랑할 만한 법과 질서가 거의 없었습니다. 무장한 사람들의 대담한 빈집털이와 노상강도 사건이 수도에서 매일 밤 일어났습니다. 가족들은 안전한 창고에 가구를 보관하지 않고는 마을을 떠나지 말라는 공개적인 경고를 받았습니다. 밤의 강도는 종종 낮에는 존경받는 상인이었습니다. 때로는 강도 사건 중에 동료 상인이 그를 알아볼 수도 있었습니다.",
"Bold burglaries by armed men and highway robberies happened in the capital city itself every single night. Families were publicly warned not to leave town without first moving their furniture to a storage warehouse to keep it safe. The highway robber in the dark might be a respectable city merchant during the day. In one case, a merchant stopped a fellow merchant while playing the role of a robber called 'the Captain.' When he was recognized and called out, he simply shot his fellow merchant in the head and rode away! The mail coach was ambushed by seven robbers; the guard managed to shoot three of them dead, but then got shot dead himself by the other four because he 'ran out of ammunition.' After that, the mail was easily robbed in peace. Even the powerful Lord Mayor of London was forced to hand over his valuables on Turnham Green by a single highwayman, who robbed the famous leader right in front of all his guards. Prisoners in London jails fought literal battles with their guards, and the legal authorities responded by firing shotguns loaded with heavy bullets into the crowds. Thieves even snipped diamond crosses right off the necks of noble lords at fancy royal parties. Musketeers went into St.": "무장한 자들의 대담한 빈집털이와 노상강도가 매일 밤 수도 자체에서 일어났습니다. 가족들은 가구를 안전하게 보관하기 위해 창고로 옮기지 않고는 도시를 떠나지 말라고 공개적으로 경고받았습니다. 어둠 속의 노상강도는 낮에는 존경받는 도시 상인일 수도 있었습니다. 한 번은 상인이 '대위'라는 강도 역할을 하다가 동료 상인을 멈춰 세운 적도 있었습니다. 자신이 누구인지 발각되어 불리자, 그는 그저 동료 상인의 머리에 총을 쏘고 도망쳤습니다! 우편 마차는 7명의 강도에게 습격당했습니다. 호위병은 세 명을 쏴 죽이는 데 성공했지만, 탄약이 떨어졌기 때문에 나머지 4명에게 쏴 죽임을 당했습니다. 그 후 우편물은 아무런 저항 없이 쉽게 털렸습니다. 런던의 권력 있는 시장조차 턴햄 그린에서 단 한 명의 노상강도에게 귀중품을 넘겨주어야만 했고, 강도는 모든 경비원이 보는 앞에서 그 유명한 지도자를 털었습니다. 런던 감옥의 죄수들은 간수들과 말 그대로 전투를 벌였고, 법적 당국은 무거운 총알이 장전된 산탄총을 군중에게 쏘아 대응했습니다. 도둑들은 심지어 화려한 왕실 파티에서 귀족 영주들의 목에서 다이아몬드 십자가를 끊어 가기도 했습니다. 총사들은 세인트에 들어갔습니다.",
"A single highwayman stopped him on Turnham Green. The robber forced the famous man to hand over all his valuables right in front of his own servants. Prisoners in London jails fought battles with their guards, and the authorities fired heavy guns loaded with bullets right into the crowd. Thieves cut diamond crosses from the necks of noble lords at royal parties. Soldiers marched into St.": "단 한 명의 노상강도가 턴햄 그린에서 그를 멈춰 세웠습니다. 강도는 자신의 하인들 바로 앞에서 유명한 남자에게 모든 귀중품을 넘기도록 강요했습니다. 런던 감옥의 죄수들은 간수들과 전투를 벌였고 당국은 군중에게 총알이 장전된 무거운 총을 쏘았습니다. 도둑들은 왕실 파티에서 귀족 영주들의 목에서 다이아몬드 십자가를 잘라냈습니다. 군인들은 세인트에 행진했습니다.",
"Giles's to search for illegal goods, the angry crowd shot at the soldiers, the soldiers shot back at the crowd, and nobody thought any of this was out of the ordinary. In the middle of all this chaos, the executioner was always busy but completely useless. Sometimes he hanged long rows of criminals. Other times he hanged a burglar on Saturday who had just been caught on Tuesday. He spent his days branding dozens of people at Newgate Prison or burning rebellious pamphlets at Westminster Hall. Today he would take the life of a terrible murderer, and tomorrow he would hang a poor thief who had stolen only sixpence from a farm boy.": "가일스는 불법 물품을 수색하기 위해 갔지만, 성난 군중은 군인들에게 총을 쏘았고 군인들은 군중에게 응사했으며, 아무도 이 중 어떤 것도 이상하다고 생각하지 않았습니다. 이 모든 혼란의 한가운데서 사형집행인은 항상 바빴지만 완전히 쓸모가 없었습니다. 때때로 그는 범죄자들을 길게 줄 세워 교수형에 처했습니다. 다른 때에는 화요일에 막 잡힌 강도를 토요일에 교수형에 처했습니다. 그는 뉴게이트 감옥에서 수십 명의 사람들에게 낙인을 찍거나 웨스트민스터 홀에서 반항적인 전단지를 태우며 하루를 보냈습니다. 오늘 그는 끔찍한 살인자의 목숨을 앗아갈 것이고, 내일은 농장 소년에게서 단지 육 펜스를 훔친 불쌍한 도둑을 교수형에 처할 것입니다.",
"All these things, and a thousand more like them, happened during and around the year 1775.": "이 모든 일들, 그리고 이와 같은 수천 가지 일들이 1775년과 그 무렵에 일어났습니다.",
"All these events happened while the woodcutter and the farmer worked unnoticed in the background. Meanwhile, the two kings with large jaws and their two queens made a great fuss. They believed they ruled with absolute authority.": "이 모든 일들은 나무꾼과 농부가 눈에 띄지 않게 뒤에서 일하는 동안 일어났습니다. 한편 턱이 큰 두 왕과 그들의 두 여왕은 큰 소란을 피웠습니다. 그들은 자신들이 절대적인 권력으로 통치한다고 믿었습니다.",
"In this way, the year 1775 led these powerful rulers, along with millions of ordinary people, including the characters in this story, along the paths that lay ahead of them.": "이런 식으로 1775년은 이 강력한 통치자들과 이 이야기의 등장인물들을 포함한 수백만 명의 평범한 사람들을 그들 앞에 놓인 길을 따라 이끌었습니다.",
"The Mail On a Friday night late in November, the Dover road lay before the first character of our story. For him, the road stretched out beyond the Dover mail coach as it slowly struggled up Shooter's Hill.": "우편 11월 하순의 금요일 밤, 우리 이야기의 첫 번째 등장인물 앞에 도버 길이 놓여 있었습니다. 그에게 그 길은 도버 우편 마차가 슈터스 힐을 힘들게 올라가는 동안 그 너머로 뻗어 있었습니다.",
"He walked up the hill through the mud next to the coach, just like the other passengers. They weren't walking because they enjoyed it. They were walking because everything was too heavy. The hill was steep.": "그는 다른 승객들과 마찬가지로 마차 옆 진흙 속을 걸어 언덕을 올라갔습니다. 그들은 걷는 것을 즐겨서 걷는 것이 아니었습니다. 그들은 모든 것이 너무 무거웠기 때문에 걷고 있었습니다. 언덕은 가팔랐습니다.",
"He walked uphill in the mud beside the mail coach, just like the rest of the passengers. They didn't do this because they had any desire for exercise in these conditions, but because the hill, the harness, the mud, and the coach itself were all so heavy. The horses had already stopped three times, and had even once dragged the coach sideways across the road, rebelliously intending to pull it right back to Blackheath.": "그는 다른 승객들처럼 우편 마차 옆에서 진흙 속에서 언덕을 걸어 올라갔습니다. 그들은 이런 환경에서 운동하고 싶은 욕구가 있어서가 아니라 언덕, 마구, 진흙, 그리고 마차 자체가 모두 너무 무거웠기 때문에 그렇게 했습니다. 말들은 이미 세 번이나 멈춰 섰고, 한 번은 마차를 길을 가로질러 옆으로 끌고 가 반항적으로 블랙히스까지 곧장 되돌아갈 작정이었습니다.",
"The reins, whip, coachman, and guard all worked together to say: no. That rebellion was not allowed. The horses reluctantly gave in and returned to their duty.": "고삐, 채찍, 마부, 호위병이 모두 함께 반대했습니다. 안 돼. 그 반란은 허용되지 않았습니다. 말들은 마지못해 굴복하고 임무로 돌아갔습니다.",
"With drooping heads and shaking tails, they struggled through the thick mud, floundering and stumbling occasionally, as if their main joints were about to fall apart.": "머리를 숙이고 꼬리를 흔들며, 그들은 짙은 진흙탕을 뚫고 몸부림쳤고, 마치 주요 관절이 떨어져 나갈 것처럼 가끔 허우적거리고 비틀거렸습니다.",
"Every time the driver stopped them to rest, with a cautious \"Woah there! Easy now!\", the left lead horse violently shook its head and harness, like an especially stubborn horse, protesting that the coach couldn't possibly get up the hill.": "마부가 조심스럽게 '워워! 조심해!'라고 말하며 쉴 때마다 왼쪽 앞말은 유난히 고집 센 말처럼 마차가 언덕을 올라갈 수 없다고 항의하듯 고개와 마구를 격렬하게 흔들었습니다.",
"Whenever the leader made that rattling noise, the passenger flinched, as a nervous traveler might, and felt uneasy.": "선두가 그런 덜걱거리는 소리를 낼 때마다 승객은 긴장한 여행자처럼 움찔했고 불안해했습니다.",
"A steaming mist filled all the low-lying areas, and it had sadly drifted up the hill like an evil spirit, seeking rest but finding none.": "김이 모는 안개가 저지대를 가득 채웠고, 마치 안식을 찾지만 찾지 못하는 악령처럼 슬프게도 언덕 위로 떠올랐습니다.",
"It was a damp and intensely cold mist, slowly moving through the air in visible ripples that followed and spread over one another like waves on an unhealthy sea. The mist was so thick that the coach-lamps could only light up a few yards of road ahead.": "그것은 축축하고 몹시 차가운 안개였고, 건강하지 못한 바다의 파도처럼 눈에 보이는 물결로 공기 중을 천천히 이동하며 서로 따라가며 퍼졌습니다. 안개가 너무 짙어서 마차 램프는 앞의 몇 야드 길만 밝힐 수 있었습니다.",
"Everything else was swallowed up in swirling white fog. The hard-working horses breathed out great clouds of steam. That steam drifted into the mist and became part of it, as if the horses themselves had made the fog.": "그 밖의 모든 것은 소용돌이치는 하얀 안개 속에 삼켜졌습니다. 힘겹게 일하는 말들은 거대한 증기 구름을 내뿜었습니다. 그 증기는 안개 속으로 떠내려가 그 일부가 되었고, 마치 말들 자체가 안개를 만든 것 같았습니다.",
"Two other passengers were trudging up the hill next to the mail coach.": "다른 두 명의 승객은 우편 마차 옆 언덕을 터벅터벅 걸어 올라가고 있었습니다.",
"All three were bundled up to their cheekbones and over their ears, and wore sturdy riding boots.": "세 사람 모두 광대뼈 위와 귀를 덮을 정도로 꽁꽁 싸매고 있었고 튼튼한 승마화를 신고 있었습니다.",
"None of the three passengers could tell, just from looking, what the other two looked like. They were all bundled up completely. Each man was as much of a mystery to his companions as he was to a total stranger.": "세 명의 승객 중 어느 누구도 외모만으로는 나머지 두 명이 어떻게 생겼는지 알 수 없었습니다. 그들은 모두 완전히 꽁꽁 싸매고 있었습니다. 각 사람은 완전히 낯선 사람만큼이나 동행자들에게 미스터리였습니다.",
"In those days, travelers did not trust strangers quickly. Anyone on the road could be a robber.": "그 시절에는 여행자들이 낯선 사람들을 쉽게 믿지 않았습니다. 도로 위의 누구든 강도일 수 있었습니다.",
"Even worse, every inn or pub could have a spy on the bandit's payroll. That spy could be the owner, a servant, or the lowliest stable hand.": "더 나쁜 것은 모든 여관이나 펍에 도적에게 고용된 스파이가 있을 수 있다는 것입니다. 그 스파이는 주인, 하인 또는 가장 지위가 낮은 마구간 일꾼일 수도 있었습니다.",
"The guard of the Dover mail knew all of this. That Friday night in November 1775, he stood on his platform at the back of the coach. He stamped his feet to stay warm. He kept one hand on the weapons chest. Inside it: a loaded shotgun on top, six or eight loaded horse pistols below, and a cutlass at the very bottom.": "도버 우편의 호위병은 이 모든 것을 알고 있었습니다. 1775년 11월의 어느 금요일 밤, 그는 마차 뒤쪽 플랫폼에 서 있었습니다. 그는 따뜻하게 지내기 위해 발을 구르고 있었습니다. 그는 무기 상자에 한 손을 얹고 있었습니다. 그 안에는 맨 위에 장전된 산탄총이, 아래에는 6개 또는 8개의 장전된 기병 권총이, 그리고 맨 밑바닥에는 짧고 넓은 칼이 있었습니다.",
"The Dover mail was running normally. The guard suspected the passengers. The passengers suspected each other and the guard. They all suspected everyone else. The only person who wasn't suspicious was the coachman. He was simply certain about one thing: the horses were not fit for this journey. He could have sworn that on the Holy Bible.": "도버 우편물은 정상적으로 운행되고 있었습니다. 호위병은 승객들을 의심했습니다. 승객들은 서로와 호위병을 의심했습니다. 그들은 모두 다른 모든 사람을 의심했습니다. 유일하게 의심하지 않은 사람은 마부였습니다. 그는 단 한 가지에 대해 확신하고 있었습니다. 말들이 이 여행에 적합하지 않다는 것이었습니다. 그는 성경에 대고 그것을 맹세할 수 있었습니다.",
"\"Woah there!\" said the coachman. \"Alright, then!": "마부가 말했습니다. \"워워! 그럼 좋아!",
"Just one more pull and youll be at the top, and damn you, because Ive had enough trouble getting you this far!, Joe!\"": "한 번만 더 당기면 정상에 도착할 거야, 빌어먹을, 여기까지 오는 데 충분히 고생했으니까!, 조!\"",
"\"Hello!\" the guard replied.": "호위병이 대답했습니다. \"안녕하세요!\"",
"\"What time do you make it, Joe?\"": "\"지금 몇 시나 됐지, 조?\"",
"\"A good ten past eleven.\"": "\"11시 10분쯤이요.\"",
"\"Damn it!\" the annoyed coachman burst out, \"and we're not even at the top of Shooter's yet!": "짜증이 난 마부가 소리쳤습니다. \"빌어먹을! 아직 슈터스 언덕 정상에도 못 왔잖아!",
"Tsk!": "쯧!",
"Come on!": "이리 와!",
"Get moving!\"": "어서 움직여!\"",
"The lead horse, which had been trying to slow down, was sharply told by the whip to keep going, and it made a determined scramble forward. The three other horses followed suit.": "속도를 늦추려던 선두 말은 채찍을 맞아 계속 가라는 날카로운 말을 들었고, 단호하게 앞으로 돌진했습니다. 다른 세 마리의 말도 그 뒤를 따랐습니다.",
"Once again, the Dover mail coach struggled onward, with its passengers' boots squelching along beside it.": "다시 한번 도버 우편 마차는 승객들의 부츠가 그 옆에서 웅덩이를 밟으며 앞으로 나아갔습니다.",
"They had stopped when the coach did, and they stayed right next to it.": "그들은 마차가 멈췄을 때 멈췄고 마차 바로 옆에 머물렀습니다.",
"If any of the three had been bold enough to suggest to another that they walk a little ahead into the mist and darkness, he would have been practically asking to be shot instantly as a highwayman.": "세 사람 중 누구라도 다른 사람에게 안개와 어둠 속으로 조금 앞서 걷자고 제안할 만큼 대담했다면, 그는 실질적으로 노상강도로 즉시 총에 맞아 죽기를 요구하는 것이나 다름없었을 것입니다.",
"That last burst of effort carried the mail coach to the top of the hill.": "그 마지막 노력 덕분에 우편 마차는 언덕 정상에 도달했습니다.",
"The horses stopped to catch their breath, and the guard got down to put the skid-shoe on the wheel for the descent, and open the coach door to let the passengers in.": "말들은 숨을 돌리기 위해 멈췄고, 호위병은 내리막길을 위해 바퀴에 스키드 슈를 씌우고 승객들이 탈 수 있도록 마차 문을 열기 위해 내렸습니다.",
"\"Psst!": "\"쉿!",
"Joe!\" the coachman called out in a warning voice, looking down from his seat.": "조!\" 마부가 자기 자리에서 내려다보며 경고하는 목소리로 불렀습니다.",
"\"What do you say, Tom?\"": "\"무슨 말인가, 톰?\"",
"They both listened.": "둘 다 귀를 기울였습니다.",
"\"I hear a horse cantering up, Joe.\"": "\"말이 달리는 소리가 들려, 조.\"",
"\"I hear a horse at a gallop, Tom,\" the guard replied, letting go of the door and nimbly climbing back to his spot. \"Gentlemen!": "호위병이 문에서 손을 떼고 재빠르게 자기 자리로 올라가며 대답했습니다. \"말이 전속력으로 달리는 소리가 들리네, 톰.\" \"신사 여러분!",
"In the King's name, everyone!\"": "모두 국왕의 이름으로!\"",
"After this urgent warning, he cocked his shotgun and got ready to fight.": "이 긴급한 경고 후 그는 산탄총을 장전하고 싸울 준비를 했습니다.",
"The passenger this story is about was on the coach step, getting inside; the two other passengers were right behind him, about to follow.": "이 이야기의 주인공인 승객은 마차 계단에 서서 안으로 들어가고 있었고, 다른 두 승객은 바로 뒤에 서서 따라가려던 참이었습니다.",
"He stayed on the step, half in and half out of the coach; they stayed on the road below him.": "그는 몸을 절반쯤 마차 안에 넣고 절반쯤 마차 밖에 내놓은 채 계단에 머물렀고, 그들은 그의 아래 길가에 머물렀습니다.",
"They all looked from the coachman to the guard, then from the guard to the coachman, and listened.": "모두가 마부에서 호위병을, 그리고 호위병에서 마부를 번갈아 보며 귀를 기울였습니다.",
"The coachman looked back, the guard looked back, and even the lead horse pricked up its ears and listened, without arguing.": "마부가 뒤돌아보고, 호위병이 뒤돌아보았으며, 선두 말조차도 군말 없이 귀를 쫑긋 세우고 귀를 기울였습니다.",
"The quiet that came after the coach stopped rumbling and working hard, combined with the silent night, made it incredibly still.": "마차가 덜컹거리며 열심히 달리던 것이 멈춘 후 찾아온 고요함은 적막한 밤과 어우러져 믿을 수 없을 정도로 고요하게 만들었습니다.",
"The horses' panting made the coach shake a little, as if it were nervous.": "말들의 헐떡임에 마차는 마치 긴장한 것처럼 약간 흔들렸습니다.",
"The passengers' hearts were probably pounding loud enough to be heard. Everyone was out of breath. Everyone was holding their breath. Everyone's heart was racing.": "승객들의 심장은 아마 들릴 정도로 크게 뛰었을 것입니다. 모두가 숨이 찼습니다. 모두가 숨을 죽이고 있었습니다. 모두의 심장이 뛰고 있었습니다.",
"The sound of a horse at a gallop came charging up the hill.": "말이 전속력으로 달리는 소리가 언덕 위로 돌진해 왔습니다.",
"\"Hey!\" the guard shouted as loud as he could. \"Hey there!": "호위병이 목청껏 소리쳤습니다. \"어이!\" \"거기 누구야!",
"Stop!": "멈춰!",
"I'll shoot!\"": "쏘겠다!\"",
"The horse suddenly stopped. There was a lot of splashing and struggling in the darkness. Then a man's voice called out from the mist. \"Is that the Dover mail?\"": "말이 갑자기 멈췄습니다. 어둠 속에서 많은 물보라가 일고 몸부림치는 소리가 들렸습니다. 그리고 안개 속에서 한 남자의 목소리가 들렸습니다. \"그게 도버 우편 마차요?\"",
"\"Don't you worry about what it is!\" the guard shot back. \"Who are you?\"": "호위병이 쏘아붙였습니다. \"그게 뭔지 걱정하지 마!\" \"당신 누구야?\"",
"\"Is that the Dover mail?\"": "\"그게 도버 우편 마차요?\"",
"\"Why do you want to know?\"": "\"왜 알고 싶은 거요?\"",
"\"I want a passenger, if it is.\"": "\"만약 그렇다면 승객 한 명을 찾고 싶소.\"",
"\"What passenger?\"": "\"어떤 승객?\"",
"\"Mr.": "\"미스터.",
"Jarvis Lorry.\"": "자비스 로리.\"",
"The passenger immediately showed that it was his name.": "그 승객은 즉시 그것이 자신의 이름임을 나타냈습니다.",
"The guard, the coachman, and the two other passengers looked at him suspiciously.": "호위병, 마부, 그리고 다른 두 명의 승객이 그를 의심스러운 듯이 쳐다보았습니다.",
"The guard called to the voice in the mist, \"Stay right there, because if I make a mistake, you'll never live to fix it.": "호위병이 안개 속의 목소리를 향해 외쳤습니다. \"거기 그대로 있어, 만약 내가 실수라도 한다면, 넌 결코 살아서 그걸 바로잡지 못할 테니까.",
"Mr. Lorry, answer clearly.\"": "미스터 로리, 똑바로 대답하시오.\"",
"\"What's going on?\" the passenger asked then, with a slightly shaky voice. \"Who wants me?": "그러자 승객은 약간 떨리는 목소리로 물었습니다. \"무슨 일입니까?\" \"누가 저를 찾습니까?",
"Is it Jerry?\"": "제리인가요?\"",
"The guard grumbled to himself, \"I dont like Jerrys voice, if it is Jerry. His voice is too hoarse for my liking, that Jerry.\"": "호위병이 혼잣말로 투덜거렸습니다. \"만약 저게 제리라면, 제리의 목소리는 마음에 안 들어. 목소리가 내 취향에는 너무 쉬었군, 그 제리라는 사람.\"",
"\"Yes, Mr.": "\"네, 미스터.",
"Lorry.\"": "로리.\"",
"\"What is the matter?\"": "\"무슨 일인가요?\"",
"\"A message sent after you from over there.": "\"저쪽에서 선생님께 보낸 메시지입니다.",
"T. and Co.\"": "T. and Co.\"",
"\"I know this messenger, guard,\" said Mr. Lorry. He stepped down onto the road.": "미스터 로리가 말했습니다. \"호위병, 난 이 심부름꾼을 압니다.\" 그는 도로로 내려섰습니다.",
"The other two passengers helped him, less out of politeness and more out of eagerness to be rid of him. The moment he was out, they scrambled back inside, slammed the door, and rolled up the window. \"He can come closer,\" Mr. Lorry called up. \"There's nothing wrong.\"": "다른 두 승객은 예의가 아니라 그를 빨리 쫓아내려는 마음에 그를 도와주었습니다. 그가 나가자마자 그들은 재빨리 안으로 기어들어가 문을 쾅 닫고 창문을 올렸습니다. 미스터 로리가 위로 외쳤습니다. \"그가 더 가까이 와도 됩니다.\" \"아무 문제 없습니다.\"",
"\"I hope not, but I cant be so sure of that,\" said the guard, muttering to himself. \"Hey you!\"": "호위병이 혼잣말로 중얼거렸습니다. \"그러길 바라지만 그렇게 확신할 순 없지.\" \"어이 너!\"",
"\"Well!": "\"글쎄요!",
"And hello to you too!\" said Jerry, more hoarsely than before.": "그리고 당신에게도 인사하죠!\" 제리가 전보다 더 쉰 목소리로 말했습니다.",
"\"Come on at a walking pace! Do you hear me?": "\"걸어서 와라! 내 말 들려?",
"And if youve got holsters on that saddle of yours, dont let me see your hand go anywhere near them.": "그리고 네 그 안장에 권총집이 있다면, 네 손이 그 근처에 가는 걸 내 눈에 띄게 하지 마.",
"Because Im very quick to make a mistake, and when I do, its with a bullet.": "왜냐하면 난 아주 빨리 실수를 저지르고, 그럴 땐 총알로 하거든.",
"So now lets get a good look at you.\"": "자, 이제 네 얼굴 좀 제대로 보자.\""
}

with open('c:/git_repo/TKprof_book/scratch_en.json', 'r', encoding='utf-8') as f:
    en_data = json.load(f)

output = []
for item in en_data:
    en_text = item['target_en']
    ko_text = ko_dict.get(en_text, en_text) # default to en_text if missing, but should be there
    output.append({
        'file': item['file'],
        'id': item['id'],
        'ko': ko_text
    })

os.makedirs('c:/git_repo/TKprof_book/translated_batches', exist_ok=True)
with open('c:/git_repo/TKprof_book/translated_batches/batch_0_99.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Saved output to batch_0_99.json")
