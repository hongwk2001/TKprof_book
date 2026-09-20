import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_06.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

empty_blocks = [item for item in data if not item.get('en') or not item.get('ko')]
batches = [empty_blocks[i:i+10] for i in range(0, len(empty_blocks), 10)]

subagents = []
for i, batch in enumerate(batches[:5]):
    prompt = f"Please translate these {len(batch)} blocks. The 'raw' text is provided. Translate it to Korean for 'ko', and copy or clean up the English for 'en'. Return ONLY a JSON array where each object has 'tag', 'en', and 'ko' fields.\n\n"
    for item in batch:
        prompt += f"Tag: {item['tag']}\nRaw: {item['raw']}\n\n"
    
    subagents.append({
        'TypeName': 'SegmentTranslator',
        'Role': f'Translator Batch',
        'Prompt': prompt,
        'Model': 'flash'
    })

with open('c:/git_repo/TKprof_book/next.json', 'w', encoding='utf-8') as f:
    json.dump(subagents, f, ensure_ascii=False)
