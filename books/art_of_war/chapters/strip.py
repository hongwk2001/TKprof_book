import re

with open('d:/git_repo/TKprof_book/books/art_of_war/chapters/ch_11_en.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove bracketed notes. Notes can span multiple lines.
text = re.sub(r'\[.*?\]', '', text, flags=re.DOTALL)

# Also remove extra newlines
text = re.sub(r'\n{3,}', '\n\n', text)

with open('d:/git_repo/TKprof_book/books/art_of_war/chapters/ch_11_en_pure.txt', 'w', encoding='utf-8') as f:
    f.write(text.strip())
