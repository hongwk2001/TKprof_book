import os
import glob
import shutil

CHAPTERS_DIR = "chapters"

# Copy chapters 00, 01, 02 to tagged_...
for ch_num in ["00", "01", "02"]:
    matches = glob.glob(os.path.join(CHAPTERS_DIR, f"ch_{ch_num}_*_en.txt"))
    if matches:
        src = matches[0]
        basename = os.path.basename(src)
        dst = os.path.join(CHAPTERS_DIR, f"tagged_{basename}")
        shutil.copy2(src, dst)
        print(f"Copied {src} to {dst}")

# Merge chapters 03 through 11
for ch_num in range(3, 12):
    ch_str = f"{ch_num:02d}"
    # find the base name of the chapter
    base_matches = glob.glob(os.path.join(CHAPTERS_DIR, f"ch_{ch_str}_*_en.txt"))
    if not base_matches:
        continue
        
    src_base = os.path.basename(base_matches[0])
    dst_name = f"tagged_{src_base}"
    dst_path = os.path.join(CHAPTERS_DIR, dst_name)
    
    parts = sorted(glob.glob(os.path.join(CHAPTERS_DIR, f"tagged_ch_{ch_str}_part*.txt")))
    if not parts:
        print(f"Warning: No tagged parts found for chapter {ch_str}")
        continue
        
    print(f"Merging {len(parts)} parts for chapter {ch_str} into {dst_name}")
    with open(dst_path, 'w', encoding='utf-8') as outfile:
        for part in parts:
            with open(part, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
            outfile.write("\n") # Ensure newline between parts
            
print("Merging complete.")
