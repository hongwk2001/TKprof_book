import os

def split_file(filepath, num_parts):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paragraphs = content.split('\n\n')
    chunk_size = max(1, len(paragraphs) // num_parts + 1)
    
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

dir_path = 'd:/git_repo/TKprof_book/books/richest_man_in_babylon/chapters'

split_file(os.path.join(dir_path, 'raw_ch_08_the_five_laws_of_gold.txt'), 3)
split_file(os.path.join(dir_path, 'raw_ch_09_the_gold_lender_of_babylon.txt'), 3)
split_file(os.path.join(dir_path, 'raw_ch_10_the_walls_of_babylon.txt'), 1)
split_file(os.path.join(dir_path, 'raw_ch_11_the_luckiest_man_in_babylon.txt'), 8)
