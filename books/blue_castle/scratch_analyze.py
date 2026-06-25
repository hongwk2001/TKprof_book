import os
import re

chapters_dir = 'D:/git_repo/TKprof_book/books/blue_castle/chapters'

# Terminology to check
terms = {
    'Blue Castle': ['블루 캐슬', '푸른 성'],
    'Mistawis': ['미스타위스'],
    'Lady Jane': ['레이디 제인'],
    'Barney': ['바니'],
    'Valancy': ['발랜시'],
    'Roaring Abel': ['울부짖는 아벨', '로어링 아벨']
}

long_sentences = []
punctuation_issues = []
term_counts = {k: {variant: 0 for variant in v} for k, v in terms.items()}

# Dialogue extraction
early_dialogue = []
late_dialogue = []

def extract_dialogue(line):
    matches = re.findall(r'"([^"]*)"', line)
    return matches

for i in range(1, 46):
    filename = f'ch_{i:02d}_ko.txt'
    filepath = os.path.join(chapters_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line_num, line in enumerate(lines):
        text = line.strip()
        if not text:
            continue
            
        # 1. Check sentence length (split by standard sentence enders)
        sentences = re.split(r'[.!?]\s', text)
        for s in sentences:
            # check if a chunk between commas is too long
            chunks = s.split(',')
            for chunk in chunks:
                if len(chunk) > 120:
                    long_sentences.append(f"{filename} (L{line_num+1}): {chunk[:60]}...")
                    
        # 2. Check punctuation
        if '...' in text:
            punctuation_issues.append(f"{filename} (L{line_num+1}): Contains ellipsis (...)")
        if '—' in text or '--' in text:
            punctuation_issues.append(f"{filename} (L{line_num+1}): Contains em-dash (—)")
            
        # 3. Check Terminology
        for key, variants in terms.items():
            for variant in variants:
                count = text.count(variant)
                if count > 0:
                    term_counts[key][variant] += count
                    
        # 4. Extract Dialogue for tone review
        dialogues = extract_dialogue(text)
        if dialogues:
            if i <= 5 and len(early_dialogue) < 3:
                early_dialogue.append(f"Ch {i}: \"{dialogues[0]}\"")
            if i >= 40 and len(late_dialogue) < 3:
                late_dialogue.append(f"Ch {i}: \"{dialogues[0]}\"")

with open('review_data.txt', 'w', encoding='utf-8') as out:
    out.write("=== Terminology Counts ===\n")
    for key, counts in term_counts.items():
        out.write(f"{key}: {counts}\n")

    out.write(f"\n=== Long Sentences without Pauses (Top 5 of {len(long_sentences)}) ===\n")
    for x in long_sentences[:5]:
        out.write(x + "\n")

    out.write(f"\n=== Punctuation Issues (Ellipses/Dashes) (Total: {len(punctuation_issues)}) ===\n")

    out.write("\n=== Early Dialogue (Valancy/Family Tone) ===\n")
    for d in early_dialogue:
        out.write(d + "\n")
        
    out.write("\n=== Late Dialogue (Valancy/Barney Tone) ===\n")
    for d in late_dialogue:
        out.write(d + "\n")
