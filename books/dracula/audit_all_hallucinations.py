import glob
import os
import re

def audit_file_for_hallucinations(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    paras = [p.strip() for p in text.split('\n\n') if p.strip()]
    issues = []

    for idx, p in enumerate(paras):
        # 1. Check for embedded paragraph number prefixes right after tag, e.g. [P016] 16. or [P017a] 17.
        m_num = re.match(r'^\[(P[a-zA-Z0-9_]+)\]\s*(\d+[\.\)\:]?)\s+', p)
        if m_num:
            issues.append((idx, f"Embedded number prefix '{m_num.group(2)}' after [{m_num.group(1)}]"))

        # 2. Check for duplicate tag, e.g. [P016] [P016]
        m_dup = re.match(r'^\[(P[a-zA-Z0-9_]+)\]\s*\[\1\]', p)
        if m_dup:
            issues.append((idx, f"Duplicate tag [{m_dup.group(1)}]"))

        # 3. Check for leftover markdown header symbols at start of paragraph
        m_head = re.match(r'^\[(P[a-zA-Z0-9_]+)\]\s*(#{1,6}\s+)', p)
        if m_head:
            issues.append((idx, f"Leftover markdown header '{m_head.group(2).strip()}' after [{m_head.group(1)}]"))

    return issues

def fix_file_hallucinations(fpath, issues):
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    paras = [p.strip() for p in text.split('\n\n') if p.strip()]
    cleaned_paras = []

    for p in paras:
        # Strip embedded number prefixes: [P016] 16. -> [P016]
        p = re.sub(r'^(\[P[a-zA-Z0-9_]+\])\s*\d+[\.\)\:]?\s*', r'\1 ', p)
        # Strip duplicate tags: [P016] [P016] -> [P016]
        p = re.sub(r'^(\[P[a-zA-Z0-9_]+\])\s*\[P[a-zA-Z0-9_]+\]\s*', r'\1 ', p)
        # Strip markdown header hashes after tag: [P016] ### -> [P016]
        p = re.sub(r'^(\[P[a-zA-Z0-9_]+\])\s*#{1,6}\s*', r'\1 ', p)
        cleaned_paras.append(p)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(cleaned_paras) + '\n')

def main():
    chapters = sorted(glob.glob('chapters/ch*.txt'))
    total_issues = 0
    file_issue_map = {}

    print("=== AUDITING ALL 54 CHAPTER FILES FOR HALLUCINATIONS ===")
    for fpath in chapters:
        issues = audit_file_for_hallucinations(fpath)
        if issues:
            file_issue_map[fpath] = issues
            total_issues += len(issues)

    if total_issues == 0:
        print("\nALL 54 CHAPTER FILES ARE 100% CLEAN! Zero number/header/tag hallucinations found.")
    else:
        print(f"\nFound {total_issues} hallucination issues across {len(file_issue_map)} files:")
        for fpath, issues in file_issue_map.items():
            print(f"\n[{fpath}]: {len(issues)} issue(s)")
            for idx, msg in issues:
                print(f"  - Para idx {idx}: {msg}")
            
            # Auto-fix them
            fix_file_hallucinations(fpath, issues)
            print(f"  -> AUTO-FIXED {fpath}")

        # Re-verify after fixing
        remaining = 0
        for fpath in file_issue_map.keys():
            re_issues = audit_file_for_hallucinations(fpath)
            remaining += len(re_issues)
        if remaining == 0:
            print("\nVerification successful! All detected hallucinations have been AUTO-FIXED.")

if __name__ == '__main__':
    main()
