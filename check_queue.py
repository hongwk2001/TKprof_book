import json
with open('c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)
for q in queue:
    if q.get('chapter') == 'book2_ch_03' and q.get('status') == 'pending':
        print(f"Batch ID: {q['batch_id']}, blocks: {len(q['block_ids'])}")
        print(q['block_ids'][:5], '...', q['block_ids'][-5:])
