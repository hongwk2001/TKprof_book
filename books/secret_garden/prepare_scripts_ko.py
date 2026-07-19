import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TAGGED_DIR = os.path.join(BASE_DIR, "chapters", "tagged")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts_ko")

os.makedirs(SCRIPTS_DIR, exist_ok=True)

# Korean Cast Voice mappings (using edge-tts neural voices)
VOICE_MAP = {
    "Narrator": ("ko-KR-SunHiNeural", 1.0),
    "mary": ("ko-KR-SunHiNeural", 1.0),
    "colin": ("ko-KR-InJoonNeural", 1.0),
    "dickon": ("ko-KR-InJoonNeural", 1.0),
    "martha": ("ko-KR-SunHiNeural", 1.0),
    "craven": ("ko-KR-InJoonNeural", 0.95),
    "ben": ("ko-KR-InJoonNeural", 0.9),
    "others": ("ko-KR-HyunsuMultilingualNeural", 1.0),
}

def parse_tagged_text(content):
    segments = []
    
    # Matching any of our defined XML tags or non-tagged narration blocks
    pattern = re.compile(
        r'(<(?P<tag>mary|colin|dickon|martha|craven|ben|others)>(?P<speech>.*?)</(?P=tag)>)|'
        r'(?P<narration>(?:(?!<(?:mary|colin|dickon|martha|craven|ben|others)>).)+)', 
        re.DOTALL
    )
    
    for match in pattern.finditer(content):
        tag = match.group('tag')
        speech = match.group('speech')
        narration = match.group('narration')
        
        if tag and speech:
            text = speech.strip().strip('"\'“”')
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
        
    chapter_files = sorted([f for f in os.listdir(TAGGED_DIR) if f.endswith("_ko.txt")])
    for filename in chapter_files:
        filepath = os.path.join(TAGGED_DIR, filename)
        
        # Determine chapter number
        match = re.search(r'ch_(\d+)_ko\.txt', filename)
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
            
    print("Korean script JSON generation completed.")

if __name__ == "__main__":
    main()
