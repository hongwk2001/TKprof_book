import re
import json

en = open('c:/git_repo/TKprof_book/books/dracula/chapters/ch23_en.txt', encoding='utf-8').read()
ko = open('c:/git_repo/TKprof_book/books/dracula/chapters/ch23_ko.txt', encoding='utf-8').read()

en_paragraphs = [p.strip() for p in re.split(r'\[P\d+\]\s*', en) if p.strip()]
ko_paragraphs = [p.strip() for p in re.split(r'\[P\d+\]\s*', ko) if p.strip()]

ko_sentences = []
for p in ko_paragraphs:
    sents = re.split(r'(?<=[.?!])\s+(?=[A-Za-z가-힣\"\'“])', p.replace('\n', ' '))
    ko_sentences.extend(sents)

print('EN paragraphs:', len(en_paragraphs))
print('Total KO sentences:', len(ko_sentences))

with open('align_data.json', 'w', encoding='utf-8') as f:
    json.dump({'en': en_paragraphs, 'ko_sents': ko_sentences}, f, ensure_ascii=False, indent=2)
