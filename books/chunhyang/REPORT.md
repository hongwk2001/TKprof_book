# 춘향전 — overnight report

Branch `chunhyang` in TKprof_book. Workflow per chapter: Claude writes the modern
Korean (`apply_ko.py`) → gemma4:12b drafts English (`modernize.py --en-only`) →
Claude reviews every item and fixes (`apply_en.py`) → one commit.

## Progress

| Ch | Title | Sentences | EN words | EN fixed | Notes |
|---|---|---|---|---|---|
| 01 | 남원 땅의 춘향 | 110 | 2,272 | 74 (67%) | Longest chapter (~15 min); tense made consistent |
| 02 | 그네 타는 춘향 | 91 | 1,410 | 31 (34%) | |
| 03 | 광한루에서 만나다 | 56 | 935 | 21 (38%) | |
| 04 | 글이 눈에 들어오지 않는 밤 | 103 | 1,879 | 91 (88%) | 천자풀이 rewritten line by line for ESL |

**Stopped after 5 of 21 chapters: the usage limit was reached.** Remaining: 05, 06, and 08–21.
To resume: write Korean → `python apply_ko.py ch_NN <file>` → `python modernize.py ch_NN --en-only` → review → `python apply_en.py ch_NN <file>`.
Uncertain reading: ch_04 P0007, the 律 line (원문 「조가ᄉᆞ치」) is my best guess.
| 07 | 첫날밤과 사랑가 | 86 | 1,454 | 48 (56%) | Wordplay chapter; see flags below |

## Sexual content: please decide

The policy is to keep it frank like the original. These are the passages I think
might be too much. Each shows the English as it stands now.

- **ch_07 P0002–P0003 (first night).** Undressing and the struggle over clothes; he hooks
  her dress string with his toe so it slides off; "her skin is as white and beautiful as a
  piece of jade". The act itself is implied, not described: "As they roll around until
  they sweat, the hemp blanket dances, and the shiny chamber pot clinks along to the beat."
- **ch_07 P0008 (mortar).** "You will be the stone bowl of a grain mortar, and I will be the
  heavy pestle… when the mortar goes thump, thump, thump, know that it is me."
- **ch_07 P0009–P0010 (millstone).** She refuses always being "on the bottom"; then
  refuses the top millstone: "What did I ever do, to carry around one more hole for the
  rest of my life?" This is the crudest joke so far; it is kept, but it is a candidate to soften.

## Decisions I made (easy to reverse)

- The maid is **향단 / Hyangdan** in the modern Korean and the English (the woodblock prints 상단).
- Chinese allusions use Pinyin (Xi Shi, Lady Yu, Wang Zhaojun…). Long lists of them are
  shortened into "the most beautiful women in history" with a few names kept.
- The 女+子=好 character pun keeps the three characters, with "woman", "son" and
  "love/good" spelled out.
