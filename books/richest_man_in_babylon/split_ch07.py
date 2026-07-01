import os

def split_file(filepath, num_parts=3):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paragraphs = content.split('\n\n')
    chunk_size = len(paragraphs) // num_parts + 1
    
    base_name = os.path.basename(filepath).replace('.txt', '')
    dir_name = os.path.dirname(filepath)
    
    for i in range(num_parts):
        chunk = paragraphs[i*chunk_size : (i+1)*chunk_size]
        if not chunk:
            continue
        
        out_path = os.path.join(dir_name, f"{base_name}_part{i+1}.txt")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(chunk))
        print(f"Created {out_path}")

split_file('d:/git_repo/TKprof_book/books/richest_man_in_babylon/chapters/raw_ch_07_meet_the_goddess_of_good_luck.txt', 3)
