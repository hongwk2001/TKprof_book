import os
import re

chapters = [
    "About the author",
    "Foreword",
    "An Historical Sketch of Babylon",
    "The Man Who Desired Gold",
    "The Richest Man in Babylon",
    "Seven Cures For a Lean Purse",
    "Meet the Goddess of Good Luck",
    "The Five Laws of Gold",
    "The Gold Lender of Babylon",
    "The Walls of Babylon",
    "The Camel Trader of Babylon",
    "The Clay Tablets From Babylon",
    "The Luckiest Man in Babylon"
]

def segment_and_stats():
    with open('raw_source.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    # Create chapters directory
    os.makedirs('chapters', exist_ok=True)
    
    # Calculate overall stats
    words = text.split()
    word_count = len(words)
    page_count = word_count // 250
    reading_time_mins = word_count // 200
    
    # Very crude splitting by chapter title
    # First, find where "About the author" starts after the TOC
    # We can split by searching for chapter titles on their own line.
    
    # We will build a regex pattern that matches any of the chapter titles as a full line
    # Note: Some chapter titles might have weird spacing or newlines in the original text, but we'll try to match them strictly or loosely.
    
    current_ch = -1 # -1 for frontmatter
    buffer = []
    
    lines = text.split('\n')
    # skip TOC
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == "About the author" and i > 140: # Skip TOC mention
            start_idx = i
            break
            
    if start_idx == 0:
        start_idx = 144 # manual fallback from previous peek
        
    ch_text = "\n".join(lines[:start_idx])
    with open(f'chapters/raw_ch_00_frontmatter.txt', 'w', encoding='utf-8') as f:
        f.write(ch_text.strip())
        
    current_text = []
    chapter_idx = 0
    
    for line in lines[start_idx:]:
        stripped = line.strip()
        
        # Check if line matches next chapter
        is_new_chapter = False
        if chapter_idx < len(chapters) and stripped.lower() == chapters[chapter_idx].lower():
            is_new_chapter = True
        
        if is_new_chapter:
            # save current
            if current_text:
                fname = f'chapters/raw_ch_{chapter_idx:02d}_{chapters[chapter_idx-1].replace(" ", "_").lower()}.txt'
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(current_text).strip())
            current_text = [line]
            chapter_idx += 1
        else:
            current_text.append(line)
            
    if current_text:
        fname = f'chapters/raw_ch_{chapter_idx:02d}_{chapters[-1].replace(" ", "_").lower()}.txt'
        with open(fname, 'w', encoding='utf-8') as f:
            f.write('\n'.join(current_text).strip())

    print(f"Word Count: {word_count}")
    print(f"Page Count: {page_count} pages (assuming 250 words/page)")
    print(f"Expected Reading Time: {reading_time_mins} minutes (assuming 200 wpm)")
    print(f"Chapters Segmented: {chapter_idx}")

if __name__ == '__main__':
    segment_and_stats()
