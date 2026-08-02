import os

def merge_files(pattern, output_file):
    parts = []
    for i in range(1, 7):
        parts.append(f'd:/git_repo/TKprof_book/books/tono_bungay/chapters/book2/book2_ch02_{pattern}_part{i}.txt')
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for part in parts:
            if os.path.exists(part):
                with open(part, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n\n')

merge_files('ko', 'd:/git_repo/TKprof_book/books/tono_bungay/chapters/book2/book2_ch02_ko.txt')
merge_files('en', 'd:/git_repo/TKprof_book/books/tono_bungay/chapters/book2/book2_ch02_en.txt')
print("Merge complete!")
