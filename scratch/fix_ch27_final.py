import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_raw_file():
    filepath = os.path.join(BASE_DIR, "books", "secret_garden", "chapters", "ch_27_ko.txt")
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace: “이제,” 이야기가 끝나자 콜린이 말했다. “더는 -> 이야기가 끝나자 콜린이 말했다. “이제, 더는
    old_str = '“이제,” 이야기가 끝나자 콜린이 말했다. “더는'
    new_str = '이야기가 끝나자 콜린이 말했다. “이제, 더는'
    
    if old_str in content:
        new_content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated ch_27_ko.txt with final edit.")
    else:
        print("Pattern not found in ch_27_ko.txt!")

def fix_tagged_file():
    filepath = os.path.join(BASE_DIR, "books", "secret_garden", "chapters", "tagged", "tagged_ch_27_ko.txt")
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace: <colin>“이제,”</colin> 이야기가 끝나자 콜린이 말했다. <colin>“더는 -> 이야기가 끝나자 콜린이 말했다. <colin>“이제, 더는
    old_str = '<colin>“이제,”</colin> 이야기가 끝나자 콜린이 말했다. <colin>“더는'
    new_str = '이야기가 끝나자 콜린이 말했다. <colin>“이제, 더는'
    
    if old_str in content:
        new_content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully updated tagged_ch_27_ko.txt with final edit.")
    else:
        print("Pattern not found in tagged_ch_27_ko.txt!")

def main():
    fix_raw_file()
    fix_tagged_file()

if __name__ == "__main__":
    main()
