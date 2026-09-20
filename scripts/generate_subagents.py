import json

subs = []
chunk_size = 739
for i in range(10):
    start = i * chunk_size
    end = min((i + 1) * chunk_size, 7383)
    prompt = f"""URGENT TRANSLATION TASK (Indices {start} to {end-1}):
1. Read `c:/git_repo/TKprof_book/work_queue.json`.
2. You are responsible for EXACTLY blocks at index {start} through {end-1}.
3. For each block, translate `target_en` (Modernized English) to natural Korean (`ko`). Use `prev_context` and `next_context` to understand fragments.
4. OBEY THIS GLOSSARY STRICTLY: Defarge(드파르지), Lorry(로리), Manette(마네트), Saint Antoine(생탕투안), Tellson(텔슨), Evrémonde(에브레몽드), Charles Darnay(찰스 다네이), Lucie(루시), Carton(카턴), Pross(프로스), Stryver(스트라이버), Cruncher(크런처), Gaspard(가스파르).
5. DO NOT TRANSLATE THEM ALL AT ONCE! Translate in batches of 50.
6. For each batch, use `write_to_file` to save a JSON array of dicts to `c:/git_repo/TKprof_book/translated_batches/batch_{i}_partX.json`.
   Example dict: {{"file": "book1_ch_01.json", "id": 1, "ko": "..."}}
7. Do not stop until you have saved all {end-start} blocks.
8. NEVER leave English words in the `ko` field.
"""
    subs.append({
        'TypeName': 'ChapterWorker',
        'Role': f'Translator {i} ({start}-{end})',
        'Prompt': prompt,
        'Model': 'pro'
    })

with open('c:/git_repo/TKprof_book/subagents.json', 'w', encoding='utf-8') as f:
    json.dump(subs, f, ensure_ascii=False)
