import re

def split_paragraph(file_path, target_tag, split_str_en, split_str_ko=None, is_ko=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the paragraph starting with target_tag
    pattern = r'(\[' + target_tag + r'\])(.*?)(?=\n\s*\[|$)'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"Could not find {target_tag} in {file_path}")
        return
    
    para_text = match.group(2)
    split_str = split_str_ko if is_ko else split_str_en
    
    # We want to replace target_tag with a, and insert \n\n[tag b] at the split_str
    # The split string might have newlines in the actual text, so we'll remove newlines for matching or use a regex
    # Wait, simple string replace in python:
    # Let's normalize spaces for searching
    
    para_norm = re.sub(r'\s+', ' ', para_text)
    split_norm = re.sub(r'\s+', ' ', split_str)
    
    if split_norm not in para_norm:
        print(f"Could not find split string in {target_tag} of {file_path}")
        return
        
    # We need to find the actual index in the original para_text
    # Construct a regex from split_norm by replacing spaces with \s+
    split_regex = re.escape(split_norm).replace(r'\ ', r'\s+')
    
    def repl(m):
        return '\n\n[' + target_tag + 'b] ' + m.group(0).lstrip()

    new_para_text = re.sub(split_regex, repl, para_text, count=1)
    
    new_para = f"[{target_tag}a]{new_para_text}"
    
    # Replace in content
    new_content = content[:match.start()] + new_para + content[match.end():]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully split {target_tag} in {file_path}")

en_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch26_en.txt'
ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch26_ko.txt'

split_paragraph(en_file, 'P031', 'Two mornings ago,', is_ko=False)
split_paragraph(ko_file, 'P031', 'Two mornings ago,', split_str_ko='이틀 전 아침,', is_ko=True)

split_paragraph(en_file, 'P082_083', 'Professor Van Helsing and I', is_ko=False)
split_paragraph(ko_file, 'P082_083', 'Professor Van Helsing and I', split_str_ko='반 헬싱 교수님과 저는 오늘 밤', is_ko=True)

split_paragraph(en_file, 'P086_087', 'Mr. Morris and Dr. Seward set off', is_ko=False)
split_paragraph(ko_file, 'P086_087', 'Mr. Morris and Dr. Seward set off', split_str_ko='모리스 씨와 수어드 박사는 우리가 배를 띄우기 전에', is_ko=True)

