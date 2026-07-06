import os
import glob
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TAGGED_DIR = os.path.join(SCRIPT_DIR, "chapters", "tagged")
INPUT_DIR = os.path.join(SCRIPT_DIR, "chapters")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "scripts_ko")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_voice_and_speed(character, text):
    """
    Returns (voice_id, speed_offset) based on character.
    Voice Mapping:
      - narrator: ko-KR-SunHiNeural (speed "+0%")
      - 발랜시: ko-KR-SunHiNeural (speed "+5%")
      - 바니: ko-KR-HyunsuMultilingualNeural (speed "+2%")
      - 기타여성: ko-KR-SunHiNeural (speed "-8%")
      - 기타남성: ko-KR-InJoonNeural (speed "-5%")
    """
    if character == "narrator":
        return "ko-KR-SunHiNeural", "+0%"
    elif character == "발랜시":
        return "ko-KR-SunHiNeural", "+5%"
    elif character == "바니":
        return "ko-KR-HyunsuMultilingualNeural", "+2%"
    elif character == "기타여성":
        return "ko-KR-SunHiNeural", "-8%"
    elif character == "기타남성":
        return "ko-KR-InJoonNeural", "-5%"
    else:
        return "ko-KR-SunHiNeural", "+0%"

# Roman to words mappings for cleanups
ROMAN_TO_WORDS_KO = {
    "I": "일", "II": "이", "III": "삼", "IV": "사", "V": "오",
    "VI": "육", "VII": "칠", "VIII": "팔", "IX": "구", "X": "십",
    "XI": "십일", "XII": "십이", "XIII": "십삼", "XIV": "십사",
    "XV": "십오", "XVI": "십육", "XVII": "십칠", "XVIII": "십팔",
    "XIX": "십구", "XX": "이십", "XXI": "이십일", "XXII": "이십이",
    "XXIII": "이십삼", "XXIV": "이십사", "XXV": "이십오", "XXVI": "이십육",
    "XXVII": "이십칠", "XXVIII": "이십팔", "XXIX": "이십구", "XXX": "삼십"
}

def clean_phonetics(text):
    """Replaces Roman numerals, abbreviations, and symbols with phonetic text."""
    # Replace chapter headers e.g. "제I장" or "제 I 장"
    for roman, word in ROMAN_TO_WORDS_KO.items():
        text = re.sub(rf"제\s*{roman}\s*장", f"제 {word} 장", text)
        text = re.sub(rf"## {roman}\b", f"## 제 {word} 장", text)
        
    text = re.sub(r"&", "그리고", text)
    return text

def parse_tagged_text_to_script(text):
    # Regex to split by any opening/closing tags of our characters
    pattern = r'(</?발랜시>|</?바니>|</?기타여성>|</?기타남성>)'
    tokens = re.split(pattern, text)
    
    script = []
    current_char = "narrator"
    
    tag_to_char = {
        "발랜시": "발랜시",
        "바니": "바니",
        "기타여성": "기타여성",
        "기타남성": "기타남성"
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
                # Apply phonetic cleanups to the content
                txt = clean_phonetics(txt)
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
        # e.g., tagged_ch_01_ko.txt -> script_ch_01.json
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
    # Process introduction_ko.txt -> scripts_ko/script_intro.json
    intro_txt_path = os.path.join(INPUT_DIR, "introduction_ko.txt")
    if os.path.exists(intro_txt_path):
        with open(intro_txt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip().replace('*', '').replace('#', '')
        
        # Phonetic cleanup
        content = clean_phonetics(content)
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

    # Process copyright_ko.txt -> scripts_ko/script_closing.json
    closing_txt_path = os.path.join(INPUT_DIR, "copyright_ko.txt")
    if os.path.exists(closing_txt_path):
        with open(closing_txt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip().replace('*', '').replace('#', '')
            
        content = clean_phonetics(content)
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
