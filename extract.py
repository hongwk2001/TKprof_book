import json

data = json.load(open('books/dracula/chunk_tasks/ch08_tasks.json', encoding='utf-8'))
with open('extracted.md', 'w', encoding='utf-8') as f:
    for d in data:
        f.write(f"\n--- PARA {d['paragraph_index']} ---\n")
        for i, c in enumerate(d['english_chunks']):
            f.write(f"E{i}: {c[:60].strip()}\n")
        f.write("KOREAN:\n")
        f.write(d['korean_original'] + "\n")
