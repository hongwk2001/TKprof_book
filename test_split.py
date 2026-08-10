
import re
ko = open('books/dracula/chapters/ch27_ko.txt', encoding='utf-8').read()
ko_clean = re.sub(r'\[P\d{3}\]', '', ko).strip()
ko_clean = re.sub(r'\n+', ' ', ko_clean)
sentences = re.split(r'(?<=[.!?])\s+', ko_clean)
print('Total sentences:', len(sentences))
for i in range(20):
    print(f'{i+1}: {sentences[i]}')

