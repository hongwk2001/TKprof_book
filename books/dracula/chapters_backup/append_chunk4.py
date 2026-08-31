import os

ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch09_ko_modern.txt'
en_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch09_en_modern.txt'

ko_content = """
수어드 박사가 명예로운 아서 홈우드에게 보낸 편지입니다.

"9월 3일.

"내 사랑하는 친구 아서에게,—

"반 헬싱 교수님이 다녀가셨네. 교수님은 나와 함께 힐링엄으로 갔고, 그곳에서 루시의 재치 덕분에 어머니가 외출 중이시라는 걸 알게 되었지. 그래서 우리는 그녀와 단둘이 있을 수 있었네. 반 헬싱 교수님은 환자를 아주 주의 깊게 진찰하셨어. 내게 보고서를 보내주기로 하셨으니, 그걸 보고 자네에게 알려주겠네. 물론 내가 진찰 내내 함께 있었던 건 아니니까 말이야. 교수님은 몹시 걱정하시는 눈치였지만, 생각이 좀 필요하다고 하셨네. 내가 우리의 우정과 자네가 이 문제에 대해 나를 얼마나 믿고 있는지 말씀드리자, 교수님은 이렇게 말씀하셨어. '자네가 생각하는 모든 것을 그에게 말해주게. 그리고 괜찮다면 자네가 짐작하는 내 생각까지도 모두 말해주게나. 아니, 농담하는 게 아닐세. 이건 농담이 아니라 삶과 죽음, 어쩌면 그 이상이 걸린 문제야.' 그가 무척 진지했기 때문에 나는 그게 무슨 뜻이냐고 물었네. 우리가 시내로 돌아와 그가 암스테르담으로 돌아가기 전 차를 마시고 있을 때였지. 그는 더 이상 어떤 단서도 주지 않았어. 아서, 그가 입을 다물었다고 해서 자네가 내게 화를 내서는 안 되네. 그의 침묵은 그가 오직 그녀를 위해 온 정신을 쏟고 있다는 뜻이니까. 때가 되면 분명히 모든 걸 명확히 말씀해 주실 거야. 그래서 나는 그에게, 마치 '데일리 텔레그래프' 신문에 특별 묘사 기사를 쓰는 것처럼 우리의 방문에 대한 이야기를 자네에게 글로 써 보내겠다고 했지. 그는 내 말을 귀담아듣지 않는 것 같더니, 런던의 매연이 자신이 학생 시절에 비하면 그리 나쁘지 않은 것 같다고 덧붙이더군. 내일쯤 교수님의 보고서를 받을 수 있을 것 같아. 어떻게든 편지는 받을 수 있을 거야.

"자, 방문에 대한 이야기를 해보지. 루시는 내가 처음 보았을 때보다 더 밝아 보였고 확실히 안색도 좋아졌더군. 자네를 그렇게나 속상하게 했던 그 유령같이 창백한 모습도 좀 사라졌고, 호흡도 정상이 되어 있었네. 그녀는 교수님께 아주 상냥하게 대했고(늘 그렇듯이 말이야), 그분을 편안하게 해드리려 노력했어. 불쌍한 아가씨가 그러려고 무진 애를 쓰고 있다는 걸 난 볼 수 있었지만 말이야. 반 헬싱 교수님도 그걸 눈치채신 것 같았네. 그분의 짙은 눈썹 아래로, 내가 예전부터 잘 알고 있던 그 날카로운 눈빛을 보았거든. 그런 다음 교수님은 우리 자신이나 질병을 제외한 모든 것에 대해 아주 유쾌하게 수다를 떨기 시작하셨네. 그 유쾌함이 어찌나 컸던지 불쌍한 루시가 억지로 꾸며낸 생기가 진짜 생기로 변하는 걸 볼 수 있었어. 그러고 나서 어떤 갑작스러운 변화도 없이 교수님은 방문 목적에 맞게 부드럽게 화제를 돌리며 다정하게 말씀하셨지.—

"'나의 사랑하는 젊은 아가씨, 당신이 이렇게나 많은 사랑을 받고 있다는 사실에 제 기분이 다 좋아집니다. 저 사람들이 당신이 기운이 없고 유령처럼 창백하다고 말했을 때, 제가 그들에게 뭐라고 했는지 아십니까? "흥!"하고 콧방귀를 뀌었죠.' 그는 내 쪽으로 손가락을 튕기더니 말을 이어나갔네. '하지만 당신과 내가 그 사람들이 얼마나 틀렸는지 보여줍시다. 대체 그가 어떻게 젊은 아가씨들에 대해 알겠습니까?' 그는 예전에 수업 시간에 특정한 일(그분은 기회만 있으면 내게 그 일을 상기시키시지)이 있은 후에 날 가리켰던 그 눈빛과 몸짓으로 날 가리키셨어. '그는 자신이 다루는 미치광이 환자들만 알죠. 그들을 행복하게 만들고 그들을 사랑하는 가족들의 품으로 돌려보내는 일 말입니다. 그건 참으로 위대한 일이고 무척 보람된 일이죠. 하지만 젊은 아가씨들이라니! 그에겐 아내도, 딸도 없답니다. 그리고 젊은 사람들은 젊은 사람에게 속마음을 털어놓지 않죠. 나처럼 많은 슬픔을 겪고 그 원인을 꿰뚫어 보는 늙은이에게 말한답니다. 그러니 사랑하는 아가씨, 저 친구는 정원에서 담배나 피우게 내보내고, 우리 둘만 조용히 이야기를 나눕시다.' 나는 그 눈치를 채고 밖으로 나와 산책을 했네. 잠시 후 교수님이 창가로 오셔서 나를 부르시더군. 그분은 진지한 표정으로 이렇게 말씀하셨어. '아주 주의 깊게 진찰해 보았지만 어떤 기능적인 원인도 찾을 수 없었네. 전에 자네 말처럼 피를 많이 흘린 것은 동의해. 하지만 그녀의 상태는 결코 빈혈이 아닐세. 내가 하나라도 놓치는 일이 없도록 그녀의 하녀를 보내달라고 부탁했지. 한두 가지 물어볼 게 있거든. 나는 그 하녀가 무슨 말을 할지 잘 안다네. 하지만 분명 원인이 있어. 모든 일에는 항상 원인이 있는 법이니까. 난 집으로 돌아가 곰곰이 생각해 봐야겠어. 자네는 매일 내게 전보를 쳐주게. 그리고 도움이 필요하다면 내가 다시 오겠네. 몸이 완전히 편치 않은 것도 병이니, 이 병은 나의 흥미를 끄는군. 저 사랑스럽고 젊은 아가씨도 그렇고 말이야. 그녀는 참 매력적이야. 설령 자네의 부탁이나 병 때문이 아니더라도, 나는 그녀를 위해 다시 올 거라네.'

"자네에게 말했듯이 교수님은 우리가 단둘이 있을 때조차 한마디도 더 하지 않으셨네. 그러니 아서, 이제 자네는 내가 아는 모든 것을 알게 된 셈이야. 나는 엄격하게 주시할 걸세. 자네의 아버님께서 병을 이겨내시길 바라네. 내 오랜 친구여, 서로에게 그토록 소중한 두 사람 사이에서 그런 입장에 처하게 된 것은 정말이지 끔찍한 일일 거야. 아버지에 대한 자네의 의무감이 어떤 것인지 잘 알고, 자네가 그 도리를 지키는 것이 옳다고 생각하네. 하지만 만약 무슨 일이 생긴다면, 즉시 루시에게 오라고 기별을 보내겠네. 그러니 내게서 연락이 갈 때까지는 너무 지나치게 걱정하지는 말게나."

수어드 박사의 일기장.

9월 4일.—동물 포식(Zoöphagous) 성향을 보이는 그 환자는 여전히 우리의 관심을 끄는 중이다. 그는 단 한 번의 폭발을 일으켰는데, 바로 어제 평소와는 다른 시간대였다. 정각 정오가 되기 직전, 그는 안절부절못하기 시작했다. 간수장은 그 증상을 알고 즉시 지원을 요청했다. 다행히 사람들이 뛰어와 제시간에 도착할 수 있었다. 정각 정오가 되자 그는 몹시 난폭해졌고, 직원들이 모든 힘을 다해 그를 붙들어야만 했기 때문이다. 하지만 약 5분 정도 지나자 그는 점차 조용해지기 시작했고, 마침내 일종의 우울 상태에 빠져들었다. 그리고 지금까지도 그 상태를 유지하고 있다. 간수장의 말에 따르면 발작을 일으키는 동안 그가 지르는 비명은 참으로 끔찍했다고 한다. 나 역시 병동에 들어왔을 때, 그 소리에 놀란 다른 환자들을 돌보느라 무척 바빴다. 그 소리가 꽤 멀리 떨어져 있던 나조차도 불안하게 만들 정도였으니, 그 영향을 충분히 이해할 수 있다. 지금은 병동의 저녁 식사 시간이 지났고, 내 환자는 여전히 구석에 앉아 무언가를 골똘히 생각하고 있다. 그의 얼굴에는 둔하고 우울하며 비통한 표정이 어려 있는데, 이는 어떤 것을 직접 보여준다기보다는 넌지시 암시하는 것 같다. 도무지 이해할 수가 없다.

***

나중에.—내 환자에게 또 다른 변화가 생겼다. 5시쯤 그를 살펴보았는데, 예전처럼 꽤 행복하고 만족스러워 보였다. 그는 파리들을 잡아먹고 있었고, 푹신한 패드 사이의 문 가장자리에 손톱 자국을 내며 파리를 잡은 횟수를 세고 있었다. 나를 보자 그는 다가와 자신의 나쁜 행동에 대해 사과했다. 그러고는 매우 겸손하고 굽실거리는 태도로 자신의 방으로 돌아가 다시 수첩을 가질 수 있게 해달라고 부탁했다. 나는 그의 비위를 맞춰주는 게 좋다고 생각했고, 그는 이제 창문을 열어둔 채 자신의 방으로 돌아가 있다. 그는 창턱에 차에서 뺀 설탕을 펼쳐놓고 제법 많은 파리를 수확하고 있다. 지금은 파리를 먹지 않고 예전처럼 상자에 넣고 있으며, 벌써 거미를 찾기 위해 방구석을 살피는 중이다. 나는 그의 생각을 알 수 있는 어떤 단서라도 엄청난 도움이 될 것 같아 지난 며칠 동안의 일에 대해 이야기해 보려 했다. 하지만 그는 내 질문에 말려들지 않았다. 그는 잠시 동안 매우 슬퍼하더니, 마치 내게 말한다기보다는 혼잣말을 하듯 멍한 목소리로 이렇게 말했다.—

"다 끝났어! 다 끝났다고! 그가 날 버렸어. 이젠 나 스스로 해내지 않으면 내겐 희망이 없어!" 그러다 갑자기 결연한 표정으로 나를 돌아보며 말했다. "선생님, 저한테 친절을 좀 베푸셔서 설탕을 조금만 더 주시면 안 될까요? 그게 제게 좋을 것 같거든요."

"파리들에게도 그렇고?" 내가 물었다.

"그렇죠! 파리들도 그걸 좋아하고, 난 파리를 좋아하니까, 결론적으로 나도 설탕을 좋아하는 거죠." 광인들은 논리적으로 생각할 줄 모른다고 여기는 어리석은 사람들이 있다. 나는 그에게 설탕을 두 배로 구해주었고, 세상 그 누구보다도 행복해 보이는 그를 남겨두고 방을 나왔다. 그의 속마음을 헤아릴 수 있다면 얼마나 좋을까.

***

자정.—그에게 또 변화가 생겼다. 나는 훨씬 상태가 호전된 웨스텐라 양을 진찰하고 막 돌아온 참이었다. 병동 문앞에 서서 일몰을 바라보고 있는데 다시 그가 소리치는 소리가 들렸다. 그의 방이 건물 이쪽에 있어서 아침보다 훨씬 더 잘 들렸다. 불길한 붉은빛, 먹물 같은 그림자, 더러운 물 위에서나 볼 수 있을 법한 온갖 기이한 색채로 물든, 런던 위로 펼쳐진 그 아름답고 매캐한 노을의 장관에서 시선을 돌려야 했다. 그러곤 끝없는 고통의 숨결로 가득 찬 차가운 돌 건물, 이 무자비한 현실, 그리고 그 모든 것을 견뎌내야 하는 나의 황량한 마음을 직면해야 하는 것은 나에게 충격이었다. 해가 저물어갈 즈음 그에게 도착했고, 나는 창문 너머로 붉은 해가 지는 것을 보았다. 해가 질수록 그의 광기도 점점 잦아들더니, 마침내 해가 완전히 넘어가자 그는 자신을 붙들고 있던 사람들의 손에서 빠져나와 바닥에 축 늘어져 버렸다. 하지만 미치광이들의 지적 회복력이란 실로 놀라웠다. 불과 몇 분 만에 그는 아주 차분하게 일어나 주위를 둘러보았다. 나는 그가 어떻게 행동할지 보고 싶어 간수장들에게 그를 붙잡지 말라고 신호를 보냈다. 그는 곧장 창가로 가서 설탕 부스러기를 털어내더니, 파리 상자를 집어 밖으로 내용물을 비우고 상자마저 던져버렸다. 그런 다음 창문을 닫고 침대로 가 앉았다. 이 모든 행동이 너무나 놀라워서 나는 그에게 물었다. "더 이상 파리를 기르지 않을 셈인가?"

"네." 그가 대답했다. "그런 쓰레기 같은 것들엔 이제 신물이 납니다!" 그는 참으로 놀랍고 흥미로운 연구 대상이다. 그의 마음속이나 갑작스러운 발작의 원인을 조금이나마 엿볼 수 있다면 좋으련만. 잠깐, 만약 오늘 그의 발작이 왜 정오와 일몰에 일어났는지 알 수 있다면 단서가 될 수도 있다. 마치 달이 어떤 사람들에게 영향을 미치듯이, 태양의 어떤 악의적인 영향력이 특정 시기에 어떤 성향의 사람들에게 영향을 미치는 것일까? 두고 보면 알겠지.

수어드가 런던에서 암스테르담의 반 헬싱에게 보낸 전보.

"9월 4일.—환자의 상태가 오늘 더 호전되었습니다."

수어드가 런던에서 암스테르담의 반 헬싱에게 보낸 전보.

"9월 5일.—환자의 상태가 크게 호전되었습니다. 식욕이 좋고 자연스럽게 수면을 취하며 기분도 좋고 안색도 돌아오고 있습니다."

수어드가 런던에서 암스테르담의 반 헬싱에게 보낸 전보.

"9월 6일.—끔찍할 정도로 상태가 악화되었습니다. 당장 와 주십시오. 한 시간도 지체해선 안 됩니다. 선생님을 뵐 때까지 홈우드에게 보내는 전보는 보류하겠습니다."
"""

en_content = """
Letter, Dr. Seward to Hon. Arthur Holmwood.

"September 3.

"My dear Art,—

"Van Helsing has already come and gone. He traveled down with me to Hillingham. Thanks to Lucy's clever planning, we found that her mother was out to lunch, giving us the perfect opportunity to be alone with her. Van Helsing conducted a very thorough examination of the patient. He promised to send me a full report, which I will summarize for you, as I was naturally out of the room for part of the time. I'm afraid he is very concerned, but he told me he needs time to think. When I explained the depth of our friendship and how much you are trusting me to handle this, he said: 'You must tell him everything you suspect. Tell him what you think my diagnosis is, if you care to guess. And no, I am not joking. This is absolutely not a joke; it is a matter of life and death, and perhaps even more than that.' I asked him exactly what he meant by that dark comment, because he looked incredibly serious. We were back in London by then, having a quick cup of tea before he had to catch his train back to Amsterdam. He flatly refused to give me any more clues. You mustn't be angry with me—or with him, Art. His silence simply means that his brilliant mind is working overtime to figure out how to save her. I assure you, he will speak very plainly when the time is right. I told him I would just write you a detailed account of our visit, as if I were a reporter writing a feature piece for The Daily Telegraph. He didn't seem to care; he just casually mentioned that the smog in London didn't seem quite as bad as it was when he studied here years ago. I should receive his official report by tomorrow, assuming he has time to write it. Either way, I am expecting a letter from him.

"Now, about the visit itself. Lucy was noticeably more cheerful than the last time I saw her, and she objectively looked better. That ghastly, ghostly paleness that upset you so much had faded somewhat, and her breathing was completely normal. She was incredibly sweet to the Professor (as she is to everyone), and she tried very hard to make him feel comfortable. However, I could tell the poor girl was making a massive effort just to keep up appearances. I am certain Van Helsing noticed it too, because I saw that quick, sharp look dart out from under his bushy eyebrows—a look I know very well from my days as his student. He then started chatting about anything and everything except us and her illness. He was so incredibly warm and genial that I actually saw poor Lucy's forced cheerfulness melt into genuine animation. Then, without missing a beat, he smoothly transitioned the conversation to the medical reason for his visit, saying in a gentle voice:—

"'My dear young lady, it brings me so much joy to see how deeply you are loved by those around you. That means a great deal, my dear, especially when I cannot physically see what is causing your distress. They warned me you were depressed and looked ghastly pale. I say to them: "Nonsense!"' He snapped his fingers in my direction and continued: 'You and I will prove exactly how wrong they are. How could he possibly understand young ladies?' He pointed at me with the exact same theatrical gesture he used to point me out to his medical class, usually after some specific incident he never lets me forget. 'He spends his days playing with lunatics, trying to bring them back to sanity and return them to the families who love them. It is important work, and yes, it is rewarding to restore that kind of happiness. But young ladies! He doesn't have a wife or a daughter! And young people rarely confess their true troubles to other young people; they tell them to old men like me, men who have seen countless sorrows and understand the root causes of them. So, my dear, we are going to send him outside to smoke a cigarette in the garden, while you and I have a nice, quiet talk all to ourselves.' I took the obvious hint and went outside for a stroll. A little while later, the Professor came to the window and called me back inside. He looked very serious and said: 'I have completed a thorough examination, but I cannot find a functional physical cause. I agree with your initial assessment that she has suffered a significant loss of blood; she clearly has, but she isn't actively losing it now. Furthermore, her overall condition does not indicate standard anemia. I have asked her to send her maid to me so I can ask a question or two, just to make absolutely sure I haven't missed a minor detail. I already know what the maid will say. And yet, there must be a cause; there is always a cause for everything. I must go back home and think about this deeply. You must send me a telegram every single day with updates. If there is a reason to return, I will come back immediately. Her illness—because failing to be perfectly well is, by definition, an illness—fascinates me. And this sweet young girl fascinates me too. She has charmed me. I will return for her sake alone, even if I wouldn't for you or the medical mystery.'

"Just as I warned you, he absolutely refused to say another word about it, even when we were finally alone. So now, Art, you know exactly as much as I do. I am going to keep a very close eye on her. I sincerely hope your poor father is recovering. It must be incredibly painful for you, my dear old friend, to be torn between two people you love so deeply. I respect your sense of duty to your father, and you are doing the right thing by staying by his side. But rest assured, if the situation changes and you are needed here, I will wire you to come to Lucy immediately. Until you hear from me, please try not to worry yourself sick."

Dr. Seward's Diary.

September 4.—My zoöphagous patient, Renfield, continues to fascinate me. He only had one violent outburst recently, and it happened yesterday at a very unusual time. Right before noon, he started becoming agitated. The ward attendant recognized the warning signs and immediately called for backup. Thank goodness the guards came running and arrived just in time, because right at the stroke of noon, he became so violently aggressive that it took the combined strength of all the men just to hold him down. After about five minutes, however, he slowly began to calm down, eventually sinking into a deep state of melancholy. He has remained in that depressed state ever since. The attendant told me that the screams Renfield let out during the fit were genuinely horrifying. I can believe it; when I arrived on the ward, my hands were full trying to calm down the other patients who had been terrified by the noise. I completely understand their reaction, because the sounds chilled me as well, even though I was quite far away when it started. It is now past the asylum's dinner hour, and my patient is currently sitting in the corner of his cell, brooding. He has a dull, sullen, miserable look on his face, which feels like it is hinting at some dark secret rather than openly displaying it. I just can't figure it out.

***

Later.—There has been another drastic change in my patient. I checked on him at five o'clock and found him looking just as happy and content as he used to be. He was back to catching flies and eating them, and he was keeping a tally of his catches by scratching marks with his fingernails on the edge of the door, right between the padded panels. When he saw me, he rushed over, apologized profusely for his bad behavior, and begged me in a very humble, groveling way to be moved back to his regular room and to have his notebook returned. I decided it was best to indulge him, so he is now back in his standard room with the window wide open. He has sprinkled the sugar he saved from his tea along the windowsill and is harvesting an impressive number of flies. He isn't eating them right now; instead, he is carefully storing them in a small box, exactly like he used to do, and he is already scouring the corners of the ceiling for a spider. I tried to coax him into talking about the events of the past few days, hoping I might get a clue to what is going on in his head, but he completely ignored the bait. For a brief moment, he looked incredibly sad. He stared off into the distance and said, almost as if he were talking to himself rather than me:—

"It's all over! All over! He has abandoned me. There is no hope for me now unless I take matters into my own hands!" Then, suddenly spinning around to face me with a determined look, he asked: "Doctor, would you be so kind as to give me a little extra sugar? I really think it would be good for my health."

"And what about the flies?" I asked.

"Exactly! The flies like sugar, and I like the flies; therefore, I like the sugar." And to think, there are ignorant people in the world who believe madmen are incapable of logical argument. I ordered the staff to give him a double ration of sugar and left him looking as happy as any man on earth. I truly wish I could understand how his mind works.

***

Midnight.—Yet another shift in his behavior. I had just returned from visiting Miss Westenra, who I am happy to say was looking much better. I was standing near the front gate of the asylum watching the sunset when I heard Renfield screaming again. Since his room faces this side of the building, the sound was much clearer than it was this morning. It was incredibly jarring to look away from the stunning, smoky beauty of the London sunset—with its fiery reds, deep black shadows, and all those incredible colors that paint polluted clouds just as beautifully as they do dirty water—and be forced to confront the grim, cold stone walls of my own building. It is a place filled with living misery, and my own lonely heart has to endure it all. I reached his room just as the sun was dipping below the horizon, and I could see the red disc sinking through his open window. As the sun disappeared, his frenzy faded with it. The exact moment the sun vanished, he went completely limp and slid out of the guards' hands onto the floor like a dead weight. It is truly astonishing how quickly a lunatic's brain can reset itself. Within a few minutes, he stood up, perfectly calm, and looked around the room. I silently signaled the attendants to let him go because I wanted to see what he would do next. He walked straight over to the window and brushed all his precious sugar crumbs outside. Next, he grabbed his box of flies, dumped them out the window, and threw the empty box away. Finally, he closed the window, walked across the room, and sat quietly on his bed. This total reversal surprised me, so I asked him: "Have you decided not to keep flies anymore?"

"No," he replied bluntly. "I am absolutely sick of all that garbage!" He is undoubtedly a fascinating psychological study. I desperately wish I could get even a glimpse into his mind, or uncover the trigger for these sudden, explosive rages. Wait a minute; there might be a clue staring me in the face, if I can just figure out why his violent fits happened precisely at noon and sunset today. Is it possible that the sun exerts some kind of malicious influence on certain susceptible minds at specific times of day, similar to how the moon affects others? I suppose we shall see.

Telegram, Seward, London, to Van Helsing, Amsterdam.

"September 4.—Patient continues to improve today."

Telegram, Seward, London, to Van Helsing, Amsterdam.

"September 5.—Patient vastly improved. Excellent appetite; sleeping soundly; high spirits; color returning to her face."

Telegram, Seward, London, to Van Helsing, Amsterdam.

"September 6.—Catastrophic change for the worse. Come back immediately; do not waste a single hour. I am withholding my telegram to Holmwood until I have consulted with you."
"""

with open(ko_file, 'a', encoding='utf-8') as f:
    f.write('\n\n' + ko_content.strip())
with open(en_file, 'a', encoding='utf-8') as f:
    f.write('\n\n' + en_content.strip())
print("Append successful.")
