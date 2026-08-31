import re

def fix(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()

    # en P086
    if "ch13_en" in filename:
        text = re.sub(
            r'(\[P086\] September 22\..*?remain silent forever\.)\s*(After Arthur and Quincey left.*)',
            r'[P086a] \1\n[P086b] \2',
            text, flags=re.DOTALL
        )

    # en P087
    if "ch13_en" in filename:
        text = re.sub(
            r'(\[P087a\] "Ah, you do not understand.*?and drained the color from my face\.)\s*(When I think of the poor boy Arthur.*?heavy burdens\.")\s*\[P087b\]',
            r'\1\n[P087b] \2\n[P087c]',
            text, flags=re.DOTALL
        )

    # en P103
    if "ch13_en" in filename:
        text = re.sub(
            r'(\[P103\] Lately, the Hampstead area.*?morning in a cold state\.)\s*(Because the first child to go missing.*?charming performance\.)',
            r'[P103a] \1\n[P103b] \2',
            text, flags=re.DOTALL
        )

    # ko P086
    if "ch13_ko" in filename:
        text = re.sub(
            r'(\[P086\] 9월 22일\..*?영원히 침묵할 것이다\.)\s*(아서와 퀸시가 역으로 떠난 후.*)',
            r'[P086a] \1\n[P086b] \2',
            text, flags=re.DOTALL
        )
    # ko P087
    if "ch13_ko" in filename:
        text = re.sub(
            r'(\[P087a\] "아, 자네는 내 마음을.*?처참한 순간에 말이야\.)\s*(불쌍한 소년 아서를 생각하면.*?앞으로 나아갈 수 있는 거야\.")\s*\[P087b\]',
            r'\1\n[P087b] \2\n[P087c]',
            text, flags=re.DOTALL
        )
    # ko P103
    if "ch13_ko" in filename:
        text = re.sub(
            r'(\[P103\] 최근 햄프스테드.*?상태로 발견되었다\.)\s*(첫 번째로 실종되었던 아이가.*?농담을 던졌다\.)',
            r'[P103a] \1\n[P103b] \2',
            text, flags=re.DOTALL
        )

    # fix double bracket for ko P086 if it happens
    text = text.replace("[P086a] [P086]", "[P086a]")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

fix('books/dracula/chapters/ch13_en.txt')
fix('books/dracula/chapters/ch13_ko.txt')
