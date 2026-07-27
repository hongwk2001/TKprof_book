import os
import glob

BASE_DIR = r"d:\git_repo\TKprof_book\books\frankenstein\chapters"
PARTS_DIR = os.path.join(BASE_DIR, "parts")
os.makedirs(PARTS_DIR, exist_ok=True)

def split_file(filepath):
    filename = os.path.basename(filepath)
    print(f"Splitting {filename}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    
    chunk_size = 25
    part_idx = 0
    for i in range(0, len(paragraphs), chunk_size):
        chunk = paragraphs[i:i+chunk_size]
        part_filename = filename.replace(".txt", f"_part_{part_idx:02d}.txt")
        part_path = os.path.join(PARTS_DIR, part_filename)
        with open(part_path, "w", encoding="utf-8") as out:
            out.write("\n\n".join(chunk))
        print(f"  Saved {part_filename} ({len(chunk)} paragraphs)")
        part_idx += 1

def main():
    ko_files = sorted(glob.glob(os.path.join(BASE_DIR, "ch_*_ko.txt")))
    for kf in ko_files:
        split_file(kf)

if __name__ == "__main__":
    main()
