import codecs

def fix_paras():
    with codecs.open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch14_ko_modern_refined.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace('"진심을 담아,\n"아브라함 반 헬싱."', '"진심을 담아,\n\n"아브라함 반 헬싱."')
    text = text.replace('"진심을 담아,\n"언제나 헌신하고 감사하는 친구,\n"미나 하커 올림."', '"진심을 담아,\n\n"언제나 헌신하고 감사하는 친구,\n\n"미나 하커 올림."')

    # Remove extra newlines at the end
    text = text.strip() + "\n\n"

    with codecs.open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch14_ko_modern_refined.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    with codecs.open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch14_ko_modern_refined.txt', 'r', encoding='utf-8') as f:
        paras = f.read().split('\n\n')
    print(f'Total paras now: {len(paras)}')

if __name__ == '__main__':
    fix_paras()
