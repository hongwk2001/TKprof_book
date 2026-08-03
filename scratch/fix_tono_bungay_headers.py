import os
import re

base_dir = r"c:\git_repo\TKprof_book\books\tono_bungay\chapters"

TITLES = {
    "book1_ch01": {
        "en": "Chapter 1: Of Bladesover House, and My Mother; and the Constitution of Society",
        "ko": "제1장: 블레이즈오버 저택과 어머니, 그리고 사회의 구조"
    },
    "book1_ch02": {
        "en": "Chapter 2: My Entry into the World and the Last I Saw of Bladesover",
        "ko": "제2장: 세상으로의 진출, 그리고 블레이즈오버에서의 마지막 기억"
    },
    "book1_ch03": {
        "en": "Chapter 3: The Wimblehurst Apprenticeship",
        "ko": "제3장: 윔블허스트에서의 견습 생활"
    },
    "book2_ch01": {
        "en": "Chapter 1: How I Became a London Student and Went Astray",
        "ko": "제1장: 런던의 학생이 되어 길을 잃다"
    },
    "book2_ch02": {
        "en": "Chapter 2: The Ponderevo Delusion",
        "ko": "제2장: 폰더리보의 환상"
    },
    "book2_ch03": {
        "en": "Chapter 3: How We Made Tono-Bungay a Massive Success",
        "ko": "제3장: 우리가 어떻게 토노-번게이를 대성공으로 이끌었는가"
    },
    "book2_ch04": {
        "en": "Chapter 4: Marion",
        "ko": "제4장: 매리언"
    },
    "book3_ch01": {
        "en": "Chapter 1: The Hardingham Hotel, and How We Became Big People",
        "ko": "제1장: 하딩엄 호텔, 그리고 우리가 거물로 성장한 과정"
    },
    "book3_ch02": {
        "en": "Chapter 2: Our Progress from Camden Town to Crest Hill",
        "ko": "제2장: 캠던타운에서 크레스트 힐까지의 과정"
    },
    "book3_ch03": {
        "en": "Chapter 3: Soaring",
        "ko": "제3장: 비상"
    },
    "book3_ch04": {
        "en": "Chapter 4: How I Stole the Huge Amount of Quap from Mordet Island",
        "ko": "제4장: 모르데트 섬에서 엄청난 양의 콰프를 어떻게 훔쳤는가"
    },
    "book4_ch01": {
        "en": "Chapter 1: The Crash of Tono-Bungay",
        "ko": "제1장: 토노-번게이의 대몰락"
    },
    "book4_ch02": {
        "en": "Chapter 2: Love Among the Wreckage",
        "ko": "제2장: 잔해 속에서 피어난 사랑"
    },
    "book4_ch03": {
        "en": "Chapter 3: Night and the Open Sea",
        "ko": "제3장: 밤 그리고 탁 트인 바다"
    }
}

def clean_file(filepath, canonical_title):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    start_idx = 0
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        # If it's a very clear content start marker
        if line in ["I", "II", "III", "IV", "V", "1", "2", "3", "4", "5"]:
            start_idx = i
            break
            
        # If it's a long paragraph, it's probably content
        if len(line) > 60 and not line.startswith("[") and not line.startswith("Book"):
            # Ensure it's not just a very long title
            if "Chapter" not in line and "제" not in line[:10]:
                start_idx = i
                break
                
        # If it's a dialogue start
        if line.startswith('"') or line.startswith("'"):
            start_idx = i
            break

    # Reconstruct the file
    content = lines[start_idx:]
    
    # Clean up leading empty lines in content
    while content and not content[0].strip():
        content.pop(0)
        
    new_lines = [f"# {canonical_title}\n", "\n"] + content
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Cleaned {filepath}")

for b in range(1, 5):
    b_dir = os.path.join(base_dir, f"book{b}")
    if not os.path.exists(b_dir): continue
    
    for c in range(1, 10):
        key = f"book{b}_ch{c:02d}"
        if key in TITLES:
            en_file = os.path.join(b_dir, f"{key}_en.txt")
            ko_file = os.path.join(b_dir, f"{key}_ko.txt")
            
            if os.path.exists(en_file):
                clean_file(en_file, TITLES[key]["en"])
            if os.path.exists(ko_file):
                clean_file(ko_file, TITLES[key]["ko"])
