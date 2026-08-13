import os
import re

def main():
    base_dir = 'chapters'
    if not os.path.exists(base_dir):
        print(f"Error: Directory {base_dir} not found. Run from books/dracula")
        return

    print("=== PARAGRAPH TAG INTEGRITY & SEQUENTIAL AUDIT ===")
    
    for i in range(1, 28):
        ch = f"{i:02d}"
        en_path = os.path.join(base_dir, f"ch{ch}_en.txt")
        ko_path = os.path.join(base_dir, f"ch{ch}_ko.txt")

        if not os.path.exists(en_path) or not os.path.exists(ko_path):
            continue

        with open(en_path, 'r', encoding='utf-8') as f:
            en_text = f.read().strip()
        with open(ko_path, 'r', encoding='utf-8') as f:
            ko_text = f.read().strip()

        en_paras = [p.strip() for p in en_text.split('\n\n') if p.strip()]
        ko_paras = [p.strip() for p in ko_text.split('\n\n') if p.strip()]

        en_tags = [re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p).group(1) for p in en_paras if re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)]
        ko_tags = [re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p).group(1) for p in ko_paras if re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)]

        # Check tag list length mismatch
        diff_tags = []
        min_len = min(len(en_tags), len(ko_tags))
        for idx in range(min_len):
            if en_tags[idx] != ko_tags[idx]:
                diff_tags.append((idx, en_tags[idx], ko_tags[idx]))

        print(f"\nChapter {ch}: EN tags = {len(en_tags)}, KO tags = {len(ko_tags)}")
        if len(en_tags) != len(ko_tags):
            print(f"  -> WARNING: Tag count mismatch! EN={len(en_tags)} vs KO={len(ko_tags)}")
        if diff_tags:
            print(f"  -> WARNING: First {min(5, len(diff_tags))} tag sequence mismatches:")
            for idx, et, kt in diff_tags[:5]:
                print(f"     Index {idx:03d}: EN [{et}] vs KO [{kt}]")
        if not diff_tags and len(en_tags) == len(ko_tags):
            print(f"  -> OK: Perfect 1:1 tag match ({len(en_tags)} tags).")

if __name__ == '__main__':
    main()
