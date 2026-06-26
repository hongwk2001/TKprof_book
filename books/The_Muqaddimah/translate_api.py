import urllib.request
import urllib.parse
import json
import re
import time

def translate_ar_to_en(text):
    # If there are no arabic characters, return as is
    if not re.search(r'[\u0600-\u06FF]', text):
        return text
        
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=ar&tl=en&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return "".join([x[0] for x in data[0]])
    except Exception as e:
        print(f"Translation failed for '{text}': {e}")
        # fallback to removing arabic chars if it fails
        return re.sub(r'[\u0600-\u06FF]+', '', text)

with open('muqaddimah_summary.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Translating lines using Google Translate API...")
with open('muqaddimah_summary_en.md', 'w', encoding='utf-8') as f:
    for i, line in enumerate(lines):
        if i % 50 == 0:
            print(f"Processing line {i}/{len(lines)}...")
            
        if '| Title (Arabic) |' in line:
            f.write('| Title (English) | Page Count | Word Count |\n')
        elif line.startswith('|---'):
            f.write('|---|---|---|\n')
        elif line.startswith('| ') and not line.startswith('| Title'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                ar_title = parts[1]
                
                # First, translate the entire arabic string using the API
                en_title = translate_ar_to_en(ar_title)
                
                word_count_str = parts[3].replace(',', '')
                try:
                    words = int(word_count_str)
                    page_count = max(1, (words + 299) // 300)
                except ValueError:
                    page_count = 1
                    
                f.write(f"| {en_title} | {page_count} | {parts[3]} |\n")
                # Sleep briefly to avoid rate limiting
                time.sleep(0.1)
            else:
                f.write(line)
        else:
            if "Estimated Start Page" in line:
                pass
            else:
                f.write(line)

print("Translation complete.")
