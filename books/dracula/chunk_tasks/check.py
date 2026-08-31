import json

with open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch09_tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    idx = item["paragraph_index"]
    k_orig = item["korean_original"]
    print(f"Paragraph {idx}:")
    print(f"Total English Chunks: {len(item['english_chunks'])}")
    print(f"Korean length: {len(k_orig)}")
    print(f"Korean ends with: {k_orig[-100:]}")
    print()
