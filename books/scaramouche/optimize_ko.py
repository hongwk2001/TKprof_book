import glob

def clean_ko(text):
    # Fix double spaces
    text = text.replace('  ', ' ')
    # Fix spacing before punctuation
    text = text.replace(' .', '.')
    text = text.replace(' ,', ',')
    text = text.replace(' ?', '?')
    text = text.replace(' !', '!')
    return text

for f in glob.glob('d:/git_repo/TKprof_book/books/scaramouche/chapters/book_1/ch_*_ko.txt'):
    with open(f, 'r', encoding='utf-8') as file:
        text = file.read()
    
    new_text = clean_ko(text)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_text)

print("Korean optimization done.")
