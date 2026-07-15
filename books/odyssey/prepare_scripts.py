import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TAGGED_DIR = os.path.join(BASE_DIR, "chapters", "tagged")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

os.makedirs(SCRIPTS_DIR, exist_ok=True)

# Voice mapping based on approved plan
VOICE_MAP = {
    "Narrator": ("en-US-AndrewNeural", 1.0),
    "odysseus": ("en-US-BrianNeural", 1.0),
    "telemachus": ("en-US-ChristopherNeural", 1.0),
    "others": ("en-US-EricNeural", 1.0),
}

def parse_tagged_text(content):
    segments = []
    
    # We match <odysseus>, <telemachus>, or <others>
    pattern = re.compile(
        r'(<(?:odysseus|telemachus|others)>(.*?)</(?:odysseus|telemachus|others)>)|'
        r'((?:(?!<(?:odysseus|telemachus|others)>).)+)',
        re.DOTALL
    )
    
    # Let's find tags matching XML structure
    tag_pattern = re.compile(r'<(odysseus|telemachus|others)>(.*?)</\1>', re.DOTALL)
    
    # To split correctly, we can find all speaker tags and slice the text
    last_idx = 0
    for match in tag_pattern.finditer(content):
        start, end = match.span()
        # Anything before the tag is narration
        if start > last_idx:
            narration_text = content[last_idx:start].strip()
            if narration_text:
                segments.append({
                    "character": "Narrator",
                    "voice": VOICE_MAP["Narrator"][0],
                    "speed": VOICE_MAP["Narrator"][1],
                    "text": narration_text
                })
        # The speech tag itself
        tag_name = match.group(1)
        speech_text = match.group(2).strip()
        if speech_text:
            segments.append({
                "character": tag_name,
                "voice": VOICE_MAP[tag_name][0],
                "speed": VOICE_MAP[tag_name][1],
                "text": speech_text
            })
        last_idx = end
        
    # Any trailing narration
    if last_idx < len(content):
        narration_text = content[last_idx:].strip()
        if narration_text:
            segments.append({
                "character": "Narrator",
                "voice": VOICE_MAP["Narrator"][0],
                "speed": VOICE_MAP["Narrator"][1],
                "text": narration_text
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
            
            ch_num = re.search(r'ch_(\d+)', filename).group(1)
            out_filename = f"script_ch_{ch_num}.json"
            out_path = os.path.join(SCRIPTS_DIR, out_filename)
            
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(segments, f, ensure_ascii=False, indent=2)
                
            print(f"Generated {out_filename} with {len(segments)} segments.")

if __name__ == "__main__":
    main()
