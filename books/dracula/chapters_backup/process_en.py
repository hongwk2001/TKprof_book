import re
import sys

def process_english(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split by double newlines to get paragraphs
    paragraphs = re.split(r'\n\n+', text)
    
    cleaned_paragraphs = []
    for p in paragraphs:
        # Strip leading/trailing whitespace
        p = p.strip()
        if not p:
            continue
        
        # Replace single newlines with a space
        p = re.sub(r'\n', ' ', p)
        # Replace multiple spaces with a single space
        p = re.sub(r' +', ' ', p)
        
        # Standardize quotes (replace smart quotes with straight double quotes)
        p = p.replace('“', '"').replace('”', '"')
        p = p.replace('‘', "'").replace('’', "'")
        
        cleaned_paragraphs.append(p)
        
    with open(output_file, 'w', encoding='utf-8') as f:
        for p in cleaned_paragraphs:
            f.write(p + '\n')
            
    print(f"Wrote {len(cleaned_paragraphs)} paragraphs to {output_file}")

if __name__ == "__main__":
    process_english(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_15.txt', r'c:\git_repo\TKprof_book\books\dracula\chapters\ch15_en.txt')
