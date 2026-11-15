import os

ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch09_ko_modern.txt'
en_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch09_en_modern.txt'

ko_content = """
아서 홈우드가 수어드 박사에게 보낸 편지입니다.

"앨버말 호텔에서, 8월 31일.

"내 사랑하는 친구 잭에게,—

"부탁 하나만 들어주게. 루시가 아파. 뭐랄까, 특별한 병이 있는 건 아닌데, 안색이 끔찍하게 안 좋고 하루가 다르게 상태가 나빠지고 있어. 무슨 까닭이라도 있냐고 그녀에게 물어보았지. 그녀의 어머니께는 감히 여쭤볼 엄두조차 내지 못했네. 웨스텐라 부인의 현재 건강 상태를 고려할 때, 딸에 대한 걱정으로 그 불쌍한 부인의 마음을 어지럽히는 것은 치명적일 테니까. 부인은 자신의 죽음이 얼마 남지 않았다는 것—심장병이지—을 내게만 털어놓으셨어. 불쌍한 루시는 아직 그 사실을 모르고 있지만 말이야. 내 사랑하는 연인의 마음을 갉아먹는 무언가가 분명히 있다고 확신하네. 그녀를 생각하면 나는 거의 미칠 지경이고, 그녀의 모습을 볼 때마다 가슴이 찢어지는 것 같아. 나는 그녀에게 자네가 진찰을 한 번 봐주면 좋겠다고 말했네. 처음엔 좀 망설이더니—자네도 그 이유를 알겠지, 오랜 친구여—결국엔 동의했어. 나도 안다네, 오랜 친구여. 이 일이 자네에겐 꽤나 고통스러운 임무가 되겠지만, 모두 루시를 위한 일이니 나도 자네에게 부탁하는 것을 망설일 수 없고 자네 역시 나서 주어야겠네. 웨스텐라 부인이 눈치채지 못하도록 내일 두 시에 힐링엄으로 점심 식사를 하러 오게나. 식사 후에 루시가 자네와 단둘이 있을 기회를 만들 걸세. 나는 차를 마실 때쯤 들를 테니, 그때 우리가 함께 자리를 뜰 수 있겠지. 나는 불안감으로 가득 차 있고, 자네가 그녀를 진찰한 후 가능한 한 빨리 단둘이서 상의하고 싶네. 꼭 와주게!

"아서 올림."

아서 홈우드가 수어드 박사에게 보낸 전보.

"9월 1일.

"아버지가 위독하셔서 급히 호출을 받았네. 지금 편지를 쓰는 중이야. 오늘 밤 우편으로 링(Ring) 지역에 있는 내게 모든 상황을 자세히 적어 보내주게. 필요하다면 전보를 치고."

수어드 박사가 아서 홈우드에게 보낸 편지.

"9월 2일.

"나의 오랜 친구에게,—

"웨스텐라 양의 건강에 관해 한시라도 빨리 자네에게 알려야 할 것 같아 편지를 쓴다네. 내 소견으로는 그녀에게 어떤 신체적 기능 장애나 내가 아는 질병은 없는 것 같아. 하지만 동시에, 그녀의 외형적인 상태는 결코 만족스럽지 않아. 내가 마지막으로 보았을 때와 비교하면 끔찍할 정도로 달라져 있더군. 물론 자네도 염두에 두어야 할 것이, 내가 바라는 만큼 충분히 진찰할 기회가 없었다는 점이야. 우리의 친밀한 우정 자체가 의학 지식이나 관행으로도 좁히기 힘든 약간의 어색함을 만들기도 하니까. 자네가 어느 정도 스스로 결론을 내릴 수 있도록, 무슨 일이 있었는지 정확히 말해주는 게 낫겠네. 그러고 나서 내가 한 조치와 앞으로의 계획을 말해주지.

"내가 보기에 웨스텐라 양은 겉으로는 꽤 밝아 보였어. 그녀의 어머니가 함께 계셨는데, 나는 몇 초 만에 그녀가 어머니를 속이고 걱정하시지 않게 하려고 온갖 노력을 다하고 있다는 걸 눈치챘지. 틀림없이 그녀는 주의를 기울여야 한다는 사실을 알고 있거나 최소한 짐작은 하고 있는 것 같아. 우리는 단둘이 점심을 먹었고, 서로 밝은 분위기를 만들려 애쓴 덕분에 그 보상으로 우리 사이에는 꽤나 진실된 활기가 돌았지. 그러고 나서 웨스텐라 부인이 쉬러 가시고 나와 루시 단둘만 남게 되었어. 우리는 그녀의 내실로 들어갔고, 그곳에 도착할 때까지는 하인들이 오가고 있어서 그녀의 발랄함이 유지되었지. 하지만 문이 닫히자마자 그녀의 얼굴에서 가면이 벗겨졌어. 그녀는 깊은 한숨을 쉬며 의자에 주저앉았고 손으로 두 눈을 가리더군. 그녀의 밝은 기운이 무너진 것을 본 순간, 나는 그 반응을 놓치지 않고 즉시 진단을 시작했네. 그녀는 아주 상냥하게 내게 말했어.—

"'제 자신에 대해 이야기하는 게 얼마나 싫은지 이루 말할 수 없어요.' 나는 그녀에게 의사의 비밀 보장은 신성한 것이지만, 자네가 그녀를 몹시 걱정하고 있다는 사실을 상기시켜 주었지. 그녀는 내 뜻을 단번에 알아차리고 한마디로 그 문제를 정리했네. '원하신다면 아서에게 모든 걸 다 말씀하세요. 전 제 자신은 상관없어요. 오직 그 사람을 위한 거예요!' 그래서 나는 아주 자유로워졌다네.

"나는 그녀에게 다소 피가 부족하다는 걸 쉽게 알 수 있었지만, 일반적인 빈혈 증상은 보이지 않았어. 우연찮게도 나는 그녀의 혈액 상태를 직접 검사할 기회를 얻게 되었지. 뻑뻑한 창문을 열다가 창문 끈이 끊어지면서 깨진 유리에 그녀의 손이 살짝 베였거든. 그 자체로는 아주 가벼운 상처였지만 내게는 확실한 기회가 되었지. 나는 그녀의 피 몇 방울을 채취해 분석했어. 정성 분석(물질의 구성 성분을 알아보는 검사) 결과 상태는 아주 정상이었고, 혈액 자체만 놓고 보면 건강하고 활력 있는 상태라고 추론할 수 있었지. 다른 신체적인 면에서도 걱정할 필요가 없다고 완전히 확신했네. 하지만 어딘가에 원인이 있어야 하니, 그건 분명 정신적인 문제일 것이라는 결론에 도달했어. 그녀는 가끔 숨쉬기가 힘들고, 무기력할 정도로 깊은 잠에 빠지며, 깨고 나면 아무것도 기억하지 못하지만 자기를 두렵게 하는 악몽을 꾼다고 호소하더군. 어릴 때 몽유병이 있었는데 윗비에 있을 때 그 습관이 다시 나타나서 밤에 걸어 나가 이스트 클리프로 향했고, 그곳에서 머레이 양(미나)이 자신을 발견했다고 했어. 하지만 최근에는 그런 증상이 다시 나타나지 않았다고 내게 장담하더군. 나는 갈피를 잡을 수 없어서 내가 아는 최선의 방법을 취했지. 모호하고 원인을 알 수 없는 질병에 관해서는 세계 최고 권위자인 내 옛 친구이자 스승이신 암스테르담의 반 헬싱 교수님께 편지를 썼네. 그분께 이곳으로 와 달라고 부탁드렸어. 자네가 모든 비용을 부담하겠다고 했으니, 자네가 누구인지 그리고 자네와 웨스텐라 양의 관계가 어떤지도 그분께 말씀드렸고. 친애하는 친구여, 이건 자네의 뜻에 따른 것이기도 하고, 나 역시 그녀를 위해 할 수 있는 일이 있다면 무엇이든 기쁘고 자랑스럽게 할 준비가 되어 있기 때문이지. 반 헬싱 교수님은 개인적인 이유 때문에 나를 위해서라면 무슨 일이든 하실 분이야. 그러니 그분이 어떤 근거로 오시든 우리는 그분의 뜻을 따라야 해. 겉보기엔 독단적인 분 같지만, 그건 그분이 누구보다도 자신이 하는 말에 대해 잘 알고 계시기 때문이지. 그는 철학자이자 형이상학자이며, 당대 가장 진보적인 과학자 중 한 명일세. 그리고 내 생각에, 그는 완벽하게 열린 마음을 가진 분이야. 강철 같은 신경, 얼음장 같은 냉철함, 불굴의 결단력, 뛰어난 자기 통제력, 그리고 단순한 미덕을 넘어선 축복과도 같은 관용, 심장처럼 고동치는 가장 친절하고 진실된 마음—이런 것들이 그분이 인류를 위해 훌륭한 일을 수행할 수 있게 하는 무기라네. 그분의 통찰력은 그분의 모든 것을 포용하는 넓은 마음만큼이나 광범위해서, 이론과 실제 모두에서 뛰어난 업적을 남기고 계시지. 내가 이 사실들을 자네에게 말해주는 건, 내가 왜 그분을 그토록 신뢰하는지 자네가 알았으면 해서야. 나는 그분께 당장 와달라고 부탁했네. 내일 웨스텐라 양을 다시 만날 생각이야. 내가 너무 일찍 방문해서 부인이 놀라시는 일이 없도록, 상점에서 그녀를 만나기로 했네.

"언제나 자네의 친구인,

"존 수어드."

에이브러햄 반 헬싱 교수(의학 박사, 철학 박사, 문학 박사 등)가 수어드 박사에게 보낸 편지.

"9월 2일.

"나의 좋은 친구에게,—

"자네의 편지를 받았을 때, 난 이미 자네에게 가고 있는 중이었네. 운 좋게도 날 믿어주는 사람들에게 피해를 주지 않고 즉시 떠날 수 있었지. 만약 상황이 달랐다면 나를 믿는 그들에겐 안 좋은 일이 되었을 거야. 왜냐하면 내 친구가 자신이 소중하게 여기는 사람을 도와달라며 날 부르면, 나는 당장 그에게 달려가기 때문이지. 친구분에게 이렇게 전해주게. 자네의 그 친구분이 자네를 돕기 위해 엄청난 재산을 쓴다 해도, 과거 자네가 날 위해 해준 일에 비하면 아무것도 아니라고 말일세. 예전에 너무 긴장한 우리 동료가 실수로 떨어뜨린 칼에 내가 베였을 때, 자네가 그 괴사독을 내 상처에서 재빨리 빨아내 주지 않았던가. 게다가 나의 좋은 친구인 자네를 위해 무언가 할 수 있다는 건 나에겐 더 큰 기쁨이지. 나는 자네를 보고 가는 거라네. 그러니 내가 가까이 머물 수 있도록 그레이트 이스턴 호텔에 내 방을 잡아주게. 그리고 내일 너무 늦지 않은 시간에 그 아가씨를 볼 수 있도록 일정을 잡아주면 좋겠네. 어쩌면 그날 밤 바로 여기로 돌아와야 할지도 모르거든. 하지만 필요하다면 3일 후에 다시 오고, 그래야 한다면 더 오래 머물 수도 있어. 그때까지 잘 있게, 내 친구 존.

"반 헬싱."
"""

en_content = """
Letter, Arthur Holmwood to Dr. Seward.

"Albemarle Hotel, August 31.

"My dear Jack,—

"I need a massive favor from you. Lucy is unwell; she doesn't seem to have a specific illness, but she looks absolutely terrible and is getting visibly worse every single day. I asked her if there was any underlying cause. I don't dare ask her mother, because given Mrs. Westenra's current frail health, upsetting her with worries about her daughter could be practically fatal. You see, Mrs. Westenra has secretly confided in me that she is dying of a heart condition—though poor Lucy has no idea yet. I am utterly convinced that something is weighing heavily on my sweet girl's mind. I am practically going out of my mind with worry; just looking at her breaks my heart. I told her I was going to ask you to examine her. She hesitated at first—and I know exactly why, old friend—but she finally agreed. I know this will be an emotionally painful task for you, my friend, but it is for her sake. I cannot hesitate to ask you, and you must not hesitate to act. Please come to Hillingham for lunch tomorrow at two o'clock. This way, we won't raise any suspicions with Mrs. Westenra. After lunch, Lucy will find an excuse to be alone with you. I will drop by around teatime so we can leave together. I am filled with overwhelming anxiety and I need to consult with you privately the moment you finish your examination. Please don't let me down!

"ARTHUR."

Telegram, Arthur Holmwood to Seward.

"September 1.

"I have been unexpectedly summoned to see my father; his condition has worsened. I am writing to you now. Please write me a full report via tonight's mail and send it to Ring. Send a telegram if it's an emergency."

Letter from Dr. Seward to Arthur Holmwood.

"September 2.

"My dear old friend,—

"Regarding Miss Westenra's health, I want to reassure you immediately that, in my medical opinion, there is no functional disorder or known disease present. That being said, I am incredibly unsatisfied with her overall appearance; she looks terribly different from the last time I saw her. Of course, you have to remember that I couldn't conduct as thorough an examination as I would have liked. Our close friendship creates a bit of awkwardness that neither medical professionalism nor social etiquette can entirely smooth over. I think it's best if I tell you exactly what happened, allowing you to draw your own conclusions to some extent. Then, I will tell you what steps I have taken and what I plan to do next.

"When I arrived, Miss Westenra seemed to be in high spirits. Her mother was in the room, and within seconds I realized that Lucy was using every ounce of her energy to mislead her mother and keep her from worrying. I have no doubt that she either knows or suspects that her mother's health requires extreme caution. We ate lunch alone, and since we both tried so hard to be cheerful, we actually ended up creating a genuinely pleasant atmosphere. Afterward, Mrs. Westenra went to lie down, leaving Lucy and me alone. We moved into her private sitting room, and her cheerful demeanor lasted until we got there, mainly because the servants were constantly coming and going. However, the exact moment the door closed, the mask completely slipped from her face. She sank heavily into a chair with a massive sigh and covered her eyes with her hands. Seeing her fake high spirits collapse, I immediately used this sudden change in mood to begin my diagnosis. She looked at me and said very sweetly:—

"'I can't even begin to tell you how much I hate talking about myself.' I gently reminded her that a doctor's confidentiality is absolute, and that you were desperately worried about her. She understood my point instantly and settled the issue with one sentence. 'Tell Arthur absolutely anything you want. I don't care about myself; I am doing this entirely for him!' So, I have complete freedom to share this with you.

"I could easily tell that she is somewhat pale and lacking in blood, but she didn't show the typical signs of standard anemia. Purely by chance, I was actually able to test the quality of her blood. While she was struggling to open a stiff window, the cord snapped, and she slightly cut her hand on the broken glass. It was a very minor injury, but it gave me the perfect opportunity. I collected a few drops of her blood and analyzed them. The qualitative analysis showed a perfectly normal condition, which indicates, in my opinion, a strong underlying state of health. As for other physical aspects, I am completely satisfied that there is no cause for concern. But since there has to be a reason for her decline somewhere, I have concluded that the root cause must be psychological. She complains that she occasionally has difficulty breathing properly, and she falls into deep, sluggish sleeps filled with terrifying dreams—though she can never remember what the dreams are actually about. She mentioned that she used to sleepwalk as a child, and that the habit returned while she was in Whitby. She even walked out into the night once and went all the way to the East Cliff, where Miss Murray found her. However, she swears that the sleepwalking hasn't happened recently. I am honestly stumped, so I did the smartest thing I could think of: I wrote to my old friend and mentor, Professor Van Helsing of Amsterdam. He knows more about obscure and mysterious diseases than anyone else in the world. I asked him to travel here, and since you insisted that all expenses would be on you, I explained who you are and your relationship to Miss Westenra. I am doing all of this, my dear friend, exactly as you wished, because I am proud and happy to do absolutely anything I can for her. I know Van Helsing would do anything for me for personal reasons, so regardless of his methods, we must follow his advice. He can sometimes seem bossy or arbitrary, but that is simply because he genuinely knows what he is talking about better than anyone else. He is a philosopher, a metaphysician, and one of the most brilliant, advanced scientists of our time; and above all, I believe he possesses a completely open mind. Combine that with nerves of steel, an icy calmness in emergencies, unstoppable determination, incredible self-control, a level of tolerance that elevates it from a mere virtue to a true blessing, and the absolute kindest, truest heart imaginable—these are the tools he brings to his noble work for humanity. His work spans both theory and direct practice, because his perspectives are as broad as his limitless empathy. I am telling you all of this so you understand exactly why I place such absolute trust in him. I have asked him to come immediately. I am going to see Miss Westenra again tomorrow. She agreed to meet me at the department store, so I don't alarm her mother by visiting the house again so soon.

"Yours always,

"JOHN SEWARD."

Letter, Abraham Van Helsing, M.D., Ph.D., D.Lit., etc., etc., to Dr. Seward.

"September 2.

"My good Friend,—

"By the time you read this letter, I will already be on my way to you. Luckily, I was able to drop everything and leave immediately without letting down anyone who was relying on me here. If the situation had been different, it would have been unfortunate for them, because when my friend calls me to help someone he cares about, I come at once. Please tell your friend that when you so quickly sucked the gangrene poison out of my wound—after that nervous colleague of ours let his scalpel slip—you did far more for him, seeing as he now needs my help and you called for it, than all his massive fortune ever could. But it is an added joy to do this for him, because he is your friend; ultimately, I am coming because of you. Please book a room for me at the Great Eastern Hotel so I can be close by, and arrange for us to see the young lady at a reasonable hour tomorrow. I will likely have to travel back here that same night. However, if necessary, I will return in three days, and I will stay longer if the situation demands it. Until then, goodbye, my friend John.

"VAN HELSING."
"""

with open(ko_file, 'a', encoding='utf-8') as f:
    f.write('\n\n' + ko_content.strip())
with open(en_file, 'a', encoding='utf-8') as f:
    f.write('\n\n' + en_content.strip())
print("Append successful.")
