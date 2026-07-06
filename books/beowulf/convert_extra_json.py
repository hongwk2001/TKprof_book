import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(SCRIPT_DIR, "chapters_en_v2")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "scripts")

def convert_extra(file_name, out_name):
    file_path = os.path.join(CHAPTERS_DIR, file_name)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()
        
    # Clean up formatting characters
    text = text.replace('*', '').replace('#', '')
    
    script_data = [
        {
            "character": "narrator",
            "voice": "am_michael",
            "text": text
        }
    ]
    
    out_path = os.path.join(OUTPUT_DIR, out_name)
    with open(out_path, 'w', encoding='utf-8') as out_f:
        json.dump(script_data, out_f, indent=2, ensure_ascii=False)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    convert_extra("introduction_en_v2.txt", "script_intro.json")
    convert_extra("copyright_en_v2.txt", "script_closing.json")
