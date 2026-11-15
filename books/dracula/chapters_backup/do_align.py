import json
import re

with open(r'C:\git_repo\TKprof_book\books\dracula\chapters\ch06_ko.txt', 'r', encoding='utf-8') as f:
    raw_text = f.read()

paras = [p.strip() for p in raw_text.split('\n\n')]
paras = [re.sub(r'^\[P\d{3}\]\s*', '', p) for p in paras]

p5 = paras[5]
p5_splits = [
    ("항구를 향해 아주 가파르게", 5), # P006
    ("항구는 제 아래로 내려다보입니다.", 6), # P007
    ("만조 때는 풍경이 근사하지만,", 7), # P008
    ("그는 퍽 재미있는 노인입니다.", 8), # P009
    ("\"아가씨, 나라면 그런 것들에", 9), # P010
    ("저는 그가 옛날 포경선 시절의", 10), # P011
    ("\"아가씨, 난 이제 집으로", 11), # P012
    ("그는 절뚝거리며 멀어졌고,", 12), # P013
    ("* * * * *", 13), # P014
    ("8월 1일. 한 시간 전에", 14), # P015
    ("우리가 자리에 앉자마자", 15), # P016
    ("\"그건 다 쓸데없는 헛소리요,", 16) # P017
]

p5_chunks = []
current_text = p5
for i in range(len(p5_splits)-1, -1, -1):
    marker = p5_splits[i][0]
    idx = current_text.rfind(marker)
    p5_chunks.insert(0, current_text[idx:].strip())
    current_text = current_text[:idx].strip()

out_paras = ["" for _ in range(73)]
for i in range(5):
    out_paras[i] = paras[i]

for i in range(12):
    out_paras[5 + i] += p5_chunks[i] + " "

mapping = {
    6: 6, 7: 7, 8: 8,
    9: 30, 10: 31, # Wait, P031 is index 30!
    11: 11, 12: 12, 13: 13,
    14: 43, 15: 47, 16: 51, 17: 57, 18: 58,
    19: 19, 20: 20,
    21: 62, 22: 66, 23: 23, 24: 67, 25: 70
}

for i in range(6, 26):
    target = mapping[i]
    out_paras[target] += paras[i] + " "

for i in range(26, 73):
    out_paras[i] += paras[i] + " "

out_paras = [p.strip() for p in out_paras]

with open(r'C:\git_repo\TKprof_book\books\dracula\chapters\aligned_ko_ch06.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(out_paras))

print("Done! Paragraphs:", len(out_paras))
