import os

def assemble(lang):
    folder = f'chunks_{lang}'
    out_file = f'book4_ch01_{lang}.txt'
    
    # Sort files correctly
    files = sorted(os.listdir(folder))
    
    with open(out_file, 'w', encoding='utf-8') as outfile:
        for fname in files:
            with open(os.path.join(folder, fname), 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write('\n\n')

if __name__ == '__main__':
    assemble('ko')
    assemble('en')
    print("Assembly complete.")
