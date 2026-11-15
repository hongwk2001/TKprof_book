import json
import re

text = open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch02_ko.txt', encoding='utf-8').read()
text = re.sub(r'\[P\d{3}\]', '', text)
text = text.replace('\n', ' ')
text = re.sub(r'\s+', ' ', text).strip()

# Split into sentences roughly
sents = re.split(r'(?<=[.!?])\s+(?=[가-힣"\'A-Z0-9*-])', text)

with open('ko_sents.json', 'w', encoding='utf-8') as f:
    json.dump(sents, f, ensure_ascii=False, indent=2)
