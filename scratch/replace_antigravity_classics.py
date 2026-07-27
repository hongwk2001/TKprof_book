import re

files_to_update = [
    r"d:\git_repo\TKprof_book\books\art_of_war\generate_audio.py",
    r"d:\git_repo\TKprof_book\books\art_of_war\generate_audio_ko.py",
    r"d:\git_repo\TKprof_book\books\art_of_war\make_epub_native.py",
    r"d:\git_repo\TKprof_book\books\art_of_war\metadata.md",
    r"d:\git_repo\TKprof_book\books\frankenstein\metadata.md",
    r"d:\git_repo\TKprof_book\books\seneca_on_happiness\generate_audio.py",
    r"d:\git_repo\TKprof_book\books\seneca_on_happiness\generate_audio_ko.py",
    r"d:\git_repo\TKprof_book\books\seneca_shortness_of_life\generate_audio.py",
    r"d:\git_repo\TKprof_book\books\seneca_shortness_of_life\generate_audio_ko.py",
    r"d:\git_repo\TKprof_book\books\seneca_shortness_of_life\make_epub_native.py",
    r"d:\git_repo\TKprof_book\books\seneca_shortness_of_life\metadata.md",
    r"d:\git_repo\TKprof_book\books\thirty_six_stratagems\copyright_en.txt",
    r"d:\git_repo\TKprof_book\books\thirty_six_stratagems\make_epub_native.py",
    r"d:\git_repo\TKprof_book\books\thirty_six_stratagems\metadata.md"
]

for f in files_to_update:
    print(f"Updating {f}...")
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Replace Antigravity Classics / Antigravity Classic with TKPROF LLC
    new_content = re.sub(r'Antigravity Classics?', 'TKPROF LLC', content, flags=re.IGNORECASE)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print("  Successfully updated!")
    else:
        print("  No changes made.")
