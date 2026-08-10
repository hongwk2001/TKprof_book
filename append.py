import sys
import os

ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch25_ko_modern.txt'
en_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch25_en_modern.txt'

try:
    with open('ko_chunk.txt', 'r', encoding='utf-8') as f:
        ko = f.read()
except FileNotFoundError:
    ko = ''
    
try:
    with open('en_chunk.txt', 'r', encoding='utf-8') as f:
        en = f.read()
except FileNotFoundError:
    en = ''

with open(ko_file, 'a', encoding='utf-8') as f:
    if ko.strip():
        f.write(ko.strip() + '\n\n')

with open(en_file, 'a', encoding='utf-8') as f:
    if en.strip():
        f.write(en.strip() + '\n\n')

# Clear the chunks
with open('ko_chunk.txt', 'w', encoding='utf-8') as f:
    f.write('')
with open('en_chunk.txt', 'w', encoding='utf-8') as f:
    f.write('')

print("Appended successfully.")
