import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_SOURCE_PATH = os.path.join(BASE_DIR, "raw_source.txt")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

def clean_gutenberg_headers(text):
    """Strip Gutenberg headers/footers and footnotes to keep only the main content."""
    start_marker = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK THE ODYSSEY \*\*\*"
    end_marker = r"^FOOTNOTES:$"
    
    start_match = re.search(start_marker, text, re.I)
    start_pos = start_match.end() if start_match else 0
    
    end_match = re.search(end_marker, text, re.I | re.M)
    end_pos = end_match.start() if end_match else len(text)
    
    return text[start_pos:end_pos].strip()

def main():
    if not os.path.exists(RAW_SOURCE_PATH):
        print(f"Error: {RAW_SOURCE_PATH} not found.")
        return

    print("Reading raw source text...")
    with open(RAW_SOURCE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize line endings
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    
    # Strip Gutenberg wrappers and footnotes
    main_text = clean_gutenberg_headers(content)
    
    # Parse lines
    lines = main_text.split("\n")
    
    chapters = []
    current_chapter_lines = []
    current_book_num = 0
    
    book_pattern = re.compile(r"^BOOK ([IVXLCDM]+)$", re.IGNORECASE)
    
    in_story = False
    
    for line in lines:
        stripped = line.strip()
        
        # Check for Book header
        book_match = book_pattern.match(stripped)
        if book_match:
            in_story = True
            # Save the previous chapter if we have one
            if current_chapter_lines and current_book_num > 0:
                chapters.append({
                    "book_num": current_book_num,
                    "text": "\n".join(current_chapter_lines).strip()
                })
                current_chapter_lines = []
            
            # Start new chapter
            current_book_num += 1
            print(f"Identified Book {current_book_num} ({stripped})")
            
        if in_story:
            current_chapter_lines.append(line)
            
    # Add final chapter
    if current_chapter_lines and current_book_num > 0:
        chapters.append({
            "book_num": current_book_num,
            "text": "\n".join(current_chapter_lines).strip()
        })
        
    print(f"Total chapters identified: {len(chapters)}")
    
    # Create chapters directory
    os.makedirs(CHAPTERS_DIR, exist_ok=True)
    
    # Clear out any existing files in chapters to avoid leftover files
    for filename in os.listdir(CHAPTERS_DIR):
        file_path = os.path.join(CHAPTERS_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
    # Write new chapters
    for chap in chapters:
        filename = f"raw_ch_{chap['book_num']:02d}.txt"
        file_path = os.path.join(CHAPTERS_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chap["text"])
        print(f"Wrote: {filename}")

if __name__ == "__main__":
    main()
