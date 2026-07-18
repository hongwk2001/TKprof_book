import os
import re

BASE_DIR = r"d:\git_repo\TKprof_book\books\secret_garden"
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
OUTPUT_FILE = os.path.join(BASE_DIR, "korean_audit_report.md")

def parse_report(filepath):
    """
    Parses a single chapter report file and extracts suggestions.
    Extracts matches for English, Current, Proposed, and Reasoning/Reason.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # We will look for blocks. Typically a block contains English, Current, Proposed, and Reason.
    # Let's split by occurrences of "Paragraph" or "paragraph" or "###" or "##"
    # To split them, let's identify paragraph sections.
    # We can split the text on headers that mention Paragraph or numbers
    items = []
    
    # We can split by headers like "## Paragraph", "### Paragraph", "**Paragraph", "#### Paragraph", etc.
    # Or simply find matches of English/Current/Proposed/Reasoning groupings.
    
    # Let's split by double newlines and then group them.
    # An alternative is a state machine scanning lines:
    lines = content.split("\n")
    
    current_item = {}
    current_field = None
    field_buffer = []
    
    overview_lines = []
    in_overview = True
    
    # Simple regexes to detect fields
    re_eng = re.compile(r'(english|영문|original|source)', re.IGNORECASE)
    re_curr = re.compile(r'(current|기존|현행)', re.IGNORECASE)
    re_prop = re.compile(r'(proposed|수정|제안|변경)', re.IGNORECASE)
    re_reason = re.compile(r'(reason|이유|원인|근거)', re.IGNORECASE)
    
    # Detect section titles
    re_p_header = re.compile(r'^\s*(#+|-|\*+)\s*(paragraph|문단|chapter|\[|\d+\.)', re.IGNORECASE)
    
    for line in lines:
        cleaned = line.strip()
        
        # Check if we transition out of overview
        if in_overview:
            if re_p_header.search(line) or "english" in line.lower() or "current" in line.lower():
                in_overview = False
            else:
                overview_lines.append(line)
                continue
                
        # If we see a new paragraph header, let's save the previous item
        if re_p_header.search(line) and not in_overview:
            if current_item.get('english') or current_item.get('proposed'):
                # Flush the last field buffer
                if current_field and field_buffer:
                    current_item[current_field] = " ".join(field_buffer).strip()
                items.append(current_item)
            current_item = {'title': cleaned.replace("#", "").replace("-", "").replace("*", "").strip()}
            current_field = None
            field_buffer = []
            continue
            
        # Detect field starts
        if (line.startswith("-") or line.startswith("*") or line.startswith("##") or "**" in line) and ":" in line:
            parts = line.split(":", 1)
            label = parts[0].replace("-", "").replace("*", "").strip().lower()
            val = parts[1].strip()
            
            # Flush previous field
            if current_field and field_buffer:
                current_item[current_field] = " ".join(field_buffer).strip()
                field_buffer = []
                
            if re_eng.search(label):
                current_field = 'english'
                if val: field_buffer.append(val)
            elif re_curr.search(label):
                current_field = 'current'
                if val: field_buffer.append(val)
            elif re_prop.search(label):
                current_field = 'proposed'
                if val: field_buffer.append(val)
            elif re_reason.search(label):
                current_field = 'reason'
                if val: field_buffer.append(val)
            else:
                # Unknown field or just a plain bullet point, append to current field if active
                if current_field:
                    field_buffer.append(line)
        else:
            if current_field:
                field_buffer.append(line)
                
    # Flush last item
    if current_field and field_buffer:
        current_item[current_field] = " ".join(field_buffer).strip()
    if current_item.get('english') or current_item.get('proposed'):
        items.append(current_item)
        
    overview = "\n".join(overview_lines).strip()
    return overview, items

def clean_value(val):
    # Strip backticks, quotes, bolding
    val = re.sub(r'^[`"\'*]+', '', val)
    val = re.sub(r'[`"\'*]+$', '', val)
    return val.strip()

def main():
    print("Compiling audit reports with flexible parser...")
    
    all_chapters_data = []
    
    for i in range(1, 28):
        report_path = os.path.join(CHAPTERS_DIR, f"audit_ch_{i:02d}.md")
        if not os.path.exists(report_path):
            print(f"Warning: report for Chapter {i} not found.")
            continue
            
        overview, suggestions = parse_report(report_path)
        
        # Clean suggestions values
        for sug in suggestions:
            sug['english'] = clean_value(sug.get('english', ''))
            sug['current'] = clean_value(sug.get('current', ''))
            sug['proposed'] = clean_value(sug.get('proposed', ''))
            sug['reason'] = clean_value(sug.get('reason', ''))
            if not sug.get('title'):
                sug['title'] = "Suggested Update"
                
        all_chapters_data.append({
            'chapter': i,
            'overview': overview,
            'suggestions': suggestions
        })
        
    # Write the compiled master report
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# Master Audit Report: The Secret Garden Korean Translation\n\n")
        
        out.write("## Executive Summary\n\n")
        out.write("This report aggregates the findings of a comprehensive paragraph-by-paragraph translation audit conducted across all 27 chapters of *The Secret Garden* using Gemini Pro. The audit focused on **dialect consistency (Yorkshire dialect)**, **honorifics & kinship terms**, **prose flow (translationese)**, and **TTS compatibility**.\n\n")
        
        out.write("| Chapter | Overview Summary | Suggestions Found | Status |\n")
        out.write("| :--- | :--- | :---: | :--- |\n")
        
        total_suggestions = 0
        for ch in all_chapters_data:
            lines = ch['overview'].split("\n")
            summary_line = ""
            for line in lines:
                if line.startswith("#"):
                    continue
                if line.strip():
                    summary_line = line.strip()
                    break
            if len(summary_line) > 80:
                summary_line = summary_line[:77] + "..."
            if not summary_line:
                summary_line = "Translation audit complete."
            
            status = "Needs Updates" if ch['suggestions'] else "Clean"
            out.write(f"| Chapter {ch['chapter']} | {summary_line} | {len(ch['suggestions'])} | {status} |\n")
            total_suggestions += len(ch['suggestions'])
            
        out.write(f"\n**Total suggested updates across the entire book: {total_suggestions}**\n\n")
        out.write("---\n\n")
        
        out.write("## Chapter-by-Chapter Detailed Findings\n\n")
        
        for ch in all_chapters_data:
            out.write(f"### Chapter {ch['chapter']}\n\n")
            if not ch['suggestions']:
                out.write("No translation or formatting issues were found in this chapter. The translation is clean and accurate.\n\n")
                continue
                
            out.write(f"Found **{len(ch['suggestions'])}** suggested updates:\n\n")
            
            for sug in ch['suggestions']:
                out.write(f"#### {sug['title']}\n")
                if sug['english']:
                    out.write(f"- **English**: {sug['english']}\n")
                if sug['current']:
                    out.write(f"- **Current Korean**: `{sug['current']}`\n")
                if sug['proposed']:
                    out.write(f"- **Proposed Korean**: `**{sug['proposed']}**`\n")
                if sug['reason']:
                    out.write(f"- **Reasoning**: {sug['reason']}\n")
                out.write("\n")
            out.write("---\n\n")
            
    print(f"Master audit report compiled at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
