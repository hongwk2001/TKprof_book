import os
import re

filepath = r"C:\Users\hongw\.gemini\antigravity\brain\9a5fe6dc-1f15-4d6a-8c11-a75866ccab95\.system_generated\steps\80\content.md"
dest_base = r"d:\git_repo\TKprof_book\books\seneca_emotional_resilience\chapters"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line boundaries (1-indexed, so we subtract 1 when slicing)
treatises = [
    {
        "name": "providence",
        "start": 103,
        "end": 744,
        "dir": "4.providence",
        "file_prefix": "raw_providence_ch"
    },
    {
        "name": "constancy",
        "start": 745,
        "end": 1529,
        "dir": "3.constancy",
        "file_prefix": "raw_constancy_ch"
    },
    {
        "name": "on_anger_book1",
        "start": 1530,
        "end": 2429,
        "dir": "1.on_anger",
        "file_prefix": "raw_on_anger_book1_ch"
    },
    {
        "name": "on_anger_book2",
        "start": 2430,
        "end": 3659,
        "dir": "1.on_anger",
        "file_prefix": "raw_on_anger_book2_ch"
    },
    {
        "name": "on_anger_book3",
        "start": 3660,
        "end": 5135,
        "dir": "1.on_anger",
        "file_prefix": "raw_on_anger_book3_ch"
    },
    {
        "name": "tranquillity_of_mind",
        "start": 7898,
        "end": 9076,
        "dir": "2.tranquillity_of_mind",
        "file_prefix": "raw_tranquillity_ch"
    }
]

def split_treatise(t):
    text = "".join(lines[t["start"]-1 : t["end"]])
    
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    
    # Find all chapter markers
    # Matches patterns like \n  I. or \nI. or \n  XXVI.
    matches = list(re.finditer(r"\n\s*([I|V|X|L]+)\.\s", text))
    
    chapters = []
    
    # If there are no matches, just take the whole thing as chapter 1
    if not matches:
        chapters.append((1, text))
    else:
        # Check if the first match is NOT "I" (meaning chapter I starts at the beginning without header)
        if matches[0].group(1) != "I":
            first_chap_text = text[:matches[0].start()].strip()
            chapters.append((1, first_chap_text))
            
            # Now extract the rest
            for idx, m in enumerate(matches):
                roman = m.group(1)
                # Convert roman numeral to integer or just count
                # Let's count them sequentially for clean filenames
                ch_num = idx + 2
                start_pos = m.start()
                end_pos = matches[idx+1].start() if idx + 1 < len(matches) else len(text)
                chapters.append((ch_num, text[start_pos:end_pos].strip()))
        else:
            # The first match is indeed chapter I
            # If there's text BEFORE the first match (like title headers), check if it's significant, otherwise ignore or pre-pend
            for idx, m in enumerate(matches):
                ch_num = idx + 1
                start_pos = m.start()
                end_pos = matches[idx+1].start() if idx + 1 < len(matches) else len(text)
                chapters.append((ch_num, text[start_pos:end_pos].strip()))
                
    # Create target directory
    target_dir = os.path.join(dest_base, t["dir"])
    os.makedirs(target_dir, exist_ok=True)
    
    # Save files
    for ch_num, ch_text in chapters:
        filename = f"{t['file_prefix']}{ch_num:02d}.txt"
        file_path = os.path.join(target_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as out_f:
            out_f.write(ch_text)
        print(f"Saved {filename} to {t['dir']}/ ({len(ch_text)} chars)")

for t in treatises:
    print(f"\nSplitting {t['name']}...")
    split_treatise(t)

print("\nDone splitting all chapters!")
