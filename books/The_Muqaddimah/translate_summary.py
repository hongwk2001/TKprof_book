import re

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
    'تابع': 'continued'
}

def translate_line(line):
    # Split by words or simple replace
    for ar, en in translations.items():
        line = line.replace(ar, en)
    return line

with open('muqaddimah_summary.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('muqaddimah_summary_en.md', 'w', encoding='utf-8') as f:
    for line in lines:
        if '| Title (Arabic) |' in line:
            f.write(line.replace('Title (Arabic)', 'Title (English Translated)'))
        elif line.startswith('| '):
            parts = line.split('|')
            if len(parts) >= 4:
                ar_title = parts[1]
                en_title = translate_line(ar_title)
                parts[1] = en_title
                f.write('|'.join(parts))
            else:
                f.write(line)
        else:
            f.write(line)

print("Translation complete.")
