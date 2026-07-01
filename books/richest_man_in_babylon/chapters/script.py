import sys
import re

arkad_lines = {20, 26, 30, 34, 44, 50, 52, 54, 56, 61, 63, 67, 69, 73, 75, 79, 81, 122, 138}
rest_lines = {3, 22, 24, 28, 36, 38, 40, 42, 46, 48, 59, 65, 77, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 120, 124, 126, 128, 130, 132, 134, 136, 140, 142, 144, 146, 148, 150}

def tag_line(line, tag):
    count = line.count('"')
    if count == 0:
        return line
    elif count % 2 == 0:
        # balanced quotes
        parts = line.split('"')
        res = ""
        for j in range(len(parts)):
            if j % 2 == 0:
                res += parts[j]
            else:
                res += f"<{tag}>{parts[j]}</{tag}>"
        return res
    elif count == 1:
        # one quote, replace with opening and add closing at end
        parts = line.split('"')
        return parts[0] + f"<{tag}>" + parts[1].rstrip('\r\n') + f"</{tag}>" + line[len(line.rstrip('\r\n')):]
    else:
        print(f"Warning: weird quote count {count} in line: {line}")
        return line

with open("d:/git_repo/TKprof_book/books/richest_man_in_babylon/chapters/ch_07_meet_the_goddess_of_good_luck_part1.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

out_lines = []
for i, line in enumerate(lines):
    line_num = i + 1
    if line_num in arkad_lines:
        out_lines.append(tag_line(line, "arkad"))
    elif line_num in rest_lines:
        out_lines.append(tag_line(line, "rest"))
    else:
        out_lines.append(line)

with open("d:/git_repo/TKprof_book/books/richest_man_in_babylon/chapters/tagged_ch_07_part1.txt", "w", encoding="utf-8") as f:
    f.writelines(out_lines)
print("Done")
