import glob
import os
import re

base_dir = r"d:\git_repo\TKprof_book\books\seneca_emotional_resilience\chapters"

questions_found = []

# Find all modernized English files
for f in glob.glob(os.path.join(base_dir, "**/*_en.txt"), recursive=True):
    # Ignore backup files
    if "_backup" in f:
        continue
        
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Split text into sentences using simple regex
    # Looking for strings ending with ?
    sentences = re.split(r'(?<=[.!?])\s+', content)
    
    for s in sentences:
        s_clean = s.strip()
        if s_clean.endswith('?'):
            rel_path = os.path.relpath(f, base_dir)
            questions_found.append((rel_path, s_clean))

print(f"Total questions found: {len(questions_found)}")
# Save the list to a temporary text file so we can view it
out_file = r"d:\git_repo\TKprof_book\scratch\rhetorical_questions.txt"
with open(out_file, 'w', encoding='utf-8') as out_f:
    out_f.write(f"Total questions found: {len(questions_found)}\n\n")
    for path, question in sorted(questions_found):
        out_f.write(f"[{path}]\n  {question}\n\n")

print(f"List saved to {out_file}")
