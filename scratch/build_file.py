import sys

def append_chunk(filename, expected_lines, content):
    lines = content.split('\n')
    # If the last line is empty and it's not expected, maybe strip it, but let's just count
    if len(lines) > 0 and lines[-1] == '':
        lines = lines[:-1]
    
    if len(lines) != expected_lines:
        print(f"Warning: Expected {expected_lines} lines, but got {len(lines)} lines.")
    
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(content)
        if not content.endswith('\n'):
            f.write('\n')

if __name__ == '__main__':
    chunk_file = sys.argv[1]
    target_file = sys.argv[2]
    expected_lines = int(sys.argv[3])
    
    with open(chunk_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    append_chunk(target_file, expected_lines, content)
    print(f"Appended {expected_lines} lines to {target_file}")
