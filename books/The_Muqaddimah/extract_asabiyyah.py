import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('The_Muqaddimah_Original.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Search for paragraphs containing 'عصبية' and defining words like 'التحام' (bonding/cohesion) or 'النعرة' (group feeling)
# Specifically looking in the early parts of the book (first 20,000 lines) where he defines it.
matches = []
for i in range(1000, 20000):
    line = lines[i]
    if 'عصبية' in line and ('التحام' in line or 'نسب' in line or 'دفاع' in line or 'حماية' in line):
        start = max(0, i - 3)
        end = min(len(lines), i + 4)
        paragraph = "".join(lines[start:end]).strip()
        
        # Avoid duplicate very similar paragraphs
        is_duplicate = False
        for _, existing in matches:
            if existing[:50] == paragraph[:50]:
                is_duplicate = True
                break
                
        if not is_duplicate:
            matches.append((i, paragraph))
            if len(matches) >= 5: # Just get the top 5 distinct definitional paragraphs
                break

with open('extracted_asabiyyah.txt', 'w', encoding='utf-8') as f:
    for idx, (line_num, para) in enumerate(matches, 1):
        f.write(f"--- MATCH {idx} (Line {line_num}) ---\n")
        f.write(para)
        f.write("\n\n")

print(f"Extracted {len(matches)} Asabiyyah occurrences to extracted_asabiyyah.txt")
