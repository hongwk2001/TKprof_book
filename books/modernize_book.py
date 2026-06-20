import os
import sys
import json
import urllib.request
import urllib.error
import argparse
import time
import re

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\git_repo\TKprof_book\books"

def load_env():
    # Look for .env in current dir or workspace root (parent of books dir)
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

PROMPT_TEMPLATE = """You are an expert editor adapting Victorian literature for modern casual readers and English as a Second Language (ESL) learners.
Translate/rewrite the following paragraphs into clear, engaging, modern casual English.

Guidelines:
1. Retain the exact meaning, detail, tone, and character voices. Do NOT summarize, shorten, or omit anything.
2. Replace archaic grammar and obsolete vocabulary with standard modern casual phrasing.
3. Output ONLY the modernized version of the paragraphs. Maintain the exact paragraph separations. No explanations, no introductory notes.

Text to modernize:
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
    
    # Retry up to 3 times on temporary network errors
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                
                # Extract response text
                candidates = res_json.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
                
                print(f"Error: Invalid API response structure: {res_body}")
                return None
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            # If rate limit or quota exceeded
            if e.code == 429:
                if "quota" in err_body.lower() or "limit" in err_body.lower():
                    print(f"\n[QUOTA_EXHAUSTED] Daily API limit reached on attempt {attempt+1} (HTTP 429).")
                    print(f"Details: {err_body}")
                    return "QUOTA_EXHAUSTED"
                print("Rate limit reached. Waiting 10 seconds...")
                time.sleep(10)
            else:
                print(f"HTTP Error {e.code} on attempt {attempt+1}: {e.reason}")
                print(f"Details: {err_body}")
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
    
    if raw_filename.startswith("raw_book"):
        dest_filename = raw_filename.replace("raw_book", "book").replace(".txt", "_en.txt")
    else:
        dest_filename = raw_filename.replace("raw_", "").replace(".txt", "_en.txt")
    dest_path = os.path.join(dest_dir, dest_filename)
    
    if not os.path.exists(raw_ch_path):
        print(f"Raw chapter file not found: {raw_ch_path}")
        return False
        
    print(f"\n--- Modernizing {raw_filename} ({book_id}) ---")
    with open(raw_ch_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    paragraphs = split_into_paragraphs(content)
    print(f"Total paragraphs in raw chapter: {len(paragraphs)}")
    
    batch_size = 30
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
        
        print(f"  Processing batch {batch_idx}/{total_batches} ({len(batch)} paras)...")
        prompt = PROMPT_TEMPLATE.format(text=batch_text)
        
        modernized_text = call_gemini_api(api_key, prompt)
        if modernized_text == "QUOTA_EXHAUSTED":
            print(f"\n[STUCK] Script stopped at batch {batch_idx} because your API key's daily free quota was exhausted.")
            return "QUOTA_EXHAUSTED"
        elif modernized_text:
            # Append immediately to the final file
            with open(dest_path, "a", encoding="utf-8") as f_out:
                if os.path.getsize(dest_path) > 0 if os.path.exists(dest_path) else False:
                    f_out.write("\n\n")
                f_out.write(modernized_text)
            time.sleep(1)
        else:
            print(f"  [ERROR] Failed to modernize batch {batch_idx}")
            return False
            
    print(f"Chapter modernization complete! Saved to {dest_path}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Modernize raw book chapters using Gemini API.")
    parser.add_argument("--book", required=True, help="Book ID folder (e.g. two_cities)")
    parser.add_argument("--api-key", help="Gemini API Key")
    parser.add_argument("--chapters", help="Comma-separated chapter numbers or file tags to process (e.g. 1 or book2_ch_01). Processes all if omitted.")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Gemini API key must be provided via --api-key or GEMINI_API_KEY environment variable.")
        sys.exit(1)
        
    book_path = os.path.join(BASE_DIR, args.book)
    raw_chapters_dir = os.path.join(book_path, "chapters")
    
    if not os.path.exists(raw_chapters_dir):
        print(f"Error: chapters directory not found for {args.book}. Run split_raw_sources.py first.")
        sys.exit(1)
        
    if args.chapters:
        requested = [x.strip() for x in args.chapters.split(",")]
        raw_files = os.listdir(raw_chapters_dir)
        ch_list = []
        for req in requested:
            found = False
            for f in raw_files:
                if f == req or f == f"raw_{req}.txt" or (f == f"raw_ch_{int(req):02d}.txt" if req.isdigit() else False):
                    ch_list.append(f)
                    found = True
                    break
            if not found and req.isdigit():
                idx = int(req) - 1
                if args.book == "two_cities":
                    if idx < 6:
                        f = f"raw_book1_ch_{idx+1:02d}.txt"
                    elif idx < 30:
                        f = f"raw_book2_ch_{idx-6+1:02d}.txt"
                    else:
                        f = f"raw_book3_ch_{idx-30+1:02d}.txt"
                    if f in raw_files:
                        ch_list.append(f)
                        found = True
            if not found:
                print(f"Warning: could not resolve chapter parameter '{req}' to a file.")
    else:
        raw_files = os.listdir(raw_chapters_dir)
        ch_list = []
        for f in sorted(raw_files):
            if f.startswith("raw_") and f.endswith(".txt"):
                ch_list.append(f)
                
    print(f"Processing chapters: {ch_list}")
    
    for ch in ch_list:
        status = process_chapter(args.book, ch, api_key)
        if status == "QUOTA_EXHAUSTED":
            sys.exit(2) # Return exit code 2 on quota exhaustion
        elif not status:
            print("Process stopped due to failure.")
            sys.exit(1)
            
    print("\nAll requested chapters modernized successfully!")
    sys.exit(0)
