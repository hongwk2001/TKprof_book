import json

with open('books/dracula/chunk_tasks/ch18_tasks.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

split_starts = {
    4: [
        "\"이 저택을 둘러보시면서", 
        "순간 나는 그가 살의를"
    ],
    15: [
        "\"하커 부인, 우리 주인장처럼",
        "내가 만난 가장 중증인"
    ],
    17: [
        "\"그러니까, 제 자신이",
        "의사 선생님도 아시겠지만",
        "시계를 보니 반 헬싱"
    ],
    23: [
        "\"아, 그 놀라운 미나 부인",
        "비록 부인이 다치지는",
        "그는 깜짝 놀라며"
    ],
    35: [
        "\"뱀파이어라는 존재는",
        "하지만 그녀는 이미",
        "우리 가운데 숨어 있는 이",
        "그렇다면 우리는 이놈을",
        "천국의 문은 우리에게"
    ],
    44: [
        "\"우리가 기댈 수 있는 건",
        "우리는 우리 두 눈으로",
        "여기까지가 우리가 행동의",
        "놈과 몇 주 동안이나",
        "우리가 휘트비에 도착한",
        "몸집을 쥐방울만 하게",
        "놈은 자기가 가고 싶다고",
        "이처럼 놈은 자신의 한계",
        "그리고 마늘처럼 놈에게",
        "관 위에 들장미 가지를"
    ],
    45: [
        "\"이렇게 우리가 한때",
        "만약 그게 사실이라면",
        "그들은 헤르만슈타트 호수",
        "이 사악한 악마가 그 모든"
    ],
    66: [
        "방에 들어서자 그는",
        "\"박사님의 친구분들께 호소"
    ],
    67: [
        "\"고달밍 경, 윈덤 클럽에서",
        "먼로 독트린이 고리타분한",
        "국적이든 혈통이든 아니면"
    ],
    72: [
        "\"그렇다면 작전을 바꿀 수밖에",
        "\" 그는 다시 우리 모두의"
    ],
    77: [
        "그러나 내가 문고리를",
        "반 헬싱을 힐끗 쳐다보니",
        "하지만 내 예상은 빗나갔다"
    ],
    78: [
        "\"부탁입니다, 수어드",
        "선생님이 떠받드는"
    ]
}

out_data = []
success = True

for task in tasks:
    idx = task['paragraph_index']
    ko_text = task['korean_original']
    starts = split_starts.get(idx)
    
    if not starts:
        print(f"Missing starts for {idx}")
        success = False
        continue
        
    chunks = []
    current_text = ko_text
    
    for i in range(1, len(starts)):
        start_str = starts[i]
        pos = current_text.find(start_str)
        if pos == -1:
            # Let's try matching a shorter prefix of start_str just in case
            pos = current_text.find(start_str[:10])
            if pos == -1:
                print(f"Could not find '{start_str}' in task {idx}")
                success = False
                break
        chunks.append(current_text[:pos].strip())
        current_text = current_text[pos:]
    
    chunks.append(current_text.strip())
    
    out_data.append({
        "paragraph_index": idx,
        "korean_chunks": chunks
    })

if success:
    with open('books/dracula/chunk_tasks/ch18_aligned.json', 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print("Successfully wrote ch18_aligned.json")
else:
    print("Failed to align all chunks")
