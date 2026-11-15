import os

out_file = 'C:/git_repo/TKprof_book/books/dracula/chapters/ch21_en.txt'
chunks = [
    'C:/git_repo/TKprof_book/books/dracula/chapters/scratch_en_chunk_0.txt',
    'C:/git_repo/TKprof_book/books/dracula/chapters/scratch_en_chunk_1.txt',
    'C:/git_repo/TKprof_book/books/dracula/chapters/scratch_en_chunk_2.txt',
    'C:/git_repo/TKprof_book/books/dracula/chapters/scratch_en_chunk_3.txt'
]

all_paragraphs = []
for chunk_file in chunks:
    with open(chunk_file, 'r', encoding='utf-8') as f:
        # read paragraphs, split by double newline or more
        content = f.read().strip()
        paras = [p for p in content.split('\n\n') if p.strip()]
        all_paragraphs.extend(paras)

print(f"Total translated paragraphs: {len(all_paragraphs)}")

with open(out_file, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(all_paragraphs) + '\n')
