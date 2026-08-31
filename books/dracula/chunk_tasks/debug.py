import json

with open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch09_tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/debug.txt', 'w', encoding='utf-8') as out:
    for item in data:
        out.write(f"Paragraph {item['paragraph_index']}:\n")
        out.write("English Chunks:\n")
        for i, ec in enumerate(item["english_chunks"]):
            out.write(f"  {i}: {ec[:50]}...{ec[-50:]}\n")
        out.write(f"Korean starts: {item['korean_original'][:100]}\n")
        out.write(f"Korean ends: {item['korean_original'][-100:]}\n")
        out.write("-" * 80 + "\n")
