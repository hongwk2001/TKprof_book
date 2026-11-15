import sys

def append_to_file(filepath, content):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write('\n\n' + content)

if __name__ == "__main__":
    import sys
    file = sys.argv[1]
    content_file = sys.argv[2]
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    append_to_file(file, content)
