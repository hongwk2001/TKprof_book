import os
import glob

dir_path = 'd:/git_repo/TKprof_book/books/richest_man_in_babylon/chapters'

chapters = {
    '08': {
        'name': 'ch_08_the_five_laws_of_gold_en.txt',
        'parts': ['ch_08_part1_en.txt', 'ch_08_part2_en.txt', 'ch_08_part3_en.txt']
    },
    '09': {
        'name': 'ch_09_the_gold_lender_of_babylon_en.txt',
        'parts': ['ch_09_part1_en.txt', 'ch_09_part2_en.txt', 'ch_09_part3_en.txt']
    },
    '10': {
        'name': 'ch_10_the_walls_of_babylon_en.txt',
        'parts': ['ch_10_part1_en.txt']
    },
    '11': {
        'name': 'ch_11_the_luckiest_man_in_babylon_en.txt',
        'parts': [f'ch_11_part{i}_en.txt' for i in range(1, 9)]
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
