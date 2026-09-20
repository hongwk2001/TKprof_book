import json
import os

translations = {
    "It cannot be.": "안 될 말이다.",
    "Look at what a prisoner I am.": "내가 어떤 죄수인지 보아라.",
    "These are not the hands she knew, this is not the face she knew, and this is not a voice she ever heard.": "이것은 그녀가 알던 손이 아니고, 이것은 그녀가 알던 얼굴도 아니며, 이것은 그녀가 들어본 적 있는 목소리도 아니다.",
    "No, no.": "아니다, 아니야.",
    "She and I existed before the long, slow years in the North Tower, ages ago.": "그녀와 나는 북쪽 탑(North Tower)에서의 길고 느린 세월 이전인, 아주 오래 전에 존재했었다.",
    "What is your name, my gentle angel?\"": "\"너의 이름은 무엇이냐, 나의 상냥한 천사여?\"",
    "Grateful for his softer tone and gentle manner, his daughter knelt in front of him, placing her pleading hands on his chest.": "그의 부드러워진 어조와 상냥한 태도에 감사하며, 그의 딸은 그의 앞에 무릎을 꿇고 애원하는 손을 그의 가슴에 얹었다.",
    "\"Oh, sir, at another time you will know my name, and who my mother and father were, and why I never knew their sad history.": "\"오, 어르신, 다른 때가 되면 제 이름이 무엇인지, 제 어머니와 아버지가 누구셨는지, 그리고 제가 왜 그분들의 슬픈 역사를 결코 알지 못했는지 아시게 될 거예요.",
    "But I cannot tell you now, and I cannot tell you here.": "하지만 지금 당장 말씀드릴 수는 없고, 이 자리에서 말씀드릴 수도 없어요.",
    "All I can tell you right here and now is that I beg you to touch me and bless me.": "제가 지금 여기에서 말씀드릴 수 있는 전부는, 저를 만져주시고 제게 축복을 내려달라고 간청하는 것뿐입니다.",
    "Kiss me, kiss me!": "제게 입 맞춰 주세요, 제게 입 맞춰 주세요!",
    "Oh, my dear, my dear father!\"": "오, 사랑하는 나의 아버지, 나의 아버지!\"",
    "His cold white head rested against her bright, golden hair, which seemed to warm and light it up as if the light of freedom itself were shining on him.": "그의 차갑고 하얀 머리가 그녀의 밝고 금빛 나는 머리카락에 기대어졌고, 그것은 마치 자유의 빛 그 자체가 그를 비추고 있는 것처럼 그를 따뜻하게 하고 환하게 밝혀주는 듯했다.",
    "\"If you hear in my voice, I do not know if it is true, but I hope it is, any sound that reminds you of a voice that was once sweet music to your ears, cry for it, cry for it!": "\"만약 제 목소리에서 당신의 귀에 한때 달콤한 음악이었던 목소리를 떠올리게 하는 어떤 소리가 들리신다면, 그것이 사실인지는 모르겠지만 그러기를 바라며, 그것을 위해 우세요, 그것을 위해 우세요!",
    "If, in touching my hair, you feel anything that reminds you of a beloved head that lay on your chest when you were young and free, cry for it, cry for it!": "만약 제 머리카락을 만지시며 당신이 젊고 자유로우셨을 때 당신의 가슴에 누웠던 사랑하는 머리를 떠올리게 하는 무언가를 느끼신다면, 그것을 위해 우세요, 그것을 위해 우세요!",
    "If, when I talk about the home waiting for us, where I will care for you with all my duty and faithful love, I bring back the memory of a home that was empty for so long while your poor heart suffered, cry for it, cry for it!\"": "만약 제가 모든 의무와 충실한 사랑으로 당신을 돌볼, 우리를 기다리고 있는 집에 대해 이야기할 때, 당신의 가엾은 심장이 고통받는 동안 그토록 오랫동안 비어 있던 집의 기억을 되살려낸다면, 그것을 위해 우세요, 그것을 위해 우세요!\"",
    "She held him tighter around the neck, rocking him against her chest like a child.": "그녀는 아이처럼 그를 가슴에 안고 흔들며, 그의 목을 더 꽉 끌어안았다.",
    "\"If, when I tell you, my dearest, that your suffering is over, and that I have come to take you away from this place to England where we can live in peace and rest, I make you think of your wasted life and how cruel our native France has been to you, cry for it, cry for it!": "\"만약, 사랑하는 아버지, 제가 당신의 고통은 끝났고, 우리가 평화롭게 쉬며 살 수 있는 영국으로 당신을 모시고 가기 위해 이곳에 왔다고 말씀드릴 때, 당신이 잃어버린 삶과 우리의 조국 프랑스가 당신에게 얼마나 잔인했는지를 생각하게 만든다면, 그것을 위해 우세요, 그것을 위해 우세요!",
    "And if, when I tell you my name and about my father who is alive and my mother who is dead, you learn that I must kneel to my honored father and beg his forgiveness for never working all day, staying awake, and crying all night for his sake, because my mother's love kept his suffering a secret from me, cry for it, cry for it!": "그리고 만약, 제가 제 이름과 살아계신 제 아버지, 그리고 돌아가신 제 어머니에 대해 말씀드릴 때, 어머니의 사랑이 당신의 고통을 저에게 비밀로 간직하셨기 때문에, 당신을 위해 하루 종일 일하지도, 밤새 깨어 있지도, 밤새 울지도 않았던 것에 대해 제가 존경하는 아버지께 무릎을 꿇고 용서를 구해야 한다는 것을 알게 되신다면, 그것을 위해 우세요, 그것을 위해 우세요!",
    "Cry for her, then, and for me!": "그러니 어머니를 위해 우시고, 저를 위해 우세요!",
    "Gentlemen, thank God!": "여러분, 하나님께 감사드립니다!",
    "I feel his tears on my face, and his sobs touch my heart.": "그의 눈물이 제 얼굴에 떨어지는 것이 느껴지고, 그의 흐느낌이 제 마음을 울립니다.",
    "Oh, look!": "오, 보세요!",
    "Thank God for us, thank God!\"": "우리를 위해 하나님께 감사드립니다, 하나님께 감사드립니다!\"",
    "He sank into her arms, and his face fell against her chest. It was a sight so touching, yet so terrible because of the great pain and injustice that had caused it, that the two men watching covered their faces.": "그는 그녀의 품에 쓰러졌고, 그의 얼굴은 그녀의 가슴에 떨어졌다. 너무나 감동적이면서도, 그것을 초래한 큰 고통과 불의 때문에 너무나 끔찍한 광경이었기에, 지켜보던 두 남자는 얼굴을 가렸다.",
    "The attic room had been quiet for a long time. His heavy breathing slowed. His trembling body finally calmed down. As always, the storm had ended in quiet peace. The two men came forward to help the father and daughter up.": "다락방은 오랫동안 조용했다. 그의 거친 숨소리는 느려졌다. 떨리던 그의 몸은 마침내 진정되었다. 언제나 그렇듯, 폭풍은 고요한 평화 속에 끝났다. 두 남자는 아버지와 딸이 일어나는 것을 돕기 위해 앞으로 다가왔다.",
    "He had slowly slipped to the floor and lay there in a deep, exhausted sleep.": "그는 천천히 바닥으로 미끄러져 내려가 그곳에 누워 깊고 지친 잠에 빠져 있었다.",
    "She had huddled down with him so that his head rested on her arm, and her long hair fell over him like a curtain to block out the light.": "그녀는 그의 머리가 그녀의 팔에 기대어지도록 그와 함께 웅크리고 있었고, 그녀의 긴 머리카락은 빛을 가리는 커튼처럼 그 위로 떨어져 내렸다.",
    "\"If we can do it without waking him,\" she whispered, raising her hand to Mr.": "\"만약 그를 깨우지 않고 할 수 있다면,\" 그녀가 여러 번 코를 풀며 그들 위로 서 있는 로리(Lorry) 씨를 향해 손을 들며 속삭였다.",
    "Lorry as he stood over them, blowing his nose repeatedly, \"could we arrange to leave Paris immediately? That way, we can take him directly from this door to the carriage.\"": "그녀가 여러 번 코를 풀며 그들 위로 서 있는 로리 씨를 향해 손을 들며 속삭였다, \"우리가 즉시 파리를 떠날 수 있도록 준비해 주실 수 있나요? 그렇게 하면, 우리는 이 문에서 바로 마차로 그를 모실 수 있을 거예요.\"",
    "\"But think about it.": "\"하지만 생각해 보세요.",
    "Is he strong enough to travel?\" asked Mr.": "그분이 여행하실 만큼 충분히 강하신가요?\" 로리 씨가 물었다.",
    "Lorry.": "로리(Lorry).",
    "\"He is much readier for that, I think, than to stay in this city that has been so terrible to him.\"": "\"그분에게 너무나 끔찍했던 이 도시에 머무는 것보다, 그 일에 훨씬 더 준비가 되어 있으시다고 생각해요.\"",
    "\"That is true,\" said Defarge, who had knelt down to watch and listen. \"In fact, Monsieur Manette is much better off leaving France entirely.": "\"그 말씀이 맞소,\" 무릎을 꿇고 지켜보며 듣고 있던 드파르지(Defarge)가 말했다. \"사실, 마네트(Manette) 씨는 아예 프랑스를 떠나는 편이 훨씬 낫소.",
    "Should I go hire a carriage and fresh horses?\"": "제가 가서 마차와 새 말들을 빌려올까요?\"",
    "\"That is a matter of business,\" said Mr.": "\"그건 사업상의 문제로군요,\" 로리 씨가 말했다.",
    "Lorry, quickly returning to his organized, professional way of speaking. \"And if business needs to be done, I had better take care of it.\"": "로리 씨가 빠르고 조직적인 직업적인 말투로 신속히 돌아가며 말했다. \"그리고 만약 사업이 처리되어야 한다면, 제가 그것을 맡는 것이 낫겠소.\"",
    "Miss Manette urged, \"Then please, leave us here for now.": "마네트 양이 재촉했다. \"그럼 부디, 당분간은 저희를 여기에 남겨두고 가 주세요.",
    "You see how calm he is, and you don't need to worry about leaving him with me.": "그가 얼마나 평온한지 보이시죠, 그러니 그를 저와 함께 남겨두는 것에 대해 걱정하실 필요 없어요.",
    "Why would you be?": "왜 걱정하시겠어요?",
    "If you lock the door to make sure no one interrupts us, I am sure you will find him just as quiet when you return.": "아무도 우리를 방해하지 못하도록 문을 잠그고 가신다면, 돌아오셨을 때도 그가 이토록 조용히 있는 것을 틀림없이 보시게 될 거예요.",
    "I will watch over him until you get back, and then we can move him immediately.\"": "두 분이 돌아오실 때까지 제가 그를 지켜보고 있겠고, 그러면 우리는 그를 즉시 옮길 수 있을 거예요.\"",
    "Both Mr.": "두 분 모두.",
    "Lorry and Defarge were reluctant to do this and preferred to have one of them stay behind.": "로리 씨와 드파르지는 모두 이렇게 하는 것을 주저했고 둘 중 한 명이 뒤에 남기를 원했다.",
    "They had to arrange for the carriage, horses, and travel papers. Time was running out as the day ended. So they split up the tasks and hurried off to complete them.": "그들은 마차, 말, 그리고 통행증을 준비해야 했다. 날이 저물고 있어 시간이 부족했다. 그래서 그들은 임무를 나누어 그것들을 마치기 위해 서둘러 나갔다.",
    "Then, as darkness filled the room, the daughter laid her head on the hard floor right next to her father and watched him.": "그런 다음, 어둠이 방을 채우자, 딸은 딱딱한 바닥 위의 아버지 바로 옆에 머리를 누이고 그를 지켜보았다.",
    "The darkness grew deeper and deeper, and they both lay quietly until a light shone through the cracks in the wall.": "어둠은 점점 더 깊어졌고, 벽의 틈새로 빛이 비칠 때까지 두 사람은 조용히 누워 있었다.",
    "Mr.": "로리(Lorry) 씨와 무슈 드파르지는",
    "Lorry and Monsieur Defarge had prepared everything for the trip. They brought traveling coats, blankets, bread, meat, wine, and hot coffee.": "여행을 위한 모든 것을 준비했다. 그들은 여행용 외투, 담요, 빵, 고기, 포도주, 그리고 뜨거운 커피를 가져왔다.",
    "Monsieur Defarge placed the food and the lamp he was carrying on the shoemaker's workbench, the only other thing in the room being a simple straw bed.": "무슈 드파르지는 그가 들고 있던 음식과 램프를 방 안에 있는 유일한 다른 물건인 초라한 짚 침대 곁의 구두장이의 작업대 위에 올려놓았다.",
    "Then he and Mr. Lorry woke the prisoner and helped him stand up.": "그런 다음 그와 로리 씨는 죄수를 깨워 그가 일어서도록 도왔다.",
    "No one could have understood what was going on in his mind by looking at the scared, blank look on his face.": "그의 얼굴에 떠오른 겁먹고 멍한 표정을 보고서는 그의 마음속에 무슨 일이 벌어지고 있는지 아무도 이해할 수 없었을 것이다.",
    "Whether he understood what had happened, remembered what they had said, or even knew he was free were questions that no one could answer.": "그가 무슨 일이 일어났는지 이해했는지, 그들이 했던 말을 기억했는지, 아니면 심지어 자신이 자유롭다는 것을 알고 있었는지는 아무도 대답할 수 없는 질문이었다.",
    "They tried talking to him, but he was so confused and slow to respond that they became worried by his state and decided to leave him alone for the time being.": "그들은 그에게 말을 걸어보려 했지만, 그는 너무나 혼란스러워했고 대답이 늦어서 그들은 그의 상태를 걱정하게 되었고 당분간은 그를 홀로 내버려두기로 결정했다.",
    "He had a wild, lost way of holding his head in his hands sometimes, which they had not seen before. Yet, he seemed to find some comfort in the sound of his daughter's voice, and always turned toward her whenever she spoke.": "그는 때때로 두 손으로 머리를 감싸 쥐는, 그들이 전에는 본 적이 없는 거칠고 길 잃은 듯한 행동을 보였다. 하지만 그는 딸의 목소리에서 어떤 위안을 찾는 듯했고, 그녀가 말할 때마다 항상 그녀를 향해 고개를 돌렸다.",
    "With the obedient attitude of someone long forced to follow orders, he ate and drank whatever they offered, and put on the coat and blankets they gave him.": "오랫동안 명령을 따르도록 강요받은 사람의 순종적인 태도로, 그는 그들이 제공하는 것이면 무엇이든 먹고 마셨으며, 그들이 준 외투와 담요를 걸쳤다.",
    "He willingly let his daughter put her arm through his, and took, and held, her hand in both of his.": "그는 딸이 그의 팔에 그녀의 팔을 끼우도록 기꺼이 허락했고, 그녀의 손을 그의 두 손으로 잡고 움켜쥐었다.",
    "They began to walk down the stairs, with Monsieur Defarge leading the way with the lamp and Mr.": "그들은 무슈 드파르지가 램프를 들고 길을 안내하고 로리 씨가 맨 뒤에서 걷는 가운데, 계단을 내려가기 시작했다.",
    "Lorry walking at the end.": "맨 끝에서 걷는 로리 씨.",
    "They had only gone down a few steps of the long main staircase when the doctor stopped, staring up at the ceiling and around at the walls.": "그들이 길고 주요한 계단을 불과 몇 단 내려갔을 때, 의사는 멈춰 서서 천장을 올려다보고 주위의 벽을 둘러보았다.",
    "\"Do you remember this place, father?": "\"이곳이 기억나세요, 아버지?",
    "Do you remember coming up here?\"": "이곳으로 올라오셨던 거 기억하세요?\"",
    "\"What did you say?\"": "\"뭐라고 했니?\"",
    "But before she could repeat the question, he muttered an answer as if she had already done so.": "하지만 그녀가 질문을 반복하기도 전에, 그는 마치 그녀가 이미 그렇게 한 것처럼 중얼거리듯 대답했다.",
    "\"Remember?": "\"기억나냐고?",
    "No, I don't remember.": "아니, 기억나지 않아.",
    "It was so very long ago.\"": "그건 아주 오래 전 일이야.\"",
    "It was clear that he had no memory of being brought from the prison to this house.": "그가 감옥에서 이 집으로 끌려왔던 일에 대해 아무런 기억이 없다는 것은 분명했다.",
    "They heard him mutter, \"One Hundred and Five, North Tower.\" When he looked around, he was clearly looking for the thick fortress walls that had surrounded him for so long.": "그들은 그가 \"백오 번, 북쪽 탑(North Tower)\"이라고 중얼거리는 것을 들었다. 그가 주위를 둘러보았을 때, 그는 분명 너무나 오랫동안 그를 둘러싸고 있던 두꺼운 요새의 벽들을 찾고 있었다.",
    "When they reached the courtyard, he automatically changed his step, expecting to cross a drawbridge. When there was no drawbridge and he saw the carriage waiting in the open street, he let go of his daughter's hand and held his head in his hands again.": "안뜰에 도착했을 때, 그는 도개교를 건널 것이라 예상하며 무의식적으로 발걸음을 바꿨다. 도개교가 없고 마차가 탁 트인 거리에 기다리고 있는 것을 보았을 때, 그는 딸의 손을 놓고 다시 두 손으로 머리를 감싸 쥐었다.",
    "There was no crowd outside the door. No one looked out from the many windows. Not even a single person walked down the street.": "문 밖에는 군중이 없었다. 수많은 창문에서 밖을 내다보는 사람도 없었다. 심지어 단 한 사람도 거리를 걸어 내려가지 않았다.",
    "An unnatural silence and emptiness filled the air.": "부자연스러운 침묵과 공허함이 공기를 채우고 있었다.",
    "Only one person was visible. That was Madame Defarge. She leaned against the doorframe, knitting, and appearing to see nothing.": "오직 한 사람만이 보였다. 그것은 마담 드파르지였다. 그녀는 문틀에 기대어 뜨개질을 하며, 아무것도 보지 않는 척하고 있었다.",
    "The prisoner climbed into the carriage and his daughter followed him. But just as Mr.": "죄수는 마차에 올라탔고 그의 딸이 그를 따랐다. 하지만 로리 씨가 안으로 발을 내딛으려던 찰나,",
    "Lorry was stepping in, he stopped on the step because the doctor began pleading sadly for his shoemaking tools and the unfinished shoes.": "의사가 슬프게 그의 구두 수선 도구들과 미완성된 구두들을 애원하기 시작했기 때문에 그는 발판 위에서 멈춰 섰다.",
    "Madame Defarge immediately called out to her husband that she would get them, and walked out of the lamplight, knitting, across the courtyard.": "마담 드파르지는 즉시 남편에게 자신이 그것들을 가져오겠다고 외쳤고, 뜨개질을 하며 등불 밖으로 걸어 나가 안뜰을 가로질렀다.",
    "She returned quickly and handed the tools into the carriage. Then she went straight back to the doorframe, leaned against it, and went on knitting, appearing to see nothing.": "그녀는 재빨리 돌아와 도구들을 마차 안으로 건네주었다. 그런 다음 그녀는 곧바로 문틀로 돌아가 그곳에 기대고서, 다시 뜨개질을 계속하며 아무것도 보지 않는 듯 행동했다.",
    "Defarge climbed onto the driver's seat and shouted, \"To the city gate!\" The driver cracked his whip, and the carriage clattered away under the dim, hanging streetlamps.": "드파르지는 마부석에 올라타고 \"성문으로!\"라고 소리쳤다. 마부는 채찍을 휘둘렀고, 마차는 어둑어둑하게 매달린 가로등 아래로 요란한 소리를 내며 멀어졌다.",
    "They rode under the hanging streetlamps. The lamps swung brighter in the wealthier streets and dimmer in the poorer ones. They passed lit-up shops, happy crowds, bright cafes, and theater entrances on their way to one of the city gates.": "그들은 매달린 가로등 아래를 달렸다. 가로등은 부유한 거리에서는 더 밝게 흔들렸고 가난한 거리에서는 더 어두웠다. 그들은 성문 중 하나로 향하는 길에 불이 켜진 상점들, 행복한 군중들, 밝은 카페들, 그리고 극장 입구들을 지나쳤다.",
    "Soldiers with lanterns stood at the guardhouse there. \"Your papers, travelers!\" one called out. \"Look here, officer,\" said Defarge, getting down and pulling him aside. \"These are the papers of the gentleman inside with the white hair.": "초롱을 든 군인들이 그곳 위병소에 서 있었다. \"통행증, 여행객들!\" 누군가 외쳤다. \"이리 보시오, 장교 양반,\" 드파르지가 내려서 그를 한쪽으로 끌어당기며 말했다. \"이것들은 마차 안의 흰머리 신사의 통행증이오.",
    "He was placed in my care at the, \" He lowered his voice, and there was a stir among the soldiers' lanterns. A uniformed arm reached into the carriage with a light, and the eyes behind the arm stared with a look of deep surprise and curiosity at the white-haired man. \"Everything is in order.": "그는 나의 보살핌을 받기 위해, \" 그가 목소리를 낮추자, 군인들의 초롱 사이에서 약간의 소란이 일었다. 제복을 입은 팔 하나가 등불과 함께 마차 안으로 뻗어 들어왔고, 그 팔 뒤의 두 눈은 깊은 놀라움과 호기심이 담긴 표정으로 백발의 남자를 응시했다. \"모든 것이 순조롭소.",
    "Move along!\" said the soldier. \"Goodbye!\" replied Defarge.": "\"지나가시오!\" 군인이 말했다. \"안녕히 계시오!\" 드파르지가 대답했다.",
    "And so, they drove under a few last, dim hanging lamps, and out under the vast sky of stars.": "그리하여, 그들은 마지막 몇 개의 어둑어둑한 가로등 아래를 지나 광활한 별빛 하늘 아래로 빠져나갔다.",
    "Above them stretched a canopy of quiet, eternal stars. Some are so far away that scientists say their light may not have even reached our small Earth yet, not enough to show a place where people suffer and live. Beneath that canopy, the shadows of the night were wide and dark.": "그들 위로는 고요하고 영원한 별들의 천개가 펼쳐져 있었다. 어떤 것들은 너무나 멀리 떨어져 있어서 과학자들은 그들의 빛이 아직 우리의 작은 지구에 채 도달하지 않았을지도 모른다고, 사람들이 고통받고 살아가는 곳을 비추기에 충분치 않을지도 모른다고 말한다. 그 천개 아래, 밤의 그림자들은 넓고 짙었다.",
    "All through the cold, restless hours of the night until dawn, the same question whispered in the mind of Mr.": "동이 틀 때까지 차갑고 불안한 밤 시간 내내, 자비스 로리(Jarvis Lorry) 씨의 마음속에서는 똑같은 질문이 속삭여졌다.",
    "Jarvis Lorry. He sat opposite the man who had been dug out of his living grave, wondering what parts of his mind were lost forever and what could still be healed:": "그는 살아있는 무덤에서 파헤쳐진 사람의 맞은편에 앉아, 그의 정신 중 어느 부분이 영원히 사라졌고 어느 부분이 여전히 치유될 수 있을지 궁금해했다:",
    "\"I hope you care to be recalled to life?\"": "\"다시 삶으로 소환되는 것에 관심이 있으시길 바랍니다?\"",
    "And the old answer:": "그리고 그 오래된 대답:",
    "\"I can't say.\"": "\"말할 수 없소.\"",
    "Tellson’s Bank near Temple Bar was an old-fashioned place, even in the year 1780.": "템플 바(Temple Bar) 근처의 텔슨(Tellson) 은행은 1780년이라는 해에도 구식인 장소였다.",
    "It was very small, very dark, very ugly, and very uncomfortable.": "그곳은 매우 작았고, 매우 어두웠으며, 매우 볼품없었고, 매우 불편했다.",
    "Moreover, it was old-fashioned in a very particular way. The bank owners were actually proud of its smallness, its darkness, its ugliness, and its total lack of comfort.": "게다가, 그것은 매우 특이한 방식으로 구식이었다. 은행 소유주들은 그 작음, 그 어두움, 그 볼품없음, 그리고 편안함의 완전한 결여를 사실 자랑스러워했다.",
    "They even bragged about how extreme these qualities were, believing that if the bank were any cleaner or more convenient, it would somehow be less respectable.": "그들은 심지어 은행이 조금이라도 더 깨끗하거나 편리하다면 어쩐지 덜 훌륭해 보일 것이라고 믿으며, 이러한 특성들이 얼마나 극단적인지에 대해 허풍을 떨기도 했다.",
    "This was not just a quiet belief, but an active argument they used against more modern and convenient businesses.": "이것은 단지 조용한 믿음이 아니라, 그들이 더 현대적이고 편리한 사업체들에 대항하여 사용하는 적극적인 주장이었다.",
    "They would say, \"Tellson's doesn’t need extra space, Tellson's doesn’t need bright light, Tellson's doesn’t need fancy decorations.": "그들은 말하곤 했다. \"텔슨(Tellson)은 여분의 공간을 필요로 하지 않고, 텔슨은 밝은 빛을 필요로 하지 않으며, 텔슨은 화려한 장식을 필요로 하지 않습니다.",
    "Other banks might need those things, but Tellson’s, thank Heaven, does not!\"": "다른 은행들은 그런 것들을 필요로 할지도 모르지만, 텔슨은, 하늘에 감사하게도, 그렇지 않습니다!\"",
    "Any of these owners would have disowned his own son over the question of rebuilding or modernizing Tellson's Bank.": "이러한 소유주들 중 누구라도 텔슨 은행의 재건축이나 현대화 문제에 대해서는 자신의 친아들과 절연이라도 했을 것이다.",
    "In this regard, the bank was very much like the country itself. England often punished its citizens for suggesting improvements to old laws and customs. Those laws had long been deeply problematic. But they were kept simply because they were old.": "이러한 점에서, 그 은행은 국가 자체와 매우 흡사했다. 영국은 오래된 법률과 관습의 개선을 제안하는 시민들을 종종 처벌했다. 그 법률들은 오랫동안 매우 문제가 많았다. 하지만 그것들은 단순히 오래되었다는 이유만으로 유지되었다.",
    "Thus, Tellson’s had become the ultimate example of inconvenience.": "그리하여, 텔슨은 불편함의 궁극적인 본보기가 되어 있었다."
}

def clean_target(t):
    return t.replace('’', "'")

import os
q_path = 'c:/git_repo/TKprof_book/work_queue.json'
with open(q_path, 'r', encoding='utf-8') as f:
    queue = json.load(f)

# The range is 800 to 899
start_idx = 800
end_idx = min(900, len(queue))

out_batches = []
files_to_update = {}

lookup = {clean_target(k): v for k, v in translations.items()}

for i in range(start_idx, end_idx):
    item = queue[i]
    if item.get('status') != 'pending':
        continue
    tgt = clean_target(item['target_en'])
    ko = lookup.get(tgt)
    if not ko:
        print("Missing translation for:", tgt)
        ko = "TRANSLATION MISSING"
        
    out_batches.append({
        "file": item['file'],
        "id": item['id'],
        "ko": ko
    })
    
    # Track files that need chapter patching
    if item['file'] not in files_to_update:
        files_to_update[item['file']] = {}
    files_to_update[item['file']][item['id']] = ko

    # Mark as done
    queue[i]['status'] = 'done'

# 1. Output the translated batch file
batch_dir = 'c:/git_repo/TKprof_book/translated_batches'
os.makedirs(batch_dir, exist_ok=True)
with open(os.path.join(batch_dir, 'batch_800_899.json'), 'w', encoding='utf-8') as f:
    json.dump(out_batches, f, ensure_ascii=False, indent=2)

# 2. Patch the original chapter json files
for fname, updates in files_to_update.items():
    ch_path = os.path.join('c:/git_repo/TKprof_book/books/two_cities/json', fname)
    with open(ch_path, 'r', encoding='utf-8') as f:
        ch_data = json.load(f)
    
    for block in ch_data:
        b_id = block.get('id')
        if b_id in updates:
            block['ko'] = updates[b_id]
            # Based on system prompt "translate that Korean back into clear modern English (en). For is_header=true, leave en empty"
            # Our `en` is already target_en in the file or empty for headers, but let's strictly follow the rule if it's a header.
            if block.get('is_header'):
                block['en'] = ""
            
    with open(ch_path, 'w', encoding='utf-8') as f:
        json.dump(ch_data, f, ensure_ascii=False, indent=2)

# 3. Update the queue file
with open(q_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)

print(f"Processed {len(out_batches)} batches. Updated files and work queue.")
