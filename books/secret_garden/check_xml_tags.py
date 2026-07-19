import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TAGGED_DIR = os.path.join(BASE_DIR, "chapters", "tagged")

VALID_TAGS = {"mary", "colin", "dickon", "martha", "craven", "ben", "others"}

def check_file_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all tags in order
    tag_pattern = re.compile(r'</?(?:mary|colin|dickon|martha|craven|ben|others)>')
    tags = tag_pattern.findall(content)
    
    stack = []
    errors = []
    
    # We can also track line numbers by counting newlines before each match
    matches = list(tag_pattern.finditer(content))
    
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

def main():
    if not os.path.exists(TAGGED_DIR):
        print(f"Directory {TAGGED_DIR} does not exist.")
        return
        
    files = sorted([f for f in os.listdir(TAGGED_DIR) if f.startswith("tagged_") and f.endswith(".txt")])
    
    total_errors = 0
    print("Checking dialogue tags integrity across all chapters...")
    
    for filename in files:
        filepath = os.path.join(TAGGED_DIR, filename)
        errors = check_file_tags(filepath)
        if errors:
            print(f"\n[ERROR] {filename} failed integrity check:")
            for err in errors:
                print(f"  {err}")
            total_errors += len(errors)
            
    if total_errors == 0:
        print("\n[SUCCESS] All tagged files have 100% correct matching XML tag pairs!")
    else:
        print(f"\n[FAIL] Found {total_errors} tag integrity errors across files.")

if __name__ == "__main__":
    main()
