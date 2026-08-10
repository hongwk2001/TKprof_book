import os

base = 'c:/git_repo/TKprof_book/books/dracula/chapters/'
en_parts = ['ch04_en_modern.txt', 'ch04_en_modern_part2.txt', 'ch04_en_modern_part3.txt', 'ch04_en_modern_part4.txt', 'ch04_en_modern_part5.txt']
ko_parts = ['ch04_ko_modern.txt', 'ch04_ko_modern_part2.txt', 'ch04_ko_modern_part3.txt', 'ch04_ko_modern_part4.txt', 'ch04_ko_modern_part5.txt']

def concat(parts, out_name):
    with open(base + out_name, 'w', encoding='utf-8') as out:
        for i, p in enumerate(parts):
            with open(base + p, 'r', encoding='utf-8') as f:
                out.write(f.read().strip())
            if i < len(parts) - 1:
                out.write('\n\n')

concat(en_parts, 'ch04_en_modern_final.txt')
concat(ko_parts, 'ch04_ko_modern_final.txt')

for p in en_parts:
    if p != 'ch04_en_modern.txt':
        os.remove(base + p)
for p in ko_parts:
    if p != 'ch04_ko_modern.txt':
        os.remove(base + p)

os.replace(base + 'ch04_en_modern_final.txt', base + 'ch04_en_modern.txt')
os.replace(base + 'ch04_ko_modern_final.txt', base + 'ch04_ko_modern.txt')
