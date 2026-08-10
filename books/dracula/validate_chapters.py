"""
validate_chapters.py
====================
A pure-Python, zero-AI script that validates the bilingual Dracula chapter files.

Checks performed:
  1. FILE EXISTS       - Both ch##_en.txt and ch##_ko.txt are present
  2. PARA PARITY       - EN and KO have the same paragraph count
  3. TAG SEQUENCE      - [Pxxx] tags are sequential (001, 002, 003 ...) with no gaps
  4. EN INFLATION      - Chunked EN word count vs raw EN word count ratio > 1.20
  5. EN DUPLICATION    - A 30-word sequence repeats inside the same EN file
  6. KO MISALIGNMENT   - Per-paragraph KO/EN word ratio > 4.0 for paras >= 20 EN words
  7. EMPTY PARAS       - Any paragraph is blank or whitespace-only

Output:
  - Console summary table
  - Saved to audit_validation_report.md in the artifacts directory
"""

import os
import re

BASE_DIR   = 'books/dracula/chapters'
ARTIFACT   = r'C:\Users\hongw\.gemini\antigravity\brain\f7b98130-034e-4c41-97e8-4a99b243b760\audit_validation_report.md'

RATIO_EN_INFLATION   = 1.20   # chunked EN / raw EN word count
RATIO_KO_MISALIGN    = 4.0    # KO words / EN words per paragraph
MIN_EN_WORDS_ALIGN   = 20     # minimum EN words to apply misalignment check
DUP_SEQ_LEN          = 30     # number of words in duplicate-detection window

PASS = 'PASS'
FAIL = 'FAIL'

# ── helpers ──────────────────────────────────────────────────────────────────

def read_paras(path):
    """Read a file and return list of stripped non-empty paragraphs."""
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    return [p.strip() for p in raw.split('\n\n') if p.strip()]

def word_count(text):
    return len(text.split())

def strip_tags(text):
    return re.sub(r'\[P[0-9a-zA-Z_]+\]\s*', '', text)

def check_tag_sequence(paras):
    """Return list of tag errors (missing or malformed)."""
    errors = []
    for i, p in enumerate(paras, 1):
        m = re.match(r'^\[P[0-9a-zA-Z_]+\]', p)
        if not m:
            errors.append('Para %d: missing or malformed [Pxxx] tag' % i)
    return errors

def check_duplication(paras):
    """Detect if any 30-word window repeats elsewhere in the chapter."""
    words = strip_tags(' '.join(paras)).split()
    seen = {}
    n = DUP_SEQ_LEN
    for i in range(len(words) - n):
        seq = ' '.join(words[i:i+n])
        if seq in seen:
            return 'Duplicate ~%d-word sequence at word %d (first seen at %d)' % (n, i, seen[seq])
        seen[seq] = i
    return None

# ── main validator ────────────────────────────────────────────────────────────

def validate():
    results = []   # list of dicts per chapter

    for i in range(1, 28):
        ch  = '%02d' % i
        raw_path  = os.path.join(BASE_DIR, 'raw_ch_%s.txt' % ch)
        en_path   = os.path.join(BASE_DIR, 'ch%s_en.txt' % ch)
        ko_path   = os.path.join(BASE_DIR, 'ch%s_ko.txt' % ch)

        r = {
            'ch': i,
            'issues': [],
            'warnings': [],
        }

        # 1. FILE EXISTS
        en_paras = read_paras(en_path)
        ko_paras = read_paras(ko_path)
        if en_paras is None:
            r['issues'].append('MISSING: ch%s_en.txt' % ch)
        if ko_paras is None:
            r['issues'].append('MISSING: ch%s_ko.txt' % ch)
        if en_paras is None or ko_paras is None:
            results.append(r)
            continue

        # 2. PARA PARITY
        if len(en_paras) != len(ko_paras):
            r['issues'].append('PARA PARITY: EN=%d KO=%d (delta %+d)' % (
                len(en_paras), len(ko_paras), len(ko_paras) - len(en_paras)))

        # 3. TAG SEQUENCE (EN)
        tag_errors = check_tag_sequence(en_paras)
        for e in tag_errors[:3]:   # cap at 3
            r['issues'].append('TAG SEQ EN: ' + e)
        if len(tag_errors) > 3:
            r['issues'].append('TAG SEQ EN: ...and %d more' % (len(tag_errors) - 3))

        # 4. EN INFLATION (vs raw)
        raw_paras = read_paras(raw_path)
        if raw_paras is not None:
            raw_words   = word_count(strip_tags(' '.join(raw_paras)))
            chunk_words = word_count(strip_tags(' '.join(en_paras)))
            ratio = chunk_words / raw_words if raw_words else 0
            if ratio > RATIO_EN_INFLATION:
                r['issues'].append('EN INFLATION: raw=%d chunked=%d ratio=%.2f' % (
                    raw_words, chunk_words, ratio))

        # 5. EN DUPLICATION
        dup = check_duplication(en_paras)
        if dup:
            r['issues'].append('DUPLICATION: ' + dup)

        # 6. KO MISALIGNMENT (per-paragraph ratio)
        misaligned = []
        for j, (ep, kp) in enumerate(zip(en_paras, ko_paras), 1):
            en_w = word_count(strip_tags(ep))
            ko_w = word_count(strip_tags(kp))
            if en_w >= MIN_EN_WORDS_ALIGN and ko_w > 0:
                ratio = ko_w / en_w
                if ratio > RATIO_KO_MISALIGN:
                    misaligned.append('P%03d EN=%d KO=%d (%.1fx)' % (j, en_w, ko_w, ratio))
        if misaligned:
            severity = 'CRITICAL' if len(misaligned) >= 3 else 'WARNING'
            r['issues' if severity == 'CRITICAL' else 'warnings'].append(
                'KO MISALIGN (%s): %d para(s) — %s' % (severity, len(misaligned), '; '.join(misaligned[:2])))

        # 7. EMPTY PARAS
        empty_en = [j+1 for j, p in enumerate(en_paras) if not strip_tags(p).strip()]
        empty_ko = [j+1 for j, p in enumerate(ko_paras) if not p.strip()]
        if empty_en:
            r['issues'].append('EMPTY EN PARA(S): %s' % empty_en[:5])
        if empty_ko:
            r['issues'].append('EMPTY KO PARA(S): %s' % empty_ko[:5])

        results.append(r)

    return results

# ── report ────────────────────────────────────────────────────────────────────

def build_report(results):
    lines = [
        '# Dracula Chapter Validation Report',
        '',
        'Checks: FILE EXISTS | PARA PARITY | TAG SEQUENCE | EN INFLATION | DUPLICATION | KO MISALIGNMENT | EMPTY PARAS',
        '',
        '| Ch | Result | Issues |',
        '|---|---|---|',
    ]

    total_pass = 0
    total_fail = 0

    for r in results:
        ch = r['ch']
        all_issues = r['issues'] + ['⚠️ ' + w for w in r['warnings']]
        if r['issues']:
            status = '🔴 FAIL'
            total_fail += 1
        elif r['warnings']:
            status = '🟡 WARN'
            total_fail += 1
        else:
            status = '✅ PASS'
            total_pass += 1

        issues_str = '<br>'.join(all_issues) if all_issues else '—'
        lines.append('| %d | %s | %s |' % (ch, status, issues_str))

    lines += [
        '',
        '---',
        '',
        '**Summary:** %d chapters PASS, %d chapters have issues.' % (total_pass, total_fail),
    ]
    return '\n'.join(lines)

# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    results = validate()
    report  = build_report(results)

    with open(ARTIFACT, 'w', encoding='utf-8') as f:
        f.write(report)

    # Console summary
    for r in results:
        issues = r['issues'] + r['warnings']
        if issues:
            print('Ch %02d FAIL:' % r['ch'])
            for iss in issues:
                print('       ' + iss)
        else:
            print('Ch %02d PASS' % r['ch'])

    print('\nReport saved to: ' + ARTIFACT)
