import os
import glob

dir_path = 'd:/git_repo/TKprof_book/books/richest_man_in_babylon/chapters'
out_path = os.path.join(dir_path, 'ch_06_seven_cures_for_a_lean_purse_en.txt')

parts = [
    'ch_06_part1_en.txt',
    'ch_06_part2_en.txt',
    'ch_06_part3_en.txt',
    'ch_06_part4_en.txt'
]

with open(out_path, 'w', encoding='utf-8') as outfile:
    for i, part in enumerate(parts):
        part_path = os.path.join(dir_path, part)
        if os.path.exists(part_path):
            with open(part_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                if i < len(parts) - 1:
                    outfile.write('\n\n')
        else:
            print(f"Missing {part_path}")

# Clean up temp files
for part in parts:
    part_path = os.path.join(dir_path, part)
    if os.path.exists(part_path):
        os.remove(part_path)

for part in glob.glob(os.path.join(dir_path, 'raw_ch_06_seven_cures_for_a_lean_purse_part*.txt')):
    os.remove(part)

print(f"Merged and cleaned up successfully into {out_path}")
