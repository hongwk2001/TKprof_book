import re

with open('books/dracula/chapters/raw_ch_27.txt', 'r', encoding='utf-8') as f:
    text = f.read()

ad_start = text.find('_There’s More to Follow!_')
if ad_start != -1:
    # Also want to remove the stars before the ad
    # Let's just find "THE END"
    end_start = text.find('THE END')
    if end_start != -1:
        text = text[:end_start + 7]

paragraphs = text.split('\n\n')

cleaned_paragraphs = []
for p in paragraphs:
    p = p.strip()
    if not p: continue
    
    if re.search(r'^\s*\*\s*\*\s*\*\s*\*\s*\*\s*$', p):
        continue
        
    # fix line wraps
    p = re.sub(r'(?<!\n)\n(?!\n)', ' ', p)
    # clean multiple spaces
    p = re.sub(r' +', ' ', p)
    p = p.strip()
    
    # replace smart quotes
    p = p.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    
    if p:
        cleaned_paragraphs.append(p)

with open('books/dracula/chapters/ch27_en.txt', 'w', encoding='utf-8') as f:
    for p in cleaned_paragraphs:
        f.write(p + '\n\n')

print(f"Wrote {len(cleaned_paragraphs)} paragraphs to ch27_en.txt")
