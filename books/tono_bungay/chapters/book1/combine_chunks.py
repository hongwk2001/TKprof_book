header = 'Book 1 Chapter 1: Of Bladesover House, and My Mother; and the Constitution of Society\n\n'
with open('d:/git_repo/TKprof_book/books/tono_bungay/chapters/book1/book1_ch01_ko.txt', 'w', encoding='utf-8') as f:
    f.write(header)
    for i in range(5):
        with open(f'd:/git_repo/TKprof_book/books/tono_bungay/chapters/book1/chunks/chunk_{i:02d}_ko.txt', 'r', encoding='utf-8') as chunk_f:
            f.write(chunk_f.read().strip() + '\n\n')

with open('d:/git_repo/TKprof_book/books/tono_bungay/chapters/book1/book1_ch01_en.txt', 'w', encoding='utf-8') as f:
    f.write(header)
    for i in range(5):
        with open(f'd:/git_repo/TKprof_book/books/tono_bungay/chapters/book1/chunks/chunk_{i:02d}_en.txt', 'r', encoding='utf-8') as chunk_f:
            f.write(chunk_f.read().strip() + '\n\n')

print('Combination completed successfully.')
