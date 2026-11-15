import json

with open('c:/git_repo/TKprof_book/work_queue.json', 'r', encoding='utf-8') as f:
    queue = json.load(f)

subset = queue[261:348]

with open('c:/git_repo/TKprof_book/blocks_to_translate.json', 'w', encoding='utf-8') as f:
    json.dump(subset, f, indent=2, ensure_ascii=False)
