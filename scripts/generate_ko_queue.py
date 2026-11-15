import json
import glob
import os
import re

files = glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/book*.json')
queue = []
english_pattern = re.compile(r'[a-zA-Z]')

for file_path in sorted(files):
    file_name = os.path.basename(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for block in data:
        ko_text = block.get('ko', '').strip()
        if not ko_text or english_pattern.search(ko_text):
            queue.append({
                'file_name': file_name,
                'id': block['id'],
                'target_en': block.get('en', ''),
                'status': 'pending'
            })

with open('c:/git_repo/TKprof_book/work_queue.json', 'w', encoding='utf-8') as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)

print(f'Generated work_queue.json with {len(queue)} pending blocks.')
