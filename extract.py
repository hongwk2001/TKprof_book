import json

with open('c:/git_repo/TKprof_book/work_queue.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# check indices 800 to 899
subset = data[800:900]
print(f"Indices 800-899 pending count: {sum(1 for i in subset if i.get('status') == 'pending')}")

# check id 800 to 899
id_subset = [d for d in data if 800 <= d.get('id', 0) <= 899]
print(f"IDs 800-899 pending count: {sum(1 for i in id_subset if i.get('status') == 'pending')}")

# find all pending indices
pending_indices = [i for i, d in enumerate(data) if d.get('status') == 'pending']
print(f"Total pending: {len(pending_indices)}. First 10 pending indices: {pending_indices[:10]}")
