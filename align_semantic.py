import json

data = json.load(open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch22_tasks.json', encoding='utf-8'))
out = []

# Combine all korean text just to have it
all_korean = "\n".join([item['korean_original'] for item in data])

# Now let's carefully construct the korean_chunks for each paragraph_index based on semantic matching.

out = []

# Index 2:
# 1. October 3rd... trivial or crucial.
# 2. In the end... What kind of end could she mean?...
# 3. Well, back to work! I must work!
k2_c1 = "반 헬싱 박사와 수어드 박사는 음식을 먹어두지 않으면 제대로 일할 수 없다고 뜻을 모았다. 신께서도 아시겠지만, 오늘 우리는 최선을 다해야만 한다. 생각할 틈을 주면 두려움에 휩싸일 것 같아 기회가 날 때마다 쉬지 않고 글을 쓰려 한다. 사소한 일이든 중대한 일이든 모조리 기록해 두어야 한다."
k2_c2 = "어쩌면 마지막에 가서는 그 사소한 흔적들이 가장 큰 깨달음을 줄지도 모르니까. 그 깨달음이 크든 작든 간에 미나와 내가 지금 처한 상황보다 더 끔찍한 구렁텅이로 우리를 끌고 가지는 못할 것이다. 그럼에도 우리는 믿음을 안고 희망을 품어야 한다. 불쌍한 미나는 방금 전 사랑스러운 두 뺨에 눈물을 흘리며, 우리의 믿음이 시험받는 것은 바로 이런 고난과 시련 속이며 우리는 계속 믿어야 하고 신께서 마지막까지 우리를 도우실 것이라고 말했다. 마지막이라니! 오 맙소사! 대체 어떤 마지막을 뜻하는 걸까."
k2_c3 = "자, 이제 일하자! 일해야 한다!"
out.append({'paragraph_index': 2, 'korean_chunks': [k2_c1, k2_c2, k2_c3]})

# Index 4:
# 1. Dr. Seward asked the orderly who was on duty in the hallway if he had heard anything... just a single "voice," the orderly replied that he couldn't be certain.
# 2. Initially, it sounded like two people... entirely unhelpful.
# 3. Given the circumstances... inevitably lead to the same conclusion.
k4_c1 = "반 헬싱 박사와 수어드 박사가 가엾은 정신병원 환자 렌필드의 상태를 살피고 돌아왔을 때, 우리는 앞으로 해야 할 일에 대해 심각하게 논의했다. 수어드 박사는 반 헬싱 박사와 함께 아래층 방으로 내려갔을 때 렌필드가 바닥에 웅크린 채 쓰러져 있는 것을 발견했다고 전했다. 그의 얼굴은 온통 멍들고 짓눌려 있었으며 목뼈는 부러진 상태였다. 수어드 박사는 복도에서 당번을 서던 간호인에게 혹시 무슨 소리를 듣지 못했느냐고 물었다. 간호인은 자리에 앉아 깜빡 졸았다고 고백하며, 방 안에서 들려온 큰 목소리에 이어 렌필드가 \"신이여! 신이여! 신이여!\" 하고 여러 번 크게 소리치는 것을 들었다고 했다. 그 직후 무언가 무겁게 떨어지는 소리가 났고, 방에 들어가 보니 의사들이 본 것과 똑같이 그가 얼굴을 바닥에 대고 쓰러져 있었다는 것이다. 반 헬싱 박사가 여러 사람의 목소리를 들었는지 아니면 한 사람의 목소리였는지 묻자, 간호인은 확실히 말할 수 없다고 대답했다."
k4_c2 = "처음에는 두 사람의 목소리 같았지만 방 안에는 아무도 없었기에 한 사람의 목소리였을 수밖에 없다고 여긴 것이다. 그는 원한다면 렌필드가 \"신이여\"라고 말했다는 사실에 대해 맹세할 수도 있다고 했다. 수어드 박사는 우리끼리만 남게 되자 이 문제를 더는 파헤치고 싶지 않다고 말했다. 검시관의 조사 문제도 고려해야 하는데, 아무도 믿지 않을 진실을 내세워 봐야 전혀 도움이 되지 않기 때문이다."
k4_c3 = "현재 상황으로는 간호인의 증언을 바탕으로 그가 침대에서 떨어져 사고사했다는 사망 진단서를 발급할 수 있을 것이라 그는 생각했다. 만약 검시관이 요구하여 공식적인 조사가 열리더라도 필연적으로 같은 결과가 나올 테니 말이다."
out.append({'paragraph_index': 4, 'korean_chunks': [k4_c1, k4_c2, k4_c3]})

# Index 5:
# 1. When we began to discuss our next steps, our very first decision was that Mina... "Alas! We have already been through too much.
# 2. Furthermore, there is nothing in this world that could inflict more pain upon me... softly:
k5_c1 = "우리의 다음 단계를 논의하기 시작했을 때 가장 먼저 결정한 것은 내 아내 미나가 모든 사실을 남김없이 알아야 한다는 것이었다. 아무리 고통스럽더라도 그녀에게 어떤 것도 숨겨서는 안 된다고 뜻을 모았다. 미나 역시 그것이 현명한 처사라며 고개를 끄덕였는데, 그토록 용감하면서도 동시에 깊은 절망과 슬픔에 빠져 있는 그녀를 보는 것은 참으로 가슴 아픈 일이었다. 우리 각자는 그녀가 무슨 뜻으로 하는 말인지 어렴풋이 짐작하고 있었다. 그녀의 대답은 마치 단순한 사실을 말하듯 직설적이고 솔직하게 흘러나왔다."
k5_c2 = "\"왜냐하면 만약 제 안에서 제가 사랑하는 사람에게 해를 끼칠 징후를 조금이라도 발견한다면, 저는 곧바로 죽음을 택할 것이기 때문입니다! 물론 그런 일이 생기지 않도록 제 자신을 예의 주시하겠지만요.\" \"설마 자살을 하겠다는 건 아니겠지요?\" 그가 쉰 목소리로 물었다. \"그럴 거예요. 만약 저를 그토록 사랑해서, 저에게 그런 끔찍한 고통과 필사적인 노력을 덜어줄 친구가 곁에 아무도 없다면 말이에요!\" 그녀는 의미심장하게 그를 바라보며 말했다. 자리에 앉아 있던 그는 이제 일어나 그녀에게 다가가 머리에 손을 얹고 엄숙하게 말했다. \"얘야, 만약 그것이 진정 널 위한 일이라면 그런 사람이 있단다. 나로서는, 설령 지금 당장 그게 최선이라 하더라도 너에게 그런 안락사를 선사하는 것이 신 앞에서의 내 책임이라고 여길 수 있단다. 아니, 그것이 안전하다면 말이다! 하지만 얘야.\" 잠시 숨이 막힌 듯 목구멍으로 솟구치는 큰 슬픔을 삼키던 그는 이내 말을 이었다."
out.append({'paragraph_index': 5, 'korean_chunks': [k5_c1, k5_c2]})

# Index 13:
# 1. "There are people here who would stand between you and death... in safety or in peril!
# 2. By your living soul, I command you not to die... speaking sweetly but oh so sorrowfully:
k13_c1 = "\"이곳에는 너와 죽음 사이를 가로막고 설 사람들이 있단다. 넌 죽어서는 안 돼. 누구의 손에 의해서든 죽어서는 안 되며, 특히 네 자신의 손으로는 절대 안 돼. 네 순결한 삶을 더럽힌 그 괴물이 진짜로 죽을 때까지 넌 죽어서는 안 된다. 왜냐하면 그놈이 여전히 살아 숨 쉬는 뱀파이어로 남아 있는 한, 네가 죽게 되면 너 역시 그놈과 똑같은 존재가 되어버릴 테니까 말이야. 안 돼, 넌 살아야 해! 죽음이 말로 다 할 수 없는 축복처럼 보일지라도 넌 살기 위해 발버둥 치고 노력해야 한다. 고통 속에서든 기쁨 속에서든, 낮이든 밤이든, 안전할 때든 위험할 때든 죽음 그 자체와 맞서 싸워야 해!"
k13_c2 = "살아 있는 네 영혼을 걸고 명하노니, 이 거대한 악이 지나갈 때까지 절대 죽어서는 안 되며, 아니 죽음을 생각해서도 안 된다.\" 가엾고 사랑스러운 미나는 밀물이 들어올 때 흔들리며 떨리는 흐르는 모래처럼 하얗게 질려 충격에 빠져 몸을 떨었다. 우리는 모두 침묵할 수밖에 없었고 완전히 무력해졌다. 마침내 조금 평온을 되찾은 그녀는 그에게 돌아서서 다정하지만 너무나 슬픈 목소리로 손을 내밀며 말했다."
out.append({'paragraph_index': 13, 'korean_chunks': [k13_c1, k13_c2]})

# Index 16:
# 1. "It is perhaps a stroke of luck," he said... rendering them useless to him.
# 2. Now that we have a much better understanding... holes, or crevices.
# 3. If he wishes to pass through a doorway... catch him and finish him off for good." At that moment, I leaped up... taking action was unbearable.
# 4. However, Van Helsing raised his hand... related items for them. He will have his writing paper and his checkbook.
# 5. There are many personal belongings... Don't you agree?"
k16_c1 = "\"어쩌면 다행인지도 모릅니다.\" 그가 말했다. \"우리가 백작의 낡은 저택 카팍스를 방문한 후 모여서 그곳에 있는 흙 상자들을 건드리지 않기로 결정했던 일이 말입니다. 만약 우리가 그 상자들에 손을 댔다면 백작은 틀림없이 우리의 목적을 눈치채고 다른 상자들에 대해서도 그런 시도를 좌절시키기 위해 미리 방어 조치를 취했을 것입니다. 하지만 지금 그는 우리의 의도를 전혀 모르고 있습니다. 게다가 우리가 성스러운 빵인 성체를 이용해 자신의 은신처를 다시는 쓰지 못하게 정화할 수 있다는 사실조차 십중팔구 모를 것입니다."
k16_c2 = "우리는 이제 그 상자들의 배치에 대해 훨씬 더 깊이 알게 되었으니, 런던 피카딜리에 있는 집을 조사하고 나면 마지막 남은 상자까지 모두 추적할 수 있을 것입니다. 그러니 오늘이야말로 우리에게 기회이며, 우리의 모든 희망은 오늘 우리가 성취하는 일에 달려 있습니다. 오늘 아침 우리의 슬픔 위로 떠오른 태양이 지는 과정을 통해 우리를 지켜줄 것입니다. 오늘 밤 해가 질 때까지 그 괴물은 지금 취하고 있는 형태를 그대로 유지해야만 합니다. 그는 육체적인 한계에 갇혀 있습니다. 허공으로 녹아들거나 갈라진 틈이나 구멍으로 숨어들 수 없습니다."
k16_c3 = "문을 통과하려면 평범한 사람처럼 직접 열어야만 하지요. 그래서 우리는 오늘 하루 동안 그의 모든 은신처를 찾아내고 그곳을 정화해야 합니다. 그렇게 하면 비록 당장 그를 붙잡아 파멸시키지 못한다 하더라도 그를 궁지로 몰아넣어 언젠가는 옴짝달싹 못 하게 붙잡아 확실하게 끝낼 수 있을 것입니다.\" 이때 나는 미나의 생명과 행복이 걸린 이 소중한 시간들이 우리가 대화나 나누며 아무런 행동도 하지 못하는 사이 덧없이 흘러가고 있다는 생각에 참을 수 없어 벌떡 일어났다."
k16_c4 = "하지만 반 헬싱은 경고하듯 손을 들어 올렸다. \"아니네, 친구 조나단.\" 그가 말했다. \"자네들 속담에 가장 빠른 길이 가장 먼 길이라는 말이 있듯 지금은 서두를 때가 아니네. 때가 오면 우리는 필사적으로 빠르고 신속하게 움직일 걸세."
k16_c5 = "\" (Note: Actually the text stops there in index 5! Let's check where the rest of index 16 is!) "

# Let's write the JSON and continue matching!
with open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch22_aligned.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

