import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('The_Muqaddimah_Original.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

matches = []
for i in range(10000, 35000):
    line = lines[i]
    if 'ألقاب' in line and 'علامة' in line and 'هرم' in line:
        start = max(0, i - 2)
        end = min(len(lines), i + 15)
        paragraph = "".join(lines[start:end]).strip()
        matches.append((i, paragraph))
        break

with open('extracted_elite.txt', 'w', encoding='utf-8') as f:
    for idx, (line_num, para) in enumerate(matches, 1):
        f.write(f"--- MATCH {idx} (Line {line_num}) ---\n")
        f.write(para)
        f.write("\n\n")

print(f"Extracted section to extracted_elite.txt")
