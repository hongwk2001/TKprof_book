import sys

ko_text = '''토머스 부부가 이 농담에 호탕하게 웃는 모습을 보니, 이 농담이 전에도 꽤 써먹었던 것 같고, 이 장황한 설명 전체가 그저 공들인 사기극에 불과하다는 것을 알 수 있었습니다. 저는 훌륭한 토머스 씨와 농담 따먹기로는 겨룰 수가 없었지만, 그의 마음을 여는 더 확실한 방법을 알고 있다고 생각해서 이렇게 말했습니다.—

"자, 빌더 씨, 처음에 드린 반 소버린짜리 금화는 밥값을 다 했다고 칩시다. 선생님께서 앞으로 어떻게 될 것 같은지 말씀해 주시면, 이 두 번째 금화도 주인을 찾아가게 될 겁니다."

"알겠습니다, 선생님," 그가 재빠르게 대답했습니다. "제가 농담을 한 건 이해해 주시리라 믿습니다. 제 아내가 저에게 눈찡긋을 했는데, 그건 계속하라는 신호였거든요."

"어머나, 내가 언제!" 늙은 부인이 말했습니다.

"제 생각은 이렇습니다. 그 늑대는 지금 어딘가에 숨어 있을 겁니다. 아무것도 기억하지 못하던 정원사는 그 늑대가 말보다 더 빨리 북쪽으로 질주하고 있었다고 말했지만, 저는 그 말을 믿지 않습니다. 왜냐하면 선생님도 아시다시피 늑대도 개와 마찬가지로 질주할 수 없거든요. 신체 구조상 그렇게 뛰지 못합니다. 늑대는 이야기책에서나 멋진 동물이죠. 저는 무리를 지어서 자기들보다 더 겁 많은 먹잇감을 쫓아갈 때는 끔찍한 소리를 내며 갈기갈기 찢어놓을 수 있다는 건 인정합니다. 하지만 맙소사, 현실에서 늑대는 하찮은 동물에 불과합니다. 훌륭한 개보다 절반도 똑똑하거나 용감하지 않고, 싸움 실력도 개의 4분의 1조차 안 되거든요. 이 늑대는 싸움은 고사하고 스스로 먹이를 구하는 것조차 익숙하지 않습니다. 십중팔구 공원 주변 어딘가에 숨어서 벌벌 떨고 있을 테고, 만약 생각이란 걸 할 줄 안다면 아침을 어디서 구해야 할지 궁금해하고 있을 겁니다. 어쩌면 어떤 집 지하 통로로 내려가 석탄 창고에 틀어박혀 있을지도 모르죠. 세상에, 어둠 속에서 녹색 눈을 번뜩이는 녀석을 본 요리사가 얼마나 기겁을 할까요! 먹이를 구하지 못하면 어떻게든 찾아 나서야 할 테니, 운이 좋으면 일찌감치 정육점을 발견할지도 모릅니다. 그렇지 못할 경우 유모가 유모차에 아기를 둔 채 군인과 산책하러 가버린다면—음, 그러면 인구 조사에서 아기 한 명이 줄어든다고 해도 저는 놀라지 않을 겁니다. 그게 다입니다."

제가 그에게 반 소버린짜리 금화를 건네주려던 참에 창문에 무언가 툭 하고 부딪혔고, 빌더 씨의 얼굴은 놀라움으로 평소보다 두 배나 길어졌습니다.

"맙소사!" 그가 말했습니다. "늙은 베르시커가 제 발로 돌아왔잖아!"

그는 문으로 가서 문을 열었습니다. 저로서는 아주 쓸데없는 행동처럼 보였습니다. 저는 야생 동물이란 우리 사이에 확실히 튼튼한 장애물이 있을 때 가장 보기 좋다고 항상 생각해왔는데, 개인적인 경험이 그 생각을 약화시키기는커녕 오히려 강화해주었기 때문입니다.

그러나 결국 습관만 한 것이 없는지, 빌더 씨나 그의 아내는 제가 개를 대하는 것보다도 그 늑대를 더 무서워하지 않았습니다. 동물 자체는, 빨간 모자의 옛 친구였던 그 그림책 늑대들의 조상이 위장을 하고서 소녀의 환심을 샀던 것처럼(동화 '빨간 모자'에서 늑대가 할머니로 변장했던 것을 의미) 얌전하고 말도 잘 들었습니다.

이 모든 광경은 희극과 비애가 뒤섞인, 이루 말할 수 없는 장면이었습니다. 반나절 동안 런던을 마비시키고 동네의 모든 아이들을 공포에 떨게 했던 그 사악한 늑대가 일종의 회개하는 태도로 그곳에 있었고, 탕아처럼 대접받으며 사랑을 받았습니다. 늙은 빌더 씨는 가장 다정한 배려로 그 녀석의 온몸을 살펴보았고, 회개한 늑대를 다 살핀 후 이렇게 말했습니다.—

"거봐, 불쌍한 이 녀석이 무슨 문제에 휘말릴 줄 알았다니까. 내가 내내 그렇게 말하지 않았나? 머리가 다 베이고 깨진 유리조각투성이군. 빌어먹을 담벼락 같은 걸 넘으려고 했던 게 틀림없어. 사람들이 담장 위에 깨진 병을 올려놓게 내버려 두다니 정말 부끄러운 일이야. 그게 다 이것 때문이라고. 이리 와, 베르시커."

그는 늑대를 데려가 우리에 가두고서 고기 한 덩어리를 던져주었는데, 적어도 양으로 따지면 (성서에 나오는) '살진 송아지'의 기본 조건은 충족시켰습니다. 그러고 나서 그는 보고를 하러 자리를 떴습니다.

저 역시 동물원에서 벌어진 이 기묘한 탈주극에 대해 오늘 단독으로 제공되는 이 정보를 기사로 쓰기 위해 발걸음을 돌렸습니다.

수어드 박사의 일기.

9월 17일.—저녁 식사 후 서재에서 장부 정리를 하고 있었습니다. 다른 업무가 밀린 데다 루시에게 여러 번 다녀오느라 장부 정리가 몹시 밀려 있었습니다. 갑자기 문이 벌컥 열리더니 분노로 얼굴이 일그러진 내 환자가 뛰어 들어왔습니다. 환자가 제 발로 원장의 서재에 들어오는 일은 거의 전례가 없는 일이라 저는 깜짝 놀랐습니다. 그는 단 한순간도 지체하지 않고 나에게 곧장 달려들었습니다. 그는 손에 저녁 식사용 칼을 쥐고 있었고, 그가 위험하다는 것을 직감한 저는 책상을 사이에 두고 거리를 유지하려 했습니다. 하지만 그는 나보다 너무 빠르고 힘이 셌습니다. 미처 중심을 잡기도 전에 그가 나를 찔렀고 내 왼쪽 손목을 꽤 심하게 베였습니다. 그러나 그가 다시 공격하기 전에 내 오른주먹이 먼저 꽂혔고, 그는 바닥에 등을 대고 대자로 뻗었습니다. 내 손목에서는 피가 콸콸 쏟아져 양탄자 위로 피가 조금 고일 정도였습니다. 나는 그 친구가 더 이상 공격할 의사가 없다는 것을 확인하고, 줄곧 쓰러진 그를 경계하며 내 손목을 지혈하는 데 집중했습니다. 간호인들이 뛰어 들어와 그에게 주의를 돌렸을 때, 그가 하고 있던 행동을 본 나는 구역질이 날 뻔했습니다. 그는 바닥에 엎드린 채, 내 상처 난 손목에서 떨어진 피를 개처럼 핥아먹고 있었습니다. 그는 쉽게 제압되었고, 놀랍게도 그저 "피는 생명이다! 피는 생명이다!"라는 말만 계속 되풀이하며 간호인들을 아주 얌전하게 따라갔습니다.

지금은 피를 잃어서는 안 되는 상황입니다. 최근 들어 내 육체적인 건강을 위해 너무 많은 피를 잃었고, 게다가 루시의 병과 그 끔찍한 국면들로 인한 기나긴 긴장감이 나를 갉아먹고 있습니다. 나는 몹시 흥분하고 지쳐 있어서 휴식이, 휴식이, 절대적인 휴식이 필요합니다. 다행히 반 헬싱이 나를 부르지 않았으니, 잠을 거를 필요는 없습니다. 오늘 밤은 푹 자야겠습니다.

전보, 안트베르펜에서 반 헬싱이 팩스의 수어드에게.

(주가 적혀 있지 않아 서식스주 팩스로 보내짐; 22시간 늦게 배달됨.)

"9월 17일.—오늘 밤 반드시 힐링엄에 가도록. 만약 계속 지켜보지 않는다면 자주 방문하여 꽃들이 제자리에 있는지 확인할 것. 아주 중요함. 반드시 해야 함. 도착하는 대로 최대한 빨리 자네에게 가겠음."

수어드 박사의 일기.

9월 18일.—런던행 기차에 막 올라탔습니다. 반 헬싱의 전보가 도착하자 나는 경악을 금치 못했습니다. 하룻밤을 통째로 허비했고, 하룻밤 사이에 무슨 일이 일어날 수 있는지 뼈저린 경험으로 알고 있기 때문입니다. 물론 아무 일도 없을 수도 있지만, 무슨 일이 일어났을지도 모릅니다. 우리가 하려는 모든 일을 훼방 놓는, 상상할 수 있는 모든 사고가 일어나는 것을 보니, 틀림없이 우리 머리 위에 어떤 끔찍한 파멸이 도사리고 있는 것 같습니다. 이 실린더를 챙겨 가서, 루시의 축음기 소리를 듣고 제 기록을 마무리해야겠습니다.

루시 웨스텐라가 남긴 기록.

9월 17일. 밤.—행여나 나 때문에 누구라도 곤경에 처하는 일이 없도록 이 글을 써서 남깁니다. 이것은 오늘 밤 일어난 일에 대한 정확한 기록입니다. 기력이 다해 죽어가는 것이 느껴지고 글을 쓸 힘조차 간신히 남아 있지만, 글을 쓰다가 죽는 한이 있더라도 이 일은 해야만 합니다.

나는 반 헬싱 박사님이 지시하신 대로 꽃들이 제자리에 놓였는지 확인하고 평소처럼 잠자리에 들었고 곧 잠이 들었습니다.

나는 창문에서 나는 파닥거리는 소리에 잠에서 깼습니다. 휘트비 절벽에서 몽유병으로 헤매다가 미나가 나를 구해주었던 그날 이후로 시작되었고 이제는 너무나 익숙해진 그 소리였습니다. 무섭지는 않았지만, 반 헬싱 박사님 말씀대로 수어드 박사님이 옆방에 계셔서 내가 부를 수 있었다면 좋았을 텐데 하고 바랐습니다. 다시 잠을 청하려 했지만 잠이 오지 않았습니다. 그러자 예전처럼 수면에 대한 두려움이 밀려왔고, 나는 계속 깨어 있기로 마음먹었습니다. 반대로 내가 원하지 않자 잠이 쏟아지려 했습니다. 혼자 있는 것이 무서워진 나는 방문을 열고 소리쳤습니다. "거기 누구 없나요?" 아무 대답이 없었습니다. 어머니를 깨우기가 겁나서 나는 다시 방문을 닫았습니다. 그때 밖의 관목 숲에서 개 짖는 소리 같지만 더 사납고 깊은 어떤 울부짖음이 들렸습니다. 나는 창가로 가서 밖을 내다보았지만, 창문에 날개를 펄럭이던 커다란 박쥐 한 마리 말고는 아무것도 볼 수 없었습니다. 그래서 나는 다시 침대로 돌아갔지만 잠들지 않기로 결심했습니다. 이윽고 문이 열리고 어머니가 안을 들여다보셨습니다. 내가 뒤척이는 것을 보고 내가 깨어 있는 것을 아신 어머니는 안으로 들어와 내 곁에 앉으셨습니다. 어머니는 평소보다 더 상냥하고 부드럽게 내게 말씀하셨습니다.—

"네가 걱정되어서 잘 있는지 보러 왔단다, 아가."

나는 어머니가 거기 앉아 계시다가 감기에 걸리실까 봐 걱정되어 침대로 들어와 같이 자자고 부탁했습니다. 어머니는 내 옆에 누우셨지만 잠옷을 벗지는 않으셨습니다. 잠시 머물다 자기 방으로 돌아가겠다고 하셨기 때문입니다. 어머니가 내 품에 안겨 있고 나도 어머니 품에 안겨 있을 때, 또다시 창문에서 파닥거리며 두드리는 소리가 났습니다. 어머니는 깜짝 놀라 조금 겁에 질린 목소리로 소리쳤습니다. "저게 무슨 소리니?" 나는 어머니를 진정시키려 애썼고 마침내 성공하여 어머니는 조용히 누워 계셨습니다. 하지만 나는 어머니의 가여운 심장이 여전히 끔찍하게 뛰고 있는 것을 들을 수 있었습니다. 잠시 후 관목 숲에서 다시 낮게 울부짖는 소리가 들렸고, 곧이어 창문에서 쨍그랑하는 소리가 나더니 수많은 유리 파편들이 바닥으로 쏟아졌습니다. 밀려드는 바람에 블라인드가 뒤로 날렸고, 깨진 유리창 틈새로 삐쩍 마른 커다란 회색 늑대 머리가 나타났습니다. 어머니는 기겁하며 비명을 지르셨고, 상체를 일으켜 앉으려고 버둥거리며 몸을 지탱할 수 있는 것이라면 무엇이든 다급하게 움켜쥐셨습니다. 그러다 반 헬싱 박사님이 내 목에 꼭 걸고 있어야 한다고 신신당부하셨던 그 화관을 움켜쥐고는 내게서 뜯어내셨습니다. 일 이 초 동안 어머니는 늑대를 가리킨 채 앉아 계셨고, 어머니의 목구멍에서는 이상하고 끔찍하게 꿀럭거리는 소리가 났습니다. 그러더니 어머니는 번개에라도 맞은 듯 픽 쓰러지셨고, 어머니의 머리가 내 이마에 부딪히면서 나는 잠시 동안 어지러웠습니다. 방과 주변의 모든 것이 빙빙 도는 것 같았습니다. 나는 시선을 창문에 고정하고 있었는데, 늑대는 머리를 뺐고, 무수히 많은 작은 먼지 알갱이들이 깨진 창문을 통해 바람을 타고 들어와 사막의 모래폭풍 때 여행자들이 묘사하는 먼지 기둥처럼 빙글빙글 소용돌이치는 것 같았습니다. 몸을 움직이려 했지만 어떤 주문에 걸린 듯했고, 심장이 멈춰버려 이미 차갑게 식어가는 듯한 어머니의 불쌍한 몸뚱이가 나를 짓눌렀습니다. 그리고 한동안 나는 아무것도 기억하지 못했습니다.

다시 의식을 되찾을 때까지 시간은 그리 길지 않았던 것 같지만, 너무나 끔찍했습니다. 어디선가 누군가의 죽음을 알리는 종소리가 울리고 있었고, 동네 개들이 사방에서 울부짖고 있었으며, 우리 집 관목 숲에서는, 마치 바로 밖인 것처럼 나이팅게일이 노래하고 있었습니다. 고통과 공포, 그리고 기진맥진함으로 정신이 멍하고 둔해졌지만, 나이팅게일 소리는 마치 죽은 어머니의 목소리가 나를 위로하러 돌아온 것 같았습니다. 그 소리에 하녀들도 깬 것인지 내 방문 밖에서 맨발로 종종걸음 치는 소리가 들렸습니다. 내가 부르자 그들이 들어왔고, 무슨 일이 일어났는지, 침대 위에 나를 덮치고 있는 것이 무엇인지 보고는 비명을 질렀습니다. 깨진 창문으로 바람이 불어닥쳤고, 방문이 쾅 하고 닫혔습니다. 그들은 사랑하는 어머니의 시신을 들어 올려 내 몸에서 떼어냈고, 내가 일어난 뒤 시신을 천으로 덮어 침대 위에 뉘었습니다. 모두들 너무 겁에 질려 불안해하길래, 나는 그들에게 식당으로 가서 와인을 한 잔씩 마시라고 지시했습니다. 문이 순식간에 활짝 열렸다가 다시 닫혔습니다. 하녀들은 비명을 지르더니 모두 함께 식당으로 갔고, 나는 가지고 있던 꽃들을 사랑하는 어머니의 가슴 위에 올려놓았습니다. 꽃들을 다 올려놓고 나자 반 헬싱 박사님이 내게 하신 말씀이 떠올랐지만 차마 그 꽃들을 치울 수는 없었고, 게다가 이제는 하녀 중 몇 명을 내 곁에 앉혀두고 싶었습니다. 하녀들이 돌아오지 않는 것이 이상했습니다. 불렀지만 아무 대답이 없어서 나는 하녀들을 찾으러 식당으로 갔습니다.

무슨 일이 벌어졌는지 본 순간 나는 가슴이 철렁 내려앉았습니다. 네 명 모두 바닥에 무방비 상태로 누워 거칠게 숨을 몰아쉬고 있었습니다. 셰리주 병은 탁자 위에 반쯤 차 있었지만, 이상하고 톡 쏘는 냄새가 났습니다. 수상한 생각이 들어 술병을 살펴보았습니다. 아편 냄새가 났고, 찬장을 보니 어머니 주치의가 처방했던—오! 처방했었던—약병이 비어 있는 것을 발견했습니다. 어쩌면 좋단 말인가? 어떻게 해야 하나? 나는 다시 어머니가 계신 방으로 돌아왔습니다. 누군가 수면제를 먹여 잠든 하녀들 말고는 혼자인 나는 어머니 곁을 떠날 수가 없습니다. 시체와 단둘이 남겨지다니! 깨진 창문 너머로 늑대의 낮게 우는 소리가 들려 감히 밖으로 나갈 엄두도 나지 않습니다.

창문에서 불어오는 바람에 먼지 알갱이들이 떠다니고 소용돌이치며 공기 중에 가득 찬 것 같고, 불빛은 파랗고 희미하게 타오릅니다. 어떻게 해야 하나? 신이여 오늘 밤 나를 해악으로부터 보호해 주소서! 나는 이 종이를 내 품속에 숨길 것이고, 나를 묻어주러 올 때 사람들이 이 종이를 발견하게 될 것입니다. 사랑하는 어머니가 돌아가시다니! 나도 이제 가야 할 시간인가 봅니다. 오늘 밤을 넘기지 못한다면 안녕, 사랑하는 아서. 신의 가호가 당신과 함께하길, 내 사랑, 그리고 신이여 나를 도우소서!
'''

en_text = '''From the hearty way that both Thomas and his wife laughed at the joke, I could tell it had been used before and that his entire long-winded explanation was just an elaborate setup. I couldn't compete with the good Thomas in bantering, but I thought I knew a better way to win him over, so I said:—

"Now, Mr. Bilder, let's consider that first half-sovereign fully earned. Once you tell me what you think will happen next, this other coin will be waiting for you."

"Right you are, sir," he said eagerly. "I know you'll excuse me for joking around, but my wife here winked at me, which was my cue to keep going."

"Well, I never!" the old lady exclaimed.

"My opinion is this: that wolf is hiding out somewhere right now. That forgetful gardener claimed the wolf was galloping north faster than a horse could run, but I don't believe him. You see, sir, wolves don't gallop any more than dogs do; they just aren't built that way. Wolves are impressive in storybooks, and I admit that when they gather in packs and are chasing something that's more scared than they are, they can make a terrifying noise and tear it to pieces. But good Lord, in real life, a wolf is just a lowly animal, not half as smart or brave as a good dog, and with not even a quarter of the fight in him. This one has never had to fight or even find his own food. Most likely, he's hiding somewhere around the park right now, shivering. If he's thinking at all, he's probably wondering where his breakfast is going to come from, or maybe he crawled down into a basement and is hiding in a coal cellar. Goodness me, some cook is going to get a terrible shock when she sees his green eyes shining at her in the dark! If he can't find food, he'll have to go looking for it, and if he's lucky, he might stumble across a butcher shop early on. If he doesn't, and some nanny wanders off with a soldier, leaving a baby alone in a carriage—well, I wouldn't be surprised if the census count goes down by one baby. That's all there is to it."

I was just handing him the half-sovereign when something suddenly bumped against the window, and Mr. Bilder's face dropped in sheer astonishment.

"God bless me!" he cried. "If it isn't old Bersicker come back on his own!"

He went to the door and opened it—a move that seemed incredibly reckless to me. I've always felt that wild animals are best admired when there's a sturdy, reliable barrier between us, and personal experience has only strengthened that belief.

However, habit is a powerful thing. Neither Bilder nor his wife seemed any more afraid of the wolf than I would be of a dog. The animal itself was as calm and well-behaved as the grandfather of all storybook wolves—Red Riding Hood's old friend, right when he was winning her trust in disguise.

The whole scene was an indescribable mix of comedy and tragedy. The wicked wolf that had paralyzed London for half a day, terrifying every child in the city, was standing there looking almost apologetic. He was welcomed and petted like a prodigal son returning home. Old Bilder carefully examined his entire body with deep concern, and when he was done checking the remorseful wolf, he said:—

"There, I knew the poor old guy would get into some kind of trouble. Didn't I say it all along? Look at his head, it's all cut up and full of broken glass. He must have tried jumping over some bloody wall. It's a shame people are allowed to put broken bottles on top of their walls. This is what happens. Come along, Bersicker."

He led the wolf away, locked him in a cage, and threw him a piece of meat that—at least in size—rivaled the Biblical fatted calf. Then he went off to report the incident.

I also left to file my report, providing the only exclusive information available today about the strange escape at the Zoo.

Dr. Seward’s Diary.

September 17.—After dinner, I was in my study, updating my records, which had fallen severely behind due to the pressure of other work and my frequent visits to Lucy. Suddenly, the door flew open, and my patient burst in, his face twisted in rage. I was completely shocked, because it is almost unheard of for a patient to voluntarily enter the Superintendent’s study. Without a moment's hesitation, he charged straight at me. He was holding a dinner knife, and seeing how dangerous he was, I tried to keep the desk between us. However, he was too fast and too strong. Before I could regain my balance, he lunged at me and slashed my left wrist quite badly. But before he could strike again, I hit him with my right hand, and he collapsed onto his back on the floor. My wrist was bleeding heavily, and a small pool of blood began to form on the carpet. Seeing that my attacker wasn't trying to get back up, I focused on bandaging my wrist while keeping a close eye on his body. When the guards rushed in and we turned our attention to him, what he was doing made me physically sick. He was lying on his stomach, licking up the blood that had dripped from my wrist like a dog. He was easily restrained, and to my surprise, he went with the guards very peacefully, simply repeating over and over: "The blood is the life! The blood is the life!"

I really can't afford to lose any blood right now. I've already lost too much lately for my own health, and the prolonged stress of Lucy’s illness and its terrifying phases is taking a toll on me. I am overstimulated and exhausted, and I desperately need rest. Fortunately, Van Helsing hasn't called for me, so I don't have to skip my sleep; I really couldn't do without it tonight.

Telegram, Van Helsing in Antwerp, to Seward at Carfax.

(Sent to Carfax, Sussex, because no county was specified; arrived twenty-two hours late.)

"September 17.—You must not fail to be at Hillingham tonight. If you are not watching her constantly, you must visit frequently and make sure the flowers are exactly where they should be. This is extremely important; do not fail. I will be with you as soon as possible after I arrive."

Dr. Seward’s Diary.

September 18.—I am just leaving to catch the train to London. Van Helsing’s telegram filled me with dread. An entire night was lost, and I know from bitter experience exactly what can happen in just one night. Of course, everything might be fine, but what could have happened? It truly feels like some horrible curse is hanging over us, ensuring that every possible accident ruins everything we try to do. I am bringing this phonograph cylinder with me so I can finish recording my entry on Lucy’s machine.

Memorandum left by Lucy Westenra.

September 17. Night.—I am writing this down and leaving it to be found so that no one gets into trouble because of me. This is an exact record of what happened tonight. I feel like I am dying from exhaustion and I barely have the strength to write, but I must finish this even if it kills me.

I went to bed as usual, making sure the flowers were placed exactly as Dr. Van Helsing had instructed, and I quickly fell asleep.

I was woken up by a flapping sound at the window—the same sound that started after my sleepwalking incident on the cliff in Whitby when Mina saved me, a sound I now know all too well. I wasn't scared, but I wished Dr. Seward was in the next room, like Dr. Van Helsing promised he would be, so I could call him. I tried to go back to sleep, but I couldn't. Then my old fear of falling asleep returned, and I decided to stay awake. Naturally, sleep then tried to overcome me when I didn't want it to. Feeling frightened to be alone, I opened my door and called out, "Is anybody there?" There was no reply. I was too scared to wake my mother, so I closed the door again. Then, from the bushes outside, I heard a sound like a dog howling, but much fiercer and deeper. I went to the window and looked out, but all I could see was a large bat throwing itself against the glass. I went back to bed, determined to stay awake. Soon after, the door opened, and my mother peeked in. Seeing me moving and realizing I was awake, she came in and sat beside me. She spoke to me even more gently and sweetly than usual:—

"I was worried about you, darling, so I came in to make sure you were alright."

I was worried she might catch a cold sitting there, so I asked her to get into bed and sleep with me. She lay down next to me, still wearing her dressing gown, saying she would only stay for a little while before going back to her own bed. As we lay there holding each other, the flapping and thumping at the window started again. It startled her, and she cried out in fear, "What is that?" I tried to calm her down, and eventually, she lay quietly, but I could hear her poor heart beating frantically. A little while later, the low howl came from the bushes again, followed shortly by a loud crash at the window as shattered glass scattered across the floor. The wind blew the blind back, and through the broken panes, the head of a massive, skinny gray wolf appeared. My mother screamed in terror, struggled to sit up, and desperately grabbed at anything she could reach. During her panic, she grabbed the wreath of garlic flowers that Dr. Van Helsing had insisted I wear and ripped it from my neck. She sat there for a second or two, pointing at the wolf, making a strange, awful gurgling sound in her throat. Then she collapsed—as if she had been struck by lightning—and her head hit my forehead, making me dizzy for a moment. The room and everything in it seemed to spin. I kept my eyes locked on the window; the wolf pulled its head back, and a huge cloud of tiny specks blew in through the broken glass. They swirled and spun around like the massive dust storms travelers describe seeing in the desert. I tried to move, but I felt paralyzed, as if under a spell. My mother’s poor body, which already felt cold as her heart had stopped beating, pinned me down. After that, I blacked out for a while.

It didn't feel like a long time, but it was absolutely terrifying when I finally regained consciousness. A funeral bell was tolling somewhere nearby, dogs were howling all over the neighborhood, and a nightingale was singing in our garden, sounding like it was right outside my window. I was confused and numb from the pain, fear, and weakness, but the nightingale's song felt like my dead mother's voice returning to comfort me. The noise must have woken the maids, because I could hear their bare feet running in the hall. I called out to them, and they came in. When they saw the shattered window and what was lying on top of me on the bed, they screamed. The wind howled through the broken window, slamming the door shut. The maids lifted my mother’s body off me, and after I got up, they laid her back down and covered her with a sheet. They were all so terrified and shaking that I told them to go to the dining room and have a glass of wine to calm their nerves. The door blew open for a second and slammed shut again. The maids shrieked and ran to the dining room together. I took the few flowers I had left and placed them on my mother’s chest. As I laid them there, I remembered what Dr. Van Helsing had told me, but I didn't want to move them. Besides, I planned to have some of the servants stay up and keep me company. I was surprised when the maids didn't return. I called for them but got no answer, so I went to the dining room to find them.

My heart dropped when I saw what had happened. All four of them were lying unconscious on the floor, breathing heavily. The sherry decanter was on the table, half-empty, but there was a strange, bitter smell in the air. Feeling suspicious, I checked the decanter; it smelled like laudanum. Looking at the cabinet, I saw that the medicine bottle my mother's doctor used for her—oh, used to use!—was completely empty. What am I supposed to do? What can I do? I am back in the room with my mother. I can't leave her, and I am entirely alone, except for the drugged servants. Alone with the dead! I am too terrified to go outside because I can hear the wolf howling low through the broken window.

The air feels thick with specks, floating and swirling in the draft from the window, and the lights are burning with a dim, blue glow. What should I do? May God protect me tonight! I will hide this paper in my dress, so they will find it when they come to prepare my body. My dear mother is gone! It must be time for me to go too. Goodbye, dear Arthur, if I don't survive this night. May God protect you, my love, and may God help me!
'''

with open('c:/git_repo/TKprof_book/books/dracula/chapters/ch11_ko_modern.txt', 'a', encoding='utf-8') as f:
    f.write(ko_text)

with open('c:/git_repo/TKprof_book/books/dracula/chapters/ch11_en_modern.txt', 'a', encoding='utf-8') as f:
    f.write(en_text)
