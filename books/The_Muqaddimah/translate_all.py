import re
import math

translations = {
    'الجزء': 'Part',
    'الفصل': 'Section',
    'المقدمة': 'Introduction',
    'الباب': 'Chapter',
    'الكتاب': 'Book',
    'الأولى': 'First',
    'الأول': 'First',
    'الثانية': 'Second',
    'الثاني': 'Second',
    'الثالثة': 'Third',
    'الثالث': 'Third',
    'الرابعة': 'Fourth',
    'الرابع': 'Fourth',
    'الخامسة': 'Fifth',
    'الخامس': 'Fifth',
    'السادسة': 'Sixth',
    'السادس': 'Sixth',
    'السابعة': 'Seventh',
    'السابع': 'Seventh',
    'الثامنة': 'Eighth',
    'الثامن': 'Eighth',
    'التاسعة': 'Ninth',
    'التاسع': 'Ninth',
    'العاشرة': 'Tenth',
    'العاشر': 'Tenth',
    'في علم التاريخ': 'On the Science of History',
    'في': 'on',
    'من': 'of',
    'تكملة': 'Continuation of',
    'تفصيل الكلام في الجغرافيا': 'Details on Geography',
    'تابع': 'continued',
    'إبطال صناعة النجوم': 'Refutation of Astrology',
    'صناعة الشعر ووجه تعلمه': 'The Art of Poetry and its Learning',
    'كيفية عمل الشعر': 'How to Make Poetry',
    'خاتمة': 'Conclusion',
    'صناعة': 'The Art',
    'علم': 'Science',
    'الدول': 'Dynasties',
    'الخراب': 'Ruins',
    'التعليم': 'Education',
    'الأمصار': 'Cities'
}

def translate_line(line):
    # Fix weird quotes and punctuation
    line = line.replace('»', ',').replace('ء', ',').replace('؛', ',')
    for ar, en in sorted(translations.items(), key=lambda x: len(x[0]), reverse=True):
        line = line.replace(ar, en)
    
    # Optional: remove remaining arabic letters if user wants a clean english-only doc
    # but some titles might disappear entirely. Let's keep them but filtered.
    return line.strip()

with open('muqaddimah_summary.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('muqaddimah_summary_en.md', 'w', encoding='utf-8') as f:
    for line in lines:
        if '| Title (Arabic) |' in line:
            f.write('| Title (English Translated) | Page Count | Word Count |\n')
        elif line.startswith('|---'):
            f.write('|---|---|---|\n')
        elif line.startswith('| ') and not line.startswith('| Title'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                ar_title = parts[1]
                en_title = translate_line(ar_title)
                
                # parts[3] is the word count string (e.g. "1,234")
                word_count_str = parts[3].replace(',', '')
                try:
                    words = int(word_count_str)
                    page_count = max(1, math.ceil(words / 300))
                except ValueError:
                    page_count = 1
                    
                f.write(f"| {en_title} | {page_count} | {parts[3]} |\n")
            else:
                f.write(line)
        else:
            if "Estimated Start Page" in line:
                pass # skip or modify if needed, but it's just the header
            else:
                f.write(line)

print("Translation and page count calculation complete.")
