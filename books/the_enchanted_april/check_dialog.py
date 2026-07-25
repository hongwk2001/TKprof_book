import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "scripts_en", "script_ch_05.json")

if not os.path.exists(json_path):
    print(f"File not found: {json_path}")
    exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for seg in data:
    idx = seg.get("index")
    char = seg.get("character")
    text = seg.get("text")
    if char != "Narrator":
        print(f"Index {idx:3d} | {char:10s} | {text}")
