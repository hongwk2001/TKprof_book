import os
import re
import sys

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

def clean_file(file_path, ch_num):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into clean paragraphs
    paras = [p.strip() for p in re.split(r'\n\s*\n', content) if p.strip()]
    
    # Check if header and synopsis are merged in paras[0]
    first_para = paras[0]
    new_header = f"Book {ch_num}"
    synopsis = ""
    body_paras = []
    
    # Match patterns like "Book X: Synopsis text" or "Book X — Synopsis text"
    match_merged = re.search(r'^(Book|제)\s*(\d+|[가-힣]+)\s*(장|)?\s*[:—\-]\s*(.*)$', first_para, re.IGNORECASE | re.DOTALL)
    
    if match_merged:
        synopsis = match_merged.group(4).strip()
        body_paras = paras[1:]
    else:
        if len(paras) < 3:
            print(f"Warning: File {os.path.basename(file_path)} has separate headers but too few paragraphs ({len(paras)})")
            return
        synopsis = paras[1]
        body_paras = paras[2:]
    
    # Clean brackets and outlines (e.g. [Synopsis], [줄거리], Synopsis:, etc.)
    synopsis = re.sub(r'^(Synopsis|Synopsis:|줄거리|\[줄거리\]|\[Synopsis\])\s*', '', synopsis, flags=re.IGNORECASE).strip()
    synopsis = synopsis.strip('[]').strip()
    
    # Standardize spaces around dashes
    synopsis = re.sub(r'\s*—\s*', ' — ', synopsis)
    synopsis = re.sub(r'\s*--\s*', ' — ', synopsis)
    
    # Remove trailing periods in synopsis if present to match repository style
    if synopsis.endswith('.'):
        synopsis = synopsis[:-1]
        
    body_text = "\n\n".join(body_paras)
    
    new_content = f"{new_header}\n\n{synopsis}\n\n{body_text}\n"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print(f"Cleaned {os.path.basename(file_path)}")
    print(f"  Header: {new_header}")
    print(f"  Synopsis: {synopsis[:80]}...")

def main():
    for num in range(1, 25):
        filename = f"ch_{num:02d}_en.txt"
        file_path = os.path.join(CHAPTERS_DIR, filename)
        if os.path.exists(file_path):
            clean_file(file_path, num)
        else:
            print(f"Warning: File {filename} not found.")

if __name__ == "__main__":
    main()
