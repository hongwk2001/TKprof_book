import os

ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch09_ko_modern.txt'
en_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch09_en_modern.txt'

ko_content = """
루시 웨스텐라가 미나 하커에게 보낸 편지입니다.

"영국 윗비에서, 8월 30일.

"가장 사랑하는 미나에게,—

"바다만큼 크고 깊은 사랑과 수백만 번의 입맞춤을 보냅니다. 당신이 하루빨리 남편과 함께 두 분만의 보금자리에 정착하기를 바라요. 당신이 이곳 윗비로 일찍 돌아와 우리와 함께 머물 수 있다면 얼마나 좋을까요. 이곳의 강하고 맑은 공기라면 조나단도 금방 건강을 되찾을 거예요. 저도 덕분에 완전히 회복했답니다. 저는 식욕이 왕성해서 엄청나게 잘 먹고, 활기가 넘치며 잠도 푹 자고 있어요. 제가 몽유병 증세를 완전히 극복했다는 소식을 들으면 당신도 무척 기뻐할 거예요. 지난 일주일 동안은 밤에 침대에 눕고 나면 밖으로 단 한 발짝도 나가지 않은 것 같아요. 아서는 제가 살이 찌고 있다고 하네요. 참, 아서가 이곳에 와 있다는 사실을 말하는 걸 깜빡했네요. 우리는 함께 산책도 하고, 마차도 타고, 승마도 하고, 보트도 타고, 테니스도 치고, 낚시도 즐기고 있답니다. 그리고 저는 그 어느 때보다도 그를 사랑하게 되었어요. 그는 절 더 많이 사랑한다고 하지만, 저는 그 말이 의심스러워요. 왜냐하면 처음엔 지금보다 더 사랑할 수는 없을 거라고 했었거든요. 하지만 이런 농담은 그만해야겠어요. 저기 그가 저를 부르고 있네요. 그러니 지금은 사랑을 담아 이만 줄일게요.

"루시 올림.

"추신.—어머니께서도 안부 전해달라 하셨어요. 우리 가엾은 어머니도 한결 나아 보이세요. "추추신.—우리는 9월 28일에 결혼하기로 했어요."

수어드 박사의 일기장.

8월 20일.—렌필드 환자의 상태가 한층 더 흥미로워지고 있다. 이제 그는 꽤나 진정되어 발작이 멈추는 기간이 생겼다. 발작이 시작된 후 첫 주 동안 그는 끊임없이 난폭했다. 그러던 어느 날 밤, 달이 떠오르자마자 그는 조용해지더니 혼잣말로 중얼거리기 시작했다. "이제 기다릴 수 있어. 이제 기다릴 수 있다고." 병동 간수장이 내게 와서 그 사실을 알렸고, 나는 그를 살펴보기 위해 즉시 아래층으로 뛰어 내려갔다. 그는 여전히 구속복(환자의 움직임을 제한하는 캔버스 천으로 된 웃옷)을 입은 채 바닥과 벽에 푹신한 패드가 깔린 격리실에 있었지만, 그의 얼굴에 감돌던 붉은 기운은 사라져 있었다. 그리고 그의 두 눈에는 예전처럼 무언가를 애원하는 듯한—거의 '굽실거리는'이라고 할 법한—부드러운 빛이 약간 서려 있었다. 나는 그의 현재 상태에 만족했고, 구속복을 풀어주라고 지시했다. 간수장들은 망설였지만, 결국 아무런 항의 없이 내 지시를 따랐다. 참으로 이상하게도 이 환자는 그들이 자신을 불신한다는 것을 눈치챌 만큼의 눈치는 있었다. 그는 간수장들을 몰래 곁눈질하며 내게 다가와 속삭였다.—

"저 바보들은 내가 선생님을 해칠 수도 있다고 생각하나 봐요! 내가 선생님을 해치다니, 말도 안 되는 소리죠!"

이 가엾은 미치광이의 마음속에서조차 내가 다른 사람들과 다르게 구별된다는 사실을 발견하니, 왠지 모르게 마음이 놓였다. 하지만 그렇다고 해서 그의 생각을 다 이해할 수 있는 것은 아니다. 우리가 서로 어떤 공통점이 있어서 이렇게 한 편처럼 서게 된 것이라고 받아들여야 할까? 아니면 그가 내게서 어떤 엄청난 이득을 얻기 위해 내 안위가 그토록 중요해진 것일까? 이 부분은 나중에 꼭 알아내야겠다. 오늘 밤 그는 아무 말도 하지 않으려 한다. 심지어 새끼 고양이나 다 자란 고양이를 주겠다고 해도 그는 흔들리지 않았다. 그는 그저 이렇게만 말했다. "난 이제 고양이 따위엔 관심 없어요. 지금은 생각할 게 더 많거든요. 난 기다릴 수 있어요. 기다릴 수 있다고요."

잠시 후 나는 그를 떠났다. 간수장의 말에 따르면 그는 동트기 직전까지 조용하다가, 점차 불안해하더니 마침내 난폭해졌고, 결국 극심한 발작을 일으켜 완전히 지친 나머지 혼수상태처럼 기절해버렸다고 한다.

***

... 같은 일이 3일 밤 연속으로 일어났다. 하루 종일 난폭하게 굴다가, 달이 뜰 때부터 해가 뜰 때까지는 잠잠해진다. 그 원인에 대한 단서를 찾을 수 있다면 좋으련만. 마치 어떤 영향력이 왔다가 사라지는 것만 같다. 아, 좋은 생각이 떠올랐다! 오늘 밤 우리는 광인에 맞서 제정신을 가진 자들의 지혜를 겨뤄볼 것이다. 그는 이전에 우리의 도움 없이도 탈출했었다. 오늘 밤엔 우리가 그가 탈출하도록 도울 것이다. 그에게 기회를 주고, 필요할 때를 대비해 직원들을 대기시켜 그를 미행하게 할 것이다....

***

8월 23일.—"예상치 못한 일은 항상 일어난다." 영국의 정치가 벤저민 디즈레일리는 참으로 인생을 잘 알고 있었다. 우리의 새는 새장 문이 열린 것을 발견하고도 날아가지 않았다. 그래서 우리의 교묘한 계획은 모두 수포로 돌아갔다. 어쨌든 우리는 한 가지 사실을 증명해냈다. 그가 조용해지는 시간이 꽤 합리적인 시간 동안 지속된다는 것이다. 앞으로 우리는 매일 몇 시간씩 그의 구속을 풀어줄 수 있을 것이다. 나는 야간 간수장에게 그가 조용해지면 해 뜨기 한 시간 전까지만 그를 패드가 깔린 격리실에 가둬두라고 지시했다. 그의 마음이 그것을 인지하지 못한다 하더라도, 이 불쌍한 영혼의 육체만큼은 구속이 풀리는 안도감을 즐길 것이다. 앗! 또다시 예상치 못한 일이 일어났다! 사람들이 나를 부르고 있다. 환자가 또 탈출했다고 한다.

***

나중에.—또 한 번의 밤중 소동이 있었다. 렌필드는 간수장이 점검하러 방에 들어올 때까지 교묘하게 기다렸다. 그리고는 그를 지나쳐 복도로 쏜살같이 뛰쳐나갔다. 나는 간수장들에게 그를 쫓으라고 지시했다. 그는 다시 그 버려진 저택의 마당으로 들어갔고, 우리는 그 낡은 예배당 문에 몸을 밀착시키고 있는 그를 예전과 같은 장소에서 찾아냈다. 그는 나를 보자 몹시 격분했고, 간수장들이 제때 그를 붙잡지 않았다면 나를 죽이려 했을 것이다. 우리가 그를 붙잡고 있을 때 기이한 일이 일어났다. 그는 갑자기 몸부림을 두 배로 치더니, 이내 거짓말처럼 평온해졌다. 나는 본능적으로 주위를 둘러보았으나 아무것도 보이지 않았다. 그때 환자의 시선을 포착하고 그것을 따라가 보았지만, 달빛이 비치는 하늘을 날아 서쪽으로 소리 없이 유령처럼 퍼덕이며 날아가는 커다란 박쥐 한 마리 외에는 아무것도 찾을 수 없었다. 보통 박쥐들은 빙빙 돌며 날아다니지만, 이 녀석은 마치 목적지를 알고 있거나 자기만의 어떤 의도가 있는 것처럼 똑바로 날아가는 듯했다. 환자는 매 순간 더 차분해졌고, 이윽고 이렇게 말했다.—

"날 묶을 필요 없어요. 얌전히 갈 테니까요!" 우리는 아무런 문제 없이 병동 건물로 돌아왔다. 나는 그의 평온함 속에 무언가 불길한 것이 있다고 느끼며, 오늘 밤을 결코 잊지 않을 것이다....

루시 웨스텐라의 일기장

힐링엄에서, 8월 24일.—나도 미나를 따라 일어난 일들을 글로 적어두어야겠다. 그러면 우리가 다시 만났을 때 길게 이야기 나눌 수 있을 테니까. 그게 언제쯤이 될지 궁금하다. 미나가 다시 내 곁에 있었으면 좋겠다. 나 자신이 너무 불행하게 느껴지기 때문이다. 어젯밤 나는 윗비에 있을 때처럼 또다시 꿈을 꾼 것 같다. 어쩌면 공기가 바뀌었거나 집에 돌아와서 그런 걸지도 모른다. 아무것도 기억나지 않아 내게는 이 모든 상황이 그저 어둡고 끔찍할 뿐이다. 막연한 두려움만 가득하고 몸은 너무 쇠약해지고 지친 느낌이다. 아서가 점심을 먹으러 왔을 때 내 모습을 보고 무척이나 슬퍼 보였고, 나는 억지로라도 밝게 행동할 기력조차 없었다. 오늘 밤엔 어머니 방에서 잘 수 있을까. 핑계를 대고 한번 시도해 봐야겠다.

***

8월 25일.—또 끔찍한 밤이었다. 어머니는 내 제안을 그리 내켜 하지 않으셨다. 어머니도 몸이 썩 좋지 않아 보이시고, 틀림없이 내게 걱정을 끼치고 싶지 않으신 눈치였다. 나는 깨어 있으려 노력했고 한동안은 성공했다. 하지만 12시를 알리는 시계 종소리에 깜빡 졸다가 깼으니, 틀림없이 잠이 들었던 모양이다. 창문에서 무언가 긁히거나 퍼덕거리는 소리 같은 게 났지만 나는 신경 쓰지 않았다. 그리고 그 이후로 아무런 기억이 없는 걸 보니 그때 다시 잠이 들었던 것 같다. 또다시 악몽을 꿨다. 그 꿈들을 기억할 수 있다면 좋으련만. 오늘 아침 나는 끔찍할 정도로 기운이 없다. 얼굴은 유령처럼 창백하고 목은 너무 아프다. 폐에 무슨 문제가 있는 게 틀림없다. 도무지 공기를 충분히 들이마실 수가 없다. 아서가 오면 기운을 내보려 노력해야지, 그러지 않으면 이런 내 모습을 보고 그가 몹시 괴로워할 테니까.
"""

en_content = """
Letter, Lucy Westenra to Mina Harker.

"Whitby, August 30.

"My dearest Mina,—

"Oceans of love and millions of kisses to you, and I truly hope you are safely settled in your new home with your husband very soon. I wish you could return to England early enough to come and stay with us here in Whitby. The bracing sea air would undoubtedly restore Jonathan’s health in no time; it has completely revitalized me! I have a massive appetite, I feel full of energy, and I am sleeping incredibly well. You will also be thrilled to hear that my sleepwalking seems to be completely cured. I don't think I have left my bed a single time during the night for an entire week now. Arthur actually teased me that I am putting on weight! Oh, speaking of Arthur, I completely forgot to mention that he is here visiting. We are having the most wonderful time—taking long walks, going on carriage rides, horseback riding, rowing boats, playing tennis, and fishing together. I swear I love him more now than I ever have before. He insists that he loves me even more, but I told him I find that hard to believe, considering he previously claimed he couldn't possibly love me any more than he already did! But anyway, that is just silly talk. I can hear him calling for me right now. So, I must stop writing for the moment.

"With all my love,

"LUCY.

"P.S.—Mother sends her love as well. She seems to be feeling a bit better, the poor dear. "P.P.S.—We have set our wedding date for September 28th."

Dr. Seward's Diary.

August 20.—The case of my patient, Renfield, is becoming even more fascinating. He has calmed down significantly, to the point where he now experiences distinct periods of rest between his fits of mania. For the entire first week following his initial attack, he was constantly aggressive and violent. Then, a few nights ago, exactly as the moon was rising, he suddenly became very peaceful and started muttering to himself, "Now I can wait; now I can wait." The ward attendant rushed to inform me, and I went straight down to his cell to observe him. He was still wearing the straitjacket and confined to the padded isolation room, but the flushed, angry look had completely vanished from his face. In its place, his eyes held a soft, pleading—I might even say groveling—expression that I hadn't seen in a while. I was satisfied that he was no longer a danger to himself or others, so I ordered the staff to remove his restraints. The attendants were visibly hesitant, but they ultimately followed my instructions without argument. Curiously enough, the patient was lucid enough to notice their suspicion. He leaned in close to me and whispered, while darting nervous glances at the guards:—

"They actually think I would hurt you! Imagine me hurting you! What fools!"

I must admit, it was oddly comforting to realize that even in the deeply disturbed mind of this poor madman, I am viewed as an ally and kept completely separate from the others. However, I still cannot fully grasp his underlying logic. Does he believe we share some kind of common ground or alliance? Or is it that he expects to gain something so incredibly important from me that my safety and well-being are absolutely vital to his plans? I will have to figure that out eventually. Tonight, though, he absolutely refuses to speak further. I even offered him a kitten, or a full-grown cat, but he wasn't interested in the slightest. His only response was, "I don't care about cats right now. I have far more important things to focus on, and I can wait; I can wait."

After a short while, I left him alone. The night attendant later reported that Renfield remained perfectly quiet until just before dawn. Then, he slowly began to grow agitated and eventually erupted into violence once more, continuing until he suffered a severe physical fit. This episode drained him completely, leaving him unconscious and in a state closely resembling a coma.

***

... This exact cycle has now repeated for three consecutive nights—he is violently aggressive throughout the day, and then perfectly calm from moonrise until sunrise. I wish I could figure out what is triggering this pattern. It almost seems as though some external force or influence is coming and going on a schedule. Wait, I just had a brilliant idea! Tonight, we will pit our sane minds against his madness. He managed to escape his cell previously without any help from us; tonight, we will secretly help him do it again. We will intentionally give him an opportunity to break out, but I will have a team of men stationed nearby, ready to track him in case we need to intervene....

***

August 23.—The British statesman Benjamin Disraeli certainly understood life when he noted that "The unexpected always happens." When our elusive 'bird' realized the cage door was left open tonight, he flatly refused to fly away. So, all of our elaborate planning was completely useless. However, we did confirm one important detail: his periods of calm last for a reasonably predictable amount of time. Going forward, this means we can safely remove his restraints for several hours every day. I have instructed the night attendant to simply lock him in the padded room once his calm phase begins, and keep him there until roughly an hour before dawn. Even if his shattered mind doesn't fully understand what is happening, his physical body will certainly benefit from the relief of being unbound. Wait! There goes the unexpected once again! An attendant is calling for me; the patient has managed to escape again.

***

Later.—We had quite the adventure tonight. Renfield cleverly hid and waited for the exact moment the attendant opened the door for a routine check. He then shoved past the man and sprinted down the hallway. I immediately ordered the staff to pursue him. Once again, he fled onto the grounds of the neighboring abandoned estate, Carfax, and we cornered him in the exact same spot as last time—pressed tightly against the heavy wooden door of the old chapel. When he saw me approach, he flew into an absolute rage. If the attendants hadn't grabbed him quickly, I am certain he would have attempted to murder me on the spot. But while we were struggling to hold him down, something very strange occurred. He suddenly fought twice as hard to break free, and then, in the blink of an eye, he went completely limp and calm. I instinctively looked around to see what had caused the change, but I saw nothing. I then noticed where the patient was staring and followed his gaze up into the moonlit sky. The only thing I could see was a very large bat, silently flapping its way westward like a ghost. Usually, bats fly in erratic, circling patterns as they hunt bugs, but this particular creature seemed to be flying in a direct, purposeful line, as if it knew exactly where it was going or was on some specific mission. Renfield grew calmer by the second, and eventually said quietly:—

"You don't need to tie me up; I will come with you peacefully." We escorted him back to the asylum without any further incident. Still, I cannot shake the feeling that there is something deeply sinister about his sudden shift in mood, and I will certainly not forget the events of this night anytime soon....

Lucy Westenra's Diary

Hillingham, August 24.—I have decided I need to start keeping a journal, just like Mina does, and write everything down. That way, we will have so much to talk about when we finally see each other again. I honestly wonder when that will be. I desperately wish she were here with me right now, because I am feeling utterly miserable. Last night, I think I started having those same strange dreams I had back in Whitby. Maybe the change of scenery or returning home triggered them again. The whole experience feels dark, confusing, and terrifying, mainly because I cannot remember a single specific detail; I am just left with a vague, overwhelming sense of dread, and I feel physically exhausted and weak. When Arthur stopped by for lunch today, he looked genuinely distressed to see me in such a state, and I didn't even have the energy to fake a smile for him. I wonder if it would help to sleep in my mother's bedroom tonight. I think I will make up an excuse and try that.

***

August 25.—I had another terrible night. My mother didn't seem very receptive to the idea of me sleeping in her room. She hasn't been feeling well herself, and I am certain she is just trying to avoid showing how worried she is about me. I tried my hardest to stay awake, and I managed it for a little while; but when the grandfather clock struck midnight, the sound startled me out of a doze, which means I must have drifted off. I vaguely recall hearing a scratching or flapping noise against the windowpane, but I ignored it. Since I don't remember anything else, I assume I fell deeply asleep right after that. I had more horrible nightmares, and I really wish I could remember what they were about. This morning, I feel shockingly weak. My face is pale as a ghost, and my throat is very sore. There must be something wrong with my lungs, because I feel like I can never catch my breath. I will have to try my best to act cheerful when Arthur visits later; otherwise, I know seeing me like this will make him absolutely miserable.
"""

with open(ko_file, 'a', encoding='utf-8') as f:
    f.write('\n\n' + ko_content.strip())
with open(en_file, 'a', encoding='utf-8') as f:
    f.write('\n\n' + en_content.strip())
print("Append successful.")
