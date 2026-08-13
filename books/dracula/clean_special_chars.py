import os

def clean_file(fpath):
    with open(fpath, 'rb') as f:
        content = f.read()

    # Check for UTF-8 BOM bytes
    has_bom = content.startswith(b'\xef\xbb\xbf')
    if has_bom:
        content = content[3:]

    # Decode UTF-8 safely
    text = content.decode('utf-8', errors='replace')

    # Count occurrences of bad characters
    bom_count = text.count('\ufeff')
    repl_count = text.count('\ufffd')
    zwsp_count = text.count('\u200b') + text.count('\u200c') + text.count('\u200d')

    if not has_bom and bom_count == 0 and repl_count == 0 and zwsp_count == 0:
        return None

    # Strip bad characters
    text = text.replace('\ufeff', '')
    text = text.replace('\ufffd', '')
    text = text.replace('\u200b', '')
    text = text.replace('\u200c', '')
    text = text.replace('\u200d', '')

    # Save as pure UTF-8 without BOM
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(text)

    stats = []
    if has_bom or bom_count > 0:
        stats.append(f"Removed {bom_count + (1 if has_bom else 0)} BOM (\\ufeff)")
    if repl_count > 0:
        stats.append(f"Removed {repl_count} replacement char (\\ufffd)")
    if zwsp_count > 0:
        stats.append(f"Removed {zwsp_count} zero-width space")

    return ', '.join(stats)

def main():
    root_dir = '.'
    cleaned_count = 0

    print("=== SPECIAL CHARACTER CLEANUP ===")
    for dirpath, _, filenames in os.walk(root_dir):
        # Ignore git or venv directories
        if '.git' in dirpath or 'venv' in dirpath or '__pycache__' in dirpath:
            continue
        for filename in filenames:
            if filename.endswith(('.txt', '.md', '.json', '.py', '.html', '.css', '.js')):
                fpath = os.path.join(dirpath, filename)
                res = clean_file(fpath)
                if res:
                    print(f"Cleaned [{fpath}]: {res}")
                    cleaned_count += 1

    print(f"\nDone! Cleaned {cleaned_count} files.")

if __name__ == '__main__':
    main()
