import json
with open('c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_05.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

empty = [{'tag': d['tag'], 'raw': d['raw']} for d in data if not d.get('en') or not d.get('ko')]
batches = [empty[i:i+10] for i in range(0, len(empty), 10)]

subagents = []
for i, b in enumerate(batches):
    prompt = f"Translate the following blocks into Korean ('ko') and English ('en'). Return ONLY a valid JSON list of objects with keys 'tag', 'ko', 'en' for each block. Blocks:\n{json.dumps(b)}"
    subagents.append({
        'TypeName': 'SegmentTranslator',
        'Role': f'Translator Batch {i+1}',
        'Prompt': prompt,
        'Model': 'flash'
    })

with open('c:/git_repo/TKprof_book/subagents.json', 'w', encoding='utf-8') as f:
    json.dump({'Subagents': subagents}, f, indent=2)
