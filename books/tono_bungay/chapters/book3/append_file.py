import sys

def append_file(target, source):
    with open(source, 'r', encoding='utf-8') as sf:
        content = sf.read()
    with open(target, 'a', encoding='utf-8') as tf:
        tf.write(content + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python append_file.py <target> <source>")
        sys.exit(1)
    append_file(sys.argv[1], sys.argv[2])
