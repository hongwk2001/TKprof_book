ko_file = r'C:\git_repo\TKprof_book\books\dracula\chapters\ch06_ko.txt'
with open(ko_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('p_lines.txt', 'w', encoding='utf-8') as f:
    for i, line in enumerate(lines):
        if line.strip() and '[P' in line:
            f.write(f'{i:03d}: {line[:60].strip()}\n')
