import json

with open(r"c:\git_repo\TKprof_book\books\dracula\chunk_tasks\ch23_tasks.json", "r", encoding="utf-8") as f:
    tasks = json.load(f)

output = []

for task in tasks:
    idx = task["paragraph_index"]
    orig = task["korean_original"]
    N = len(task["english_chunks"])
    chunks = [""] * N
    
    if idx == 2:
        parts = orig.split("다행히 기력마저 꺾인 것은 아니었다.")
        chunks[0] = parts[0]
        chunks[1] = "다행히 기력마저 꺾인 것은 아니었다." + parts[1]
    elif idx == 3:
        parts1 = orig.split("비상한 두뇌와 타의 추종을 불허하는 학식을 갖추었고,")
        chunks[0] = parts1[0]
        parts2 = parts1[1].split("놈은 훌륭하게 실험을 거듭하고 있소.")
        chunks[1] = "비상한 두뇌와 타의 추종을 불허하는 학식을 갖추었고," + parts2[0]
        chunks[2] = "놈은 훌륭하게 실험을 거듭하고 있소." + parts2[1]
    elif idx == 8:
        parts1 = orig.split("하지만 그 거대한 아이의 두뇌가 성장하면서,")
        chunks[0] = parts1[0]
        parts2 = parts1[1].split("하지만, 내 아이야, 절망하지 말게.")
        chunks[1] = "하지만 그 거대한 아이의 두뇌가 성장하면서," + parts2[0]
        chunks[2] = "하지만, 내 아이야, 절망하지 말게." + parts2[1]
    elif idx == 21:
        chunks[0] = ""
        chunks[1] = orig
    elif idx == 22:
        chunks[0] = ""
        chunks[1] = orig
    elif idx == 23:
        chunks[0] = ""
        parts1 = orig.split("아슬아슬하게 칼끝이 백작의 외투 자락만 찢어")
        chunks[1] = parts1[0]
        parts2 = parts1[1].split("백작의 얼굴에 스쳐 지나간 증오와 좌절된 악의,")
        chunks[2] = "아슬아슬하게 칼끝이 백작의 외투 자락만 찢어" + parts2[0]
        parts3 = parts2[1].split("깨진 유리가 쏟아지는 소리 너머로 금화 몇 닢이")
        chunks[3] = "백작의 얼굴에 스쳐 지나간 증오와 좌절된 악의," + parts3[0]
        chunks[4] = "깨진 유리가 쏟아지는 소리 너머로 금화 몇 닢이" + parts3[1]
    elif idx == 32:
        chunks[0] = ""
        chunks[1] = ""
        chunks[2] = orig
    elif idx == 40:
        chunks[0] = ""
        chunks[1] = ""
        chunks[2] = orig
    elif idx == 59:
        chunks[0] = ""
        chunks[1] = orig
    elif idx == 76:
        chunks[0] = ""
        chunks[1] = ""
        chunks[2] = orig

    output.append({
        "paragraph_index": idx,
        "korean_chunks": chunks
    })

with open(r"c:\git_repo\TKprof_book\books\dracula\chunk_tasks\ch23_aligned.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
