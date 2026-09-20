import json
import glob
import random

files = glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/book*.json')
all_blocks = []

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for block in data:
            if block.get('ko') and block.get('en') and block.get('raw'):
                all_blocks.append({
                    'file': file_path.split('\\')[-1].split('/')[-1],
                    'id': block.get('id'),
                    'raw': block.get('raw'),
                    'en': block.get('en'),
                    'ko': block.get('ko')
                })

sampled = random.sample(all_blocks, 30)

with open('c:/git_repo/TKprof_book/random_30_audit.md', 'w', encoding='utf-8') as f:
    f.write('# Random 30 Paragraph Audit\n\n')
    for i, block in enumerate(sampled, 1):
        f.write(f"## Sample {i} ({block['file']} ID {block['id']})\n")
        f.write(f"**Raw (Original English):**\n{block['raw']}\n\n")
        f.write(f"**Modernized English (en):**\n{block['en']}\n\n")
        f.write(f"**Korean (ko):**\n{block['ko']}\n\n")
        f.write('---\n\n')

print(f"Generated audit report for 30 blocks out of {len(all_blocks)}.")
