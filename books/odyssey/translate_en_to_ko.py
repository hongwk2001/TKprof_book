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

BASE_DIR = r"d:\git_repo\TKprof_book\books\odyssey"

def load_env():
    # Look for .env in project root (two levels up from odyssey folder)
    path = os.path.join(BASE_DIR, "..", "..", ".env")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    parts = line.split("=", 1)
                    os.environ[parts[0].strip()] = parts[1].strip()

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
                # Check for retry duration
                match = re.search(r'retry in\s+([\d\.]+)s', err_body)
                wait_secs = None
                if match:
                    wait_secs = float(match.group(1)) + 2.0
                else:
                    # Check in JSON structure for retryDelay
                    try:
                        res_json = json.loads(err_body)
                        for detail in res_json.get("details", []):
                            if "retryDelay" in detail:
                                secs = float(detail["retryDelay"].replace("s", ""))
                                wait_secs = secs + 2.0
                                break
                    except Exception:
                        pass
                
                if wait_secs is not None:
                    print(f"Rate limit (RPM) hit. Sleeping for {wait_secs:.1f}s before retry...")
                    time.sleep(wait_secs)
                else:
                    # No retry info, so it's a real daily quota exhaustion or credit depletion
                    print(f"\n[QUOTA_EXHAUSTED] Daily limit or credits depleted on attempt {attempt+1} (HTTP 429): {err_body}")
                    return "QUOTA_EXHAUSTED"
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

def translate_chapter(ch_num, api_key):
    chapters_dir = os.path.join(BASE_DIR, "chapters")
    src_filename = f"ch_{ch_num:02d}_en.txt"
    dest_filename = f"ch_{ch_num:02d}_ko.txt"
    
    src_path = os.path.join(chapters_dir, src_filename)
    dest_path = os.path.join(chapters_dir, dest_filename)
    
    if not os.path.exists(src_path):
        print(f"Source chapter file not found: {src_path}")
        return False
        
    print(f"\n--- Direct Translating {src_filename} to Korean ({dest_filename}) ---")
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    paragraphs = split_into_paragraphs(content)
    print(f"Total paragraphs in English chapter: {len(paragraphs)}")
    
    # Load translation prompt template
    prompt_file = os.path.join(BASE_DIR, "prompt_en_to_ko.txt")
    if os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as pf:
            prompt_template = pf.read()
    else:
        print("Error: prompt_en_to_ko.txt not found!")
        return False
        
    batch_size = 10
    start_batch = 0
    
    # Clean file and start from scratch if we want to overwrite, otherwise support resume
    if os.path.exists(dest_path):
        with open(dest_path, "r", encoding="utf-8") as f_existing:
            existing_content = f_existing.read()
        existing_paragraphs = split_into_paragraphs(existing_content)
        start_batch = len(existing_paragraphs) // batch_size
        print(f"Found existing progress: {len(existing_paragraphs)} paragraphs completed (~{start_batch} batches).")
        
    total_batches = (len(paragraphs) + batch_size - 1) // batch_size
    
    for i in range(start_batch * batch_size, len(paragraphs), batch_size):
        batch_idx = i // batch_size + 1
        batch = paragraphs[i:i+batch_size]
        batch_text = "\n\n".join(batch)
        
        print(f"  Processing translation batch {batch_idx}/{total_batches} ({len(batch)} paras)...")
        prompt = f"{prompt_template}\n\nText to translate:\n{batch_text}"
        
        translated_text = call_gemini_api(api_key, prompt)
        if translated_text == "QUOTA_EXHAUSTED":
            print(f"\n[STUCK] Script stopped at batch {batch_idx} because daily free quota is exhausted.")
            return "QUOTA_EXHAUSTED"
        elif translated_text:
            with open(dest_path, "a", encoding="utf-8") as f_out:
                if os.path.getsize(dest_path) > 0 if os.path.exists(dest_path) else False:
                    f_out.write("\n\n")
                f_out.write(translated_text)
            time.sleep(8)
        else:
            print(f"  [ERROR] Failed to translate batch {batch_idx}")
            return False
            
    print(f"Chapter {ch_num} translation complete!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate modernized English chapters to Korean.")
    parser.add_argument("--chapters", required=True, help="Comma-separated chapter numbers (e.g. 3,4 or 1-24)")
    parser.add_argument("--overwrite", action="store_true", help="Delete existing Korean translations and start fresh")
    
    args = parser.parse_args()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)
        
    # Resolve chapter numbers
    ch_nums = []
    if "-" in args.chapters:
        start_ch, end_ch = args.chapters.split("-")
        ch_nums = list(range(int(start_ch), int(end_ch) + 1))
    else:
        ch_nums = [int(x.strip()) for x in args.chapters.split(",")]
        
    if args.overwrite:
        print("Overwrite flag set. Deleting target files for selected chapters...")
        for ch in ch_nums:
            dest_filename = f"ch_{ch:02d}_ko.txt"
            dest_path = os.path.join(BASE_DIR, "chapters", dest_filename)
            if os.path.exists(dest_path):
                os.remove(dest_path)
                print(f"Deleted {dest_filename}")
                
    for ch in ch_nums:
        res = translate_chapter(ch, api_key)
        if res == "QUOTA_EXHAUSTED":
            print("Translation stopped due to quota exhaustion.")
            sys.exit(1)
        elif not res:
            print(f"Aborting due to failure in chapter {ch}.")
            sys.exit(1)
            
    print("All requested translations finished successfully!")
