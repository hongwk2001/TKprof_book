"""
translate_back_to_en.py
Translates modernized Korean chapters of Odyssey back to modernized English using raw English as a reference.
"""

import os
import sys
import json
import urllib.request
import urllib.error
import time
import re
import argparse

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\git_repo\TKprof_book\books"

def load_env():
    for path in [os.path.join(BASE_DIR, "..", ".env"), ".env", os.path.join(BASE_DIR, ".env")]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        parts = line.split("=", 1)
                        os.environ[parts[0].strip()] = parts[1].strip()
            break

load_env()

def call_gemini_api(api_key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    for attempt in range(7):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                
                candidates = res_json.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
                
                print(f"Error: Invalid API response structure: {res_body}")
                return None
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            if e.code == 429:
                if "quota" in err_body.lower() or "limit" in err_body.lower():
                    print(f"\n[QUOTA_EXHAUSTED] Daily API limit reached on attempt {attempt+1} (HTTP 429).")
                    return "QUOTA_EXHAUSTED"
                print("Rate limit reached. Waiting 10 seconds...")
                time.sleep(10)
            else:
                print(f"HTTP Error {e.code} on attempt {attempt+1}: {e.reason}")
                if e.code in [503, 500, 502, 504]:
                    delay = min(60, 2 ** attempt * 5)
                    time.sleep(delay)
                else:
                    time.sleep(2)
        except Exception as e:
            print(f"Network error on attempt {attempt+1}: {e}")
            time.sleep(2)
            
    return None

def split_into_paragraphs(text):
    paras = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paras if p.strip()]

def process_chapter(ch_num, api_key):
    book_path = os.path.join(BASE_DIR, "odyssey")
    chapters_dir = os.path.join(book_path, "chapters")
    
    raw_path = os.path.join(chapters_dir, f"raw_ch_{ch_num:02d}.txt")
    ko_path = os.path.join(chapters_dir, f"ch_{ch_num:02d}_ko.txt")
    en_dest_path = os.path.join(chapters_dir, f"ch_{ch_num:02d}_en.txt")
    
    prompt_file = os.path.join(book_path, "prompt.txt")
    if os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as pf:
            current_prompt_template = pf.read()
            if "{text}" not in current_prompt_template:
                current_prompt_template += "\n\nText to translate:\n{text}"
    else:
        print("Error: prompt.txt template not found!")
        return False
        
    if not os.path.exists(raw_path):
        print(f"Raw chapter file not found: {raw_path}")
        return False
    if not os.path.exists(ko_path):
        print(f"Korean chapter file not found: {ko_path}")
        return False
        
    print(f"\n--- Translating ch_{ch_num:02d}_ko.txt back to Modernized English ---")
    
    # Read both contents
    ko_content = read_file_content(ko_path)
    raw_content = read_file_content(raw_path)
    
    ko_paras = split_into_paragraphs(ko_content)
    raw_paras = split_into_paragraphs(raw_content)
    
    # Align the chapter header if needed
    # Usually both files start with paragraph 0 as Title/Header, paragraph 1 as Synopsis, and the rest as body
    print(f"Total paragraphs: Korean={len(ko_paras)}, Raw English={len(raw_paras)}")
    
    batch_size = 20
    
    # Check progress
    start_batch = 0
    if os.path.exists(en_dest_path):
        with open(en_dest_path, "r", encoding="utf-8") as f_existing:
            existing_content = f_existing.read()
        existing_paras = split_into_paragraphs(existing_content)
        if len(existing_paras) >= len(ko_paras) - 5:
            print(f"Chapter {ch_num:02d} already fully completed. Skipping.")
            return True
        else:
            start_batch = len(existing_paras) // batch_size
            truncated_paras = existing_paras[:start_batch * batch_size]
            with open(en_dest_path, "w", encoding="utf-8") as f_trunc:
                f_trunc.write("\n\n".join(truncated_paras))
            print(f"Chapter {ch_num:02d} is partially completed. Truncated to {len(truncated_paras)} paragraphs. Resuming from batch {start_batch}.")
        
    total_batches = (len(ko_paras) + batch_size - 1) // batch_size
    
    for i in range(start_batch * batch_size, len(ko_paras), batch_size):
        batch_idx = i // batch_size + 1
        
        ko_batch = ko_paras[i:i+batch_size]
        # Make sure we don't index out of bounds for raw English paragraphs
        raw_batch = raw_paras[i:i+batch_size] if i < len(raw_paras) else []
        
        # Build structured input
        batch_text = "=== SOURCE KOREAN TEXT ===\n" + "\n\n".join(ko_batch)
        if raw_batch:
            batch_text += "\n\n=== ORIGINAL ENGLISH REFERENCE ===\n" + "\n\n".join(raw_batch)
            
        print(f"  Processing batch {batch_idx}/{total_batches} ({len(ko_batch)} paras)...")
        prompt = current_prompt_template.format(text=batch_text)
        
        translated_text = call_gemini_api(api_key, prompt)
        if translated_text == "QUOTA_EXHAUSTED":
            print(f"\n[STUCK] Stopped at batch {batch_idx} due to API quota exhaustion.")
            return "QUOTA_EXHAUSTED"
        elif translated_text:
            with open(en_dest_path, "a", encoding="utf-8") as f_out:
                if os.path.getsize(en_dest_path) > 0 if os.path.exists(en_dest_path) else False:
                    f_out.write("\n\n")
                f_out.write(translated_text)
            time.sleep(1)
        else:
            print(f"  [ERROR] Failed to translate batch {batch_idx}")
            return False
            
    print(f"Chapter translation complete! Saved to {en_dest_path}")
    return True

def read_file_content(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description="Back-translate Korean chapters to Modernized English using Gemini.")
    parser.add_argument("--chapters", required=True, help="Comma-separated chapter numbers (e.g. 1 or 1,2,3 or all)")
    parser.add_argument("--api-key", help="Gemini API Key")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Gemini API key must be provided.")
        sys.exit(1)
        
    if args.chapters.lower() == "all":
        ch_list = list(range(1, 25))
    else:
        ch_list = [int(x.strip()) for x in args.chapters.split(",")]
        
    print(f"Back-translating chapters: {ch_list}")
    
    for ch in ch_list:
        status = process_chapter(ch, api_key)
        if status == "QUOTA_EXHAUSTED":
            sys.exit(2)
        elif not status:
            sys.exit(1)
            
    print("\nAll requested chapters completed successfully!")
    sys.exit(0)

if __name__ == "__main__":
    main()
