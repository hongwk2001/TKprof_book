import os
import json

def apply_aligned_chunks():
    for i in range(1, 28):
        ch = f'ch{i:02d}'
        en_file = f'books/dracula/chapters/{ch}_en.txt'
        ko_file = f'books/dracula/chapters/{ch}_ko.txt'
        tasks_file = f'books/dracula/chunk_tasks/{ch}_tasks.json'
        aligned_file = f'books/dracula/chunk_tasks/{ch}_aligned.json'
        
        if not os.path.exists(en_file) or not os.path.exists(ko_file):
            continue
            
        with open(en_file, 'r', encoding='utf-8') as f:
            en_paras = [p for p in f.read().split('\n\n') if p.strip()]
            
        with open(ko_file, 'r', encoding='utf-8') as f:
            ko_paras = [p for p in f.read().split('\n\n') if p.strip()]
            
        aligned_data = {}
        if os.path.exists(aligned_file):
            with open(aligned_file, 'r', encoding='utf-8', errors='replace') as f:
                try:
                    data = json.load(f)
                    for item in data:
                        aligned_data[item['paragraph_index']] = item['korean_chunks']
                except Exception as e:
                    print(f"Error parsing {aligned_file}: {e}")
                    
        tasks_data = {}
        if os.path.exists(tasks_file):
            with open(tasks_file, 'r', encoding='utf-8', errors='replace') as f:
                try:
                    data = json.load(f)
                    for item in data:
                        tasks_data[item['paragraph_index']] = item['english_chunks']
                except Exception as e:
                    print(f"Error parsing {tasks_file}: {e}")
                    
        new_en_paras = []
        new_ko_paras = []
        
        for p_idx in range(len(en_paras)):
            if p_idx in tasks_data and p_idx in aligned_data:
                en_chunks = tasks_data[p_idx]
                ko_chunks = aligned_data[p_idx]
                
                # Check if counts match. If not, fallback to original to avoid parity break
                if len(en_chunks) == len(ko_chunks):
                    # Preserve tags from the original paragraphs if they exist
                    import re
                    en_match = re.match(r'^(\[P\d+\])\s+', en_paras[p_idx])
                    ko_match = re.match(r'^(\[P\d+\])\s+', ko_paras[p_idx])
                    
                    ko_chunks = [k if k.strip() else '...' for k in ko_chunks]
                    
                    if en_match:
                        en_chunks[0] = en_match.group(1) + ' ' + en_chunks[0]
                    if ko_match:
                        ko_chunks[0] = ko_match.group(1) + ' ' + ko_chunks[0]
                        
                    new_en_paras.extend(en_chunks)
                    new_ko_paras.extend(ko_chunks)
                else:
                    print(f"WARNING: Chunk count mismatch in {ch} para {p_idx}. EN: {len(en_chunks)}, KO: {len(ko_chunks)}. Falling back to original.")
                    new_en_paras.append(en_paras[p_idx])
                    new_ko_paras.append(ko_paras[p_idx])
            else:
                new_en_paras.append(en_paras[p_idx])
                new_ko_paras.append(ko_paras[p_idx])
                
        # Write back to files
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(new_en_paras))
            
        with open(ko_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(new_ko_paras))
            
        print(f"Processed {ch}. Final paragraphs: {len(new_en_paras)}")

if __name__ == '__main__':
    apply_aligned_chunks()
