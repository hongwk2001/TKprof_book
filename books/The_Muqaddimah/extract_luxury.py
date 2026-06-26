import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('The_Muqaddimah_Original.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

matches = []
for i in range(10000, 30000): # Focusing around Chapter 3 and 4 where this is discussed heavily
    line = lines[i]
    # Looking for paragraphs that discuss luxury destroying the state/asabiyyah
    if 'ترف' in line and ('فساد' in line or 'هرم' in line or 'عصبية' in line or 'هلاك' in line or 'نعيم' in line):
        start = max(0, i - 4)
        end = min(len(lines), i + 5)
        paragraph = "".join(lines[start:end]).strip()
        
        # Avoid duplicate very similar paragraphs
        is_duplicate = False
        for _, existing in matches:
            if existing[:50] == paragraph[:50]:
                is_duplicate = True
                break
                
        if not is_duplicate and len(paragraph) > 100:
            matches.append((i, paragraph))
            if len(matches) >= 5: # Get top 5 strong matches
                break

with open('extracted_luxury.txt', 'w', encoding='utf-8') as f:
    for idx, (line_num, para) in enumerate(matches, 1):
        f.write(f"--- MATCH {idx} (Line {line_num}) ---\n")
        f.write(para)
        f.write("\n\n")

print(f"Extracted {len(matches)} Luxury occurrences to extracted_luxury.txt")
