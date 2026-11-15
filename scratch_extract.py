import json
import sys

def main():
    file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_07.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open('c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_07_extract.txt', 'w', encoding='utf-8') as f:
        f.write(f"Total: {len(data)}\n")
        for d in data:
            if not d.get('ko'):
                f.write(f"TAG: {d['tag']}\nIS_HEADER: {d['is_header']}\nRAW: {d['raw']}\n\n")

if __name__ == '__main__':
    main()
