"""
The six 향가 (鄕歌) inside 기이 제1-2.

These are NOT Classical Chinese. They are Old Korean written in 향찰 -- Chinese
characters used partly for sound and partly for meaning -- and a translator handed
one as if it were 한문 will produce confident nonsense, because the grammatical
particles (隱 肹 叱 尸 賜 古 如) are being read as content words.

They also cannot simply be handed a published reading: every standard reconstruction
(양주동 1942, 김완진 1980) is still in copyright. So these items are translated from
the surrounding narrative, which in every one of these six cases states what the song
is for and what it says -- a faithful prose rendering, never a line-by-line claim.

Spans are exact substrings of raw/vol_2.txt, verified against that file. The songs
run flush into the prose around them (서동요 ends and 童謠滿京 begins with no
punctuation at all), so they are pinned by explicit start/end rather than detected.
"""

HYANGGA = [
    {
        "ko": "모죽지랑가", "en": "Song in Longing for Jukji-rang",
        "start": "去隱春皆理米", "end": "蓬次叱巷中宿尸夜音有叱下是",
        "gloss_ko": "득오가 죽지랑을 그리워하며 지은 노래.",
        "gloss_en": "Deugo's song of longing for his lord Jukji-rang.",
    },
    {
        "ko": "헌화가", "en": "The Flower-Offering Song",
        "start": "紫布岩乎過希", "end": "花肹折叱可獻乎理音如",
        "gloss_ko": "소를 몰던 노인이 수로부인에게 벼랑의 철쭉꽃을 꺾어 바치며 부른 노래.",
        "gloss_en": "An old herdsman's song as he picks azaleas from a cliff for Lady Suro.",
    },
    {
        "ko": "안민가", "en": "Song for Governing the People",
        "start": "君隱父也", "end": "為內尸等焉國惡太平恨音叱如",
        "gloss_ko": "충담사가 경덕왕의 명을 받아 지은 노래. 임금은 아버지, 신하는 어머니, 백성은 어린아이에 견주어, 각자 제 도리를 다하면 나라가 태평하다고 노래했다. 부른 이는 충담사다.",
        "gloss_en": "Master Chungdam's song, made at King Gyeongdeok's command, on what a ruler, a minister and a people each owe.",
    },
    {
        "ko": "찬기파랑가", "en": "Song in Praise of Gipa-rang",
        "start": "咽嗚爾處米", "end": "雪是毛冬乃乎尸花判也",
        "gloss_ko": "충담사가 화랑 기파랑의 높은 뜻을 기려 지은 노래.",
        "gloss_en": "Master Chungdam's song praising the hwarang Gipa-rang, likening him to the moon and to a pine that snow cannot bend.",
    },
    {
        "ko": "처용가", "en": "The Song of Cheoyong",
        "start": "東京明期月良", "end": "奪叱良乙何如為理古",
        "gloss_ko": "처용이 아내의 자리를 범한 역신을 보고 춤추며 부른 노래.",
        "gloss_en": "Cheoyong's song, sung and danced on finding the plague spirit in his wife's bed.",
    },
    {
        "ko": "서동요", "en": "The Seodong Song",
        "start": "善化公主主隱", "end": "夜矣卯乙抱遣去如",
        "gloss_ko": "서동이 아이들에게 부르게 하여 선화공주를 얻은 노래.",
        "gloss_en": "The rhyme Seodong taught the village children to sing, and by which he won Princess Seonhwa.",
    },
]

# Classical Chinese verse -- translatable as ordinary 한문, but set as lines rather than
# prose, and pinned because both run flush into the surrounding narrative with no
# punctuation. 해가 in particular uses spaces as its only line break, so leaving it
# unpinned let the packer cut 入網捕 / 掠燔之喫 straight through the middle of a line.
HANMUN_VERSE = [
    {
        "ko": "해가", "en": "The Song of the Sea",
        "start": "龜乎龜乎出水路", "end": "入網捕掠燔之喫",
        "gloss_ko": "바닷가 사람들이 용에게 수로부인을 돌려달라며 막대로 언덕을 치면서 부른 노래.",
        "gloss_en": "The song the people beat out on the shore, demanding the dragon give Lady Suro back.",
    },
    {
        "ko": "가락국기 명(銘)", "en": "The Garak Inscription",
        "start": "元胎肇啟", "end": "規儀不傾",
        "gloss_ko": "가락국의 창건과 수로왕을 기린 사언(四言) 명문.",
        "gloss_en": "A four-character inscription celebrating the founding of Garak and King Suro.",
    },
]

HANMUN_VERSE_MARKERS = ("讚曰", "銘曰", "詞曰")
