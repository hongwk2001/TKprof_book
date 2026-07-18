import os
import sys
import re

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\git_repo\TKprof_book\books\secret_garden"
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

def clean_text(val):
    # Strip backticks, quotes, bolding, leading/trailing ellipses, and whitespace
    val = re.sub(r'^[`"\'*\.\s~…]+', '', val)
    val = re.sub(r'[`"\'*\.\s~…]+$', '', val)
    return val.strip()

def main():
    print("Applying translation audit fixes with advanced stripping...")
    
    total_attempted = 0
    total_applied = 0
    total_failed = 0
    
    for i in range(1, 28):
        txt_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_ko.txt")
        audit_path = os.path.join(CHAPTERS_DIR, f"audit_ch_{i:02d}.md")
        
        if not os.path.exists(txt_path) or not os.path.exists(audit_path):
            continue
            
        with open(txt_path, "r", encoding="utf-8") as f:
            txt_content = f.read()
            
        with open(audit_path, "r", encoding="utf-8") as f:
            audit_content = f.read()
            
        lines = audit_content.split("\n")
        
        replacements = []
        curr_val = None
        prop_val = None
        
        re_curr = re.compile(r'(current|기존|현행)', re.IGNORECASE)
        re_prop = re.compile(r'(proposed|수정|제안|변경)', re.IGNORECASE)
        
        for line in lines:
            if ":" in line:
                parts = line.split(":", 1)
                label = parts[0].replace("-", "").replace("*", "").strip().lower()
                val = parts[1].strip()
                
                if re_curr.search(label):
                    curr_val = clean_text(val)
                elif re_prop.search(label):
                    prop_val = clean_text(val)
                    if curr_val and prop_val:
                        replacements.append((curr_val, prop_val))
                        curr_val = None
                        prop_val = None
                        
        if not replacements:
            continue
            
        modified = False
        
        for curr, prop in replacements:
            if not curr:
                continue
            total_attempted += 1
            
            # Try to replace exactly
            if curr in txt_content:
                txt_content = txt_content.replace(curr, prop)
                total_applied += 1
                modified = True
            else:
                # Try with normalized spaces
                escaped = re.escape(curr)
                pattern = re.sub(r'\\ ', r'\\s+', escaped)
                try:
                    match = re.search(pattern, txt_content)
                    if match:
                        txt_content = txt_content[:match.start()] + prop + txt_content[match.end():]
                        total_applied += 1
                        modified = True
                    else:
                        # Let's print out the failed ones so we can see them
                        total_failed += 1
                        print(f"  Warning: Could not find target text in Chapter {i:02d}.")
                        print(f"    Target: '{curr}'")
                        print(f"    Proposed: '{prop}'")
                except Exception as e:
                    total_failed += 1
                    print(f"  Regex match error for target in Chapter {i:02d}: {e}")
                    
        if modified:
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(txt_content)
                
    print(f"\nAudit Application Summary:")
    print(f"  Total Attempted: {total_attempted}")
    print(f"  Successfully Applied: {total_applied}")
    print(f"  Failed to Apply: {total_failed}")

if __name__ == "__main__":
    main()
