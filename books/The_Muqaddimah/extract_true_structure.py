import math

# Keywords indicating the start of a chapter (searching after line 1000 to skip TOC)
chapter_markers = [
    ("Book One, Chapter One: Human civilization in general", "في العمران البشري"),
    ("Book One, Chapter Two: Bedouin civilization", "في العمران البدوي"),
    ("Book One, Chapter Three: Dynasties, royal authority, the caliphate", "في الدول والملك"),
    ("Book One, Chapter Four: Countries and cities", "في البلدان والأمصار"),
    ("Book One, Chapter Five: Making a living, crafts", "في المعاش"),
    ("Book One, Chapter Six: Sciences and education", "في العلوم وأصنافها"),
    ("END", None) # End marker
]

with open('The_Muqaddimah_Original.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start lines of each chapter
chapter_lines = []
for title, marker in chapter_markers[:-1]:
    for i, line in enumerate(lines):
        if i < 1000: # skip TOC
            continue
        if marker in line:
            chapter_lines.append((title, i))
            break # found the first actual chapter occurrence

chapter_lines.append(("End of Document", len(lines)))

# Calculate word counts
results = []
for i in range(len(chapter_lines) - 1):
    title = chapter_lines[i][0]
    start_line = chapter_lines[i][1]
    end_line = chapter_lines[i+1][1]
    
    # Calculate word count between these lines
    words = 0
    for j in range(start_line, end_line):
        words += len(lines[j].split())
        
    page_count = max(1, math.ceil(words / 300))
    results.append((title, page_count, words))

# Write to the true structure summary
with open('muqaddimah_true_structure.md', 'w', encoding='utf-8') as f:
    f.write("# The True Structure of The Muqaddimah\n\n")
    f.write("This table shows the actual structured chapters of Ibn Khaldun's work, skipping the noisy publisher's Table of Contents and prefaces.\n\n")
    f.write("| Title (English) | Estimated Page Count | Word Count |\n")
    f.write("|---|---|---|\n")
    
    total_words = 0
    total_pages = 0
    for title, pages, words in results:
        f.write(f"| {title} | {pages} | {words:,} |\n")
        total_words += words
        total_pages += pages
        
    f.write(f"| **Total (Main Chapters only)** | **{total_pages}** | **{total_words:,}** |\n")

print("Created muqaddimah_true_structure.md")
