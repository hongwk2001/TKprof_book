import re
import os
from bs4 import BeautifulSoup

html_path = r'C:\Users\hongw\.gemini\antigravity\brain\b51f772a-c706-4b0f-bb91-3048de8ff7b0\.system_generated\steps\76\content.md'
out_dir = r'D:\git_repo\TKprof_book\books\beowulf\chapters'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# remove the frontmatter
html = re.sub(r'^.*?---', '', html, flags=re.DOTALL)

soup = BeautifulSoup(html, 'html.parser')
os.makedirs(out_dir, exist_ok=True)

current_chapter = 'Prologue'
chapters = {current_chapter: []}

# Find all relevant tags in order
for tag in soup.find_all(['span', 'p', 'tr']):
    text = tag.get_text(strip=True)
    if re.fullmatch(r'[IVXLC]+', text):
        current_chapter = 'Chapter_' + text
        if current_chapter not in chapters:
            chapters[current_chapter] = []
    elif tag.name == 'tr':
        tds = tag.find_all('td')
        if len(tds) >= 1:
            oe_text = tds[0].get_text(' ', strip=True)
            if oe_text:
                # Add only unique lines to avoid duplicating if multiple tags match
                if not chapters[current_chapter] or chapters[current_chapter][-1] != oe_text:
                    chapters[current_chapter].append(oe_text)

for chap, lines in chapters.items():
    if lines:
        with open(os.path.join(out_dir, f'{chap}.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
