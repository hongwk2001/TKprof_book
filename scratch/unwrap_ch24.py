import re
import os

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_24.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paragraphs = []
for block in text.split('\n\n'):
    block = block.strip()
    if block:
        # Join lines in block to unwrap
        # also remove lines with asterisks like *       *       *       *       *
        if block.startswith('*') and block.endswith('*'):
            paragraphs.append(block)
        else:
            unwrapped = " ".join(block.split())
            paragraphs.append(unwrapped)

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch24_en.txt', 'w', encoding='utf-8') as f:
    for p in paragraphs:
        f.write(p + '\n\n')

print(f"Total non-empty paragraphs: {len(paragraphs)}")
