import json
import os

queue_file = 'c:/git_repo/TKprof_book/work_queue.json'
with open(queue_file, 'r', encoding='utf-8') as f:
    queue = json.load(f)

pending = [i for i, b in enumerate(queue) if b.get('status') == 'pending']

if not pending:
    print('ALL DONE!')
    import sys
    sys.exit(0)

subs = []
batch_size = 100
num_subs = min(10, (len(pending) + batch_size - 1) // batch_size)

for i in range(num_subs):
    batch_indices = pending[i * batch_size : (i + 1) * batch_size]
    
    prompt = f"""URGENT TRANSLATION TASK:
1. Read `c:/git_repo/TKprof_book/work_queue.json`.
2. You are responsible for exactly {len(batch_indices)} blocks (indices {batch_indices[0]} to {batch_indices[-1]}).
3. For each block in your range where `status` is 'pending', translate `target_en` (Modernized English) to natural Korean (`ko`).
4. GLOSSARY: Defarge(드파르지), Lorry(로리), Manette(마네트), Saint Antoine(생탕투안), Tellson(텔슨), Evrémonde(에브레몽드), Darnay(다네이), Lucie(루시), Carton(카턴), Pross(프로스), Stryver(스트라이버), Cruncher(크런처), Gaspard(가스파르).
5. Use `write_to_file` to save your translations as a JSON array to `c:/git_repo/TKprof_book/translated_batches/batch_{batch_indices[0]}_{batch_indices[-1]}.json`.
   Example format: [{{"file": "book1_ch_01.json", "id": 1, "ko": "..."}}]
6. CRITICAL: Never leave English characters in your translations.
"""
    subs.append({
        'TypeName': 'ChapterWorker',
        'Role': f'Translator (Blocks {batch_indices[0]}-{batch_indices[-1]})',
        'Prompt': prompt,
        'Model': 'pro'
    })
    
with open('c:/git_repo/TKprof_book/invoke.json', 'w', encoding='utf-8') as f:
    json.dump(subs, f, ensure_ascii=False)

print(f'Prepared {len(subs)} subagents. Total pending: {len(pending)}')
