import os
import re

path = r"d:\git_repo\TKprof_book\books\frankenstein\chapters\ch_05_ko.txt"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Normalize line endings
content = content.replace("\r\n", "\n").replace("\r", "\n")

lines = content.split("\n")
cleaned_lines = []

hangul_re = re.compile(r'[\uac00-\ud7a3\u3130-\u318f]')

for line in lines:
    line_strip = line.strip()
    if not line_strip:
        # Keep empty lines to preserve paragraph separation
        cleaned_lines.append("")
    elif hangul_re.search(line_strip):
        # Keep lines containing Hangul
        cleaned_lines.append(line)
    else:
        # Drop lines with text but no Hangul
        print("Dropped line:", repr(line_strip[:80]))

# Join and clean up multiple consecutive blank lines
result_text = "\n".join(cleaned_lines)
# Replace 3 or more newlines with 2 newlines (double newline)
result_text = re.sub(r'\n{3,}', '\n\n', result_text)

with open(path, "w", encoding="utf-8-sig") as out:
    out.write(result_text.strip() + "\n")

print("Cleanup complete!")
