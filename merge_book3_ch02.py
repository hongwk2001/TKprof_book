import os
import glob

def merge_chunks(base_dir, lang, output_file):
    pattern = os.path.join(base_dir, 'chunks', f'chunk_*_{lang}.txt')
    chunks = sorted(glob.glob(pattern))
    
    if not chunks:
        print(f"No chunks found for {lang} in {base_dir}\\chunks\\")
        return
        
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for chunk_file in chunks:
            with open(chunk_file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                # Add a newline between chunks just in case
                outfile.write('\n')
    print(f"Successfully merged {len(chunks)} {lang} chunks into {output_file}")

if __name__ == '__main__':
    base_dir = r"d:\git_repo\TKprof_book\books\tono_bungay\chapters\book3"
    
    # Merge Korean chunks
    merge_chunks(base_dir, 'ko', os.path.join(base_dir, 'book3_ch02_ko.txt'))
    
    # Merge English chunks
    merge_chunks(base_dir, 'en', os.path.join(base_dir, 'book3_ch02_en.txt'))
