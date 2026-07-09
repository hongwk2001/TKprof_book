import json
import os
import re

target_files = [f"script_ch_{i:02d}.json" for i in range(8, 15)]

for filename in target_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for i, block in enumerate(data):
        if block.get("character") == "Other":
            prev_text = data[i-1]["text"] if i > 0 else ""
            next_text = data[i+1]["text"] if i < len(data)-1 else ""
            
            # extract the subject before "말했다", "대답했다", "물었다", etc.
            # this is a simple regex
            match = re.search(r'([가-힣\s]+(?:가|는|이|은))\s+[^.]*(?:말했|물었|대답|속삭|대꾸|설명|덧붙|소리|생각|중얼|탄식|지적|가리|외쳤|불렀)', next_text)
            if not match:
                match = re.search(r'([가-힣\s]+(?:가|는|이|은))\s+[^.]*(?:말했|물었|대답|속삭|대꾸|설명|덧붙|소리|생각|중얼|탄식|지적|가리|외쳤|불렀)', prev_text)
            
            subject = match.group(1).strip() if match else "UNKNOWN"
            with open("subjects.txt", "a", encoding="utf-8") as out:
                out.write(f"{filename} [{i}]: {block['text']} -> {subject}\n")
