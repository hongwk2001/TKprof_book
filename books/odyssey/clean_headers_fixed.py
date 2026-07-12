import os
import re
import sys

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

NUM_MAP = {
    1: '일', 2: '이', 3: '삼', 4: '사', 5: '오', 6: '육', 7: '칠', 8: '팔', 9: '구', 10: '십',
    11: '십일', 12: '십이', 13: '십삼', 14: '십사', 15: '십오', 16: '십육', 17: '십칠', 18: '십팔', 19: '십구', 20: '이십',
    21: '이십일', 22: '이십이', 23: '이십삼', 24: '이십사'
}

def clean_file(file_path, ch_num):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into clean paragraphs
    paras = [p.strip() for p in re.split(r'\n\s*\n', content) if p.strip()]
    
    if len(paras) < 3:
        print(f"Warning: File {os.path.basename(file_path)} has too few paragraphs ({len(paras)})")
        return

    # Standardize header: "제 X장"
    sino_num = NUM_MAP[ch_num]
    new_header = f"제 {sino_num}장"
    
    # Standardize synopsis (always paragraph 1, index 1)
    synopsis = paras[1]
    
    # Clean brackets and outlines
    synopsis = re.sub(r'^\[줄거리\]', '', synopsis).strip()
    synopsis = synopsis.strip('[]').strip()
    
    # Standardize spaces around dashes
    synopsis = re.sub(r'\s*—\s*', ' — ', synopsis)
    
    # Remove trailing periods
    if synopsis.endswith('.'):
        synopsis = synopsis[:-1]
        
    # The rest of the paragraphs are the body
    body_paras = paras[2:]
    body_text = "\n\n".join(body_paras)
    
    new_content = f"{new_header}\n\n{synopsis}\n\n{body_text}\n"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print(f"Cleaned {os.path.basename(file_path)}")
    print(f"  Header: {new_header}")
    print(f"  Synopsis: {synopsis[:80]}...")

def main():
    for num in range(1, 25):
        filename = f"ch_{num:02d}_ko.txt"
        file_path = os.path.join(CHAPTERS_DIR, filename)
        if os.path.exists(file_path):
            clean_file(file_path, num)
        else:
            print(f"Warning: File {filename} not found.")

if __name__ == "__main__":
    main()
