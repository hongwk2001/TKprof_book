import os
import glob
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TAGGED_DIR = os.path.join(SCRIPT_DIR, "chapters_kr_v2", "tagged")
INPUT_DIR = os.path.join(SCRIPT_DIR, "chapters_kr_v2")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "scripts_ko")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_voice_and_speed(character, text):
    """
    Returns (voice_id, speed_offset) based on character and dialogue content.
    Voice Mapping:
      - Narrator: ko-KR-InJoonNeural (speed "+0%")
      - 베오울프: ko-KR-HyunsuMultilingualNeural (speed "+5%")
      - 흐로스가르: ko-KR-InJoonNeural (speed "-12%")
      - 위글라프 / 기타: ko-KR-HyunsuMultilingualNeural (speed "+0%")
      - 여왕 / 여성: ko-KR-SunHiNeural (speed "+0%")
    """
    if character == "narrator":
        return "ko-KR-InJoonNeural", "+0%"
    elif character == "베오울프":
        return "ko-KR-HyunsuMultilingualNeural", "+5%"
    elif character == "흐로스가르":
        return "ko-KR-InJoonNeural", "-12%"
    elif character == "위글라프":
        return "ko-KR-HyunsuMultilingualNeural", "+0%"
    elif character == "기타":
        # Check if the dialogue or text has female indicators
        female_keywords = ["여왕", "왕비", "웰흐세오우", "힐드부르흐", "어머니", "휘그드", "여인", "여성", "그렌델의 어미"]
        if any(kw in text for kw in female_keywords):
            return "ko-KR-SunHiNeural", "+0%"
        return "ko-KR-HyunsuMultilingualNeural", "+0%"
    else:
        return "ko-KR-HyunsuMultilingualNeural", "+0%"

def parse_tagged_text_to_script(text):
    # Regex to split by any opening/closing tags of our characters
    pattern = r'(</?베오울프>|</?흐로스가르>|</?위글라프>|</?기타>)'
    tokens = re.split(pattern, text)
    
    script = []
    current_char = "narrator"
    
    tag_to_char = {
        "베오울프": "베오울프",
        "흐로스가르": "흐로스가르",
        "위글라프": "위글라프",
        "기타": "기타"
    }
    
    for token in tokens:
        if token.startswith("<") and token.endswith(">"):
            if not token.startswith("</"):
                char_name = token[1:-1]
                if char_name in tag_to_char:
                    current_char = tag_to_char[char_name]
            else:
                current_char = "narrator"
        else:
            txt = token.strip()
            # Strip formatting asterisks/hash characters if any
            txt = txt.replace('*', '').replace('#', '')
            if txt:
                voice, speed = get_voice_and_speed(current_char, txt)
                script.append({
                    "character": current_char,
                    "voice": voice,
                    "speed": speed,
                    "text": txt
                })
    return script

def process_chapters():
    files = sorted(glob.glob(os.path.join(TAGGED_DIR, "tagged_ch_*_ko.txt")))
    print(f"Found {len(files)} tagged files in {TAGGED_DIR} to process.")
    for file_path in files:
        basename = os.path.basename(file_path)
        # e.g., tagged_ch_00_ko.txt -> script_ch_00.json
        match = re.search(r'tagged_ch_(\d+)', basename)
        if match:
            ch_num = match.group(1)
            out_name = f"script_ch_{ch_num}.json"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            script_data = parse_tagged_text_to_script(content)
            
            out_path = os.path.join(OUTPUT_DIR, out_name)
            with open(out_path, 'w', encoding='utf-8') as out_f:
                json.dump(script_data, out_f, indent=2, ensure_ascii=False)
            print(f"Generated {out_path}")

def process_special_files():
    # Process introduction_ko_v2.txt -> scripts_ko/script_intro.json
    intro_txt_path = os.path.join(INPUT_DIR, "introduction_ko_v2.txt")
    if os.path.exists(intro_txt_path):
        with open(intro_txt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip().replace('*', '').replace('#', '')
        
        voice, speed = get_voice_and_speed("narrator", content)
        script_data = [{
            "character": "narrator",
            "voice": voice,
            "speed": speed,
            "text": content
        }]
        
        out_path = os.path.join(OUTPUT_DIR, "script_intro.json")
        with open(out_path, 'w', encoding='utf-8') as out_f:
            json.dump(script_data, out_f, indent=2, ensure_ascii=False)
        print(f"Generated {out_path}")

    # Process copyright_ko_v2.txt -> scripts_ko/script_closing.json
    closing_txt_path = os.path.join(INPUT_DIR, "copyright_ko_v2.txt")
    if os.path.exists(closing_txt_path):
        with open(closing_txt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip().replace('*', '').replace('#', '')
            
        voice, speed = get_voice_and_speed("narrator", content)
        script_data = [{
            "character": "narrator",
            "voice": voice,
            "speed": speed,
            "text": content
        }]
        
        out_path = os.path.join(OUTPUT_DIR, "script_closing.json")
        with open(out_path, 'w', encoding='utf-8') as out_f:
            json.dump(script_data, out_f, indent=2, ensure_ascii=False)
        print(f"Generated {out_path}")

if __name__ == "__main__":
    process_chapters()
    process_special_files()
