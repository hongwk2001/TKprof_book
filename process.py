import os
import shutil

src_dir = r"C:\Users\hongw\.gemini\antigravity\brain\6fe0243e-4057-4007-b994-c7d4a9aaa4f3\scratch"
ko_out = r"d:\git_repo\TKprof_book\books\tono_bungay\chapters\book1\book1_ch02_ko.txt"
en_out = r"d:\git_repo\TKprof_book\books\tono_bungay\chapters\book1\book1_ch02_en.txt"

with open(ko_out, 'wb') as fko:
    for i in range(1, 8):
        ko_file = os.path.join(src_dir, f"proposal_ko_{i}.txt")
        if os.path.exists(ko_file):
            with open(ko_file, 'rb') as f:
                fko.write(f.read())
            fko.write(b'\n')

with open(en_out, 'wb') as fen:
    for i in range(1, 8):
        en_file = os.path.join(src_dir, f"proposal_en_{i}.txt")
        if os.path.exists(en_file):
            with open(en_file, 'rb') as f:
                fen.write(f.read())
            fen.write(b'\n')

print("All chunks have been combined successfully!")
