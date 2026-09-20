import json

def get_missing():
    with open('c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_15.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    missing = [b for b in data if b['ko'] == '' and not b['is_header']]
    
    with open('c:/git_repo/TKprof_book/missing_blocks.json', 'w', encoding='utf-8') as f:
        json.dump(missing, f, indent=2, ensure_ascii=False)
        
get_missing()
