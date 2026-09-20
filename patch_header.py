import json
file_path = 'c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_24.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if item.get('tag') == 'H001':
        item['ko'] = '[2부 24장: 천연자석 바위로 이끌려]'
        item['en'] = ''

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

queue_path = 'c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json'
with open(queue_path, 'r', encoding='utf-8') as f:
    queue = json.load(f)

for batch in queue:
    if batch.get('batch_id') == 'book2_ch_24.json__batch0000':
        batch['status'] = 'done'

with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)

print('Header patched and work queue updated.')
