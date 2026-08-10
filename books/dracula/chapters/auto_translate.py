import os
import re
import urllib.request
import urllib.parse
import json
import time

chapters = ['ch20', 'ch21', 'ch23', 'ch24']
base_dir = 'C:/git_repo/TKprof_book/books/dracula/chapters'

def translate_text(text):
    if not text.strip():
        return ""
    q = urllib.parse.quote(text)
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ko&tl=en&dt=t&q={q}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    retries = 3
    for attempt in range(retries):
        try:
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))
            return ''.join([sentence[0] for sentence in data[0]])
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                print(f"Failed to translate: {text[:30]}... Error: {e}")
                return "Translation Error"

for ch in chapters:
    print(f"Processing {ch}...")
    # List all chunks for this chapter
    chunk_files = sorted([f for f in os.listdir(base_dir) if f.startswith(f'{ch}_ko_chunk_') and f.endswith('.txt')], 
                         key=lambda x: int(x.split('_')[-1].split('.')[0]))
    
    en_chunks = []
    
    ko_total_paras = 0
    en_total_paras = 0
    
    for chunk_file in chunk_files:
        filepath = os.path.join(base_dir, chunk_file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        ko_total_paras += len(paragraphs)
        
        en_paragraphs = []
        for p in paragraphs:
            # Strip [Pxxx]
            clean_p = re.sub(r'^\[P\d{3}\]\s*', '', p)
            translated = translate_text(clean_p)
            en_paragraphs.append(translated)
        
        out_chunk_name = chunk_file.replace('_ko_', '_en_')
        out_chunk_path = os.path.join(base_dir, out_chunk_name)
        with open(out_chunk_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(en_paragraphs))
        
        en_chunks.append(out_chunk_path)
        print(f"Translated {chunk_file} -> {out_chunk_name}")
    
    # Merge
    final_en_path = os.path.join(base_dir, f'{ch}_en.txt')
    all_en_paragraphs = []
    for en_chunk_path in en_chunks:
        with open(en_chunk_path, 'r', encoding='utf-8') as f:
            content = f.read()
        paras = [p for p in content.split('\n\n') if p.strip()]
        all_en_paragraphs.extend(paras)
    
    with open(final_en_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(all_en_paragraphs))
    
    en_total_paras = len(all_en_paragraphs)
    
    print(f"{ch} original paragraphs: {ko_total_paras}, translated: {en_total_paras}")
    
    # Delete temporary files
    for chunk_file in chunk_files:
        os.remove(os.path.join(base_dir, chunk_file))
    for en_chunk_path in en_chunks:
        os.remove(en_chunk_path)
    print(f"Cleaned up chunks for {ch}")
