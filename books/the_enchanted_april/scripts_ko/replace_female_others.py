import json
import os
import re

target_files = [f"script_ch_{i:02d}.json" for i in range(8, 15)]

female_subjects = ["캐롤라인", "스크랩", "피셔", "코스탄차", "프란체스카", "그녀", "어머니", "아가씨", "부인", "로티", "로즈", "윌킨스 부인", "아버스넛 부인"]
male_subjects = ["도메니코", "프레더릭", "윌킨스", "아버스넛", "브리그스", "목사", "칼라일", "그", "주세페", "아버지", "남편", "남자"]

verbs = ["말했", "물었", "대답", "속삭", "대꾸", "설명", "덧붙", "소리", "생각", "중얼", "탄식", "지적", "가리", "외쳤", "불렀", "물어", "답했", "물음"]

total_changed = 0

for filename in target_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changed = False
    for i, block in enumerate(data):
        if block.get("character") == "Other":
            prev_text = data[i-1]["text"] if i > 0 else ""
            next_text = data[i+1]["text"] if i < len(data)-1 else ""
            
            # Extract only the sentence closest to the quote
            # Often, the speaker is identified right after the quote.
            context = ""
            if i > 0 and data[i-1].get("character") == "Narrator":
                context += prev_text.split(".")[-1] + " "
            if i < len(data)-1 and data[i+1].get("character") == "Narrator":
                context += next_text.split(".")[0] + " "
            
            is_female = False
            # Check for female subjects with '가' or '는' or '이' or '은'
            for fs in female_subjects:
                if fs in context:
                    is_female = True
            
            # Check for male subjects
            for ms in male_subjects:
                if ms in context:
                    # If both are present, we might have a conflict
                    # but usually, "도메니코가" vs "그녀에게" -> Look at verbs
                    pass
            
            # Let's do a broader check on the full narrator block if context wasn't enough
            if not is_female:
                full_context = ""
                if i > 0 and data[i-1].get("character") == "Narrator":
                    full_context += prev_text + " "
                if i < len(data)-1 and data[i+1].get("character") == "Narrator":
                    full_context += next_text + " "
                    
                # count
                f_count = sum(full_context.count(fs) for fs in female_subjects)
                m_count = sum(full_context.count(ms) for ms in male_subjects)
                
                if f_count > m_count:
                    is_female = True
            
            # Hardcoded fix for known issues
            if block["text"] in ["\"머리가 아파요.\"", "\"자고 싶어요.\"", "\"전 그런 적 없어요.\"", "\"그럼 내가 헛걸음을 한 셈이구려.\"", "\"글쎄요, 그것도 고민해 볼 문제 중 하나이긴 하네요.\"", "\"하지만 그것이 궁극적인 해답이라고 생각하진 않아요.\"", "\"전 정말 괜찮아요.\"", "\"그럼 아프다는 소식은 왜 전한 거요?\""]:
                if "아파요" in block["text"] or "자고" in block["text"] or "전 그런 적" in block["text"] or "글쎄요" in block["text"] or "궁극적인" in block["text"] or "정말 괜찮아요" in block["text"]:
                    is_female = True
                if "헛걸음" in block["text"] or "아프다는 소식" in block["text"]:
                    is_female = True # Mrs Fisher
            
            # Apply changes
            if is_female:
                block["character"] = "Rose"
                block["voice"] = "ko-KR-SunHiNeural"
                block["speed"] = 0.95
                changed = True
                total_changed += 1

    if changed:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Total female 'Other' blocks changed to Rose: {total_changed}")
