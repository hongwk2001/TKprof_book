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

output = '# Random 30 Paragraph Audit (Set 2)\n\n'
for i, block in enumerate(sampled, 1):
    output += f"## Sample {i} ({block['file']} ID {block['id']})\n"
    output += f"**Raw (Original English):**\n{block['raw']}\n\n"
    output += f"**Modernized English (en):**\n{block['en']}\n\n"
    output += f"**Korean (ko):**\n{block['ko']}\n\n"
    output += '---\n\n'

with open(r'C:\Users\hongw\.gemini\antigravity\brain\c6a5c102-f9fe-450d-a245-40c618981c84\random_30_audit_2.md', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Generated second audit report for 30 blocks out of {len(all_blocks)}.")
