import re

def count_sentences_raw(text):
    return len(re.findall(r'[.!?](?:\s|"|”|”|\'|$)', text))

def count_sentences_smart(text):
    # Ignore periods in common abbreviations: Dr., Mr., Mrs., Ms., St., Vol., etc.
    cleaned = re.sub(r'\b(Dr|Mr|Mrs|Ms|St|Prof|Rev|Sr|Jr|Vol|P\.S)\.\s+', r'\1_ ', text)
    matches = re.findall(r'[.!?](?:\s|"|”|”|\'|$)', cleaned)
    return max(1, len(matches)) if text.strip() else 0

text_en = "[P003a] October 3rd.—I am writing this diary because I feel I might go mad if I don't do something. It is currently six o'clock, and we are scheduled to gather in the study in half an hour to grab a bite to eat. Dr. Van Helsing and Dr. Seward have agreed that we cannot work at our best if we skip a meal. And heaven knows, we will absolutely need to be at our best today."
text_ko = "[P003a] 10월 3일.—무언가라도 하지 않으면 미쳐버릴 것 같아 이렇게 일기를 쓴다. 지금은 6시. 우리는 30분 뒤 서재에 모여 요기를 할 참이다. 반 헬싱 박사와 수어드 박사는 음식을 먹어두지 않으면 제대로 일할 수 없다고 뜻을 모았다. 신께서도 아시겠지만, 오늘 우리는 최선을 다해야만 한다."

print("Raw EN sents:", count_sentences_raw(text_en))
print("Smart EN sents:", count_sentences_smart(text_en))
print("KO sents:", count_sentences_raw(text_ko))
