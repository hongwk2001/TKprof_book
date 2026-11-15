import glob
import re

def fix_title_splits_in_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    paras = text.split('\n\n')
    new_paras = []
    i = 0
    fixed = 0

    while i < len(paras):
        p = paras[i].strip()
        
        # Check if paragraph ends with a title like "Dr.", "Mr.", "Mrs.", "Ms.", "St.", "Prof.", "Rev."
        if i + 1 < len(paras) and re.search(r'\b(Dr|Mr|Mrs|Ms|St|Prof|Rev)\.\s*$', p):
            next_p = paras[i + 1].strip()
            # Remove the tag from next_p if it has one (e.g. [P005b])
            next_p_clean = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', next_p)
            
            # Merge next_p into current paragraph!
            merged_p = f"{p} {next_p_clean}"
            new_paras.append(merged_p)
            fixed += 1
            i += 2 # Skip next_p since it's merged
        else:
            new_paras.append(p)
            i += 1

    if fixed > 0:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(new_paras) + '\n')
        print(f"Fixed {fixed} broken title split(s) in {fpath}")

def main():
    chapters = glob.glob('chapters/ch*_en.txt')
    for fpath in chapters:
        fix_title_splits_in_file(fpath)

if __name__ == '__main__':
    main()
