"""
Chapter map: the 60 조 of 기이 제1-2 grouped into 24 reader chapters.

Grouping rules:
  - strict textual order, never resequenced
  - no famous narrative 조 is ever split across a chapter boundary
  - the four oversized 조 (태종춘추공, 후백제 견훤, 가락국기 and, marginally, 김부대왕)
    are split internally into 상/하 rather than bundled
  - the short geographic/administrative 조 (이부, 북대방, 사절유택 …) are bundled so a
    chapter never opens on 41 hanja of place-name gloss
  - each chapter is titled for its most memorable story, not its first entry

`split` marks a 조 that is cut into N parts, each its own chapter.
Entry indices are 1-based into VOL1 + VOL2 concatenated (see entries.py).
"""

CHAPTERS = [
    # (ko title, en title, [entry indices], split)
    ("나라의 시작: 단군왕검",      "In the Beginning: Dangun Wanggeom",        [1, 2, 3],              1),
    ("옛 나라들",                 "The Old Kingdoms",                         [4, 5, 6, 7, 8, 9, 10, 11, 12], 1),
    ("주몽, 고구려를 세우다",      "Jumong Founds Goguryeo",                   [13, 14, 15],           1),
    ("혁거세, 알에서 나다",        "Hyeokgeose Born from an Egg",              [16, 17, 18, 19],       1),
    ("탈해, 궤에서 나온 왕",       "Talhae, the King from the Chest",          [20, 21, 22],           1),
    ("황금 궤와 해와 달",          "The Golden Chest, the Sun and the Moon",   [23, 24, 25],           1),
    ("김제상의 충절",             "The Loyalty of Gim Je-sang",               [26],                   1),
    ("거문고 갑을 쏘다",           "Shoot the Zither Case",                    [27, 28, 29, 30],       1),
    ("도화녀와 비형랑",            "Lady Peach Blossom and Bihyeong-rang",     [31, 32, 33],           1),
    ("김유신",                    "Gim Yu-sin",                               [34, 35],               1),
    ("태종 춘추공",               "Lord Chunchu, King Taejong",               [36],                   2),
    ("문무왕 법민",               "King Munmu, Beommin",                      [37, 38],               1),
    ("만파식적",                  "The Flute That Calms Ten Thousand Waves",  [39, 40, 41],           1),
    ("수로부인과 헌화가",          "Lady Suro and the Flower Song",            [42, 43, 44, 45],       1),
    ("원성대왕",                  "Great King Wonseong",                      [46, 47, 48, 49],       1),
    ("처용랑과 망해사",            "Cheoyong-rang and Manghae Temple",         [50, 51],               1),
    ("거타지, 활을 겨누다",        "Geotaji Draws His Bow",                    [52, 53, 54, 55],       1),
    ("김부대왕: 신라의 마지막",    "Great King Gimbu: The Last of Silla",      [56],                   1),
    ("무왕과 서동요",             "King Mu and the Seodong Song",             [57, 58],               1),
    ("후백제 견훤",               "Later Baekje: Gyeon Hwon",                 [59],                   2),
    ("가락국기",                  "Record of the Garak Kingdom",              [60],                   2),
]


def part_label(index, total):
    """'상/하' for a 2-way split, '상/중/하' for 3-way, plain numbers beyond that."""
    if total == 1:
        return ""
    if total == 2:
        return "상하"[index]
    if total == 3:
        return "상중하"[index]
    return str(index + 1)
