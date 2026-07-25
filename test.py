import sys
import re

def process_file():
    with open('books/the_enchanted_april/chapters/ch_01_ko.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(text[:500])
    print("\n--- Quotes ---\n")
    quotes = re.findall(r'([“"”].*?[“"”])', text)
    if not quotes:
        quotes = re.findall(r'([\'‘].*?[\'’])', text)
    for q in quotes[:10]:
        print(q)

if __name__ == '__main__':
    process_file()
