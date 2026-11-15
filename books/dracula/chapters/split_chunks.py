import os

input_file = 'C:/git_repo/TKprof_book/books/dracula/chapters/ch21_ko.txt'
with open(input_file, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f if line.strip()]

print(f"Total paragraphs: {len(lines)}")

for i in range(0, len(lines), 20):
    chunk = lines[i:i+20]
    out_name = f'C:/git_repo/TKprof_book/books/dracula/chapters/scratch_ko_chunk_{i//20}.txt'
    with open(out_name, 'w', encoding='utf-8') as out:
        out.write('\n\n'.join(chunk))
    print(f"Wrote {len(chunk)} paragraphs to {out_name}")
