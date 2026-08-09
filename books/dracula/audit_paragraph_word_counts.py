import os
import re

def count_metrics(filepath):
    if not os.path.exists(filepath):
        return "-", "-", []

    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    if not text:
        return 0, 0, []

    # Paragraphs are separated by blank lines
    paras = [p.strip() for p in text.split('\n\n') if p.strip()]
    p_count = len(paras)

    # Strip out the paragraph IDs if they exist (e.g. [P001]) before counting words
    clean_text = re.sub(r'\[P\d+\]\s*', '', text)
    w_count = len(clean_text.split())

    return p_count, f"{w_count:,}", paras


def detect_misalignment(en_paras, ko_paras, chapter, threshold=4.0, min_en_words=20):
    """
    Flag paragraphs where the KO/EN word ratio exceeds `threshold`
    and the English paragraph has at least `min_en_words` words.
    Returns a list of (para_num, en_words, ko_words, ratio) tuples.
    """
    issues = []
    for i, (ep, kp) in enumerate(zip(en_paras, ko_paras)):
        en_clean = re.sub(r'\[P\d+\]\s*', '', ep)
        ko_clean = re.sub(r'\[P\d+\]\s*', '', kp)
        en_words = len(en_clean.split())
        ko_words = len(ko_clean.split())
        if en_words >= min_en_words and ko_words > 0:
            ratio = ko_words / en_words
            if ratio > threshold:
                issues.append((i + 1, en_words, ko_words, round(ratio, 1)))
    return issues


def generate_report():
    base_dir = 'books/dracula/chapters'

    markdown_lines = [
        "# Dracula Bilingual Alignment Audit",
        "",
        "## Audit 1: Paragraph & Word Count Summary",
        "",
        "Verifies total paragraph counts and word counts for the raw English, chunked English, and final Korean files.",
        "",
        "| Chapter | Raw EN (Para/Words) | Chunked EN (Para/Words) | Final KO (Para/Words) |",
        "|---|---|---|---|"
    ]

    total_raw_en_p = 0
    total_chunk_en_p = 0
    total_chunk_ko_p = 0

    chapter_data = {}

    for i in range(1, 28):
        ch = f"{i:02d}"

        raw_en  = os.path.join(base_dir, f"raw_ch_{ch}.txt")
        chunk_en = os.path.join(base_dir, f"ch{ch}_en.txt")
        chunk_ko = os.path.join(base_dir, f"ch{ch}_ko.txt")

        p_raw_en, w_raw_en, _         = count_metrics(raw_en)
        p_chk_en, w_chk_en, en_paras  = count_metrics(chunk_en)
        p_chk_ko, w_chk_ko, ko_paras  = count_metrics(chunk_ko)

        if isinstance(p_raw_en, int): total_raw_en_p  += p_raw_en
        if isinstance(p_chk_en, int): total_chunk_en_p += p_chk_en
        if isinstance(p_chk_ko, int): total_chunk_ko_p += p_chk_ko

        row = f"| {i} | {p_raw_en} / {w_raw_en} | {p_chk_en} / {w_chk_en} | {p_chk_ko} / {w_chk_ko} |"
        markdown_lines.append(row)

        chapter_data[i] = (en_paras, ko_paras)

    markdown_lines.append(
        f"| **TOTAL** | **{total_raw_en_p}** | **{total_chunk_en_p}** | **{total_chunk_ko_p}** |"
    )

    # ── Audit 2: Per-Paragraph Misalignment Detection ───────────────────────
    markdown_lines += [
        "",
        "---",
        "",
        "## Audit 2: Per-Paragraph Misalignment Detection",
        "",
        "Flags paragraphs where the Korean word count is **>4x the English word count** (for EN paragraphs ≥20 words).",
        "A high ratio strongly suggests that the Korean paragraph contains content from a different section.",
        "",
        "| Chapter | Para # | EN Words | KO Words | Ratio | Status |",
        "|---|---|---|---|---|---|"
    ]

    any_issues = False
    for i in range(1, 28):
        en_paras, ko_paras = chapter_data[i]
        if not en_paras or not ko_paras:
            continue
        issues = detect_misalignment(en_paras, ko_paras, i)
        for (para_num, en_w, ko_w, ratio) in issues:
            severity = "⚠️ WARNING" if ratio < 7.0 else "🔴 CRITICAL"
            markdown_lines.append(f"| {i} | {para_num} | {en_w} | {ko_w} | {ratio}x | {severity} |")
            any_issues = True

    if not any_issues:
        markdown_lines.append("| — | — | — | — | — | ✅ No issues found |")

    # Save
    artifact_path = r"C:\Users\hongw\.gemini\antigravity\brain\b85acb0a-6fb8-4473-bf15-263a48b385aa\audit_report.md"
    with open(artifact_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_lines))

    print(f"Report generated at: {artifact_path}")


if __name__ == '__main__':
    generate_report()
