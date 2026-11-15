import os

ko_file = r"C:\git_repo\TKprof_book\books\dracula\chapters\ch09_ko.txt"
with open(ko_file, 'r', encoding='utf-8') as f:
    text = f.read()

# P005
p005_old = text[text.find('[P005]'):text.find('\n', text.find('[P005]'))]
p005_new = p005_old.replace('[P005]', '[P005a]').replace('겁이 나. 아가사', '겁이 나.\n\n[P005b] 아가사')

# P052e
p052e_old = text[text.find('[P052e]'):text.find('\n', text.find('[P052e]'))]
p052e_new = p052e_old.replace('[P052e]', '[P052ea]').replace('설명해 두었지. 내 오랜', '설명해 두었지.\n\n[P052eb] 내 오랜')

# P065
p065_old = text[text.find('[P065]'):text.find('\n', text.find('[P065]'))]
p065_new = p065_old.replace('[P065]', '[P065a]').replace("나눠봅시다.' 나는 그 눈치를", "나눠봅시다.'\n\n[P065b] 나는 그 눈치를")

text = text.replace(p005_old, p005_new)
text = text.replace(p052e_old, p052e_new)
text = text.replace(p065_old, p065_new)

with open(ko_file, 'w', encoding='utf-8') as f:
    f.write(text)
