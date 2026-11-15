import json

updates = {
273: ("Cruncher(크런처) 씨는 증언을 듣는 동안 어느새 손가락에 묻은 녹을 점심 식사처럼 잔뜩 먹어 치우고 있었다.", "Mr. Cruncher had by this time eaten quite a lunch of rust off his fingers while following the evidence."),
274: ("이제 그는 Stryver(스트라이버) 씨가 죄수의 변론을 배심원들에게 꼭 맞는 양복처럼 재단하여 입히는 과정을 지켜보아야 했다.", "Now he had to watch as Mr. Stryver fitted the prisoner's case onto the jury like a well-tailored suit of clothes."),
275: ("그 애국자 Barsad(바사드)가 사실은 고용된 스파이이자 배신자이며, 피를 파는 뻔뻔한 장사꾼이고, 저주받은 유다(Judas) 이래로 지상 최대의 악당 중 한 명이라는 사실을 배심원들에게 보여주었다. (실제로 그는 유다와 꽤 닮아 보였다.)", "He showed them how the patriot Barsad was actually a hired spy and traitor, a shameless trafficker in blood, and one of the greatest scoundrels on earth since the accursed Judas—whom he certainly did resemble."),
276: ("그리고 그 도덕적인 하인 Cly(클라이)가 그의 친구이자 동업자였으며, 그럴 만한 자격이 충분하다는 것을 보여주었다.", "He also showed how the virtuous servant Cly was his friend and partner, and fully deserved to be."),
277: ("프랑스 혈통인 죄수가 프랑스 내의 가족 문제 때문에 어쩔 수 없이 영국 해협(the Channel)을 건너야만 했는데, 바로 그 점 때문에 위조범들과 위증자들의 매서운 눈길이 그를 희생양으로 삼았다는 것을 보여주었다. 물론 그 가족 문제가 무엇인지는 그와 가까운 소중한 사람들을 보호하기 위해, 심지어 목숨이 위태로운 상황에서도 그가 밝힐 수 없었다.", "He showed how the watchful eyes of those forgers and false swearers had targeted the prisoner as a victim, simply because his French ancestry and certain family matters in France required him to travel across the Channel. However, out of consideration for his loved ones, he was forbidden from disclosing what those matters were, even to save his own life."),
278: ("배심원들도 목격했듯 증언을 하며 고통스러워했던 젊은 숙녀에게서 억지로 짜내고 왜곡한 증거는 결국 아무것도 아니었으며, 그저 우연히 함께 있게 된 젊은 신사와 숙녀 사이에 오갈 법한 작고 순수한 호의와 예의에 불과했다는 점도 지적했다. 단, 조지 워싱턴(George Washington)에 대한 언급만은 예외였는데, 그것은 터무니없을 정도로 과장된 것이어서 그저 끔찍한 농담으로밖에 볼 수 없었다.", "He pointed out that the evidence forced and twisted from the young lady, whose anguish during her testimony they had all witnessed, amounted to nothing. It involved only the minor, innocent courtesies and acts of politeness typical between a young gentleman and lady thrown together in such circumstances—except for the reference to George Washington, which was so absurdly extravagant that it could only be viewed as a monstrous joke."),
279: ("정부가 가장 저열한 국민적 반감과 공포심을 자극하여 인기를 얻으려는 이 시도에서 실패한다면 그것은 정부의 약점을 드러내는 꼴이 될 것이며, 그렇기에 검찰총장(Mr. Attorney-General)이 이 사건을 최대한 이용했다는 사실도 폭로했다.", "He revealed that if the government failed in this attempt to gain popularity by exploiting the basest national prejudices and fears, it would be seen as a weakness, which is why the Attorney-General had made the most of it."),
280: ("그럼에도 불구하고, 이 사건은 영국의 국사범 재판(State Trials)에서 흔히 볼 수 있으며 이런 사건들을 종종 흉하게 만드는 비열하고 악명 높은 성격의 증거 말고는 아무런 근거가 없다는 점을 강조했다.", "Nevertheless, he emphasized that the case rested on absolutely nothing except the vile and infamous type of evidence that too often marred such cases, and of which the State Trials of this country were completely full."),
281: ("그러나 바로 그 순간, 판사(my Lord)가 (마치 그것이 사실이 아니라는 듯 심각한 표정을 지으며) 법관석(that Bench)에 앉아서 그런 암시를 묵과할 수는 없다고 개입했다.", "But at that moment, the judge intervened (with as serious a face as if it were not true), stating that he could not sit on the bench and tolerate such insinuations."),
282: ("그러자 Stryver 씨는 몇 안 되는 자신의 증인들을 불렀고,", "Then Mr. Stryver called his few witnesses, and"),
283: ("Cruncher 씨는 다음으로 검찰총장이 Stryver 씨가 배심원들에게 입혀놓은 그 옷 전체를,", "Mr. Cruncher next had to pay attention as the Attorney-General turned the entire suit of clothes Mr."),
284: ("뒤집어엎어 놓는 과정을 지켜보아야 했다.", "Stryver had fitted onto the jury completely inside out."),
285: ("검찰총장은 Barsad와 Cly가 배심원들이 생각했던 것보다 백 배는 더 훌륭한 사람들이며, 죄수는 백 배는 더 악랄한 인간이라는 것을 보여주었다.", "He showed how Barsad and Cly were a hundred times better than previously thought, and the prisoner a hundred times worse."),
286: ("마지막으로 판사가 직접 나서서 그 옷을 뒤집었다 엎었다 했지만, 전체적으로는 그 옷을 죄수를 위한 수의(grave-clothes)로 확실하게 다듬고 모양을 잡았다.", "Finally, the judge himself took over, turning the suit of clothes inside out and then outside in, but overall decisively trimming and shaping them into burial clothes for the prisoner."),
287: ("이제 배심원들이 평결을 내리기 위해 돌아서자, 거대한 파리 떼가 다시 몰려들었다. (역주: 파리 떼는 재판 구경꾼들을 의미함)", "Now the jury turned to deliberate, and the swarm of great flies gathered once more."),
288: ("오랫동안 법정의 천장만 응시하며 앉아 있던 Carton(칼튼) 씨는 이 흥분된 분위기 속에서도 자리나 자세를 전혀 바꾸지 않았다.", "Mr. Carton, who had sat for so long looking at the courtroom ceiling, changed neither his position nor his posture, even amid this excitement."),
289: ("그의 박식한 동료 Stryver 씨가 자기 앞의 서류들을 모아 정리하며 주변에 앉은 사람들과 귓속말을 나누고, 이따금 배심원석을 불안하게 힐끗거리는 동안에도,", "While his learned colleague, Mr. Stryver, gathered his papers, whispered with those sitting nearby, and occasionally cast anxious glances at the jury,"),
290: ("또한 모든 구경꾼들이 다소 움직이며 새롭게 무리를 짓는 동안에도,", "while all the spectators shifted around to some degree and formed new groups,"),
291: ("심지어 판사 본인조차 자리에서 일어나 단상을 천천히 왔다 갔다 하며 방청객들로 하여금 그가 열에 들뜬 상태가 아닌가 하는 의심을 품게 만드는 동안에도,", "and even while the judge himself rose from his seat and slowly paced up and down his platform—raising suspicions among the audience that he was in a feverish state—"),
292: ("이 남자만은 찢어진 법복을 반쯤 걸친 채 뒤로 기대어 앉아 있었다. 한번 벗었다가 대충 얹어 놓은 듯 헝클어진 가발을 쓴 채, 두 손은 주머니에 찔러 넣고 종일 그랬던 것처럼 눈은 천장을 향하고 있었다.", "this single man sat leaning back, with his torn gown half falling off. His messy wig was perched on his head just as it had landed after being taken off, his hands were shoved in his pockets, and his eyes remained fixed on the ceiling, just as they had been all day."),
293: ("그의 태도에 묻어나는 특유의 무모함은 그를 불량해 보이게 만들었을 뿐만 아니라, 그가 죄수와 틀림없이 닮았다는 인상마저 크게 반감시켰다. (두 사람을 비교했을 때 그가 잠깐 보여준 진지함이 그 닮은꼴을 강화했었음에도 불구하고 말이다.) 그래서 지금 그를 유심히 살펴보던 많은 구경꾼들은 두 사람이 그렇게 닮았다고는 생각조차 못 하겠다고 서로 수군거렸다.", "A particular recklessness in his manner not only gave him a disreputable appearance but also so greatly diminished the strong resemblance he certainly shared with the prisoner (a resemblance that his brief moment of seriousness during their comparison had heightened). As a result, many of the onlookers who observed him now murmured to one another that they could hardly believe the two men looked so alike."),
294: ("Cruncher 씨는 옆 사람에게 그렇게 평하며 덧붙였다. \"내 반 기니(half a guinea, 영국 옛 화폐)를 걸고 장담하는데, 저 양반은 법률 일거리를 전혀 받지 못할 거요.\"", "Mr. Cruncher shared this observation with his neighbor and added, \"I'd bet half a guinea that he doesn't get any legal work to do.\""),
295: ("\"일거리를 받을 만한 사람처럼 보이지는 않잖아, 안 그래요?\"", "\"He doesn't look like the kind of person who would get any, does he?\""),
296: ("하지만 이 Carton 씨는 겉보기보다 이 현장의 세부적인 상황을 훨씬 더 많이 파악하고 있었다.", "Yet, this Mr. Carton was observing far more details of the scene than he appeared to be."),
297: ("왜냐하면 지금, Manette(마네뜨) 양의 고개가 아버지의 가슴 위로 툭 떨쳐졌을 때, 그것을 가장 먼저 발견하고 큰 소리로 외친 사람이 바로 그였기 때문이다.", "For right now, when Miss Manette's head dropped onto her father's chest, he was the very first to notice it and speak up loud enough to be heard:"),
298: ("\"경관님! 저 젊은 숙녀분을 좀 보시오.\"", "\"Officer! Check on that young lady.\""),
299: ("\"저 신사분이 아가씨를 밖으로 모시고 나가는 것을 도와주시오.\"", "\"Help the gentleman escort her out.\""),
300: ("\"쓰러지려는 게 안 보이오!\"", "\"Can't you see she is about to fall!\""),
301: ("그녀가 밖으로 실려 나갈 때 사람들은 그녀를 깊이 동정했고, 그녀의 아버지에게도 큰 연민을 표했다.", "There was a great deal of pity for her as she was carried out, and much sympathy for her father."),
302: ("감옥에 갇혀 있던 시절이 다시 언급되는 것은 분명 그에게 크나큰 고통이었을 것이다.", "Having the days of his imprisonment brought up again had clearly been a source of great distress to him."),
303: ("그는 심문을 받을 때 내면의 강한 동요를 보였으며, 그를 늙어 보이게 하는 그 깊이 생각에 잠기거나 우울한 표정이 그 이후로 줄곧 짙은 먹구름처럼 그에게 드리워져 있었다.", "He had displayed intense internal agitation when questioned, and the thoughtful, brooding look that aged him had hung over him like a heavy cloud ever since."),
304: ("그가 밖으로 나갈 때, 잠시 걸음을 멈추고 돌아선 배심원들이 배심원장을 통해 입을 열었다.", "As he exited, the jury, who had turned back and paused for a moment, spoke up through their foreman."),
305: ("그들은 합의에 이르지 못하여, 따로 모여서 회의하기를 원했다.", "They had not reached an agreement and wished to retire to deliberate."),
306: ("판사는 (아마도 조지 워싱턴을 염두에 두고 있었는지) 그들이 합의하지 못했다는 사실에 약간 놀란 기색을 보였으나, 감시 하에 회의실로 물러나는 것을 허락한다는 뜻을 내비치고는 자신도 퇴장했다.", "The judge (perhaps thinking of George Washington) showed slight surprise that they had not agreed, but indicated his approval for them to retire under guard, and then he left the courtroom as well."),
307: ("재판은 하루 종일 이어졌고, 이제 법정에 램프 불이 켜지고 있었다.", "The trial had gone on all day, and the lamps in the courtroom were now being lit."),
308: ("배심원들의 회의가 길어질 것이라는 소문이 돌기 시작했다.", "Rumors began to circulate that the jury would be out deliberating for a long time."),
309: ("구경꾼들은 요기를 하려고 자리를 떴고, 죄수는 피고석 뒤쪽으로 물러나 앉았다.", "The spectators left to get some food and drink, and the prisoner retreated to the back of the dock and sat down."),
310: ("젊은 숙녀와 그녀의 아버지가 나갈 때 함께 따라 나갔던 Lorry(로리) 씨가 이제 다시 나타나서 Jerry(제리)에게 손짓했다.", "Mr. Lorry, who had left when the young lady and her father went out, now reappeared and gestured to Jerry."),
311: ("재판에 대한 관심이 느슨해진 틈을 타서 제리는 쉽게 그에게 다가갈 수 있었다.", "Taking advantage of the relaxed attention in the room, Jerry was easily able to get close to him."),
312: ("\"Jerry, 뭐 좀 먹고 싶으면 가서 먹고 오게.\"", "\"Jerry, if you'd like to get something to eat, you may go.\""),
313: ("\"하지만 금방 올 수 있게 근처에 있어야 해.\"", "\"But make sure you stay nearby.\""),
314: ("\"배심원들이 돌아오면 틀림없이 소식을 들을 수 있을 거야.\"", "\"You'll definitely hear when the jury returns.\""),
315: ("\"그들보다 한순간도 늦어서는 안 되네. 자네가 그 평결 결과를 은행으로 가져가야 하니까.\"", "\"Don't be a second late behind them, because I need you to carry the verdict back to the bank.\""),
316: ("\"자네는 내가 아는 가장 빠른 심부름꾼이니, 나보다 훨씬 먼저 템플 바(Temple Bar)에 도착할 수 있을 걸세.\"", "\"You're the fastest messenger I know, and you'll reach Temple Bar much sooner than I could.\""),
317: ("제리는 주먹 쥔 손을 갖다 댈 이마가 겨우 조금 남아 있었는데, 그는 이 지시와 함께 받은 1실링 동전에 대한 감사의 표시로 자기 이마에 주먹을 갖다 댔다. (역주: 영국 노동자 계층의 인사법)", "Jerry had just enough forehead to touch with his knuckle, and he did so in acknowledgment of the instruction and the shilling he received."),
318: ("바로 그 순간 Carton 씨가 다가와 Lorry 씨의 어깨를 툭 쳤다.", "Just then, Mr. Carton walked up and tapped Mr. Lorry."),
320: ("\"그 젊은 숙녀분은 좀 어떻습니까?\"", "\"How is the young lady doing?\""),
321: ("\"그녀는 몹시 괴로워하고 있습니다.\"", "\"She is extremely distressed;\""),
322: ("\"하지만 아버지가 그녀를 위로하고 있고, 법정 밖으로 나가서 그나마 좀 나아졌습니다.\"", "\"But her father is comforting her, and she feels better now that she is out of the courtroom.\""),
323: ("\"죄수에게 그렇게 전하죠.\"", "\"I will tell the prisoner.\""),
324: ("\"당신처럼 훌륭한 은행 신사가 공개적으로 죄수와 말을 섞는 모습이 남들에게 띄면 곤란할 테니까요, 안 그렇습니까.\"", "\"It wouldn't do for a respectable bank gentleman like you to be seen talking to him in public, you know.\""),
325: ("Lorry 씨는 마치 속으로 그 문제를 저울질하고 있었던 것을 들키기라도 한 것처럼 얼굴이 붉어졌고,", "Mr. Lorry turned red as if he realized he had been debating that very point in his mind, and Mr."),
326: ("Carton 씨는 변호사석(bar) 바깥쪽으로 발걸음을 옮겼다.", "Carton made his way out of the lawyers' section."),
327: ("법정 밖으로 나가는 길이 그 방향이었으므로, 제리는 눈과 귀를 번쩍이고 삐죽 솟은 머리카락을 세운 채 그를 뒤따랐다.", "The exit from the court was in that direction, so Jerry followed him, completely alert with his eyes, ears, and spiky hair."),
328: ("\"Darnay(다네이) 씨!\"", "\"Mr. Darnay!\""),
329: ("죄수는 즉시 앞으로 나왔다.", "The prisoner stepped forward immediately."),
330: ("\"당연히 증인으로 나섰던 Manette 양의 소식이 궁금하실 겁니다.\"", "\"You must naturally be anxious to hear about the witness, Miss Manette.\""),
331: ("\"그녀는 괜찮아질 겁니다.\"", "\"She will be just fine.\""),
332: ("\"당신은 그녀가 가장 불안해하던 고비를 넘긴 모습을 보셨으니까요.\"", "\"You have already seen the worst of her distress.\""),
333: ("\"제가 그 원인이 된 것에 깊이 사과드립니다.\"", "\"I am deeply sorry to have caused it.\""),
334: ("\"제 진심 어린 감사의 마음과 함께, 그녀에게 그렇게 전해 주실 수 있겠습니까?\"", "\"Could you please pass that on to her for me, along with my deepest gratitude?\""),
335: ("\"네, 전해드리죠.\"", "\"Yes, I can.\""),
336: ("\"부탁하신다면 그렇게 하겠습니다.\"", "\"I will do so, since you ask.\""),
337: ("Carton 씨의 태도는 거의 무례할 정도로 무심했다.", "Mr. Carton's manner was so careless that it bordered on insolence."),
338: ("그는 죄수를 반쯤 등진 채로, 팔꿈치를 나무 난간에 기대고 비스듬히 서 있었다.", "He stood half-turned away from the prisoner, leaning lazily with his elbow on the railing."),
339: ("\"부탁드립니다.\"", "\"I do ask it of you.\""),
340: ("\"제 진심 어린 감사를 받아주십시오.\"", "\"Please accept my sincere thanks.\""),
341: ("\"그래,\" Carton은 여전히 그를 반쯤만 쳐다본 채 말했다. \"무엇을 예상하고 있소, Darnay 씨?\"", "\"What,\" said Carton, still only half-facing him, \"do you expect will happen, Mr. Darnay?\""),
342: ("\"최악의 상황이겠죠.\"", "\"The worst.\""),
343: ("\"그게 가장 현명한 예상이자 가장 가능성 높은 결과요.\"", "\"That's the wisest thing to expect, and the most likely.\""),
344: ("\"하지만 배심원들이 따로 물러나서 회의하는 것은 당신에게 유리하게 작용할 것 같소.\"", "\"But I think the fact that they withdrew to deliberate works in your favor.\""),
345: ("법정 밖으로 나가는 길에 서성거리는 것이 금지되어 있었기 때문에, 제리는 더 이상 듣지 못했다.", "Since loitering on the way out of the courtroom was not permitted, Jerry didn't hear anything else."),
346: ("그러나 그는 생김새는 너무도 닮았지만 태도는 너무나도 다른 그 두 사람이 나란히 서서 머리 위의 거울에 비친 모습을 뒤로한 채 그곳을 떠났다.", "Instead, he left them standing side by side—so identical in their physical features, yet so completely different in their manners—both of their reflections visible in the glass above them."),
347: ("비록 양고기 파이와 에일 맥주로 달래긴 했지만, 도둑과 악당들로 득실거리는 아래층 복도에서 한 시간 반이라는 시간은 무겁게 절뚝거리며 지나갔다.", "An hour and a half dragged by heavily in the hallways below, crowded with thieves and rascals, even though the wait was somewhat eased by mutton pies and ale."),
348: ("목이 쉰 그 심부름꾼은 요기를 마친 후 긴 의자에 불편하게 앉아 꾸벅꾸벅 졸고 있다가, 큰 웅성거림과 함께 법정으로 이어지는 계단으로 몰려드는 사람들의 빠른 물결에 휩쓸려 따라 올라갔다.", "The hoarse messenger, who had fallen into a doze while sitting uncomfortably on a bench after his meal, was swept along when a loud murmur and a fast-moving crowd of people surged up the stairs leading to the courtroom."),
349: ("\"Jerry!\"", "\"Jerry!\""),
350: ("\"Jerry!\" 그가 도착했을 때 Lorry 씨는 이미 문가에서 부르고 있었다.", "\"Jerry!\" Mr. Lorry was already calling out at the door by the time he got there."),
351: ("\"여기 있습니다, 나리!\"", "\"Here I am, sir!\""),
352: ("\"다시 돌아오느라 한바탕 전쟁을 치렀습니다.\"", "\"It was a struggle to get back in.\""),
353: ("\"저 여기 있습니다, 나리!\"", "\"I'm right here, sir!\""),
354: ("Lorry 씨는 인파 속에서 그에게 쪽지 하나를 건네주었다. \"빨리!\"", "Mr. Lorry handed him a piece of paper through the crowd. \"Quick!\""),
355: ("받았나?\"", "\"Do you have it?\""),
356: ("\"네, 나리.\"", "\"Yes, sir.\""),
357: ("그 쪽지에는 '무죄 방면(ACQUITTED).'이라는 단어가 급하게 휘갈겨 쓰여 있었다.", "Scrawled hastily on the paper was a single word: \"ACQUITTED.\""),
358: ("\"만약 나리가 또다시 '생환(Recalled to Life)'이라는 메시지를 보내셨더라면,\" 제리는 몸을 돌리며 중얼거렸다. \"이번에는 그게 무슨 뜻인지 알았을 텐데 말이야.\"", "\"If you had sent the message 'Recalled to Life' again,\" Jerry muttered as he turned around, \"I would have known exactly what you meant this time.\""),
359: ("그는 올드 베일리(Old Bailey) 재판소를 완전히 빠져나올 때까지는 다른 어떤 말도 할 기회가 없었고, 심지어 생각할 겨를조차 없었다.", "He had no chance to say, or even think, anything else until he was completely clear of the Old Bailey."),
360: ("왜냐하면 사람들이 그를 다리가 풀려 넘어질 만큼 격렬하게 쏟아져 나왔고, 마치 허탕을 친 쉬파리 떼가 다른 썩은 고기를 찾아 흩어지는 것처럼 웅성거리는 큰 소음이 거리를 휩쓸었기 때문이다.", "This was because the crowd came pouring out with such force that it nearly swept him off his feet, and a loud buzzing noise filled the street, much like frustrated blowflies scattering to find another piece of rotting meat.")
}

book_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_03.json'
with open(book_path, 'r', encoding='utf-8') as f:
    book_data = json.load(f)

for block in book_data:
    block_id = block.get("id")
    if block_id in updates:
        ko_text, en_text = updates[block_id]
        if block.get("is_header"):
            block["ko"] = ko_text
            block["en"] = ""
        else:
            block["ko"] = ko_text
            block["en"] = en_text

with open(book_path, 'w', encoding='utf-8') as f:
    json.dump(book_data, f, indent=2, ensure_ascii=False)
