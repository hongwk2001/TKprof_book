import os
import re

def clean_tag(text):
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())

def main():
    # Let's check Ch 13 Para 20 (P020) and Ch 15 Para 103 (P105)
    
    # 1. Ch 13 P020
    print("=== Ch 13 P020 Comparison ===")
    with open('books/dracula/chapters_backup/raw_ch_13.txt', 'r', encoding='utf-8') as f:
        raw_13 = [p.strip() for p in f.read().split('\n\n') if p.strip()]
    with open('books/dracula/chapters/ch13_en.txt', 'r', encoding='utf-8') as f:
        en_13 = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        
    p020_en = next(p for p in en_13 if p.startswith('[P020]'))
    print("RAW:")
    print(raw_13[19]) # 20th paragraph (0-indexed 19)
    print("\nMODERNIZED:")
    print(clean_tag(p020_en))
    
    print("\n" + "="*50 + "\n")
    
    # 2. Ch 15 P105 (Modernized para index 103)
    print("=== Ch 15 P105 Comparison ===")
    with open('books/dracula/chapters_backup/raw_ch_15.txt', 'r', encoding='utf-8') as f:
        raw_15 = [p.strip() for p in f.read().split('\n\n') if p.strip()]
    with open('books/dracula/chapters/ch15_en.txt', 'r', encoding='utf-8') as f:
        en_15 = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        
    p105_en = next(p for p in en_15 if p.startswith('[P105]'))
    print("RAW:")
    print(raw_15[104]) # 105th paragraph (0-indexed 104)
    print("\nMODERNIZED:")
    print(clean_tag(p105_en))

if __name__ == '__main__':
    main()
