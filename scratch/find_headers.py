import re

filepath = r"C:\Users\hongw\.gemini\antigravity\brain\9a5fe6dc-1f15-4d6a-8c11-a75866ccab95\.system_generated\steps\80\content.md"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "MARCIA" in line.upper():
        print(f"Line {i+1}: {line.strip()}")
