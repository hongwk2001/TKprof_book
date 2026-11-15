import json
import glob
import os

def validate_all():
    files = glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/*.json')
    if not files:
        print("ERROR: No JSON files found!")
        return

    print(f"Validating {len(files)} JSON files...\n")
    
    total_omissions = 0
    schema_errors = 0
    continuity_errors = 0
    
    required_keys = {"id", "tag", "raw", "en", "ko", "is_header"}

    for filepath in files:
        filename = os.path.basename(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[SYNTAX ERROR] {filename}: {e}")
            schema_errors += 1
            continue
            
        expected_id = 1
        seen_tags = set()
        
        for item in data:
            # 1. Schema check
            if not isinstance(item, dict):
                print(f"[SCHEMA ERROR] {filename}: item is not a dictionary")
                schema_errors += 1
                continue
                
            missing_keys = required_keys - set(item.keys())
            if missing_keys:
                print(f"[SCHEMA ERROR] {filename} (Tag {item.get('tag')}): Missing keys {missing_keys}")
                schema_errors += 1
                
            # 2. Continuity check
            item_id = item.get('id')
            item_tag = item.get('tag')
            
            if item_id != expected_id:
                print(f"[CONTINUITY ERROR] {filename}: Expected ID {expected_id}, got {item_id}")
                continuity_errors += 1
            expected_id += 1
            
            if item_tag in seen_tags:
                print(f"[CONTINUITY ERROR] {filename}: Duplicate tag found: {item_tag}")
                continuity_errors += 1
            if item_tag:
                seen_tags.add(item_tag)
                
            # 3. Omission check
            raw = item.get('raw', '')
            en = item.get('en', '')
            
            if item.get('is_header') or not raw or not en:
                continue
                
            raw_words = len(raw.split())
            en_words = len(en.split())
            
            if raw_words >= 8 and (en_words / raw_words) < 0.5:
                print(f"[OMISSION] {filename} (Tag {item_tag}): Ratio {round(en_words/raw_words, 2)}")
                total_omissions += 1

    print("\n--- VALIDATION RESULTS ---")
    print(f"Files Scanned: {len(files)}")
    print(f"Schema Errors: {schema_errors}")
    print(f"Continuity Errors: {continuity_errors}")
    print(f"Remaining Severe Omissions: {total_omissions}")
    
    if schema_errors == 0 and continuity_errors == 0 and total_omissions == 0:
        print("\n[PERFECT PASS] The dataset is pristine.")
    else:
        print("\n[FAILED] Check the errors above.")

if __name__ == "__main__":
    validate_all()
