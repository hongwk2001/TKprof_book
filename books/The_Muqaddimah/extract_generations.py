import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('The_Muqaddimah_Original.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

search_term = "ثلاثة أجيال"
context_lines = 5

matches = []
for i, line in enumerate(lines):
    if search_term in line:
        start = max(0, i - context_lines)
        end = min(len(lines), i + context_lines + 1)
        
        # Build the paragraph
        paragraph = "".join(lines[start:end]).strip()
        matches.append((i, paragraph))

with open('extracted_generations.txt', 'w', encoding='utf-8') as f:
    for idx, (line_num, para) in enumerate(matches, 1):
        f.write(f"--- MATCH {idx} (Line {line_num}) ---\n")
        f.write(para)
        f.write("\n\n")

print(f"Extracted {len(matches)} occurrences to extracted_generations.txt")
