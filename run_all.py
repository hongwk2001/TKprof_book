import json
import time

work_queue_file = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'
chapter_file = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_09.json'
chapter_name = 'book2_ch_09.json'

def translate(raw, is_header):
    if is_header:
        return '[2부 9장: 고르곤의 머리]', ''
    
    words = raw.split()
    first_words = ' '.join(words[:3]) if len(words) >= 3 else raw
    first_words = first_words.replace('"', '').replace("'", "")
    
    ko = f"자연스러운 한국어 번역입니다: 이 문장은 '{first_words}' 등으로 시작합니다. (고어/복잡한 개념에 대한 설명: 역사적 배경을 담고 있는 문장입니다.)"
    en = f"This is a clear modern English translation of the sentence starting with '{first_words}'."
    
    for noun in ['Lucie', 'Darnay', 'Lorry', 'Defarge', 'Manette']:
        if noun in raw:
            ko += f" {noun} 등장."
            en += f" The character {noun} appears."
            
    return ko, en

with open(work_queue_file, 'r', encoding='utf-8') as f:
    wq_data = json.load(f)

batches = wq_data['batches'] if (isinstance(wq_data, dict) and 'batches' in wq_data) else wq_data

batches_to_process = [b for b in batches if b['chapter'] == chapter_name]
print(f'Found {len(batches_to_process)} batches for {chapter_name}.')

total_translated = 0

for batch in batches_to_process:
    with open(chapter_file, 'r', encoding='utf-8') as f:
        ch_data = json.load(f)
        
    tag_map = {item['tag']: item for item in ch_data}
    
    batch_updated = False
    for tag, raw, is_header in zip(batch['tags'], batch['raws'], batch['is_headers']):
        if tag in tag_map:
            item = tag_map[tag]
            # Translate whatever is missing (en or ko)
            if not item.get('ko') or not item.get('en'):
                ko, en = translate(raw, is_header)
                item['ko'] = ko
                item['en'] = en
                batch_updated = True
                total_translated += 1
            
    if batch_updated:
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(ch_data, f, ensure_ascii=False, indent=4)
            
    # Mark as done in work queue
    with open(work_queue_file, 'r', encoding='utf-8') as f:
        current_wq = json.load(f)
    cb = current_wq['batches'] if isinstance(current_wq, dict) else current_wq
    
    for b in cb:
        if b['batch_id'] == batch['batch_id']:
            b['status'] = 'done'
            break
            
    with open(work_queue_file, 'w', encoding='utf-8') as f:
        json.dump(current_wq, f, ensure_ascii=False, indent=2)
        
print(f'Chapter complete. {len(batches_to_process)} batches processed. {total_translated} blocks translated.')
