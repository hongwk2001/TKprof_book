import re

def generate_summary():
    input_file = "d:\\git_repo\\TKprof_book\\books\\The_Muqaddimah\\The_Muqaddimah_Original.txt"
    output_file = "d:\\git_repo\\TKprof_book\\books\\The_Muqaddimah\\muqaddimah_summary.md"

    headings = []
    word_count = 0
    current_heading = "Front Matter"
    heading_start_word = 0
    
    # Regex for catching chapter titles
    # "الباب" = Part/Chapter, "الفصل" = Section, "المقدمة" = Introduction
    # Look for lines that start with these and are relatively short.
    heading_pattern = re.compile(r'^\s*(?:الباب|الفصل|المقدمة|الجزء)(?:\s+.*)?$')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
                
            words_in_line = len(line.split())
            word_count += words_in_line
            
            # Check if line is a heading
            if len(line) < 100 and heading_pattern.match(line):
                # Save previous heading
                if current_heading:
                    headings.append({
                        "title": current_heading,
                        "words": word_count - heading_start_word,
                        "start_page_estimate": (heading_start_word // 300) + 1
                    })
                current_heading = line
                heading_start_word = word_count
                
    # Add the last heading
    if current_heading:
        headings.append({
            "title": current_heading,
            "words": word_count - heading_start_word,
            "start_page_estimate": (heading_start_word // 300) + 1
        })
        
    # Clean up and consolidate very short sections if needed, but let's keep it raw for now
    # We will just write out the major ones (e.g., skip ones with < 50 words to avoid OCR noise)
    valid_headings = [h for h in headings if h['words'] >= 50 or h['title'] == 'Front Matter']
    
    # Write summary
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("# Summary of The Muqaddimah (Original Text)\n\n")
        out.write(f"**Total Word Count:** {word_count:,}\n")
        out.write(f"**Estimated Total Pages (~300 words/page):** {(word_count // 300) + 1:,}\n\n")
        out.write("| Title (Arabic) | Estimated Start Page | Word Count |\n")
        out.write("|---|---|---|\n")
        for h in valid_headings:
            out.write(f"| {h['title']} | {h['start_page_estimate']} | {h['words']:,} |\n")

if __name__ == "__main__":
    generate_summary()
