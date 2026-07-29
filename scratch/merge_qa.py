import os

base_dir = r"d:\git_repo\TKprof_book\books\seneca_emotional_resilience"
output_file = os.path.join(base_dir, "qa_report.md")

reports = [
    ("qa_report_anger1.md", "Book 1: On Anger (Chapters 1-21)"),
    ("qa_report_anger2.md", "Book 1: On Anger (Chapters 22-36)"), # Note: Actually Book 2 of On Anger
    ("qa_report_anger3.md", "Book 1: On Anger (Chapters 37-43)"), # Note: Actually Book 3 of On Anger
    ("qa_report_others.md", "Other Treatises (Tranquillity, Constancy, Providence)")
]

master_content = """# QA Readability Report: Stoic Treatises on Emotional Resilience

This report compiles all findings from a Quality Assurance (QA) pass on the modernized English chapters of Seneca's essays. The audit was conducted from the perspective of an ESL (English as a Second Language) learner and a middle school student. 

The goal is to ensure maximum clarity, smooth reading flow for Text-to-Speech (TTS), and the elimination of archaic expressions or overly convoluted grammar.

---

"""

for filename, section_title in reports:
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Find where content starts (skip first few header lines)
        content_lines = []
        skip_header = True
        for line in lines:
            if line.startswith("### ") or line.startswith("## ") or line.startswith("* "):
                skip_header = False
            if not skip_header:
                content_lines.append(line)
                
        master_content += f"## {section_title}\n\n"
        master_content += "".join(content_lines)
        master_content += "\n---\n\n"

# Remove the trailing line
if master_content.endswith("\n---\n\n"):
    master_content = master_content[:-7]

with open(output_file, 'w', encoding='utf-8') as out_f:
    out_f.write(master_content.strip() + "\n")

print(f"Master report written to {output_file}")
