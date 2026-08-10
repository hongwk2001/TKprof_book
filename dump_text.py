import json

with open('books/dracula/chunk_tasks/ch12_tasks.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

with open('dump.txt', 'w', encoding='utf-8') as out:
    for item in d:
        out.write(f"ID: {item['paragraph_index']}\n")
        for i, e in enumerate(item['english_chunks']):
            out.write(f"E{i}: {e}\n")
        out.write(f"KOR:\n{item['korean_original']}\n")
        out.write("-" * 40 + "\n")
