import sys

def append_to_file(filename, content):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(content + '\n\n')

if __name__ == '__main__':
    filename = sys.argv[1]
    content = sys.stdin.read().strip()
    append_to_file(filename, content)
