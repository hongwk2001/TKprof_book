import os
import glob

dir_path = 'd:/git_repo/TKprof_book/books/richest_man_in_babylon/chapters'

chapters = {
    '04': {
        'name': 'ch_04_the_man_who_desired_gold_en.txt',
        'parts': ['ch_04_part1_en.txt', 'ch_04_part2_en.txt']
    },
    '05': {
        'name': 'ch_05_the_richest_man_in_babylon_en.txt',
        'parts': ['ch_05_part1_en.txt', 'ch_05_part2_en.txt', 'ch_05_part3_en.txt']
    },
    '06': {
        'name': 'ch_06_seven_cures_for_a_lean_purse_en.txt',
        'parts': ['ch_06_part1_en.txt', 'ch_06_part2_en.txt', 'ch_06_part3_en.txt', 'ch_06_part4_en.txt']
    },
    '07': {
        'name': 'ch_07_meet_the_goddess_of_good_luck_en.txt',
        'parts': ['ch_07_part1_en.txt', 'ch_07_part2_en.txt', 'ch_07_part3_en.txt']
    }
}

for ch_num, ch_data in chapters.items():
    out_path = os.path.join(dir_path, ch_data['name'])
    with open(out_path, 'w', encoding='utf-8') as outfile:
        for i, part in enumerate(ch_data['parts']):
            part_path = os.path.join(dir_path, part)
            if os.path.exists(part_path):
                with open(part_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    if i < len(ch_data['parts']) - 1:
                        outfile.write('\n\n')
            else:
                print(f"Missing {part_path}")

# Clean up all temp files
for ch_num, ch_data in chapters.items():
    for part in ch_data['parts']:
        part_path = os.path.join(dir_path, part)
        if os.path.exists(part_path):
            os.remove(part_path)

for part in glob.glob(os.path.join(dir_path, 'raw_ch_*_part*.txt')):
    os.remove(part)

print("All chapters merged and temp files cleaned up successfully!")
