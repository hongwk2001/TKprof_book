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

DEFAULT_PROMPT_TEMPLATE = """You are an expert translator. Translate the following text to Korean.
{text}"""

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

def process_chapter(book_id, raw_filename, api_key):
    book_path = os.path.join(BASE_DIR, book_id)
    dest_dir = os.path.join(book_path, "chapters")
    os.makedirs(dest_dir, exist_ok=True)
    raw_ch_path = os.path.join(dest_dir, raw_filename)
    
    dest_filename = raw_filename.replace("raw_", "").replace(".txt", "_ko.txt")
    dest_path = os.path.join(dest_dir, dest_filename)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Check for custom translation prompt
    prompt_file = os.path.join(book_path, "prompt_ko.txt")
    if os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as pf:
            current_prompt_template = pf.read()
            if "{text}" not in current_prompt_template:
                current_prompt_template += "\n\nText to translate:\n{text}"
    else:
        current_prompt_template = DEFAULT_PROMPT_TEMPLATE
    
    if not os.path.exists(raw_ch_path):
        print(f"Raw chapter file not found: {raw_ch_path}")
        return False
        
    print(f"\n--- Translating {raw_filename} to Korean ({book_id}) ---")
    with open(raw_ch_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    paragraphs = split_into_paragraphs(content)
    print(f"Total paragraphs in raw chapter: {len(paragraphs)}")
    
    batch_size = 10 # smaller batch for high quality translation
    modernized_paragraphs = []
    
    # Check if we have progress already saved
    start_batch = 0
    if os.path.exists(dest_path):
        with open(dest_path, "r", encoding="utf-8") as f_existing:
            existing_content = f_existing.read()
        existing_paragraphs = split_into_paragraphs(existing_content)
        start_batch = len(existing_paragraphs) // batch_size
        print(f"Found existing progress: {len(existing_paragraphs)} paragraphs completed (~{start_batch} batches).")
        modernized_paragraphs = [existing_content] if existing_content.strip() else []
        
    total_batches = (len(paragraphs) + batch_size - 1) // batch_size
    
    for i in range(start_batch * batch_size, len(paragraphs), batch_size):
        batch_idx = i // batch_size + 1
        batch = paragraphs[i:i+batch_size]
        batch_text = "\n\n".join(batch)
        
        print(f"  Processing translation batch {batch_idx}/{total_batches} ({len(batch)} paras)...")
        prompt = current_prompt_template.format(text=batch_text)
        
        translated_text = call_gemini_api(api_key, prompt)
        if translated_text == "QUOTA_EXHAUSTED":
            print(f"\n[STUCK] Script stopped at batch {batch_idx} because your API key's daily free quota was exhausted.")
            return "QUOTA_EXHAUSTED"
        elif translated_text:
            with open(dest_path, "a", encoding="utf-8") as f_out:
                if os.path.getsize(dest_path) > 0 if os.path.exists(dest_path) else False:
                    f_out.write("\n\n")
                f_out.write(translated_text)
            time.sleep(5)
        else:
            print(f"  [ERROR] Failed to translate batch {batch_idx}")
            return False
            
    print(f"Chapter translation complete! Saved to {dest_path}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate raw book chapters to Korean using Gemini API.")
    parser.add_argument("--book", required=True, help="Book ID folder (e.g. scaramouche)")
    parser.add_argument("--api-key", help="Gemini API Key")
    parser.add_argument("--chapters", help="Comma-separated chapter numbers (e.g. 1)")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Gemini API key must be provided via --api-key or GEMINI_API_KEY environment variable.")
        sys.exit(1)
        
    book_path = os.path.join(BASE_DIR, args.book)
    raw_chapters_dir = os.path.join(book_path, "chapters")
    
    if not os.path.exists(raw_chapters_dir):
        print(f"Error: chapters directory not found for {args.book}.")
        sys.exit(1)
        
    if args.chapters:
        requested = [x.strip() for x in args.chapters.split(",")]
        raw_files = []
        for root, dirs, files in os.walk(raw_chapters_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), raw_chapters_dir).replace("\\", "/")
                raw_files.append(rel_path)
        ch_list = []
        for req in requested:
            found = False
            for f in raw_files:
                basename = os.path.basename(f)
                if f == req or basename == req or basename == f"raw_{req}.txt" or (basename == f"raw_ch_{int(req):02d}.txt" if req.isdigit() else False):
                    ch_list.append(f)
                    found = True
                    break
            if not found:
                print(f"Warning: could not resolve chapter parameter '{req}' to a file.")
    else:
        raw_files = []
        for root, dirs, files in os.walk(raw_chapters_dir):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), raw_chapters_dir).replace("\\", "/")
                raw_files.append(rel_path)
        ch_list = []
        for f in sorted(raw_files):
            basename = os.path.basename(f)
            if basename.startswith("raw_") and basename.endswith(".txt"):
                ch_list.append(f)
                
    print(f"Translating chapters: {ch_list}")
    
    for ch in ch_list:
        status = process_chapter(args.book, ch, api_key)
        if status == "QUOTA_EXHAUSTED":
            sys.exit(2)
        elif not status:
            print("Process stopped due to failure.")
            sys.exit(1)
            
    print("\nAll requested chapters translated successfully!")
    sys.exit(0)
