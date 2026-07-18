import os
import sys

# Force UTF-8 stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"d:\git_repo\TKprof_book\books\secret_garden"
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")

def main():
    print("Checking chapter titles for all Korean files...")
    
    for i in range(1, 28):
        ko_path = os.path.join(CHAPTERS_DIR, f"ch_{i:02d}_ko.txt")
        if not os.path.exists(ko_path):
            continue
            
        with open(ko_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            
        print(f"Chapter {i:02d}: '{first_line}'")
        
        # Verify if it starts with '제' (and contains '장')
        if not (first_line.startswith("제") and "장" in first_line):
            print(f"  --> WARNING: Missing proper title line!")

if __name__ == "__main__":
    main()
