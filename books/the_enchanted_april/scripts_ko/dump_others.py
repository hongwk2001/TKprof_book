import json
import os

target_files = [f"script_ch_{i:02d}.json" for i in range(8, 15)]
out_lines = []

for filename in target_files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for i, block in enumerate(data):
        if block.get("character") == "Other":
            prev_text = data[i-1]["text"] if i > 0 else ""
            next_text = data[i+1]["text"] if i < len(data)-1 else ""
            
            out_lines.append(f"File: {filename} | Index: {i}")
            out_lines.append(f"Prev: {prev_text[-100:]}")
            out_lines.append(f"Text: {block['text']}")
            out_lines.append(f"Next: {next_text[:100]}")
            out_lines.append("-" * 40)

with open("inspect_others.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
