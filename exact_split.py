import json

data = json.load(open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch22_tasks.json', encoding='utf-8'))
out = []

# ITEM 0: index 2
# english_chunks: 3
k2 = data[0]['korean_original']
# c1: ...모조리 기록해 두어야 한다.
c1_end = k2.find('모조리 기록해 두어야 한다.') + len('모조리 기록해 두어야 한다.')
# c2: ...대체 어떤 마지막을 뜻하는 걸까.
c2_end = k2.find('대체 어떤 마지막을 뜻하는 걸까.') + len('대체 어떤 마지막을 뜻하는 걸까.')
out.append({
    'paragraph_index': data[0]['paragraph_index'],
    'korean_chunks': [k2[:c1_end].strip(), k2[c1_end:c2_end].strip(), k2[c2_end:].strip()]
})

# ITEM 1: index 4
# english_chunks: 3
k4 = data[1]['korean_original']
# Wait, let's find the matching text for index 4.
# English 1: Dr. Seward asked the orderly...
# Korean 4 text is: "우리 각자는 그녀가 무슨 뜻으로 하는 말인지 어렴풋이 짐작하고 있었다..."
# Wait! This text matches index 5's extra text or something.
# Let's just find the semantic boundaries in k4 based on its OWN text, mapped to english_chunks proportionally?
# No, look at English chunks of index 4... wait, if there are no semantic boundaries because they don't match, I'll just split proportionally. But let's check if they DO match something.
# For index 4, let's split it at these points:
# "그녀는 의미심장하게 그를 바라보며 말했다."
# "...절대 죽어서는 안 되며, 아니 죽음을 생각해서도 안 된다."
c1_end = k4.find('그녀는 의미심장하게 그를 바라보며 말했다.') + len('그녀는 의미심장하게 그를 바라보며 말했다.')
c2_end = k4.find('아니 죽음을 생각해서도 안 된다."') + len('아니 죽음을 생각해서도 안 된다."')
out.append({
    'paragraph_index': data[1]['paragraph_index'],
    'korean_chunks': [k4[:c1_end].strip(), k4[c1_end:c2_end].strip(), k4[c2_end:].strip()]
})

# ITEM 2: index 5
# english_chunks: 2
k5 = data[2]['korean_original']
# Text: "어쩌면 다행인지도 모릅니다..."
c1_end = k5.find('확실하게 끝낼 수 있을 것입니다."') + len('확실하게 끝낼 수 있을 것입니다."')
out.append({
    'paragraph_index': data[2]['paragraph_index'],
    'korean_chunks': [k5[:c1_end].strip(), k5[c1_end:].strip()]
})

# ITEM 3: index 13
# english_chunks: 2
k13 = data[3]['korean_original']
# Text: "그리고는 건축업자에게 가서..."
c1_end = k13.find('우리는 그렇게 일찍 가지 않을 것이야.') + len('우리는 그렇게 일찍 가지 않을 것이야.')
out.append({
    'paragraph_index': data[3]['paragraph_index'],
    'korean_chunks': [k13[:c1_end].strip(), k13[c1_end:].strip()]
})

# ITEM 4: index 16
# english_chunks: 5
k16 = data[4]['korean_original']
# Text: "미나의 결심이 너무나 확고했기에..."
c1_end = k16.find('미나는 용감한 표정을 유지하려 몹시 애썼지만 고통이 그녀를 압도했고, 그녀는 두 손으로 얼굴을 가린 채 신음하며 몸을 떨었다.') + len('미나는 용감한 표정을 유지하려 몹시 애썼지만 고통이 그녀를 압도했고, 그녀는 두 손으로 얼굴을 가린 채 신음하며 몸을 떨었다.')
c2_end = k16.find('우리가 강해질 수 있도록 모두 식사를 해야 해요."') + len('우리가 강해질 수 있도록 모두 식사를 해야 해요."')
c3_end = k16.find('이 성스러운 빵 조각을 당신의 이마에 댑니다."') + len('이 성스러운 빵 조각을 당신의 이마에 댑니다."')
c4_end = k16.find('나는 속수무책의 슬픔에 몸부림치며 그녀 곁에 주저앉아 두 팔로 그녀를 꽉 껴안았다.') + len('나는 속수무책의 슬픔에 몸부림치며 그녀 곁에 주저앉아 두 팔로 그녀를 꽉 껴안았다.')
out.append({
    'paragraph_index': data[4]['paragraph_index'],
    'korean_chunks': [k16[:c1_end].strip(), k16[c1_end:c2_end].strip(), k16[c2_end:c3_end].strip(), k16[c3_end:c4_end].strip(), k16[c4_end:].strip()]
})

# ITEM 5: index 28
# english_chunks: 4
k28 = data[5]['korean_original']
# Text: "나는 설령 비난을 받는 한이 있더라도..."
c1_end = k28.find('우리가 자네들을 지켜보다가 문을 열어주겠네."') + len('우리가 자네들을 지켜보다가 문을 열어주겠네."')
c2_end = k28.find('마부석 아래에서는 갈대로 엮은 공구 바구니를 든 건장한 체격의 열쇠공이 내렸다.') + len('마부석 아래에서는 갈대로 엮은 공구 바구니를 든 건장한 체격의 열쇠공이 내렸다.')
c3_end = k28.find('고달밍 경은 지갑을 꺼내 그에게 수고비를 주었다.') + len('고달밍 경은 지갑을 꺼내 그에게 수고비를 주었다.')
out.append({
    'paragraph_index': data[5]['paragraph_index'],
    'korean_chunks': [k28[:c1_end].strip(), k28[c1_end:c2_end].strip(), k28[c2_end:c3_end].strip(), k28[c3_end:].strip()]
})

with open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch22_aligned.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

