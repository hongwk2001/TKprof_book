import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json', 'r', encoding='utf-8') as f:
    q = json.load(f)

my_batches = [b for b in q if b['chapter'] == 'book2_ch_03' and b['status'] == 'pending']
print(f"Found {len(my_batches)} pending batches for book2_ch_03")

if my_batches:
    print(f"Batch 0 items: {len(my_batches[0]['items'])}")
