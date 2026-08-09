import os
import re

def normalize_text(text):
    # Remove tags like [P001]
    text = re.sub(r'\[P\d+\]', '', text)
    # Lowercase
    text = text.lower()
    # Remove all punctuation and non-alphanumeric chars, keep only words
    words = re.findall(r'\b\w+\b', text)
    return words

def audit():
    base = 'books/dracula/chapters'
    print(f"{'Ch':>4} | {'Raw Words':>10} | {'Chunk Words':>11} | {'Diff (Words)':>12} | Status")
    print("-" * 60)
    
    corrupted_chapters = []
    
    for i in range(1, 28):
        ch = f'{i:02d}'
        raw_path = os.path.join(base, f'raw_ch_{ch}.txt')
        en_path = os.path.join(base, f'ch{ch}_en.txt')
        
        if not os.path.exists(raw_path) or not os.path.exists(en_path):
            continue
            
        with open(raw_path, 'r', encoding='utf-8') as f:
            raw_words = normalize_text(f.read())
            
        with open(en_path, 'r', encoding='utf-8') as f:
            en_words = normalize_text(f.read())
            
        len_raw = len(raw_words)
        len_en = len(en_words)
        diff = abs(len_raw - len_en)
        
        status = "✅ MATCH"
        
        # We allow a very tiny difference due to hyphenation parsing differences etc (e.g. < 5 words)
        if diff > 10 or len_raw == 0:
            status = "🔴 CORRUPTED"
            corrupted_chapters.append(i)
            
        print(f"{i:>4} | {len_raw:>10} | {len_en:>11} | {diff:>12} | {status}")
        
    print("-" * 60)
    print(f"Total Corrupted Chapters: {len(corrupted_chapters)}")
    if corrupted_chapters:
        print(f"Chapters needing restore: {corrupted_chapters}")

if __name__ == '__main__':
    audit()
