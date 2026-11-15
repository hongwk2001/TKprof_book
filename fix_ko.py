import re

filename = 'books/dracula/chapters/ch13_ko.txt'
with open(filename, 'r', encoding='utf-8') as f:
    text = f.read()

# ko P086
text = re.sub(
    r'(\[P086\] 9월 22일\..*?영원히 침묵할 것이다\.)\s*(아서와 퀸시가 역으로 떠난 후.*?(?=\n\[))',
    r'[P086a] \1\n[P086b] \2',
    text, flags=re.DOTALL
)

# ko P087
text = re.sub(
    r'(\[P087a\] "아, 자네는 내 마음을.*?처참한 순간에 말이야\.)\s*(불쌍한 소년 아서를 생각하면.*?앞으로 나아갈 수 있는 거야\.")\s*\[P087b\]',
    r'\1\n[P087b] \2\n[P087c]',
    text, flags=re.DOTALL
)

# ko P103
text = re.sub(
    r'(\[P103\] 최근 햄프스테드.*?상태로 발견되었다\.)\s*(첫 번째로 실종되었던 아이가.*?(?=\n\[|$))',
    r'[P103a] \1\n[P103b] \2',
    text, flags=re.DOTALL
)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(text)
