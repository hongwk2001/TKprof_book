import re
import os
import glob
import json

def split_sentences(text):
    # Regex to split on ., !, ? (followed by space and uppercase/quote) OR split on ; and :
    # Ignore common abbreviations.
    pattern = r'(?<!\bMr)(?<!\bMrs)(?<!\bMs)(?<!\bDr)(?<!\bSt)(?<!\bProf)(?<!\bRev)(?<=[.!?])\s+(?=[A-Z"\'\[])|(?<=[;:])\s+'
    
    # We use re.split. This will return a list.
    chunks = re.split(pattern, text)
    # Filter out empty strings
    return [c.strip() for c in chunks if c.strip()]

def generate_base_jsons():
    raw_files = glob.glob('c:/git_repo/TKprof_book/books/two_cities/chapters/raw_book*_ch_*.txt')
    out_dir = 'c:/git_repo/TKprof_book/books/two_cities/json'
    
    os.makedirs(out_dir, exist_ok=True)
    
    for raw_path in raw_files:
        basename = os.path.basename(raw_path).replace('raw_', '').replace('.txt', '.json')
        out_path = os.path.join(out_dir, basename)
        
        with open(raw_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            
        # Rebuild paragraphs (split by double newline)
        raw_paras = [p.strip() for p in raw_text.split('\n\n') if p.strip()]
        
        json_data = []
        block_id = 1
        
        for p_idx, para in enumerate(raw_paras):
            # Strip single newlines to reflow text
            para = re.sub(r'(?<!\n)\n(?!\n)', ' ', para)
            
            # Simple heuristic for headers (no ending punctuation, or all caps, or very short)
            is_header = False
            if p_idx < 3 and (para.isupper() or not re.search(r'[.!?]$', para)):
                is_header = True
                
            if is_header:
                json_data.append({
                    "id": block_id,
                    "tag": f"H{p_idx+1:03d}",
                    "raw": para,
                    "en": "",
                    "ko": "",
                    "is_header": True
                })
                block_id += 1
            else:
                sentences = split_sentences(para)
                for s_idx, sentence in enumerate(sentences):
                    json_data.append({
                        "id": block_id,
                        "tag": f"P{p_idx+1:03d}_{s_idx+1}",
                        "raw": sentence,
                        "en": "",
                        "ko": "",
                        "is_header": False
                    })
                    block_id += 1
                    
        with open(out_path, 'w', encoding='utf-8') as out_f:
            json.dump(json_data, out_f, indent=2, ensure_ascii=False)
            
    print(f"Successfully generated base JSON files for {len(raw_files)} chapters.")

if __name__ == "__main__":
    generate_base_jsons()
