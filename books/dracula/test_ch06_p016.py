import re

def count_sents(text):
    cleaned = re.sub(r'\b(Dr|Mr|Mrs|Ms|St|Prof|Rev|Sr|Jr|Vol|P\.S)\.\s+', r'\1_ ', text)
    cleaned = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', cleaned)
    matches = re.findall(r'[.!?](?:\s|"|”|”|\'|$)', cleaned)
    return max(1, len(matches)) if text.strip() else 0

en_p016 = '[P016] "Edward Spencelagh, master mariner, murdered by pirates off the coast of Andres, April, 1854, age 30." When I returned, Mr. Swales continued:'
ko_p016_old = '[P016] 16. "에드워드 스펜슬라, 선장. 1854년 4월 안드레스 연안에서 해적에게 살해됨. 향년 30세." 제가 돌아오자 스웨일스 할아버지가 계속해서 말했습니다.'
ko_p016_new = '[P016] "에드워드 스펜슬라, 선장, 1854년 4월 안드레스 연안에서 해적에게 살해됨, 향년 30세." 제가 돌아오자 스웨일스 할아버지가 계속해서 말했습니다.'

print('EN count:', count_sents(en_p016))
print('KO old count:', count_sents(ko_p016_old))
print('KO new count:', count_sents(ko_p016_new))
