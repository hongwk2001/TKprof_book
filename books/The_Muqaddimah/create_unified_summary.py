import re
import math

ar_to_en = {
    'المقدمة': 'Introduction',
    'الباب': 'Chapter',
    'الفصل': 'Section',
    'الجزء': 'Part',
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
    'في قسط العمران من الأرض': 'on the portion of civilization on Earth',
    'والإشارة إلى بعض': 'and reference to some',
    'في الدول والملك والخلافة والمراتب': 'on dynasties, royal authority, the caliphate, and ranks',
    'في الفكر الإنسانى الذي تميز به البشر عن الحيوانات': 'on human thought that distinguishes humans from animals',
    'واهتديى': 'and guided',
    'في أشعار العرب وأهل الأمصار لهذا العهد': 'on poetry of the Arabs and city dwellers of this era',
    'من كتاب العبر في أخبار العرب والعجم والبربر': 'from the Book of Lessons on the history of Arabs, Persians, and Berbers',
    'وهي علمية كلها': 'and it is all scientific',
    'في فضل علم التاريخ': 'on the merit of the science of history',
    'في علم التاريخ': 'on the science of history',
    'تكملة': 'Continuation of',
    'تفصيل الكلام في الجغرافيا': 'Details on Geography',
    'في البلدان والأمصار والمدن وسائر': 'on countries, regions, cities, and others',
    'في المعاش ووجوهه من الكسب': 'on making a living and its ways of earning',
    'في العلوم وأصنافهاء والتعليم': 'on sciences, their types, and education',
    'إبطال صناعة النجوم': 'Refutation of Astrology',
    'صناعة الشعر ووجه تعلمه': 'The Art of Poetry and its Learning',
    'كيفية عمل الشعر': 'How to Make Poetry',
    'من مزوجات ابن شجاع وملعبة الكفيف': 'from the poems of Ibn Shuja and the play of the blind',
    'خاتمة': 'Conclusion',
    'الخراب في الأمصار': 'Ruins in cities',
    'أمهات الصنائع': 'Mother of crafts',
    'التفاوت بين مراتب السيف والقلم': 'Disparity between the ranks of the sword and the pen',
    'في الحاجة إلى صناعة الطب في الأمصار': 'on the need for the medical profession in cities',
    'كيفية العمل في الزايرجة': 'How to work with the Zairajah',
    'والثاني في الباب الثالث': 'and the second in Chapter Three',
    'بواسطتهما معّاء': 'through them together',
    'وتحقيق مذاهبه وال ااع بمغالط المؤرخين': 'and verifying its methods and avoiding historians fallacies',
    'في أن آثار الدولة كلها على نسبة قوتها في أصلها': 'that all effects of a dynasty are proportionate to its original strength',
    'انعكاس نقص العطاء على الجباية': 'Reflection of decreased spending on tax collection',
    'ولطالما': 'And often',
    'من': 'of',
    'في': 'in/on',
    'تابع': 'continued',
    'نص': 'Text',
    'الفكر الإغريقي إلى الثقافة العربية': 'Greek thought to Arabic culture',
    'الإسلام في التاريثخ العالمي': 'Islam in World History',
    'من أعمال عبد السلام الشدادي': 'From the works of Abdesselam Cheddadi',
    'ابن خلدون وعلم العمران البشري': 'Ibn Khaldun and the Science of Human Civilization',
    'العرب واستملاك التاريخ': 'Arabs and the appropriation of history',
    'الطبعة الخاصة فى خمسة مجلدات': 'Special edition in five volumes',
    'خزانة ابن خلدون': 'Ibn Khaldun Library',
    'هذا العمل نشر بدعم': 'This work was published with support',
    'إن المركز الوطنى': 'The National Center',
    'إضافة إلى ذلك': 'In addition to that',
    'Front Matter': 'Front Matter',
    'والتعليم': 'and education',
    'صناعة': 'The art',
    'الدول العامة والملك': 'General dynasties and royal authority',
    'الدول': 'Dynasties',
    'الخراب': 'Ruins',
    'الأمصار': 'Cities/Regions',
    'المقدمة أو في التعريف': 'Introduction or Definition',
    'يعبر ابن خلدون عن شعور حاد بالمصير الكوني لا': 'Ibn Khaldun expresses an acute sense of cosmic destiny',
    'بالاعتراف التام كإسهام علمي أساسيء فإنه لم يُعْتَبَّر التاريخ': 'With full recognition as a fundamental scientific contribution, history was not considered',
    'الفصل الذي عنوانه': 'The section titled',
    'ورد': 'mentioned',
    'انظر الجزء الأول': 'See Part One',
    'الباب الآخر ولزوم العمل به تلق إن شاء الله نحاحًا': 'The other chapter and the necessity of acting upon it, God willing, you will find success',
    'باب تخريب البيت ذو السويقتين': 'Chapter on the destruction of the Kaaba by Dhul-Suwayqatayn',
    'الفصل كله مشروط بالمدرك البشري': 'The entire section is conditioned by human perception',
    'فلو فرضنا عدم المدرك البشري جملة': 'If we assume the absence of human perception entirely',
    'الفصل المخصص للمقصورة يآتي بعد الفصل المخصص للآلة': 'The section dedicated to the maqsurah comes after the section dedicated to the instrument',
    'والفصل المخصص للدعاء في الخطبة': 'and the section dedicated to supplication in the sermon',
    'الفصل المتقدم قبل هذاء والله أعلم': 'The preceding section before this, and God knows best',
    'ولأجل ذلك': 'And for that reason',
    'من الأرض': 'of the Earth',
    'الخلافة': 'Caliphate',
    'والمراتب': 'and Ranks',
    'السلطانية': 'Sultanic',
    'الجزء الرابع من الإقليم الثاني': 'Fourth part of the second zone',
    'ويصب في بحيرة الفيوم': 'and flows into Lake Faiyum',
    'وعلى سمته شرثًا': 'and on its path eastwards',
    'من الشرق على طرف قد امتد من هذا البحر مشرقًا ووراءه إلى': 'from the east on an edge extending from this sea eastwards and behind it to',
    'ويذهب مشرقًا بانحراف إلى الشمال إلى أن يخرج إلى الجزء التاسع': 'and goes eastwards inclining north until it exits to the ninth part',
    'فتقع فيه قطعة منه تفضي ثناياها إلى البر المتصل': 'a piece of it falls in it leading its folds to the connected mainland',
    'ويسمى أرض': 'and is called the land of',
    'قطعة نحو الثلث؛. يمر الشمالي منها إلى الغرب منعطمًا مع البحرء كما': 'a piece about a third; its northern part passes westwards turning with the sea, as',
    'من شرقه': 'from its east',
    'ويمر في وسط هذه القطعة نهر الفرات ونهر دجلة': 'and the Euphrates and Tigris rivers pass through the middle of this piece',
    'يخرجان': 'they exit',
    'ويتصل على سمته بجبل السلسلة في الجزء الخامس': 'and connects on its path to the Chain Mountain in the fifth part',
    'فيقطع': 'so it cuts',
    'منه أكثره مغمور بالماء': 'of it mostly submerged in water',
    'إلا قليلاً من جنوبه وشرقه لأن البحر': 'except a little of its south and east because the sea',
    'من شرقه آنمًا': 'from its east earlier',
    'وتنكشف من هذا الجزء قطعة عند زاويته': 'and a piece is exposed from this part at its corner',
    'من الإقليم السادس': 'of the sixth zone',
    'وفيه السد هنالك؛ كما نذكر': 'and there is the dam there, as we mention',
    'وبقيت منه': 'and remained of it',
    'واتصلت بها القطعة الأخرى في الشمال من غربه إلى شرقه': 'and the other piece connected to it in the north from its west to its east',
    'وهر مغربًا بانحراف إلى الشمالء إلى أن يقف في بلاد': 'and goes westwards inclining to the north until it stops in the countries of',
    'من السادس': 'of the sixth',
    'وتخرج منه جداول تذهب مغربًا وتنصب في': 'and streams exit from it going west and flowing into',
    'والخامس منه': 'and the fifth of it',
    'من شماله جبل قوفاياء متصل من غربه إلى شرقه': 'from its north Qawfaya Mountain connected from its west to its east',
    'بانحراف إلى الغرب': 'inclining to the west',
    'فيغمر ما بين شرقيه وجوفيه قطعة مثلثة عليها من': 'so it submerges between its east and its interior a triangular piece on which is',
    'في [ب] ]': 'in [B]',
    'ش': 'Sh',
    'ظ': '',
    'ء': ',',
    '»': ',',
    '؛': ',',
    '؟': '?'
}

def clean_arabic(text):
    # Sort keys by length descending to replace longer phrases first
    sorted_keys = sorted(ar_to_en.keys(), key=len, reverse=True)
    for ar in sorted_keys:
        text = text.replace(ar, ar_to_en[ar])
    # Remove any stray Arabic characters that missed the dictionary
    text = re.sub(r'[\u0600-\u06FF]+', '', text)
    # Cleanup extra spaces/commas
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s*,\s*', ', ', text)
    text = re.sub(r',\s*$', '', text)
    return text.strip()

with open('muqaddimah_summary.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
output_lines.append("# Summary of The Muqaddimah\n\n")
output_lines.append("| Title (English) | Page Count | Word Count |\n")
output_lines.append("|---|---|---|\n")

for line in lines:
    if line.startswith('| ') and not line.startswith('| Title'):
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:
            ar_title = parts[1]
            words_str = parts[3].replace(',', '')
            try:
                words = int(words_str)
                page_count = max(1, math.ceil(words / 300))
            except ValueError:
                page_count = 1
                
            en_title = clean_arabic(ar_title)
            if not en_title:
                en_title = "Section"
                
            output_lines.append(f"| {en_title} | {page_count} | {parts[3]} |\n")

with open('muqaddimah_summary_en.md', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print("Unified english summary created.")
