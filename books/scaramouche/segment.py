import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_SOURCE_PATH = os.path.join(BASE_DIR, "raw_source.txt")
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

def clean_gutenberg_headers(text):
    """Strip Gutenberg headers/footers to keep only the main content."""
    start_marker = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK SCARAMOUCHE: A ROMANCE OF THE FRENCH REVOLUTION \*\*\*"
    end_marker = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK SCARAMOUCHE: A ROMANCE OF THE FRENCH REVOLUTION \*\*\*"
    
    start_match = re.search(start_marker, text, re.I)
    start_pos = start_match.end() if start_match else 0
    
    end_match = re.search(end_marker, text, re.I)
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
    
    # Strip Gutenberg wrappers
    main_text = clean_gutenberg_headers(content)
    
    # Parse lines
    lines = main_text.split("\n")
    
    chapters = []
    current_chapter_text = []
    current_chapter_title = ""
    current_book = ""
    current_book_header = ""
    
    book_pattern = re.compile(r"^BOOK (I|II|III): (.*)$", re.IGNORECASE)
    chapter_pattern = re.compile(r"^CHAPTER ([IVXLCDM]+)\. (.*)$", re.IGNORECASE)
    
    in_story = False
    
    for line in lines:
        stripped = line.strip()
        
        # Check for Book header (not indented)
        book_match = book_pattern.match(stripped)
        if book_match and not line.startswith(" ") and not line.startswith("\t"):
            in_story = True
            current_book = book_match.group(1).upper()
            current_book_header = stripped
            continue  # Don't add the BOOK header line as standard text yet
            
        # Check for Chapter header (not indented)
        chap_match = chapter_pattern.match(stripped)
        if chap_match and not line.startswith(" ") and not line.startswith("\t"):
            in_story = True
            # Save the previous chapter if we have one
            if current_chapter_title:
                chapters.append({
                    "book": current_book,
                    "title": current_chapter_title,
                    "text": "\n".join(current_chapter_text).strip()
                })
                current_chapter_text = []
            
            # Start new chapter
            current_chapter_title = f"Book {current_book} - Chapter {chap_match.group(1)}: {chap_match.group(2)}"
            print(f"Segmenting: {current_chapter_title}")
            
            # If we had a book header that wasn't written, prepend it
            if current_book_header:
                current_chapter_text.append(current_book_header)
                current_book_header = "" # consume it
                
        if in_story:
            current_chapter_text.append(line)
            
    # Add final chapter
    if current_chapter_text:
        chapters.append({
            "book": current_book,
            "title": current_chapter_title,
            "text": "\n".join(current_chapter_text).strip()
        })
        
    print(f"Total chapters identified: {len(chapters)}")
    
    # Create chapters directory
    os.makedirs(CHAPTERS_DIR, exist_ok=True)
    
    # Clear out any existing files in chapters to avoid leftover files
    for filename in os.listdir(CHAPTERS_DIR):
        file_path = os.path.join(CHAPTERS_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
    # Write chapters to files
    for idx, chap in enumerate(chapters, 1):
        filename = f"raw_ch_{idx:02d}.txt"
        filepath = os.path.join(CHAPTERS_DIR, filename)
        
        # Prepend the formal title header
        full_text = f"[{chap['title']}]\n\n{chap['text']}"
        
        with open(filepath, "w", encoding="utf-8") as out:
            out.write(full_text)
            
        print(f"  Saved {filename} ({len(full_text)} characters) -> {chap['title']}")

if __name__ == "__main__":
    main()
