import re
import os

ko_file = 'c:/git_repo/TKprof_book/books/dracula/chapters/ch20_ko.txt'
en_file = 'c:/git_repo/TKprof_book/books/dracula/chapters/ch20_en.txt'
out_file = 'c:/git_repo/TKprof_book/books/dracula/chapters/aligned_ko_ch20.txt'

with open(ko_file, 'r', encoding='utf-8') as f:
    ko_text = f.read()

# Clean up [Pxxx] and newlines
ko_text = re.sub(r'\[P\d{3}\]', '', ko_text)
# We want to keep spaces between paragraphs if any, but replace newlines with space
ko_text = re.sub(r'\n+', ' ', ko_text)
# We don't want to break the asterisks string, so let's temporarily protect it
ko_text = ko_text.replace("*       *       *       *       *", "ASTERISK_SEP")
ko_text = re.sub(r' +', ' ', ko_text).strip()
ko_text = ko_text.replace("ASTERISK_SEP", "*       *       *       *       *")

# Now we need to split it into 123 paragraphs.
splits = [
    "제20장", # 1
    "조나단 하커의 일기", # 2
    "10월 1일 저녁.—나는", # 3
    "예의 바르고 총명해", # 4
    "이렇게 치밀하게 움직이는", # 5
    "그가 대답했다.—", # 6
    "\"나리께서 아주 후하게", # 7
    "\"이보쇼 나리, 여기서", # 8
    "그의 말이 일리가", # 9
    "지금 잠시 실망하고", # 10
    "*       *       *       *       *", # 11
    "10월 2일 저녁.—길고", # 12
    "\"샘 블록섬, 왈워스", # 13
    "나는 침대에서 편지를", # 14
    "마차를 몰아 왈워스로", # 15
    "나는 스몰렛의 편지를", # 16
    "\"내가 하숙집 관리인이오.\"", # 17
    "낮 12시가 되어서야", # 18
    "돈을 쥐여주자 무뚝뚝한", # 19
    "내가 정보에 대한", # 20
    "\"글쎄요, 나리. 번지수는", # 21
    "\"두 집 다", # 22
    "\"퍼플리트 집에서는 저를", # 23
    "이런 그의 묘사에", # 24  Wait, I need to check P024 Korean! Let me look.
    "\"아니, 그 양반이", # 25 Wait, check P025
    "\"피카딜리에 있는 집엔", # 26 Wait
]
