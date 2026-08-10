import codecs

def find_mismatch():
    with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch14_en.txt', 'rb') as f:
        en_text = f.read().decode('utf-8').replace('\r\n', '\n')
    en_paras = en_text.strip().split('\n\n')
    
    with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch14_ko_modern_refined.txt', 'rb') as f:
        ko_text = f.read().decode('utf-8').replace('\r\n', '\n')
    ko_paras = ko_text.strip().split('\n\n')

    with codecs.open(r'c:\git_repo\TKprof_book\books\dracula\chapters\mismatch_log.txt', 'w', encoding='utf-8') as log:
        log.write(f"EN: {len(en_paras)}, KO: {len(ko_paras)}\n")
        for i in range(max(len(en_paras), len(ko_paras))):
            en_str = en_paras[i][:30].replace('\n', ' ') if i < len(en_paras) else "N/A"
            ko_str = ko_paras[i][:30].replace('\n', ' ') if i < len(ko_paras) else "N/A"
            log.write(f"[{i}] EN: {en_str} | KO: {ko_str}\n")

if __name__ == '__main__':
    find_mismatch()
