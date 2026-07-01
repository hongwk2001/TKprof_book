import json
import os

def create_script(txt_path, json_path):
    if not os.path.exists(txt_path):
        print(f"File not found: {txt_path}")
        return
        
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    # Strip special chars
    text = text.replace('*', '').replace('#', '')
    
    script_data = [{
        "character": "narrator",
        "voice": "en-US-ChristopherNeural",
        "text": text.strip()
    }]
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)
        
    print(f"Created {json_path}")

create_script('introduction_en.txt', 'scripts/script_intro.json')
create_script('copyright_en.txt', 'scripts/script_copyright.json')
