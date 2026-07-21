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
    current_chapter_book = ""
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
                    "book": current_chapter_book,
                    "title": current_chapter_title,
                    "text": "\n".join(current_chapter_text).strip()
                })
                current_chapter_text = []
            
            # Start new chapter
            current_chapter_book = current_book
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
            "book": current_chapter_book,
            "title": current_chapter_title,
            "text": "\n".join(current_chapter_text).strip()
        })
        
    print(f"Total chapters identified: {len(chapters)}")
    
    # Create chapters directory
    os.makedirs(CHAPTERS_DIR, exist_ok=True)
    
    # Helper to map 1-based sequential chapter index to book number and book chapter index
    def map_sequential_to_book_ch(idx):
        if idx <= 9:
            return 1, idx
        elif idx <= 20:
            return 2, idx - 9
        else:
            return 3, idx - 20

    # Migrate any existing flat files in chapters to their respective book directories
    import shutil
    print("Checking for existing files to migrate...")
    for filename in os.listdir(CHAPTERS_DIR):
        file_path = os.path.join(CHAPTERS_DIR, filename)
        if not os.path.isfile(file_path):
            continue
        
        # Match files starting with raw_ch_XX or ch_XX
        match = re.match(r"^(raw_ch_|ch_)?(\d+)(.*)$", filename)
        if match:
            seq_idx = int(match.group(2))
            prefix = match.group(1) or ""
            suffix = match.group(3)
            
            # Map to book and chapter
            book_num, ch_num = map_sequential_to_book_ch(seq_idx)
            
            # Target dir
            book_dir = os.path.join(CHAPTERS_DIR, f"book_{book_num}")
            os.makedirs(book_dir, exist_ok=True)
            
            # Generate new filename
            new_prefix = "raw_ch_" if "raw_" in prefix else "ch_"
            new_filename = f"{new_prefix}{ch_num:02d}{suffix}"
            dest_path = os.path.join(book_dir, new_filename)
            
            print(f"  Migrating {filename} -> book_{book_num}/{new_filename}")
            shutil.move(file_path, dest_path)
            
    # Write raw chapters to book directories and build metadata
    import json
    metadata_path = os.path.join(CHAPTERS_DIR, "metadata.json")
    existing_metadata = {}
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                existing_metadata = json.load(f)
        except Exception:
            pass

    metadata = {}
    book_counters = {1: 0, 2: 0, 3: 0}
    book_map = {"I": 1, "II": 2, "III": 3}
    
    for idx, chap in enumerate(chapters, 1):
        book_num = book_map.get(chap['book'], 1)
        book_counters[book_num] += 1
        ch_num = book_counters[book_num]
        
        book_dir = os.path.join(CHAPTERS_DIR, f"book_{book_num}")
        os.makedirs(book_dir, exist_ok=True)
        
        filename = f"raw_ch_{ch_num:02d}.txt"
        filepath = os.path.join(book_dir, filename)
        
        # Write only the original text (no bracketed header)
        full_text = chap['text']
        
        with open(filepath, "w", encoding="utf-8") as out:
            out.write(full_text)
            
        print(f"  Saved book_{book_num}/{filename} ({len(full_text)} characters) -> {chap['title']}")
        
        # Populate metadata
        book_key = f"book_{book_num}"
        if book_key not in metadata:
            metadata[book_key] = {}
            
        ch_key = f"ch_{ch_num:02d}"
        
        title_text = chap['title']
        if " - " in title_text:
            title_text = title_text.split(" - ", 1)[1]
        if ":" in title_text:
            title_text = title_text.split(":", 1)[1].strip()
            
        # Preserve existing Korean title if available
        existing_ch = existing_metadata.get(book_key, {}).get(ch_key, {})
        title_ko = existing_ch.get("title_ko", "")
        
        metadata[book_key][ch_key] = {
            "title_en": title_text,
            "title_ko": title_ko
        }
        
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Metadata saved to: {metadata_path}")

if __name__ == "__main__":
    main()
