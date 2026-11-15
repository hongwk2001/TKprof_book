import os
import re

def count_sentences(text):
    # Ignore periods in common abbreviations: Dr., Mr., Mrs., Ms., St., Prof., Rev., Sr., Jr., Vol., P.S., a.m., p.m.
    cleaned = re.sub(r'\b(Dr|Mr|Mrs|Ms|St|Prof|Rev|Sr|Jr|Vol|P\.S|a\.m|p\.m)\.', r'\1_', text, flags=re.IGNORECASE)
    matches = re.findall(r'[.!?](?:\s|"|”|”|\'|$)', cleaned)
    return max(1, len(matches)) if text.strip() else 0

def clean_paragraph(p):
    # Remove tags like [P001] or [P004a]
    return re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p.strip())

def main():
    base_dir = 'chapters'
    if not os.path.exists(base_dir):
        print(f"Error: Directory {base_dir} not found. Run from books/dracula")
        return

    # Verified notes map: (ch, para_id) -> note
    verified_notes = {
        ('05', 'P028'): 'OK (manually verified)',
        ('06', 'P047a'): 'OK (manually verified)',
        ('08', 'P047'): 'OK (checked by agent - missing text supplied)',
        ('08', 'P051a'): 'OK (checked by agent - missing text supplied)',
        ('08', 'P051b'): 'OK (checked by agent - missing text supplied)',
        ('08', 'P055a'): 'OK (checked by agent - missing text supplied)',
        ('08', 'P055b'): 'OK (checked by agent - missing text supplied)',
        ('08', 'P055c'): 'OK (checked by agent - missing text supplied)',
        ('19', 'P003b'): 'OK (manually verified - high literary quality)',
        ('19', 'P004'): 'OK (manually verified - high literary quality)',
        ('22', 'P052a'): 'OK (checked by agent - tag realigned)',
        ('22', 'P052b'): 'OK (checked by agent - tag realigned)',
        ('22', 'P056a'): 'OK (checked by agent - tag realigned)',
        ('22', 'P056b'): 'OK (checked by agent - tag realigned)',
    }

    report_lines = [
        "# Sentence-Level Paragraph Alignment Audit",
        "",
        "This report flags paragraphs where the absolute difference in sentence counts between English and Korean is **> 2** AND the ratio is **outside [0.5, 2.0]**.",
        "",
        "| Chapter | Para | EN Sents | KO Sents | Difference | Ratio | Status / Notes |",
        "|---|---|---|---|---|---|---|"
    ]

    total_suspicious = 0

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
        
        for j, (ep, kp) in enumerate(zip(en_paras, ko_paras)):
            m = re.match(r'^\[(P[a-zA-Z0-9_]+)\]', ep)
            para_id = m.group(1) if m else f"Idx {j}"
            
            en_clean = clean_paragraph(ep)
            ko_clean = clean_paragraph(kp)

            if not en_clean and not ko_clean:
                continue

            en_sents = count_sentences(en_clean)
            ko_sents = count_sentences(ko_clean)

            if en_sents == 0 or ko_sents == 0:
                continue

            diff = abs(en_sents - ko_sents)
            ratio = ko_sents / en_sents
            
            if diff > 2 and (ratio < 0.5 or ratio > 2.0):
                note = verified_notes.get((ch, para_id), "Pending Review")
                report_lines.append(f"| {ch} | {para_id} | {en_sents} | {ko_sents} | {diff} | {ratio:.2f}x | {note} |")
                total_suspicious += 1

    if total_suspicious == 0:
        report_lines.append("| - | - | - | - | - | - | - |")
        report_lines.append("\n**Result:** No suspicious paragraphs found.")
    else:
        report_lines.append(f"\n**Total Suspicious Paragraphs:** {total_suspicious}")

    with open('audit_sentences_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print(f"Report generated: audit_sentences_report.md with {total_suspicious} suspicious paragraphs flagged.")

if __name__ == '__main__':
    main()
