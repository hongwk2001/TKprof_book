import json
import sys

def main():
    try:
        input_data = sys.stdin.read()
        updates = json.loads(input_data)
        
        with open('c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_06.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        update_map = {item['tag']: item for item in updates}
        count = 0
        for i, item in enumerate(data):
            if item['tag'] in update_map:
                data[i]['en'] = update_map[item['tag']]['en']
                data[i]['ko'] = update_map[item['tag']]['ko']
                count += 1
                
        with open('c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_06.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Updated {count} items successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
