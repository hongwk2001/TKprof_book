"""
Entry (조) table for 삼국유사 권1 기이제1 + 권2 기이제2.

Volume 2 headings come from the wiki's own section markup. Volume 1 is transcluded
page-by-page from the 1512 奎章閣本 scan and carries no headings, so its boundaries are
listed here by the exact text of the title block as it appears in raw/vol_1.txt --
verified against that file, not asserted from an edition.

`ko` / `en` are the reader-facing chapter headings (is_header rows in the app JSON).
"""

# (title-block text as it appears in raw/vol_1.txt, ko, en)
VOL1 = [
    ("紀異卷第一",    "기이 제1 · 서문",        "Marvels I: Preface"),
    ("古朝鮮",        "고조선 (왕검조선)",       "Gojoseon: Dangun Wanggeom"),
    ("魏滿朝鮮",      "위만조선",              "Wiman Joseon"),
    ("馬韓",          "마한",                 "Mahan"),
    ("二府",          "이부",                 "The Two Commands"),
    ("七十二國",      "칠십이국",              "The Seventy-Two States"),
    ("樂浪國",        "낙랑국",                "The State of Nangnang"),
    ("北帶方",        "북대방",                "Northern Daebang"),
    ("南帶方",        "남대방",                "Southern Daebang"),
    ("靺鞨",          "말갈과 발해",            "Malgal and Balhae"),
    ("伊西國",        "이서국",                "The State of Iseo"),
    ("五伽耶",        "오가야",                "The Five Gaya"),
    ("北扶餘",        "북부여",                "Northern Buyeo"),
    ("東扶餘",        "동부여",                "Eastern Buyeo"),
    ("高句麗",        "고구려 (주몽)",          "Goguryeo: Jumong"),
    ("卞韓百濟",      "변한과 백제",            "Byeonhan and Baekje"),
    ("辰韓",          "진한",                  "Jinhan"),
    ("又四節遊宅",    "사절유택",               "The Four Seasonal Villas"),
    ("新羅始祖赫居世王", "신라 시조 혁거세왕",    "Hyeokgeose, Founder of Silla"),
    ("第二南解王",    "제2대 남해왕",           "King Namhae, the Second"),
    ("第三弩禮王",    "제3대 노례왕",           "King Norye, the Third"),
    ("第四脫解王",    "제4대 탈해왕",           "King Talhae, the Fourth"),
    ("金閼智 脫解王代", "김알지 · 탈해왕대",      "Gim Alji, in the Reign of Talhae"),
    ("延烏郎 細烏女",  "연오랑과 세오녀",        "Yeono-rang and Seo-nyeo"),
    ("末鄒王 竹葉軍",  "미추왕과 죽엽군",        "King Michu and the Bamboo-Leaf Army"),
    ("奈勿王",        "내물왕과 김제상",        "King Naemul and Gim Je-sang"),
    ("第十八實聖王",  "제18대 실성왕",          "King Silseong, the Eighteenth"),
    ("射琴匣",        "사금갑 (거문고 갑을 쏘다)", "Shoot the Zither Case"),
    ("智哲老王",      "지철로왕",               "King Jicheollo"),
    ("真興王",        "진흥왕",                "King Jinheung"),
    ("桃花女 鼻荊郎",  "도화녀와 비형랑",        "Lady Peach Blossom and Bihyeong-rang"),
    ("天賜玉帶",      "천사옥대",               "The Jade Belt from Heaven"),
    ("善德王知幾三事", "선덕여왕 지기삼사",       "Queen Seondeok Foresaw Three Things"),
    ("真德王",        "진덕여왕",               "Queen Jindeok"),
    ("金庾信",        "김유신",                "Gim Yu-sin"),
    ("大宗春秋公",    "태종 춘추공",            "Lord Chunchu, King Taejong"),
    ("春郎 罷郎",     "장춘랑과 파랑",          "Jangchun-rang and Parang"),
]

# Volume 2 -- keys are the wiki section headings, matched on their leading title text.
VOL2 = [
    ("文虎王法敏",    "문무왕 법민",            "King Munmu, Beommin"),
    ("万波息笛",      "만파식적",               "The Flute That Calms Ten Thousand Waves"),
    ("孝昭王代 竹旨郎", "효소왕대 죽지랑",        "Jukji-rang, in the Reign of Hyoso"),
    ("聖德王",        "성덕왕",                "King Seongdeok"),
    ("水路夫人",      "수로부인 (헌화가)",       "Lady Suro and the Flower Song"),
    ("孝成王",        "효성왕",                "King Hyoseong"),
    ("景德王 忠談師 表訓大德", "경덕왕 · 충담사 · 표훈대덕", "King Gyeongdeok, Master Chungdam, Great Virtue Pyohun"),
    ("惠恭王",        "혜공왕",                "King Hyegong"),
    ("元聖大王",      "원성대왕",               "Great King Wonseong"),
    ("早雪",          "이른 눈",                "Early Snow"),
    ("興德王鸚鵡",    "흥덕왕과 앵무새",         "King Heungdeok and the Parrot"),
    ("神武大王閻長 弓巴", "신무대왕 · 염장 · 궁파", "Great King Sinmu, Yeomjang, and Gungpa"),
    ("四十八景文大王", "제48대 경문대왕",         "Great King Gyeongmun, the Forty-Eighth"),
    ("處容郎 望海寺",  "처용랑과 망해사",        "Cheoyong-rang and Manghae Temple"),
    ("真聖女大王居陀知", "진성여대왕과 거타지",    "Queen Jinseong and Geotaji"),
    ("孝恭王",        "효공왕",                "King Hyogong"),
    ("景明王",        "경명왕",                "King Gyeongmyeong"),
    ("景哀王",        "경애왕",                "King Gyeongae"),
    ("金傳大王",      "김부대왕",               "Great King Gimbu"),
    ("南扶餘 前百濟",  "남부여 · 전백제",        "Nambuyeo and Former Baekje"),
    ("武王",          "무왕 (서동요)",          "King Mu and the Seodong Song"),
    ("後百濟 甄萱",    "후백제 견훤",            "Later Baekje: Gyeon Hwon"),
    ("駕洛國記",      "가락국기",               "Record of the Garak Kingdom"),
]

# Everything at or after this vol_1 title block is 王曆 king-list tables + wiki
# footnote debris, not 기이 -- dropped.
VOL1_END_MARKER = "東晉中宗建虎"
