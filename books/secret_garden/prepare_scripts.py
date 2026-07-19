import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TAGGED_DIR = os.path.join(BASE_DIR, "chapters", "tagged")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts_en")

os.makedirs(SCRIPTS_DIR, exist_ok=True)

# English Cast Voice mappings (from approved candidate samples)
VOICE_MAP = {
    "Narrator": ("af_sarah", 1.0),
    "mary": ("af_sarah", 1.0),      # Changed from af_nicole to af_sarah as af_nicole was deleted
    "colin": ("am_adam", 1.0),
    "dickon": ("am_michael", 1.0),   # Changed from bm_george to am_michael as bm_george was deleted
    "martha": ("bf_isabella", 1.0),
    "craven": ("bm_lewis", 1.0),
    "ben": ("bm_lewis", 0.95),  # Aged older voice
    "others": ("am_michael", 1.0),
}

def parse_tagged_text(content):
    segments = []
    
    # Matching any of our defined XML tags including narrator
    pattern = re.compile(
        r'<(?P<tag>mary|colin|dickon|martha|craven|ben|others|narrator)>(?P<speech>.*?)</(?P=tag)>',
        re.DOTALL
    )
    
    for match in pattern.finditer(content):
        tag = match.group('tag')
        speech = match.group('speech')
        
        if tag and speech:
            text = speech.strip()
            for q in ['"', '“', '”', "'", '‘', '’']:
                text = text.replace(q, '')
            if text:
                char_name = "Narrator" if tag == "narrator" else tag
                voice, speed = VOICE_MAP[char_name]
                segments.append({
                    "character": char_name,
                    "voice": voice,
                    "speed": speed,
                    "text": text
                })
                
    return segments

def main():
    if not os.path.exists(TAGGED_DIR):
        print(f"Directory {TAGGED_DIR} does not exist.")
        return
        
    chapter_files = sorted([f for f in os.listdir(TAGGED_DIR) if f.endswith("_en.txt")])
    for filename in chapter_files:
        filepath = os.path.join(TAGGED_DIR, filename)
        
        # Determine chapter number
        match = re.search(r'ch_(\d+)_en\.txt', filename)
        if not match:
            continue
        ch_num = match.group(1)
        
        print(f"Parsing {filename} into segments...")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        segments = parse_tagged_text(content)
        
        out_filepath = os.path.join(SCRIPTS_DIR, f"script_ch_{ch_num}.json")
        with open(out_filepath, "w", encoding="utf-8") as f:
            json.dump(segments, f, ensure_ascii=False, indent=2)
            
    print("English script JSON generation completed.")

if __name__ == "__main__":
    main()
