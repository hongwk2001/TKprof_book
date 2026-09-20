import json
import sys

def update_file(json_file_path, translated_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    with open(translated_file_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)
        
    updated = 0
    for block in data:
        tag = block['tag']
        if tag in translations:
            en = translations[tag].get('en', '')
            ko = translations[tag].get('ko', '')
            if en: block['en'] = en
            if ko: block['ko'] = ko
            updated += 1
            
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Updated {updated} blocks.")

if __name__ == "__main__":
    update_file(sys.argv[1], sys.argv[2])
