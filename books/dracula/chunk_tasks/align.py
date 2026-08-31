import json
d = json.load(open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch26_tasks.json', encoding='utf-8'))[0]
eng_chunks = d['english_chunks']
kor = d['korean_original']

boundaries = [
    '1: 제26장',
    '평소라면 가벼운 단어 하나만 던져도',
    '5: 부인은 거기서 말을 멈췄다.',
    '6: "다들 차 한 잔 하시겠어요?',
    '만약 누군가 옮기려 한다 해도,',
    '이번에는 최면 상태에 빠져드는 데',
    '11: 그리하여 우리는 피를 말리는',
    '우리에게 가장 절실한 이 순간에 백작의',
    '14: "무언가 빠져나가고 있어요.',
    '15: *       *       *       *       *',
    '17: "사방이 어둠뿐이에요.',
    '우리 얼굴에 번진 경악을 알아챈',
    '21: "오, 미나 부인." 교수가',
    '워낙 시간이 촉박했던 터라,',
    '직원들은 몹시 친절하고 정중했으며,',
    '운이 너무 좋으니 나중에 이 균형을 맞추려고',
    '지브롤터를 지날 때는 신호조차 보낼 수 없었고,',
    '투박함과 교활함, 짙은 미신과 철저한',
    '놈들이 그 사내를 처음 봤을 때',
    '아니나 다를까, 오는 내내 물길은 탁 트였고',
    '명심하십시오, 놈들은 상자를 내던지려고',
    '솔직히 말해, 저도 점점 그 상자 때문에',
    '34: 우리는 사무실에 있는 힐데스하임을',
    '힐데스하임은 수고비로 영국 지폐를',
    '스킨스키를 몹시 꺼림칙하게 여기던',
    '이야기를 듣던 사람들이 그 끔찍한',
    '상황은 절망의 늪으로 빠져들고 있었다.',
    '펜 하나에 의지해 이 방대한 기록을',
    '42: 반 헬싱 박사님께 내가 아직 읽지',
]

def split_korean(k, bnds):
    chunks = []
    curr = 0
    for i in range(1, len(bnds)):
        nxt = k.find(bnds[i], curr)
        if nxt == -1:
            print('MISSING:', bnds[i])
            return None
        chunks.append(k[curr:nxt])
        curr = nxt
    chunks.append(k[curr:])
    return chunks

chunks = split_korean(kor, boundaries)
if chunks:
    d['korean_chunks'] = chunks
    with open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch26_aligned.json', 'w', encoding='utf-8') as f:
        json.dump([d], f, ensure_ascii=False, indent=2)
    print('SUCCESS')
