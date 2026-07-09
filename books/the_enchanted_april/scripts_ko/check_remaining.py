import json
import os

target_files = [f"script_ch_{i:02d}.json" for i in range(8, 15)]

for filename in target_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for i, block in enumerate(data):
        if block.get("character") == "Other":
            with open("remaining.txt", "a", encoding="utf-8") as out:
                out.write(f"Remaining in {filename} [{i}]: {block['text']}\n")
