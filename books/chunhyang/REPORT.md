# 춘향전 — translation report

Branch `chunhyang` in TKprof_book. **All 21 chapters have modern Korean and English.**
Per-chapter review files: `review/ch_NN.md` (numbered Korean/English side by side,
with the items to check at the top). Line ids like `P0003.4` are what the fix
scripts use.

## Totals

- 1,435 sentence pairs · 27,106 English words · **~3 h 01 min** at 150 wpm (target 2.5–3.5 h)
- Source: 국립중앙박물관 신수15187 scans, transcribed in-house (leaves 1–84).
  Pages 5b–6a are missing from the scans; ch_01 P0008 is an in-house bridge marked 〔 〕.

## How each chapter was made

| Ch | Title | Pairs | EN words | Method |
|---|---|---|---|---|
| 01 | 남원 땅의 춘향 | 110 | 2,061 | Korean by Claude, English gemma → reviewed (67% changed) |
| 02 | 그네 타는 춘향 | 91 | 1,445 | same (34%) |
| 03 | 광한루에서 만나다 | 56 | 940 | same (38%) |
| 04 | 글이 눈에 들어오지 않는 밤 | 103 | 1,791 | same (88%) |
| 05 | 춘향의 집을 찾아가다 | 76 | 1,218 | same (71%) |
| 06 | 백년가약 | 68 | 1,319 | same (88%) |
| 07 | 첫날밤과 사랑가 | 86 | 1,406 | same (56%) |
| 08 | 사랑 놀이 | 90 | 1,440 | both written by Claude |
| 09 | 떠나야 하는 도련님 | 58 | 1,157 | gemma → reviewed (69%) |
| 10 | 이별 | 87 | 1,634 | same (85%) |
| 11–21 | … | 662 | 11,955 | both written by Claude (`apply_pair.py`) |

From ch_11 on, gemma was dropped: its drafts were being rewritten 70–88% anyway,
mostly for misreadings, flipped negatives, dropped quotes, and puns turned into
vague stand-ins. `modernize.py` is kept if you want to compare.

## Please decide (details in each review file's "Please check" box)

**Sexual content (kept frank; flagged where I softened):**
- ch_07 first night (implied), mortar-and-pestle, millstone. P0010.2 softened.
- ch_08 palace-song pun softened; piggyback and horsey games with nudity kept;
  "ride the boat called Chunhyang", with the original's cruder line dropped.
- ch_02 P0006.5 mild (underpants on the swing).

**Crude humor softened one step:** ch_17 P0009.5 farmer's insult; ch_21 P0002.8
the magistrate "wets himself" (original: soils himself).

**Violence kept as in the original:** ch_14 the beating, ch_15 Lady Qi's ghost,
ch_19 crows and the mother's eyes.

**Readings to check:** ch_04 P0007.12 (律 line), ch_14 P0018.10 and ch_15 P0006
(ink-damaged scan, reconstructed from context).

**Choices you can reverse:** 향단 / Hyangdan (the woodblock prints 상단); Chinese
allusions in Pinyin, with long lists shortened; ch_01 is the longest at about 14 minutes.

## Not done yet

- Migrate to the app module (`Book_apps/chunhyang`) and build.
- A human read of the Korean, which was written by Claude without a second reviewer.
