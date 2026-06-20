import os
import re
import sys
import glob

# Force UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

def split_into_equal_parts(text, num_parts):
    """Splits text into num_parts roughly equal segments, trying to break at paragraph ends."""
    paragraphs = text.split("\n\n")
    total_chars = len(text)
    target_part_chars = total_chars / num_parts
    
    parts = []
    current_part = []
    current_chars = 0
    
    for para in paragraphs:
        current_part.append(para)
        current_chars += len(para) + 2 # +2 for the newlines
        
        # If we have reached the target size and we aren't on the last part yet
        if current_chars >= target_part_chars and len(parts) < num_parts - 1:
            parts.append("\n\n".join(current_part).strip())
            current_part = []
            current_chars = 0
            
    if current_part:
        parts.append("\n\n".join(current_part).strip())
        
    # Ensure we got exactly the requested number of parts (pad with empty if needed)
    while len(parts) < num_parts:
        parts.append("")
        
    return parts

def split_christmas_carol(text):
    """Splits A Christmas Carol into 5 chapters by Staves."""
    # Find positions of STAVE I to V
    stave_patterns = [
        r"STAVE\s+I\b",
        r"STAVE\s+II\b",
        r"STAVE\s+III\b",
        r"STAVE\s+IV\b",
        r"STAVE\s+V\b"
    ]
    
    positions = []
    for pattern in stave_patterns:
        matches = list(re.finditer(pattern, text, re.I))
        if matches:
            # Take the last match since table of contents might match earlier
            positions.append(matches[-1].start())
            
    positions.append(len(text))
    
    parts = []
    for i in range(len(positions) - 1):
        start = positions[i]
        end = positions[i+1]
        parts.append(text[start:end].strip())
        
    return parts

def split_frankenstein(text):
    """Splits Frankenstein into 7 chapters (Prologue + 6 parts)."""
    # Frankenstein is 100% complete already, but we write this logic just in case
    # Letter I to IV is Chapter 00
    # Then Chapter I to XXIV are split into 6 chapters (4 chapters each)
    letter_match = re.search(r"LETTER\s+I\b", text, re.I)
    start_letters = letter_match.start() if letter_match else 0
    
    chapter_matches = list(re.finditer(r"\bChapter\s+([I|V|X|L]+)\b", text, re.I))
    # Filter out TOC matches by checking if they are in the beginning
    actual_chapters = []
    for m in chapter_matches:
        if m.start() > start_letters + 5000:
            actual_chapters.append(m)
            
    # We want Chapter 1, 5, 9, 13, 17, 21 as boundary markers
    # There are 24 chapters total
    # Group 1: Ch 1-4
    # Group 2: Ch 5-8
    # Group 3: Ch 9-12
    # Group 4: Ch 13-16
    # Group 5: Ch 17-20
    # Group 6: Ch 21-24
    
    boundaries = [start_letters]
    target_indices = [1, 5, 9, 13, 17, 21]
    
    # Map roman numerals to their numeric values
    roman_map = {
        "I": 1, "V": 5, "IX": 9, "XIII": 13, "XVII": 17, "XXI": 21
    }
    
    for target in target_indices:
        found = False
        for m in actual_chapters:
            chap_num_str = m.group(1).upper()
            if roman_map.get(chap_num_str) == target:
                boundaries.append(m.start())
                found = True
                break
        if not found:
            # If a specific chapter header was not found, estimate position
            pass
            
    boundaries.append(len(text))
    boundaries = sorted(list(set(boundaries)))
    
    parts = []
    for i in range(len(boundaries) - 1):
        parts.append(text[boundaries[i]:boundaries[i+1]].strip())
        
    # We expect 7 parts (Letters + 6 chapter groups)
    while len(parts) < 7:
        parts.append("")
    return parts[:7]

def split_gilgamesh(text):
    """Splits Gilgamesh into 6 chapters."""
    # Gilgamesh text has Tablets. Let's find Tablet I, II, III, IV, V, VI or split equally.
    # Since Gilgamesh text has a complex structure, split into 6 equal parts.
    return split_into_equal_parts(text, 6)

def split_odyssey(text):
    """Splits Odyssey into 6 chapters (Books 1-4, 5-8, 9-12, 13-16, 17-20, 21-24)."""
    book_headers = [f"BOOK {roman}" for roman in [
        "I", "V", "IX", "XIII", "XVII", "XXI"
    ]]
    
    positions = []
    for header in book_headers:
        matches = list(re.finditer(rf"\b{header}\b", text))
        if matches:
            # Take the last match (ignoring TOC)
            positions.append(matches[-1].start())
            
    positions.append(len(text))
    positions = sorted(list(set(positions)))
    
    parts = []
    for i in range(len(positions) - 1):
        parts.append(text[positions[i]:positions[i+1]].strip())
        
    while len(parts) < 6:
        parts.append("")
    return parts[:6]

def split_two_cities(text):
    """Splits A Tale of Two Cities into its 45 actual chapters."""
    matches = list(re.finditer(r"^\s*CHAPTER\s+[IVXLCDM]+\.\s*$", text, re.MULTILINE))
    if not matches:
        return split_into_equal_parts(text, 45)
    
    parts = []
    for i in range(len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        parts.append(text[start:end].strip())
    return parts

def split_great_expectations(text):
    """Splits Great Expectations into 6 chapters."""
    # The book has 59 chapters total. Let's split into 6 equal parts.
    return split_into_equal_parts(text, 6)

def process_book(book_name, num_chapters):
    book_path = os.path.join(BASE_DIR, book_name)
    raw_source_path = os.path.join(book_path, "raw_source.txt")
    
    if not os.path.exists(raw_source_path):
        print(f"Error: {raw_source_path} does not exist.")
        return
        
    print(f"Processing '{book_name}'...")
    with open(raw_source_path, "r", encoding="utf-8", newline="") as f:
        raw_text = f.read()
        
    # Normalize line endings to avoid double-spacing and bad paragraph splitting
    raw_text = raw_text.replace("\r\r\n", "\n").replace("\r\n", "\n").replace("\r", "\n")
        
    # Clean Gutenberg headers
    clean_text = clean_gutenberg_headers(raw_text)
    
    # Perform custom split depending on the book
    if book_name == "christmas_carol":
        chapters = split_christmas_carol(clean_text)
    elif book_name == "frankenstein":
        chapters = split_frankenstein(clean_text)
    elif book_name == "two_cities":
        chapters = split_two_cities(clean_text)
    else:
        # Default split for other books
        chapters = split_into_equal_parts(clean_text, num_chapters)
        
    # Create chapters directory
    raw_chapters_dir = os.path.join(book_path, "chapters")
    os.makedirs(raw_chapters_dir, exist_ok=True)
    
    # Save split chapters
    for idx, chapter_text in enumerate(chapters):
        if book_name == "two_cities":
            # Book 1: 6 chapters, Book 2: 24 chapters, Book 3: 15 chapters
            if idx < 6:
                book_num = 1
                ch_num = idx + 1
                if idx == 0:
                    chapter_text = "Book the First--Recalled to Life\n\n" + chapter_text
            elif idx < 30:
                book_num = 2
                ch_num = idx - 6 + 1
                if idx == 6:
                    chapter_text = "Book the Second--the Golden Thread\n\n" + chapter_text
            else:
                book_num = 3
                ch_num = idx - 30 + 1
                if idx == 30:
                    chapter_text = "Book the Third--the Track of a Storm\n\n" + chapter_text
            chapter_filename = f"raw_book{book_num}_ch_{ch_num:02d}.txt"
        else:
            # We start chapter index at 00 for Frankenstein prologue, and 01 for others
            start_idx = 0 if book_name == "frankenstein" else 1
            ch_num = idx + start_idx
            chapter_filename = f"raw_ch_{ch_num:02d}.txt"
            
        chapter_path = os.path.join(raw_chapters_dir, chapter_filename)
        with open(chapter_path, "w", encoding="utf-8") as out:
            out.write(chapter_text)
        print(f"  Saved {chapter_filename} to chapters/ ({len(chapter_text)} characters)")

def main():
    books_to_process = [
        ("christmas_carol", 5),
        ("frankenstein", 7),
        ("gilgamesh", 6),
        ("hong_gildong", 6),
        ("nine_cloud_dream", 5),
        ("odyssey", 6),
        ("two_cities", 45),
        ("great_expectations", 6),
        ("journey_to_the_west", 5),
        ("three_kingdoms", 5)
    ]
    
    for book, num in books_to_process:
        process_book(book, num)

if __name__ == "__main__":
    main()
