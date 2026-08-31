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
    9: 30, 10: 31,
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

# Now fix the empty paragraphs: 17, 18, 21, 22, 24, 25

# 16 currently has: "그건 다 쓸데없는 헛소리요, 처음부터 끝까지 전부 다 말이오. 그 이상도 그 이하도 아니지. 그런 저주니, 유령이니, 괴물이니, 도깨비니 하는 이야기들은 그저 어린애들이나 철없는 여자들을 울리기에나 딱 좋은 것들이요. 다 허공에 떠도는 거품 같은 거지. 그런 것들과 온갖 징조나 경고 같은 것들은 다 목사들이나 심술궂은 학자들, 그리고 기차표 파는 놈들이 어수룩한 사람들을 겁주고 혼을 쏙 빼놓아서, 원래라면 하지 않을 짓을 하게 만들려고 지어낸 거란 말이오."
# Split it to fill 16, 17, 18
p16_text = out_paras[16]
s1 = p16_text.find("그런 저주니,")
s2 = p16_text.find("다 허공에 떠도는")
out_paras[16] = p16_text[:s1].strip()
out_paras[17] = p16_text[s1:s2].strip()
out_paras[18] = p16_text[s2:].strip()

# 20 currently has: "\"오, 스웨일스 할아버지, 진심은 아니시겠죠. 설마 이 묘비들이 전부 가짜라는 건가요?\""
p20_text = out_paras[20]
s3 = p20_text.find("설마 이 묘비들이")
out_paras[20] = p20_text[:s3].strip()
out_paras[21] = p20_text[s3:].strip()

# 23 currently has: "\"에드워드 스펜슬라, 선장. 1854년 4월 안드레스 연안에서 해적에게 살해됨. 향년 30세.\" 제가 돌아오자 스웨일스 할아버지가 계속해서 말했습니다."
p23_text = out_paras[23]
s4 = p23_text.find("1854년 4월")
s5 = p23_text.find("제가 돌아오자")
out_paras[22] = p23_text[:s4].strip()
out_paras[23] = p23_text[s4:s5].strip()
out_paras[24] = p23_text[s5:].strip()

# 26 currently has: "\"하지만,\" 제가 말했습니다. \"할아버지 말씀이 완전히 맞지는 않아요. 할아버지께서는 모든 가엾은 사람들이나 그들의 영혼이 심판의 날에 자기 묘비를 챙겨가야 한다는 가정을 바탕으로 말씀하고 계시잖아요. 그게 정말 필요할 거라고 생각하세요?\""
p26_text = out_paras[26]
s6 = p26_text.find("\"할아버지 말씀이")
out_paras[25] = p26_text[:s6].strip()
out_paras[26] = p26_text[s6:].strip()

with open(r'C:\git_repo\TKprof_book\books\dracula\chapters\aligned_ko_ch06.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(out_paras))

print("Done! Paragraphs:", len(out_paras))
print("Empty paragraphs:", sum(1 for p in out_paras if not p))
