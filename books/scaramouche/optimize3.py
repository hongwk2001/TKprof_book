import re, glob

def process_text(text):
    text = re.sub(r'\bhitherto\b', 'until now', text, flags=re.IGNORECASE)
    text = re.sub(r'\bwhereby\b', 'by which', text, flags=re.IGNORECASE)
    text = re.sub(r'\bthereafter\b', 'after that', text, flags=re.IGNORECASE)
    text = re.sub(r'\btherein\b', 'in there', text, flags=re.IGNORECASE)
    text = re.sub(r'\blest\b', 'in case', text, flags=re.IGNORECASE)
    
    paragraphs = text.split('\n')
    new_paragraphs = []
    for p in paragraphs:
        if not p.strip():
            new_paragraphs.append(p)
            continue
            
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9\"\'\“\‘])', p)
        new_sentences = []
        for s in sentences:
            if len(s.split()) > 25:
                match = re.search(r', (and|but|so) |; ', s)
                if match:
                    idx = match.start()
                    part1 = s[:idx] + '.'
                    
                    part2_start = match.end()
                    part2 = s[part2_start:]
                    if len(part2) > 0:
                        part2 = part2[0].upper() + part2[1:]
                    
                    new_sentences.append(part1)
                    new_sentences.append(part2)
                else:
                    new_sentences.append(s)
            else:
                new_sentences.append(s)
        new_paragraphs.append(' '.join(new_sentences))
    return '\n'.join(new_paragraphs)

for f in glob.glob('d:/git_repo/TKprof_book/books/scaramouche/chapters/book_3/ch_*_en.txt'):
    with open(f, 'r', encoding='utf-8') as file:
        text = file.read()
    
    new_text = process_text(text)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_text)

def clean_ko(text):
    text = text.replace('  ', ' ')
    text = text.replace(' .', '.')
    text = text.replace(' ,', ',')
    text = text.replace(' ?', '?')
    text = text.replace(' !', '!')
    return text

for f in glob.glob('d:/git_repo/TKprof_book/books/scaramouche/chapters/book_3/ch_*_ko.txt'):
    with open(f, 'r', encoding='utf-8') as file:
        text = file.read()
    
    new_text = clean_ko(text)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_text)

print('Optimization for Book 3 done.')
