import re

def fix_ch08_p070():
    filepath = 'chapters/ch08_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split [P069b] before "주인님, 당신의 명을" so "주인님..." becomes [P070]
    # And then re-tag subsequent paragraphs to P071a, P071b, P072, P073, P074
    
    text = text.replace('[P071a] "주인님, 당신의 명을', '[P070] "주인님, 당신의 명을')
    text = text.replace('[P071b] 어쨌거나 그는', '[P071a] 어쨌거나 그는')
    text = text.replace('[P072] 그 정도의 힘과', '[P071b] 그 정도의 힘과')
    
    # Insert [P072] "조금 전 그가..." right before [P073]
    text = text.replace('[P073] "기다리겠습니다', '[P072] 조금 전 그가 처음으로 앞뒤가 맞는 말을 내뱉었다.\n\n[P073] "기다리겠습니다')
    text = text.replace('[P074] 그래서 나도', '[P074] 그래서 나도')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print("Fixed P070-P074 split and realignment in ch08_ko.txt")

if __name__ == '__main__':
    fix_ch08_p070()
