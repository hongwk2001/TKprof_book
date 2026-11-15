import glob
import os
import re

def clean_tag(text):
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())

def word_count(text):
    return len(re.findall(r'\b\w+\b', text))

def main():
    base_path = 'books/dracula/chapters/ch*_en.txt'
    long_paras = []
    
    for filepath in sorted(glob.glob(base_path)):
        filename = os.path.basename(filepath)
        ch_num = re.search(r'\d+', filename).group()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
            
        for p in paras:
            tag_match = re.match(r'^\[(P[0-9a-zA-Z_]+)\]', p)
            if tag_match:
                tag = tag_match.group(1)
                text = clean_tag(p)
                w_cnt = word_count(text)
                c_cnt = len(text)
                
                if c_cnt > 1800:
                    long_paras.append({
                        'ch': int(ch_num),
                        'tag': tag,
                        'chars': c_cnt,
                        'words': w_cnt,
                        'text': text
                    })
                    
    # Generate Markdown report
    md_lines = [
        "# Dracula Long Paragraphs Audit Report",
        "",
        "This report identifies all paragraphs across the 27 modernized English chapters of **Dracula** that exceed **1,800 characters** in length. These are candidates for splitting to improve Text-to-Speech (TTS) pacing and general readability.",
        "",
        "## Summary statistics",
        f"- **Total Long Paragraphs (>1,800 chars):** {len(long_paras)}",
        f"- **Extremely Long Paragraphs (>3,000 chars):** {len([p for p in long_paras if p['chars'] > 3000])}",
        f"- **Very Long Paragraphs (2,000 - 3,000 chars):** {len([p for p in long_paras if 2000 <= p['chars'] <= 3000])}",
        "",
        "---",
        "",
        "## Top Priority Candidates (>3,000 characters)",
        "",
        "These paragraphs are extremely long (equivalent to 500+ words) and are the most critical candidates for splitting.",
        "",
        "| Chapter | Tag | Characters | Words | Snippet |",
        "|---|---|---|---|---|",
    ]
    
    # Filter and sort top priority
    top_priority = sorted([p for p in long_paras if p['chars'] > 3000], key=lambda x: x['chars'], reverse=True)
    for p in top_priority:
        snippet = p['text'][:100].replace('\n', ' ')
        md_lines.append(f"| {p['ch']:02d} | `[{p['tag']}]` | {p['chars']:,} | {p['words']} | {snippet}... |")
        
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("## Detailed Paragraph Audit (By Chapter)")
    md_lines.append("")
    
    # Group by Chapter
    for ch in range(1, 28):
        ch_paras = [p for p in long_paras if p['ch'] == ch]
        if not ch_paras:
            continue
            
        md_lines.append(f"### Chapter {ch:02d}")
        md_lines.append("")
        md_lines.append("| Tag | Characters | Words | Snippet |")
        md_lines.append("|---|---|---|---|")
        for p in ch_paras:
            snippet = p['text'][:80].replace('\n', ' ')
            md_lines.append(f"| `[{p['tag']}]` | {p['chars']:,} | {p['words']} | {snippet}... |")
        md_lines.append("")
        
    artifact_path = r"C:\Users\hongw\.gemini\antigravity\brain\3ddf8683-f4e2-437b-8ee1-79e2d403a4a0\long_paragraphs_report.md"
    with open(artifact_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
        
    print(f"Report written to {artifact_path}")

if __name__ == '__main__':
    main()
