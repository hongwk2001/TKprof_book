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

def clean_synopsis(synopsis_lines):
    # Flatten/clean synopsis lines
    clean_parts = []
    for line in synopsis_lines:
        line = line.strip()
        if not line:
            continue
        # Remove [줄거리] or similar markers
        line = re.sub(r'^\[줄거리\]', '', line).strip()
        # Strip brackets
        line = line.strip('[]').strip()
        if line:
            clean_parts.append(line)
            
    # Combine with ' — ' (em-dash style)
    combined = " — ".join(clean_parts)
    # Standardize spaces around dashes
    combined = re.sub(r'\s*—\s*', ' — ', combined)
    # Remove trailing periods to match synopsis style, but keep internal ones
    if combined.endswith('.'):
        combined = combined[:-1]
    return combined

def clean_file(file_path, ch_num):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize line endings
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    lines = content.split("\n")
    
    # Identify non-empty lines at the top of the file
    header_index = -1
    synopsis_lines = []
    first_para_index = -1
    
    # Scan to separate headers, synopses, and actual body paragraphs
    # The first line with text is the chapter header
    # Subsequent non-empty lines before the actual story starts are the synopsis.
    # The story usually starts with standard Korean narrative sentences.
    # Let's check how many lines we have and do a simple heuristic:
    # 1. The first text line matching '제' or containing '장' is the header.
    # 2. Any lines after the header that are bracketed or represent short summaries (not starting with a common indentation or narrative flow) are the synopsis.
    non_empty_indices = [i for i, line in enumerate(lines) if line.strip()]
    
    if not non_empty_indices:
        print(f"Skipping empty file: {file_path}")
        return
        
    header_idx = non_empty_indices[0]
    
    # Find synopsis lines
    body_idx = -1
    for idx in non_empty_indices[1:]:
        line = lines[idx].strip()
        # Heuristic: Synopsis lines are short, bracketed, or contain outline/bullet-like info.
        # Story body paragraphs are typically longer and start with standard narration like "장밋빛", "그동안", "뮤즈여", "아름다운", etc.
        # Outlines often contain '—', ':', or are bracketed '[]'.
        is_synopsis = (
            line.startswith('[') or 
            line.endswith(']') or 
            '—' in line or 
            ':' in line or 
            len(line) < 150
        )
        # Exception: if the line looks like the start of a story (e.g. over 150 chars, no brackets, looks like narrative prose)
        if len(line) > 200 and not line.startswith('[') and not ' — ' in line:
            is_synopsis = False
            
        if is_synopsis:
            synopsis_lines.append(line)
        else:
            body_idx = idx
            break
            
    if body_idx == -1:
        # Fallback if we couldn't distinguish body
        body_idx = non_empty_indices[-1]
        synopsis_lines = [lines[i] for i in non_empty_indices[1:-1]]
        
    # Format the header consistently: "제 X장"
    sino_num = NUM_MAP[ch_num]
    new_header = f"제 {sino_num}장"
    
    # Format the synopsis
    new_synopsis = clean_synopsis(synopsis_lines)
    
    # Reassemble the file
    body_text = "\n\n".join([lines[i].strip() for i in range(body_idx, len(lines)) if lines[i].strip()])
    
    new_content = f"{new_header}\n\n{new_synopsis}\n\n{body_text}\n"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print(f"Cleaned {os.path.basename(file_path)}")
    print(f"  Header: {new_header}")
    print(f"  Synopsis: {new_synopsis[:80]}...")

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
