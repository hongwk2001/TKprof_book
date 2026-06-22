import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
os.makedirs(CHAPTERS_DIR, exist_ok=True)

def clean_gutenberg_headers(text):
    """Strip Gutenberg headers/footers to keep only the main content."""
    start_markers = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK.*?\*\*\*"
    ]
    end_markers = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK.*?\*\*\*"
    ]
    
    start_pos = 0
    for marker in start_markers:
        match = re.search(marker, text, re.I)
        if match:
            start_pos = match.end()
            break
            
    end_pos = len(text)
    for marker in end_markers:
        match = re.search(marker, text, re.I)
        if match:
            end_pos = match.start()
            break
            
    return text[start_pos:end_pos].strip()

def split_chapters():
    raw_path = os.path.join(BASE_DIR, "raw_source.txt")
    with open(raw_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Normalize line endings
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    
    # Strip Gutenberg headers
    clean_content = clean_gutenberg_headers(content)
    
    # We split the chapters by Roman numerals.
    # The Roman numeral headers are lines like "I.", "II.", "XXIV."
    # The split pattern will match the Roman numeral lines.
    pattern = r"\n\s*([IVXLCDM]+)\.\s*\n"
    parts = re.split(pattern, clean_content)
    
    # The first part (parts[0]) contains Preface, Table of Contents, and THE CUSTOM-HOUSE.
    # Subsequent parts will be pairs of (roman_numeral, chapter_content).
    
    chapters = {}
    # Save the custom house / preamble as chapter 0
    # Let's clean it up slightly to remove the table of contents if needed, or leave it.
    # Typically, we just keep it as the introductory chapter.
    chapters[0] = parts[0].strip()
    
    # Iterate through Roman numerals and their contents
    for i in range(1, len(parts), 2):
        roman_num = parts[i]
        ch_text = parts[i+1].strip() if i+1 < len(parts) else ""
        
        # Parse chapter index from the Roman numeral
        roman_vals = {
            'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
            'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15, 'XVI': 16, 'XVII': 17, 'XVIII': 18,
            'XIX': 19, 'XX': 20, 'XXI': 21, 'XXII': 22, 'XXIII': 23, 'XXIV': 24
        }
        ch_num = roman_vals.get(roman_num.upper())
        if ch_num:
            # Reconstruct chapter content with its header
            chapters[ch_num] = f"{roman_num}.\n\n{ch_text}"
            
    # Write each chapter to its respective file
    for ch_num, ch_content in chapters.items():
        dest_path = os.path.join(CHAPTERS_DIR, f"raw_ch_{ch_num:02d}.txt")
        with open(dest_path, "w", encoding="utf-8") as out:
            out.write(ch_content)
        print(f"Saved {dest_path} ({len(ch_content)} characters)")

if __name__ == "__main__":
    split_chapters()
