import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TAGGED_DIR = os.path.join(BASE_DIR, "chapters", "tagged")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts_en")

os.makedirs(SCRIPTS_DIR, exist_ok=True)

# Voice mapping based on approved plan
VOICE_MAP = {
    "Narrator": ("af_heart", 1.0),       # Generic soothing female narrator
    "Lotty": ("af_bella", 1.0),          # Lotty (Mrs. Wilkins)
    "Rose": ("bf_lily", 1.0),            # Rose (Mrs. Arbuthnot) - updated to bf_lily
    "Other": ("am_michael", 1.0),        # Others
}

def parse_tagged_text(content):
    # This regex looks for text wrapped in our XML tags or plain text
    # It assumes the file is composed of tagged sections and plain narration
    segments = []
    
    # Simple regex to find all <Tag>...</Tag> and text outside them
    pattern = re.compile(r'(<(?P<tag>Lotty|Rose|Other)>(?P<speech>.*?)</(?P=tag)>)|(?P<narration>(?:(?!<Lotty>|<Rose>|<Other>).)+)', re.DOTALL)
    
    for match in pattern.finditer(content):
        tag = match.group('tag')
        speech = match.group('speech')
        narration = match.group('narration')
        
        if tag and speech:
            text = speech.strip()
            if text:
                voice, speed = VOICE_MAP[tag]
                segments.append({
                    "character": tag,
                    "voice": voice,
                    "speed": speed,
                    "text": text
                })
        elif narration:
            text = narration.strip()
            if text:
                voice, speed = VOICE_MAP["Narrator"]
                segments.append({
                    "character": "Narrator",
                    "voice": voice,
                    "speed": speed,
                    "text": text
                })
                
    return segments

def main():
    if not os.path.exists(TAGGED_DIR):
        print(f"Directory {TAGGED_DIR} does not exist.")
        return
        
    for filename in sorted(os.listdir(TAGGED_DIR)):
        if filename.endswith("_en.txt"):
            file_path = os.path.join(TAGGED_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            segments = parse_tagged_text(content)
            
            # Save to JSON
            ch_num = re.search(r'ch_(\d+)', filename).group(1)
            out_filename = f"script_ch_{ch_num}.json"
            out_path = os.path.join(SCRIPTS_DIR, out_filename)
            
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(segments, f, ensure_ascii=False, indent=2)
                
            print(f"Generated {out_filename} with {len(segments)} segments.")

if __name__ == "__main__":
    main()
