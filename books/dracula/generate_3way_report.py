import os
import re

TARGET_DIR = r'c:\git_repo\TKprof_book\books\dracula\chapters'
BACKUP_DIR = r'c:\git_repo\TKprof_book\books\dracula\chapters_backup'

def get_words(text):
    return len(text.split())

def strip_tags(text):
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())

def generate_report():
    lines = ["# 3-Way Paragraph Word Count Report (Raw vs EN vs KO)\n",
             "| Chapter | Tag | Raw Words | EN Words | KO Words | Status |",
             "|---|---|---|---|---|---|"]
    
    # Paragraphs manually reviewed and accepted as OK (legitimate translation adaptations)
    # Format: (chapter_str, base_tag)
    ACCEPTED_FLAGS = {
        ('14', '059'),  # Letter closing: 'Yours the most faithful,' -> 'Sincerely,'
        ('14', '073'),  # Context added: 'And how?' -> 'How do you mean I cured you?'
    }
    
    total_ok = 0
    total_flag = 0
    
    for i in range(1, 28):
        ch = f"{i:02d}"
        raw_path = os.path.join(BACKUP_DIR, f'raw_ch_{ch}.txt')
        en_path = os.path.join(TARGET_DIR, f'ch{ch}_en.txt')
        ko_path = os.path.join(TARGET_DIR, f'ch{ch}_ko.txt')
        
        with open(raw_path, 'r', encoding='utf-8') as f:
            raw_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        with open(en_path, 'r', encoding='utf-8') as f:
            en_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        with open(ko_path, 'r', encoding='utf-8') as f:
            ko_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        
        # Raw word counts indexed by 1-based paragraph number
        raw_wc = {}
        for idx, rp in enumerate(raw_paras):
            raw_wc[idx + 1] = get_words(rp)
        
        # Collect unique base tags from EN file, preserving order
        # A base tag is: P012, P013, P012_014, etc. (strip trailing lowercase suffix)
        seen_bases = []
        seen_set = set()
        en_agg = {}
        ko_agg = {}
        raw_agg = {}
        
        for ep, kp in zip(en_paras, ko_paras):
            tag_m = re.match(r'^\[P([0-9a-zA-Z_]+)\]', ep)
            if not tag_m:
                continue
            full_tag = tag_m.group(1)  # e.g. "012a", "013", "012_014"
            
            # Strip trailing lowercase letter to get the base
            base = re.sub(r'[a-z]$', '', full_tag)  # "012a" -> "012", "012_014" -> "012_014"
            
            if base not in seen_set:
                seen_set.add(base)
                seen_bases.append(base)
                
                # Calculate raw word count for this base
                # Parse the base to figure out which raw paragraphs it covers
                if '_' in base:
                    # Merged range like "012_014" -> raw paras 12, 13, 14
                    parts = base.split('_')
                    start_p = int(parts[0])
                    end_p = int(parts[1])
                    raw_total = sum(raw_wc.get(p, 0) for p in range(start_p, end_p + 1))
                else:
                    # Single paragraph like "012"
                    raw_total = raw_wc.get(int(base), 0)
                raw_agg[base] = raw_total
            
            # Aggregate EN/KO word counts
            en_agg[base] = en_agg.get(base, 0) + get_words(strip_tags(ep))
            ko_agg[base] = ko_agg.get(base, 0) + get_words(strip_tags(kp))
        
        for base in seen_bases:
            rw = raw_agg.get(base, 0)
            ew = en_agg.get(base, 0)
            kw = ko_agg.get(base, 0)
            
            # Flag if any column is zero or ratio is extreme
            if rw == 0 or ew == 0 or kw == 0:
                status = 'MISS'
            elif ew / rw > 3.0 or rw / ew > 3.0:
                status = 'FLAG'
            else:
                status = 'OK'
            
            # Override with user-accepted flags
            if status == 'FLAG' and (ch, base) in ACCEPTED_FLAGS:
                status = 'OK (accepted)'
            
            if 'OK' in status:
                total_ok += 1
            else:
                total_flag += 1
            
            tag_display = f'[P{base}]'
            lines.append(f"| {ch} | {tag_display} | {rw} | {ew} | {kw} | {status} |")

    
    # Add summary at the top
    lines.insert(1, f"\n**Summary:** {total_ok} OK, {total_flag} flagged (MISS/FLAG)\n")
    
    out_path = r'c:\git_repo\TKprof_book\books\dracula\raw_en_ko_ratio_report.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
        
    print(f"Report generated: {out_path}")
    print(f"  OK: {total_ok}  |  Flagged: {total_flag}")

if __name__ == '__main__':
    generate_report()
