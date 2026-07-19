import os
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TAGGED_DIR = os.path.join(BASE_DIR, "chapters", "tagged")
SCRIPTS_EN_DIR = os.path.join(BASE_DIR, "scripts_en")
SCRIPTS_KO_DIR = os.path.join(BASE_DIR, "scripts_ko")

VALID_TAGS = {"mary", "colin", "dickon", "martha", "craven", "ben", "others"}
QUOTE_CHARS = {'"', '“', '”', "'"}

def check_file_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    tag_pattern = re.compile(r'</?(?:mary|colin|dickon|martha|craven|ben|others)>')
    matches = list(tag_pattern.finditer(content))
    
    stack = []
    errors = []
    
    for match in matches:
        tag_str = match.group()
        start_idx = match.start()
        line_num = content.count('\n', 0, start_idx) + 1
        
        if tag_str.startswith('</'):
            tag_name = tag_str[2:-1]
            if not stack:
                errors.append(f"Line {line_num}: Unopened closing tag {tag_str}")
            else:
                last_open_name, last_open_line = stack.pop()
                if last_open_name != tag_name:
                    errors.append(
                        f"Line {line_num}: Mismatched tags! Opened <{last_open_name}> on line {last_open_line} "
                        f"but closed with {tag_str}"
                    )
        else:
            tag_name = tag_str[1:-1]
            stack.append((tag_name, line_num))
            
    while stack:
        tag_name, line_num = stack.pop()
        errors.append(f"Line {line_num}: Unclosed opening tag <{tag_name}>")
        
    return errors

def check_json_file(filepath):
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            segments = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON format: {str(e)}"]
    except Exception as e:
        return [f"Failed to read file: {str(e)}"]
        
    if not isinstance(segments, list):
        return ["JSON root must be a list of segments"]
        
    for i, seg in enumerate(segments):
        # 1. Field validation
        for field in ["character", "voice", "speed", "text"]:
            if field not in seg:
                errors.append(f"Segment {i}: Missing required field '{field}'")
                
        if len(errors) > 10:  # Cap segment errors to prevent noise
            break
            
        char = seg.get("character")
        text = seg.get("text", "")
        
        # 2. Check for leaked XML tags inside dialogue text
        if isinstance(text, str):
            for tag in VALID_TAGS:
                if f"<{tag}>" in text or f"</{tag}>" in text:
                    errors.append(f"Segment {i} ({char}): Leaked XML tag found in text: '{text}'")
                    
            # 3. Check for leading/trailing quotation marks in direct speech
            if char != "Narrator" and text:
                stripped = text.strip()
                if stripped and (stripped[0] in QUOTE_CHARS or stripped[-1] in QUOTE_CHARS):
                    errors.append(f"Segment {i} ({char}): Direct speech text contains outer quotes: '{text}'")
                    
    return errors

def main():
    total_errors = 0
    
    # 1. XML Tag Checks
    print("============================================================")
    print("STEP 1: Checking Dialogue XML Tags...")
    print("============================================================")
    if os.path.exists(TAGGED_DIR):
        tagged_files = sorted([f for f in os.listdir(TAGGED_DIR) if f.startswith("tagged_") and f.endswith(".txt")])
        for filename in tagged_files:
            filepath = os.path.join(TAGGED_DIR, filename)
            errors = check_file_tags(filepath)
            if errors:
                print(f"[FAIL] {filename}:")
                for err in errors:
                    print(f"  - {err}")
                total_errors += len(errors)
            else:
                pass
    else:
        print("Tagged directory not found.")
        
    # 2. JSON Script Checks
    print("\n============================================================")
    print("STEP 2: Checking Generated JSON Scripts...")
    print("============================================================")
    for lang, directory in [("English", SCRIPTS_EN_DIR), ("Korean", SCRIPTS_KO_DIR)]:
        print(f"\nAuditing {lang} JSON scripts...")
        if os.path.exists(directory):
            json_files = sorted([f for f in os.listdir(directory) if f.endswith(".json")])
            for filename in json_files:
                filepath = os.path.join(directory, filename)
                errors = check_json_file(filepath)
                if errors:
                    print(f"[FAIL] {filename}:")
                    for err in errors:
                        print(f"  - {err}")
                    total_errors += len(errors)
        else:
            print(f"Directory {directory} not found.")
            
    print("\n" + "="*60)
    if total_errors == 0:
        print("[SUCCESS] All files passed XML and JSON integrity checks!")
    else:
        print(f"[FAIL] Found {total_errors} integrity errors across project files.")
    print("="*60)

if __name__ == "__main__":
    main()
