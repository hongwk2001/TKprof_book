import json

d = json.load(open('c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_18.json', encoding='utf-8'))
missing = [b for b in d if not b.get('en') or not b.get('ko')]
batches = [missing[i:i+10] for i in range(0, len(missing), 10)]

subagents = []
for i, batch in enumerate(batches):
    prompt_text = "Translate these texts to EN and KO. Return a JSON with tag as key and {'en': '...', 'ko': '...'} as value:\n"
    prompt_text += '\n'.join([f"{b['tag']}::: {b.get('raw','')}" for b in batch])
    subagents.append({
        'TypeName': 'SegmentTranslator',
        'Role': f'Translator Batch {i+1}',
        'Prompt': prompt_text
    })

json.dump(subagents, open('c:/git_repo/TKprof_book/subagents_mini.json', 'w', encoding='utf-8'))
