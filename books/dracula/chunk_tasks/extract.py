import json

def get_summary(text):
    return text[:40] + " ... " + text[-40:]

with open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch09_tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("English chunks:")
for item in data:
    print(f"\n--- Paragraph {item['paragraph_index']} ---")
    for i, ec in enumerate(item['english_chunks']):
        print(f" E{i}: {get_summary(ec)}")

print("\n\nKorean original:")
for item in data:
    print(f"\n--- Paragraph {item['paragraph_index']} ---")
    print(f" K: {get_summary(item['korean_original'])}")
