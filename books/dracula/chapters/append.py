import sys

def append_to_file(filename):
    text = sys.stdin.read()
    with open(filename, 'a', encoding='utf-8') as f:
        if f.tell() > 0:
            f.write('\n\n')
        f.write(text)

if __name__ == '__main__':
    append_to_file(sys.argv[1])
