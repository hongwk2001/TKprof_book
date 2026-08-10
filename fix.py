import re

with open('c:/git_repo/TKprof_book/books/dracula/chapters/ch10_ko.txt', 'r', encoding='utf-8') as f:
    text = f.read()

paragraphs = re.split(r'\[P\d{3}\]', text)[1:]
paragraphs = [p.strip() for p in paragraphs]

p26_orig = paragraphs[25]
idx1 = p26_orig.find('주저앉았기 때문이다.') + len('주저앉았기 때문이다.')
part1 = p26_orig[:idx1].strip()

idx2 = p26_orig.rfind('"당신이 아가씨를 도와야 합니다.')
part2 = p26_orig[idx2:].strip()

paragraphs[25] = part1 + ' ' + part2

with open('c:/git_repo/TKprof_book/books/dracula/chapters/aligned_ko_ch10.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(paragraphs))

print('Total paragraphs:', len(paragraphs))
