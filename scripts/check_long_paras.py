import json
import glob
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
files = sorted(glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/book*_ch_*.json'))
blocks = []

for f in files:
    try:
        data = json.load(open(f, encoding='utf-8'))
        for b in data:
            if not b.get('is_header') and b.get('en'):
                en_text = b.get('en')
                blocks.append({
                    'file': f.split('/')[-1].split('\\')[-1],
                    'id': b.get('id'),
                    'word_count': len(en_text.split()),
                    'char_count': len(en_text),
                    'en': en_text
                })
    except Exception as e:
        pass

blocks.sort(key=lambda x: x['word_count'], reverse=True)

print('Top 10 longest modernized English paragraphs (by word count):')
for i in range(min(10, len(blocks))):
    print(f"{i+1}. {blocks[i]['file']} (ID {blocks[i]['id']}) - {blocks[i]['word_count']} words, {blocks[i]['char_count']} chars")
    print(f"   Preview: {blocks[i]['en'][:150]}...\n")
