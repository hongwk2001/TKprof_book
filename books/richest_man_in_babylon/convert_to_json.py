import os
import glob
import json
import re

CHAPTERS_DIR = "chapters"
OUTPUT_DIR = "scripts"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

VOICE_MAP = {
    "narrator": "en-US-ChristopherNeural",
    "arkad": "en-US-SteffanNeural",
    "rest": "en-GB-RyanNeural"
}

def parse_text_to_script(text):
    # We will use regex to find all <tag>...</tag> and treat text outside as narrator.
    # regex pattern to match tags and non-tags
    # pattern: (.*?)<(arkad|rest)>(.*?)</\2>
    # Wait, simple tokenization is better.
    
    # Let's split by <arkad>, </arkad>, <rest>, </rest>
    tokens = re.split(r'(</?arkad>|</?rest>)', text)
    
    script = []
    current_voice = "narrator"
    
    for token in tokens:
        if token == "<arkad>":
            current_voice = "arkad"
        elif token == "</arkad>":
            current_voice = "narrator"
        elif token == "<rest>":
            current_voice = "rest"
        elif token == "</rest>":
            current_voice = "narrator"
        else:
            txt = token.strip()
            # Strip problematic characters for TTS
            txt = txt.replace('*', '').replace('#', '')
            if txt: # only append non-empty text
                script.append({
                    "character": current_voice,
                    "voice": VOICE_MAP[current_voice],
                    "text": txt
                })
    return script

def process_all():
    files = sorted(glob.glob(os.path.join(CHAPTERS_DIR, "tagged_ch_*_en.txt")))
    for file_path in files:
        basename = os.path.basename(file_path)
        # e.g. tagged_ch_04_the_man_who_desired_gold_en.txt -> script_ch_04.json
        match = re.search(r'tagged_ch_(\d+)', basename)
        if match:
            ch_num = match.group(1)
            out_name = f"script_ch_{ch_num}.json"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            script_data = parse_text_to_script(content)
            
            out_path = os.path.join(OUTPUT_DIR, out_name)
            with open(out_path, 'w', encoding='utf-8') as out_f:
                json.dump(script_data, out_f, indent=2, ensure_ascii=False)
            print(f"Generated {out_path}")

if __name__ == "__main__":
    process_all()
