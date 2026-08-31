import re

def fix_ch08_end():
    filepath = 'chapters/ch08_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # In Korean, [P073] "조금 전 그가..." was split, causing duplicate [P074]
    # Let's merge "조금 전 그가..." back into [P072] and make [P073] "기다리겠습니다..."
    
    text = text.replace('[P073] 조금 전 그가 처음으로 앞뒤가 맞는 말을 내뱉었다.\n\n[P074] "기다리겠습니다, 주인님. 오고 있다—오고 있다—오고 있다!"', '조금 전 그가 처음으로 앞뒤가 맞는 말을 내뱉었다.\n\n[P073] "기다리겠습니다, 주인님. 오고 있다—오고 있다—오고 있다!"')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print("Fixed duplicate P074 at the end of ch08_ko.txt")

if __name__ == '__main__':
    fix_ch08_end()
