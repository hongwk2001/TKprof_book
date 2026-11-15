import os

chapters = ['ch20', 'ch21', 'ch23', 'ch24']
base_dir = 'C:/git_repo/TKprof_book/books/dracula/chapters'

for ch in chapters:
    filepath = os.path.join(base_dir, f'{ch}_ko.txt')
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paragraphs = [p for p in content.split('\n\n') if p.strip()]
    
    chunk_size = 20
    for i in range(0, len(paragraphs), chunk_size):
        chunk = paragraphs[i:i+chunk_size]
        chunk_idx = i // chunk_size + 1
        outpath = os.path.join(base_dir, f'{ch}_ko_chunk_{chunk_idx}.txt')
        with open(outpath, 'w', encoding='utf-8') as out_f:
            out_f.write('\n\n'.join(chunk))
        print(f"Created {outpath} with {len(chunk)} paragraphs")
