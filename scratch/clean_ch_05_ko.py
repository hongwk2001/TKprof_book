import os
import re

path = r"d:\git_repo\TKprof_book\books\frankenstein\chapters\ch_05_ko.txt"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

paragraphs = content.split("\n\n")
filtered_paragraphs = []

# Regex to detect Hangul characters
hangul_re = re.compile(r'[\uac00-\ud7a3\u3130-\u318f]')

for p in paragraphs:
    p_strip = p.strip()
    if not p_strip:
        continue
    # Keep if it contains Hangul
    if hangul_re.search(p_strip):
        filtered_paragraphs.append(p_strip)
    else:
        # Also keep if it looks like a chapter header translated (though chapter headers in Chapter 5 are like "제17장", which contains Hangul)
        # Just print dropped paragraph to verify
        print("Dropped:", repr(p_strip[:60]))

clean_content = "\n\n".join(filtered_paragraphs)

# Save back to file
with open(path, "w", encoding="utf-8-sig") as out:
    out.write(clean_content)

print(f"Cleaned file saved. Old paragraphs: {len(paragraphs)}, New paragraphs: {len(filtered_paragraphs)}")
