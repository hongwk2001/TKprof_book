import codecs

def final_fix():
    with codecs.open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch14_ko_modern_refined.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    # Fix space
    text = text.replace(' 하커 부인이 반 헬싱에게 보낸 전보.', '하커 부인이 반 헬싱에게 보낸 전보.')
    
    # Fix the merged lines:
    text = text.replace('"언제나 헌신하고 감사하는 친구,\n"미나 하커 올림."', '"언제나 헌신하고 감사하는 친구,\n\n"미나 하커 올림."')

    # Also check if I missed any other \n that should be \n\n.
    # EN 64 is "Believe me,", EN 65 is "Your faithful...", EN 66 is "Mina Harker"
    
    with codecs.open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch14_ko_modern_refined.txt', 'w', encoding='utf-8') as f:
        f.write(text.strip() + "\n\n")

    with codecs.open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch14_ko_modern_refined.txt', 'r', encoding='utf-8') as f:
        paras = f.read().strip().split('\n\n')
    print(f'Total paras now: {len(paras)}')

if __name__ == '__main__':
    final_fix()
