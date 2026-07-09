import json
import os
import re

target_files = [f"script_ch_{i:02d}.json" for i in range(8, 15)]
out_data = []

female_keywords = ["캐롤라인", "스크랩", "피셔", "코스탄차", "프란체스카", "그녀", "레이디", "로티", "로즈", "아가씨", "부인", "어머니"]
male_keywords = ["도메니코", "프레더릭", "브리그스", "목사", "칼라일", "그가", "그는", "그에게", "주세페", "아버지", "남편", "남자"]

for filename in target_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for i, block in enumerate(data):
        if block.get("character") == "Other":
            prev_text = data[i-1]["text"] if i > 0 else ""
            next_text = data[i+1]["text"] if i < len(data)-1 else ""
            
            # Combine nearby text to search for keywords
            context = ""
            if i > 0 and data[i-1].get("character") == "Narrator":
                context += prev_text[-150:]
            if i < len(data)-1 and data[i+1].get("character") == "Narrator":
                context += next_text[:150]
                
            is_female = False
            # Find the closest keyword
            # We will just score them
            f_score = sum(1 for k in female_keywords if k in context)
            m_score = sum(1 for k in male_keywords if k in context)
            
            if f_score > m_score:
                is_female = True
            elif m_score > f_score:
                is_female = False
            else:
                # Tie breaker: look exactly at the sentence before or after the quote
                pass # default False for manual review
                
            out_data.append({
                "file": filename,
                "index": i,
                "text": block["text"],
                "is_female": is_female,
                "f_score": f_score,
                "m_score": m_score,
                "context": context.replace("\n", " ")
            })

with open("classify_others.json", "w", encoding="utf-8") as f:
    json.dump(out_data, f, ensure_ascii=False, indent=2)
