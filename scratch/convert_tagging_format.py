import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGGED_DIR = os.path.join(BASE_DIR, "books", "secret_garden", "chapters", "tagged")

TAGS = "mary|colin|dickon|martha|craven|ben|others"

def wrap_untagged_narrator(text):
    if not text.strip():
        return text
        
    # Split by paragraph breaks to keep newlines outside of tags
    parts = text.split("\n\n")
    wrapped_parts = []
    for part in parts:
        if not part.strip():
            wrapped_parts.append(part)
        else:
            match = re.match(r'^(\s*)(.*?)(\s*)$', part, re.DOTALL)
            leading = match.group(1)
            inner = match.group(2)
            trailing = match.group(3)
            if inner:
                # Make sure we don't double wrap narrator if already wrapped (safety)
                if inner.startswith("<narrator>") and inner.endswith("</narrator>"):
                    wrapped_parts.append(part)
                else:
                    wrapped_parts.append(f"{leading}<narrator>{inner}</narrator>{trailing}")
            else:
                wrapped_parts.append(part)
                
    return "\n\n".join(wrapped_parts)

def migrate_content(content):
    # 1. Remove all quotes
    for q in ['"', '“', '”', "'", '‘', '’']:
        content = content.replace(q, '')
        
    # 2. Find all tag blocks (excluding narrator, which we are adding now)
    pattern = re.compile(r'(<(?P<tag>' + TAGS + r')>.*?</(?P=tag)>)', re.DOTALL)
    
    last_idx = 0
    new_parts = []
    
    for match in pattern.finditer(content):
        start, end = match.span()
        
        # Untagged text before the match
        untagged_text = content[last_idx:start]
        new_parts.append(wrap_untagged_narrator(untagged_text))
        
        # Tagged speech block
        tagged_text = content[start:end]
        new_parts.append(tagged_text)
        
        last_idx = end
        
    # Untagged text at the end
    untagged_text = content[last_idx:]
    new_parts.append(wrap_untagged_narrator(untagged_text))
    
    return "".join(new_parts)

def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = migrate_content(content)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    if not os.path.exists(TAGGED_DIR):
        print(f"Directory not found: {TAGGED_DIR}")
        return
        
    files = sorted([f for f in os.listdir(TAGGED_DIR) if f.startswith("tagged_") and f.endswith(".txt")])
    print(f"Migrating {len(files)} files to the new explicit tagging schema...")
    for filename in files:
        filepath = os.path.join(TAGGED_DIR, filename)
        migrate_file(filepath)
        print(f"  [MIGRATED] {filename}")
        
    print("\nMigration complete! All source files updated.")

if __name__ == "__main__":
    main()
