import os
import re

def split_into_sentences(text):
    # Very simple sentence splitter based on punctuation
    # This avoids splitting on Mr. Mrs. but gets the job done for a rough audit
    text = re.sub(r'(?<!Mr)(?<!Mrs)(?<!Dr)\.\s+', '.\n', text)
    text = re.sub(r'!\s+', '!\n', text)
    text = re.sub(r'\?\s+', '?\n', text)
    sentences = text.split('\n')
    return [s.strip() for s in sentences if s.strip()]

def main():
    chapters_dir = r"d:\git_repo\TKprof_book\books\two_cities\chapters"
    output_file = r"d:\git_repo\TKprof_book\books\two_cities\surgical_fix_list.md"
    
    files = [f for f in os.listdir(chapters_dir) if f.endswith("_en.txt")]
    files.sort()
    
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("# 📝 Two Cities: Surgical Fix Master List\n\n")
        out.write("This document tracks all exceptionally long or grammatically complex sentences that require an 'ultra-casual' rewrite for audiobook compliance.\n\n")
        
        for filename in files:
            file_path = os.path.join(chapters_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            sentences = split_into_sentences(content)
            
            flagged = []
            for s in sentences:
                word_count = len(s.split())
                comma_count = s.count(',')
                semi_count = s.count(';')
                
                # Flag if: over 35 words OR has more than 3 commas/semicolons
                if word_count > 35 or (comma_count + semi_count) > 3:
                    flagged.append(s)
            
            if flagged:
                out.write(f"## {filename}\n")
                for s in flagged:
                    # Clean up the sentence for display
                    clean_s = s.replace('\n', ' ')
                    out.write(f"- [ ] {clean_s}\n")
                out.write("\n")

    print(f"Master list generated at {output_file}")

if __name__ == "__main__":
    main()
