import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_raw_file():
    filepath = os.path.join(BASE_DIR, "books", "secret_garden", "chapters", "ch_27_ko.txt")
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replacements
    replacements = [
        # 1. 아버지 -> 아빠 in Colin's first line
        ('“아버지,” 그가 말했다.', '“아빠,” 그가 말했다.'),
        # 2. 화원에 있다니 -> 화원에 있다더니
        ('“화원에! 화원에 있다니!”', '“화원에! 화원에 있다더니!”'),
        # 3. “네,” 콜린이 말을 이었다. -> 콜린이 말을 이었다. “네,
        ('“네,” 콜린이 말을 이었다. “화원이 그렇게 만들어 주었어요.', '콜린이 말을 이었다. “네, 화원이 그렇게 만들어 주었어요.'),
        # 4. 아버지가 오시면 -> 아빠가 오시면
        ('아버지가 오시면 말씀드리려고 우리끼리만', '아빠가 오시면 말씀드리려고 우리끼리만'),
        # 5. 기쁘지 않으세요, 아버지? -> 기쁘지 않아요, 아빠 ?
        ('“기쁘지 않으세요, 아버지?”', '“기쁘지 않아요, 아빠 ?”'),
        # 6. 아버지와 함께 걸어서 저택으로 돌아갈래요.
        ('아버지와 함께 걸어서 저택으로 돌아갈래요.', '아빠와 함께 걸어서 저택으로 돌아갈래요.')
    ]
    
    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated ch_27_ko.txt")
    else:
        print("No changes made to ch_27_ko.txt. Check patterns!")

def fix_tagged_file():
    filepath = os.path.join(BASE_DIR, "books", "secret_garden", "chapters", "tagged", "tagged_ch_27_ko.txt")
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replacements
    replacements = [
        ('<colin>“아버지,”</colin> 그가 말했다.', '<colin>“아빠,”</colin> 그가 말했다.'),
        ('<craven>“화원에! 화원에 있다니!”</craven>', '<craven>“화원에! 화원에 있다더니!”</craven>'),
        ('<colin>“네,”</colin> 콜린이 말을 이었다. <colin>“화원이 그렇게 만들어 주었어요.', '콜린이 말을 이었다. <colin>“네, 화원이 그렇게 만들어 주었어요.'),
        ('아버지가 오시면 말씀드리려고 우리끼리만', '아빠가 오시면 말씀드리려고 우리끼리만'),
        ('<colin>“기쁘지 않으세요, 아버지?”</colin>', '<colin>“기쁘지 않아요, 아빠 ?”</colin>'),
        ('아버지와 함께 걸어서 저택으로 돌아갈래요.', '아빠와 함께 걸어서 저택으로 돌아갈래요.')
    ]
    
    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated tagged_ch_27_ko.txt")
    else:
        print("No changes made to tagged_ch_27_ko.txt. Check patterns!")

def main():
    fix_raw_file()
    fix_tagged_file()

if __name__ == "__main__":
    main()
