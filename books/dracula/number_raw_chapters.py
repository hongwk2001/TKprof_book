import os
import re

def number_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by double/multiple newlines and clean whitespace
    raw_paras = content.split('\n\n')
    paras = []
    for p in raw_paras:
        # Replace carriage returns and strip
        p_clean = p.replace('\r', '').strip()
        if p_clean:
            paras.append(p_clean)
            
    # Re-apply tags, preserving the original formatting of the body
    tagged = []
    for i, p in enumerate(paras, 1):
        # Remove any existing [Pxxx] tag if somehow present
        p_no_tag = re.sub(r'^\[P\d+\]\s*', '', p)
        tagged.append(f"[P{i:03d}] {p_no_tag}")
        
    # Write back in-place
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(tagged))
    print(f"Numbered {path}: {len(tagged)} paragraphs.")

def main():
    base = 'books/dracula/chapters'
    for i in range(1, 28):
        ch = f'{i:02d}'
        raw_path = os.path.join(base, f'raw_ch_{ch}.txt')
        if os.path.exists(raw_path):
            number_file(raw_path)

if __name__ == '__main__':
    main()
