import glob
import os
import sys

# Configure stdout for UTF-8
sys.stdout.reconfigure(encoding='utf-8')

files = [
    'books/seneca_on_happiness/copyright_ko.txt',
    'books/seneca_shortness_of_life/copyright_ko.txt',
    'books/thirty_six_stratagems/copyright_en.txt'
]

for f in files:
    if os.path.exists(f):
        print("="*40)
        print(f)
        print("="*40)
        with open(f, 'r', encoding='utf-8') as file:
            text = file.read()
        print(repr(text))
