import os
import glob
import json
import re

# Determine directories relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(SCRIPT_DIR, "chapters_en_v2", "tagged")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "scripts")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# Kokoro voice mappings
VOICE_MAP = {
    "narrator": "am_michael",
    "beowulf": "bm_george",
    "hrothgar": "am_adam",
    "unferth": "am_adam",
    "wealhtheow": "bf_emma",
    "wiglaf": "am_adam",
    "rest": "af_sarah"
}

def parse_text_to_script(text):
    # Regex to split by any opening/closing tags of our characters
    pattern = r'(</?beowulf>|</?hrothgar>|</?unferth>|</?wealhtheow>|</?wiglaf>|</?rest>)'
    tokens = re.split(pattern, text)
    
    script = []
    current_voice = "narrator"
    
    tag_to_char = {
        "beowulf": "beowulf",
        "hrothgar": "hrothgar",
        "unferth": "unferth",
        "wealhtheow": "wealhtheow",
        "wiglaf": "wiglaf",
        "rest": "rest"
    }
    
    for token in tokens:
        if token.startswith("<") and token.endswith(">"):
            if not token.startswith("</"):
                char_name = token[1:-1]
                if char_name in tag_to_char:
                    current_voice = tag_to_char[char_name]
            else:
                current_voice = "narrator"
        else:
            txt = token.strip()
            # Strip markdown formatting symbols like asterisks or hash characters that shouldn't be read
            txt = txt.replace('*', '').replace('#', '')
            if txt:
                script.append({
                    "character": current_voice,
                    "voice": VOICE_MAP[current_voice],
                    "text": txt
                })
    return script

def process_all():
    files = sorted(glob.glob(os.path.join(CHAPTERS_DIR, "tagged_ch_*_en.txt")))
    print(f"Found {len(files)} tagged files in {CHAPTERS_DIR} to process.")
    for file_path in files:
        basename = os.path.basename(file_path)
        # e.g. tagged_ch_00_en.txt -> script_ch_00.json
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
